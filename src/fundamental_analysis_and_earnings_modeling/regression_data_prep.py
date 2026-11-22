# Main script for regression analysis of earnings

import re

import pandas as pd
from Utils.data_clean import select_columns, melt_data, strip_whitespace, pivot_data, drop_columns, remove_commas
from Utils.load_data import load_regression_data, save_dataframe_to_csv

# Load regression data for each company into dataframes and add to dictionary
regression_data_dict = {}
for ticker in ["WMT","COST","DG","DLTR","TGT"]:
    regression_data_dict[ticker] = load_regression_data(ticker)

# Preprocess and format regression data for all companies
for ticker, regression_data in regression_data_dict.items():
    # Drop column name ttm in raw data if it exists
    if "ttm" in regression_data.columns:
        regression_data = drop_columns(regression_data, ["ttm"])

    # Clear whitespace from all columns
    for column in regression_data.columns:
        regression_data = strip_whitespace(regression_data, column)

    # Melt and pivot the regression data to format for easier analysis
    regression_data = melt_data(regression_data, id_vars=["name"], var_name="Date", value_name="Amount")
    regression_data = pivot_data(regression_data, index=["Date"], columns="name", values="Amount")

    # Select needed columns for analysis
    required_columns = ["Total Revenue","Cost of Revenue","Operating Expense","Interest Expense",
                    "Net Income"]
    regression_data = remove_commas(regression_data, required_columns)
    regression_data = select_columns(regression_data, required_columns)

    regression_data = regression_data.apply(pd.to_numeric, errors='coerce')

    # Check initial shape of the dataframe
    print(f"Initial shape of regression data for ticker: {ticker}")
    print(regression_data.shape)

    # Check dataframe for missing values and duplicates
    print(f"Missing values for ticker: {ticker}")
    print(regression_data.isnull().sum())
    print(f"Duplicate rows for ticker: {ticker}")
    print(regression_data.duplicated().sum())

    # Drop rows with any missing values
    regression_data = regression_data.dropna()

    # Drop duplicate rows after removing missing values
    regression_data = regression_data.drop_duplicates()

    # Print the shape of the cleaned dataframe
    print(f"Shape of cleaned regression data for ticker: {ticker}")
    print(regression_data.shape)

    # Check if missing values and duplicates are completely removed
    print(f"Missing values after cleaning for ticker: {ticker}")
    print(regression_data.isnull().sum())
    print(f"Duplicate rows after cleaning for ticker: {ticker}")
    print(regression_data.duplicated().sum())
    

    # Print data types of columns in the dataframe for the current ticker
    print(f"Data types of columns for ticker: {ticker}")
    print(regression_data.dtypes)

    regression_data_dict[ticker] = regression_data
    save_dataframe_to_csv(regression_data_dict[ticker], ticker)