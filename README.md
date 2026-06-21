# 🛒 Quick-Commerce Dark Store Control Tower Analytics

An end-to-end data analytics and supply chain optimization framework designed for high-velocity dark store operations (e.g., Blinkit, Zepto, Instamart). This system processes real-time inventory telemetry, evaluates lead-time risks, and quantifies financial leakage due to out-of-stock (OOS) conditions.

## 🚀 Live Production Dashboard
*Built with Python, Plotly, and Streamlit*
* **Dynamic KPI Summary Tiles:** Live monitoring of Revenue Leakage, Critical Stockouts, and Service Level targets.
* **Financial Leakage Engine:** Quantifies the immediate monetary impact of stockouts to prioritize procurement batches.
* **Dynamic Reorder Trigger Layer:** Real-time stock counts mapped dynamically against safety thresholds and Reorder Points (ROP).

---

## 📐 Supply Chain & Product Logic

To protect Blinkit's **10-minute delivery promise**, dark store inventory cannot rely on standard daily/weekly replenishment cycles. This project implements localized operations constraints:

1. **Fulfillment Lead Time ($LT$):** Modeled around a tight 3-hour turnaround window for micro-warehouse delivery truck replenishment batches.
2. **Reorder Point ($ROP$) Formula:** $$ROP = (\text{Average Daily Demand} \times Lead\ Time) + Safety\ Stock$$
3. **Financial Leakage Multiplier:** OOS impact is quantified by scaling the cost of safety stock buffer across a high-frequency **4x daily inventory turnover** multiplier.

---

## 📁 Repository Structure
* `/scripts/real_dashboards.py`: Production Streamlit application code.
* `/scripts/build_plotly_dashboards.py`: Lightweight standalone HTML component generator.
* `/data/`: Raw and engineered inventory snapshots and targets.

## 🛠️ Installation & Setup
1. Clone this repository.
2. Install the required dependencies:
   ```bash
   pip install streamlit plotly pandas
