# Installation
# =========================

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



# Usage:
# =========================

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
