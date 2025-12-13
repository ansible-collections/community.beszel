# Contributing

## Getting Started

The `community.beszel` Ansible collection uses [uv](https://docs.astral.sh/uv/) and [Ansible Development Environment (ADE)](https://github.com/ansible/ansible-dev-environment) for collection development. The recommended method for [installing](https://github.com/ansible/ansible-dev-environment?tab=readme-ov-file#installation) ADE is using [`uv`](https://docs.astral.sh/uv/):

```bash
uv tool install ansible-dev-environment
```

Once ADE is installed, follow the steps below for contributing to `community.beszel`:

1. [Fork](https://github.com/ansible-collections/community.beszel/fork) the `community.beszel` collection.

2. Clone your fork of the `community.beszel` collection:

    ```bash
    git clone https://github.com/YOUR_USERNAME/community.beszel.git ~/ansible_collections/community/beszel
    cd ~/ansible_collections/community/beszel
    ```

3. Create your feature branch:

    ```bash
    git checkout -b feature/my-new-feature
    ```

4. Initialize the development environment using `uv` and ADE:

    ```bash
    uv sync --dev
    uv run prek install
    uv pip install -r meta/ee-requirements.txt
    ade install --editable --no-seed --venv .venv .
    ade install --no-seed --venv .venv -r extensions/molecule/requirements.yml
    ```

You are now ready to begin developing the collection. Please familiarize yourself with the [Ansible community guide](https://docs.ansible.com/ansible/devel/community/index.html).

When you are ready to merge your changes from your fork, create a pull request in this repository.

## Adding a new development dependency

Add a new development dependency using `uv`:

```bash
uv add <package> --dev
```

## Adding a new Python collection dependency

Add a new Python collection dependency by adding it to the [`meta/ee-requirements.txt`](meta/ee-requirements.txt). The Python dependency must be version constrained.

## Running Molecule tests

The `community.beszel` Ansible collection uses [Molecule](https://ansible.readthedocs.io/projects/molecule/index.html) to test the roles in the collection. You must have [Docker](https://docs.docker.com/engine/install/) installed to run the Molecule scenarios.

Run the Molecule scenarios:

```bash
cd extensions
uv run molecule test --all
```

## Adding a new Molecule collection dependency

The Molecule scenarios rely on collection dependencies. Add a new one by modifying the [`extensions/molecule/requirements.yml`](extensions/molecule/requirements.yml).

## Running default nox sessions

The `community.beszel` Ansible collection uses [`antsibull-nox`](https://docs.ansible.com/projects/antsibull-nox/) to run various checks on the collection and its content. The default nox sessions include: `lint`, `formatters`, `codeqa`, `yamllint`, `antsibull-nox-config`, `docs-check`, `extra-checks`, and `build-import-check`.

It is highly recommended to run the default nox sessions before committing your changes.

Run the default nox sessions:

```bash
uv run nox
```

## Running Integration tests

The `community.beszel` Ansible collection uses [`antsibull-nox`](https://docs.ansible.com/projects/antsibull-nox/) to run integration tests for the modules in the collection. You must have [Docker](https://docs.docker.com/engine/install/) installed to run the integration tests.

Run the integration tests:

```bash
uv run nox -e ansible-test-integration
```

## Running Unit tests

The `community.beszel` Ansible collection uses [`antsibull-nox`](https://docs.ansible.com/projects/antsibull-nox/) to run unit tests for the modules in the collection. You must have [Docker](https://docs.docker.com/engine/install/) installed to run the unit tests.

Run the unit tests:

```bash
uv run nox -e ansible-test-units
```

## Running Sanity checks

The `community.beszel` Ansible collection uses [`antsibull-nox`](https://docs.ansible.com/projects/antsibull-nox/) to perform sanity checks for the modules in the collection. You must have [Docker](https://docs.docker.com/engine/install/) installed to run the sanity tests.

Run the sanity checks:

```bash
uv run nox -e ansible-test-sanity
```

## Running Ansible Lint

The `community.beszel` Ansible collection uses [`ansible-lint`](http://ansible.readthedocs.io/projects/lint/) to lint Ansible roles and playbooks located in the `roles` and `playbooks` directories respectively. The collection uses [`antsibull-nox`](https://docs.ansible.com/projects/antsibull-nox/) to run `ansible-lint`.

Run `ansible-lint`:

```bash
uv run nox -e ansible-lint
```

## Adding a new Python integration tests dependency

Add a new Python integration tests dependency by adding it to the [`tests/integration/requirements.txt`](tests/integration/requirements.txt).

## Creating a changelog fragment

The `community.beszel` Ansible collection uses [antsibull-changelog](https://github.com/ansible-community/antsibull-changelog) for generating the changelog. When make any changes to the collection, you need to create a changelog fragment in [`changelogs/fragments`](changelogs/fragments/) outlining the details of your changes. There are several [options](https://ansible.readthedocs.io/projects/antsibull-changelog/changelog.yaml-format/#changes) that you can use in your fragment. If you are unsure and need help with this step, please ask one of the collection [MAINTAINERS](MAINTAINERS).
