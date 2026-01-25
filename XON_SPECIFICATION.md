# XON (XML Object Notation) Specification

## Overview

XON is an XML-based format for representing JSON data without losing type information. It uses attributes in the `xon:` namespace to specify the data types of JSON values.

## Namespace

- **Namespace URI**: `https://xmlon.org/`
- **Prefix**: `xon:`
- **Namespace Declaration**: `xmlns:xon="https://xmlon.org/"`

## Type Attributes

The following type attributes are used in the `xon:` namespace:

- `xon:type="object"` - JSON object
- `xon:type="array"` - JSON array
- `xon:type="string"` - JSON string
- `xon:type="number"` - JSON number
- `xon:type="boolean"` - JSON boolean (true/false)
- `xon:type="null"` - JSON null

## Structure Rules

### Root Element
- The root element should have `xon:type` attribute indicating the top-level JSON type
- Root element name can be `<json>`, `<root>`, or any meaningful name

### Objects
- Represented as XML elements
- Each property becomes a child element
- Element name = property key
- Must have `xon:type` attribute indicating the value type

### Arrays
- Represented as XML elements with `xon:type="array"`
- Each array item becomes a child element
- Array item elements can be named `<item>` or `<i>` with an index attribute
- Each item must have `xon:type` attribute

### Primitives
- **String**: Element with `xon:type="string"`, text content is the string value
- **Number**: Element with `xon:type="number"`, text content is the number value
- **Boolean**: Element with `xon:type="boolean"`, text content is "true" or "false"
- **Null**: Element with `xon:type="null"`, can be empty or self-closing

### Special Characters
- XML special characters in string values are escaped using XML entities
- Property names that are not valid XML element names can use `xon:name` attribute

## Examples

### Simple Object
```json
{
  "name": "John",
  "age": 30,
  "active": true
}
```

```xml
<json xmlns:xon="https://xmlon.org/" xon:type="object">
  <name xon:type="string">John</name>
  <age xon:type="number">30</age>
  <active xon:type="boolean">true</active>
</json>
```

### Array
```json
["apple", "banana", "cherry"]
```

```xml
<json xmlns:xon="http://www.w3.org/2001/XMLSchema-instance" xon:type="array">
  <item xon:type="string">apple</item>
  <item xon:type="string">banana</item>
  <item xon:type="string">cherry</item>
</json>
```

### Nested Structures
```json
{
  "users": [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
  ],
  "count": 2
}
```

```xml
<json xmlns:xon="https://xmlon.org/" xon:type="object">
  <users xon:type="array">
    <item xon:type="object">
      <id xon:type="number">1</id>
      <name xon:type="string">Alice</name>
    </item>
    <item xon:type="object">
      <id xon:type="number">2</id>
      <name xon:type="string">Bob</name>
    </item>
  </users>
  <count xon:type="number">2</count>
</json>
```

### Null Values
```json
{
  "value": null,
  "data": "test"
}
```

```xml
<json xmlns:xon="https://xmlon.org/" xon:type="object">
  <value xon:type="null"/>
  <data xon:type="string">test</data>
</json>
```

### Invalid XML Element Names
For property names that aren't valid XML element names (e.g., starting with numbers, containing special chars), use `xon:name`:

```json
{
  "123invalid": "value",
  "my-key": "data"
}
```

```xml
<json xmlns:xon="https://xmlon.org/" xon:type="object">
  <prop xon:name="123invalid" xon:type="string">value</prop>
  <prop xon:name="my-key" xon:type="string">data</prop>
</json>
```
