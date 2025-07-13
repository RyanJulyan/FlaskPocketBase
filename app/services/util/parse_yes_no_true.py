from typing import Optional, Union


def parse_yes_no_true(value: Optional[Union[str, bool]]) -> Optional[bool]:
    """
    Convert a string or boolean value into a boolean or None.

    Args:
        value (Optional[Union[str, bool]]): The input value to be parsed.
            - If None, the function returns None.
            - If a boolean, it is returned as is.
            - If a string, it is parsed into a boolean based on specific keywords:
              "yes", "y", "true", "t", "1" -> True
              "no", "n", "false", "f", "0" -> False

    Returns:
        Optional[bool]:
            - True if the input matches truthy values.
            - False if the input matches falsy values.
            - None if the input is None.

    Raises:
        ValueError: If the input string does not match any known truthy or falsy values.
    """
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if value.lower() in ("yes", "y", "true", "t", "1"):
        return True
    elif value.lower() in ("no", "n", "false", "f", "0"):
        return False
    else:
        raise ValueError(f"Invalid value '{value}' for boolean conversion")
