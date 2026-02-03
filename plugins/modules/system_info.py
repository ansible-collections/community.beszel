#!/usr/bin/python

# Copyright: (c) 2025, Daniel Brennand <contact@danielbrennand.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: system_info

short_description: Get information about Beszel systems.

version_added: "0.3.0"

description: Get information about registered Beszel systems.

author:
    - Daniel Brennand (@dbrennand) <contact@danielbrennand.com>

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
        description:
            - Name of the Beszel system.
            - If not provided, all systems will be returned.
        required: false
        type: str

attributes:
    check_mode:
        description: This module does not support check mode.
        details:
            - This module is read-only.
            - Check mode behavior is the same as normal execution.
        support: N/A
    diff_mode:
        description: This module does not support diff mode.
        support: none
"""

EXAMPLES = r"""
---
- name: Get information about a Beszel system
  community.beszel.system_info:
    url: https://beszel.example.tld
    username: admin@example.com
    password: admin
    name: instance

- name: Get information about all Beszel systems
  community.beszel.system_info:
    url: https://beszel.example.tld
    username: admin@example.com
    password: admin
"""

RETURN = r"""
---
systems:
    description: List of Beszel systems.
    type: list
    returned: always
    sample: [
        {
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
    ]
"""

import traceback

try:
    from ansible_collections.community.beszel.plugins.module_utils.pocketbase_utils import (
        PocketBaseClient,
    )
except ImportError:
    HAS_POCKETBASE = False
    POCKETBASE_IMPORT_ERROR = traceback.format_exc()
else:
    HAS_POCKETBASE = True
    POCKETBASE_IMPORT_ERROR = None

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import missing_required_lib

def run_module(client, params: dict) -> dict:
    result = dict(changed=False, systems=[])
    try:
        client = PocketBaseClient(
            url=params["url"],
            username=params["username"],
            password=params["password"],
            timeout=params["timeout"],
        ).authenticate()
    except Exception as e:
        return dict(msg=(str(e)), failed=True)
        #module.fail_json(msg=str(e))

    # If we are provided a system name, we want to get a single record for that system
    if params["name"]:
        try:
            data = client.collection("systems").get_first_list_item(
                filter=f"name='{params['name']}'"
            )
            result["systems"] = [data.__dict__]
        except Exception as e:
            return dict(msg=str(e), failed=True)
    # If we are not provided a system name, get all systems sorted by creation date
    else:
        data = client.collection("systems").get_full_list(
            query_params={"sort": "created"}
        )
        result["systems"] = [record.__dict__ for record in data]

    return result


def main():
    # Note: This module is read-only, so check_mode behavior is the same as normal execution
    module_args = dict(
        url=dict(type="str", required=True),
        username=dict(type="str", required=True),
        password=dict(type="str", required=True, no_log=True),
        timeout=dict(type="float", required=False, default=120),
        name=dict(type="str", required=False),
    )

    if not HAS_POCKETBASE:
        module.fail_json(
            msg=missing_required_lib("pocketbase"), exception=POCKETBASE_IMPORT_ERROR
        )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    result = run_module(params=module.params)
    module.exit_json(**result)


if __name__ == "__main__":
    main()
