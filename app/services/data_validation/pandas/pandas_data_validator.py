import pandas as pd
from jsonschema import Draft7Validator
from typing import Dict, Union, Optional

from app.services.data_validation.i_data_validator import IDataValidator

class PandasDataValidator(IDataValidator):
    def __init__(self, df: Optional[pd.DataFrame] = None, schema: Optional[Dict] = None):
        """
        Initialize the DataValidator with a DataFrame and a JSON schema.

        Parameters:
            df (pd.DataFrame, optional): The DataFrame to validate.
            schema (Dict, optional): The JSON schema to validate against.
        """
        self.df = df
        self.schema = schema
        self.validator = Draft7Validator(schema) if schema else None

    def apply_validation(self, df: Optional[pd.DataFrame] = None, schema: Optional[Dict] = None) -> pd.DataFrame:
        """
        Apply JSON schema validation to a DataFrame.

        Parameters:
            df (pd.DataFrame, optional): The DataFrame to validate. If not provided, the class attribute is used.
            schema (Dict, optional): The JSON schema to validate against. If not provided, the class attribute is used.

        Returns:
            pd.DataFrame: The DataFrame with additional columns that indicate whether each row is valid and the error message if not.
        """
        df = df if df is not None else self.df
        schema = schema if schema is not None else self.schema
        validator = Draft7Validator(schema) if schema else self.validator

        if df is None or validator is None:
            raise ValueError("Both df and schema must be provided either as parameters or as class attributes.")

        # Define a function that checks if a row is valid
        def get_validation_result(row: pd.Series) -> Dict[str, Union[bool, str]]:
            """
            Validate a row against the JSON schema and return the validation result.

            Parameters:
                row (pd.Series): The DataFrame row to validate.

            Returns:
                Dict[str, Union[bool, str]]: A dictionary with 'is_valid' and 'error_message' keys. 'is_valid' is True if the row is valid and False otherwise. 'error_message' is None if the row is valid and the validation error message otherwise.
            """
            errors = list(validator.iter_errors(row.to_dict()))
            if errors:
                return {"is_valid": False, "error_message": errors[0].message}  # Return the first error message
            else:
                return {"is_valid": True, "error_message": None}

        # Apply the function to each row
        validation_results = df.apply(get_validation_result, axis=1, result_type='expand')

        # Concatenate the original DataFrame with the validation results
        df = pd.concat([df, validation_results], axis=1)
        
        return df

    def get_valid_data(self, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Get the valid data from a DataFrame.

        Parameters:
            df (pd.DataFrame, optional): The DataFrame to get the valid data from. If not provided, the class attribute is used.

        Returns:
            pd.DataFrame: The valid data.
        """
        df = df if df is not None else self.df

        if df is None:
            raise ValueError("df must be provided either as a parameter or as a class attribute.")

        valid_data = df[df['is_valid']]
        valid_data = valid_data.drop(columns=['is_valid', 'error_message'])
        return valid_data

    def get_invalid_data(self, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Get the invalid data from a DataFrame.

        Parameters:
            df (pd.DataFrame, optional): The DataFrame to get the invalid data from. If not provided, the class attribute is used.

        Returns:
            pd.DataFrame: The invalid data.
        """
        df = df if df is not None else self.df

        if df is None:
            raise ValueError("df must be provided either as a parameter or as a class attribute.")

        invalid_data = df[~df['is_valid']]
        invalid_data = invalid_data.drop(columns='is_valid')
        return invalid_data


if __name__ == "__main__":
    # Define your data
    data = pd.DataFrame([
        {"name": "John", "age": 30},
        {"name": "Alice", "age": "thirty"},  # This will cause a validation error
        {"name": "Bob", "age": 40},
    ])

    # Define your schema
    schema = {
        "type" : "object",
        "properties" : {
            "name" : {"type" : "string"},
            "age" : {"type" : "number"},
        },
    }

    # Create a DataValidator
    validator = PandasDataValidator(data, schema)

    # Apply validation
    data = validator.apply_validation()

    # Get valid and invalid data
    valid_data = validator.get_valid_data(data)
    invalid_data = validator.get_invalid_data(data)

    # Now, valid_data contains the valid items and invalid_data contains the invalid items
    print("Valid data:")
    print(valid_data)
    print("\nInvalid data:")
    print(invalid_data)

    # Define new data
    new_data = pd.DataFrame([
        {"fruit": "apple", "quantity": 10},
        {"fruit": "banana", "quantity": "ten"},  # This will cause a validation error
        {"fruit": "cherry", "quantity": 20},
    ])

    # Define new schema
    new_schema = {
        "type" : "object",
        "properties" : {
            "fruit" : {"type" : "string"},
            "quantity" : {"type" : "number"},
        },
    }

    # Apply new validation
    new_data = validator.apply_validation(new_data, new_schema)

    # Get valid and invalid data
    valid_data = validator.get_valid_data(new_data)
    invalid_data = validator.get_invalid_data(new_data)

    # Now, valid_data contains the valid items and invalid_data contains the invalid items
    print("\nNew valid data:")
    print(valid_data)
    print("\nNew invalid data:")
    print(invalid_data)

