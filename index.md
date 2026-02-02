---
layout: default
title: XON – XML Object Notation
---

# XON (XML Object Notation)

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

The `examples/` directory contains sample JSON and XON files:

- `simple.json` ⇄ `simple.xon.xml`
- `array.json` ⇄ `array.xon.xml`
- `complex.json` ⇄ `complex.xon.xml`
- `complex_roundtrip.json`

You can use these to see how typical JSON structures map into XON.

## Using XON

The repository includes implementations and helpers for converting between JSON and XON from Python and Java (streaming).

See `README.md` in the repository for:

- Command-line examples
- Python API usage
- Java streaming API usage

## How to Publish This Site on GitHub Pages

1. **Create a GitHub repository** with this folder (`xmlon.org`) as the root of the repo.  
2. Commit and push the files, including `_config.yml` and `index.md`, to the default branch (e.g. `main`).  
3. In GitHub, go to **Settings → Pages** for the repository.  
4. Under **Source**, select the branch (e.g. `main`) and **root** (or `/`), then save.  
5. GitHub Pages will build the site using Jekyll and the `jekyll-theme-cayman` theme; your homepage will be this `index.md`.

Optionally, you can configure a custom domain (such as `xmlon.org`) in the same **Settings → Pages** section and by adding the appropriate DNS records.

