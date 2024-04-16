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

"""Tests for exporting schemapacks in mermaid format."""

import pytest

from schemapack import load_schemapack
from schemapack.export.mermaid import export_mermaid
from tests.fixtures.examples import EXAMPLES_DIR, VALID_SCHEMAPACK_PATHS


@pytest.mark.parametrize(
    "with_properties, file_suffix",
    [(True, "_w_props.mm.txt"), (False, "_wo_props.mm.txt")],
)
def test_export_mermaid(with_properties: bool, file_suffix: str):
    """Test dumping a schemapack in mermaid format."""
    example = "comprehensive_cardinalities_and_types"
    input_schemapack = load_schemapack(VALID_SCHEMAPACK_PATHS[example])
    expected_output_path = EXAMPLES_DIR / "mermaid" / f"{example}{file_suffix}"

    observed_output = export_mermaid(
        schemapack=input_schemapack, content_properties=with_properties
    )
    assert observed_output == expected_output_path.read_text()
