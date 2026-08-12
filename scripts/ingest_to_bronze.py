import os
import pandas as pd
from sqlalchemy import create_engine

print("⚡ Starting Bronze Layer Ingestion Process...")

BRONZE_DIR = os.path.join("data", "lakehouse", "bronze")
SAMPLE_DIR = os.path.join("data", "sample")

for folder in ["customers", "orders", "products", "returns", "inventory"]:
    os.makedirs(os.path.join(BRONZE_DIR, folder), exist_ok=True)

# -------------------------------------------------------------
# 1. INGEST CUSTOMERS (SQLAlchemy for Clean Reading)
# -------------------------------------------------------------
print("\n📥 [1/5] Ingesting Customers from MySQL DB (Port 3307)...")
try:
    engine = create_engine("mysql+mysqlconnector://retailx_user:retailx_password@localhost:3307/retailx_source")
    df_customers = pd.read_sql("SELECT * FROM customers", engine)
    
    output_path = os.path.join(BRONZE_DIR, "customers", "customers_raw.parquet")
    df_customers.to_parquet(output_path, index=False)
    print(f"✅ Customers loaded into Bronze. Record count: {len(df_customers)}")
except Exception as e:
    print(f"❌ Error reading MySQL: {e}")

# -------------------------------------------------------------
# 2. INGEST ORDERS
# -------------------------------------------------------------
print("\n📥 [2/5] Ingesting Orders from CSV...")
df_orders = pd.read_csv(os.path.join(SAMPLE_DIR, "orders.csv"))
df_orders.to_parquet(os.path.join(BRONZE_DIR, "orders", "orders_raw.parquet"), index=False)
print(f"✅ Orders loaded into Bronze. Record count: {len(df_orders)}")

# -------------------------------------------------------------
# 3. INGEST PRODUCTS
# -------------------------------------------------------------
print("\n📥 [3/5] Ingesting Products from Excel...")
df_products = pd.read_excel(os.path.join(SAMPLE_DIR, "products.xlsx"))
df_products.to_parquet(os.path.join(BRONZE_DIR, "products", "products_raw.parquet"), index=False)
print(f"✅ Products loaded into Bronze. Record count: {len(df_products)}")

# -------------------------------------------------------------
# 4. INGEST RETURNS
# -------------------------------------------------------------
print("\n📥 [4/5] Ingesting Returns from CSV...")
df_returns = pd.read_csv(os.path.join(SAMPLE_DIR, "returns.csv"))
df_returns.to_parquet(os.path.join(BRONZE_DIR, "returns", "returns_raw.parquet"), index=False)
print(f"✅ Returns loaded into Bronze. Record count: {len(df_returns)}")

# -------------------------------------------------------------
# 5. INGEST INVENTORY
# -------------------------------------------------------------
print("\n📥 [5/5] Ingesting Inventory from CSV...")
df_inventory = pd.read_csv(os.path.join(SAMPLE_DIR, "inventory.csv"))
df_inventory.to_parquet(os.path.join(BRONZE_DIR, "inventory", "inventory_raw.parquet"), index=False)
print(f"✅ Inventory loaded into Bronze. Record count: {len(df_inventory)}")

print("\n🎉 BRONZE LAYER INGESTION COMPLETE!")