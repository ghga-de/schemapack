<!-- Please provide a short overview of the features of this service. -->

Schemapack is a lightweight data modeling framework that defines two components: a schemapack for describing linked data structures, and a datapack for representing instance data that conforms to those structures.


Schemapack builds on JSON Schema to describe the structure of individual resources. In addition, it defines how resources are linked to each other. Links are described in terms of multiplicity (e.g. one-to-one, one-to-many) and mandatoriness (required or optional). Resources refer to one another by ID, rather than by embedding, which avoids redundancy and simplifies reference resolution.

Validation is built into the framework. Schemapack uses JSON Schema to validate the content of each resource. It includes additional validators to verify datapacks and schemapack's compliance with the modeling language specifications. For validation across resources, it extends the validation layer to check:
* Reference integrity
* Multiplicity constraints
* Mandatoriness of references

Schemapack includes tooling to isolate individual resources and their dependencies from larger datasets. This can be useful for partial extraction, targeted validation, or incremental processing.
