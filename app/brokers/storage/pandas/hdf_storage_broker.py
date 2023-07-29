import os
from typing import Any, Union

import pandas as pd

from app.brokers.storage.i_storage_broker import IStorageBroker


class PandasHdfStorageBroker(IStorageBroker):
    """
    A class to interface with HDF files using pandas.

    Methods
    -------
    create(file_path: Union[str, os.PathLike[str]], data: pd.DataFrame, key: str, *args: Any, **kwargs: Any) -> None:
        Writes a pandas DataFrame to an HDF file. If the file already exists, it will be overwritten.
    read(file_path: Union[str, os.PathLike[str]], key: str, *args: Any, **kwargs: Any) -> pd.DataFrame:
        Reads the HDF file and returns a pandas DataFrame.
    update(file_path: Union[str, os.PathLike[str]], data: pd.DataFrame, key: str, *args: Any, **kwargs: Any) -> None:
        Appends new data to the existing data in the HDF file.
    delete(file_path: Union[str, os.PathLike[str]], condition: Any, key: str, *args: Any, **kwargs: Any) -> None:
        Removes rows that satisfy a certain condition from the HDF file.
    """

    def create(self, file_path: Union[str, os.PathLike[str]], data: pd.DataFrame, key: str, *args: Any, **kwargs: Any) -> None:
        """
        Writes a pandas DataFrame to an HDF file. If the file already exists, it will be overwritten.

        Parameters
        ----------
        file_path : Union[str, os.PathLike[str]]
            The path to the HDF file.
        data : pd.DataFrame
            The data to write to the HDF file.
        key : str
            Identifier for the group in the store.
        *args : Any
            Variable length argument list.
        **kwargs : Any
            Arbitrary keyword arguments.
        """
        data.to_hdf(file_path, key, *args, **kwargs)

    def read(self, file_path: Union[str, os.PathLike[str]], key: str, *args: Any, **kwargs: Any) -> pd.DataFrame:
        """
        Reads the HDF file and returns a pandas DataFrame.

        Parameters
        ----------
        file_path : Union[str, os.PathLike[str]]
            The path to the HDF file.
        key : str
            Identifier for the group in the store.
        *args : Any
            Variable length argument list.
        **kwargs : Any
            Arbitrary keyword arguments.

        Returns
        -------
        pd.DataFrame
            The data from the HDF file.
        """
        return pd.read_hdf(file_path, key, *args, **kwargs)

    def update(self, file_path: Union[str, os.PathLike[str]], data: pd.DataFrame, key: str, *args: Any, **kwargs: Any) -> None:
        """
        Appends new data to the existing data in the HDF file.

        Parameters
        ----------
        file_path : Union[str, os.PathLike[str]]
            The path to the HDF file.
        data : pd.DataFrame
            The data to append to the HDF file.
        key : str
            Identifier for the group in the store.
        *args : Any
            Variable length argument list.
        **kwargs : Any
            Arbitrary keyword arguments.
        """
        existing_data = self.read(file_path, key)
        updated_data = existing_data.append(data)
        self.create(file_path, updated_data, key, *args, **kwargs)

    def delete(self, file_path: Union[str, os.PathLike[str]], condition: Any, key: str, *args: Any, **kwargs: Any) -> None:
        """
        Removes rows that satisfy a certain condition from the HDF file.

        Parameters
        ----------
        file_path : Union[str, os.PathLike[str]]
            The path to the HDF file.
        condition : Any
            The condition to satisfy for rows to be removed.
        key : str
            Identifier for the group in the store.
        *args : Any
            Variable length argument list.
        **kwargs : Any
            Arbitrary keyword arguments.
        """
        data = self.read(file_path, key)
        data = data.drop(data[condition].index)
        self.create(file_path, data, key, *args, **kwargs)
