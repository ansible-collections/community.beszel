# Ansible community collection for Beszel Release Notes

**Topics**

- <a href="#v2-1-0">v2\.1\.0</a>
    - <a href="#release-summary">Release Summary</a>
    - <a href="#minor-changes">Minor Changes</a>
    - <a href="#bugfixes">Bugfixes</a>
- <a href="#v2-0-0">v2\.0\.0</a>
    - <a href="#release-summary-1">Release Summary</a>
    - <a href="#minor-changes-1">Minor Changes</a>
    - <a href="#breaking-changes--porting-guide">Breaking Changes / Porting Guide</a>
- <a href="#v1-0-0">v1\.0\.0</a>
    - <a href="#release-summary-2">Release Summary</a>
    - <a href="#minor-changes-2">Minor Changes</a>
    - <a href="#breaking-changes--porting-guide-1">Breaking Changes / Porting Guide</a>
    - <a href="#bugfixes-1">Bugfixes</a>
- <a href="#v0-7-1">v0\.7\.1</a>
    - <a href="#release-summary-3">Release Summary</a>
    - <a href="#bugfixes-2">Bugfixes</a>
- <a href="#v0-7-0">v0\.7\.0</a>
    - <a href="#release-summary-4">Release Summary</a>
    - <a href="#minor-changes-3">Minor Changes</a>
- <a href="#v0-6-2">v0\.6\.2</a>
    - <a href="#release-summary-5">Release Summary</a>
    - <a href="#minor-changes-4">Minor Changes</a>
- <a href="#v0-6-1">v0\.6\.1</a>
    - <a href="#release-summary-6">Release Summary</a>
    - <a href="#minor-changes-5">Minor Changes</a>
- <a href="#v0-6-0">v0\.6\.0</a>
    - <a href="#release-summary-7">Release Summary</a>
    - <a href="#minor-changes-6">Minor Changes</a>
    - <a href="#new-modules">New Modules</a>
- <a href="#v0-5-0">v0\.5\.0</a>
    - <a href="#release-summary-8">Release Summary</a>
    - <a href="#minor-changes-7">Minor Changes</a>
- <a href="#v0-4-0">v0\.4\.0</a>
    - <a href="#release-summary-9">Release Summary</a>
    - <a href="#minor-changes-8">Minor Changes</a>
- <a href="#v0-3-0">v0\.3\.0</a>
    - <a href="#release-summary-10">Release Summary</a>
    - <a href="#minor-changes-9">Minor Changes</a>
    - <a href="#new-modules-1">New Modules</a>
- <a href="#v0-2-0">v0\.2\.0</a>
    - <a href="#release-summary-11">Release Summary</a>
    - <a href="#minor-changes-10">Minor Changes</a>
- <a href="#v0-1-0">v0\.1\.0</a>
    - <a href="#release-summary-12">Release Summary</a>

<a id="v2-1-0"></a>
## v2\.1\.0

<a id="release-summary"></a>
### Release Summary

Release 2\.1\.0 of the Ansible community collection for Beszel\.

<a id="minor-changes"></a>
### Minor Changes

* Added <em class="title-reference">agent\_additional\_devices</em> variable\. Devices and access modes to grant to the Beszel binary agent\'s systemd service\.
* Added <em class="title-reference">agent\_systemd\_journal\_access</em> variable \(default\: <em class="title-reference">true</em>\) to enable systemd journal log access for the Beszel agent\. This adds <em class="title-reference">SupplementaryGroups\=systemd\-journal</em> to the systemd service unit\.
* community\.beszel\.agent \- Add <code>agent\_disable\_ssh</code> variable to disable the Beszel binary agent SSH server \(<code>DISABLE\_SSH</code>\)\. When enabled\, <code>agent\_hub\_url</code> and <code>agent\_token</code> must both be provided
* community\.beszel\.agent \- Add <code>agent\_icmp</code> variable to grant the Beszel binary agent the <code>CAP\_NET\_RAW</code> capability for ICMP network monitors\.
* community\.beszel\.agent \- Add <code>agent\_package\_updates\_interval</code> variable to configure the Beszel binary agent package update check interval \(<code>PACKAGE\_UPDATES\_INTERVAL</code>\)\.
* community\.beszel\.agent \- Add <code>agent\_sensors</code> variable to configure which temperature sensors are monitored by the Beszel binary agent \(<code>SENSORS</code>\)\.
* community\.beszel\.hub \- Add <code>hub\_app\_url</code> variable to set the public URL of the Beszel hub \(<code>APP\_URL</code>\)
* community\.beszel\.hub \- Add <code>hub\_check\_updates</code> variable to enable the update available notification in the Beszel hub web UI \(<code>CHECK\_UPDATES</code>\)
* community\.beszel\.hub \- Add <code>hub\_disable\_ssh</code> variable to disable the Beszel hub SSH fallback \(<code>DISABLE\_SSH</code>\)
* community\.beszel\.hub \- Add <code>hub\_share\_all\_systems</code> variable to share all systems with all users of the Beszel hub \(<code>SHARE\_ALL\_SYSTEMS</code>\)
* community\.beszel\.hub \- Add <code>hub\_sync\_system\_names</code> variable to sync system names with agent hostnames \(<code>SYNC\_SYSTEM\_NAMES</code>\)

<a id="bugfixes"></a>
### Bugfixes

* community\.beszel\.agent \- Set <code>CapabilityBoundingSet</code> whenever ambient capabilities are configured\, not only when S\.M\.A\.R\.T disks are monitored\.

<a id="v2-0-0"></a>
## v2\.0\.0

<a id="release-summary-1"></a>
### Release Summary

Release 2\.0\.0 of the Ansible community collection for Beszel\.

<a id="minor-changes-1"></a>
### Minor Changes

* Add unit test coverage reporting to the tox\-ansible test matrix\.
* Adopt the ansible\-lint production profile and Ruff formatting checks\.
* Consolidate GitHub Actions into a generated tox\-ansible test matrix with a separate ansible\-lint job\.
* Refine collection build exclusions to omit development\, test\, cache\, and local environment files from release artifacts\.
* Replace antsibull\-nox with tox\-ansible to run sanity\, unit\, and integration tests across the supported Python and ansible\-core versions\.
* Run Molecule integration scenarios through the pytest\-ansible Molecule fixture\.
* Simplify development and test dependency management and remove obsolete test configuration and workarounds\.
* community\.beszel\.agent \- Add argument spec for role input validation\.

<a id="breaking-changes--porting-guide"></a>
### Breaking Changes / Porting Guide

* Drop support for ansible\-core 2\.17 and 2\.18\. The minimum supported version is now ansible\-core 2\.19\.

<a id="v1-0-0"></a>
## v1\.0\.0

<a id="release-summary-2"></a>
### Release Summary

Release 1\.0\.0 of the Ansible community collection for Beszel\.

<a id="minor-changes-2"></a>
### Minor Changes

* community\.beszel\.agent \- Add GPU and S\.M\.A\.R\.T disk monitoring support with agent\_gpus and agent\_smart\_disks variables\.
* community\.beszel\.hub \- Add hub\_bind\_address to customize the bind address to listen on\.
* community\.beszel\.hub \- Add hub\_uid and hub\_user\_groups variables

<a id="breaking-changes--porting-guide-1"></a>
### Breaking Changes / Porting Guide

* community\.beszel\.agent \- Replace auto docker\-group detection with configurable agent\_user\_groups and agent\_docker\_host variables

<a id="bugfixes-1"></a>
### Bugfixes

* Remove append flag from user creation tasks in agent and hub roles

<a id="v0-7-1"></a>
## v0\.7\.1

<a id="release-summary-3"></a>
### Release Summary

Release 0\.7\.1 of the Ansible community collection for Beszel\.

<a id="bugfixes-2"></a>
### Bugfixes

* community\.beszel\.agent \- Skip tarball extraction tasks when running in Ansible check mode to prevent failures on fresh systems where the tarball has not been downloaded yet\.
* community\.beszel\.hub \- Skip tarball extraction tasks when running in Ansible check mode to prevent failures on fresh systems where the tarball has not been downloaded yet\.

<a id="v0-7-0"></a>
## v0\.7\.0

<a id="release-summary-4"></a>
### Release Summary

Release 0\.7\.0 of the Ansible community collection for Beszel\.

<a id="minor-changes-3"></a>
### Minor Changes

* community\.beszel\.agent \- Add \'agent\_uid\' role variable to specify the UID for the agent user\.
* community\.beszel\.universal\_token \- Add persistence parameter to control token permanence with choices ephemeral \(default\) or permanent\.

<a id="v0-6-2"></a>
## v0\.6\.2

<a id="release-summary-5"></a>
### Release Summary

Release 0\.6\.2 of the Ansible community collection for Beszel\.

<a id="minor-changes-4"></a>
### Minor Changes

* community\.beszel\.agent \- Create beszel user as a system user without home directory\.
* community\.beszel\.hub \- Create beszel user as a system user without home directory\.

<a id="v0-6-1"></a>
## v0\.6\.1

<a id="release-summary-6"></a>
### Release Summary

Release 0\.6\.1 of the Ansible community collection for Beszel\.

<a id="minor-changes-5"></a>
### Minor Changes

* community\.beszel\.agent \- Ensure the beszel\-agent systemd service is restarted to apply changes correctly\.

<a id="v0-6-0"></a>
## v0\.6\.0

<a id="release-summary-7"></a>
### Release Summary

Release 0\.6\.0 of the Ansible community collection for Beszel\.

<a id="minor-changes-6"></a>
### Minor Changes

* Add GitHub Actions workflow for running antsibull\-nox\.
* Add antsibull\-nox to the project\.
* Fix linting issues with all modules\.

<a id="new-modules"></a>
### New Modules

* community\.beszel\.universal\_token \- Enable or disable the universal token for the Beszel hub\.

<a id="v0-5-0"></a>
## v0\.5\.0

<a id="release-summary-8"></a>
### Release Summary

Release 0\.5\.0 of the Ansible community collection for Beszel\.

<a id="minor-changes-7"></a>
### Minor Changes

* Add AGENTS\.md to instruct AI agents how to perform development tasks within this project\.
* community\.beszel\.agent \- Add support for air\-gapped deployment mode via the \'agent\_airgap\' variable\. When enabled\, the Beszel binary agent is copied from the Ansible Controller instead of being downloaded from GitHub\, enabling deployment in disconnected or restricted network environments\.
* community\.beszel\.agent \- Add support for arm64 architecture\.
* community\.beszel\.agent \- Enhanced README documentation with additional information about authentication variables and their requirements\.
* community\.beszel\.agent \- Enhanced authentication validation logic to ensure \'agent\_public\_key\' is always required\, and \'agent\_hub\_url\' must be provided when using \'agent\_token\' authentication\.
* community\.beszel\.agent \- Improve documentation of example playbooks\.

<a id="v0-4-0"></a>
## v0\.4\.0

<a id="release-summary-9"></a>
### Release Summary

Release 0\.4\.0 of the Ansible community collection for Beszel\.

<a id="minor-changes-8"></a>
### Minor Changes

* community\.beszel\.agent \- Add \'agent\_name\' role variable\. Name of the host in the Beszel hub that is used instead of the system hostname when registering with the Beszel hub \(v0\.13\.0\+\)\.

<a id="v0-3-0"></a>
## v0\.3\.0

<a id="release-summary-10"></a>
### Release Summary

Release 0\.3\.0 of the Ansible community collection for Beszel\.

<a id="minor-changes-9"></a>
### Minor Changes

* community\.beszel\.agent \- Add \'agent\_token\' role variable\. Universal token used by the Beszel binary agent to automatically register with Beszel hub\.
* community\.beszel\.agent \- Force flushing of handlers to resolve issue 6\.

<a id="new-modules-1"></a>
### New Modules

* community\.beszel\.system \- Manage Beszel systems\.
* community\.beszel\.system\_info \- Get information about Beszel systems\.

<a id="v0-2-0"></a>
## v0\.2\.0

<a id="release-summary-11"></a>
### Release Summary

Release 0\.2\.0 of the Ansible community collection for Beszel\.

<a id="minor-changes-10"></a>
### Minor Changes

* community\.beszel\.agent \- Add \'agent\_hub\_url\' role variable\. URL of the Beszel hub for the Beszel binary agent to connect to\.

<a id="v0-1-0"></a>
## v0\.1\.0

<a id="release-summary-12"></a>
### Release Summary

Release 0\.1\.0 of the Ansible community collection for Beszel\.
