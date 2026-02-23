# Ansible community collection for Beszel Release Notes

**Topics**

- <a href="#v0-7-2">v0\.7\.2</a>
    - <a href="#release-summary">Release Summary</a>
    - <a href="#minor-changes">Minor Changes</a>
- <a href="#v0-7-0">v0\.7\.0</a>
    - <a href="#release-summary-1">Release Summary</a>
    - <a href="#minor-changes-1">Minor Changes</a>
- <a href="#v0-6-2">v0\.6\.2</a>
    - <a href="#release-summary-2">Release Summary</a>
    - <a href="#minor-changes-2">Minor Changes</a>
- <a href="#v0-6-1">v0\.6\.1</a>
    - <a href="#release-summary-3">Release Summary</a>
    - <a href="#minor-changes-3">Minor Changes</a>
- <a href="#v0-6-0">v0\.6\.0</a>
    - <a href="#release-summary-4">Release Summary</a>
    - <a href="#minor-changes-4">Minor Changes</a>
    - <a href="#new-modules">New Modules</a>
- <a href="#v0-5-0">v0\.5\.0</a>
    - <a href="#release-summary-5">Release Summary</a>
    - <a href="#minor-changes-5">Minor Changes</a>
- <a href="#v0-4-0">v0\.4\.0</a>
    - <a href="#release-summary-6">Release Summary</a>
    - <a href="#minor-changes-6">Minor Changes</a>
- <a href="#v0-3-0">v0\.3\.0</a>
    - <a href="#release-summary-7">Release Summary</a>
    - <a href="#minor-changes-7">Minor Changes</a>
    - <a href="#new-modules-1">New Modules</a>
- <a href="#v0-2-0">v0\.2\.0</a>
    - <a href="#release-summary-8">Release Summary</a>
    - <a href="#minor-changes-8">Minor Changes</a>
- <a href="#v0-1-0">v0\.1\.0</a>
    - <a href="#release-summary-9">Release Summary</a>

<a id="v0-7-2"></a>
## v0\.7\.2

<a id="release-summary"></a>
### Release Summary

Release 0\.7\.2 of the Ansible community collection for Beszel\.

<a id="minor-changes"></a>
### Minor Changes

* Add Molecule scenario <code>hub\_openrc</code> to test hub deployment with OpenRC \(Alpine\)\.
* community\.beszel\.agent \- Add default for \'agent\_uid\' role variable to specify the UID for the agent user \(default omits UID\)\.
* community\.beszel\.agent \- Add support for managing the Beszel agent service with OpenRC in addition to systemd\.
* community\.beszel\.hub \- Add support for managing the Beszel hub service with OpenRC in addition to systemd\.

<a id="v0-7-0"></a>
## v0\.7\.0

<a id="release-summary-1"></a>
### Release Summary

Release 0\.7\.0 of the Ansible community collection for Beszel\.

<a id="minor-changes-1"></a>
### Minor Changes

* community\.beszel\.agent \- Add \'agent\_uid\' role variable to specify the UID for the agent user\.
* community\.beszel\.universal\_token \- Add persistence parameter to control token permanence with choices ephemeral \(default\) or permanent\.

<a id="v0-6-2"></a>
## v0\.6\.2

<a id="release-summary-2"></a>
### Release Summary

Release 0\.6\.2 of the Ansible community collection for Beszel\.

<a id="minor-changes-2"></a>
### Minor Changes

* community\.beszel\.agent \- Create beszel user as a system user without home directory\.
* community\.beszel\.hub \- Create beszel user as a system user without home directory\.

<a id="v0-6-1"></a>
## v0\.6\.1

<a id="release-summary-3"></a>
### Release Summary

Release 0\.6\.1 of the Ansible community collection for Beszel\.

<a id="minor-changes-3"></a>
### Minor Changes

* community\.beszel\.agent \- Ensure the beszel\-agent systemd service is restarted to apply changes correctly\.

<a id="v0-6-0"></a>
## v0\.6\.0

<a id="release-summary-4"></a>
### Release Summary

Release 0\.6\.0 of the Ansible community collection for Beszel\.

<a id="minor-changes-4"></a>
### Minor Changes

* Add GitHub Actions workflow for running antsibull\-nox\.
* Add antsibull\-nox to the project\.
* Fix linting issues with all modules\.

<a id="new-modules"></a>
### New Modules

* community\.beszel\.universal\_token \- Enable or disable the universal token for the Beszel hub\.

<a id="v0-5-0"></a>
## v0\.5\.0

<a id="release-summary-5"></a>
### Release Summary

Release 0\.5\.0 of the Ansible community collection for Beszel\.

<a id="minor-changes-5"></a>
### Minor Changes

* Add AGENTS\.md to instruct AI agents how to perform development tasks within this project\.
* community\.beszel\.agent \- Add support for air\-gapped deployment mode via the \'agent\_airgap\' variable\. When enabled\, the Beszel binary agent is copied from the Ansible Controller instead of being downloaded from GitHub\, enabling deployment in disconnected or restricted network environments\.
* community\.beszel\.agent \- Add support for arm64 architecture\.
* community\.beszel\.agent \- Enhanced README documentation with additional information about authentication variables and their requirements\.
* community\.beszel\.agent \- Enhanced authentication validation logic to ensure \'agent\_public\_key\' is always required\, and \'agent\_hub\_url\' must be provided when using \'agent\_token\' authentication\.
* community\.beszel\.agent \- Improve documentation of example playbooks\.

<a id="v0-4-0"></a>
## v0\.4\.0

<a id="release-summary-6"></a>
### Release Summary

Release 0\.4\.0 of the Ansible community collection for Beszel\.

<a id="minor-changes-6"></a>
### Minor Changes

* community\.beszel\.agent \- Add \'agent\_name\' role variable\. Name of the host in the Beszel hub that is used instead of the system hostname when registering with the Beszel hub \(v0\.13\.0\+\)\.

<a id="v0-3-0"></a>
## v0\.3\.0

<a id="release-summary-7"></a>
### Release Summary

Release 0\.3\.0 of the Ansible community collection for Beszel\.

<a id="minor-changes-7"></a>
### Minor Changes

* community\.beszel\.agent \- Add \'agent\_token\' role variable\. Universal token used by the Beszel binary agent to automatically register with Beszel hub\.
* community\.beszel\.agent \- Force flushing of handlers to resolve issue 6\.

<a id="new-modules-1"></a>
### New Modules

* community\.beszel\.system \- Manage Beszel systems\.
* community\.beszel\.system\_info \- Get information about Beszel systems\.

<a id="v0-2-0"></a>
## v0\.2\.0

<a id="release-summary-8"></a>
### Release Summary

Release 0\.2\.0 of the Ansible community collection for Beszel\.

<a id="minor-changes-8"></a>
### Minor Changes

* community\.beszel\.agent \- Add \'agent\_hub\_url\' role variable\. URL of the Beszel hub for the Beszel binary agent to connect to\.

<a id="v0-1-0"></a>
## v0\.1\.0

<a id="release-summary-9"></a>
### Release Summary

Release 0\.1\.0 of the Ansible community collection for Beszel\.
