import pandas as pd
import os

# Path to the CSV file
csv_file = "tips.csv"
readme_file = "README.md"

# Read the CSV file
try:
    df = pd.read_csv(csv_file, header=0)
except FileNotFoundError:
    raise FileNotFoundError(f"{csv_file} not found")
except pd.errors.EmptyDataError:
    raise ValueError(f"{csv_file} is empty or invalid")

required_columns = ["Date", "Tips"]
if not all(col in df.columns for col in required_columns):
    missing_cols = [col for col in required_columns if col not in df.columns]
    raise ValueError(f"Missing columns: {', '.join(missing_cols)}")


# Convert date column to datetime
df["Date"] = pd.to_datetime(df["Date"], errors="coerce", dayfirst=True)

df = df.dropna(subset=["Date"])
if df.empty:
    print("No valid dates")
    with open(readme_file, "w") as f:
        f.write("""
# My Project

## Tips Data Overview

### Sample Data

### Monthly Tips Summary

*This section is automatically updated when `tips.csv` changes.*
"""
        )
    quit()
    







display_columns = ["Date", "Time-Worked", "Tips"]
df["Date_display"] = df["Date"].dt.strftime("%d.%m.%Y")
sample_data = df[["Date_display", "Time-Worked", "Tips"]].rename(columns={"Date_display": "Date"}).to_markdown(index=False)

# Calculate sum of tips per month
df["year_month"] = df["Date"].dt.strftime("%Y-%m")  # Format as YYYY-MM
monthly_tips = df.groupby("year_month")[["Tips", "Time-Worked"]].sum().round(2)

total_worked = df["Time-Worked"].sum()

# Format monthly tips as a Markdown list
monthly_tips_list = "\n".join(
    [f"- {month} - ({totals['Time-Worked']}h): CHF {totals['Tips']:.2f}" for month, totals in monthly_tips.iterrows()]
)

# Get last updated date
last_updated = df["Date"].max().strftime("%d-%m-%Y")

total_tips = df['Tips'].sum()

# Content to add to README
new_content = f"""# My Project

## Tips Data Overview
Last updated: {last_updated}

Total time worked since {df["Date_display"].head(1).values[0]}: {total_worked}

Total tips earned since {df["Date_display"].head(1).values[0]}: {total_tips}

### Monthly Tips Summary
{monthly_tips_list}

### Tip History
{sample_data}

*This section is automatically updated when `tips.csv` changes.*
"""

# Write to README.md
with open(readme_file, "w") as f:
    f.write(new_content)

print("README.md updated successfully!")
