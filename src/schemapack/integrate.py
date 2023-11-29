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

"""Integrate rooted datapacks into nested json objects."""

from typing_extensions import TypeAlias

from schemapack.spec.datapack import DataPack
from schemapack.spec.schemapack import SchemaPack

JsonObjectCompatible: TypeAlias = dict[str, object]


def integrate(*, datapack: DataPack, schemapack: SchemaPack) -> JsonObjectCompatible:
    """Integrate a rooted datapack into a nested json object-compatible data structure.
    It is assumed that the provided datapack has already been validated against the
    provided schemapack.

    Args:
        datapack:
            The datapack to be integrated. Must be rooted.
        schemapack:
            The schemapack to be used for looking up the classes of relations.

    Raises:
        ValueError:
            If the datapack is not rooted.
        schemapack.exceptions.ValidationAssumptionError:
            If the datapack is not valid against the schemapack.
        schemapack.exceptions.CircularRelationError:
            If a circular relation is detected.
    """
    raise NotImplementedError()
