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

import ruamel.yaml

from schemapack import dumps_schemapack, load_schemapack
from tests.fixtures.examples import VALID_SCHEMAPACK_PATHS

yaml = ruamel.yaml.YAML(typ="safe")


def test_dumps_yaml():
    """Tests that using the dumps_schemapack function to dump a schemapack as a yaml
    string yields the expected result.
    """
    input_schemapack = load_schemapack(VALID_SCHEMAPACK_PATHS["simple_relations"])
    expected_dict = yaml.load(VALID_SCHEMAPACK_PATHS["simple_relations_condensed"])

    observed_str = dumps_schemapack(input_schemapack)
    observed_dict = yaml.load(observed_str)

    assert observed_dict == expected_dict


def test_dumps_json():
    """Tests that using the dumps_schemapack function to dump a schemapack as a json
    string yields the expected result.
    """
    input_schemapack = load_schemapack(VALID_SCHEMAPACK_PATHS["simple_relations"])
    expected_dict = yaml.load(VALID_SCHEMAPACK_PATHS["simple_relations_condensed"])

    observed_str = dumps_schemapack(input_schemapack, yaml_format=False)
    observed_dict = json.loads(observed_str)

    assert observed_dict == expected_dict
