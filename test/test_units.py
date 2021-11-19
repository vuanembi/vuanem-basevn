from unittest.mock import Mock

import pytest

from main import main
from controller.tasks import TABLES


def run(data):
    return main(Mock(get_json=Mock(return_value=data), args=data))


@pytest.mark.parametrize(
    "data",
    TABLES,
    ids=[f"{i['resource']} || {i['table']}" for i in TABLES],
)
def test_pipelines(data):
    res = run(data)["results"]
    assert res["num_processed"] >= 0
    if res["num_processed"] > 0:
        assert res["num_processed"] == res["output_rows"]


def test_tasks():
    res = run(
        {
            "tasks": "basevn",
        }
    )
    assert res["tasks"] > 0
