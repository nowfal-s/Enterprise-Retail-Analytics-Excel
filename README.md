# Enterprise Retail Analytics – Excel / Power Pivot BI Project

## 📌 Project Overview

This is an end-to-end Business Intelligence and Data Warehousing project built entirely within Microsoft Excel, leveraging the xVelocity/VertiPaq engine. The project simulates a large-scale enterprise retail environment, transforming over 100,000 rows of raw synthetic transaction data into a fully relational analytical model.

The goal of this project is to demonstrate advanced data modeling, ETL, and analytical capabilities using Power Query and DAX—skills that transfer directly to Power BI and enterprise data engineering workflows.

### Technologies Used
* **Microsoft Excel:** Dashboarding, PivotTables, and PivotCharts
* **Power Query (M):** ETL, data staging, and transformation
* **Power Pivot:** Dimensional modeling and Star Schema architecture
* **DAX:** Explicit measure authoring and time-intelligence calculations
* **Python (Pandas/NumPy):** Synthetic data generation
* **Git/GitHub:** Version control and portfolio documentation

---

## 🗄️ Data Generation & Architecture

### Synthetic Data Pipeline
The foundational dataset was synthetically generated using Python to simulate a realistic retail environment covering 2019–2023. 

*Note: The generated data was deliberately imperfect. A critical component of this project involved identifying data anomalies and modeling gaps during the development lifecycle and remediating them via Power Query.* 

*(Large raw CSV files are excluded from this repository; the provided Python script allows for complete recreation of the source data).*

### Dimensional Data Model
The architecture follows strict one-to-many dimensional modeling principles. Wide dimensions were utilized where appropriate (e.g., nesting Category/Brand within Product, or Region/City within Customer) to optimize VertiPaq engine performance over heavy snowflaking.

**Fact Tables:** 
`Fact_Sales`, `Fact_Returns`, `Fact_Inventory`, `Fact_Purchase`, `Fact_Shipments`, `Fact_Payments`, `Fact_EmployeeSales`, `Fact_Website`, `Fact_Marketing`, `Fact_CustomerSupport`, `Fact_Budget`

**Dimension Tables:** 
`Dim_Date`, `Dim_Product`, `Dim_Customer`, `Dim_Store`, `Dim_Employee`, `Dim_Supplier`, `Dim_Warehouse`, `Dim_Promotion`, `Dim_Campaign`, `Dim_PaymentMethod`, `Dim_ShippingMethod`, `Dim_Department`

**Advanced Modeling Techniques Implemented:**
* **Role-Playing Dimensions:** Configured active/inactive relationships (e.g., `Dim_Date` filtering `Fact_Returns` by Sale Date vs. Return Date).
* **Many-to-Many Resolution:** Built a bridge table connecting Products and Promotions.
* **Disconnected Tables:** Created a parameter table to drive dynamic KPI selection on the dashboards.

![Data Model](screenshots/data_model_relationships.png)

---

## ⚙️ ETL & Data Preparation (Power Query)

Power Query was utilized to extract, clean, and stage the data before loading it into the Data Model. Key transformations include:

* **Staging Architecture:** Loading raw files as "Connection Only" to keep the workbook lightweight.
* **Merge Operations:** Functioning similarly to SQL `LEFT JOIN`, enriching transaction tables with dimensional attributes to preserve historical accuracy (e.g., hardcoding unit costs at the time of sale).
* **Unpivoting:** Transforming wide, matrix-style departmental budgets (`Department | Jan | Feb | Mar`) into a normalized, analytical format (`Department | Month | Budget Amount`).
* **Append Operations:** Simulating a SQL `UNION` to stack segmented data files, accompanied by deduplication steps to ensure accurate aggregations.
* **Dynamic Parameters:** Implementing a `FolderPath` parameter to ensure queries remain dynamic and maintainable without hardcoded file paths.

---

## 📊 Analytical Layer (DAX)

To ensure accurate and reusable calculations across all reports, implicit PivotTable aggregations were disabled in favor of explicit DAX measures. Over 25 measures were authored across various business subject areas.

**Key Analytical Concepts Implemented:**
* **Iterators (`SUMX`):** Row-by-row calculations for profit margins and inventory valuation.
* **Context Modification (`CALCULATE`):** Overriding default filter contexts for precise variance reporting.
* **Time Intelligence:** YoY, YTD, and Same Period Last Year calculations.
* **Ranking & Percentages:** `RANKX` for product performance and `ALLSELECTED` for percentage-of-total calculations.

### Representative DAX Examples

**1. Activating Inactive Relationships (Role-Playing Dimensions):**
```dax
Returns (by Return Date) := 
CALCULATE(
    [Total Returns], 
    USERELATIONSHIP(Fact_Returns[Return_Date], Dim_Date[Date])
)
