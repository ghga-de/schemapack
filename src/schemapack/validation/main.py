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

"""Logic for running multiple validation plugins on a datapack with respect to a
schemapack.
"""

from typing import Optional, Union, overload

from schemapack.exceptions import (
    ValidationError,
    ValidationErrorRecord,
    ValidationPluginError,
)
from schemapack.models.data import DataPack
from schemapack.models.schema import ClassDefinition, SchemaPack
from schemapack.validation.base import (
    ClassValidationPlugin,
    GlobalValidationPlugin,
    ResourceValidationPlugin,
)
from schemapack.validation.content_schema import ContentSchemaValidationPlugin

DEFAULT_GLOBAL_PLUGIN_REGISTRY: list[type[GlobalValidationPlugin]] = []
DEFAULT_CLASS_PLUGIN_REGISTRY: list[type[ClassValidationPlugin]] = []
DEFAULT_RESOURCE_PLUGIN_REGISTRY: list[type[ResourceValidationPlugin]] = [
    ContentSchemaValidationPlugin
]


def _create_global_plugins(
    *, schemapack: SchemaPack, plugin_classes: list[type[GlobalValidationPlugin]]
):
    """Create instances of all the provided global plugins that apply to the given
    schemapack.
    """
    return [
        cls(schemapack=schemapack)
        for cls in plugin_classes
        if cls.does_apply(schemapack=schemapack)
    ]


@overload
def _create_plugins_for_class(
    *, class_: ClassDefinition, plugin_classes: list[type[ClassValidationPlugin]]
) -> list[ClassValidationPlugin]:
    ...


@overload
def _create_plugins_for_class(
    *, class_: ClassDefinition, plugin_classes: list[type[ResourceValidationPlugin]]
) -> list[ResourceValidationPlugin]:
    ...


@overload
def _create_plugins_for_class(
    *,
    class_: ClassDefinition,
    plugin_classes: list[
        Union[type[ClassValidationPlugin], type[ResourceValidationPlugin]]
    ],
) -> list[Union[ClassValidationPlugin, ResourceValidationPlugin]]:
    ...


def _create_plugins_for_class(
    *,
    class_: ClassDefinition,
    plugin_classes: Union[
        list[type[ClassValidationPlugin]],
        list[type[ResourceValidationPlugin]],
        list[Union[type[ClassValidationPlugin], type[ResourceValidationPlugin]]],
    ],
) -> Union[
    list[ClassValidationPlugin],
    list[ResourceValidationPlugin],
    list[Union[ClassValidationPlugin, ResourceValidationPlugin]],
]:
    """Create instances of all the provided class or resource plugins that apply to the given
    schemapack class.
    """
    return [
        cls(class_=class_) for cls in plugin_classes if cls.does_apply(class_=class_)
    ]


def _create_class_plugins(
    *, schemapack: SchemaPack, plugin_classes: list[type[ClassValidationPlugin]]
) -> dict[str, list[ClassValidationPlugin]]:
    """Create instances of the provided class plugins for each class (if relevant) in
    the given schemapack.

    Returns:
        A dictionary mapping class names to the corresponding class plugin instances.
    """
    return {
        class_name: _create_plugins_for_class(
            class_=class_, plugin_classes=plugin_classes
        )
        for class_name, class_ in schemapack.classes.items()
    }


def _create_resource_plugins(
    *, schemapack: SchemaPack, plugin_classes: list[type[ResourceValidationPlugin]]
) -> dict[str, list[ResourceValidationPlugin]]:
    """Create instances of the provided resource plugins for each class (if relevant) in
    the given schemapack.

    Returns:
        A dictionary mapping class names to the corresponding resource plugin instances.
    """
    return {
        class_name: _create_plugins_for_class(
            class_=class_, plugin_classes=plugin_classes
        )
        for class_name, class_ in schemapack.classes.items()
    }


def _plugin_error_to_record(
    subject_class: Optional[str],
    subject_resource: Optional[str],
    error: ValidationPluginError,
) -> ValidationErrorRecord:
    """Convert a ValidationPluginError to a ValidationErrorRecord."""
    return ValidationErrorRecord(
        subject_class=subject_class,
        subject_resource=subject_resource,
        type=error.type,
        message=error.message,
        details=error.details,
    )


class SchemaPackValidator:
    """A class for validating arbitrary datapacks against a specific schemapack."""

    def __init__(
        self,
        *,
        schemapack: SchemaPack,
        add_global_plugins: Optional[list[type[GlobalValidationPlugin]]] = None,
        add_class_plugins: Optional[list[type[ClassValidationPlugin]]] = None,
        add_resource_plugins: Optional[list[type[ResourceValidationPlugin]]] = None,
    ):
        """Initialize with a specific schemapack.

        Args:
            schemapack: The schemapack to validate against.
            add_global_plugins: Additional global validation plugins to use.
            add_class_plugins: Additional class validation plugins to use.
            add_resource_plugins: Additional resource validation plugins to use.
        """
        self._schemapack = schemapack
        self._global_plugins = _create_global_plugins(
            schemapack=schemapack,
            plugin_classes=DEFAULT_GLOBAL_PLUGIN_REGISTRY + (add_global_plugins or []),
        )
        self._class_plugins = _create_class_plugins(
            schemapack=schemapack,
            plugin_classes=DEFAULT_CLASS_PLUGIN_REGISTRY + (add_class_plugins or []),
        )
        self._resource_plugins = _create_resource_plugins(
            schemapack=schemapack,
            plugin_classes=DEFAULT_RESOURCE_PLUGIN_REGISTRY
            + (add_resource_plugins or []),
        )

    def validate(self, *, datapack: DataPack):
        """Validates the given datapack against the configured schemapack.

        Raises:
            schemapack.exceptions.ValidationError: If validation fails.
        """
