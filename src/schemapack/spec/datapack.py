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

"""Models representing the datapack spec (part of the public API of this package)."""

from schemapack._internals.spec.datapack import (
    SUPPORTED_DATA_PACK_VERSIONS,
    DataPack,
    Resource,
    SupportedDataPackVersions,
)

__all__ = [
    "DataPack",
    "Resource",
    "SupportedDataPackVersions",
    "SUPPORTED_DATA_PACK_VERSIONS",
]
