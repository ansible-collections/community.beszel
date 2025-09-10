# Ansible community collection for Beszel Release Notes

**Topics**

- <a href="#v0-3-0">v0\.3\.0</a>
    - <a href="#release-summary">Release Summary</a>
    - <a href="#minor-changes">Minor Changes</a>
    - <a href="#new-modules">New Modules</a>
    - <a href="#new-roles">New Roles</a>
- <a href="#v0-2-0">v0\.2\.0</a>
    - <a href="#release-summary-1">Release Summary</a>
    - <a href="#minor-changes-1">Minor Changes</a>
- <a href="#v0-1-0">v0\.1\.0</a>
    - <a href="#release-summary-2">Release Summary</a>
    - <a href="#new-roles-1">New Roles</a>

<a id="v0-3-0"></a>
## v0\.3\.0

<a id="release-summary"></a>
### Release Summary

Release 0\.3\.0 of the Ansible community collection for Beszel\.

<a id="minor-changes"></a>
### Minor Changes

* community\.beszel\.agent \- Add \'agent\_token\' role variable\. Universal token used by the Beszel binary agent to automatically register with Beszel hub\.
* community\.beszel\.agent \- Force flushing of handlers to resolve issue 6\.

<a id="new-modules"></a>
### New Modules

* community\.beszel\.system \- Manage Beszel systems\.
* community\.beszel\.system\_info \- Get information about Beszel systems\.

<a id="new-roles"></a>
### New Roles

* community\.beszel\.hub \- Install and configure Beszel hub\.

<a id="v0-2-0"></a>
## v0\.2\.0

<a id="release-summary-1"></a>
### Release Summary

Release 0\.2\.0 of the Ansible community collection for Beszel\.

<a id="minor-changes-1"></a>
### Minor Changes

* community\.beszel\.agent \- Add \'agent\_hub\_url\' role variable\. URL of the Beszel hub for the Beszel binary agent to connect to\.

<a id="v0-1-0"></a>
## v0\.1\.0

<a id="release-summary-2"></a>
### Release Summary

Release 0\.1\.0 of the Ansible community collection for Beszel\.

<a id="new-roles-1"></a>
### New Roles

* community\.beszel\.agent \- Install and configure a Beszel binary agent\.
