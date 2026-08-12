import os
import pandas as pd

print("⚡ Starting Gold Layer Transformation (Star Schema Modeling)...")

SILVER_DIR = os.path.join("data", "lakehouse", "silver")
GOLD_DIR = os.path.join("data", "lakehouse", "gold")
os.makedirs(GOLD_DIR, exist_ok=True)

# Load Silver Clean Data
df_cust = pd.read_parquet(os.path.join(SILVER_DIR, "customers", "customers_clean.parquet"))
df_orders = pd.read_parquet(os.path.join(SILVER_DIR, "orders", "orders_clean.parquet"))
df_products = pd.read_parquet(os.path.join(SILVER_DIR, "products", "products_clean.parquet"))
df_returns = pd.read_parquet(os.path.join(SILVER_DIR, "returns", "returns_clean.parquet"))

# -------------------------------------------------------------
# 1. BUILD DIMENSION TABLES (dim_customers, dim_products, dim_date)
# -------------------------------------------------------------
print("\n🌟 [1/3] Building Dimension Tables...")

# 1.1 Dim Customers
dim_customers = df_cust[['customer_id', 'first_name', 'last_name', 'email', 'city', 'state', 'signup_date']].copy()
dim_customers['full_name'] = dim_customers['first_name'] + ' ' + dim_customers['last_name']
dim_customers.to_parquet(os.path.join(GOLD_DIR, "dim_customers.parquet"), index=False)
print(f"✅ Created dim_customers ({len(dim_customers)} rows)")

# 1.2 Dim Products
dim_products = df_products[['product_id', 'product_name', 'category', 'cost_price', 'selling_price', 'profit_margin']].copy()
dim_products.to_parquet(os.path.join(GOLD_DIR, "dim_products.parquet"), index=False)
print(f"✅ Created dim_products ({len(dim_products)} rows)")

# 1.3 Dim Date (Calendar Table)
all_dates = pd.to_datetime(df_orders['order_date']).unique()
dim_date = pd.DataFrame({'date': sorted(all_dates)})
dim_date['year'] = pd.to_datetime(dim_date['date']).dt.year
dim_date['quarter'] = 'Q' + pd.to_datetime(dim_date['date']).dt.quarter.astype(str)
dim_date['month'] = pd.to_datetime(dim_date['date']).dt.strftime('%B')
dim_date['month_num'] = pd.to_datetime(dim_date['date']).dt.month
dim_date['day_of_week'] = pd.to_datetime(dim_date['date']).dt.strftime('%A')
dim_date['is_weekend'] = pd.to_datetime(dim_date['date']).dt.dayofweek.isin([5, 6])

dim_date.to_parquet(os.path.join(GOLD_DIR, "dim_date.parquet"), index=False)
print(f"✅ Created dim_date ({len(dim_date)} rows)")

# -------------------------------------------------------------
# 2. BUILD FACT TABLE (fact_sales)
# -------------------------------------------------------------
print("\n🌟 [2/3] Building Fact Sales Table...")

# Join Orders with Products for Financials
fact_sales = df_orders.merge(dim_products[['product_id', 'cost_price', 'selling_price']], on='product_id', how='left')

# Rename selling_price to unit_price to match standard fact table naming
fact_sales.rename(columns={'selling_price': 'unit_price'}, inplace=True)

# Calculate Gross Financial Metrics
fact_sales['gross_revenue'] = fact_sales['quantity'] * fact_sales['unit_price']
fact_sales['total_cost'] = fact_sales['quantity'] * fact_sales['cost_price']
fact_sales['gross_profit'] = fact_sales['gross_revenue'] - fact_sales['total_cost']

# Flag Returns
returned_order_ids = set(df_returns['order_id'])
fact_sales['is_returned'] = fact_sales['order_id'].isin(returned_order_ids)
fact_sales['net_revenue'] = fact_sales.apply(lambda row: 0.0 if row['is_returned'] else row['gross_revenue'], axis=1)

# Clean Columns for Fact Storage
fact_cols = [
    'order_id', 'order_date', 'customer_id', 'product_id', 
    'quantity', 'unit_price', 'gross_revenue', 'total_cost', 
    'gross_profit', 'net_revenue', 'payment_method', 'order_status', 'is_returned'
]
fact_sales = fact_sales[fact_cols]
fact_sales.to_parquet(os.path.join(GOLD_DIR, "fact_sales.parquet"), index=False)
print(f"✅ Created fact_sales ({len(fact_sales)} rows)")

# -------------------------------------------------------------
# 3. BUILD AGGREGATED BUSINESS KPIS TABLE (agg_daily_sales)
# -------------------------------------------------------------
print("\n🌟 [3/3] Building Daily Sales Aggregates Table...")

agg_daily = fact_sales.groupby('order_date').agg(
    total_orders=('order_id', 'count'),
    gross_revenue=('gross_revenue', 'sum'),
    net_revenue=('net_revenue', 'sum'),
    total_profit=('gross_profit', 'sum'),
    total_returns=('is_returned', 'sum')
).reset_index()

agg_daily.to_parquet(os.path.join(GOLD_DIR, "agg_daily_sales.parquet"), index=False)
print(f"✅ Created agg_daily_sales ({len(agg_daily)} rows)")

print("\n🎉 GOLD LAYER TRANSFORMATIONS COMPLETE!")