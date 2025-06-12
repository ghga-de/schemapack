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


### Usage:

To view the help message:

```
bash

$shortname --help
```

```
Usage: schemapack [OPTIONS] COMMAND [ARGS]...

Common arguments and options.

Options
    --version                     Show the version of the library and exit.
    --install-completion          Install completion for the current shell.
    --show-completion             Show completion for the current shell, to copy it or
                                    customize the installation.
    --help                        Show this message and exit.


Commands
    validate              Validate a datapack against a schemapack.
    check-schemapack      Check if the provided JSON/YAML document complies with
                            the schemapack specs.
    check-datapack        Check if the provided JSON/YAML document complies with
                            the datapack specs.
    condense-schemapack   Writes a condensed version of the provided schemapack that
                            contains content schemas to stdout.
    isolate-resource      Isolate a resource from the given datapack and write a datapack
                            that is rooted to this resource to stdout.
    isolate-class         Isolate a class from the given schemapack and write a condensed
                            (with content schemas being embedded) schemapack that is
                            rooted to this class to stdout.
    export-mermaid        Generate an entity relationship diagram based on the mermaid
                            markup from the provided schemapack.

```

## Architecture and Design:
$design_description

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
if you update dependencies in the [`./pyproject.toml`](./pyproject.toml) or the
[`./requirements-dev.txt`](./requirements-dev.txt), please run it again.

## License

This repository is free to use and modify according to the
[Apache 2.0 License](./LICENSE).

## README Generation

This README file is auto-generated, please see [`readme_generation.md`](./readme_generation.md)
for details.
