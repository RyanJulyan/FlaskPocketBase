import os
from typing import Any, Union

import pandas as pd

from app.brokers.storage.i_storage_broker import IStorageBroker


class PandasPickleStorageBroker(IStorageBroker):
    """
    A class to interface with Pickle files using pandas.

    Methods
    -------
    create(file_path: Union[str, os.PathLike[str]], data: pd.DataFrame, *args: Any, **kwargs: Any) -> None:
        Writes a pandas DataFrame to a Pickle file. If the file already exists, it will be overwritten.
    read(file_path: Union[str, os.PathLike[str]], *args: Any, **kwargs: Any) -> pd.DataFrame:
        Reads the Pickle file and returns a pandas DataFrame.
    update(file_path: Union[str, os.PathLike[str]], data: pd.DataFrame, *args: Any, **kwargs: Any) -> None:
        Appends new data to the existing data in the Pickle file.
    delete(file_path: Union[str, os.PathLike[str]], condition: Any, *args: Any, **kwargs: Any) -> None:
        Removes rows that satisfy a certain condition from the Pickle file.
    """

    def create(self, file_path: Union[str, os.PathLike[str]], data: pd.DataFrame, *args: Any, **kwargs: Any) -> None:
        """
        Writes a pandas DataFrame to a Pickle file. If the file already exists, it will be overwritten.

        Parameters
        ----------
        file_path : Union[str, os.PathLike[str]]
            The path to the Pickle file.
        data : pd.DataFrame
            The data to write to the Pickle file.
        *args : Any
            Variable length argument list.
        **kwargs : Any
            Arbitrary keyword arguments.
        """
        data.to_pickle(file_path, *args, **kwargs)

    def read(self, file_path: Union[str, os.PathLike[str]], *args: Any, **kwargs: Any) -> pd.DataFrame:
        """
        Reads the Pickle file and returns a pandas DataFrame.

        Parameters
        ----------
        file_path : Union[str, os.PathLike[str]]
            The path to the Pickle file.
        *args : Any
            Variable length argument list.
        **kwargs : Any
            Arbitrary keyword arguments.

        Returns
        -------
        pd.DataFrame
            The data from the Pickle file.
        """
        return pd.read_pickle(file_path, *args, **kwargs)

    def update(self, file_path: Union[str, os.PathLike[str]], data: pd.DataFrame, *args: Any, **kwargs: Any) -> None:
        """
        Appends new data to the existing data in the Pickle file.

        Parameters
        ----------
        file_path : Union[str, os.PathLike[str]]
            The path to the Pickle file.
        data : pd.DataFrame
            The data to append to the Pickle file.
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
        Removes rows that satisfy a certain condition from the Pickle file.

        Parameters
        ----------
        file_path : Union[str, os.PathLike[str]]
            The path to the Pickle file.
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
