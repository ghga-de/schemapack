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

import typing
from enum import Enum
from functools import cached_property
from pathlib import Path
from typing import Any, Literal, Optional, Union

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_serializer,
    field_validator,
    model_validator,
)
from pydantic_core import PydanticCustomError

from schemapack.utils import (
    DecodeError,
    FrozenDict,
    JsonSchemaError,
    JsonSchemaValidator,
    get_json_schema_validator,
    read_json_or_yaml,
)

SupportedSchemaPackVersions = Literal["0.1.0"]
SUPPORTED_SCHEMA_PACK_VERSIONS = typing.get_args(SupportedSchemaPackVersions)


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

    model_config = ConfigDict(frozen=True, use_enum_values=True, extra="forbid")


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

    path: Optional[Path] = Field(
        None,
        description=(
            "Optionally, the path to the JSON schema file defining the content schema."
        ),
    )
    json_schema: FrozenDict[str, Any] = Field(
        ...,
        description=("A JSON schema describing the content of the class instances."),
    )

    @cached_property
    def validator(self) -> JsonSchemaValidator:
        """Get a JSON schema validator for validating data against the content schema.

        Raises:
            JsonSchemaError: If the schema is invalid.
        """
        return get_json_schema_validator(dict(self.json_schema))

    @model_validator(mode="after")
    def trigger_validator_construction(self) -> "ContentSchema":
        """Trigger the construction of a validator (for validating data against the
        schema. This also validates the content schema itself.
        """
        try:
            _ = self.validator
        except JsonSchemaError as error:
            raise PydanticCustomError(
                "InvalidContentSchemaError",
                "The content schema is not a valid JSON schema: {error_message}",
                {"error_message": str(error)},
            ) from error

        return self


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
    lookup: RelationLookupMethod = Field(
        RelationLookupMethod.IN_DOCUMENT,
        description="The method used to lookup the foreign class instance(s).",
    )
    to: str = Field(
        ...,
        description="The name of the foreign class.",
    )


class ClassDefinition(FrozenBaseModel):
    """A model for describing a schemapack class definition."""

    id: IdField
    content: ContentSchema
    relations: FrozenDict[str, Relation] = Field(
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
        cls, v: Union[ContentSchema, Path, str, dict[str, Any], FrozenDict[str, Any]]
    ) -> ContentSchema:
        """Validate and convert the type of the content schema."""
        if isinstance(v, ContentSchema):
            return v

        if isinstance(v, str):
            # assume that the string is a path to a JSON or YAML file
            v = Path(v)

        if isinstance(v, Path):
            if not v.is_file():
                absolute_path = v.absolute().resolve()
                raise PydanticCustomError(
                    "ContentSchemaNotFoundError",
                    (
                        "Content schema path does not exist or is not a file."
                        + " Absolute path: {absolute_path}"
                    ),
                    {
                        "absolute_path": absolute_path,
                    },
                )

            try:
                json_schema = read_json_or_yaml(v)
            except DecodeError as error:
                raise PydanticCustomError(
                    "InvalidContentSchemaError",
                    (
                        "Content schema at the specified path could not be decoded"
                        + " assuming {assumed_format} format."
                    ),
                    {
                        "assumed_format": error.assumed_format,
                    },
                ) from error

            return ContentSchema.model_validate({"path": v, "json_schema": json_schema})

        if isinstance(v, (dict, FrozenDict)):
            return ContentSchema.model_validate({"json_schema": v})

        raise PydanticCustomError(
            "InvalidContentSchemaError",
            (
                "Expected an instance of class ContentSchema, a dict[str, Any], a"
                + " FrozenDict[str, Any] or a path (pathlib.Path or str) to a JSON or"
                + " YAML file."
            ),
        )

    @field_serializer("content")
    def content_schema_serializer(
        self, content: ContentSchema, _info
    ) -> Union[str, dict[str, Any]]:
        """Serialize the content schema by representing it either as the path to the
        JSON schema (if the path is known) or as the JSON schema itself.
        """
        if content.path:
            return str(content.path)

        return dict(content.json_schema)

    @field_validator("relations", mode="after")
    @classmethod
    def relation_name_validator(
        cls, v: FrozenDict[str, Relation]
    ) -> FrozenDict[str, Relation]:
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

    @model_validator(mode="after")
    def id_from_content_validator(self) -> "ClassDefinition":
        """Validate that the from_content field of id is part of the content schema."""
        if (
            self.content.json_schema.get("properties", {}).get(self.id.from_content)
            is None
        ):
            raise PydanticCustomError(
                "IdNotInContentSchemaError",
                ("The ID field '{id_field}' is not part of the content schema."),
                {
                    "id_field": self.id.from_content,
                },
            )

        return self


class SchemaPack(FrozenBaseModel):
    """A model for describing a schemapack definition."""

    schemapack: SupportedSchemaPackVersions = Field(
        ...,
        description=(
            "Has two purposes: (1) it clearly identifies a YAML/JSON document as"
            + " a schemapack definition and (2) it specifies the used version of the"
            + " schemapack specification."
        ),
    )
    classes: FrozenDict[str, ClassDefinition] = Field(
        ...,
        description=(
            "A mapping of class names to class definitions. Class names should use"
            + " PascalCase."
        ),
        min_length=1,
    )
    root: Optional[str] = Field(
        None,
        description=(
            "By default, schemapacks are unrooted meaning that they can be used to"
            + " describe any number of instances of the classes contained in the"
            + " schemapack."
            + " Using this field, you may optionally specify the name of a class that"
            + " acts as root. The schemapack will then be scoped to only"
            + " describe a single instance of the root class along with its relations."
        ),
    )
    self_path: Optional[Path] = Field(
        None, description="The path to this schemapack.", exclude=True
    )

    @model_validator(mode="before")
    @classmethod
    def check_schemapack_field_exists(cls, data: Any) -> Any:
        """Checks that the schemapack field exists and points to a supported version
        before doing anything else. Please note, this validation only takes place if the
        data is passed as dict. However, the data can be pretty much anything.
        """
        if isinstance(data, dict):
            if "schemapack" not in data:
                raise PydanticCustomError(
                    "MissingSchemaPackVersionError",
                    (
                        "Missing a `schemapack` field. Are you sure you have passed a"
                        + " schemapack definition?"
                    ),
                )

            if data["schemapack"] not in SUPPORTED_SCHEMA_PACK_VERSIONS:
                raise PydanticCustomError(
                    "UnsupportedSchemaPackVersionError",
                    (
                        "Unsupported schemapack version '{current_version}'."
                        " Supported versions are: {supported_versions}"
                    ),
                    {
                        "current_version": data["schemapack"],
                        "supported_versions": SUPPORTED_SCHEMA_PACK_VERSIONS,
                    },
                )

        return data

    @field_validator("classes", mode="after")
    @classmethod
    def class_name_validator(
        cls, v: FrozenDict[str, ClassDefinition]
    ) -> FrozenDict[str, ClassDefinition]:
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

    @field_validator("self_path", mode="after")
    @classmethod
    def self_path_validator(cls, v: Optional[Path]) -> Optional[Path]:
        """Validates that self_path is a file and make it absolute."""
        if v is None:
            return v

        if not v.is_file():
            raise ValueError("self_path must be a file.")

        return v.absolute()

    @model_validator(mode="after")
    def relation_to_class_validation(self) -> "SchemaPack":
        """Validate that all relations point to existing classes."""
        # store invalid relations as a list of strings ({class_name}.{relation_name}):
        invalid_relations: list[str] = []

        for class_name, class_definition in self.classes.items():
            for relation_name, relation in class_definition.relations.items():
                if relation.to not in self.classes:
                    invalid_relations.append(f"{class_name}.{relation_name}")

        if invalid_relations:
            raise PydanticCustomError(
                "RelationClassNotFoundError",
                (
                    "Found {number} relation(s) that point to non-existing classes:"
                    + " {invalid_relations}"
                ),
                {
                    "number": len(invalid_relations),
                    "invalid_relations": invalid_relations,
                },
            )

        return self

    @model_validator(mode="after")
    def root_class_validation(self) -> "SchemaPack":
        """Validate that the root class exists."""
        if self.root and self.root not in self.classes:
            raise PydanticCustomError(
                "RootClassNotFoundError",
                ("The root class '{root}' does not exist."),
                {
                    "root": self.root,
                },
            )

        return self
