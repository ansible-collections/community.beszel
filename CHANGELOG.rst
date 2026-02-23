=====================================================
Ansible community collection for Beszel Release Notes
=====================================================

.. contents:: Topics

v0.7.1
======

Release Summary
---------------

Release 0.7.1 of the Ansible community collection for Beszel.

Bugfixes
--------

- community.beszel.agent - Skip tarball extraction tasks when running in Ansible check mode to prevent failures on fresh systems where the tarball has not been downloaded yet.
- community.beszel.hub - Skip tarball extraction tasks when running in Ansible check mode to prevent failures on fresh systems where the tarball has not been downloaded yet.

v0.7.0
======

Release Summary
---------------

Release 0.7.0 of the Ansible community collection for Beszel.

Minor Changes
-------------

- community.beszel.agent - Add 'agent_uid' role variable to specify the UID for the agent user.
- community.beszel.universal_token - Add persistence parameter to control token permanence with choices ephemeral (default) or permanent.

v0.6.2
======

Release Summary
---------------

Release 0.6.2 of the Ansible community collection for Beszel.

Minor Changes
-------------

- community.beszel.agent - Create beszel user as a system user without home directory.
- community.beszel.hub - Create beszel user as a system user without home directory.

v0.6.1
======

Release Summary
---------------

Release 0.6.1 of the Ansible community collection for Beszel.

Minor Changes
-------------

- community.beszel.agent - Ensure the beszel-agent systemd service is restarted to apply changes correctly.

v0.6.0
======

Release Summary
---------------

Release 0.6.0 of the Ansible community collection for Beszel.

Minor Changes
-------------

- Add GitHub Actions workflow for running antsibull-nox.
- Add antsibull-nox to the project.
- Fix linting issues with all modules.

New Modules
-----------

- community.beszel.universal_token - Enable or disable the universal token for the Beszel hub.

v0.5.0
======

Release Summary
---------------

Release 0.5.0 of the Ansible community collection for Beszel.

Minor Changes
-------------

- Add AGENTS.md to instruct AI agents how to perform development tasks within this project.
- community.beszel.agent - Add support for air-gapped deployment mode via the 'agent_airgap' variable. When enabled, the Beszel binary agent is copied from the Ansible Controller instead of being downloaded from GitHub, enabling deployment in disconnected or restricted network environments.
- community.beszel.agent - Add support for arm64 architecture.
- community.beszel.agent - Enhanced README documentation with additional information about authentication variables and their requirements.
- community.beszel.agent - Enhanced authentication validation logic to ensure 'agent_public_key' is always required, and 'agent_hub_url' must be provided when using 'agent_token' authentication.
- community.beszel.agent - Improve documentation of example playbooks.

v0.4.0
======

Release Summary
---------------

Release 0.4.0 of the Ansible community collection for Beszel.

Minor Changes
-------------

- community.beszel.agent - Add 'agent_name' role variable. Name of the host in the Beszel hub that is used instead of the system hostname when registering with the Beszel hub (v0.13.0+).

v0.3.0
======

Release Summary
---------------

Release 0.3.0 of the Ansible community collection for Beszel.

Minor Changes
-------------

- community.beszel.agent - Add 'agent_token' role variable. Universal token used by the Beszel binary agent to automatically register with Beszel hub.
- community.beszel.agent - Force flushing of handlers to resolve issue 6.

New Modules
-----------

- community.beszel.system - Manage Beszel systems.
- community.beszel.system_info - Get information about Beszel systems.

v0.2.0
======

Release Summary
---------------

Release 0.2.0 of the Ansible community collection for Beszel.

Minor Changes
-------------

- community.beszel.agent - Add 'agent_hub_url' role variable. URL of the Beszel hub for the Beszel binary agent to connect to.

v0.1.0
======

Release Summary
---------------

Release 0.1.0 of the Ansible community collection for Beszel.
