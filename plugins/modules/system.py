#!/usr/bin/python

# Copyright: (c) 2025, Daniel Brennand <contact@danielbrennand.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: system

short_description: Manage Beszel systems.

version_added: "0.3.0"

description: Create, update and delete Beszel systems.

options:
    url:
        description: URL of the Beszel hub.
        required: true
        type: str
    username:
        description: Username used to authenticate to Beszel hub.
        required: true
        type: str
    password:
        description: Password used to authenticate to Beszel hub.
        required: true
        type: str
    timeout:
        description: Number of seconds to wait for the Beszel hub to respond.
        required: false
        type: float
        default: 120
    name:
        description: Name of the Beszel system.
        required: true
        type: str
    host:
        description:
            - IP address, FQDN or hostname of the Beszel system.
            - Required when state is present.
        required: false
        type: str
    port:
        description: Port of the Beszel system.
        required: false
        default: 45876
        type: int
    users:
        description:
            - List of users to add to the Beszel system.
            - If not provided, the current user specified in the username option will be added to the system.
        required: false
        type: list
        elements: str
    state:
        description: State of the Beszel system.
        required: false
        default: present
        type: str
        choices: [present, absent]
author:
    - Daniel Brennand (@dbrennand)
"""

EXAMPLES = r"""
- name: Register a Beszel system
  community.beszel.system:
    url: https://beszel.example.tld
    username: admin@example.com
    password: admin
    name: instance
    host: instance
    port: 45876
    state: present

- name: Modify an existing Beszel system
  community.beszel.system:
    url: https://beszel.example.tld
    username: admin@example.com
    password: admin
    name: instance
    host: instance
    port: 45877
    state: present

- name: Unregister a Beszel system
  community.beszel.system:
    url: https://beszel.example.tld
    username: admin@example.com
    password: admin
    name: instance
    state: absent
"""

RETURN = r"""
changed:
    description: Whether the Beszel system was changed.
    type: bool
    returned: always
msg:
    description: Message indicating the result of the operation.
    type: str
    returned: always
system:
    description:
        - Information about the Beszel system.
        - When state is absent and the system does not exist, the system will be returned as an empty dictionary.
    type: dict
    returned: always
    sample: {
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
                "la": [
                    0,
                    0,
                    0
                ],
                "m": "",
                "mp": 2.07,
                "os": 0,
                "t": 10,
                "u": 29081,
                "v": "0.12.6"
            },
            "name": "instance",
            "port": "45876",
            "status": "up",
            "updated": "2025-08-30T11:08:36",
            "users": [
                "zsk3bb1p2uisg4g"
            ]
        }
"""

import traceback

try:
    from ansible_collections.community.beszel.plugins.module_utils.pocketbase_utils import (
        PocketBaseClient,
    )
    from pocketbase.errors import ClientResponseError

    HAS_POCKETBASE = True
    POCKETBASE_IMPORT_ERROR = None
except ImportError:
    HAS_POCKETBASE = False
    POCKETBASE_IMPORT_ERROR = traceback.format_exc()

from typing import Union
from datetime import datetime
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import missing_required_lib


def run_module():
    def get_existing_system(
        module: AnsibleModule, client: PocketBaseClient, name: str
    ) -> Union[dict, None]:
        """Get the existing system given the name.

        Args:
            module (AnsibleModule): The Ansible module instance.
            client (PocketBaseClient): The PocketBaseClient instance.
            name (str): The name of the system to get.

        Returns:
            Union[dict, None]: The existing system if it exists, otherwise None.
        """
        try:
            return (
                client.collection("systems")
                .get_first_list_item(filter=f"name='{name}'")
                .__dict__
            )
        except ClientResponseError:
            return None
        except Exception as e:
            module.fail_json(
                msg=f"Failed to get existing system with name '{name}': {e}"
            )

    module_args = dict(
        url=dict(type="str", required=True),
        username=dict(type="str", required=True),
        password=dict(type="str", required=True, no_log=True),
        timeout=dict(type="float", required=False, default=120),
        name=dict(type="str", required=True),
        host=dict(type="str", required=False),
        port=dict(type="int", required=False, default=45876),
        users=dict(type="list", required=False, elements="str"),
        state=dict(
            type="str", required=False, default="present", choices=["present", "absent"]
        ),
    )

    result = dict(changed=False, msg="", system={})

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    if not HAS_POCKETBASE:
        module.fail_json(
            msg=missing_required_lib("pocketbase"), exception=POCKETBASE_IMPORT_ERROR
        )

    try:
        client = PocketBaseClient(
            url=module.params["url"],
            username=module.params["username"],
            password=module.params["password"],
            timeout=module.params["timeout"],
        ).authenticate()
    except Exception as e:
        module.fail_json(msg=str(e))

    if module.params["state"] == "present":
        if module.params["host"] is None:
            module.fail_json(msg="Host is required when state is present.")

        # Attempt to get the existing system (if it exists)
        existing_system = get_existing_system(module, client, module.params["name"])

        # If we have a list of users, then we need to get the IDs of the users
        if module.params["users"] is not None:
            user_ids = []
            for user in module.params["users"]:
                try:
                    user_ids.append(
                        client.collection("users")
                        .get_first_list_item(filter=f"email='{user}'")
                        .id
                    )
                except Exception as e:
                    module.fail_json(msg=f"Failed to get ID of user '{user}': {e}")
        else:
            # Get the ID of the current user
            try:
                user_ids = [
                    client.collection("users")
                    .get_first_list_item(filter=f"email='{module.params['username']}'")
                    .id
                ]
            except Exception as e:
                module.fail_json(
                    msg=f"Failed to get ID of current user '{module.params['username']}': {e}"
                )

        # If we have an existing system, then we need to determine if the
        # new config is different from the existing config
        if existing_system is not None:
            if (
                existing_system["host"] != module.params["host"]
                or int(existing_system["port"]) != module.params["port"]
                or existing_system["users"] != user_ids
            ):
                # We need to update the system
                if module.check_mode:
                    # In check mode, simulate what the update would look like
                    simulated_system = existing_system.copy()
                    simulated_system.update(
                        {
                            "host": module.params["host"],
                            "port": module.params["port"],
                            "users": user_ids,
                        }
                    )
                    result["system"] = simulated_system
                    result["changed"] = True
                    result["msg"] = "System would be updated."
                else:
                    try:
                        data = client.collection("systems").update(
                            id=existing_system["id"],
                            body_params={
                                "host": module.params["host"],
                                "port": module.params["port"],
                                "users": user_ids,
                            },
                        )
                        result["system"] = data.__dict__
                        result["changed"] = True
                        result["msg"] = "System was updated."
                    except Exception as e:
                        module.fail_json(
                            msg=f"Failed to update system '{module.params['name']}': {e}"
                        )
            else:
                # The system is already in the desired state
                result["system"] = existing_system
                result["changed"] = False
                result["msg"] = "System is already in the desired state."
        else:
            # We need to create a new system
            if module.check_mode:
                # In check mode, simulate what the new system would look like
                simulated_system = {
                    "collection_id": "2hz5ncl8tizk5nx",
                    "collection_name": "systems",
                    "created": datetime.now().isoformat()[:19],
                    "expand": {},
                    "host": module.params["host"],
                    "id": "zh6pbqnwwjx0lxv",
                    "info": {
                        "b": 0,
                        "bb": 0,
                        "c": 0,
                        "cpu": 0,
                        "dp": 0,
                        "h": "",
                        "la": [0, 0, 0],
                        "m": "",
                        "mp": 0,
                        "os": 0,
                        "u": 0,
                        "v": "",
                    },
                    "name": module.params["name"],
                    "port": module.params["port"],
                    "status": "pending",
                    "updated": datetime.now().isoformat()[:19],
                    "users": user_ids,
                }
                result["system"] = simulated_system
                result["changed"] = True
                result["msg"] = "System would be created."
            else:
                try:
                    data = client.collection("systems").create(
                        body_params={
                            "name": module.params["name"],
                            "host": module.params["host"],
                            "port": module.params["port"],
                            "users": user_ids,
                        }
                    )
                    result["system"] = data.__dict__
                    result["changed"] = True
                    result["msg"] = "System was created."
                except Exception as e:
                    module.fail_json(
                        msg=f"Failed to create system '{module.params['name']}': {e}"
                    )

    elif module.params["state"] == "absent":
        existing_system = get_existing_system(module, client, module.params["name"])
        if existing_system is None:
            # The system does not exist, so we don't need to do anything
            result["changed"] = False
            result["msg"] = "System does not exist. Nothing to remove."
        else:
            # We need to delete the system
            if module.check_mode:
                # In check mode, show what would be deleted
                result["changed"] = True
                result["system"] = existing_system
                result["msg"] = "System would be deleted."
            else:
                try:
                    client.collection("systems").delete(id=existing_system["id"])
                    result["changed"] = True
                    result["system"] = existing_system
                    result["msg"] = "System was deleted."
                except Exception as e:
                    module.fail_json(
                        msg=f"Failed to delete system '{module.params['name']}': {e}"
                    )

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
