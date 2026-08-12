import os
import pandas as pd

GOLD_DIR = os.path.join("data", "lakehouse", "gold")

print("==================================================")
print("📊 RETAILX GOLD LAYER DATA LAKEHOUSE REPORT")
print("==================================================")

# Load Fact & Daily KPI Tables
fact_sales = pd.read_parquet(os.path.join(GOLD_DIR, "fact_sales.parquet"))
agg_daily = pd.read_parquet(os.path.join(GOLD_DIR, "agg_daily_sales.parquet"))
dim_customers = pd.read_parquet(os.path.join(GOLD_DIR, "dim_customers.parquet"))
dim_products = pd.read_parquet(os.path.join(GOLD_DIR, "dim_products.parquet"))

print("\n💰 FINANCIAL SUMMARY (FACT SALES):")
print(f"• Total Orders Processed : {len(fact_sales)}")
print(f"• Total Gross Revenue    : ₹{fact_sales['gross_revenue'].sum():,.2f}")
print(f"• Total Net Revenue      : ₹{fact_sales['net_revenue'].sum():,.2f}")
print(f"• Total Gross Profit     : ₹{fact_sales['gross_profit'].sum():,.2f}")
print(f"• Total Returns Count    : {fact_sales['is_returned'].sum()}")

print("\n🏆 TOP PERFORMING PRODUCTS BY REVENUE:")
prod_summary = fact_sales.merge(dim_products, on="product_id") \
    .groupby("product_name") \
    .agg(Units_Sold=("quantity", "sum"), Net_Revenue=("net_revenue", "sum")) \
    .sort_values(by="Net_Revenue", ascending=False)
print(prod_summary.to_string())

print("\n👥 CUSTOMER PURCHASE SUMMARY:")
cust_summary = fact_sales.merge(dim_customers, on="customer_id") \
    .groupby("full_name") \
    .agg(Orders=("order_id", "count"), Spent=("net_revenue", "sum")) \
    .sort_values(by="Spent", ascending=False)
print(cust_summary.to_string())

print("\n==================================================")