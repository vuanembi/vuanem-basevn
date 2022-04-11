from typing import Callable, Any
import os

import requests
from compose import compose

from basevn.interface import Service

_GetFn = Callable[[dict[str, Any], int], list[dict]]
GetFn = Callable[[requests.Session], _GetFn]

WORKFLOW = Service("https://workflow.base.vn/extapi/v1", os.getenv("WORKFLOW_TOKEN"))
WEWORK = Service("https://wework.base.vn/extapi/v3", os.getenv("WEWORK_TOKEN"))


def get_single(
    service: Service,
    uri: str,
    page_fn: Callable[[int], dict[str, Any]],
    res_fn: Callable[[dict[str, Any]], list[dict[str, Any]]],
) -> GetFn:
    def _get(session):
        def __get(body: dict[str, Any] = {}, page: int = 0) -> list[dict]:
            with session.post(
                f"{service.base_url}/{uri}",
                data={
                    **body,
                    **page_fn(page),
                    "access_token": service.token,
                },
            ) as r:
                res = r.json()
            data = res_fn(res)
            return data + __get(body, page + 1) if data else []

        return __get

    return _get


def get_multiple(
    get_listing_fn: GetFn,
    get_one_fn: GetFn,
    id_fn: Callable[[dict[str, Any]], Any],
    res_fn: Callable[[list[dict[str, Any]]], list[dict[str, Any]]] = lambda x: x,
    body_fn: Callable[[dict[str, Any]], Any] = lambda _: {},
):
    def _get(session: requests.Session):
        def __get():
            return [
                i
                for j in [
                    compose(
                        res_fn,
                        get_one_fn(session),
                        body_fn,
                        id_fn,
                    )(id)
                    for id in get_listing_fn(session)()  # type: ignore
                ]
                for i in j
            ]

        return __get

    return _get
