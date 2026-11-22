"""
This script contains utility functions for loading income, cashflow, and regression data from CSV files.
"""
# Import necessary libraries
import pandas as pd
import numpy as np
from pathlib import Path
import os 

#############
# Data Cleaning Functions
#############

# Define function to load income data from a CSV file
def load_income_data(ticker:str):
    """
    Load data from a CSV file for the given ticker.
    
    Parameters:
    ticker (str): The ticker symbol of the stock.

    Returns:
    pd.DataFrame: The loaded data as a pandas DataFrame.
    """
    parent_dir = Path(__file__).parent.parent.parent
    income_path = parent_dir / f"data/raw/{ticker}_quarterly_income.csv"
    if not income_path.exists():
        raise FileNotFoundError(f"No income statement data found for ticker: {ticker}")
    income_data = pd.read_csv(income_path)
    return income_data


# Define function to load cashflow data from a CSV file
def load_cashflow_data(ticker:str):
    """
    Load cashflow data from a CSV file for the given ticker.
    
    Parameters:
    ticker (str): The ticker symbol of the stock.

    Returns:
    pd.DataFrame: The loaded cashflow data as a pandas DataFrame.
    """
    parent_dir = Path(__file__).parent.parent.parent
    cashflow_path = parent_dir / f"data/raw/{ticker}_quarterly_cashflow.csv"
    if not cashflow_path.exists():
        raise FileNotFoundError(f"No cashflow statement data found for ticker: {ticker}")
    cashflow_data = pd.read_csv(cashflow_path)
    return cashflow_data

# Define function to load regression data from a CSV file
def load_regression_data(ticker:str):
    """
    Load regression data from a CSV file for the given ticker.
    
    Parameters:
    ticker (str): The ticker symbol of the stock.

    Returns:
    pd.DataFrame: The loaded regression data as a pandas DataFrame.
    """
    parent_dir = Path(__file__).parent.parent.parent
    regression_path = parent_dir / f"data/raw/{ticker}_quarterly_financials.csv"
    if not regression_path.exists():
        raise FileNotFoundError(f"No regression data found for ticker: {ticker}")
    regression_data = pd.read_csv(regression_path)
    return regression_data

# Define function to save specified dataframe to a CSV file
def save_dataframe_to_csv(df: pd.DataFrame, ticker: str):
    """
    Save the specified dataframe to a CSV file for the given ticker.
    
    Parameters:
    df (pd.DataFrame): The dataframe to save.
    ticker (str): The ticker symbol of the stock.

    Returns:
    None
    """
    parent_dir = Path(__file__).parent.parent.parent
    os.makedirs(parent_dir / "data/processed", exist_ok=True)
    save_path = parent_dir / f"data/processed/{ticker}_regression.csv"
    df.to_csv(save_path, index=False)

# Define function to save database dataframe to a CSV file
def save_database_dataframe_to_csv(df: pd.DataFrame, name: str):
    """
    Save the specified database dataframe to a CSV file for the given name.
    
    Parameters:
    df (pd.DataFrame): The dataframe to save.
    name (str): The name to use for the saved file.

    Returns:
    None
    """
    parent_dir = Path(__file__).parent.parent.parent
    os.makedirs(parent_dir / "data/processed", exist_ok=True)
    save_path = parent_dir / f"data/processed/{name}_database.csv"
    df.to_csv(save_path, index=False)

# Define function to load database dataframe from a CSV file
def load_database_dataframe(name: str):
    """
    Load database dataframe from a CSV file for the given name.
    
    Parameters:
    name (str): The name of the database file to load.

    Returns:
    pd.DataFrame: The loaded database dataframe as a pandas DataFrame.
    """
    parent_dir = Path(__file__).parent.parent.parent
    database_path = parent_dir / f"data/processed/{name}_database.csv"
    if not database_path.exists():
        raise FileNotFoundError(f"No database data found for name: {name}")
    database_data = pd.read_csv(database_path)
    return database_data


