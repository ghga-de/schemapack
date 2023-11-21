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

"""Tests the load module."""

from contextlib import nullcontext
from pathlib import Path

import pytest

from schemapack.exceptions import DataPackSpecError, SchemaPackSpecError
from schemapack.load import load_datapack, load_schemapack
from tests.fixtures.examples import (
    INVALID_DATAPACK_PATHS,
    INVALID_SCHEMAPACK_PATHS,
    VALID_DATAPACK_PATHS,
    VALID_SCHEMAPACK_PATHS,
)


@pytest.mark.parametrize(
    "path", VALID_SCHEMAPACK_PATHS.values(), ids=VALID_SCHEMAPACK_PATHS
)
def test_load_schemapack_valid(path: Path):
    """Test loading valid schemapacks."""
    _ = load_schemapack(path)


@pytest.mark.parametrize(
    "name, path", INVALID_SCHEMAPACK_PATHS.items(), ids=INVALID_SCHEMAPACK_PATHS
)
def test_load_schemapack_invalid(name: str, path: Path):
    """Test loading invalid schemapacks."""
    error_type = name.split(".")[0]

    with pytest.raises(SchemaPackSpecError) as exception_info:
        _ = load_schemapack(path)

    error_details = exception_info.value.details
    assert len(error_details) == 1

    assert error_details[0]["type"] == error_type


@pytest.mark.parametrize(
    "path", VALID_DATAPACK_PATHS.values(), ids=VALID_DATAPACK_PATHS
)
def test_load_datapack_valid(path: Path):
    """Test loading valid datapacks."""
    _ = load_datapack(path)


@pytest.mark.parametrize(
    "name, path", INVALID_DATAPACK_PATHS.items(), ids=INVALID_DATAPACK_PATHS
)
def test_load_datapack_invalid(name: str, path: Path):
    """Test loading invalid datapacks."""
    error_type = name.split(".")[1]

    with pytest.raises(
        DataPackSpecError
    ) if error_type == "DataPackSpecError" else nullcontext():
        _ = load_datapack(path)
