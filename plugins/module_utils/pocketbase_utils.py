#!/usr/bin/python

# Copyright: (c) 2025, Daniel Brennand <contact@danielbrennand.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import missing_required_lib

try:
    from pocketbase import PocketBase
    from pocketbase.errors import ClientResponseError
except ImportError:
    raise ImportError(missing_required_lib("pocketbase"))


class PocketBaseClient:
    def __init__(self, url: str, username: str, password: str, timeout: float = 120):
        self.url = url
        self.username = username
        self.password = password
        self.timeout = timeout
        self.client = PocketBase(base_url=self.url, timeout=timeout)

    def authenticate(self):
        """Authenticate with PocketBase API using admin auth."""
        try:
            auth_data = self.client.admins.auth_with_password(
                self.username, self.password
            )
            if auth_data.is_valid:
                return self.client
            else:
                raise Exception("Token is not valid.")
        except (ClientResponseError, Exception) as e:
            raise Exception(f"Authentication failed: {e}")
