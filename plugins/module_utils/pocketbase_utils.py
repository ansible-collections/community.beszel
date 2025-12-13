# Copyright: (c) 2025, Daniel Brennand <contact@danielbrennand.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

try:
    from pocketbase import PocketBase
    from pocketbase.errors import ClientResponseError

    HAS_POCKETBASE = True
except ImportError:
    HAS_POCKETBASE = False
    PocketBase = None
    ClientResponseError = None


class PocketBaseClient:
    def __init__(self, url: str, username: str, password: str, timeout: float = 120):
        if not HAS_POCKETBASE:
            raise ImportError("pocketbase library is required but not available.")
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

    def authenticate_user(self):
        """Authenticate with PocketBase API using user auth."""
        try:
            auth_data = self.client.collection("users").auth_with_password(
                self.username, self.password
            )
            if auth_data.is_valid:
                return self.client
            else:
                raise Exception("Token is not valid.")
        except (ClientResponseError, Exception) as e:
            raise Exception(f"Authentication failed: {e}")
