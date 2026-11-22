# Define utility functions for feature engineering

import pandas as pd

# Define function to calculate all Profit Margins 
def calculate_profit_margins(df: pd.DataFrame):
    """
    Calculate all profit margins (Gross, Operating, and Net) for a specified DataFrame.
    
    Parameters:.
    df (pd.DataFrame): The input DataFrame. Must contain columns "Total Revenue", "Gross Profit", "Operating Income", and "Net Income".

    Returns:
    pd.DataFrame: The DataFrame with additional columns for Gross, Operating, and Net Profit Margins.
    """
    df["Gross_Profit_Margin"] = df["Gross Profit"] / df["Total Revenue"]
    df["Operating_Profit_Margin"] = df["Operating Income"] / df["Total Revenue"]
    df["Net_Profit_Margin"] = df["Net Income"] / df["Total Revenue"]
    return df

# Define function to calculate all expense ratios
def calculate_expense_ratios(df: pd.DataFrame):
    """
    Calculate all expense ratios (Cost of Revenue, Operating Expense, and Interest Expense) for a specified DataFrame.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame. Must contain columns "Total Revenue", "Cost of Revenue", "Operating Expense", and "Interest Expense".

    Returns:
    pd.DataFrame: The DataFrame with additional columns for Cost of Revenue, Operating Expense, and Interest Expense Ratios.
    """
    df["Cost_of_Revenue_Ratio"] = df["Cost of Revenue"] / df["Total Revenue"]
    df["Operating_Expense_Ratio"] = df["Operating Expense"] / df["Total Revenue"]
    df["Interest_Expense_Ratio"] = df["Interest Expense"] / df["Total Revenue"]
    df["Tax_Provision_Ratio"] = df["Tax Provision"] / df["Total Revenue"]
    return df

# Define function to calculate cash flow ratios
def calculate_cashflow_ratios(df: pd.DataFrame):
    """
    Calculate cash flow ratios (Operating Cash Flow, Net Income from Continuing Operations, and Free Cash Flow) for a specified DataFrame.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame. Must contain columns "Total Revenue", "Operating Cash Flow", "Net Income from Continuing Operations", and "Free Cash Flow".

    Returns:
    pd.DataFrame: The DataFrame with additional columns for Operating Cash Flow, Net Income from Continuing Operations, and Free Cash Flow Ratios.
    """
    df["Cash_Conversion_Ratio"] = df["Operating Cash Flow"] / df["Net Income from Continuing Operations"]
    df["Free_Cash_Flow_Ratio"] = df["Free Cash Flow"] / df["Net Income from Continuing Operations"]
    return df