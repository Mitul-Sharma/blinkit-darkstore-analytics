import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Ensure the script outputs files to the correct '../data/' folder relative to this script
os.makedirs('../data', exist_ok=True)

# Set seed for reproducibility
np.random.seed(42)

# 1. Create Products Master
products = pd.DataFrame({
    'product_id': [101, 102, 103, 104, 105],
    'product_name': ['Amul Taaza Milk 1L', 'Maggi Noodles 4-Pack', 'Bread White regular', 'Coca Cola 250ml', 'Rin Detergent Bar'],
    'category': ['Dairy & Eggs', 'Munchies', 'Bakery', 'Drinks', 'Household'],
    'price': [68, 60, 45, 20, 15]
})

# 2. Create hourly inventory snapshot for a Dark Store (Store ID: DS_01)
base_time = datetime(2026, 6, 15, 0, 0)
records = []

for hour in range(72): # 3 days of hourly simulation data
    current_time = base_time + timedelta(hours=hour)
    for p_id in products['product_id']:
        # Simulate inventory dropping and getting replenished
        if hour in [0, 24, 48]: # Scheduled replenishment times
            stock = np.random.randint(40, 60)
        else:
            # Drop stock randomly based on typical hourly grocery demand
            prev_stock = [r[2] for r in records if r[1] == p_id][-1] if records else 50
            demand = np.random.randint(0, 8)
            stock = max(0, prev_stock - demand)
            
        records.append([current_time.strftime('%Y-%m-%d %H:%M:%S'), p_id, stock])

inventory = pd.DataFrame(records, columns=['timestamp', 'product_id', 'current_stock'])

# Export data directly to the data folder
products.to_csv('../data/products.csv', index=False)
inventory.to_csv('../data/inventory_snapshots.csv', index=False)

print("✅ Success! 'products.csv' and 'inventory_snapshots.csv' created inside the /data folder.")