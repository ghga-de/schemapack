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

"""Logic for exporting schemapacks in mermaid format."""

from collections.abc import Mapping
from typing import Any

from schemapack._internals.spec.schemapack import ClassDefinition, Relation
from schemapack.spec.schemapack import SchemaPack


def get_property_type(json_schema_props: Mapping[str, Any], prop_name: str) -> str:
    """Get the type of a property from a JSON schema properties map. If no type is
    specified, 'object' is assumed. If the property has an enum key, 'enum' is returned.

    Args:
        json_schema_props: The properties of the class.
        prop_name: The name of the property to get the type of.

    Returns:
        The type of the property.
    """
    prop = json_schema_props[prop_name]
    if isinstance(prop, dict):
        type = prop.get("type", "object") if not prop.get("enum") else "enum"
        if type == "array":
            return f"array[{prop.get('items', {}).get('type', 'object')}]"
        return type
    raise ValueError(
        f"Invalid JSON schema. Expected property {prop_name} to be a dict."
    )


def export_class_entity(
    class_name: str, class_def: ClassDefinition, with_properties: bool
) -> str:
    """
    Export a class entity in mermaid format.

    Args:
        class_name: The name of the class to export.
        class_def: The definition of the class to export.
        show_properties: Whether to include the properties of the class in the diagram.

    Returns:
        A string representing the class entity in mermaid format.
    """
    if not with_properties:
        return f"{class_name} {{}}"

    json_schema_obj = class_def.content.json_schema_dict
    json_schema_obj_props = json_schema_obj.get("properties", {})
    json_schema_obj_reqs = json_schema_obj.get("required", [])

    if not isinstance(json_schema_obj_reqs, list):
        raise ValueError("Invalid JSON schema. Expected 'required' to be a list.")

    fields = "\n".join(
        f"{get_property_type(json_schema_props=json_schema_obj_props, prop_name=field)}"
        + f" {field} "
        + ('"req"' if field in json_schema_obj_reqs else '"opt"')
        for field in json_schema_obj_props
    )
    return f"{class_name} {{\n{fields}\n}}"


def export_class_relation(
    class_name: str, property_name: str, relation: Relation
) -> str:
    """Export a relation between two classes in mermaid format.

    Args:
        class_name: The name of the class that contains the relation.
        property_name: The name of the relation.
        relation: The relation definition.

    Returns:
        A string representing the relation between the two classes in mermaid format.
    """
    origin_multiple = "}" if relation.multiple.origin else "|"
    target_multiple = "{" if relation.multiple.target else "|"
    origin_mandatory = "|" if relation.mandatory.origin else "o"
    target_mandatory = "|" if relation.mandatory.target else "o"
    return (
        f"{class_name} "
        f"{origin_multiple}{origin_mandatory}--"
        + f"{target_mandatory}{target_multiple}"
        + f' {relation.targetClass} : "{class_name}.{property_name}"'
    )


def export_class(
    class_name: str, class_def: ClassDefinition, with_properties: bool
) -> str:
    """Export a class in mermaid format.

    Args:
        class_name: The name of the class to export.
        class_def: The definition of the class to export.
        show_properties: Whether to include the properties of the class in the diagram.

    Returns:
        A string representing the class in mermaid format.
    """
    return (
        export_class_entity(
            class_name=class_name, class_def=class_def, with_properties=with_properties
        )
        + "\n"
        + "\n".join(
            export_class_relation(class_name, prop_name, relation)
            for prop_name, relation in class_def.relations.items()
        )
    )


def export_mermaid(schemapack: SchemaPack, with_properties: bool = True) -> str:
    """
    Export a SchemaPack in mermaid format.

    Args:
        schemapack: The SchemaPack to export.
        show_properties: Whether to include the properties of the classes in the diagram.

    Returns:
        A string representing the SchemaPack in mermaid format.
    """
    return "erDiagram\n" + "\n".join(
        export_class(
            class_name=class_name, class_def=class_def, with_properties=with_properties
        )
        for class_name, class_def in schemapack.classes.items()
    )
