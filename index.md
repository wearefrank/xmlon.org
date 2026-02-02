---
layout: default
title: XON – XML Object Notation
---

# XON (XML Object Notation)

**GitHub Repository**: [github.com/wearefrank/xmlon](https://github.com/wearefrank/xmlon)

XON is an **XML-based format for representing JSON data without losing type information**.  
It uses attributes in the `xon:` namespace to preserve JSON types such as objects, arrays, strings, numbers, booleans, and nulls.

## Why XON?

- **Preserves all JSON type information** (object, array, string, number, boolean, null)
- **Handles nested structures** cleanly
- **Supports invalid XML element names** via the `xon:name` attribute
- **Bidirectional conversion** between JSON and XON
- **Pretty-printed XML output**
- **Streaming Java implementation** for large JSON files

## Specification

The full format specification is documented in `XON_SPECIFICATION.md` in the repository.

- **Namespace URI**: `https://xmlon.org/`  
- **Prefix**: `xon:`  
- **Namespace declaration**: `xmlns:xon="https://xmlon.org/"`

Key type attributes:

- `xon:type="object"` – JSON object  
- `xon:type="array"` – JSON array  
- `xon:type="string"` – JSON string  
- `xon:type="number"` – JSON number  
- `xon:type="boolean"` – JSON boolean  
- `xon:type="null"` – JSON null  

## Examples

### Simple Object

**JSON:**
```json
{
  "name": "John",
  "age": 30,
  "active": true,
  "tags": ["developer", "python"],
  "address": {
    "street": "123 Main St",
    "city": "New York"
  }
}
```

**XON:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<json xmlns:xon="https://xmlon.org/" xon:type="object">
  <name xon:type="string">John</name>
  <age xon:type="number">30</age>
  <active xon:type="boolean">true</active>
  <tags xon:type="array">
    <item xon:type="string">developer</item>
    <item xon:type="string">python</item>
  </tags>
  <address xon:type="object">
    <street xon:type="string">123 Main St</street>
    <city xon:type="string">New York</city>
  </address>
</json>
```

### Array with Mixed Types

**JSON:**
```json
["apple", "banana", "cherry", 42, true, null]
```

**XON:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<json xmlns:xon="https://xmlon.org/" xon:type="array">
  <item xon:type="string">apple</item>
  <item xon:type="string">banana</item>
  <item xon:type="string">cherry</item>
  <item xon:type="number">42</item>
  <item xon:type="boolean">true</item>
  <item xon:type="null"/>
</json>
```

### Complex Nested Structure

**JSON:**
```json
{
  "user": {
    "name": "John Doe",
    "email": "john@example.com",
    "123invalid": "starts with number",
    "my-key": "contains dash",
    "special.chars": "has dots",
    "nested": {
      "deep": {
        "value": 42
      }
    }
  },
  "items": [
    {
      "id": 1,
      "name": "Item 1",
      "price": 19.99,
      "in_stock": true
    },
    {
      "id": 2,
      "name": "Item 2",
      "price": 29.99,
      "in_stock": false,
      "tags": ["new", "featured"]
    }
  ],
  "metadata": {
    "created": "2025-01-25",
    "version": 1,
    "active": true,
    "null_value": null
  }
}
```

**XON:**
```xml
<?xml version="1.0" ?>
<json xmlns:xon="https://xmlon.org/" xon:type="object">
  <user xon:type="object">
    <name xon:type="string">John Doe</name>
    <email xon:type="string">john@example.com</email>
    <prop xon:name="123invalid" xon:type="string">starts with number</prop>
    <my-key xon:type="string">contains dash</my-key>
    <special.chars xon:type="string">has dots</special.chars>
    <nested xon:type="object">
      <deep xon:type="object">
        <value xon:type="number">42</value>
      </deep>
    </nested>
  </user>
  <items xon:type="array">
    <item xon:type="object">
      <id xon:type="number">1</id>
      <name xon:type="string">Item 1</name>
      <price xon:type="number">19.99</price>
      <in_stock xon:type="boolean">true</in_stock>
    </item>
    <item xon:type="object">
      <id xon:type="number">2</id>
      <name xon:type="string">Item 2</name>
      <price xon:type="number">29.99</price>
      <in_stock xon:type="boolean">false</in_stock>
      <tags xon:type="array">
        <item xon:type="string">new</item>
        <item xon:type="string">featured</item>
      </tags>
    </item>
  </items>
  <metadata xon:type="object">
    <created xon:type="string">2025-01-25</created>
    <version xon:type="number">1</version>
    <active xon:type="boolean">true</active>
    <null_value xon:type="null"/>
  </metadata>
</json>
```

All example files are available in the [examples directory](https://github.com/wearefrank/xmlon/tree/main/examples) of the repository.

## Using XON

The repository includes implementations and helpers for converting between JSON and XON from Python and Java (streaming).

See the [README.md](https://github.com/wearefrank/xmlon/blob/main/README.md) in the repository for:

- Command-line examples
- Python API usage
- Java streaming API usage

