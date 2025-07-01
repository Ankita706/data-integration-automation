# Data Integration and Automation Project 
This project demonstrates how to go beyond static datasets (like those from Kaggle) and generate your own realistic business data, enrich it using real-world economic indicators from APIs, and automate the entire data pipeline — all in Python.

This is a practical use case for analysts, data scientists, and developers who want to simulate, validate, and deliver data in a real-world scenario.

# Why This Project?
In real-world data roles, you rarely get clean datasets handed to you.
You create, clean, validate, and enrich your data yourself.
This project shows you how to:

Simulate weekly sales data for 50 products over a year

Pull real-world gas prices and inflation (CPI) from the FRED API

Merge and align this external data with sales

Run automated data quality checks

Output a ready-to-analyze file in CSV format

# Folder Structure
data-integration-automation/
│
├── data_integration_automation/
│   └── data_integration_automation.py     # Main Python script
│
├── merged_sales_data/
│   └── merged_sales_data.csv              # Final enriched dataset
│
├── data_quality_log/
│   └── data_quality_log.txt               # Log of data quality issues
│
├── requirements.txt                       # Python dependencies
└── README.md                              # You're reading it!

# How to Run the Project
1. Install Python dependencies

pip install -r requirements.txt

Or install manually:

pip install pandas numpy requests

2. Update File Paths (Optional)
   
Ensure these folders exist:

merged_sales_data/

data_quality_log/

If needed, update paths inside data_integration_automation.py:

OUTPUT_PATH = "merged_sales_data/merged_sales_data.csv"
LOG_PATH = "data_quality_log/data_quality_log.txt"

3. Run the Script

python data_integration_automation/data_integration_automation.py

# What Happens When You Run the Script?
Simulates Weekly Sales Data

50 products × 52 weeks = 2,600+ rows of fake but realistic sales data.

Includes pricing, discounts, revenue, and region (USA).

Fetches Economic Indicators

Gas Prices (weekly) and CPI (monthly) from the official FRED API.

API key is already included for ease of testing.

Merges and Aligns the Data

Aligns weekly gas prices with sales weeks.

Aligns CPI with the corresponding sales month.

Fills missing values if data is delayed or not available.

Performs Data Quality Checks

Detects missing values

Flags strange sales anomalies (sudden spikes or drops)

Verifies that all 50 products appear each week

Creates Output Files

Saves a final enriched dataset: merged_sales_data.csv

Logs any issues to: data_quality_log.txt (deletes this file if no issues found)

# Example Use Cases
- Build real-time dashboards with simulated + real data

- Test anomaly detection techniques

- Analyze how gas prices or inflation affect product sales

- Learn API integration, data automation, and quality validation

FAQs
# Why simulate data when Kaggle exists?
Because real-world projects often start with no data — you create it using APIs, logs, or systems. This builds real-world confidence.

# Why is Gas Price weekly and CPI monthly?
Gas prices fluctuate frequently, so they are reported weekly.
CPI reflects broader inflation trends, so it’s reported monthly.

# What if the API doesn't work?
You can check your internet connection or get a free API key from FRED.

# Project Highlights
Feature	Description
🔄 Data Simulation	Creates fake but realistic business data
🌐 API Integration	Uses FRED API for economic indicators
🔗 Data Merging Logic	Aligns timeframes with real-world rules
⚠️ Data Quality Validation	Ensures completeness and flags anomalies
🧹 Clean Final Output	Delivers a polished CSV file ready for dashboards/reports

# Final Note
This project is a reminder that you don’t need to rely on public datasets alone.
With Python and a bit of logic, you can simulate, enrich, and automate your own data pipeline — just like it happens in real-world data teams.

# License & Attribution 
FRED Data: U.S. Federal Reserve Economic Data

Built by: Ankita Ahirwar 

