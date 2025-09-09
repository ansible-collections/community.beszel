from ansible_collections.community.internal_test_tools.tests.unit.plugins.modules.utils import (
    AnsibleExitJson,
    AnsibleFailJson,
    set_module_args,
    ModuleTestCase,
)
from ansible_collections.community.beszel.plugins.module_utils import pocketbase_utils
from ansible_collections.community.beszel.plugins.modules import system
from unittest.mock import patch, MagicMock

import pytest
import types


SINGLE_SYSTEM_EXISTING = {
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
    "users": ["user-current-id"],
}


class TestSystem(ModuleTestCase):
    def setUp(self):
        super(TestSystem, self).setUp()

        # Ensure module thinks pocketbase is available
        pocketbase_utils.HAS_POCKETBASE = True
        system.HAS_POCKETBASE = True
        system.POCKETBASE_IMPORT_ERROR = None

        class _DummyClientResponseError(Exception):
            """Simulate a client response error."""

            pass

        system.ClientResponseError = _DummyClientResponseError

        # Patch PocketBaseClient inside the module under test
        self.patcher = patch(
            "ansible_collections.community.beszel.plugins.modules.system.PocketBaseClient"
        )
        self.pocketbase_client_mock = self.patcher.start()

        # Fake client and collections
        self.fake_client = MagicMock()
        self.systems_collection = MagicMock()
        self.users_collection = MagicMock()

        def collection_side_effect(name):
            if name == "users":
                return self.users_collection
            return self.systems_collection

        self.fake_client.collection.side_effect = collection_side_effect
        self.pocketbase_client_mock.return_value.authenticate.return_value = (
            self.fake_client
        )

        # Default behaviors
        self.users_collection.get_first_list_item.return_value = types.SimpleNamespace(
            id="user-current-id"
        )
        self.systems_collection.get_first_list_item.return_value = (
            types.SimpleNamespace(**SINGLE_SYSTEM_EXISTING)
        )
        self.systems_collection.update.return_value = types.SimpleNamespace(
            **{
                **SINGLE_SYSTEM_EXISTING,
                "host": "instance-updated",
                "port": 45877,
                "users": ["user-current-id"],
            }
        )
        self.systems_collection.create.return_value = types.SimpleNamespace(
            **{
                **SINGLE_SYSTEM_EXISTING,
                "id": "new-system-id",
                "name": "new-instance",
                "host": "new-host",
                "port": 45876,
                "users": ["user-current-id"],
                "status": "pending",
            }
        )

    def tearDown(self):
        self.patcher.stop()
        super(TestSystem, self).tearDown()

    def test_system_fails_with_no_arguments(self):
        with set_module_args({}):
            with pytest.raises(AnsibleFailJson):
                system.main()

    def test_system_present_requires_host(self):
        with set_module_args(
            {
                "url": "http://localhost:8090",
                "username": "units@example.com",
                "password": "testing",
                "name": "instance",
                # host omitted
                "state": "present",
            }
        ):
            with pytest.raises(AnsibleFailJson) as exc_info:
                system.main()
            assert (
                "Host is required when state is present"
                in exc_info.value.args[0]["msg"]
            )

    def test_system_present_no_change_when_same(self):
        # Parameters match existing state; expect no change
        with set_module_args(
            {
                "url": "http://localhost:8090",
                "username": "units@example.com",
                "password": "testing",
                "name": SINGLE_SYSTEM_EXISTING["name"],
                "host": SINGLE_SYSTEM_EXISTING["host"],
                "port": int(SINGLE_SYSTEM_EXISTING["port"]),
                "users": ["user-current-id"],
                "state": "present",
            }
        ):
            with pytest.raises(AnsibleExitJson) as exc_info:
                system.main()

            result = exc_info.value.args[0]
            assert result["changed"] is False
            assert result["msg"] == "System is already in the desired state."
            assert result["system"]["name"] == SINGLE_SYSTEM_EXISTING["name"]
            assert result["system"]["host"] == SINGLE_SYSTEM_EXISTING["host"]

    def test_system_present_updates_when_different(self):
        # Existing differs (host/port), expect update
        with set_module_args(
            {
                "url": "http://localhost:8090",
                "username": "units@example.com",
                "password": "testing",
                "name": SINGLE_SYSTEM_EXISTING["name"],
                "host": "instance-updated",
                "port": 45877,
                # users not provided -> resolves to current user id
                "state": "present",
            }
        ):
            with pytest.raises(AnsibleExitJson) as exc_info:
                system.main()

            result = exc_info.value.args[0]
            assert result["changed"] is True
            assert result["msg"] == "System was updated."
            assert result["system"]["host"] == "instance-updated"
            assert int(result["system"]["port"]) == 45877

    def test_system_present_creates_when_absent(self):
        # Simulate system not found
        self.systems_collection.get_first_list_item.side_effect = (
            system.ClientResponseError()
        )

        with set_module_args(
            {
                "url": "http://localhost:8090",
                "username": "units@example.com",
                "password": "testing",
                "name": "new-instance",
                "host": "new-host",
                "port": 45876,
                "state": "present",
            }
        ):
            with pytest.raises(AnsibleExitJson) as exc_info:
                system.main()

            result = exc_info.value.args[0]
            assert result["changed"] is True
            assert result["msg"] == "System was created."
            assert result["system"]["name"] == "new-instance"
            assert result["system"]["host"] == "new-host"
            assert result["system"]["status"] in ["pending", "up"]

    def test_system_present_creates_when_absent_check_mode(self):
        # Simulate system not found so it creates a new one
        self.systems_collection.get_first_list_item.side_effect = (
            system.ClientResponseError()
        )

        with set_module_args(
            {
                "_ansible_check_mode": True,
                "url": "http://localhost:8090",
                "username": "units@example.com",
                "password": "testing",
                "name": "new-instance",
                "host": "new-host",
                "port": 45876,
                "state": "present",
            }
        ):
            with pytest.raises(AnsibleExitJson) as exc_info:
                system.main()

            result = exc_info.value.args[0]
            assert result["changed"] is True
            assert result["msg"] == "System would be created."
            assert result["system"]["name"] == "new-instance"
            assert result["system"]["host"] == "new-host"
            assert result["system"]["status"] == "pending"

    def test_system_absent_deletes_when_exists(self):
        with set_module_args(
            {
                "url": "http://localhost:8090",
                "username": "units@example.com",
                "password": "testing",
                "name": SINGLE_SYSTEM_EXISTING["name"],
                "state": "absent",
            }
        ):
            with pytest.raises(AnsibleExitJson) as exc_info:
                system.main()

            result = exc_info.value.args[0]
            assert result["changed"] is True
            assert result["system"]["id"] == SINGLE_SYSTEM_EXISTING["id"]
            assert result["msg"] == "System was deleted."
            self.systems_collection.delete.assert_called_once()

    def test_system_absent_deletes_when_exists_check_mode(self):
        with set_module_args(
            {
                "_ansible_check_mode": True,
                "url": "http://localhost:8090",
                "username": "units@example.com",
                "password": "testing",
                "name": SINGLE_SYSTEM_EXISTING["name"],
                "state": "absent",
            }
        ):
            with pytest.raises(AnsibleExitJson) as exc_info:
                system.main()

            result = exc_info.value.args[0]
            assert result["changed"] is True
            assert result["system"]["id"] == SINGLE_SYSTEM_EXISTING["id"]
            assert result["msg"] == "System would be deleted."
            self.systems_collection.delete.assert_not_called()

    def test_system_absent_noop_when_not_exists(self):
        # Simulate system not found so it does nothing
        self.systems_collection.get_first_list_item.side_effect = (
            system.ClientResponseError()
        )

        with set_module_args(
            {
                "url": "http://localhost:8090",
                "username": "units@example.com",
                "password": "testing",
                "name": "missing",
                "state": "absent",
            }
        ):
            with pytest.raises(AnsibleExitJson) as exc_info:
                system.main()

            result = exc_info.value.args[0]
            assert result["changed"] is False
            assert result["msg"] == "System does not exist. Nothing to remove."

    def test_system_authentication_failure(self):
        # Make authenticate raise an exception
        self.pocketbase_client_mock.return_value.authenticate.side_effect = Exception(
            "auth failed"
        )

        with set_module_args(
            {
                "url": "http://localhost:8090",
                "username": "units@example.com",
                "password": "testing",
                "name": "instance",
                "state": "present",
                "host": "x",
            }
        ):
            with pytest.raises(AnsibleFailJson) as exc_info:
                system.main()
            assert "auth failed" in exc_info.value.args[0]["msg"]
