<!--
 Copyright 2021 - 2025 Universität Tübingen, DKFZ, EMBL, and Universität zu Köln
 for the German Human Genome-Phenome Archive (GHGA)

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
-->


### Keywords:

`schemapack`: Specifies the Schemapack version the schema is built under.

`description` *(optional)*: A short, human-readable summary of the schema.

`classes`: A mapping of class names to *class definitions*. Class names must use PascalCase.

Example:
```
yaml

schemapack: 3.0.0
description: Schema for experimental metadata
classes:
    Experiment:
        ...
```

### Class Definition

A class definition includes the following properties:

`description` *(optional)*: A brief explanation of the class.

`id`: Defines the class's identifier property. Must follow this structure:

* `propertyName`: The name of the identifier property. Must not conflict with names used in `content` or `relations`.

* `description` *(optional)*: A human-readable description of the identifier.

    Example:
    ```
    yaml

    id:
        propertyName: alias
        description: alias is id
    ```

`content`: A schema describing the structure of the class content. Must be a valid JSON Schema object. You may embed it inline or reference an external JSON or YAML file, which will be automatically loaded.

```
yaml

content: content_schemas/Experiment.schema.json # <- path to the json schema
```

```
content: # <- content schema embedded here
    type: object
    properties:
        name:
            type: string
        description:
            type: string
```


Given that the content of the Experiment.schema.json file is:
```json
{
    "type": "object",
    "properties": {
        "name": {
            "type": "string"
        },
        "description": {
            "type": "string"
        }
    }
}
```

`relations` *(optional)*: A mapping of relation names to *relation definitions*. Relation names must:
  * Use `snake_case`.
  * Start with a letter.
  * Contain only alphanumeric characters and underscores.

Example:

```
yaml

schemapack: 3.0.0
description: Schema for experimental metadata
classes:
    Experiment:
        id:
            propertyName: alias
            description: alias is id
        content: content_schemas/Experiment.schema.json
        relations:
            samples: # <- relation name
                ...
```


### Relation Definition

A relation is defined with the mapping of the relation name to the relation specification. It specifies:

**description:** (optional) A description of the relation.

**targetClass:** The name of the target class meaning the class name that is being referred by the class where the relation is described.

**mandatory:** The modality of the relation. It describes the minimum number of instances the origin and the target end must contribute to the relation. TODO iyice yaz nasil belirlendigini cunku en karisik yeri burasi

Example:
```
yaml

mandatory:
    origin: true
    target: true
```

**multiple:** The cardinality of the relation. It describes the maximum number of instances the origin and the target end may contribute to the relation. For instance, if the origin is `True` and target is `False`, the origin may contribute multiple instances to the relation, while the target may at most contribute a single instance to the relation. This is equivalent to a 'many-to-one' cardinality.

Example:
```
yaml

multiple:
    origin: true
    target: false
```


A full schemapack example:

```
yaml

schemapack: 3.0.0
description: Schema for experimental metadata
classes:
    Experiment:
        id:
            propertyName: alias
            description: alias is id
        content: content_schemas/Experiment.schema.json
        relations:
            samples:
                targetClass: Sample
                mandatory:
                    origin: true
                    target: true
                multiple:
                    origin: true
                    target: false
    Sample:
        id:
            propertyName: alias
            description: alias is id
        content: content_schemas/Sample.schema.json
```
This example describes Experiment and Sample classes and their relations.
