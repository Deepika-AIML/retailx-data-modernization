
# 🛒 RetailX: End-to-End Modern Data Engineering & Analytics Pipeline

A robust, production-grade Data Engineering pipeline and Analytics solution built using **Python, Docker, MySQL, Parquet, and Power BI**. 

This project simulates real-world retail transactions, processes data through a multi-tier **Medallion Architecture (Bronze ➔ Silver ➔ Gold)**, and delivers actionable business insights through an interactive **Power BI Executive Dashboard**.

---

## 🏗️ Architecture & Data Flow


```

+-------------------+      +-------------------+      +-------------------+
|   Bronze Layer    | ───> |   Silver Layer    | ───> |    Gold Layer     |
| (Raw Ingestion)   |      | (Cleaned & Valid) |      | (Star Schema /    |
|                   |      |                   |      |  Parquet Models)  |
+-------------------+      +-------------------+      +-------------------+
│
▼
+-------------------+
|     Power BI      |
| (DAX Measures &   |
|   Dashboards)     |
+-------------------+                                 +-------------------+

```

---

## 🛠️ Tech Stack & Skills Demonstrated

* **Programming:** Python 3.x (Pandas, PyArrow)
* **Containerization & DB:** Docker, Docker Compose, MySQL
* **Storage & Processing:** Columnar Parquet format, Medallion Architecture
* **Data Modeling:** Star Schema Design (Fact & Dimension Tables)
* **Business Intelligence:** Power BI Desktop, DAX (Data Analysis Expressions)
* **Version Control:** Git & GitHub

---

## 📊 Medallion Architecture Highlights

1. **Bronze Layer (Raw Storage):** Ingests raw sales, customer, and product data directly from MySQL / simulated feeds into storage without altering schemas.
2. **Silver Layer (Data Cleansing):** 
   * Handles missing values, duplicates, and invalid transaction records.
   * Standardizes date formats, currency values, and category taxonomy.
3. **Gold Layer (Analytics-Ready):** 
   * Models data into a **Star Schema** (`fact_sales`, `dim_customers`, `dim_products`, `dim_date`).
   * Exports optimized **Parquet files** for fast, columnar query execution in Power BI.

---

## 📈 Executive Power BI Dashboard

The Gold layer datasets are connected to Power BI to drive key business decisions through custom DAX calculations.

### Key DAX Metrics Built:
* **Total Net Revenue:** `SUM(fact_sales[net_revenue])`
* **Total Gross Profit:** `SUM(fact_sales[gross_profit])`
* **Profit Margin %:** `DIVIDE([Total Gross Profit], [Total Net Revenue], 0)`
* **Total Orders:** `COUNTROWS(fact_sales)`

### Core Visualizations:
* **Executive Summary Cards:** Instant snapshot of Revenue, Profit, Margin %, and Total Orders.
* **Top Selling Products:** Clustered Bar Chart tracking highest-revenue merchandise.
* **Payment Preference:** Donut Chart breaking down payment channels (Credit Card, UPI, Net Banking, COD).
* **Customer Lifetime Value Leaderboard:** Table visual showcasing highest-spending customers.

---

## 📁 Repository Structure


```

retailx-data-modernization/
├── data/                    # Lakehouse layers (Bronze, Silver, Gold)
├── docker/
│   └── mysql/               # Database setup and init scripts
├── scripts/                 # Python pipeline scripts
├── .gitignore               # Ignored files (virtualenvs, .pbix, cache)
├── docker-compose.yml       # Docker container setup
├── main.py                  # Main execution entry point
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation

```

---

## 🚀 How to Run This Project Locally

### 1. Clone the Repository
```bash
git clone [https://github.com/Deepika-AIML/retailx-data-modernization.git](https://github.com/Deepika-AIML/retailx-data-modernization.git)
cd retailx-data-modernization

```

### 2. Set Up Virtual Environment & Dependencies

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt

```

### 3. Spin Up Docker Database Container

```bash
docker-compose up -d

```

### 4. Run the Data Pipeline

```bash
python main.py

```

### 5. Open Power BI Dashboard

Launch Power BI Desktop and open your local `.pbix` dashboard file connected to the Gold Layer Parquet files/MySQL tables.

```

---

### 📤 To push this update to GitHub:

Open your terminal in VS Code and run:

```powershell
git add README.md
git commit -m "Added comprehensive English README documentation"
git push origin main
