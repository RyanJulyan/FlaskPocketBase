from dateutil import parser
from datetime import datetime, timezone
from typing import Union

from configuration.config import Config


def convert_and_format_to_datetime(
    date_input: Union[str, datetime],
    DATE_FORMAT: str = Config().DATE_FORMAT,
    TIME_FORMAT: str = Config().TIME_FORMAT,
    DATETIME_FORMAT: str = Config().DATETIME_FORMAT,
) -> datetime:
    """
    Converts any date or datetime input into a single datetime object formatted
    according to the config's date and time formats. Ensures the datetime is in UTC.

    Args:
        date_input (Union[str, datetime]): The input date or datetime. Can be a string,
            or a datetime object.
        DATE_FORMAT (str): The format string for the date part. Defaults to `Config().DATE_FORMAT`.
        TIME_FORMAT (str): The format string for the time part. Defaults to `Config().TIME_FORMAT`.
        DATETIME_FORMAT (str): The combined format string for date and time. Defaults to
            `Config().DATETIME_FORMAT`.

    Returns:
        datetime: A UTC datetime object formatted to the specified date and time formats.

    Raises:
        ValueError: If the input string cannot be parsed or the formatted datetime is invalid.
        TypeError: If the input type is neither a string nor a datetime object.
    """

    if not isinstance(date_input, (str, datetime)):
        raise TypeError("Input must be a string, date, or datetime object.")

    if isinstance(date_input, datetime):
        # If input already has a timezone, convert to UTC
        if date_input.tzinfo is not None:
            dt_obj = date_input.astimezone(timezone.utc)
        else:
            # Assume naive datetime is in UTC
            dt_obj = date_input.replace(tzinfo=timezone.utc)
    elif isinstance(date_input, str):
        # Input is a string; parse it
        try:
            dt_obj = parser.parse(date_input)
            # Convert to UTC if timezone info is present, otherwise assume UTC
            if dt_obj.tzinfo is not None:
                dt_obj = dt_obj.astimezone(timezone.utc)
            else:
                dt_obj = dt_obj.replace(tzinfo=timezone.utc)
        except Exception as e:
            raise ValueError(
                f"Invalid date string format: {date_input}"
            ) from e

    # Format the datetime object into strings for date and time
    formatted_date: str = dt_obj.strftime(DATE_FORMAT)
    formatted_time: str = dt_obj.strftime(TIME_FORMAT)

    # Combine formatted date and time and return as a datetime object
    formatted_datetime_str: str = f"{formatted_date} {formatted_time}"

    try:
        # Parse the formatted string back into a datetime object with UTC timezone
        formatted_datetime: datetime = datetime.strptime(
            formatted_datetime_str, DATETIME_FORMAT
        ).replace(tzinfo=timezone.utc)
        return formatted_datetime
    except ValueError as e:
        raise ValueError(
            f"Error formatting datetime: {formatted_datetime_str}"
        ) from e
