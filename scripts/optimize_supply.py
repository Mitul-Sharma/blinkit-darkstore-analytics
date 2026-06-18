import pandas as pd
import numpy as np

# 1. Load data
inventory = pd.read_csv('../data/inventory_snapshots.csv')
products = pd.read_csv('../data/products.csv')

# 2. Operational Assumption: 
# It takes exactly 3 hours for a replenishment truck to arrive at the Dark Store 
# once an order is placed to the central hub.
lead_time_hours = 3 

# 3. Calculate hourly sales velocity by looking at stock drops
inventory['prev_stock'] = inventory.groupby('product_id')['current_stock'].shift(1)
inventory['units_sold'] = (inventory['prev_stock'] - inventory['current_stock']).clip(lower=0)

# Drop rows where replenishment happened (stock jumped up instead of down)
inventory.loc[inventory['current_stock'] > inventory['prev_stock'], 'units_sold'] = 0

# 4. Aggregate metrics per product
metrics = inventory.groupby('product_id').agg(
    avg_hourly_sales=('units_sold', 'mean'),
    max_hourly_sales=('units_sold', 'max')
).reset_index()

# 5. Apply the Classic Supply Chain Formulas
# Safety Stock = (Max Hourly Sales * Lead Time) - (Avg Hourly Sales * Lead Time)
metrics['safety_stock'] = (metrics['max_hourly_sales'] * lead_time_hours) - (metrics['avg_hourly_sales'] * lead_time_hours)

# Reorder Point (ROP) = (Avg Hourly Sales * Lead Time) + Safety Stock
metrics['reorder_point'] = (metrics['avg_hourly_sales'] * lead_time_hours) + metrics['safety_stock']

# Round values up to whole units
metrics['safety_stock'] = np.ceil(metrics['safety_stock']).astype(int)
metrics['reorder_point'] = np.ceil(metrics['reorder_point']).astype(int)

# 6. Merge with product master for clean names
final_optimization = pd.merge(products, metrics, on='product_id')

print("================================================================")
print("🎯 STEP 6: CALCULATED SAFETY STOCK & REORDER POINTS (ROP)")
print("================================================================")
print(final_optimization[['product_name', 'avg_hourly_sales', 'safety_stock', 'reorder_point']].to_string(index=False))

# Save this optimization master sheet back to the data folder for your dashboard
final_optimization.to_csv('../data/inventory_targets.csv', index=False)
print("\n✅ Optimization metrics exported successfully to '/data/inventory_targets.csv'")