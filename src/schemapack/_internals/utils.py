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

"""Utility functions.

Warning: This is an internal part of the library and might change without notice.
"""

import json
import os
from contextlib import contextmanager
from functools import lru_cache
from pathlib import Path

import jsonschema
import jsonschema.exceptions
import jsonschema.protocols
import jsonschema.validators
import ruamel.yaml

from schemapack.exceptions import ParsingError

yaml = ruamel.yaml.YAML(typ="safe")


def read_json_or_yaml_mapping(path: Path) -> dict:
    """Reads a JSON object or YAML mapping from file.

    Raises:
        ParsingError:
            If the file cannot be decoded as JSON or YAML or does not contain a
            JSON object or YAML Mapping. Please note, that this parser raise a
            ParsingError for duplicate keys in both JSON objects and YAML mappings.
    """
    with path.open("r", encoding="utf-8") as file:
        try:
            data = yaml.load(file)
        except ruamel.yaml.YAMLError as error:
            raise ParsingError(
                f"The file at '{path}' could not be parsed as JSON or YAML."
            ) from error

    if not isinstance(data, dict):
        raise ParsingError(
            f"The file at '{path}' did not contain a JSON object or a YAML mapping."
        )

    return data


class JsonSchemaError(ValueError):
    """Raised when a JSON schema is invalid."""


@lru_cache
def assert_valid_json_schema(schema_str: str) -> None:
    """Asserts that the given string is a valid JSON Schema.

    Raises:
        JsonSchemaError: If the schema is invalid.
    """
    schema = json.loads(schema_str)
    cls: type[jsonschema.protocols.Validator] = jsonschema.validators.validator_for(
        schema
    )

    try:
        cls.check_schema(schema)
    except jsonschema.exceptions.SchemaError as error:
        raise JsonSchemaError(error.message) from error


@contextmanager
def transient_directory_change(path: Path):
    """Change the current working directory temporarily within a with block."""
    original_cwd = os.getcwd()
    os.chdir(path)

    try:
        yield
    finally:
        os.chdir(original_cwd)
