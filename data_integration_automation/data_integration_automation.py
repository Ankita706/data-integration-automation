import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
import os

#Configuration
FRED_API_KEY = "0d745001a1668064bf4f07221d11802c"
GAS_URL = f"https://api.stlouisfed.org/fred/series/observations?series_id=GASREGW&api_key={FRED_API_KEY}&file_type=json"
CPI_URL = f"https://api.stlouisfed.org/fred/series/observations?series_id=CPIAUCSL&api_key={FRED_API_KEY}&file_type=json"
OUTPUT_PATH = "C:/Users/Ankita/OneDrive/Desktop/Data_Integration_Project/merged_sales_data/merged_sales_data.csv"
LOG_PATH = "C:/Users/Ankita/OneDrive/Desktop/Data_Integration_Project/data_quality_log/data_quality_log.txt"

#Utility Functions 

def fetch_fred_data(url, date_col="date", value_col="value", new_col_name=""):
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch data: {url}")
    json_data = response.json()["observations"]
    df = pd.DataFrame(json_data)
    df['date'] = pd.to_datetime(df['date'])
    df['value'] = pd.to_numeric(df['value'], errors="coerce")
    df = df.rename(columns={value_col: new_col_name})
    return df[[date_col, new_col_name]]

def generate_sales_data(start_date, weeks):
    np.random.seed(42)
    week_dates = [start_date + timedelta(weeks=i) for i in range(weeks)]
    product_ids = [f"P{i:03}" for i in range(1, 51)]
    product_names = [f"Product_{i}" for i in range(1, 51)]
    data = []

    for week_start in week_dates:
        for pid, pname in zip(product_ids, product_names):
            base_price = np.random.uniform(5, 50)
            discount = np.random.choice([0, 5, 10, 15, 20], p=[0.5, 0.2, 0.15, 0.1, 0.05])
            effective_price = base_price * (1 - discount / 100)
            week_of_year = week_start.isocalendar().week
            seasonality = 1.5 if 48 <= week_of_year <= 52 else 1.2 if 22 <= week_of_year <= 35 else 1.0
            units_sold = max(int(np.random.normal(loc=20, scale=5) * seasonality), 0)
            revenue = units_sold * effective_price

            data.append({
                "Week Start Date": week_start,
                "Product ID": pid,
                "Product Name": pname,
                "Units Sold": units_sold,
                "Price ($)": round(base_price, 2),
                "Discount Percentage": discount,
                "Revenue ($)": round(revenue, 2),
                "Region": "USA"
            })

    return pd.DataFrame(data)

def merge_economic_data(sales_df, gas_df, cpi_df):
    sales_df['Week Start Date'] = pd.to_datetime(sales_df['Week Start Date'])
    gas_df['date'] = pd.to_datetime(gas_df['date'])
    cpi_df['date'] = pd.to_datetime(cpi_df['date'])

    sales_df = sales_df.sort_values('Week Start Date')
    gas_df = gas_df.sort_values('date')
    cpi_df = cpi_df.sort_values('date')

    merged = pd.merge_asof(sales_df, gas_df.rename(columns={"date": "Gas Date", "Avg Gas Price": "Avg Gas Price"}), 
                           left_on='Week Start Date', right_on='Gas Date', direction='backward')
    merged = merged.drop(columns=["Gas Date"])

    cpi_df['Month'] = cpi_df['date'].dt.to_period('M')
    cpi_df = cpi_df.rename(columns={"value": "CPI"}).drop(columns=["date"])
    merged['Month'] = merged['Week Start Date'].dt.to_period('M')
    merged = merged.merge(cpi_df.drop_duplicates(), on="Month", how="left")
    merged = merged.drop(columns=["Month"])

    merged[['Avg Gas Price', 'CPI']] = merged[['Avg Gas Price', 'CPI']].fillna(method='ffill').fillna(method='bfill')

    return merged

def check_data_quality(df):
    issues = []
    if df.isnull().any().any():
        issues.append("Missing values detected.")
    weekly_sales = df.groupby("Week Start Date")["Units Sold"].sum()
    z_scores = (weekly_sales - weekly_sales.mean()) / weekly_sales.std()
    if (z_scores.abs() > 3).any():
        issues.append("Anomalies detected in weekly sales.")
    expected = set(df["Product ID"].unique())
    for date in df["Week Start Date"].unique():
        present = set(df[df["Week Start Date"] == date]["Product ID"])
        if expected != present:
            issues.append(f"Missing products on {date.date()}")
    return issues

def log_issues(issues):
    if issues:
        with open(LOG_PATH, "w") as f:
            for issue in issues:
                f.write(issue + "\n")
        print("  Data issues found. Logged.")
    else:
        if os.path.exists(LOG_PATH):
            os.remove(LOG_PATH)
        print(" Data integrity check passed.")

#  Final Execution 

def full_run():
    print(" Starting full pipeline...")

    # Step 1: Generate full-year sales data
    print(" Generating sales data for 2024...")
    sales_df = generate_sales_data(start_date=datetime(2024, 1, 7), weeks=52)

    # Step 2: Fetch economic data
    print(" Fetching economic indicators from FRED...")
    gas_df = fetch_fred_data(GAS_URL, new_col_name="Avg Gas Price")
    cpi_df = fetch_fred_data(CPI_URL, new_col_name="CPI")

    # Step 3: Merge datasets
    print(" Merging datasets...")
    merged_df = merge_economic_data(sales_df, gas_df, cpi_df)

    # Step 4: Data quality checks
    print(" Running data quality checks...")
    issues = check_data_quality(merged_df)
    log_issues(issues)

    # Step 5: Save to file
    print(f" Saving final merged dataset to: {OUTPUT_PATH}")
    merged_df.to_csv(OUTPUT_PATH, index=False)
    print(" Pipeline complete.")

if __name__ == "__main__":
    full_run()
