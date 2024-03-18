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

"""Describes a command line interface"""

from enum import Enum
from pathlib import Path
from typing import Annotated, Final

import typer

from schemapack import __version__, exceptions
from schemapack._internals.main import load_and_validate

# exit codes:
SUCCESS_CODE: Final = 0
VALIDATION_ERROR_CODE: Final = 10
DATAPACK_SPEC_ERROR_CODE: Final = 20
SCHEMAPACK_SPEC_ERROR_CODE: Final = 30


class MessageLevel(str, Enum):
    """The level of the message."""

    INFO = "info"
    ERROR = "error"
    SUCCESS = "success"


LEVEL_COLOR_MAP = {
    MessageLevel.INFO: typer.colors.BLUE,
    MessageLevel.ERROR: typer.colors.RED,
    MessageLevel.SUCCESS: typer.colors.GREEN,
}


def echo(message: str, *, level: MessageLevel, stderr: bool = False):
    """Print a message colored depending on the level.
    Optionally, write to stderr, if `stderr` is True.
    """
    styled_message = typer.style(text=message, fg=LEVEL_COLOR_MAP[level])
    typer.echo(styled_message, err=stderr)


cli = typer.Typer()


def version_callback(
    version: bool = False,
):
    if version:
        echo(str(__version__), level=MessageLevel.INFO)
        raise typer.Exit(SUCCESS_CODE)


@cli.callback()
def common(
    ctx: typer.Context,
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            callback=version_callback,
            help="Show the version of the library and exit.",
        ),
    ] = False,
):
    """Common arguments and options."""
    pass


@cli.command()
def validate(
    *,
    schemapack: Annotated[
        Path,
        typer.Option(
            "--schemapack",
            "-s",
            help="Provide the path to a schemapack to validate against.",
        ),
    ],
    datapack: Annotated[
        Path,
        typer.Option(
            "--datapack", "-d", help="Provide the path to a datapack to validate."
        ),
    ],
):
    """Validate a datapack against a schemapack."""
    try:
        load_and_validate(schemapack_path=schemapack, datapack_path=datapack)

    except exceptions.ValidationError as error:
        echo(str(error), level=MessageLevel.ERROR, stderr=True)
        echo("The datapack is invalid.", level=MessageLevel.ERROR, stderr=False)
        raise typer.Exit(VALIDATION_ERROR_CODE) from None

    except exceptions.DataPackSpecError as error:
        echo(str(error), level=MessageLevel.ERROR, stderr=True)
        echo(
            "The provided datapack did not comply with the specs of a datapack.",
            level=MessageLevel.ERROR,
            stderr=False,
        )
        raise typer.Exit(DATAPACK_SPEC_ERROR_CODE) from None

    except exceptions.SchemaPackSpecError as error:
        echo(str(error), level=MessageLevel.ERROR, stderr=True)
        echo(
            "The provided schemapack did not comply with the specs of a schemapack.",
            level=MessageLevel.ERROR,
            stderr=False,
        )
        raise typer.Exit(SCHEMAPACK_SPEC_ERROR_CODE) from None

    echo("The datapack is valid.", level=MessageLevel.SUCCESS)
