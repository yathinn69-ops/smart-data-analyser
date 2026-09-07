"""
Smart Data Analyser
-------------------
Loads a sales CSV, cleans the data, performs basic analysis,
exports summary results, and creates visualizations.

Run:
    python src/data_analyser.py
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "sales_data.csv"
OUTPUT_DIR = BASE_DIR / "output"
VIS_DIR = BASE_DIR / "visualizations"

OUTPUT_DIR.mkdir(exist_ok=True)
VIS_DIR.mkdir(exist_ok=True)


def load_and_clean_data(path):
    df = pd.read_csv(path)
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    df["Category"] = df["Category"].fillna("Unknown")
    df["Discount"] = df["Discount"].fillna(0)
    df["Revenue"] = df["Revenue"].fillna(0)
    return df


def analyse(df):
    total_revenue = df["Revenue"].sum()
    total_units = df["Units_Sold"].sum()
    average_order_revenue = df["Revenue"].mean()

    product_revenue = df.groupby("Product")["Revenue"].sum().sort_values(ascending=False)
    category_revenue = df.groupby("Category")["Revenue"].sum().sort_values(ascending=False)
    monthly_revenue = df.groupby(df["Order_Date"].dt.to_period("M"))["Revenue"].sum()

    summary = pd.DataFrame({
        "Metric": [
            "Total Revenue",
            "Total Units Sold",
            "Average Order Revenue",
            "Best-Selling Product by Revenue",
            "Top Category by Revenue",
            "Number of Orders",
        ],
        "Value": [
            round(total_revenue, 2),
            int(total_units),
            round(average_order_revenue, 2),
            product_revenue.index[0],
            category_revenue.index[0],
            len(df),
        ],
    })

    return summary, product_revenue, category_revenue, monthly_revenue


def save_results(summary):
    summary.to_csv(OUTPUT_DIR / "analysis_results.csv", index=False)


def create_charts(product_revenue, category_revenue, monthly_revenue):
    plt.figure(figsize=(9, 5))
    monthly_revenue.plot(kind="line", marker="o")
    plt.title("Monthly Revenue Trend")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(VIS_DIR / "monthly_sales.png", dpi=160)
    plt.close()

    plt.figure(figsize=(8, 5))
    category_revenue.plot(kind="bar")
    plt.title("Revenue by Category")
    plt.xlabel("Category")
    plt.ylabel("Revenue")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(VIS_DIR / "category_sales.png", dpi=160)
    plt.close()

    plt.figure(figsize=(9, 5))
    product_revenue.head(5).plot(kind="bar")
    plt.title("Top 5 Products by Revenue")
    plt.xlabel("Product")
    plt.ylabel("Revenue")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(VIS_DIR / "top_products.png", dpi=160)
    plt.close()


def main():
    df = load_and_clean_data(DATA_FILE)
    summary, product_revenue, category_revenue, monthly_revenue = analyse(df)
    save_results(summary)
    create_charts(product_revenue, category_revenue, monthly_revenue)

    print("Smart Data Analyser completed successfully.")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
