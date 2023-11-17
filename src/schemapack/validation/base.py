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

"""Base classes for defining validation plugins."""

from abc import ABC, abstractmethod

from schemapack.models.data import DataPack, Resource, ResourceId
from schemapack.models.schema import ClassDefinition, SchemaPack


class GlobalValidationPlugin(ABC):
    """Protocol for a plugin that performs validation of a datapack with respect to the
    entire schemapack.

    Please note:
    A ValidationPlugin should always just check for one single aspect of validation
    and should not perform all checks possible with a schemapack.
    The "global" scope of validation plugin inheriting from this class does only mean
    that it does not focus on one specific class or resource but rather a validation
    aspect that applies to the entire datapack.
    """

    @staticmethod
    @abstractmethod
    def does_apply(*, schemapack: SchemaPack):
        """A classmethod to check whether this validation plugin is relevant for the
        given schemapack.
        """
        raise NotImplementedError

    @abstractmethod
    def __init__(self, *, schemapack: SchemaPack):
        """This plugin is configured with the entire schemapack."""
        raise NotImplementedError

    @abstractmethod
    def validate(self, *, datapack: DataPack):
        """Validate the entire datapack.

        Raises:
            schemapack.exceptions.DataValidationError: If validation fails.
        """
        raise NotImplementedError


class ClassValidationPlugin(ABC):
    """Protocol for defining class-scoped validation plugin. Instances of this class
    perform validation with respect to one specific class defined in a schemapack.
    """

    @staticmethod
    @abstractmethod
    def does_apply(*, class_: ClassDefinition):
        """A classmethod to check whether this validation plugin is relevant for the
        given class definition.
        """
        raise NotImplementedError

    @abstractmethod
    def __init__(self, *, class_: ClassDefinition):
        """This plugin is configured with one specific class definition of a schemapack."""
        raise NotImplementedError

    @abstractmethod
    def validate(
        self, *, class_resources: dict[ResourceId, Resource], datapack: DataPack
    ):
        """Validate all resources of a specific class. The entire datapack is provided
        for resolving relations to other classes.

        Raises:
            schemapack.exceptions.DataValidationError: If validation fails.
        """
        raise NotImplementedError


class ResourceValidationPlugin(ABC):
    """Protocol for defining resource-scoped validation plugin. Instances of this class
    perform validation with respect to one specific resource of a class defined in a
    schemapack.
    """

    @staticmethod
    @abstractmethod
    def does_apply(*, class_: ClassDefinition):
        """A classmethod to check whether this validation plugin is relevant for the
        given schemapack.
        """
        raise NotImplementedError

    @abstractmethod
    def __init__(self, *, class_: ClassDefinition):
        """This plugin is configured with one specific class definition of a schemapack."""
        raise NotImplementedError

    @abstractmethod
    def validate(
        self, *, resource: Resource, resource_id: ResourceId, datapack: DataPack
    ):
        """Validates a specific resource of the defined class. The entire datapack is
        provided for resolving relations to resources of other classes.

        Raises:
            schemapack.exceptions.DataValidationError: If validation fails.
        """
        raise NotImplementedError
