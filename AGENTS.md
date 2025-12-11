# Project Overview

This repository contains the `community.beszel` Ansible Collection. It follows the standard Ansible Collection structure.

This file is intended for use by AI agents to execute tasks within this project. It has been structured to remain human-readable so that contributors can easily understand the purpose of the included tools and files, and learn how to use them to perform development tasks.

## Development Environment

- This project uses the Python package and project manager [`uv`](https://docs.astral.sh/uv/).
- This project uses [Ansible Development Environment (ADE)](https://github.com/ansible/ansible-dev-environment) for collection development.
- Install ADE using the command: `uv tool install ansible-dev-environment`.
- Initialize the Python project and all its dependencies using the following commands:

    ```bash
    uv sync --dev
    uv run prek install
    uv pip install -r meta/ee-requirements.txt
    ade install --editable --no-seed --venv .venv .
    ade install --no-seed --venv .venv -r extensions/molecule/requirements.yml
    ```

## Testing Instructions

- [Molecule](https://ansible.readthedocs.io/projects/molecule/) is used for testing Ansible roles located in the `roles` directory.
- Run Molecule tests from the `extensions` directory.
- Run all Molecule scenarios using the command: `uv run molecule test --all`.
- Run a specific Molecule scenario using the command: `uv run molecule test -s <scenario>`.
- [Ansible Lint](http://ansible.readthedocs.io/projects/lint/) is used for linting Ansible roles and playbooks located in the `roles` and `playbooks` directories respectively.
- Run `ansible-lint` from the project root using the command: `uv run ansible-lint -v`.
- Run `pre-commit` hooks from the project root using the command: `uv run pre-commit run --all-files`.
- [ansible-test](https://docs.ansible.com/ansible/latest/dev_guide/testing.html) is used to run sanity, integration and unit tests on content in the Ansible Collection.
- Run sanity tests from the project root using the command: `uv run ansible-test sanity --docker`.
- Run integration tests from the project root using the command: `uv run ansible-test integration --docker`.
- Run unit tests from the project root using the command: `uv run ansible-test units --docker`.

## Coding Guidelines

- Ansible plugins and modules should be formatted using `ruff`.
- Format Ansible plugins and modules from the project root using the command: `uv run ruff format plugins/`.
- Ansible plugins and modules should use the standard snake_case variable convention.
- Ansible plugins and modules should pass checks performed by `uv run ansible-test sanity --docker`.
- All files committed should pass `pre-commit` hook checks.
- All Ansible content in the `roles` and `playbooks` directory should pass `ansible-lint`.

## Architecture

- The repository follows the standard Ansible Collection structure.
- Ansible roles are located in the `roles` directory.
- Ansible plugins and modules are located in the `plugins` directory. Modules specifically are located in `plugins/modules`.
- A Python function which is used by multiple modules should be implemented in the `plugins/module_utils` directory. This ensures code conforms to DRY (Don't repeat yourself) principle.
- Ansible Molecule scenarios are located in the `extensions/molecule` directory.
- Each Ansible role should contain at least one Molecule scenario.
- Add a new Python integration tests dependency by adding it to the [`tests/integration/requirements.txt`](tests/integration/requirements.txt) file.
- Molecule scenarios rely on collection dependencies located in [`extensions/molecule/requirements.yml`](extensions/molecule/requirements.yml). Add a new collection dependency by modifying this file.
- Any Python dependencies required by the collection reside in the [`meta/ee-requirements.txt`](meta/ee-requirements.txt) file. Any Python dependencies required by this collection must be added to this file and be version constrained.
- Development dependencies are defined in the [`pyproject.toml`](pyproject.toml) file in the `dev` `[dependency-groups]`.
- Development dependencies can be added to the project using the command: `uv add <package> --dev`.
- The `version` in the [`pyproject.toml`](pyproject.toml) file should match the `version` in the [`galaxy.yml`](galaxy.yml) file.

## Changelogs

- The project uses the [antsibull-changelog](https://ansible.readthedocs.io/projects/antsibull-changelog/) Python package to automatically generate changelogs for the Ansible Collection.
- `antsibull-changelog` uses fragments located in the `changelogs/fragments` directory. Changes to the collection should be included in a changelog fragment file.
- `antsibull-changelog` generates two changelog files in the project root called `CHANGELOG.md` and `CHANGELOG.rst`. The fragments located in the `changelogs/fragments` directory determine the content of these files.
- Generating the `CHANGELOG.md` and `CHANGELOG.rst` files can be done using the command: `uv run antsibull-changelog release -v`.
