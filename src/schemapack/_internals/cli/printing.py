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

"""Utilities for implementing a CLI"""

import rich.console
import rich.panel

EXCEPTION_CONSOLE = rich.console.Console(stderr=True, style="red")
SUCCESS_CONSOLE = rich.console.Console(style="green bold")
FAILURE_CONSOLE = rich.console.Console(style="red bold")
INFO_CONSOLE = rich.console.Console()


def print_exception(exception: Exception, exception_name: str = "Exception"):
    """Print an exception."""
    EXCEPTION_CONSOLE.print(rich.panel.Panel(str(exception), title=exception_name))


def print_success(
    message: str,
):
    """Print a final message indicating success."""
    SUCCESS_CONSOLE.print(message)


def print_failure(
    message: str,
):
    """Print a final message indicating failure."""
    FAILURE_CONSOLE.print(message)


def print_info(
    message: str,
):
    """Print non-rated message."""
    FAILURE_CONSOLE.print(message)
