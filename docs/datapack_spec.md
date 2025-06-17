This document defines the structure and required fields of a `datapack.yaml` file, which represents a structured data conforming to a given schemapack. Each datapack consists of:

* A datapack version identifier,

* A resources section containing all data instances grouped by class and uniquely identified, following a format with clearly separated content (data fields) and relations (links to other resources),

* Optional rootResource and rootClass fields to restrict the datapack to a subgraph of interest.


### Keywords:

`datapack`:  Specifies the version of the datapack specification being used.

Example:
```yaml

datapack: 3.0.0
```

`resources`:A nested dictionary containing resources per class name and resource ID. Each class defined in the schemapack must be present even if no resources are defined for it in this datapack.


Example:
```yaml

datapack: 3.0.0
resources:
    Experiment: # <- class name
        exp1: # <- resource ID
            ... # <- resource definition
    Sample: # <- class name
        sample1: # <- resource ID
            ... # <- resource definition
```

*Resource definition* must follow the following structure:

* `content`: The content of the resource that complies with the content schema defined in the corresponding schemapack.

    ```yaml

    content: # <- content schema embedded here
        name: Example Resource
        description: This is an example resource.
    ```

 A dictionary specifying the relations of this resource to other resources. Each key is the name of a relation property. Each value contains the targetClass and targetResources of the relation. It maps relation names to their datapack relation definitions.

* `relations`: A dictionary containing the relations of the resource to other resources. Each key is the name of a relation mapped to their datapack relation definitions. Each value contains the target class and target resource(s) of the relation.

  Relation definition must follow the following structure:

    * `targetClass`:  The name of the referenced class.

    * `targetResources`: The ID(s) of target resources of the targetClass. Based on the schemapack definition, this field can be one of the following types:
    1. A single resource ID, if multiple.target is False.
    2. None, if both multiple.target and mandatory.target are False.
    3. A set of resource IDs, if multiple.target is True.
    4. An empty set, if multiple.target is True and mandatory.target is False.

    ```yaml

    relations:
        samples: # <- relation name
            targetClass: Sample
            targetResources: [sample1, sample2]
    ```


`rootResource` *(optional)*: Defines the id of the resource of the class defined in `className` that should act as root. This means that, in addition to the root resource itself, the datapack must only contain resources that are direct or indirect (dependencies of dependencies) of the root resource.

`rootClass` *(optional)*: Defines the class name of the resource that should act as root.


A full datapack example:

```yaml
datapack: 3.0.0
resources:
    Experiment:
        exp1:
            content:
                name: Experiment 1
                description: This is the first experiment.
            relations:
                samples:
                    targetClass: Sample
                    targetResources: sample1
        exp2:
            content:
                name: Experiment 2
                description: This is the second experiment.
            relations:
                samples:
                    targetClass: Sample
                    targetResources: sample1
    Sample:
        sample1:
            content:
                name: Sample 1
                description: This is the first sample.

rootResource: exp1
rootClass: Experiment
```
