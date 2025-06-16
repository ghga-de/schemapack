```python

from pathlib import Path

from schemapack import SchemaPackValidator, load_datapack, load_schemapack

schemapack_path = Path("path/to/schemapack.yaml")
datapack_path = Path("path/to/datapack.yaml")

# load schemapack
schemapack = load_schemapack(schemapack_path)

# load datapack
datapack = load_datapack(datapack_path)

# validate datapack against schemapack
validator = SchemaPackValidator(schemapack=schemapack)
validator.validate(datapack=datapack)
```
