import os
import random
from datetime import datetime, timedelta
import pandas as pd

# Create target directory if it doesn't exist
OUTPUT_DIR = os.path.join("data", "sample")
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("🚀 Generating synthetic enterprise datasets for RetailX...")

# 1. PRODUCTS DATA (Excel format)
products_data = [
    {"product_id": 1001, "product_name": "Pro Wireless Headphones", "category": "Electronics", "subcategory": "Audio", "brand": "SoundPro", "cost_price": 45.0, "selling_price": 89.99, "supplier_id": "SUP_01"},
    {"product_id": 1002, "product_name": "Ergonomic Office Chair", "category": "Furniture", "subcategory": "Chairs", "brand": "FlexiSit", "cost_price": 110.0, "selling_price": 199.50, "supplier_id": "SUP_02"},
    {"product_id": 1003, "product_name": "Mechanical Gaming Keyboard", "category": "Electronics", "subcategory": "Accessories", "brand": "KeyMaster", "cost_price": 30.0, "selling_price": 69.99, "supplier_id": "SUP_01"},
    {"product_id": 1004, "product_name": "Stainless Steel Water Bottle", "category": "Home & Kitchen", "subcategory": "Drinkware", "brand": "HydroPeak", "cost_price": 5.0, "selling_price": 18.00, "supplier_id": "SUP_03"},
    {"product_id": 1005, "product_name": "4K Ultra HD Monitor 27-inch", "category": "Electronics", "subcategory": "Monitors", "brand": "VisionX", "cost_price": 180.0, "selling_price": 329.99, "supplier_id": "SUP_01"},
    {"product_id": 1006, "product_name": "Organic Cotton T-Shirt", "category": "Apparel", "subcategory": "Men Wear", "brand": "EcoStyle", "cost_price": 7.5, "selling_price": 24.99, "supplier_id": "SUP_04"},
]

df_products = pd.DataFrame(products_data)
df_products.to_excel(os.path.join(OUTPUT_DIR, "products.xlsx"), index=False)
print("✅ Saved: products.xlsx")

# 2. ORDERS DATA (CSV format with intentional dirty data)
random.seed(42)
customer_ids = [101, 102, 103, 104, 105, 9999]  # 9999 is an invalid orphan customer_id for quarantine testing!
product_ids = [1001, 1002, 1003, 1004, 1005, 1006]
payment_methods = ["Credit Card", "UPI", "Debit Card", "Net Banking", "COD", "credit_card", "upi"] # Inconsistent formatting

orders_data = []
start_date = datetime(2025, 1, 1)

for i in range(1, 151): # 150 Sample Orders
    order_id = 5000 + i
    c_id = random.choice(customer_ids)
    p_id = random.choice(product_ids)
    
    # Random date within last 1.5 years
    o_date = start_date + timedelta(days=random.randint(0, 500))
    
    # Intentional date string variations for silver layer cleaning testing
    date_str = o_date.strftime("%Y-%m-%d") if i % 4 != 0 else o_date.strftime("%d/%m/%Y")
    
    qty = random.randint(1, 5)
    discount = round(random.uniform(0.0, 0.20), 2)
    p_method = random.choice(payment_methods)
    status = random.choice(["Delivered", "Delivered", "Delivered", "Cancelled", "Processing", "DELIVERED"])

    orders_data.append({
        "order_id": order_id,
        "customer_id": c_id,
        "product_id": p_id,
        "order_date": date_str,
        "quantity": qty,
        "discount": discount,
        "payment_method": p_method,
        "order_status": status
    })

# Add an intentional exact duplicate order record
orders_data.append(orders_data[0])

df_orders = pd.DataFrame(orders_data)
df_orders.to_csv(os.path.join(OUTPUT_DIR, "orders.csv"), index=False)
print("✅ Saved: orders.csv")

# 3. RETURNS DATA (CSV format)
returns_data = [
    {"return_id": 801, "order_id": 5005, "return_date": "2025-02-10", "return_reason": "Defective product", "refund_amount": 89.99},
    {"return_id": 802, "order_id": 5012, "return_date": "2025-02-18", "return_reason": "Wrong item delivered", "refund_amount": 24.99},
    {"return_id": 803, "order_id": 5025, "return_date": "2025-03-01", "return_reason": "Changed mind", "refund_amount": 199.50},
    {"return_id": 804, "order_id": 5040, "return_date": "2025-03-15", "return_reason": "Damaged in transit", "refund_amount": 69.99},
]
df_returns = pd.DataFrame(returns_data)
df_returns.to_csv(os.path.join(OUTPUT_DIR, "returns.csv"), index=False)
print("✅ Saved: returns.csv")

# 4. INVENTORY DATA (CSV format)
inventory_data = [
    {"product_id": 1001, "warehouse_id": "WH_NORTH", "stock_quantity": 150, "reorder_level": 30, "last_updated": "2026-08-01"},
    {"product_id": 1002, "warehouse_id": "WH_WEST", "stock_quantity": 45, "reorder_level": 10, "last_updated": "2026-08-01"},
    {"product_id": 1003, "warehouse_id": "WH_NORTH", "stock_quantity": 200, "reorder_level": 50, "last_updated": "2026-08-01"},
    {"product_id": 1004, "warehouse_id": "WH_SOUTH", "stock_quantity": 500, "reorder_level": 100, "last_updated": "2026-08-01"},
    {"product_id": 1005, "warehouse_id": "WH_EAST", "stock_quantity": 20, "reorder_level": 15, "last_updated": "2026-08-01"},
    {"product_id": 1006, "warehouse_id": "WH_SOUTH", "stock_quantity": 350, "reorder_level": 80, "last_updated": "2026-08-01"},
]
df_inventory = pd.DataFrame(inventory_data)
df_inventory.to_csv(os.path.join(OUTPUT_DIR, "inventory.csv"), index=False)
print("✅ Saved: inventory.csv")

print("\n🎉 All raw source datasets successfully created in 'data/sample/'!")