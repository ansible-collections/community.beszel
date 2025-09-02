from unittest.mock import Mock, patch
import pytest
from types import SimpleNamespace

from ansible_collections.community.beszel.plugins.modules import system_info
from ansible_collections.community.internal_test_tools.tests.unit.plugins.modules.utils import (
    AnsibleExitJson,
    ModuleTestCase,
    set_module_args,
)


@pytest.fixture
def mock_pocketbase_client(request):
    with patch(
        "ansible_collections.community.beszel.plugins.modules.system_info.PocketBaseClient"
    ) as MockPB:
        fake_client = Mock()
        MockPB.return_value.authenticate.return_value = fake_client
        if getattr(request, "instance", None) is not None:
            setattr(request.instance, "fake_pb_client", fake_client)
        yield fake_client


@pytest.mark.usefixtures("mock_pocketbase_client")
class TestSystemInfo(ModuleTestCase):
    def setUp(self):
        super(TestSystemInfo, self).setUp()
        self.module = system_info

    def test_system_info_named_success(self):
        set_module_args(
            {
                "url": "http://localhost:8090",
                "username": "admin",
                "password": "admin",
                "name": "example_system",
            }
        )

        systems_coll = Mock()
        self.fake_pb_client.collection.return_value = systems_coll
        systems_coll.get_first_list_item.return_value = SimpleNamespace(
            id="q1", name="example_system"
        )

        with pytest.raises(AnsibleExitJson) as exc:
            system_info.main()

        result = exc.value.args[0]
        assert result["changed"] is False
        assert result["systems"] == [{"id": "q1", "name": "example_system"}]

    def test_system_info_all_success(self):
        set_module_args(
            {
                "url": "http://localhost:8090",
                "username": "admin",
                "password": "admin",
            }
        )

        systems_coll = Mock()
        self.fake_pb_client.collection.return_value = systems_coll
        systems_coll.get_full_list.return_value = [
            SimpleNamespace(id="a1", name="one"),
            SimpleNamespace(id="b2", name="two"),
        ]

        with pytest.raises(AnsibleExitJson) as exc:
            system_info.main()

        result = exc.value.args[0]
        assert result["changed"] is False
        assert result["systems"] == [
            {"id": "a1", "name": "one"},
            {"id": "b2", "name": "two"},
        ]
