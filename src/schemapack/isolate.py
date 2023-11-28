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

"""Logic to isolate a resource from a non-rooted datapack to created a rooted datapack."""

from schemapack.spec.datapack import ClassName, DataPack, ResourceId


def isolate(
    *, datapack: DataPack, resource_class: ClassName, resource_id: ResourceId
) -> DataPack:
    """Isolate a resource from a non-rooted datapack to created a rooted datapack. I.e.
    the resulting datapack will only contain resources referenced by the root resource
    as well as the root resource itself.
    """
    raise NotImplementedError
