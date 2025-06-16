[![tests](https://github.com/ghga-de/schemapack/actions/workflows/tests.yaml/badge.svg)](https://github.com/ghga-de/schemapack/actions/workflows/tests.yaml)
[![Coverage Status](https://coveralls.io/repos/github/ghga-de/schemapack/badge.svg?branch=main)](https://coveralls.io/github/ghga-de/schemapack?branch=main)
[![PyPI version shields.io](https://img.shields.io/pypi/v/schemapack.svg)](https://pypi.python.org/pypi/schemapack/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/schemapack.svg)](https://pypi.python.org/pypi/schemapack/)

# Schemapack

Make your JSON Schemas sociable and create linked data model.

## Description

<!-- Please provide a short overview of the features of this service. -->

Schemapack is a lightweight data modeling framework that defines two components: a schemapack for describing linked data structures, and a datapack for representing instance data that conforms to those structures.


<!-- Schemapack builds on JSON Schema to describe the structure of individual resources. In addition, it defines how resources are linked to each other. Links are described in terms of multiplicity (e.g. one-to-one, one-to-many) and mandatoriness (required or optional). Resources refer to one another by ID, rather than by embedding, which avoids redundancy and simplifies reference resolution.

Schemapack is suitable for ETL operations that transform a model and its corresponding data into other model and data representations. It is designed to support such transformations in a structured and consistent manner.

Validation is built into the framework. SJSON Schema is used to validate the internal structure of each resource. For validating links across resources, Schemapack includes an extended validation layer that checks reference integrity and enforces multiplicity and mandatoriness constraints.

Schemapack includes tooling to isolate individual resources and their dependencies from larger datasets. This can be useful for partial extraction, targeted validation, or incremental processing. -->

### Specification

bok la la

## Installation

This package is available at PyPI:
https://pypi.org/project/schemapack

Install:
```
bash

pip install schemapack
```

Upgrade:
```
pip install --upgrade schemapack
```


### Usage:

To view the help message:

```
bash

schemapack --help
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

### Quick Start:

## Architecture and Design:
<!-- Please provide an overview of the architecture and design of the code base.
Mention anything that deviates from the standard Triple Hexagonal Architecture and
the corresponding structure. -->

This is a Python-based CLI tool.


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
