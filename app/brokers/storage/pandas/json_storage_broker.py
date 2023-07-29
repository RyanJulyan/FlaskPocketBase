import os
from typing import Any, Union

import pandas as pd

from app.brokers.storage.i_storage_broker import IStorageBroker


class PandasJsonStorageBroker(IStorageBroker):
    """
    A class to interface with JSON files using pandas.

    Methods
    -------
    create(file_path: Union[str, os.PathLike[str]], data: pd.DataFrame, *args: Any, **kwargs: Any) -> None:
        Writes a pandas DataFrame to a JSON file. If the file already exists, it will be overwritten.
    read(file_path: Union[str, os.PathLike[str]], *args: Any, **kwargs: Any) -> pd.DataFrame:
        Reads the JSON file and returns a pandas DataFrame.
    update(file_path: Union[str, os.PathLike[str]], data: pd.DataFrame, *args: Any, **kwargs: Any) -> None:
        Appends new data to the existing data in the JSON file.
    delete(file_path: Union[str, os.PathLike[str]], condition: Any, *args: Any, **kwargs: Any) -> None:
        Removes rows that satisfy a certain condition from the JSON file.
    """

    def create(self, file_path: Union[str, os.PathLike[str]], data: pd.DataFrame, *args: Any, **kwargs: Any) -> None:
        """
        Writes a pandas DataFrame to a JSON file. If the file already exists, it will be overwritten.

        Parameters
        ----------
        file_path : Union[str, os.PathLike[str]]
            The path to the JSON file.
        data : pd.DataFrame
            The data to write to the JSON file.
        *args : Any
            Variable length argument list.
        **kwargs : Any
            Arbitrary keyword arguments.
        """
        data.to_json(file_path, *args, **kwargs)

    def read(self, file_path: Union[str, os.PathLike[str]], *args: Any, **kwargs: Any) -> pd.DataFrame:
        """
        Reads the JSON file and returns a pandas DataFrame.

        Parameters
        ----------
        file_path : Union[str, os.PathLike[str]]
            The path to the JSON file.
        *args : Any
            Variable length argument list.
        **kwargs : Any
            Arbitrary keyword arguments.

        Returns
        -------
        pd.DataFrame
            The data from the JSON file.
        """
        return pd.read_json(file_path, *args, **kwargs)

    def update(self, file_path: Union[str, os.PathLike[str]], data: pd.DataFrame, *args: Any, **kwargs: Any) -> None:
        """
        Appends new data to the existing data in the JSON file.

        Parameters
        ----------
        file_path : Union[str, os.PathLike[str]]
            The path to the JSON file.
        data : pd.DataFrame
            The data to append to the JSON file.
        *args : Any
            Variable length argument list.
        **kwargs : Any
            Arbitrary keyword arguments.
        """
        existing_data = self.read(file_path)
        updated_data = existing_data.append(data)
        self.create(file_path, updated_data, *args, **kwargs)

    def delete(self, file_path: Union[str, os.PathLike[str]], condition: Any, *args: Any, **kwargs: Any) -> None:
        """
        Removes rows that satisfy a certain condition from the JSON file.

        Parameters
        ----------
        file_path : Union[str, os.PathLike[str]]
            The path to the JSON file.
        condition : Any
            The condition to satisfy for rows to be removed.
        *args : Any
            Variable length argument list.
        **kwargs : Any
            Arbitrary keyword arguments.
        """
        data = self.read(file_path)
        data = data.drop(data[condition].index)
        self.create(file_path, data, *args, **kwargs)
