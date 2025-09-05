import json
import pytest
from types import SimpleNamespace
from unittest.mock import patch

from ansible.module_utils import basic
from ansible.module_utils.common.text.converters import to_bytes


class AnsibleExitJson(Exception):
    pass


class AnsibleFailJson(Exception):
    pass


def set_module_args(args):
    basic._ANSIBLE_ARGS = to_bytes(json.dumps({"ANSIBLE_MODULE_ARGS": args}))


def exit_json(*args, **kwargs):
    raise AnsibleExitJson(kwargs)


def fail_json(*args, **kwargs):
    raise AnsibleFailJson(kwargs)


class FakeCollection:
    def __init__(self, record):
        self.record = record
        self.last_filter = None

    def get_first_list_item(self, filter):
        self.last_filter = filter
        return SimpleNamespace(**self.record)


class FakeClient:
    def __init__(self, record):
        self._record = record

    def collection(self, name):
        assert name == "systems"
        return FakeCollection(self._record)


class FakePocketBaseClient:
    def __init__(self, url, username, password, timeout=120):
        self.url = url
        self.username = username
        self.password = password
        self.timeout = timeout

    def authenticate(self):
        record = {
            "id": "abc123",
            "name": "instance",
            "status": "up",
        }
        return FakeClient(record)


def test_returns_single_system_when_name_provided(monkeypatch):
    # Patch AnsibleModule handlers
    monkeypatch.setattr(basic.AnsibleModule, "exit_json", exit_json)
    monkeypatch.setattr(basic.AnsibleModule, "fail_json", fail_json)

    from ansible_collections.community.beszel.plugins.modules import (
        system_info as mod,
    )

    # Patch PocketBaseClient used by the module to avoid real dependency
    monkeypatch.setattr(mod, "PocketBaseClient", FakePocketBaseClient)

    set_module_args(
        {
            "url": "http://localhost:8090",
            "username": "admin@example.com",
            "password": "admin",
            "name": "instance",
        }
    )

    with pytest.raises(AnsibleExitJson) as exc:
        mod.main()

    result = exc.value.args[0]

    assert result["changed"] is False
    assert "systems" in result
    assert isinstance(result["systems"], list)
    assert len(result["systems"]) == 1
    assert result["systems"][0]["name"] == "instance"


class FakeCollectionAll:
    def __init__(self, records):
        self.records = records

    def get_full_list(self, query_params=None):
        return [SimpleNamespace(**r) for r in self.records]


class FakeClientAll:
    def __init__(self, records):
        self._records = records

    def collection(self, name):
        assert name == "systems"
        return FakeCollectionAll(self._records)


class FakePocketBaseClientAll:
    def __init__(self, url, username, password, timeout=120):
        self.url = url
        self.username = username
        self.password = password
        self.timeout = timeout

    def authenticate(self):
        records = [
            {"id": "id1", "name": "instance1", "status": "up"},
            {"id": "id2", "name": "instance2", "status": "down"},
        ]
        return FakeClientAll(records)


def test_returns_two_systems_when_no_name_provided(monkeypatch):
    monkeypatch.setattr(basic.AnsibleModule, "exit_json", exit_json)
    monkeypatch.setattr(basic.AnsibleModule, "fail_json", fail_json)

    from ansible_collections.community.beszel.plugins.modules import (
        system_info as mod,
    )

    monkeypatch.setattr(mod, "PocketBaseClient", FakePocketBaseClientAll)

    set_module_args(
        {
            "url": "http://localhost:8090",
            "username": "admin@example.com",
            "password": "admin",
        }
    )

    with pytest.raises(AnsibleExitJson) as exc:
        mod.main()

    result = exc.value.args[0]

    assert result["changed"] is False
    assert "systems" in result
    assert isinstance(result["systems"], list)
    assert len(result["systems"]) == 2
    names = {s["name"] for s in result["systems"]}
    assert names == {"instance1", "instance2"}


class FakePocketBaseClientAuthError:
    def __init__(self, url, username, password, timeout=120):
        self.url = url
        self.username = username
        self.password = password
        self.timeout = timeout

    def authenticate(self):
        raise Exception("Authentication failed: invalid credentials")


def test_authentication_failure(monkeypatch):
    monkeypatch.setattr(basic.AnsibleModule, "exit_json", exit_json)
    monkeypatch.setattr(basic.AnsibleModule, "fail_json", fail_json)

    from ansible_collections.community.beszel.plugins.modules import (
        system_info as mod,
    )

    # Force authentication to fail
    monkeypatch.setattr(mod, "PocketBaseClient", FakePocketBaseClientAuthError)

    set_module_args(
        {
            "url": "http://localhost:8090",
            "username": "admin@example.com",
            "password": "wrong",
            # name omitted intentionally; failure happens before any query
        }
    )

    with pytest.raises(AnsibleFailJson) as exc:
        mod.main()

    result = exc.value.args[0]
    assert "msg" in result
    assert "Authentication failed" in result["msg"]


def test_missing_pocketbase_dependency(monkeypatch):
    monkeypatch.setattr(basic.AnsibleModule, "exit_json", exit_json)
    monkeypatch.setattr(basic.AnsibleModule, "fail_json", fail_json)

    from ansible_collections.community.beszel.plugins.modules import (
        system_info as mod,
    )

    # Simulate missing pocketbase dependency
    monkeypatch.setattr(mod, "HAS_POCKETBASE", False)
    monkeypatch.setattr(mod, "POCKETBASE_IMPORT_ERROR", "import error: pocketbase")

    set_module_args(
        {
            "url": "http://localhost:8090",
            "username": "admin@example.com",
            "password": "admin",
        }
    )

    with pytest.raises(AnsibleFailJson) as exc:
        mod.main()

    result = exc.value.args[0]
    assert "msg" in result
    assert "pocketbase" in result["msg"].lower()
    assert "exception" in result
    assert "pocketbase" in result["exception"].lower()
