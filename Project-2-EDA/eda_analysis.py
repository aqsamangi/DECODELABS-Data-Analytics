import pandas as pd            # for working with the spreadsheet data  # type: ignore[import]
import numpy as np             # for numerical calculations  # type: ignore[import]
import matplotlib.pyplot as plt  # for creating charts  # type: ignore[import]
import matplotlib.ticker as mticker  # type: ignore[import]

INPUT_FILE = "Cleaned_Dataset_for_Data_Analytics.xlsx"

# Columns that hold numbers we want to analyze statistically
NUMERIC_COLUMNS = ["Quantity", "UnitPrice", "ItemsInCart", "TotalPrice"]

# Columns that hold categories (text groups) we want frequency counts for
CATEGORICAL_COLUMNS = ["Product", "PaymentMethod", "OrderStatus",
                        "ReferralSource", "CouponCode"]


def section(title):
    """Small helper to print a neat section header in the terminal."""
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def main():
    # LOAD THE CLEANED DATA
    section("STEP 1: LOADING THE CLEANED DATA")
    df = pd.read_excel(INPUT_FILE)
    df["Date"] = pd.to_datetime(df["Date"])  # make sure Date is a real date

    print(f"Loaded '{INPUT_FILE}'")
    print(f"Rows: {df.shape[0]} | Columns: {df.shape[1]}")
    print(f"Column names: {list(df.columns)}")

    # CONFIRM NO MISSING VALUES REMAIN
    section("STEP 2: MISSING VALUE CHECK (should be 0 after Project 1)")
    missing = df.isnull().sum()
    total_missing = missing.sum()
    print(missing)
    print(f"\nTotal missing values in the whole dataset: {total_missing}")
    if total_missing == 0:
        print("Confirmed: no missing values remain.")

    # SUMMARY STATISTICS FOR NUMERIC COLUMNS
    section("STEP 3: SUMMARY STATISTICS (Count, Mean, Median, Mode, "
            "Min, Max, Std Dev, Variance, Quartiles)")

    stats_rows = []
    for col in NUMERIC_COLUMNS:
        data = df[col]
        stats_rows.append({
            "Column": col,
            "Count": data.count(),
            "Mean": round(data.mean(), 2),
            "Median": round(data.median(), 2),
            "Mode": data.mode().iloc[0],
            "Min": data.min(),
            "Max": data.max(),
            "StdDev": round(data.std(), 2),
            "Variance": round(data.var(), 2),
            "Q1 (25%)": round(data.quantile(0.25), 2),
            "Q3 (75%)": round(data.quantile(0.75), 2),
        })
    stats_df = pd.DataFrame(stats_rows)
    print(stats_df.to_string(index=False))

    # FREQUENCY COUNTS FOR CATEGORICAL COLUMNS
    section("STEP 4: FREQUENCY COUNTS (categorical columns)")
    for col in CATEGORICAL_COLUMNS:
        print(f"\n--- {col} ---")
        print(df[col].value_counts())

    # OUTLIER DETECTION (IQR METHOD)
    section("STEP 5: OUTLIER DETECTION (IQR method)")
    outlier_summary = {}
    for col in NUMERIC_COLUMNS:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        outlier_summary[col] = len(outliers)
        print(f"{col}: {len(outliers)} outlier(s) "
              f"(normal range: {round(lower_bound,2)} to {round(upper_bound,2)})")

    # CORRELATION ANALYSIS
    section("STEP 6: CORRELATION ANALYSIS (numeric columns)")
    corr_matrix = df[NUMERIC_COLUMNS].corr().round(2)
    print(corr_matrix)

    # TREND CHECK OVER TIME
    section("STEP 7: TREND OVER TIME (monthly orders & revenue)")
    df["YearMonth"] = df["Date"].dt.to_period("M")
    monthly = df.groupby("YearMonth").agg(
        Orders=("OrderID", "count"),
        Revenue=("TotalPrice", "sum")
    ).reset_index()
    monthly["YearMonth"] = monthly["YearMonth"].astype(str)
    print(monthly.to_string(index=False))

    # VISUALIZATIONS - saved as PNG files
    section("STEP 8: CREATING AND SAVING CHARTS")
    plt.rcParams["figure.autolayout"] = True

    # Chart 1: Histogram of TotalPrice (distribution of order values) 
    plt.figure(figsize=(8, 5))
    plt.hist(df["TotalPrice"], bins=30, color="#4C72B0", edgecolor="white")
    plt.title("Distribution of Order Total Price")
    plt.xlabel("Total Price ($)")
    plt.ylabel("Number of Orders")
    plt.savefig("chart1_totalprice_histogram.png", dpi=150)
    plt.close()
    print("Saved: chart1_totalprice_histogram.png")

    # Chart 2: Bar chart of orders per Product 
    plt.figure(figsize=(8, 5))
    df["Product"].value_counts().sort_values().plot(kind="barh", color="#55A868")
    plt.title("Number of Orders per Product")
    plt.xlabel("Number of Orders")
    plt.ylabel("Product")
    plt.savefig("chart2_orders_per_product.png", dpi=150)
    plt.close()
    print("Saved: chart2_orders_per_product.png")

    # Chart 3: Bar chart of revenue per Product 
    plt.figure(figsize=(8, 5))
    df.groupby("Product")["TotalPrice"].sum().sort_values().plot(
        kind="barh", color="#C44E52")
    plt.title("Total Revenue per Product")
    plt.xlabel("Revenue ($)")
    plt.ylabel("Product")
    plt.gca().xaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    plt.savefig("chart3_revenue_per_product.png", dpi=150)
    plt.close()
    print("Saved: chart3_revenue_per_product.png")

    # Chart 4: Box plot of TotalPrice (shows spread + outliers visually) 
    plt.figure(figsize=(6, 5))
    plt.boxplot(df["TotalPrice"], vert=True, patch_artist=True,
                boxprops=dict(facecolor="#8172B2"))
    plt.title("Box Plot of Order Total Price (outlier check)")
    plt.ylabel("Total Price ($)")
    plt.savefig("chart4_totalprice_boxplot.png", dpi=150)
    plt.close()
    print("Saved: chart4_totalprice_boxplot.png")

    # Chart 5: Scatter plot of Quantity vs TotalPrice 
    plt.figure(figsize=(8, 5))
    plt.scatter(df["Quantity"], df["TotalPrice"], alpha=0.5, color="#4C72B0")
    plt.title("Quantity vs Total Price")
    plt.xlabel("Quantity")
    plt.ylabel("Total Price ($)")
    plt.savefig("chart5_quantity_vs_totalprice_scatter.png", dpi=150)
    plt.close()
    print("Saved: chart5_quantity_vs_totalprice_scatter.png")

    # Chart 6: Correlation heatmap 
    plt.figure(figsize=(6, 5))
    plt.imshow(corr_matrix, cmap="coolwarm", vmin=-1, vmax=1)
    plt.colorbar(label="Correlation")
    plt.xticks(range(len(NUMERIC_COLUMNS)), NUMERIC_COLUMNS, rotation=45, ha="right")
    plt.yticks(range(len(NUMERIC_COLUMNS)), NUMERIC_COLUMNS)
    for i in range(len(NUMERIC_COLUMNS)):
        for j in range(len(NUMERIC_COLUMNS)):
            plt.text(j, i, corr_matrix.iloc[i, j], ha="center", va="center",
                      color="black")
    plt.title("Correlation Heatmap (numeric columns)")
    plt.savefig("chart6_correlation_heatmap.png", dpi=150)
    plt.close()
    print("Saved: chart6_correlation_heatmap.png")

    # KEY OBSERVATIONS
    section("STEP 9: KEY OBSERVATIONS")
    top_product_orders = df["Product"].value_counts().idxmax()
    top_product_revenue = df.groupby("Product")["TotalPrice"].sum().idxmax()
    top_payment = df["PaymentMethod"].value_counts().idxmax()
    top_status = df["OrderStatus"].value_counts().idxmax()
    strongest_corr = corr_matrix.where(
        ~np.eye(len(corr_matrix), dtype=bool)).abs().stack().idxmax()

    print(f"- Most frequently ordered product: {top_product_orders}")
    print(f"- Product generating the most total revenue: {top_product_revenue}")
    print(f"- Most common payment method: {top_payment}")
    print(f"- Most common order status: {top_status}")
    print(f"- Strongest relationship between numeric columns: "
          f"{strongest_corr[0]} & {strongest_corr[1]} "
          f"(correlation = {corr_matrix.loc[strongest_corr[0], strongest_corr[1]]})")
    print(f"- TotalPrice outliers found (IQR method): {outlier_summary['TotalPrice']}")
    print("- Order categories (Product, PaymentMethod, OrderStatus, "
          "ReferralSource) are all fairly evenly distributed - no single "
          "category dominates heavily.")

    print("\nAll statistics, charts, and observations are complete.")


if __name__ == "__main__":
    main()