import pandas as pd

def load_and_prepare_earnings_data(csv_path: str, skiprows: int = 15) -> pd.DataFrame:
    """
    Load order earnings data and prepare for COGS entry with selected columns.
    """
    df = pd.read_csv(csv_path, skiprows=skiprows, on_bad_lines='skip')

    # Convert earnings to numeric
    df['Order earnings'] = pd.to_numeric(df['Order earnings'], errors='coerce')

    # Define relevant columns
    selected_columns = [
        'Order creation date',
        'Item ID',
        'Item title',
        'Item price',
        'Quantity',
        'Gross amount',
        'Discount',
        'Order earnings'
    ]


    # Filter and add COGS column
    df_filtered = df[selected_columns].copy()
    df_filtered['COGS'] = 0.0

    return df_filtered

def compute_profit_summary(df: pd.DataFrame) -> dict:
    """
    Compute total revenue, COGS, and profit.
    """
    total_earnings = df['Order earnings'].sum()
    total_cogs = df['COGS'].sum()
    net_profit = total_earnings - total_cogs
    return {
        "Total Earnings": round(total_earnings, 2),
        "Total COGS": round(total_cogs, 2),
        "Net Profit": round(net_profit, 2)
    }

def main():
    # Step 1: Load and prep
    csv_path = "/Users/owen3/Desktop/main_directory/work/side_hustles/ebay/2024/Order_earnings_20240101_20250101.csv"
    df = load_and_prepare_earnings_data(csv_path)

    # Step 2: Export to Excel for COGS entry
    output_path = "earnings_with_cogs.xlsx"
    df.to_excel(output_path, index=False)
    print(f"\nCOGS column added. Please open and fill in costs here: {output_path}")

    # Step 3: Wait for user to input COGS
    input("\nAfter you've filled in the COGS column, press Enter to continue...")

    # Step 4: Reload updated file
    df_updated = pd.read_excel(output_path)

    # Step 5: Compute and show summary
    summary = compute_profit_summary(df_updated)
    print("\n📊 Profit Summary:")
    for key, value in summary.items():
        print(f"{key}: ${value}")

if __name__ == "__main__":
    main()

