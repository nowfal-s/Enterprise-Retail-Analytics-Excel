from openpyxl import Workbook
import pandas as pd
import numpy as np
import os, zipfile

np.random.seed(42)

folder="/mnt/data/Enterprise_Retail_Data"
os.makedirs(folder, exist_ok=True)

dates = pd.date_range(start='2019-01-01', end='2023-12-31')

dim_date = pd.DataFrame({
    'Date': dates,
    'Year': dates.year,
    'Month': dates.month,
    'Quarter': dates.quarter
})
dim_date.to_csv(f'{folder}/Dim_Date.csv', index=False)

dim_product = pd.DataFrame({
    'Product_ID': range(1, 2001),
    'Category': np.random.choice(['Electronics', 'Apparel', 'Home', 'Grocery', 'Toys'], 2000),
    'Brand': np.random.choice(['Brand_A', 'Brand_B', 'Brand_C', 'Brand_D'], 2000),
    'Cost': np.round(np.random.uniform(5, 500), 2)
})
dim_product['Price'] = np.round(dim_product['Cost'] * np.random.uniform(1.2, 2.5, 2000), 2)
dim_product.to_csv(f'{folder}/Dim_Product.csv', index=False)

dim_customer = pd.DataFrame({
    'Customer_ID': range(1, 5001),
    'Segment': np.random.choice(['VIP', 'Regular', 'Occasional', 'New'], 5000),
    'Region': np.random.choice(['North', 'South', 'East', 'West'], 5000)
})
dim_customer.to_csv(f'{folder}/Dim_Customer.csv', index=False)

dim_store = pd.DataFrame({
    'Store_ID': range(1, 101),
    'Store_Type': np.random.choice(['Flagship', 'Standard', 'Express'], 100),
    'City': np.random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'], 100)
})
dim_store.to_csv(f'{folder}/Dim_Store.csv', index=False)

n_sales=100000
fact_sales = pd.DataFrame({
    'Order_ID': range(1,n_sales+1),
    'Date': np.random.choice(dates, n_sales),
    'Product_ID': np.random.choice(dim_product['Product_ID'], n_sales),
    'Customer_ID': np.random.choice(dim_customer['Customer_ID'], n_sales),
    'Store_ID': np.random.choice(dim_store['Store_ID'], n_sales),
    'Quantity': np.random.randint(1,10,n_sales),
    'Discount_Pct': np.random.choice([0,0.05,0.10,0.20], n_sales, p=[0.7,0.15,0.1,0.05])
})
fact_sales.to_csv(f'{folder}/Fact_Sales.csv', index=False)

fact_returns = fact_sales.sample(n=10000, random_state=42)[['Order_ID','Date','Product_ID','Customer_ID','Store_ID']].copy()
fact_returns['Return_Date']=pd.to_datetime(fact_returns['Date'])+pd.to_timedelta(np.random.randint(1,30,10000),unit='D')
fact_returns['Return_Quantity']=1
fact_returns['Return_Reason']=np.random.choice(['Defective','Changed Mind','Wrong Item'],10000)
fact_returns.to_csv(f'{folder}/Fact_Returns.csv', index=False)

zip_path="/mnt/data/Enterprise_Retail_Data.zip"
with zipfile.ZipFile(zip_path,"w",zipfile.ZIP_DEFLATED) as z:
    for f in os.listdir(folder):
        z.write(os.path.join(folder,f), arcname=f)

print(zip_path)

