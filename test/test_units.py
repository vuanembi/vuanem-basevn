import pytest

from basevn.basevn_controller import basevn_controller
from basevn.basevn_service import pipelines, pipeline_service
from tasks import tasks_service


class TestPipeline:
    @pytest.fixture(
        ids=pipelines.keys(),
        params=pipelines.values(),
    )
    def resource(self, request):
        return request.param

    def test_service(self, resource):
        res = pipeline_service(resource)
        assert res['num_processed'] > 0

    def test_controller(self, resource):
        res = basevn_controller(
            {
                "table": resource.name,
            }
        )
        res


def test_tasks():
    res = tasks_service()
    res
