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


from re import I
from typing import Any

from immutabledict import immutabledict
from pydantic import BaseModel, GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema

# class immutabledict(immutabledict_):
#     """Wrapper around immutabledict to make it pydantic compatible."""


class FrozenDict(immutabledict):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls,
            handler(dict),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: dict(instance)
            ),
        )


class InnerTest(BaseModel):
    dict_: FrozenDict


class Test(BaseModel):
    inner: FrozenDict[str, InnerTest]


test = Test(inner={"test": {"dict_": {1: 2}}})
