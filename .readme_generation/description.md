<!-- Please provide a short overview of the features of this service. -->

Schemapack is a lightweight data modeling framework that defines two components: a schemapack for describing linked data structures, and a datapack for representing instance data that conforms to those structures.


Schemapack builds on JSON Schema to describe the structure of individual resources. In addition, it defines how resources are linked to each other. Links are described in terms of multiplicity (e.g. one-to-one, one-to-many) and mandatoriness (required or optional). Resources refer to one another by ID, rather than by embedding, which avoids redundancy and simplifies reference resolution.

<!-- Schemapack is suitable for ETL operations that transform a model and its corresponding data into other model and data representations. It is designed to support such transformations in a structured and consistent manner.

Validation is built into the framework. JSON Schema is used to validate the internal structure of each resource. For validating links across resources, Schemapack includes an extended validation layer that checks reference integrity and enforces multiplicity and mandatoriness constraints.

Schemapack includes tooling to isolate individual resources and their dependencies from larger datasets. This can be useful for partial extraction, targeted validation, or incremental processing. -->
