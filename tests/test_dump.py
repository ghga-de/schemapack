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

"""Test dumping a schemapack."""

import json
from pathlib import Path

import pytest
import ruamel.yaml

from schemapack import dump_schemapack, load_schemapack
from tests.fixtures.examples import VALID_SCHEMAPACK_PATHS

yaml = ruamel.yaml.YAML(typ="safe")


@pytest.mark.parametrize(
    "yaml_format", [True, False], ids=["yaml_format", "json_format"]
)
def test_dump_condensed(yaml_format: bool, tmp_path: Path):
    """Tests using the dump_schemapack function to dump a schemapack as a
    condensed representation to file.
    """
    input_schemapack = load_schemapack(VALID_SCHEMAPACK_PATHS["simple_relations"])
    expected_dict = yaml.load(VALID_SCHEMAPACK_PATHS["simple_relations_condensed"])
    output_path = tmp_path / "output.schemapack.yaml"

    dump_schemapack(input_schemapack, path=output_path, yaml_format=yaml_format)
    if yaml_format:
        observed_dict = yaml.load(output_path)
    else:
        with open(output_path, encoding="utf-8") as file:
            observed_dict = json.load(file)

    assert observed_dict == expected_dict


def test_dump_not_condensed(tmp_path: Path):
    """Tests using the dump_schemapack function to dump a schemapack as a representation
    to file with content schemas being written to dedicated files.
    """
    input_path = VALID_SCHEMAPACK_PATHS["simple_relations"]
    input_schemapack = load_schemapack(input_path)
    expected_dict = yaml.load(input_path)
    schemapack_dir = tmp_path / "schemapack" / "valid"
    output_path = schemapack_dir / "output.schemapack.yaml"
    rel_content_schema_path = Path("../../content_schemas/")

    schemapack_dir.mkdir(parents=True)

    dump_schemapack(
        input_schemapack,
        path=output_path,
        condensed=False,
        content_schema_dir=rel_content_schema_path,
    )

    # check schemapack file itself:
    observed_dict = yaml.load(output_path)
    assert observed_dict == expected_dict

    # check content schema files:
    for class_name, class_ in input_schemapack.classes.items():
        content_schema_path = (
            schemapack_dir / rel_content_schema_path / f"{class_name}.schema.json"
        )
        with open(content_schema_path, encoding="utf-8") as file:
            observed_content_schema = json.load(file)
        assert observed_content_schema == class_.content.json_schema_dict
