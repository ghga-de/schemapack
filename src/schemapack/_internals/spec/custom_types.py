# Copyright 2021 - 2024 Universität Tübingen, DKFZ, EMBL, and Universität zu Köln
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

"""Custom types annotations used for type hinting."""

from typing import Annotated, TypeAlias

from arcticfreeze import FrozenDict
from pydantic import Field as _Field

_NonEmptyStr: TypeAlias = Annotated[str, _Field(..., min_length=1)]
ClassName: TypeAlias = _NonEmptyStr
ResourceId: TypeAlias = _NonEmptyStr
RelationPropertyName: TypeAlias = _NonEmptyStr
ContentPropertyName: TypeAlias = _NonEmptyStr
IdPropertyName: TypeAlias = _NonEmptyStr
FrozenType: TypeAlias = FrozenDict[str, str | FrozenDict | tuple]
ThawedType: TypeAlias = dict[str, str | dict | list]
