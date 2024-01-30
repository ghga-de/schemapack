#!/usr/bin/env python3

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

"""Demo on how to use schemapack."""

from pathlib import Path

import yaml

from schemapack.integrate import integrate
from schemapack.isolate import isolate
from schemapack.load import load_datapack, load_schemapack
from schemapack.validation.main import SchemaPackValidator

DEMO_DIR = Path("/workspace/demo")
EXAMPLE_DIR = DEMO_DIR / "examples"
SCHEMAPACK_PATH = EXAMPLE_DIR / "submission.schemapack.yaml"
DATAPACK_PATH = EXAMPLE_DIR / "submission.datapack.yaml"
INVALID_DATAPACK_PATH = EXAMPLE_DIR / "invalid_submission.datapack.yaml"
ISOLATED_DATAPACK_PATH = DEMO_DIR / "isolated.datapack.yaml"
INTEGRATED_DATA_PATH = DEMO_DIR / "integrated.yaml"

# load the schemapack and datapack into an in memory datastructure:
schemapack = load_schemapack(SCHEMAPACK_PATH)
datapack = load_datapack(DATAPACK_PATH)
invlaid_datapack = load_datapack(INVALID_DATAPACK_PATH)

# validate:
validator = SchemaPackValidator(schemapack=schemapack)
validator.validate(datapack=datapack)
validator.validate(datapack=invlaid_datapack)

# isolate a single dataset:
isolated_datapack = isolate(
    datapack=datapack,
    class_name="Dataset",
    resource_id="dataset_1",
    schemapack=schemapack,
)
with open(ISOLATED_DATAPACK_PATH, "w") as file:
    yaml.safe_dump(isolated_datapack.model_dump(), file)

# convert into an integrated view:
integrated_data = integrate(datapack=isolated_datapack, schemapack=schemapack)
with open(INTEGRATED_DATA_PATH, "w") as file:
    yaml.safe_dump(integrated_data, file)
