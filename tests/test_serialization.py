# Copyright 2021 - 2026 Universität Tübingen, DKFZ, EMBL, and Universität zu Köln
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

"""Serialization/deserialization invariant tests for SchemaPack and DataPack.

Invariants under test:
  1. Both serialization paths (model_dump_json and model_dump(mode='json')) produce
     output that deserializes back to an equal instance.
  2. Fields whose values equal their defaults (e.g. empty `relations`) are omitted
     when serializing with exclude_defaults=True.
  3. model_dump(mode='json') returns only plain Python types — no FrozenDict or
     immutabledict instances — at any nesting level.
"""

import json
from collections.abc import Mapping
from pathlib import Path

import pytest
from arcticfreeze import FrozenDict
from immutabledict import immutabledict

from schemapack import load_schemapack
from schemapack._internals.load import load_datapack
from schemapack.spec.datapack import DataPack
from schemapack.spec.schemapack import SchemaPack
from tests.fixtures.examples import VALID_DATAPACK_PATHS, VALID_SCHEMAPACK_PATHS

_FROZEN_TYPES = (FrozenDict, immutabledict)


def _collect_frozen_paths(obj: object, path: str = "root") -> list[str]:
    """Return dotted paths where frozen mapping types appear in a nested structure."""
    found: list[str] = []
    if isinstance(obj, _FROZEN_TYPES):
        found.append(f"{path} ({type(obj).__name__})")
    if isinstance(obj, Mapping):
        for key, value in obj.items():
            found.extend(_collect_frozen_paths(value, f"{path}.{key}"))
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            found.extend(_collect_frozen_paths(item, f"{path}[{i}]"))
    return found


def _both_serialized(model: SchemaPack | DataPack) -> list[dict]:
    """Return the model serialized via both supported JSON paths."""
    return [
        json.loads(model.model_dump_json()),
        model.model_dump(mode="json"),
    ]


def _both_serialized_exclude_defaults(model: SchemaPack | DataPack) -> list[dict]:
    return [
        json.loads(model.model_dump_json(exclude_defaults=True)),
        model.model_dump(mode="json", exclude_defaults=True),
    ]


@pytest.mark.parametrize(
    "path",
    VALID_SCHEMAPACK_PATHS.values(),
    ids=VALID_SCHEMAPACK_PATHS.keys(),
)
def test_schemapack_serialization_roundtrip(path: Path):
    """SchemaPack survives a full serialize/deserialize cycle unchanged."""
    original = load_schemapack(path)
    for serialized in _both_serialized(original):
        assert SchemaPack.model_validate(serialized) == original


@pytest.mark.parametrize(
    "path",
    VALID_DATAPACK_PATHS.values(),
    ids=VALID_DATAPACK_PATHS.keys(),
)
def test_datapack_serialization_roundtrip(path: Path):
    """DataPack survives a full serialize/deserialize cycle unchanged."""
    original = load_datapack(path)
    for serialized in _both_serialized(original):
        assert DataPack.model_validate(serialized) == original


@pytest.mark.parametrize(
    "path",
    VALID_SCHEMAPACK_PATHS.values(),
    ids=VALID_SCHEMAPACK_PATHS.keys(),
)
def test_schemapack_exclude_defaults_omits_empty_relations(path: Path):
    """Classes with no relations must not emit a 'relations' key under exclude_defaults."""
    schemapack = load_schemapack(path)
    for serialized in _both_serialized_exclude_defaults(schemapack):
        for class_name, class_dict in serialized["classes"].items():
            if schemapack.classes[class_name].relations:
                assert "relations" in class_dict, (
                    f"Class '{class_name}' has relations but key is missing"
                )
            else:
                assert "relations" not in class_dict, (
                    f"Class '{class_name}' has no relations but 'relations: {{}}' was emitted"
                )


@pytest.mark.parametrize(
    "path",
    VALID_DATAPACK_PATHS.values(),
    ids=VALID_DATAPACK_PATHS.keys(),
)
def test_datapack_exclude_defaults_omits_empty_relations(path: Path):
    """Resources with no relations must not emit a 'relations' key under exclude_defaults."""
    datapack = load_datapack(path)
    for serialized in _both_serialized_exclude_defaults(datapack):
        for class_name, resources in serialized["resources"].items():
            for resource_id, resource_dict in resources.items():
                has_relations = datapack.resources[class_name][resource_id].relations
                if has_relations:
                    assert "relations" in resource_dict, (
                        f"Resource '{class_name}.{resource_id}' has relations but key is missing"
                    )
                else:
                    assert "relations" not in resource_dict, (
                        f"Resource '{class_name}.{resource_id}' has no relations"
                        f" but 'relations: {{}}' was emitted"
                    )


@pytest.mark.parametrize(
    "path",
    VALID_SCHEMAPACK_PATHS.values(),
    ids=VALID_SCHEMAPACK_PATHS.keys(),
)
def test_schemapack_model_dump_json_mode_no_frozen_types(path: Path):
    """model_dump(mode='json') must not contain FrozenDict or immutabledict instances."""
    schemapack = load_schemapack(path)
    result = schemapack.model_dump(mode="json")
    frozen_paths = _collect_frozen_paths(result)
    assert not frozen_paths, (
        f"Frozen types found in model_dump(mode='json'): {frozen_paths}"
    )


@pytest.mark.parametrize(
    "path",
    VALID_DATAPACK_PATHS.values(),
    ids=VALID_DATAPACK_PATHS.keys(),
)
def test_datapack_model_dump_json_mode_no_frozen_types(path: Path):
    """model_dump(mode='json') must not contain FrozenDict or immutabledict instances."""
    datapack = load_datapack(path)
    result = datapack.model_dump(mode="json")
    frozen_paths = _collect_frozen_paths(result)
    assert not frozen_paths, (
        f"Frozen types found in model_dump(mode='json'): {frozen_paths}"
    )
