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

"""Loading schemapack and datapack definitions."""

from pathlib import Path

from schemapack.models import SchemaPack
from schemapack.utils import read_json_or_yaml, transient_directory_change


def load_schemapack(path: Path):
    """Load a schemapack definition from a file."""
    schemapack_dict = read_json_or_yaml(path)

    with transient_directory_change(path.parent):
        return SchemaPack.model_validate({**schemapack_dict, "self_path": path})
