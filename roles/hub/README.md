# `community.beszel.hub`

Install and configure [Beszel](https://github.com/henrygd/beszel) hub.

## Role Variables

```yaml
hub_state: present
```

State of the Beszel hub installation. Can be either `present` or `absent`.

```yaml
hub_version: latest
```

Version of the Beszel hub to install. Can be a specific version from GitHub (e.g., `v0.9.1`).

```yaml
hub_bind_address: 0.0.0.0
```

Bind address for the Beszel hub to listen on.

```yaml
hub_port: 8090
```

Port for the Beszel hub to listen on.

```yaml
hub_install_dir: /usr/local/bin
```

Directory to install the Beszel hub into.

```yaml
hub_data_dir: /var/lib/beszel
```

Directory to create and place the Beszel hub data into.

```yaml
hub_user: beszel
```

Name of the user to create and run the Beszel hub as.

```yaml
# hub_uid: 1001
```

UID for the hub user used to run the Beszel hub. Chosen automatically by the OS if not specified.

```yaml
hub_user_groups: []
```

Groups to add the Beszel hub user to.

```yaml
hub_args: ""
```

Custom arguments for the Beszel hub.

```yaml
hub_check_updates: false
```

Show an "update available" notification in the Beszel hub web UI when a newer release is published on GitHub (`CHECK_UPDATES`, v0.18.5+).

```yaml
hub_share_all_systems: false
```

Share all systems with all users of the Beszel hub (`SHARE_ALL_SYSTEMS`), instead of only with the users each system is assigned to. Read-only users still cannot modify systems.

```yaml
hub_disable_ssh: false
```

Disable the SSH fallback of the Beszel hub (v0.21.0+), so the hub only communicates with agents that connect to it via WebSocket and never dials agents over SSH. Agents registered without `agent_hub_url` will be unreachable.

```yaml
hub_app_url: ""
# Example
hub_app_url: https://beszel.example.tld
```

Public URL of the Beszel hub (`APP_URL`), used for links in notifications. Set this when the hub is served behind a reverse proxy or on a non-default URL.

```yaml
hub_service_enabled: true
```

Enable the Beszel hub systemd service on boot.

```yaml
hub_service_state: started
```

State of the Beszel hub systemd service.

## Dependencies

This role depends on precompiled binaries published on GitHub at [henrygd/beszel](https://github.com/henrygd/beszel/releases).

## Example Playbook

```yaml
- name: Install and configure Beszel hub.
  hosts: all
  roles:
    - community.beszel.hub
```
