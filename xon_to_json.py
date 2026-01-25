#!/usr/bin/env python3
"""
XON (XML Object Notation) to JSON Converter

Converts XON XML format back to JSON, using xon: namespace attributes
to determine correct types.
"""

import json
import xml.etree.ElementTree as ET
from typing import Any, Optional


XON_NAMESPACE = "https://xmlon.org/"
XON_PREFIX = "xon"


def get_xon_type(elem: ET.Element) -> Optional[str]:
    """Get the xon:type attribute value from an element."""
    return elem.get(f"{{{XON_NAMESPACE}}}type") or elem.get(f"{XON_PREFIX}:type")


def get_xon_name(elem: ET.Element) -> Optional[str]:
    """Get the xon:name attribute value from an element (for invalid XML names)."""
    return elem.get(f"{{{XON_NAMESPACE}}}name") or elem.get(f"{XON_PREFIX}:name")


def xon_element_to_json(elem: ET.Element) -> Any:
    """
    Recursively convert XON XML element to JSON value.
    
    Args:
        elem: XML element to convert
        
    Returns:
        JSON value (dict, list, or primitive)
    """
    xon_type = get_xon_type(elem)
    
    if xon_type == "null":
        return None
    elif xon_type == "boolean":
        text = (elem.text or "").strip().lower()
        return text == "true"
    elif xon_type == "number":
        text = (elem.text or "").strip()
        # Try int first, then float
        try:
            if '.' in text or 'e' in text.lower():
                return float(text)
            return int(text)
        except ValueError:
            return float(text) if text else 0
    elif xon_type == "string":
        return elem.text or ""
    elif xon_type == "object":
        result = {}
        for child in elem:
            # Get the key name
            xon_name = get_xon_name(child)
            if xon_name:
                key = xon_name
            else:
                key = child.tag
            result[key] = xon_element_to_json(child)
        return result
    elif xon_type == "array":
        result = []
        for child in elem:
            result.append(xon_element_to_json(child))
        return result
    else:
        # Fallback: try to infer type from content
        if len(elem) == 0:
            # Leaf node - try to infer type
            text = (elem.text or "").strip()
            if text == "":
                return None
            elif text.lower() in ("true", "false"):
                return text.lower() == "true"
            else:
                try:
                    if '.' in text or 'e' in text.lower():
                        return float(text)
                    return int(text)
                except ValueError:
                    return text
        else:
            # Has children - could be object or array
            # Check if all children have same tag (likely array) or different tags (likely object)
            child_tags = [c.tag for c in elem]
            if len(set(child_tags)) == 1 and child_tags[0] in ("item", "i"):
                # Array
                return [xon_element_to_json(child) for child in elem]
            else:
                # Object
                result = {}
                for child in elem:
                    xon_name = get_xon_name(child)
                    if xon_name:
                        key = xon_name
                    else:
                        key = child.tag
                    result[key] = xon_element_to_json(child)
                return result


def xon_to_json(xon_xml: str) -> Any:
    """
    Convert XON XML string to JSON data.
    
    Args:
        xon_xml: XON XML string
        
    Returns:
        JSON data (dict, list, or primitive)
    """
    root = ET.fromstring(xon_xml)
    return xon_element_to_json(root)


def xon_file_to_json_file(xon_file: str, json_file: str, indent: int = 2) -> None:
    """
    Convert XON XML file to JSON file.
    
    Args:
        xon_file: Path to input XON XML file
        json_file: Path to output JSON file
        indent: JSON indentation level
    """
    with open(xon_file, 'r', encoding='utf-8') as f:
        xon_xml = f.read()
    
    json_data = xon_to_json(xon_xml)
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=indent, ensure_ascii=False)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: xon_to_json.py <input.xon.xml> <output.json> [indent]")
        sys.exit(1)
    
    xon_file = sys.argv[1]
    json_file = sys.argv[2]
    indent = int(sys.argv[3]) if len(sys.argv) > 3 else 2
    
    xon_file_to_json_file(xon_file, json_file, indent)
    print(f"Converted {xon_file} to {json_file}")
