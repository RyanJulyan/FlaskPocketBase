from typing import Any

import pandas as pd
from sqlalchemy import create_engine

from app.brokers.storage.i_storage_broker import IStorageBroker


class PandasSqlAlchemyStorageBroker(IStorageBroker):
    """
    A class to interface with SQL databases using SQLAlchemy and pandas.

    Methods
    -------
    create(connection_string: str, table_name: str, data: pd.DataFrame, *args: Any, **kwargs: Any) -> None:
        Writes a pandas DataFrame to an SQL table. If the table already exists, it will be overwritten.
    read(connection_string: str, table_name: str, *args: Any, **kwargs: Any) -> pd.DataFrame:
        Reads the SQL table and returns a pandas DataFrame.
    update(connection_string: str, table_name: str, data: pd.DataFrame, *args: Any, **kwargs: Any) -> None:
        Appends new data to the existing data in the SQL table.
    delete(connection_string: str, table_name: str, condition: str, *args: Any, **kwargs: Any) -> None:
        Removes rows that satisfy a certain SQL condition from the SQL table.
    """

    def create(self, connection_string: str, table_name: str, data: pd.DataFrame, *args: Any, **kwargs: Any) -> None:
        """
        Writes a pandas DataFrame to an SQL table. If the table already exists, it will be overwritten.

        Parameters
        ----------
        connection_string : str
            The connection string to the SQL database.
        table_name : str
            The name of the SQL table.
        data : pd.DataFrame
            The data to write to the SQL table.
        *args : Any
            Variable length argument list.
        **kwargs : Any
            Arbitrary keyword arguments.
        """
        engine = create_engine(connection_string)
        data.to_sql(table_name, engine, if_exists='replace', *args, **kwargs)

    def read(self, connection_string: str, table_name: str, *args: Any, **kwargs: Any) -> pd.DataFrame:
        """
        Reads the SQL table and returns a pandas DataFrame.

        Parameters
        ----------
        connection_string : str
            The connection string to the SQL database.
        table_name : str
            The name of the SQL table.
        *args : Any
            Variable length argument list.
        **kwargs : Any
            Arbitrary keyword arguments.

        Returns
        -------
        pd.DataFrame
            The data from the SQL table.
        """
        engine = create_engine(connection_string)
        return pd.read_sql_table(table_name, engine, *args, **kwargs)

    def update(self, connection_string: str, table_name: str, data: pd.DataFrame, *args: Any, **kwargs: Any) -> None:
        """
        Appends new data to the existing data in the SQL table.

        Parameters
        ----------
        connection_string : str
            The connection string to the SQL database.
        table_name : str
            The name of the SQL table.
        data : pd.DataFrame
            The data to append to the SQL table.
        *args : Any
            Variable length argument list.
        **kwargs : Any
            Arbitrary keyword arguments.
        """
        engine = create_engine(connection_string)
        existing_data = self.read(connection_string, table_name)
        updated_data = existing_data.append(data)
        updated_data.to_sql(table_name, engine, if_exists='replace', *args, **kwargs)

    def delete(self, connection_string: str, table_name: str, condition: str, *args: Any, **kwargs: Any) -> None:
        """
        Removes rows that satisfy a certain SQL condition from the SQL table.

        Parameters
        ----------
        connection_string : str
            The connection string to the SQL database.
        table_name : str
            The name of the SQL table.
        condition : str
            The SQL condition to satisfy for rows to be removed.
        *args : Any
            Variable length argument list.
        **kwargs : Any
            Arbitrary keyword arguments.
        """
        engine = create_engine(connection_string)
        data = self.read(connection_string, table_name)
        data.query(condition, inplace=True)
        data.to_sql(table_name, engine, if_exists='replace', *args, **kwargs)
