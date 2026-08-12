import os
import pandas as pd
import numpy as np

print("⚡ Starting Silver Layer Cleaning & Standardization...")

BRONZE_DIR = os.path.join("data", "lakehouse", "bronze")
SILVER_DIR = os.path.join("data", "lakehouse", "silver")
QUARANTINE_DIR = os.path.join("data", "lakehouse", "quarantine")

for d in [SILVER_DIR, QUARANTINE_DIR]:
    for folder in ["customers", "orders", "products", "returns", "inventory"]:
        os.makedirs(os.path.join(d, folder), exist_ok=True)

# -------------------------------------------------------------
# 1. CLEAN CUSTOMERS
# -------------------------------------------------------------
print("\n🧹 [1/5] Processing Customers...")
df_cust = pd.read_parquet(os.path.join(BRONZE_DIR, "customers", "customers_raw.parquet"))
df_cust["email"] = df_cust["email"].str.lower().str.strip()
df_cust["first_name"] = df_cust["first_name"].str.title().str.strip()
df_cust["last_name"] = df_cust["last_name"].str.title().str.strip()
df_cust.drop_duplicates(subset=["customer_id"], keep="first", inplace=True)

df_cust.to_parquet(os.path.join(SILVER_DIR, "customers", "customers_clean.parquet"), index=False)
print(f"✅ Clean Customers saved. Valid count: {len(df_cust)}")

# -------------------------------------------------------------
# 2. CLEAN ORDERS & DATA QUALITY QUARANTINE CHECK
# -------------------------------------------------------------
print("\n🧹 [2/5] Processing Orders & Performing Quarantine Checks...")
df_orders = pd.read_parquet(os.path.join(BRONZE_DIR, "orders", "orders_raw.parquet"))

# Deduplication
initial_count = len(df_orders)
df_orders.drop_duplicates(keep="first", inplace=True)
dedup_count = len(df_orders)

# Standardize Strings
df_orders["payment_method"] = df_orders["payment_method"].str.replace("_", " ").str.title().str.strip()
df_orders["order_status"] = df_orders["order_status"].str.title().str.strip()

# Standardize Dates
df_orders["order_date"] = pd.to_datetime(df_orders["order_date"], format='mixed').dt.strftime('%Y-%m-%d')

# Data Quality Rule: Identify Orphan Customer IDs (Customer 9999 doesn't exist in Customers master)
valid_customer_ids = set(df_cust["customer_id"])
valid_orders_mask = df_orders["customer_id"].isin(valid_customer_ids)

df_valid_orders = df_orders[valid_orders_mask].copy()
df_quarantine_orders = df_orders[~valid_orders_mask].copy()

# Save Silver & Quarantine
df_valid_orders.to_parquet(os.path.join(SILVER_DIR, "orders", "orders_clean.parquet"), index=False)
df_quarantine_orders.to_parquet(os.path.join(QUARANTINE_DIR, "orders", "orders_quarantined.parquet"), index=False)

print(f"✅ Deduplication removed: {initial_count - dedup_count} duplicates.")
print(f"✅ Valid Orders saved to Silver: {len(df_valid_orders)}")
print(f"🚨 Quarantined Bad Orders (Invalid Customer IDs): {len(df_quarantine_orders)}")

# -------------------------------------------------------------
# 3. CLEAN PRODUCTS
# -------------------------------------------------------------
print("\n🧹 [3/5] Processing Products...")
df_prod = pd.read_parquet(os.path.join(BRONZE_DIR, "products", "products_raw.parquet"))
df_prod["product_name"] = df_prod["product_name"].str.strip()
df_prod["profit_margin"] = round((df_prod["selling_price"] - df_prod["cost_price"]), 2)

df_prod.to_parquet(os.path.join(SILVER_DIR, "products", "products_clean.parquet"), index=False)
print(f"✅ Clean Products saved. Count: {len(df_prod)}")

# -------------------------------------------------------------
# 4. CLEAN RETURNS
# -------------------------------------------------------------
print("\n🧹 [4/5] Processing Returns...")
df_ret = pd.read_parquet(os.path.join(BRONZE_DIR, "returns", "returns_raw.parquet"))
df_ret["return_date"] = pd.to_datetime(df_ret["return_date"]).dt.strftime('%Y-%m-%d')

df_ret.to_parquet(os.path.join(SILVER_DIR, "returns", "returns_clean.parquet"), index=False)
print(f"✅ Clean Returns saved. Count: {len(df_ret)}")

# -------------------------------------------------------------
# 5. CLEAN INVENTORY
# -------------------------------------------------------------
print("\n🧹 [5/5] Processing Inventory...")
df_inv = pd.read_parquet(os.path.join(BRONZE_DIR, "inventory", "inventory_raw.parquet"))
df_inv["reorder_flag"] = np.where(df_inv["stock_quantity"] <= df_inv["reorder_level"], True, False)

df_inv.to_parquet(os.path.join(SILVER_DIR, "inventory", "inventory_clean.parquet"), index=False)
print(f"✅ Clean Inventory saved. Count: {len(df_inv)}")

print("\n🎉 SILVER LAYER PROCESSING COMPLETE! Clean datasets in 'data/lakehouse/silver/'")