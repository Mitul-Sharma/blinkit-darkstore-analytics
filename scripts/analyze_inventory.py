import pandas as pd
import sqlite3

# 1. Load the CSV data we generated in Step 3
products_df = pd.read_csv('../data/products.csv')
inventory_df = pd.read_csv('../data/inventory_snapshots.csv')

# 2. Connect to a temporary in-memory SQLite Database
conn = sqlite3.connect(':memory:')

# 3. Write dataframes to SQL tables
products_df.to_sql('products', conn, index=False, if_exists='replace')
inventory_df.to_sql('inventory_snapshots', conn, index=False, if_exists='replace')

print("✅ Data successfully loaded into temporary SQL database engine.\n")
print("================================================================")
print("🎯 INSIGHT 1: TOTAL HOURS OUT-OF-STOCK & ESTIMATED LOST REVENUE")
print("================================================================")

# Query 1: Calculate total hours spent at 0 stock and estimate lost revenue
# (Assuming an average quick-commerce demand of 4 units lost per hour of stockout)
query_lost_revenue = """
SELECT 
    i.product_id,
    p.product_name,
    p.category,
    COUNT(CASE WHEN i.current_stock = 0 THEN 1 END) as hours_out_of_stock,
    -- Formula: hours_oos * estimated 4 missing orders/hr * product price
    COUNT(CASE WHEN i.current_stock = 0 THEN 1 END) * 4 * p.price as estimated_lost_revenue
FROM inventory_snapshots i
JOIN products p ON i.product_id = p.product_id
GROUP BY i.product_id, p.product_name, p.price
ORDER BY estimated_lost_revenue DESC;
"""

lost_rev_results = pd.read_sql_query(query_lost_revenue, conn)
print(lost_rev_results.to_string(index=False))


print("\n================================================================")
print("🎯 INSIGHT 2: TRACKING STOCK DEFORMATION TIMELINES (WINDOW FUNCTION)")
print("================================================================")

# Query 2: Using LAG() to pinpoint the exact moment stock dropped to zero
query_oos_moments = """
WITH stock_trends AS (
    SELECT 
        timestamp,
        product_id,
        current_stock,
        LAG(current_stock, 1) OVER (PARTITION BY product_id ORDER BY timestamp) as previous_hour_stock
    FROM inventory_snapshots
)
SELECT 
    s.timestamp as stockout_timestamp,
    s.product_id,
    p.product_name,
    s.previous_hour_stock as stock_just_before_drop,
    s.current_stock
FROM stock_trends s
JOIN products p ON s.product_id = p.product_id
WHERE s.current_stock = 0 AND (s.previous_hour_stock > 0 OR s.previous_hour_stock IS NULL)
LIMIT 5;
"""

oos_moments_results = pd.read_sql_query(query_oos_moments, conn)
print(oos_moments_results.to_string(index=False))

# Close database connection
conn.close()