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

"""Models for describing and working with datapack definitions."""

import typing
from typing import Any, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import TypeAlias

SupportedDataPackVersions = Literal["0.1.0"]
SUPPORTED_DATA_PACK_VERSIONS = typing.get_args(SupportedDataPackVersions)

ClassName: TypeAlias = str
ResourceId: TypeAlias = str
RelationName: TypeAlias = str


class NoExtraBaseModel(BaseModel):
    """A BaseModel that does not allow any extra fields."""

    model_config = ConfigDict(use_enum_values=True, extra="forbid")


class Resource(NoExtraBaseModel):
    """A model defining content and relations of a resource
    of a specific class.
    """

    content: dict[str, Any] = Field(
        ...,
        description=(
            "The content of the resource that complies with the content schema defined"
            + " in the corresponding schemapack."
        ),
    )

    relations: dict[
        RelationName, Union[Optional[ResourceId], list[ResourceId]]
    ] = Field(
        {},
        description=(
            "A dictionary containing the relations of the resource to other resources."
            + " Each key correspond to the name of a relation property as per the"
            + " schemapack definition. Each value could be one of the following types"
            + " depending on the corresponding schemapack definition:"
            + " (1) a id of a single target resource (multiple.target is False),"
            + " (2) None (multiple.target and mandatory.target are both False),"
            + " (3) a list of ids of target resources (multiple.target is True),"
            + " (4) an empty list (multiple.target is True and mandatory.target is"
            + " False)."
        ),
    )

    def get_target_id_list(self, relation_name: RelationName) -> list[ResourceId]:
        """Get the target ids for the given relation always represented as a list.
        This is even the case if the actual value in the relations dict is a single
        string (translated into a list of length one) or None (translated into an
        empty list).

        Raises:
            KeyError: If the given relation name does not exist in the relations dict.

        """
        targets = self.relations[relation_name]
        if targets is None:
            return []
        if isinstance(targets, list):
            return targets
        return [targets]


class DataPack(NoExtraBaseModel):
    """A model for describing a schemapack definition."""

    datapack: SupportedDataPackVersions = Field(
        ...,
        description=(
            "Has two purposes: (1) it clearly identifies a YAML/JSON document as"
            + " a datapack definition and (2) it specifies the used version of the"
            + " datapack specification."
        ),
    )

    resources: dict[ClassName, dict[ResourceId, Resource]] = Field(
        ...,
        description=(
            "A nested dictionary containing resources per class name (keys on the first"
            + " level) and resource ID (keys on the second level). Each class defined"
            + " in the schemapack must be present even if no resources are defined for"
            + " it in this datapack."
        ),
    )

    root_resource: Optional[str] = Field(
        None,
        description=(
            "Defines the id of the resource that should act as root. This means"
            + " that, in addition to the root resource itself, the datapack must only"
            + " contain resources that are direct or indirect (dependencies of"
            + " dependencies) of the root resource."
            + " Please note, the datapack must define a root resource if the"
            + " corresponding schemapack defines a root class and vice versa."
        ),
    )
