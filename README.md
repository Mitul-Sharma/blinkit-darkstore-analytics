# 🛒 Blinkit Dark Store Control Tower Analytics 📊

## Project Overview
This project focuses on optimizing real-time inventory fulfillment and supply chain telemetry for high-velocity quick-commerce dark store operations (e.g., Blinkit, Zepto, Instamart). By evaluating localized lead-time risks and modeling dynamic stockout intervals, the system isolates financial leakages and automates reorder workflows to preserve a strict 10-to-20 minute delivery SLA.

The backend engine processes operational telemetry to generate algorithmic Reorder Points (ROP) and safety stock buffers, surfacing them through an executive-level business intelligence dashboard.

---

## Data Engineering & Supply Chain Challenges (The "Hard" Part)
Quick-commerce inventory dynamics move too fast for traditional daily or weekly batch replenishment. I isolated and modeled several critical localized operational constraints:

* **Fulfillment Lead-Time Window ($LT$):** Modeled around a tight 3-hour turnaround truck delivery constraint from regional distribution fulfillment centers.
* **Dynamic Reorder Trigger Layer:** Implemented algorithmic boundaries mapping live physical counts against safety thresholds to eliminate manual auditing lag and stockout gaps.
* **Quantifying Revenue Leakage:** Isolated exactly how much potential revenue is permanently lost during down-time windows by executing demand turnover multipliers based on a 4x daily velocity matrix.

---

## 🛠️ Tech Stack & Data Engine
* **Backend Core:** Python, Pandas, NumPy
* **Operational Interface:** Streamlit Framework
* **Visual Layer:** Interactive Plotly Dark Engine
* **Database & Logic:** Advanced Supply Chain SQL Window Functions

---

## 📋 Key Analytics & SQL Snippets
One of the most critical analytics phases involved using advanced SQL window functions to partition inventory snapshots, isolate exact historical stockout intervals, and calculate preceding run-rates:

```sql
-- Partitioning snapshots to calculate inventory depletion intervals and track stockout windows
SELECT 
    product_id,
    timestamp,
    current_stock,
    LAG(current_stock, 1) OVER (PARTITION BY product_id ORDER BY timestamp) AS previous_stock_level,
    CASE 
        WHEN current_stock = 0 AND LAG(current_stock, 1) OVER (PARTITION BY product_id ORDER BY timestamp) > 0 
        THEN '🚨 Stockout Triggered'
        ELSE 'Healthy'
    END AS operational_status
FROM inventory_snapshots
ORDER BY product_id, timestamp;
