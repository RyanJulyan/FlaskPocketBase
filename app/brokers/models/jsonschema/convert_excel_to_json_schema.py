from typing import Dict, Optional, Any
import json

import openpyxl
from jsonschema import Draft7Validator


def convert_excel_to_json_schema(excel_file_path: str, sheet_name: Optional[str]=None, json_schema_kwargs: Dict[Any, Any] = {}):
    """
    Convert an Excel file to a JSON schema.

    The Excel file should have the following columns:
    - Property: The name of the property. Use '.' to specify nested properties.
    - Type: The type of the property. Should be one of the JSON schema types.
    - Description: A description of the property.
    - Required: Whether the property is required. Should be 'Yes' or 'No'.
    - Minimum: The minimum value of the property. Used for number types.
    - Maximum: The maximum value of the property. Used for number types.
    - Pattern: A regex pattern that the property should match. Used for string types.
    - Enum: A comma-separated list of possible values for the property.

    Args:
        excel_file_path (str): The path to the Excel file.
        sheet_name (Optional[str]): The name of the sheet in the Excel file to convert. If not provided, the active sheet is used.
        json_schema_kwargs (Dict[Any, Any]): Additional top-level properties to include in the JSON schema.

    Returns:
        dict: The JSON schema as a dictionary.
    """

    # Load the Excel file
    workbook = openpyxl.load_workbook(excel_file_path)

    # Set the sheet to extract
    if sheet_name is None:
        sheet = workbook.active
    else:
        sheet = workbook[sheet_name]

    # Create a dictionary to store the JSON schema
    json_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "properties": {},
        "required": [],
        **json_schema_kwargs
    }

    # Function to get nested property
    def get_nested_property(schema: Dict[str, Any], property_path: List[str]) -> Dict[str, Any]:
        """
        Get a nested property from a JSON schema.

        This function traverses the JSON schema according to the provided property path and returns the nested property.
        If the property does not exist, it is created with a default structure of {"type": "object", "properties": {}}.

        Args:
            schema (Dict[str, Any]): The JSON schema to get the nested property from.
            property_path (List[str]): The path to the nested property. Each element in the list is a key in the schema.

        Returns:
            Dict[str, Any]: The nested property.
        """
        properties = schema
        for key in property_path:
            if key not in properties:
                properties[key] = {"type": "object", "properties": {}}
            properties = properties[key]
        return properties

    # Iterate over the rows in the sheet
    for row in sheet.iter_rows(min_row=2, values_only=True):
        property, type, description, required, minimum, maximum, pattern, enum = row
        property_path = property.split('.')
        property_name = property_path.pop()
        properties = get_nested_property(json_schema["properties"], property_path)
        properties[property_name] = {"type": type, "description": description}
        if minimum:
            properties[property_name]["minimum"] = minimum
        if maximum:
            properties[property_name]["maximum"] = maximum
        if pattern:
            properties[property_name]["pattern"] = pattern
        if enum:
            properties[property_name]["enum"] = [e.strip() for e in enum.split(',')]
        if required == 'Yes':
            if "required" not in json_schema:
                json_schema["required"] = []
            json_schema["required"].append(property)

    return json_schema


if __name__ == "__main__":
    excel_file_path = "data_schema.xlsx"
    json_schema_file_path = "example_json_schema.json"
    json_schema = convert_excel_to_json_schema(excel_file_path, json_schema_kwargs={"type": "array"})

    # Write the JSON schema to a file
    with open(json_schema_file_path, 'w') as json_file:
        json.dump(json_schema, json_file, indent=4)

    def validate_json_schema(json_data, json_schema_file_path):
        with open(json_schema_file_path, "r") as json_file:
            json_schema = json.load(json_file)

        validator = Draft7Validator(json_schema)
        errors = validator.iter_errors(json_data)

        for error in errors:
            print(error.message)

    json_data = [
        {
            "name": "John Doe",
            "age": 30,
            "gender": "Male",
            "address": {
                "street": "123 Main St",
                "city": "New York"
            }
        },
        {
            "name": "Jane Doe",
            "age": 28,
            "gender": "Other",
            "address": {
                "street": "456 Oak Ave",
                "city": "Los Angeles"
            }
        }
    ]

    # Validate the JSON data against the JSON schema
    validate_json_schema(json_data, json_schema_file_path)


