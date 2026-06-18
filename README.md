# Quick-Commerce Dark Store Inventory Optimization

A data analytics project focused on minimizing **Out-of-Stock (OOS)** revenue leakage and calculating optimal **Safety Stock** thresholds for a quick-commerce (Blinkit-style) micro-warehouse.

## 📌 Business Context & Problem Statement
In quick commerce, dark stores operate with extremely limited shelf space in high-density urban areas. 
* Running **out of stock** on high-velocity essential items (like milk or bread) leads to immediate cart abandonment and revenue loss.
* Overstocking leads to high inventory holding costs and perishable wastage.

This project builds an automated analytics pipeline to quantify the financial damage of stockouts and determine exact **Reorder Points (ROP)** using a 3-hour fulfillment lead time framework.

---

## 📂 Project Structure
```text
blinkit-darkstore-analytics/
├── data/
│   ├── products.csv              # Product Master data
│   ├── inventory_snapshots.csv   # Mocked hourly dark store inventory logs
│   └── inventory_targets.csv     # Engineered supply chain optimization metrics
└── scripts/
    ├── generate_data.py          # Python script simulating store transaction telemetry
    ├── analyze_inventory.py       # SQL engine isolating OOS windows & lost revenue
    └── optimize_supply.py        # Python script calculating Safety Stock & ROP
