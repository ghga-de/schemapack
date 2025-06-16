[![tests](https://github.com/ghga-de/schemapack/actions/workflows/tests.yaml/badge.svg)](https://github.com/ghga-de/schemapack/actions/workflows/tests.yaml)
[![Coverage Status](https://coveralls.io/repos/github/ghga-de/schemapack/badge.svg?branch=main)](https://coveralls.io/github/ghga-de/schemapack?branch=main)
[![PyPI version shields.io](https://img.shields.io/pypi/v/schemapack.svg)](https://pypi.python.org/pypi/schemapack/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/schemapack.svg)](https://pypi.python.org/pypi/schemapack/)

# Schemapack

Make your JSON Schemas sociable and create linked data model.

## Description

<!-- Please provide a short overview of the features of this service. -->

Schemapack is a lightweight data modeling framework that defines two components: a schemapack for describing linked data structures, and a datapack for representing instance data that conforms to those structures.


Schemapack builds on JSON Schema to describe the structure of individual resources. In addition, it defines how resources are linked to each other. Links are described in terms of multiplicity (e.g. one-to-one, one-to-many) and mandatoriness (required or optional). Resources refer to one another by ID, rather than by embedding, which avoids redundancy and simplifies reference resolution.

Validation is built into the framework. Schemapack uses JSON Schema to validate the content of each resource. It includes additional validators to verify datapacks and schemapack's compliance with the modeling language specifications. For validation across resources, it extends the validation layer to check:
* Reference integrity
* Multiplicity constraints
* Mandatoriness of references

Schemapack includes tooling to isolate individual resources and their dependencies from larger datasets. This can be useful for partial extraction, targeted validation, or incremental processing.


## Documentation

- Installation and usage instructions: [docs/installation.md](./docs/installation_usage.md)
- SchemaPack specification: [docs/schemapack_spec.md](./docs/schemapack_spec.md)
- DataPack specification: [docs/datapack_spec.md](./docs/datapack_spec.md)
- Quickstart guide: [docs/quickstart.md](./docs/quickstart.md)
- Development guide: [docs/development.md](./docs/development.md)


## License

This repository is free to use and modify according to the
[Apache 2.0 License](./LICENSE).

## README Generation

This README file is auto-generated, please see [`readme_generation.md`](./readme_generation.md)
for details.
