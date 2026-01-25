# XON (XML Object Notation)

XON is an XML-based format for representing JSON data without losing type information. It uses attributes in the `xon:` namespace to specify data types.

## Features

- ✅ Preserves all JSON type information (object, array, string, number, boolean, null)
- ✅ Handles nested structures
- ✅ Supports invalid XML element names via `xon:name` attribute
- ✅ Bidirectional conversion (JSON ↔ XON)
- ✅ Pretty-printed XML output

## Quick Start

### Convert JSON to XON

```bash
python json_to_xon.py examples/simple.json output.xon.xml
```

### Convert XON to JSON

```bash
python xon_to_json.py examples/simple.xon.xml output.json
```

### Python API

```python
from json_to_xon import json_to_xon
from xon_to_json import xon_to_json
import json

# JSON to XON
json_data = {"name": "John", "age": 30}
xon_xml = json_to_xon(json_data)
print(xon_xml)

# XON to JSON
json_data = xon_to_json(xon_xml)
print(json.dumps(json_data, indent=2))
```

## Format Specification

See [XON_SPECIFICATION.md](XON_SPECIFICATION.md) for detailed format specification.

## Examples

See the `examples/` directory for sample JSON and XON files.

## Type Attributes

- `xon:type="object"` - JSON object
- `xon:type="array"` - JSON array
- `xon:type="string"` - JSON string
- `xon:type="number"` - JSON number
- `xon:type="boolean"` - JSON boolean
- `xon:type="null"` - JSON null

## Namespace

Default namespace URI: `https://xmlon.org/`
Default prefix: `xon`

You can customize the namespace URI in the converter code if needed.
