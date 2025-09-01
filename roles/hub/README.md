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
hub_args: ""
```

Custom arguments for the Beszel hub.

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
