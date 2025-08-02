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
    ```

Finally, please familiarize yourself with the [Ansible community guide](https://docs.ansible.com/ansible/devel/community/index.html).

## Adding a new development dependency

Add a new development dependency using `uv`:

```bash
uv add <package> --dev
```

## Adding a new Python collection dependency

Add a new Python collection dependency by adding it to the [`meta/ee-requirements.txt`](meta/ee-requirements.txt). The Python dependency should be version constrained.
