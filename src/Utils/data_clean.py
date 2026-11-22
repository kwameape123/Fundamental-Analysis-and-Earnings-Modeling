"""
This script contains utility functions for cleaning and preprocessing data.
"""
# Import necessary libraries
import pandas as pd
import numpy as np
from pathlib import Path
import os 

#############
# Data Cleaning Functions
#############

# Define function to remove whitespace from dataframe column entries
def strip_whitespace(df: pd.DataFrame, column: str):
    """
    Remove leading and trailing whitespace from the specified column's entries.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame.
    column (str): The column to strip whitespace from.

    Returns:
    pd.DataFrame: The DataFrame with stripped column entries.
    """
    df[column] = df[column].str.strip()
    return df

# Define function to keep specific columns of a dataframe
def select_columns(df: pd.DataFrame, columns: list):
    """
    Keep only the specified columns of a dataframe.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame.
    columns (list): List of columns to keep.

    Returns:
    pd.DataFrame: The DataFrame with only the specified columns.
    """
    return df[columns]

# Define function to drop specific columns from a dataframe
def drop_columns(df: pd.DataFrame, columns: list):
    """
    Drop the specified columns from a dataframe.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame.
    columns (list): List of columns to drop.

    Returns:
    pd.DataFrame: The DataFrame with the specified columns dropped.
    """
    return df.drop(columns=columns)

# Define function to create a new column with the same value for all rows
def create_column(df: pd.DataFrame, column: str, value):
    """
    Create a new column in the dataframe with the specified values.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame.
    column (str): The name of the new column to create.
    value: The value to assign to the new column.

    Returns:
    pd.DataFrame: The DataFrame with the new column added.
    """
    df[column] = value
    return df

# Define function to set data types for specific columns
def set_dtype(df: pd.DataFrame, column: str, dtype):
    """
    Set the data type for a specific column in the dataframe.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame.
    column (str): The column to set the data type for.
    dtype: The data type to set for the column.

    Returns:
    pd.DataFrame: The DataFrame with the column data type set.
    """
    df[column] = df[column].astype(dtype)
    return df

# Define function to use pd.to_numeric with errors = 'coerce' to convert list of columns to numeric
def to_numeric(df: pd.DataFrame, columns: list):
    """
    Convert a list of columns to numeric, coercing errors to NaN.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame.
    columns (list): List of columns to convert to numeric.

    Returns:
    pd.DataFrame: The DataFrame with the columns converted to numeric.
    """
    for col in columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

# Define function to remove all commas from a list of columns in a dataframe
def remove_commas(df: pd.DataFrame, columns: list):
    """
    Remove all commas from the specified columns in the dataframe.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame.
    columns (list): List of columns to remove commas from.

    Returns:
    pd.DataFrame: The DataFrame with commas removed from the specified columns.
    """
    for col in columns:
        df[col] = df[col].str.replace(',', '')
    return df

# Define a function that melts a data frame from wide to long format
def melt_data(df: pd.DataFrame, id_vars: list, var_name: str, value_name: str):
    """
    Melt a data frame from wide to long format.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame in wide format.
    id_vars (list): List of columns to use as identifier variables.
    var_name (str): Name to use for the 'variable' column.
    value_name (str): Name to use for the 'value' column.

    Returns:
    pd.DataFrame: The melted DataFrame.
    """
    if id_vars is None:
        id_vars = ["name"]
    return df.melt(id_vars=id_vars, var_name=var_name, value_name=value_name)

# Define function to pivot melted data
def pivot_data(df: pd.DataFrame, index: list, columns: str, values: str):
    """
    Pivot a melted DataFrame back to wide format.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame in long format.
    index (list): List of columns to use as the new index.
    columns (str): Column to use to make new columns.
    values (str): Column to use for populating new values.

    Returns:
    pd.DataFrame: The pivoted DataFrame.
    """
    df = df.pivot(index=index, columns=columns, values=values)
    return df.reset_index().rename_axis(None, axis=1)

# Define function to check dataframe for missing values
def check_missing(df: pd.DataFrame):
    """
    Check the dataframe for missing values.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame.

    Returns:
    pd.Series: A series with the count of missing values for each column.
    """
    return df.isnull().sum()

# Define function to check for duplicate rows in a dataframe
def check_duplicates(df: pd.DataFrame):
    """
    Check the dataframe for duplicate rows.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame.

    Returns:
    pd.Series: A series with the count of duplicate rows for each column.
    """
    return df.duplicated().sum()

