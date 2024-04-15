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

from contextlib import contextmanager
from pathlib import Path

import typer

from schemapack._internals.cli import exit_codes
from schemapack._internals.cli.printing import print_final_failure


@contextmanager
def check_force(output: Path, force: bool):
    """Check if the output file exists and if so, whether to overwrite it."""
    if output.exists() and not force:
        print_final_failure(
            "The specified output file exists. Use --force to overwrite."
        )
        raise typer.Exit(exit_codes.OUTPUT_EXISTS) from None
    yield