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

"""Models for describing and working with schemapack definitions."""

import json
import typing
from enum import Enum
from pathlib import Path
from typing import Any, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator
from pydantic_core import PydanticCustomError

SupportedSchemaPackVersions = Literal["0.1.0"]
SUPPORTED_SCHEMA_PACK_VERSIONS = typing.get_args(SupportedSchemaPackVersions)


class Schema(str, Enum):
    """Cardinality of a relation.
    Read as `{this class}_to_{foreign class}`. I.e. MANY_TO_ONE means that this class
    may have many instances that point to the same foreign class instance.
    """

    ONE_TO_ONE = "one_to_one"
    ONE_TO_MANY = "one_to_many"
    MANY_TO_ONE = "many_to_one"
    MANY_TO_MANY = "many_to_many"


class Cardinality(str, Enum):
    """Cardinality of a relation.
    Read as `{this class}_to_{foreign class}`. I.e. MANY_TO_ONE means that this class
    may have many instances that point to the same foreign class instance.
    """

    ONE_TO_ONE = "one_to_one"
    ONE_TO_MANY = "one_to_many"
    MANY_TO_ONE = "many_to_one"
    MANY_TO_MANY = "many_to_many"


class RelationLookupMethod(str, Enum):
    """The method used to lookup the foreign class instance(s) referenced in a
    relation.
    """

    # currently only one method is supported
    IN_DOCUMENT = "in_document"


class FrozenBaseModel(BaseModel):
    """A BaseModel that cannot be changed after initialization."""

    model_config = ConfigDict(frozen=True, use_enum_values=True)


class IdField(FrozenBaseModel):
    """A model for describing a schemapack ID field definition."""

    # currently only IDs that are inherited from a field of the content schema are
    # supported

    from_content: str = Field(
        ...,
        description=(
            "The name of the property from the content schema to be used as ID field."
        ),
    )


class ContentSchema(FrozenBaseModel):
    """A model for describing a schemapack content schema."""

    path: Optional[str] = Field(
        None,
        description=(
            "Optionally, the path to the JSON schema file defining the content schema."
        ),
    )
    json_schema: dict[str, Any] = Field(
        ...,
        description=("A JSON schema describing the content of the class instances."),
    )


class Relation(FrozenBaseModel):
    """A model for describing a schemapack relation definition."""

    cardinality: Cardinality = Field(
        ...,
        description=(
            "The cardinality of the relation. Read as `{this class}_to_{foreign class}`."
            + " I.e. MANY_TO_ONE means that this class may have many instances that"
            + " point to the same foreign class instance."
        ),
    )
    lookup_method: RelationLookupMethod = Field(
        ...,
        description=("The method used to lookup the foreign class instance(s)."),
    )
    to: str = Field(
        ...,
        description="The name of the foreign class.",
    )


class ClassDefinition(FrozenBaseModel):
    """A model for describing a schemapack class definition."""

    id: IdField
    content: ContentSchema
    relations: dict[str, Relation] = Field(
        {},
        description=(
            "A mapping of relation names to relation definitions. Relation names"
            + " should use snake_case and may only contain alphanumeric characters and"
            + " underscores. They must start with a letter."
        ),
    )

    @field_validator("content", mode="before")
    @classmethod
    def content_schema_validator(
        cls, v: Union[ContentSchema, Path, dict[str, Any]]
    ) -> ContentSchema:
        """Validate and convert the type of the content schema."""
        if isinstance(v, ContentSchema):
            return v

        if isinstance(v, Path):
            if not v.exists():
                raise PydanticCustomError(
                    "ContentSchemaNotFoundError",
                    "Content schema at the specified path does not exist.",
                )

            if not v.is_file():
                raise PydanticCustomError(
                    "ContentSchemaNotFoundError",
                    "Content schema path is not a file.",
                )

            with v.open("r", encoding="utf-8") as file:
                try:
                    json_schema = json.load(file)
                except json.JSONDecodeError as error:
                    raise PydanticCustomError(
                        "InvalidContentSchemaError",
                        "Content schema at the specified path is not valid JSON.",
                    ) from error

            return ContentSchema(path=v, json_schema=json_schema)

        if isinstance(v, dict):
            return ContentSchema(json_schema=v)

        raise PydanticCustomError(
            "InvalidContentSchemaError",
            "Expected an instance of class ContentSchema, Path, or a dict[str, Any].",
        )

    @field_serializer("content")
    def content_schema_serializer(
        self, content: ContentSchema, _info
    ) -> Union[str, dict[str, Any]]:
        """Serialize the content schema by representing it either as the path to the
        JSON schema (if the path is known) or as the JSON schema itself.
        """
        if content.path:
            return content.path

        return content.json_schema

    @field_validator("class", mode="after")
    @classmethod
    def relation_name_validator(cls, v: dict[str, Relation]) -> dict[str, Relation]:
        """Validate relation names."""
        invalid_relation_names = [
            relation_name for relation_name in v if not relation_name.isidentifier()
        ]

        if invalid_relation_names:
            raise PydanticCustomError(
                "InvalidRelationNameError",
                (
                    "Relation names may only contain alphanumeric characters and"
                    + " underscores. They must not start with a number."
                    + " Got {number} invalid names: {relation_name}"
                ),
                {
                    "number": len(invalid_relation_names),
                    "invalid_relation_names": invalid_relation_names,
                },
            )

        return v


class SchemaPack(FrozenBaseModel):
    """A model for describing a schemapack definition."""

    schemapack_version: SupportedSchemaPackVersions = Field(
        ...,
        description=(
            "Has two purposes: (1) it clearly identifies a YAML/JSON document as"
            + " a schemapack definition and (2) it specifies the used version of the"
            + " schemapack specification."
        ),
    )
    classes: dict[str, ClassDefinition] = Field(
        ...,
        description=(
            "A mapping of class names to class definitions. Class names should use"
            + " PascalCase."
        ),
    )

    @field_validator("classes", mode="before")
    @classmethod
    def relation_name_validator(
        cls, v: dict[str, ClassDefinition]
    ) -> dict[str, ClassDefinition]:
        """Validates class names."""
        invalid_relation_names = [
            relation_name for relation_name in v if not relation_name.isidentifier()
        ]

        if invalid_relation_names:
            raise PydanticCustomError(
                "InvalidClassNameError",
                (
                    "Class names may only contain alphanumeric characters and"
                    + " underscores. They must not start with a number."
                    + " Got {number} invalid names: {relation_name}"
                ),
                {
                    "number": len(invalid_relation_names),
                    "invalid_relation_names": invalid_relation_names,
                },
            )

        return v
