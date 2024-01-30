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

DEMO_DIR = Path("/workspace/demo")
EXAMPLE_DIR = DEMO_DIR / "examples"
SCHEMAPACK_PATH = EXAMPLE_DIR / "submission.schemapack.yaml"
DATAPACK_PATH = EXAMPLE_DIR / "submission.datapack.yaml"
INVALID_DATAPACK_PATH = EXAMPLE_DIR / "invalid_submission.datapack.yaml"
ISOLATED_DATAPACK_PATH = DEMO_DIR / "isolated.datapack.yaml"
INTEGRATED_DATA_PATH = DEMO_DIR / "integrated.yaml"
