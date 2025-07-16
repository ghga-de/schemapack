[![tests](https://github.com/ghga-de/$repo_name/actions/workflows/tests.yaml/badge.svg)](https://github.com/ghga-de/$repo_name/actions/workflows/tests.yaml)
[![Coverage Status](https://coveralls.io/repos/github/ghga-de/$repo_name/badge.svg?branch=main)](https://coveralls.io/github/ghga-de/$repo_name?branch=main)
[![PyPI version shields.io](https://img.shields.io/pypi/v/$repo_name.svg)](https://pypi.python.org/pypi/$repo_name/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/$repo_name.svg)](https://pypi.python.org/pypi/$repo_name/)

# $title

$summary

## Description

$description

## Installation

This package is available at PyPI:
https://pypi.org/project/schemapack

Install:
```
bash

pip install $shortname
```

Upgrade:
```
pip install --upgrade $shortname
```

## Usage

```
bash

$shortname --help

$usage
```
## Quick Start

$quick_start


## Documentation

- [SchemaPack specification](./docs/schemapack_spec.md)
- [DataPack specification](./docs/datapack_spec.md)
- [Data isolation](./docs/data_isolation.md)


## Development

For setting up the development environment, we rely on the
[devcontainer feature](https://code.visualstudio.com/docs/remote/containers) of VS Code
in combination with Docker Compose.

To use it, you have to have Docker Compose as well as VS Code with its "Remote - Containers"
extension (`ms-vscode-remote.remote-containers`) installed.
Then open this repository in VS Code and run the command
`Remote-Containers: Reopen in Container` from the VS Code "Command Palette".

This will give you a full-fledged, pre-configured development environment including:
- infrastructural dependencies of the service (databases, etc.)
- all relevant VS Code extensions pre-installed
- pre-configured linting and auto-formatting
- a pre-configured debugger
- automatic license-header insertion

Moreover, inside the devcontainer, a command `dev_install` is available for convenience.
It installs the service with all development dependencies, and it installs pre-commit.

The installation is performed automatically when you build the devcontainer. However,
if you update dependencies in the [`pyproject.toml`](pyproject.toml) or the
[`requirements-dev.txt`](lock/requirements-dev.txt), please run it again.


## License

This repository is free to use and modify according to the
[Apache 2.0 License](./LICENSE).

## README Generation

This README file is auto-generated, please see [`readme_generation`](.readme_generation/README.md)
for details.
