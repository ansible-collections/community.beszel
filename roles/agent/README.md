# `community.beszel.agent`

Install and configure a [Beszel](https://github.com/henrygd/beszel) binary agent.

## Role Variables

```yaml
agent_public_key: ""
```

Public key used for system-specific registration to authenticate the Beszel binary agent to the Hub. **Either `agent_public_key` OR `agent_token` must be provided.**

```yaml
agent_state: present
```

State of the Beszel binary agent installation. Can be either `present` or `absent`.

```yaml
agent_version: latest
```

Version of the Beszel binary agent to install. Can be a specific version from GitHub (e.g., `v0.9.1`).

```yaml
agent_port: 45876
```

Port for the Beszel binary agent to listen on.

```yaml
agent_install_dir: /usr/local/bin
```

Directory to install the Beszel binary agent into.

```yaml
agent_user: beszel
```

Name of the user to create and run the Beszel binary agent as.

```yaml
agent_args: ""
```

Custom arguments for the Beszel binary agent. See [Beszel - Agent Installation](https://beszel.dev/guide/agent-installation) for more details.

```yaml
agent_extra_filesystems: []
# Example with extra file systems
agent_extra_filesystems:
  - sdb1
  - sdc1
  - mmcblk0
  - /mnt/network-share
```

Extra filesystems to be monitored by the Beszel binary agent. Configures the [EXTRA_FILESYSTEMS](https://beszel.dev/guide/additional-disks#binary-agent) environment variable in the agent systemd unit file.

```yaml
agent_service_enabled: true
```

Enable the Beszel binary agent systemd service on boot.

```yaml
agent_service_state: started
```

State of the Beszel binary agent systemd service.

```yaml
agent_hub_url: ""
# Example
agent_hub_url: https://beszel.example.tld
```

URL of the Beszel hub for the Beszel binary agent to connect to.

```yaml
agent_token: ""
# Example
agent_token: "633f71ba-e38b-4fdl-a454-3a214900b0u5"
```

Universal token used for automatic registration with Beszel hub. **Either `agent_public_key` OR `agent_token` must be provided.**

## Dependencies

This role depends on precompiled binaries published on GitHub at [henrygd/beszel](https://github.com/henrygd/beszel/releases).

## Example Playbook

### Using System-Specific Registration (`agent_public_key`)

```yaml
- name: Install and configure a Beszel binary agent with public key.
  hosts: all
  roles:
    - role: community.beszel.agent
      vars:
        agent_public_key: "<Public key for Beszel hub>"
```

### Using Universal Token Authentication (`agent_token`)

```yaml
- name: Install and configure a Beszel binary agent with universal token.
  hosts: all
  roles:
    - role: community.beszel.agent
      vars:
        agent_token: "633f71ba-e38b-4fdl-a454-3a214900b0u5"
```

## Contributors

[Daniel Brennand](https://github.com/dbrennand)

[Matthias Stegmann](https://github.com/stegmatze)

[Matthew Andersen](https://github.com/crzykidd)
