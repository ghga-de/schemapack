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

"""Public details about the command line interface."""

from schemapack._internals.cli import (
    DATAPACK_SPEC_ERROR_CODE as DATAPACK_SPEC_ERROR,
)
from schemapack._internals.cli import (
    SCHEMAPACK_SPEC_ERROR_CODE as SCHEMAPACK_SPEC_ERROR,
)
from schemapack._internals.cli import (
    SUCCESS_CODE as SUCCESS,
)
from schemapack._internals.cli import (
    VALIDATION_ERROR_CODE as VALIDATION_ERROR,
)

__all__ = [
    "SCHEMAPACK_SPEC_ERROR",
    "DATAPACK_SPEC_ERROR",
    "SUCCESS",
    "VALIDATION_ERROR",
]
