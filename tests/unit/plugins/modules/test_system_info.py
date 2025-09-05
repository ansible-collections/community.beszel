from ansible_collections.community.internal_test_tools.tests.unit.plugins.modules.utils import (
    AnsibleExitJson,
    AnsibleFailJson,
    set_module_args,
    ModuleTestCase,
)
from ansible_collections.community.beszel.plugins.module_utils import pocketbase_utils
from ansible_collections.community.beszel.plugins.modules import system_info
from unittest.mock import patch, MagicMock

import pytest
import types

SINGLE_SYSTEM_RESPONSE = {
    "collection_id": "2hz5ncl8tizk5nx",
    "collection_name": "systems",
    "created": "2025-08-30T07:48:04",
    "expand": {},
    "host": "instance",
    "id": "q5y5h742bwueyns",
    "info": {
        "b": 0,
        "bb": 40,
        "c": 10,
        "cpu": 0.06,
        "dp": 4.09,
        "h": "90ba6044d626",
        "k": "6.15.11-orbstack-00539-g9885ebd8e3f4",
        "la": [0, 0, 0],
        "m": "",
        "mp": 2.07,
        "os": 0,
        "t": 10,
        "u": 29081,
        "v": "0.12.6",
    },
    "name": "instance",
    "port": "45876",
    "status": "up",
    "updated": "2025-08-30T11:08:36",
    "users": ["zsk3bb1p2uisg4g"],
}

MULTIPLE_SYSTEM_RESPONSE = [
    SINGLE_SYSTEM_RESPONSE,
    {
        "collection_id": "2hz5ncl8tizk5nx",
        "collection_name": "systems",
        "created": "2025-08-30T07:48:04",
        "expand": {},
        "host": "instance1",
        "id": "q5y5h742bwugyns",
        "info": {
            "b": 0,
            "bb": 40,
            "c": 10,
            "cpu": 0.06,
            "dp": 4.09,
            "h": "90ba6044d626",
            "k": "6.15.11-orbstack-00539-g9885ebd8e3f4",
            "la": [0, 0, 0],
            "m": "",
            "mp": 2.07,
            "os": 0,
            "t": 10,
            "u": 29081,
            "v": "0.12.6",
        },
        "name": "instance1",
        "port": "45877",
        "status": "up",
        "updated": "2025-08-30T11:08:36",
        "users": ["zsk3bb1p2uisg4g"],
    },
]


class TestSystemInfo(ModuleTestCase):
    def setUp(self):
        super(TestSystemInfo, self).setUp()
        pocketbase_utils.HAS_POCKETBASE = True
        # self.module = system_info
        self.patcher = patch(
            "ansible_collections.community.beszel.plugins.modules.system_info.PocketBaseClient"
        )
        self.pocketbase_client_mock = self.patcher.start()

        self.fake_client = MagicMock()
        self.fake_collection = MagicMock()
        self.fake_client.collection.return_value = self.fake_collection
        self.pocketbase_client_mock.return_value.authenticate.return_value = (
            self.fake_client
        )

        self.fake_collection.get_first_list_item.return_value = types.SimpleNamespace(
            **SINGLE_SYSTEM_RESPONSE
        )
        self.fake_collection.get_full_list.return_value = [
            types.SimpleNamespace(**record) for record in MULTIPLE_SYSTEM_RESPONSE
        ]

    def tearDown(self):
        self.patcher.stop()
        super(TestSystemInfo, self).tearDown()

    def test_system_info_fails_with_no_arguments(self):
        with set_module_args({}):
            with pytest.raises(AnsibleFailJson):
                system_info.main()

    def test_system_info_returns_one_system_given_name(self):
        with set_module_args(
            {
                "url": "http://localhost:8090",
                "username": "units@example.com",
                "password": "testing",
                "name": "example_system",
            }
        ):
            with pytest.raises(AnsibleExitJson) as exc_info:
                system_info.main()

            result = exc_info.value.args[0]
            assert result["changed"] is False
            assert len(result["systems"]) == 1
            assert result["systems"][0]["name"] == SINGLE_SYSTEM_RESPONSE["name"]
            assert result["systems"][0]["host"] == SINGLE_SYSTEM_RESPONSE["host"]

    def test_system_info_returns_two_systems_with_no_name(self):
        with set_module_args(
            {
                "url": "http://localhost:8090",
                "username": "units@example.com",
                "password": "testing",
            }
        ):
            with pytest.raises(AnsibleExitJson) as exc_info:
                system_info.main()

            result = exc_info.value.args[0]
            assert result["changed"] is False
            assert len(result["systems"]) == 2
            assert result["systems"][0]["name"] == MULTIPLE_SYSTEM_RESPONSE[0]["name"]
            assert result["systems"][0]["host"] == MULTIPLE_SYSTEM_RESPONSE[0]["host"]
            assert result["systems"][1]["name"] == MULTIPLE_SYSTEM_RESPONSE[1]["name"]
            assert result["systems"][1]["host"] == MULTIPLE_SYSTEM_RESPONSE[1]["host"]
