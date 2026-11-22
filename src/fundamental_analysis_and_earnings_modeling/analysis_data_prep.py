# Main script for fundamental analysis of earnings

# Import necessary libraries and dependencies
import pandas as pd

from Utils.data_clean import select_columns, melt_data, strip_whitespace,pivot_data,drop_columns,create_column,set_dtype,to_numeric, remove_commas, check_missing, check_duplicates
from Utils.feature_engineering import calculate_cashflow_ratios, calculate_profit_margins, calculate_expense_ratios
from Utils.load_data import load_income_data, load_cashflow_data, save_database_dataframe_to_csv

# Load income data for each company into dataframes and add to dictionary
income_data_dict = {}
for ticker in ["WMT","COST","DG","DLTR","TGT"]:
    income_data_dict[ticker] = load_income_data(ticker)

# Load cashflow data for each company into dataframes and add to dictionary
cashflow_data_dict = {}
for ticker in ["WMT","COST","DG","DLTR","TGT"]:
    cashflow_data_dict[ticker] = load_cashflow_data(ticker)

##################
# Preprocess and engineer features for all dataframes in income data dictionaries.
##################
for ticker, income_data in income_data_dict.items():
    # Drop column name ttm in raw data
    income_data = drop_columns(income_data, ["ttm"])

    # Clear whitespace from all columns
    for column in income_data.columns:
        income_data = strip_whitespace(income_data, column)

    # Melt and pivot the income data to format for easier analysis
    income_data = melt_data(income_data, id_vars=["name"], var_name="Date", value_name="Amount")
    income_data = pivot_data(income_data, index=["Date"], columns="name", values="Amount")

    # Select needed columns for analysis and create a new column for the company ticker
    required_columns = ["Date", "Total Revenue","Cost of Revenue","Gross Profit","Operating Expense","Operating Income","Interest Expense",
                        "Tax Provision","Net Income"]
    income_data = select_columns(income_data, required_columns)
    income_data = create_column(income_data, "Ticker", ticker)

    # Set data types for specific columns if needed
    income_data = set_dtype(income_data, "Date", "datetime64[ns]")
    income_data = set_dtype(income_data, "Ticker", "string")
    Amount = ["Total Revenue","Cost of Revenue","Gross Profit","Operating Expense","Operating Income","Interest Expense","Tax Provision","Net Income"]
    income_data = remove_commas(income_data, Amount)
    income_data = to_numeric(income_data, Amount)

    income_data = calculate_profit_margins(income_data)
    income_data = calculate_expense_ratios(income_data)

    # Update the dictionary with the cleaned and processed data
    income_data_dict[ticker] = income_data

    # Union all cleaned income data into a single dataframe for further analysis
all_income_data = pd.concat(income_data_dict.values(), ignore_index=True)
print("All cleaned income data:")
print(all_income_data.shape)

##################
# Preprocess and engineer features for all dataframes in cashflow data dictionaries.
##################
for ticker, cashflow_data in cashflow_data_dict.items():
    # Drop column name ttm in raw data
    cashflow_data = drop_columns(cashflow_data, ["ttm"])

    # Clear whitespace from all columns
    for column in cashflow_data.columns:
        cashflow_data = strip_whitespace(cashflow_data, column)

    # Melt and pivot the cashflow data to format for easier analysis
    cashflow_data = melt_data(cashflow_data, id_vars=["name"], var_name="Date", value_name="Amount")
    cashflow_data = pivot_data(cashflow_data, index=["Date"], columns="name", values="Amount")

    # Select needed columns for analysis and create a new column for the company ticker
    required_columns = ["Date", "Operating Cash Flow", "Net Income from Continuing Operations", "Free Cash Flow"]
    cashflow_data = select_columns(cashflow_data, required_columns)
    cashflow_data = create_column(cashflow_data, "Ticker", ticker)

    # Set data types for specific columns if needed
    cashflow_data = set_dtype(cashflow_data, "Date", "datetime64[ns]")
    cashflow_data = set_dtype(cashflow_data, "Ticker", "string")
    Amount = ["Operating Cash Flow", "Net Income from Continuing Operations", "Free Cash Flow"]
    cashflow_data = remove_commas(cashflow_data, Amount)
    cashflow_data = to_numeric(cashflow_data, Amount)

    # Calculate cash flow ratios
    cashflow_data = calculate_cashflow_ratios(cashflow_data)

    # Drop Net Income from Continuing Operations
    cashflow_data = drop_columns(cashflow_data, ["Net Income from Continuing Operations"])

    # Update the dictionary with the cleaned and processed data
    cashflow_data_dict[ticker] = cashflow_data

    

# Union all cleaned cashflow data into a single dataframe for further analysis
all_cashflow_data = pd.concat(cashflow_data_dict.values(), ignore_index=True)
print("All cleaned cashflow data:")
print(all_cashflow_data.shape)

############
# Clean Preprocessed datasets
############
# Check for missing values and duplicates in all preprocessed datasets
print("Checking for missing values and duplicates in all preprocessed datasets:")

print("Income data:")
print("Missing values:")
print(check_missing(all_income_data))
print("Duplicate rows:")
print(check_duplicates(all_income_data))

print("Cashflow data:")
print("Missing values:")
print(check_missing(all_cashflow_data))
print("Duplicate rows:")
print(check_duplicates(all_cashflow_data))

# Check column data types in all preprocessed datasets
print("Income data column types:")
print(all_income_data.dtypes)
print("Cashflow data column types:")
print(all_cashflow_data.dtypes)

# Join all cleaned income and cashflow data for further analysis if needed
all_analysis_data = pd.merge(all_income_data, all_cashflow_data, on=["Date", "Ticker"], how="outer")
print("All joined analysis data:")
print(all_analysis_data.shape)

# Save the cleaned and processed cashflow data to a CSV file
save_database_dataframe_to_csv(all_cashflow_data, "all_cashflow_data")

# Save the cleaned and processed income data to a CSV file
save_database_dataframe_to_csv(all_income_data, "all_income_data")

# Save the joined analysis data to a CSV file
save_database_dataframe_to_csv(all_analysis_data, "all_analysis_data")

