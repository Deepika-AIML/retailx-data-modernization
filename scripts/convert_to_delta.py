import os
import pandas as pd
from deltalake import write_deltalake

print("⚡ Starting Delta Lake Conversion for Microsoft Fabric Readiness...")

GOLD_DIR = os.path.join("data", "lakehouse", "gold")
FABRIC_DELTA_DIR = os.path.join("data", "lakehouse", "fabric_delta")

# Delta Tables to create
tables = ["dim_customers", "dim_products", "dim_date", "fact_sales", "agg_daily_sales"]

for table_name in tables:
    parquet_path = os.path.join(GOLD_DIR, f"{table_name}.parquet")
    delta_path = os.path.join(FABRIC_DELTA_DIR, table_name)
    
    if os.path.exists(parquet_path):
        # Load Gold Parquet File
        df = pd.read_parquet(parquet_path)
        
        # Write as Delta Lake Format (Fabric Native)
        write_deltalake(delta_path, df, mode="overwrite")
        print(f"✅ Converted '{table_name}' to Fabric-ready Delta Table ({len(df)} rows)")

print("\n🎉 ALL GOLD TABLES CONVERTED TO DELTA LAKE FORMAT!")
print(f"📁 Delta Lake Directory: {os.path.abspath(FABRIC_DELTA_DIR)}")