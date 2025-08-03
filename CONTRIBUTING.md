# Contributing

## Getting Started

The `community.beszel` Ansible collection uses [uv](https://docs.astral.sh/uv/) and [Ansible Development Environment (ADE)](https://github.com/ansible/ansible-dev-environment) for collection development. The recommended method for [installing](https://github.com/ansible/ansible-dev-environment?tab=readme-ov-file#installation) ADE is using [`uv`](https://docs.astral.sh/uv/):

```bash
uv tool install ansible-dev-environment
```

Once ADE is installed, follow the steps below for contributing to `community.beszel`:

1. Clone the `community.beszel` collection:

    ```bash
    git clone https://github.com/ansible-collections/community.beszel.git
    cd community.beszel
    ```

2. Create your feature branch:

    ```bash
    git checkout -b feature/my-new-feature
    ```

3. Initialize the development environment using `uv` and ADE:

    ```bash
    uv sync --dev
    uv pip install -r meta/ee-requirements.txt
    ade install --editable --no-seed --ansible-core-version 2.18.7 --venv .venv .
    ade install --no-seed --ansible-core-version 2.18.7 --venv .venv -r extensions/molecule/requirements.yml
    ```

You are now ready to begin developing the collection. Please familiarize yourself with the [Ansible community guide](https://docs.ansible.com/ansible/devel/community/index.html).

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
molecule test --all
```
