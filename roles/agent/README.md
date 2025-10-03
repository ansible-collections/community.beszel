# `community.beszel.agent`

Install and configure a [Beszel](https://github.com/henrygd/beszel) binary agent.

## Role Variables

### Authentication Methods

Beszel supports two authentication methods for agents:

#### Method 1: Individual System Authentication (Traditional)

```yaml
agent_public_key: ""
agent_token: ""
# Example
agent_public_key: "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJxK7vQ9rL2mN8pYfGhU3zWcE5tRoS6iD1bV4nM9qX8A"
agent_token: "944bb14b-25d7-47f8-bf79-ca9c048a3370"
```

Individual system authentication using a public key and system token. Requires manual system registration in Beszel hub where you provide the public key and receive the corresponding token. Alternatively, the ``community.beszel.system`` module can be used to the register the system.

#### Method 2: Universal Token (Beszel v0.12.0+)

```yaml
agent_universal_token: ""
# Example
agent_universal_token: "35c673e6-bbb9-4b5e-a9d3-1e62f9063532"
```

Universal token for automatic agent registration. No manual system creation required - agents automatically register when connecting to Beszel hub.

### Other Variables

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

## Dependencies

This role depends on precompiled binaries published on GitHub at [henrygd/beszel](https://github.com/henrygd/beszel/releases).

## Example Playbooks

### Using Individual System Authentication

```yaml
- name: Install and configure a Beszel binary agent with individual system auth
  hosts: all
  roles:
    - role: community.beszel.agent
      vars:
        agent_public_key: "<Public Key for Beszel Hub>"
        agent_token: "<Token from Beszel Hub>"
        agent_hub_url: "https://beszel.example.tld"
```

### Using Universal Token (Recommended for Beszel v0.12.0+)

```yaml
- name: Install and configure a Beszel binary agent with universal token
  hosts: all
  roles:
    - role: community.beszel.agent
      vars:
        agent_universal_token: "<Universal Token from Beszel Hub>"
        agent_hub_url: "https://beszel.example.tld"
```

## Contributors

[Daniel Brennand](https://github.com/dbrennand)

[Matthias Stegmann](https://github.com/stegmatze)

[Matthew Andersen](https://github.com/crzykidd)
