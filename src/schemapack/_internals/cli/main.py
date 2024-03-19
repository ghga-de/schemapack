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

from pathlib import Path
from typing import Annotated

import typer

from schemapack import __version__, exceptions
from schemapack._internals.cli import exit_codes
from schemapack._internals.cli.utils import (
    print_exception,
    print_failure,
    print_info,
    print_success,
)
from schemapack._internals.main import load_and_validate

cli = typer.Typer()


def version_callback(
    version: bool = False,
):
    if version:
        print_info(__version__)
        raise typer.Exit(exit_codes.SUCCESS)


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
        print_exception(error, exception_name="ValidationError")
        print_failure(
            "The datapack is invalid.",
        )
        raise typer.Exit(exit_codes.VALIDATION_ERROR) from None

    except exceptions.DataPackSpecError as error:
        print_exception(error, exception_name="DataPackSpecError")
        print_failure(
            "The provided datapack did not comply with the specs of a datapack."
        )
        raise typer.Exit(exit_codes.DATAPACK_SPEC_ERROR) from None

    except exceptions.SchemaPackSpecError as error:
        print_exception(error, exception_name="SchemaPackSpecError")
        print_failure(
            "The provided schemapack did not comply with the specs of a schemapack."
        )
        raise typer.Exit(exit_codes.SCHEMAPACK_SPEC_ERROR) from None

    print_success("The datapack is valid.")
