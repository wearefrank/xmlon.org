#!/usr/bin/env python3
"""
JSON to XON (XML Object Notation) Converter

Converts JSON data to XML format with xon: namespace attributes
preserving all type information.
"""

import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import Any
import re


XON_NAMESPACE = "https://xmlon.org/"
XON_PREFIX = "xon"


def is_valid_xml_name(name: str) -> bool:
    """Check if a string is a valid XML element name."""
    if not name or not name[0].isalpha() and name[0] != '_':
        return False
    return all(c.isalnum() or c in ('_', '-', '.', ':') for c in name)


def json_to_xon_element(parent: ET.Element, key: str, value: Any, root_element: ET.Element = None) -> None:
    """
    Recursively convert JSON value to XON XML element.
    
    Args:
        parent: Parent XML element
        key: Key name (for objects) or None (for array items)
        value: JSON value to convert
        root_element: Root element (for namespace registration)
    """
    if root_element is None:
        root_element = parent
    
    # Register namespace if not already registered
    if f"{{{XON_NAMESPACE}}}" not in root_element.attrib:
        root_element.set(f"xmlns:{XON_PREFIX}", XON_NAMESPACE)
    
    # Determine element name
    if key:
        if is_valid_xml_name(key):
            elem_name = key
        else:
            elem_name = "prop"
    else:
        elem_name = "item"
    
    if value is None:
        # Null value
        elem = ET.SubElement(parent, elem_name)
        if key and not is_valid_xml_name(key):
            elem.set(f"{XON_PREFIX}:name", key)
        elem.set(f"{XON_PREFIX}:type", "null")
    elif isinstance(value, bool):
        # Boolean
        elem = ET.SubElement(parent, elem_name)
        if key and not is_valid_xml_name(key):
            elem.set(f"{XON_PREFIX}:name", key)
        elem.set(f"{XON_PREFIX}:type", "boolean")
        elem.text = str(value).lower()
    elif isinstance(value, (int, float)):
        # Number
        elem = ET.SubElement(parent, elem_name)
        if key and not is_valid_xml_name(key):
            elem.set(f"{XON_PREFIX}:name", key)
        elem.set(f"{XON_PREFIX}:type", "number")
        elem.text = str(value)
    elif isinstance(value, str):
        # String
        elem = ET.SubElement(parent, elem_name)
        if key and not is_valid_xml_name(key):
            elem.set(f"{XON_PREFIX}:name", key)
        elem.set(f"{XON_PREFIX}:type", "string")
        elem.text = value
    elif isinstance(value, dict):
        # Object
        if key:
            if is_valid_xml_name(key):
                elem = ET.SubElement(parent, key)
            else:
                elem = ET.SubElement(parent, "prop")
                elem.set(f"{XON_PREFIX}:name", key)
        else:
            elem = ET.SubElement(parent, "item")
        elem.set(f"{XON_PREFIX}:type", "object")
        
        for k, v in value.items():
            json_to_xon_element(elem, k, v, root_element)
    elif isinstance(value, list):
        # Array
        if key:
            if is_valid_xml_name(key):
                elem = ET.SubElement(parent, key)
            else:
                elem = ET.SubElement(parent, "prop")
                elem.set(f"{XON_PREFIX}:name", key)
        else:
            elem = ET.SubElement(parent, "item")
        elem.set(f"{XON_PREFIX}:type", "array")
        
        for item in value:
            json_to_xon_element(elem, None, item, root_element)
    else:
        raise ValueError(f"Unsupported type: {type(value)}")


def json_to_xon(json_data: Any, root_name: str = "json") -> str:
    """
    Convert JSON data to XON XML string.
    
    Args:
        json_data: JSON data (dict, list, or primitive)
        root_name: Name for the root XML element
        
    Returns:
        Pretty-printed XML string
    """
    root = ET.Element(root_name)
    
    # Determine root type
    if json_data is None:
        root.set(f"{XON_PREFIX}:type", "null")
    elif isinstance(json_data, bool):
        root.set(f"{XON_PREFIX}:type", "boolean")
        root.text = str(json_data).lower()
    elif isinstance(json_data, (int, float)):
        root.set(f"{XON_PREFIX}:type", "number")
        root.text = str(json_data)
    elif isinstance(json_data, str):
        root.set(f"{XON_PREFIX}:type", "string")
        root.text = json_data
    elif isinstance(json_data, dict):
        root.set(f"{XON_PREFIX}:type", "object")
        for k, v in json_data.items():
            json_to_xon_element(root, k, v, root)
    elif isinstance(json_data, list):
        root.set(f"{XON_PREFIX}:type", "array")
        for item in json_data:
            json_to_xon_element(root, None, item, root)
    else:
        raise ValueError(f"Unsupported root type: {type(json_data)}")
    
    # Register namespace
    root.set(f"xmlns:{XON_PREFIX}", XON_NAMESPACE)
    
    # Convert to string with pretty printing
    rough_string = ET.tostring(root, encoding='unicode')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def json_file_to_xon_file(json_file: str, xon_file: str, root_name: str = "json") -> None:
    """
    Convert JSON file to XON XML file.
    
    Args:
        json_file: Path to input JSON file
        xon_file: Path to output XON XML file
        root_name: Name for the root XML element
    """
    with open(json_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    
    xon_xml = json_to_xon(json_data, root_name)
    
    with open(xon_file, 'w', encoding='utf-8') as f:
        f.write(xon_xml)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: json_to_xon.py <input.json> <output.xon.xml> [root_name]")
        sys.exit(1)
    
    json_file = sys.argv[1]
    xon_file = sys.argv[2]
    root_name = sys.argv[3] if len(sys.argv) > 3 else "json"
    
    json_file_to_xon_file(json_file, xon_file, root_name)
    print(f"Converted {json_file} to {xon_file}")
