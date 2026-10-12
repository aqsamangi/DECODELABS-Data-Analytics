import pandas as pd                 # for working with the spreadsheet data
import matplotlib.pyplot as plt     # for building charts
import matplotlib.ticker as mticker  # for formatting axis labels (e.g. $)
import seaborn as sns               # used only where it genuinely helps
                                     # (box plot, count plot, heatmap)

INPUT_FILE = "Cleaned_Dataset_for_Data_Analytics.xlsx"

# A consistent, readable look for every chart in this script
sns.set_style("whitegrid")
plt.rcParams["figure.autolayout"] = True
plt.rcParams["font.size"] = 11


def describe(title, text):
    """Small helper to print a chart's explanation neatly."""
    print("\n" + "-" * 70)
    print(title)
    print("-" * 70)
    print(text)


def main():
    # LOAD THE CLEANED DATA
    print("=" * 70)
    print("LOADING THE CLEANED DATA")
    print("=" * 70)
    df = pd.read_excel(INPUT_FILE)
    df["Date"] = pd.to_datetime(df["Date"])
    print(f"Loaded '{INPUT_FILE}' - {df.shape[0]} rows, {df.shape[1]} columns")

    # -----------------------------------------------------------
    # CHART 1: HISTOGRAM - distribution of order values
    # -----------------------------------------------------------
    # WHY a histogram: TotalPrice is a continuous number, and a
    # histogram is the standard chart for showing the SHAPE of a
    # continuous variable's distribution (symmetric vs skewed).
    plt.figure(figsize=(8, 5))
    plt.hist(df["TotalPrice"], bins=30, color="#4C72B0", edgecolor="white")
    plt.title("Distribution of Order Total Price", fontsize=14, fontweight="bold")
    plt.xlabel("Total Price ($)")
    plt.ylabel("Number of Orders")
    plt.savefig("viz1_histogram_totalprice.png", dpi=200)
    plt.close()
    describe(
        "CHART 1 - Histogram: Distribution of Order Total Price",
        "This shows how order values are spread out. The shape is "
        "right-skewed (a long tail toward high values) rather than a "
        "symmetric bell curve - most orders are small-to-mid value, with "
        "fewer large ones pulling the tail to the right. Business "
        "insight: the 'typical' order is smaller than the average dollar "
        "amount suggests."
    )

    # -----------------------------------------------------------
    # CHART 2: BOX PLOT - TotalPrice spread by Product
    # -----------------------------------------------------------
    # WHY a box plot: it compares the spread AND outliers of a numeric
    # variable ACROSS multiple categories at once - better than a single
    # box plot when we want to compare products against each other.
    plt.figure(figsize=(9, 5))
    sns.boxplot(data=df, x="Product", y="TotalPrice", hue="Product",
                palette="Set2", legend=False)
    plt.title("Order Value Spread by Product", fontsize=14, fontweight="bold")
    plt.xlabel("Product")
    plt.ylabel("Total Price ($)")
    plt.xticks(rotation=20)
    plt.savefig("viz2_boxplot_totalprice_by_product.png", dpi=200)
    plt.close()
    describe(
        "CHART 2 - Box Plot: Order Value Spread by Product",
        "Each box shows the middle 50% of order values for that product, "
        "with the line inside as the median and dots above/below as "
        "outliers. All 7 products show a similar wide spread and a "
        "handful of high-value outlier orders - no single product "
        "behaves very differently from the others in terms of price "
        "spread."
    )

    # -----------------------------------------------------------
    # CHART 3: BAR CHART - total revenue per Payment Method
    # -----------------------------------------------------------
    # WHY a bar chart: PaymentMethod is a small set of categories, and
    # we want to compare ONE total number (revenue) across them - the
    # classic use case for a bar chart.
    revenue_by_payment = df.groupby("PaymentMethod")["TotalPrice"].sum().sort_values()
    plt.figure(figsize=(8, 5))
    revenue_by_payment.plot(kind="barh", color="#55A868")
    plt.title("Total Revenue by Payment Method", fontsize=14, fontweight="bold")
    plt.xlabel("Total Revenue ($)")
    plt.ylabel("Payment Method")
    plt.gca().xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    plt.savefig("viz3_barchart_revenue_by_payment.png", dpi=200)
    plt.close()
    describe(
        "CHART 3 - Bar Chart: Total Revenue by Payment Method",
        f"Revenue is fairly evenly split across all 5 payment methods "
        f"(no single one dominates). The highest-earning method is "
        f"'{revenue_by_payment.idxmax()}' at ${revenue_by_payment.max():,.2f}, "
        f"and the lowest is '{revenue_by_payment.idxmin()}' at "
        f"${revenue_by_payment.min():,.2f}. This suggests customers are not "
        "strongly favoring one payment option over another."
    )

    # -----------------------------------------------------------
    # CHART 4: PIE CHART - share of orders by Order Status
    # -----------------------------------------------------------
    # WHY a pie chart: OrderStatus has a small number of categories
    # (5) and we specifically want to show each one's SHARE of the
    # whole (100% of orders) - exactly what a pie chart is for.
    status_counts = df["OrderStatus"].value_counts()
    plt.figure(figsize=(7, 7))
    plt.pie(
        status_counts,
        labels=status_counts.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=sns.color_palette("Set2", len(status_counts)),
    )
    plt.title("Share of Orders by Order Status", fontsize=14, fontweight="bold")
    plt.savefig("viz4_piechart_orderstatus_share.png", dpi=200)
    plt.close()
    cancelled_returned_pct = (
        status_counts.get("Cancelled", 0) + status_counts.get("Returned", 0)
    ) / status_counts.sum() * 100
    describe(
        "CHART 4 - Pie Chart: Share of Orders by Order Status",
        f"Orders are almost evenly split across all 5 statuses, with "
        f"Cancelled slightly the largest slice ({status_counts.max()} orders). "
        f"The important insight: Cancelled + Returned together make up "
        f"about {cancelled_returned_pct:.1f}% of ALL orders - meaning "
        "nearly 2 in 5 orders never end up successfully delivered."
    )

    # -----------------------------------------------------------
    # CHART 5: LINE CHART - revenue trend over time (monthly)
    # -----------------------------------------------------------
    # WHY a line chart: Date is a continuous time variable, and a line
    # chart is the standard way to show how a number changes over time
    # (a trend), which bar/pie/histogram cannot show as clearly.
    df["YearMonth"] = df["Date"].dt.to_period("M")
    monthly_revenue = df.groupby("YearMonth")["TotalPrice"].sum()
    monthly_revenue.index = monthly_revenue.index.astype(str)
    plt.figure(figsize=(11, 5))
    plt.plot(monthly_revenue.index, monthly_revenue.values,
              marker="o", color="#C44E52", linewidth=1.5, markersize=4)
    plt.title("Monthly Revenue Trend", fontsize=14, fontweight="bold")
    plt.xlabel("Month")
    plt.ylabel("Revenue ($)")
    plt.xticks(rotation=90, fontsize=8)
    plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    plt.savefig("viz5_linechart_monthly_revenue.png", dpi=200)
    plt.close()
    describe(
        "CHART 5 - Line Chart: Monthly Revenue Trend",
        "This tracks total revenue month by month across the full date "
        "range in the dataset. The line moves up and down without a "
        "clear steady upward or downward direction, and there is no "
        "obvious repeating seasonal pattern (like a holiday spike every "
        "December) - revenue simply fluctuates month to month."
    )

    # -----------------------------------------------------------
    # CHART 6: SCATTER PLOT - UnitPrice vs TotalPrice
    # -----------------------------------------------------------
    # WHY a scatter plot: both UnitPrice and TotalPrice are continuous
    # numbers, and a scatter plot is the right chart to see if two
    # numeric variables move together (a relationship).
    plt.figure(figsize=(8, 5))
    plt.scatter(df["UnitPrice"], df["TotalPrice"], alpha=0.5, color="#4C72B0")
    plt.title("Unit Price vs Total Price", fontsize=14, fontweight="bold")
    plt.xlabel("Unit Price ($)")
    plt.ylabel("Total Price ($)")
    plt.savefig("viz6_scatterplot_unitprice_vs_totalprice.png", dpi=200)
    plt.close()
    corr_value = df["UnitPrice"].corr(df["TotalPrice"])
    describe(
        "CHART 6 - Scatter Plot: Unit Price vs Total Price",
        f"There's a clear upward drift - as UnitPrice goes up, TotalPrice "
        f"tends to go up too (correlation = {corr_value:.2f}, a moderate-"
        "to-strong positive relationship). The points are not tightly "
        "packed on a single line, though, because Quantity also affects "
        "TotalPrice - UnitPrice alone doesn't fully determine it."
    )

    # -----------------------------------------------------------
    # CHART 7: CORRELATION HEATMAP - numeric columns
    # -----------------------------------------------------------
    # WHY a heatmap: with 4 numeric columns, a heatmap lets us see ALL
    # pairwise relationships at once, using color instead of reading
    # a table of numbers one by one.
    numeric_cols = ["Quantity", "UnitPrice", "ItemsInCart", "TotalPrice"]
    corr_matrix = df[numeric_cols].corr()
    plt.figure(figsize=(6.5, 5.5))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", vmin=-1, vmax=1, fmt=".2f")
    plt.title("Correlation Heatmap (Numeric Columns)", fontsize=14, fontweight="bold")
    plt.savefig("viz7_correlation_heatmap.png", dpi=200)
    plt.close()
    strongest = corr_matrix.where(
        ~pd.DataFrame(
            [[i == j for j in numeric_cols] for i in numeric_cols],
            index=numeric_cols, columns=numeric_cols
        )
    ).abs().stack().idxmax()
    describe(
        "CHART 7 - Correlation Heatmap: Numeric Columns",
        f"Darker red means a stronger positive relationship. The "
        f"strongest relationship in the whole dataset is between "
        f"'{strongest[0]}' and '{strongest[1]}' "
        f"(correlation = {corr_matrix.loc[strongest[0], strongest[1]]:.2f}). "
        "Important caveat: correlation shows two numbers move together, "
        "not that one causes the other."
    )

    # -----------------------------------------------------------
    # CHART 8: COUNT PLOT - number of orders per Referral Source
    # -----------------------------------------------------------
    # WHY a count plot: ReferralSource is categorical, and we simply
    # want to count how many orders came from each source - a count
    # plot (seaborn's version of a bar chart built for counting rows)
    # is the natural fit and adds cleaner default styling here.
    plt.figure(figsize=(8, 5))
    order = df["ReferralSource"].value_counts().index
    sns.countplot(data=df, y="ReferralSource", order=order, hue="ReferralSource",
                  palette="Set2", legend=False)
    plt.title("Number of Orders per Referral Source", fontsize=14, fontweight="bold")
    plt.xlabel("Number of Orders")
    plt.ylabel("Referral Source")
    plt.savefig("viz8_countplot_referralsource.png", dpi=200)
    plt.close()
    top_source = df["ReferralSource"].value_counts().idxmax()
    describe(
        "CHART 8 - Count Plot: Number of Orders per Referral Source",
        f"'{top_source}' brought in the most orders, but every source "
        "is fairly close in count - no single referral channel "
        "dominates the customer base. This suggests marketing spend "
        "is currently spread across channels rather than concentrated."
    )

    print("\n" + "=" * 70)
    print("ALL 8 CHARTS CREATED AND SAVED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":
    main()