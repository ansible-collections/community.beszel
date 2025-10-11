=====================================================
Ansible community collection for Beszel Release Notes
=====================================================

.. contents:: Topics

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

New Roles
---------

- community.beszel.hub - Install and configure Beszel hub.

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

New Roles
---------

- community.beszel.agent - Install and configure a Beszel binary agent.
