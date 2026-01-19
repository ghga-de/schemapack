# Copyright 2021 - 2025 Universität Tübingen, DKFZ, EMBL, and Universität zu Köln
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

"""Test schema comparison functionality."""

from pathlib import Path

import pytest

from schemapack import load_schemapack
from schemapack._internals.compare import compare_schemapacks
from tests.fixtures.examples import COMPARISON_SCHEMAPACK_PATHS

# Expected comparison results for each test case
# True indicates schemapacks should be considered equal
EXPECTED_RESULTS = {
    "equal_schemas_optional_untyped_property": True,
    "equal_schemas_with_relations": True,
    "unequal_schemas_different_classes": False,
    "unequal_schemas_different_relation_spec": False,
    "unequal_schemas_different_content": False,
}


@pytest.mark.parametrize(
    "case_name, schema1_path, schema2_path", COMPARISON_SCHEMAPACK_PATHS
)
def test_schemapack_comparison(case_name: str, schema1_path: Path, schema2_path: Path):
    """Test comparing two schemapacks semantically."""
    schema1 = load_schemapack(schema1_path)
    schema2 = load_schemapack(schema2_path)

    assert compare_schemapacks(schema1, schema2) == EXPECTED_RESULTS[case_name]
