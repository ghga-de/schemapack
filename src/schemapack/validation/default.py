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

"""Default Validation Plugin Registry"""

from schemapack.validation.base import (
    ClassValidationPlugin,
    GlobalValidationPlugin,
    ResourceValidationPlugin,
)
from schemapack.validation.plugins import (
    ContentSchemaValidationPlugin,
    ExpectedRootValidationPlugin,
    MissingClassSlotValidationPlugin,
    MissingMandatoryOriginValidationPlugin,
    MissingMandatoryTargetValidationPlugin,
    MissingRelationValidationPlugin,
    MultipleTargetValidationPlugin,
    TargetIdValidationPlugin,
    TargetOverlapValidationPlugin,
    UnexpectedRootValidationPlugin,
    UnknownClassSlotValidationPlugin,
    UnknownRelationValidationPlugin,
    UnkownRootResourceValidationPlugin,
)

DEFAULT_GLOBAL_PLUGIN_REGISTRY: list[type[GlobalValidationPlugin]] = [
    MissingClassSlotValidationPlugin,
    UnknownClassSlotValidationPlugin,
    ExpectedRootValidationPlugin,
    UnkownRootResourceValidationPlugin,
    UnexpectedRootValidationPlugin,
]
DEFAULT_CLASS_PLUGIN_REGISTRY: list[type[ClassValidationPlugin]] = [
    TargetOverlapValidationPlugin,
    MissingMandatoryOriginValidationPlugin,
]
DEFAULT_RESOURCE_PLUGIN_REGISTRY: list[type[ResourceValidationPlugin]] = [
    ContentSchemaValidationPlugin,
    TargetIdValidationPlugin,
    MissingRelationValidationPlugin,
    UnknownRelationValidationPlugin,
    MultipleTargetValidationPlugin,
    MissingMandatoryTargetValidationPlugin,
]
