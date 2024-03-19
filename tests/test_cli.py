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

"""Test the cli.

Please note, these tests will just shallowly test that the cli commands can be called
and produce the expected output. However, the output is not deeply investigated and
only a single senario is tester for each command. More deeper testing is done on the
python API (to avoid redundancy of tests).
"""

from pathlib import Path

import pytest
from typer.testing import CliRunner

import schemapack
from schemapack._internals.cli import cli
from schemapack.cli import exit_codes
from tests.fixtures.examples import (
    INVALID_DATAPACK_PATHS,
    INVALID_SCHEMAPACK_PATHS,
    VALID_DATAPACK_PATHS,
    VALID_SCHEMAPACK_PATHS,
)

runner = CliRunner(mix_stderr=False)


def test_version():
    """Test the version command."""
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == exit_codes.SUCCESS == 0
    assert result.stdout.strip() == str(schemapack.__version__)


def generate_validate_command(
    *, schemapack: Path, datapack: Path, abbreviate: bool
) -> list[str]:
    """Generate a command line to validate a datapack against a schemapack."""
    return [
        "validate",
        "-s" if abbreviate else "--schemapack",
        str(schemapack),
        "-d" if abbreviate else "--datapack",
        str(datapack),
    ]


@pytest.mark.parametrize(
    "abbreviate", [True, False], ids=["abbreviate", "no_abbreviate"]
)
def test_validate_valid(abbreviate: bool):
    """Test validating a valid datapack against a schemapack."""
    schemapack = VALID_SCHEMAPACK_PATHS["simple_relations"]
    datapack = VALID_DATAPACK_PATHS["simple_relations.simple_resources"]

    result = runner.invoke(
        cli,
        generate_validate_command(
            schemapack=schemapack, datapack=datapack, abbreviate=abbreviate
        ),
    )
    assert result.exit_code == exit_codes.SUCCESS == 0
    last_stdout_line = result.stdout.splitlines()[-1]
    assert " valid" in last_stdout_line.lower()


@pytest.mark.parametrize(
    "abbreviate", [True, False], ids=["abbreviate", "no_abbreviate"]
)
def test_validate_invalid(abbreviate: bool):
    """Test validating a invalid datapack against a schemapack."""
    schemapack = VALID_SCHEMAPACK_PATHS["simple_relations"]
    datapack = INVALID_DATAPACK_PATHS[
        "simple_relations.ContentValidationError.missing_property"
    ]

    result = runner.invoke(
        cli,
        generate_validate_command(
            schemapack=schemapack, datapack=datapack, abbreviate=abbreviate
        ),
    )
    assert result.exit_code == exit_codes.VALIDATION_ERROR != 0
    last_stdout_line = result.stdout.splitlines()[-1]
    assert " not valid" in last_stdout_line.lower()
    assert "ContentValidationError" in result.stderr


@pytest.mark.parametrize(
    "abbreviate", [True, False], ids=["abbreviate", "no_abbreviate"]
)
def test_validate_datapack_spec_error(abbreviate: bool):
    """Test validating a invalid datapack against a schemapack."""
    schemapack = VALID_SCHEMAPACK_PATHS["simple_relations"]
    datapack = INVALID_DATAPACK_PATHS[
        "simple_relations.DataPackSpecError.DuplicateTargetIdError"
    ]

    result = runner.invoke(
        cli,
        generate_validate_command(
            schemapack=schemapack, datapack=datapack, abbreviate=abbreviate
        ),
    )
    assert result.exit_code == exit_codes.DATAPACK_SPEC_ERROR != 0
    last_stdout_line = result.stdout.splitlines()[-1]
    assert " spec" in last_stdout_line
    assert "DataPackSpecError" in result.stderr


@pytest.mark.parametrize(
    "abbreviate", [True, False], ids=["abbreviate", "no_abbreviate"]
)
def test_validate_schemapack_spec_error(abbreviate: bool):
    """Test validating a invalid datapack against a schemapack."""
    schemapack = INVALID_SCHEMAPACK_PATHS["ContentSchemaNotFoundError"]
    datapack = VALID_DATAPACK_PATHS["simple_relations.simple_resources"]

    result = runner.invoke(
        cli,
        generate_validate_command(
            schemapack=schemapack, datapack=datapack, abbreviate=abbreviate
        ),
    )
    assert result.exit_code == exit_codes.SCHEMAPACK_SPEC_ERROR != 0
    last_stdout_line = result.stdout.splitlines()[-1]
    assert " spec" in last_stdout_line
    assert "SchemaPackSpecError" in result.stderr
