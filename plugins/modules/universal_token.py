#!/usr/bin/python

# Copyright: (c) 2025, Daniel Brennand <contact@danielbrennand.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: universal_token

short_description: Enable or disable the universal token for the Beszel hub.

version_added: "0.6.0"

description: Enable or disable the universal token for the Beszel hub.

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
    state:
        description: State of the universal token.
        required: false
        type: str
        default: enabled
        choices: ["enabled", "disabled"]
    persistence:
        description: Persistence mode of the universal token.
        required: false
        type: str
        default: ephemeral
        choices: ["ephemeral", "permanent"]

attributes:
    check_mode:
        description: This module does not support check mode.
        details:
            - Check mode behavior is the same as normal execution.
        support: N/A
    diff_mode:
        description: This module does not support diff mode.
        support: none
"""

EXAMPLES = r"""
---
- name: Enable the universal token for the Beszel hub
  community.beszel.universal_token:
    url: https://beszel.example.tld
    username: admin@example.com
    password: admin
    state: enabled

- name: Disable the universal token for the Beszel hub
  community.beszel.universal_token:
    url: https://beszel.example.tld
    username: admin@example.com
    password: admin
    state: disabled

- name: Enable the universal token with permanent persistence
  community.beszel.universal_token:
    url: https://beszel.example.tld
    username: admin@example.com
    password: admin
    state: enabled
    persistence: permanent
"""

RETURN = r"""
---
universal_token:
    description: Information about the universal token.
    type: dict
    returned: always
    sample: {
        "token": "ca995e6d-a8d1-416f-b77d-ea2d297060ae",
        "active": true,
        "permanent": false
    }
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


def run_module():
    module_args = dict(
        url=dict(type="str", required=True),
        username=dict(type="str", required=True),
        password=dict(type="str", required=True, no_log=True),
        timeout=dict(type="float", required=False, default=120),
        state=dict(
            type="str",
            required=False,
            default="enabled",
            choices=["enabled", "disabled"],
        ),
        persistence=dict(
            type="str",
            required=False,
            default="ephemeral",
            choices=["ephemeral", "permanent"],
        ),
    )

    result = dict(changed=False, universal_token={})

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
        ).authenticate_user()
    except Exception as e:
        module.fail_json(msg=str(e))

    # Get the current universal token state
    try:
        universal_token_response = client._send("/api/beszel/universal-token", {})
        universal_token_current_state = universal_token_response.json()
    except Exception as e:
        module.fail_json(msg=str(e))

    # Check if the current state is the same as the desired state
    desired_state_enabled = module.params["state"] == "enabled"
    desired_permanent = module.params["persistence"] == "permanent"
    current_permanent = universal_token_current_state.get("permanent", False)

    # Check if both active and permanent states match the desired states
    if (
        universal_token_current_state["active"] == desired_state_enabled
        and current_permanent == desired_permanent
    ):
        result["changed"] = False
        result["universal_token"] = universal_token_current_state
    else:
        # Enable or disable the universal token based on desired state
        enable_value = 1 if desired_state_enabled else 0
        permanent_value = 1 if desired_permanent else 0
        try:
            token_url = f"/api/beszel/universal-token?enable={enable_value}&permanent={permanent_value}"
            if not enable_value:
                token_url = (
                    f"{token_url}&token={universal_token_current_state['token']}"
                )
            universal_token_response = client._send(token_url, {})
            result["changed"] = True
            result["universal_token"] = universal_token_response.json()
        except Exception as e:
            module.fail_json(msg=str(e))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
