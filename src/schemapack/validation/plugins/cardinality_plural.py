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

"""A validation plugin."""

from schemapack.exceptions import ValidationPluginError
from schemapack.spec.datapack import DataPack, Resource, ResourceId
from schemapack.spec.schemapack import ClassDefinition
from schemapack.validation.base import ResourceValidationPlugin


class CardinalityPluralityValidationPlugin(ResourceValidationPlugin):
    """A resource-scoped validation plugin validating the plurality of relations,
    i.e. *_to_many relations must be lists, *_to_one relations must be single values.
    This only applies to schemapack classes with relations.
    """

    @staticmethod
    def does_apply(*, class_: ClassDefinition) -> bool:
        """A classmethod to check whether this validation plugin is relevant for the
        given schemapack.

        Returns: True if this plugin is relevant for the given class definition.
        """
        return bool(class_.relations)

    def __init__(self, *, class_: ClassDefinition):
        """This plugin is configured with one specific class definition of a schemapack."""
        self._relations = class_.relations

    def validate(
        self, *, resource: Resource, resource_id: ResourceId, datapack: DataPack
    ):
        """Validates a specific resource of the defined class. The entire datapack is
        provided for resolving relations to resources of other classes.

        Raises:
            schemapack.exceptions.DataValidationError: If validation fails.
        """
        wrong_relations: list[str] = []
        for relation_name, relation in resource.relations.items():
            is_list = isinstance(relation, list)

            try:
                expected_list = self._relations[relation_name].cardinality.endswith(
                    "to_many"
                )
            except KeyError:
                # Unknown relations are handled in a different plugin:
                continue

            if is_list != expected_list:
                wrong_relations.append(relation_name)

        if wrong_relations:
            raise ValidationPluginError(
                type_="CardinalityPluralityError",
                message=(
                    "Expected a single foreign ID but got a list, or vise versa, for"
                    " the following relation propertie(s): "
                    + ", ".join(wrong_relations)
                ),
                details={
                    "wrong_relations": wrong_relations,
                },
            )
