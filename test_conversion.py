#!/usr/bin/env python3
"""
Test script to verify round-trip conversion (JSON -> XON -> JSON)
"""

import json
from json_to_xon import json_to_xon
from xon_to_json import xon_to_json


def test_round_trip(test_name: str, json_data: dict):
    """Test round-trip conversion and verify data integrity."""
    print(f"\n{'='*60}")
    print(f"Test: {test_name}")
    print(f"{'='*60}")
    
    # Convert JSON to XON
    xon_xml = json_to_xon(json_data)
    print("\nXON XML:")
    print(xon_xml)
    
    # Convert XON back to JSON
    converted_json = xon_to_json(xon_xml)
    
    # Compare
    print("\nOriginal JSON:")
    print(json.dumps(json_data, indent=2))
    print("\nConverted JSON:")
    print(json.dumps(converted_json, indent=2))
    
    # Verify
    if json_data == converted_json:
        print("\n[PASS] Round-trip conversion successful!")
    else:
        print("\n[FAIL] Round-trip conversion failed!")
        print("Differences:")
        print(f"Original: {json_data}")
        print(f"Converted: {converted_json}")
    
    return json_data == converted_json


def main():
    """Run all tests."""
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Simple object
    tests_total += 1
    if test_round_trip("Simple Object", {
        "name": "John",
        "age": 30,
        "active": True
    }):
        tests_passed += 1
    
    # Test 2: Array
    tests_total += 1
    if test_round_trip("Array", ["apple", "banana", "cherry"]):
        tests_passed += 1
    
    # Test 3: Nested structures
    tests_total += 1
    if test_round_trip("Nested Structures", {
        "users": [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"}
        ],
        "count": 2,
        "tags": ["developer", "python"]
    }):
        tests_passed += 1
    
    # Test 4: All types
    tests_total += 1
    if test_round_trip("All Types", {
        "string": "text",
        "number": 42,
        "float": 3.14,
        "boolean_true": True,
        "boolean_false": False,
        "null": None,
        "array": [1, "two", True, None],
        "object": {"nested": "value"}
    }):
        tests_passed += 1
    
    # Test 5: Empty structures
    tests_total += 1
    if test_round_trip("Empty Structures", {
        "empty_object": {},
        "empty_array": []
    }):
        tests_passed += 1
    
    # Test 6: Array as root
    tests_total += 1
    if test_round_trip("Array as Root", [1, 2, {"three": 3}]):
        tests_passed += 1
    
    # Summary
    print(f"\n{'='*60}")
    print(f"Tests: {tests_passed}/{tests_total} passed")
    print(f"{'='*60}")
    
    if tests_passed == tests_total:
        print("[PASS] All tests passed!")
        return 0
    else:
        print("[FAIL] Some tests failed!")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
