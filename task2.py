# Process Soul foods

import pandas as pd

# Define file paths
file_paths = ["data/daily_sales_data_0.csv", "data/daily_sales_data_1.csv", "data/daily_sales_data_2.csv"]

# Read and combine csv files
dataframes = [pd.read_csv(file_path) for file_path in file_paths]
combined_df = pd.concat(dataframes, ignore_index=True)

# Filter for pink morsels
filtered_df = combined_df[combined_df["product"] == "pink morsel"]

# Ensure price is numerical
filtered_df["price"] = filtered_df["price"].str.replace("$", "", regex=False)
filtered_df["price"] = pd.to_numeric(filtered_df["price"], errors="coerce")

# Calculate sales
filtered_df["sales"] = filtered_df["price"] * filtered_df["quantity"]

# Add currency sign
filtered_df["sales"] = filtered_df["sales"].apply(lambda x: f"${x:,.2f}")

# Select relevant columns
final_df = filtered_df[["sales", "date", "region"]]

# Save to output file
output_file = "data/soul_data.csv"
final_df.to_csv(output_file, index=False)