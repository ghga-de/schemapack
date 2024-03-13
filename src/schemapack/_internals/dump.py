# Copyright 2021 - 2023 Universität Tübingen, DKFZ, EMBL, and Universität zu Köln
# for the German Human Genome-Phenome Archive (GHGA)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""Logic for dumping schemapacks."""

from pathlib import Path

from schemapack._internals.spec.schemapack import SchemaPack


def dumps_schemapack(schemapack: SchemaPack, yaml_format: bool = True) -> str:
    """Dumps a condensed version (i.e. with content schemas embedded) of the provided
    schemapack as a JSON or YAML formatted string.

    Args:
        schemapack:
            The schemapack to dump.
        yaml_format:
            Whether to dump as YAML (`True`) or JSON (`False`).
    """
    raise NotImplementedError


def dump_schemapack(
    schemapack: SchemaPack,
    *,
    path: Path,
    condensed: bool = True,
    content_schema_dir: Path = Path("content_schemas"),
    yaml_format: bool = True,
) -> None:
    """Dumps the provided schemapack as a JSON or YAML file to the provided path.

    Args:
        schemapack:
            The schemapack to dump.
        path:
            The path to write the output to.
        condensed:
            Whether to dump a condensed version (i.e. with content schemas embedded) of
            the provided schemapack.
        content_schema_dir:
            The path to the directory used to output the content schemas of individual
            classes defined in the provided schemapack as separate files. The path is
            relative to the `path` of the schemapack. If it does not exist, it will be
            created. Please note, this is only relevant if `condensed` is set to
            `False`.
        yaml_format:
            Whether to dump as YAML (`True`) or JSON (`False`).
    """
    ...
