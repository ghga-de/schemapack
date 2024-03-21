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
    EXAMPLES_DIR,
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
    """Test the validate command with a valid datapack."""
    schemapack = VALID_SCHEMAPACK_PATHS["simple_relations"]
    datapack = VALID_DATAPACK_PATHS["simple_relations.simple_resources"]

    result = runner.invoke(
        cli,
        generate_validate_command(
            schemapack=schemapack, datapack=datapack, abbreviate=abbreviate
        ),
    )
    assert result.exit_code == exit_codes.SUCCESS == 0


@pytest.mark.parametrize(
    "abbreviate", [True, False], ids=["abbreviate", "no_abbreviate"]
)
def test_validate_invalid(abbreviate: bool):
    """Test the validate command with an invalid datapack."""
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
    assert "ContentValidationError" in result.stderr


@pytest.mark.parametrize(
    "abbreviate", [True, False], ids=["abbreviate", "no_abbreviate"]
)
def test_validate_datapack_spec_error(abbreviate: bool):
    """Test the validate command with a datapack that does not comply with the specs."""
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
    assert "DataPackSpecError" in result.stderr


@pytest.mark.parametrize(
    "abbreviate", [True, False], ids=["abbreviate", "no_abbreviate"]
)
def test_validate_schemapack_spec_error(abbreviate: bool):
    """Test the validate command with a schemapack that does not comply with the specs."""
    schemapack = INVALID_SCHEMAPACK_PATHS["ContentSchemaNotFoundError"]
    datapack = VALID_DATAPACK_PATHS["simple_relations.simple_resources"]

    result = runner.invoke(
        cli,
        generate_validate_command(
            schemapack=schemapack, datapack=datapack, abbreviate=abbreviate
        ),
    )
    assert result.exit_code == exit_codes.SCHEMAPACK_SPEC_ERROR != 0
    assert "SchemaPackSpecError" in result.stderr


def test_check_schemapack_complies():
    """Test the check-schemapack command with a complies document."""
    schemapack = VALID_SCHEMAPACK_PATHS["simple_relations"]

    result = runner.invoke(cli, ["check-schemapack", str(schemapack)])
    assert result.exit_code == exit_codes.SUCCESS == 0


def test_check_schemapack_not_complies():
    """Test the check-schemapack command with a non compliant document."""
    schemapack = INVALID_SCHEMAPACK_PATHS["ContentSchemaNotFoundError"]

    result = runner.invoke(cli, ["check-schemapack", str(schemapack)])
    assert result.exit_code == exit_codes.SCHEMAPACK_SPEC_ERROR != 0
    assert "SchemaPackSpecError" in result.stderr


def test_check_datapack_complies():
    """Test the check-datapack command with a complies document."""
    datapack = VALID_DATAPACK_PATHS["simple_relations.simple_resources"]

    result = runner.invoke(cli, ["check-datapack", str(datapack)])
    assert result.exit_code == exit_codes.SUCCESS == 0


def test_check_datapack_not_complies():
    """Test the check-datapack command with a non compliant document."""
    datapack = INVALID_DATAPACK_PATHS[
        "simple_relations.DataPackSpecError.DuplicateTargetIdError"
    ]

    result = runner.invoke(cli, ["check-datapack", str(datapack)])
    assert result.exit_code == exit_codes.DATAPACK_SPEC_ERROR != 0
    assert "DataPackSpecError" in result.stderr


@pytest.mark.parametrize(
    "props,example_suffix", [([], "_wo_props.mm.txt"), (["-p"], "_w_props.mm.txt")]
)
def test_export_mermaid(tmp_path, props: list[str], example_suffix: str):
    """Test the export-mermaid command."""
    example = "comprehensive_cardinalities_and_types"
    schemapack = VALID_SCHEMAPACK_PATHS[example]
    output_path = tmp_path / "output.mermaid"
    expected_output_path = EXAMPLES_DIR / "mermaid" / f"{example}{example_suffix}"

    args = [
        "export-mermaid",
        str(schemapack),
        str(output_path),
        *props,
    ]
    result = runner.invoke(cli, args)
    assert result.exit_code == exit_codes.SUCCESS == 0
    assert output_path.read_text() == expected_output_path.read_text()


def test_export_mermaid_force(tmp_path):
    """Test the export-mermaid command force overwrite guard."""
    example = "comprehensive_cardinalities_and_types"
    schemapack = VALID_SCHEMAPACK_PATHS[example]
    output_path = tmp_path / "output.mermaid"
    dummy_content = "dummy content"

    args = [
        "export-mermaid",
        str(schemapack),
        str(output_path),
    ]
    output_path.write_text(dummy_content)
    result = runner.invoke(cli, args)
    assert result.exit_code == exit_codes.OUTPUT_EXISTS != 0
    assert output_path.read_text() == dummy_content

    result = runner.invoke(cli, [*args, "--force"])
    assert result.exit_code == exit_codes.SUCCESS == 0
    assert output_path.read_text() != dummy_content
