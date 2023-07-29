from abc import ABC, abstractmethod
from typing import Dict, Optional, Any

class IDataValidator(ABC):
    @abstractmethod
    def __init__(self, df: Optional[Any] = None, schema: Optional[Dict] = None):
        """
        Initialize the DataValidator with a DataFrame and a JSON schema.

        Parameters:
            df (Any, optional): The DataFrame to validate.
            schema (Dict, optional): The JSON schema to validate against.
        """
        pass

    @abstractmethod
    def apply_validation(self, df: Optional[Any] = None, schema: Optional[Dict] = None) -> Any:
        """
        Apply JSON schema validation to a DataFrame.

        Parameters:
            df (Any, optional): The DataFrame to validate. If not provided, the class attribute is used.
            schema (Dict, optional): The JSON schema to validate against. If not provided, the class attribute is used.

        Returns:
            Any: The DataFrame with additional columns that indicate whether each row is valid and the error message if not.
        """
        pass

    @abstractmethod
    def get_valid_data(self, df: Optional[Any] = None) -> Any:
        """
        Get the valid data from a DataFrame.

        Parameters:
            df (Any, optional): The DataFrame to get the valid data from. If not provided, the class attribute is used.

        Returns:
            Any: The valid data.
        """
        pass

    @abstractmethod
    def get_invalid_data(self, df: Optional[Any] = None) -> Any:
        """
        Get the invalid data from a DataFrame.

        Parameters:
            df (Any, optional): The DataFrame to get the invalid data from. If not provided, the class attribute is used.

        Returns:
            Any: The invalid data.
        """
        pass
