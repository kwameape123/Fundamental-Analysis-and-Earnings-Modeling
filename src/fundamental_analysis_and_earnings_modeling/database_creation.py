""" The purpose of this module is to create a duckdb database with modeled data for fundamental analysis"""

# Import necessary libraries for database creation and manipulation
import duckdb
import pandas as pd
from Utils.load_data import load_database_dataframe, save_database_dataframe_to_csv
import os

##########
# Create a subset of all_analysis_data_database dataframe with only relevant quarters for year-over-year analysis
# of corresponding quarters
##########

# Load the all_analysis_data_database dataframe
all_analysis_data_database = load_database_dataframe("all_analysis_data")

# Create a dataframe for each quarter with selecting month in date that correspond to the quarter
q1_data = all_analysis_data_database[all_analysis_data_database['Date'].str[5:7].isin(['01'])]
q2_data = all_analysis_data_database[all_analysis_data_database['Date'].str[5:7].isin(['04'])]
q3_data = all_analysis_data_database[all_analysis_data_database['Date'].str[5:7].isin(['07'])]
q4_data = all_analysis_data_database[all_analysis_data_database['Date'].str[5:7].isin(['10'])]

# Save each quarter's dataframe to a folder in data folder named processed.
save_database_dataframe_to_csv(q1_data, "q1_data")
save_database_dataframe_to_csv(q2_data, "q2_data")
save_database_dataframe_to_csv(q3_data, "q3_data")
save_database_dataframe_to_csv(q4_data, "q4_data")

# Create a duckdb database and create a table with columns ticker and company name in new folder name database.
# Create folder with data folder if it does not exist
os.makedirs("data/database", exist_ok=True)
con = duckdb.connect("data/database/fundamental_analysis.db")
con.execute("""
CREATE TABLE IF NOT EXISTS company_info (
    Ticker VARCHAR PRIMARY KEY,
    company_name TEXT
)
""")

# Write the company information row into the company_info table manually
con.execute("""
INSERT INTO company_info (Ticker, company_name)
VALUES
('WMT', 'Walmart Inc.'),
('COST', 'Costco Wholesale Corporation'),
('DG', 'Dollar General Corporation'),
('DLTR', 'Dollar Tree Inc.'),
('TGT', 'Target Corporation')
ON CONFLICT (Ticker) DO NOTHING;
""")

# Create the all_analysis_data table.
con.execute("""
CREATE TABLE IF NOT EXISTS all_analysis_data (
    Date TEXT,
    Ticker VARCHAR,
    FOREIGN KEY (Ticker) REFERENCES company_info(Ticker),
    "Total Revenue" BIGINT,
    "Cost of Revenue" BIGINT,
    "Gross Profit" BIGINT,
    "Operating Expense" BIGINT,
    "Operating Income" BIGINT,
    "Interest Expense" BIGINT,
    "Tax Provision" BIGINT,
    "Net Income" BIGINT,
    Gross_Profit_Margin FLOAT,
    Operating_Profit_Margin FLOAT,
    Net_Profit_Margin FLOAT,
    Cost_of_Revenue_Ratio FLOAT,
    Operating_Expense_Ratio FLOAT,
    Interest_Expense_Ratio FLOAT,
    Tax_Provision_Ratio FLOAT,
    "Operating Cash Flow" BIGINT,
    "Free Cash Flow" BIGINT,
    Cash_Conversion_Ratio FLOAT,
    Free_Cash_Flow_Ratio FLOAT,
    PRIMARY KEY (Ticker, Date)
)
""")    

# Insert data rows from all_analysis_data_database csv file into the all_analysis_data table
con.execute(
    "INSERT INTO all_analysis_data (Date, Ticker, \"Total Revenue\", \"Cost of Revenue\", \"Gross Profit\", \"Operating Expense\", \"Operating Income\", \"Interest Expense\", \"Tax Provision\", \"Net Income\", Gross_Profit_Margin, Operating_Profit_Margin, Net_Profit_Margin, Cost_of_Revenue_Ratio, Operating_Expense_Ratio, Interest_Expense_Ratio, Tax_Provision_Ratio, \"Operating Cash Flow\", \"Free Cash Flow\", Cash_Conversion_Ratio, Free_Cash_Flow_Ratio) " \
    "SELECT csv.Date, csv.Ticker, csv.\"Total Revenue\", csv.\"Cost of Revenue\", csv.\"Gross Profit\", csv.\"Operating Expense\", csv.\"Operating Income\", csv.\"Interest Expense\", csv.\"Tax Provision\", csv.\"Net Income\", csv.Gross_Profit_Margin, csv.Operating_Profit_Margin, csv.Net_Profit_Margin, csv.Cost_of_Revenue_Ratio, csv.Operating_Expense_Ratio, csv.Interest_Expense_Ratio, csv.Tax_Provision_Ratio, csv.\"Operating Cash Flow\", csv.\"Free Cash Flow\", csv.Cash_Conversion_Ratio, csv.Free_Cash_Flow_Ratio " \
    "FROM read_csv('data/processed/all_analysis_data_database.csv') AS csv " \
    "ANTI JOIN all_analysis_data AS existing ON csv.Ticker = existing.Ticker AND csv.Date = existing.Date " \
    "QUALIFY row_number() OVER (PARTITION BY csv.Ticker, csv.Date ORDER BY csv.Ticker) = 1;")

# Close the database connection
con.close()