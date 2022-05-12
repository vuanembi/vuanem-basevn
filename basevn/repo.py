from typing import Callable, Any
import os
import asyncio

import httpx
from compose import compose

from basevn.pipeline.interface import Service, GetFn

ACCOUNT = Service(
    "https://account.base.vn/extapi/v1",
    os.getenv("ACCOUNT_TOKEN", ""),
)
WORKFLOW = Service(
    "https://workflow.base.vn/extapi/v1",
    os.getenv("WORKFLOW_TOKEN", ""),
)
WEWORK = Service(
    "https://wework.base.vn/extapi/v3",
    os.getenv("WEWORK_TOKEN", ""),
)
EHIRING = Service(
    "https://hiring.base.vn/publicapi/v2/",
    os.getenv("EHIRING_TOKEN", ""),
)


def get_single(
    service: Service,
    uri: str,
    res_fn: Callable[[dict[str, Any]], Any] = lambda x: x,
    page_fn: Callable[[int], dict[str, Any]] = lambda _: {},
    page_start: int = 0,
):
    def _get(client: httpx.AsyncClient):
        async def __get(
            body: dict[str, Any] = {},
            page: int = page_start,
        ) -> list[dict]:
            payload = {
                **body,
                **page_fn(page),
                "access_token": service.token,
            }
            r = await client.post(
                f"{service.base_url}/{uri}",
                data=payload,
            )
            res = r.json()
            data = res_fn(res)
            return (
                data + await __get(body, page + 1)
                if data and page_fn(page) != {}
                else data
            )

        return __get

    return _get


def get_multiple(
    get_listing_fn: GetFn,
    get_one_fn: GetFn,
    id_fn: Callable[[dict[str, Any]], Any],
    res_fn: Callable[[list[dict[str, Any]]], list[dict[str, Any]]] = lambda x: x,
    body_fn: Callable[[dict[str, Any]], Any] = lambda _: {},
):
    def _get(client: httpx.AsyncClient):
        async def __get():
            ids = [
                compose(
                    body_fn,
                    id_fn,
                )(id)
                for id in await get_listing_fn(client)()
            ]
            tasks = [asyncio.create_task(get_one_fn(client)(id)) for id in ids]
            results = await asyncio.gather(*tasks)
            return [i for j in results for i in res_fn(j)]

        return __get

    return _get
