# Copyright 2021 - 2025 Universität Tübingen, DKFZ, EMBL, and Universität zu Köln
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

"""Compare two schema definitions for semantic equality."""

from arcticfreeze import FrozenDict
from jsonsubschema import isEquivalent

from schemapack._internals.spec.custom_types import ContentSchema, RelationPropertyName
from schemapack._internals.spec.schemapack import ClassDefinition, ClassRelation
from schemapack.spec.schemapack import SchemaPack


def compare_relations(
    relations1: FrozenDict[RelationPropertyName, ClassRelation],
    relations2: FrozenDict[RelationPropertyName, ClassRelation],
) -> bool:
    """Compare two relations for semantic equality."""
    if not relations1 and not relations2:
        return True

    if relations1.keys() != relations2.keys():
        return False

    for key in relations1:
        if not compare_class_relations(relations1[key], relations2[key]):
            return False
    return True


def compare_class_relations(
    relation1: ClassRelation,
    relation2: ClassRelation,
) -> bool:
    """Compare two ClassRelation objects for equality."""
    return (
        relation1.targetClass == relation2.targetClass
        and relation1.mandatory == relation2.mandatory
        and relation1.multiple == relation2.multiple
    )


def compare_content(schema1: ContentSchema, schema2: ContentSchema) -> bool:
    """Compare two content schemas for equality."""
    return isEquivalent(schema1, schema2)


def compare_class_definitions(
    class_def1: ClassDefinition,
    class_def2: ClassDefinition,
) -> bool:
    """Compare two ClassDefinition objects for equality."""
    return (
        class_def1.id.propertyName == class_def2.id.propertyName
        and compare_relations(class_def1.relations, class_def2.relations)
        and compare_content(class_def1.content, class_def2.content)
    )


def compare_schemapacks(
    schemapack1: SchemaPack,
    schemapack2: SchemaPack,
) -> bool:
    """Compare two SchemaPack objects for semantic equality."""
    if schemapack1.classes.keys() != schemapack2.classes.keys():
        return False

    if schemapack1.rootClass != schemapack2.rootClass:
        return False

    for class_name in schemapack1.classes:
        if not compare_class_definitions(
            schemapack1.classes[class_name],
            schemapack2.classes[class_name],
        ):
            return False

    return True
