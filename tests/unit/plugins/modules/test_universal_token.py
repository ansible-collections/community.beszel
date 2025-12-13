from ansible_collections.community.internal_test_tools.tests.unit.plugins.modules.utils import (
    AnsibleExitJson,
    AnsibleFailJson,
    set_module_args,
    ModuleTestCase,
)
from ansible_collections.community.beszel.plugins.module_utils import pocketbase_utils
from ansible_collections.community.beszel.plugins.modules import universal_token
from unittest.mock import patch, MagicMock

import pytest


UNIVERSAL_TOKEN_ENABLED = {
    "token": "ca995e6d-a8d1-416f-b77d-ea2d297060ae",
    "active": True,
}

UNIVERSAL_TOKEN_DISABLED = {
    "token": "ca995e6d-a8d1-416f-b77d-ea2d297060ae",
    "active": False,
}


class TestUniversalToken(ModuleTestCase):
    def setUp(self):
        super(TestUniversalToken, self).setUp()

        # Ensure module thinks pocketbase is available
        pocketbase_utils.HAS_POCKETBASE = True
        universal_token.HAS_POCKETBASE = True
        universal_token.POCKETBASE_IMPORT_ERROR = None

        # Patch PocketBaseClient inside the module under test
        self.patcher = patch(
            "ansible_collections.community.beszel.plugins.modules.universal_token.PocketBaseClient"
        )
        self.pocketbase_client_mock = self.patcher.start()

        # Fake client
        self.fake_client = MagicMock()
        self.fake_response = MagicMock()

        # Setup default response for getting current state
        self.fake_response.json.return_value = UNIVERSAL_TOKEN_ENABLED
        self.fake_client._send.return_value = self.fake_response

        # Setup authenticate_user to return the fake client
        self.pocketbase_client_mock.return_value.authenticate_user.return_value = (
            self.fake_client
        )

    def tearDown(self):
        self.patcher.stop()
        super(TestUniversalToken, self).tearDown()

    def test_universal_token_fails_with_no_arguments(self):
        with set_module_args({}):
            with pytest.raises(AnsibleFailJson):
                universal_token.main()

    def test_universal_token_no_change_when_already_enabled(self):
        # Token is already enabled, desired state is enabled
        self.fake_response.json.return_value = UNIVERSAL_TOKEN_ENABLED

        with set_module_args(
            {
                "url": "http://localhost:8090",
                "username": "units@example.com",
                "password": "testing",
                "state": "enabled",
            }
        ):
            with pytest.raises(AnsibleExitJson) as exc_info:
                universal_token.main()

            result = exc_info.value.args[0]
            assert result["changed"] is False
            assert result["universal_token"]["active"] is True
            assert (
                result["universal_token"]["token"] == UNIVERSAL_TOKEN_ENABLED["token"]
            )
            # Should only call _send once to get current state
            assert self.fake_client._send.call_count == 1
            self.fake_client._send.assert_called_with("/api/beszel/universal-token", {})

    def test_universal_token_no_change_when_already_disabled(self):
        # Token is already disabled, desired state is disabled
        self.fake_response.json.return_value = UNIVERSAL_TOKEN_DISABLED

        with set_module_args(
            {
                "url": "http://localhost:8090",
                "username": "units@example.com",
                "password": "testing",
                "state": "disabled",
            }
        ):
            with pytest.raises(AnsibleExitJson) as exc_info:
                universal_token.main()

            result = exc_info.value.args[0]
            assert result["changed"] is False
            assert result["universal_token"]["active"] is False
            assert (
                result["universal_token"]["token"] == UNIVERSAL_TOKEN_DISABLED["token"]
            )
            # Should only call _send once to get current state
            assert self.fake_client._send.call_count == 1

    def test_universal_token_enables_when_disabled(self):
        # Token is disabled, desired state is enabled
        # First call returns disabled state, second call returns enabled state
        self.fake_client._send.side_effect = [
            MagicMock(json=lambda: UNIVERSAL_TOKEN_DISABLED),
            MagicMock(json=lambda: UNIVERSAL_TOKEN_ENABLED),
        ]

        with set_module_args(
            {
                "url": "http://localhost:8090",
                "username": "units@example.com",
                "password": "testing",
                "state": "enabled",
            }
        ):
            with pytest.raises(AnsibleExitJson) as exc_info:
                universal_token.main()

            result = exc_info.value.args[0]
            assert result["changed"] is True
            assert result["universal_token"]["active"] is True
            assert (
                result["universal_token"]["token"] == UNIVERSAL_TOKEN_ENABLED["token"]
            )
            # Should call _send twice: once to get state, once to enable
            assert self.fake_client._send.call_count == 2
            # Verify the enable call
            self.fake_client._send.assert_any_call(
                "/api/beszel/universal-token?enable=1", {}
            )

    def test_universal_token_disables_when_enabled(self):
        # Token is enabled, desired state is disabled
        # First call returns enabled state, second call returns disabled state
        self.fake_client._send.side_effect = [
            MagicMock(json=lambda: UNIVERSAL_TOKEN_ENABLED),
            MagicMock(json=lambda: UNIVERSAL_TOKEN_DISABLED),
        ]

        with set_module_args(
            {
                "url": "http://localhost:8090",
                "username": "units@example.com",
                "password": "testing",
                "state": "disabled",
            }
        ):
            with pytest.raises(AnsibleExitJson) as exc_info:
                universal_token.main()

            result = exc_info.value.args[0]
            assert result["changed"] is True
            assert result["universal_token"]["active"] is False
            assert (
                result["universal_token"]["token"] == UNIVERSAL_TOKEN_DISABLED["token"]
            )
            # Should call _send twice: once to get state, once to disable
            assert self.fake_client._send.call_count == 2
            # Verify the disable call includes the token
            expected_url = (
                f"/api/beszel/universal-token?enable=0"
                f"&token={UNIVERSAL_TOKEN_ENABLED['token']}"
            )
            self.fake_client._send.assert_any_call(expected_url, {})

    def test_universal_token_authentication_failure(self):
        # Make authenticate_user raise an exception
        self.pocketbase_client_mock.return_value.authenticate_user.side_effect = (
            Exception("Authentication failed")
        )

        with set_module_args(
            {
                "url": "http://localhost:8090",
                "username": "units@example.com",
                "password": "testing",
                "state": "enabled",
            }
        ):
            with pytest.raises(AnsibleFailJson) as exc_info:
                universal_token.main()
            assert "Authentication failed" in exc_info.value.args[0]["msg"]

    def test_universal_token_get_state_failure(self):
        # Make _send raise an exception when getting current state
        self.fake_client._send.side_effect = Exception("API error")

        with set_module_args(
            {
                "url": "http://localhost:8090",
                "username": "units@example.com",
                "password": "testing",
                "state": "enabled",
            }
        ):
            with pytest.raises(AnsibleFailJson) as exc_info:
                universal_token.main()
            assert "API error" in exc_info.value.args[0]["msg"]

    def test_universal_token_update_failure(self):
        # Token is disabled, desired state is enabled, but update fails
        self.fake_client._send.side_effect = [
            MagicMock(json=lambda: UNIVERSAL_TOKEN_DISABLED),
            Exception("Update failed"),
        ]

        with set_module_args(
            {
                "url": "http://localhost:8090",
                "username": "units@example.com",
                "password": "testing",
                "state": "enabled",
            }
        ):
            with pytest.raises(AnsibleFailJson) as exc_info:
                universal_token.main()
            assert "Update failed" in exc_info.value.args[0]["msg"]

    def test_universal_token_with_timeout(self):
        # Test that timeout parameter is passed correctly
        self.fake_response.json.return_value = UNIVERSAL_TOKEN_ENABLED

        with set_module_args(
            {
                "url": "http://localhost:8090",
                "username": "units@example.com",
                "password": "testing",
                "timeout": 60.0,
                "state": "enabled",
            }
        ):
            with pytest.raises(AnsibleExitJson):
                universal_token.main()

            # Verify PocketBaseClient was called with timeout
            self.pocketbase_client_mock.assert_called_once_with(
                url="http://localhost:8090",
                username="units@example.com",
                password="testing",
                timeout=60.0,
            )
