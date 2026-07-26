from pathlib import Path
import pandas as pd
import numpy as np
import zipfile

np.random.seed(42)
folder=Path("/mnt/data/Enterprise_Retail_Data")
folder.mkdir(exist_ok=True)

dates=pd.date_range("2019-01-01","2023-12-31")

# Dimensions
dim_employee=pd.DataFrame({
    "Employee_ID":range(1,401),
    "Role":np.random.choice(['Sales Associate','Manager','Support','Warehouse'],400),
    "Store_ID":np.random.choice(range(1,101),400)
})
dim_employee.to_csv(folder/"Dim_Employee.csv",index=False)

pd.DataFrame({
    "Supplier_ID":range(1,51),
    "Supplier_Name":[f"Supplier_{i}" for i in range(1,51)]
}).to_csv(folder/"Dim_Supplier.csv",index=False)

pd.DataFrame({
    "Warehouse_ID":range(1,11),
    "Location":np.random.choice(['North','South','East','West'],10)
}).to_csv(folder/"Dim_Warehouse.csv",index=False)

pd.DataFrame({
    "Promotion_ID":range(1,21),
    "Promo_Type":np.random.choice(['BOGO','Clearance','Seasonal','Flash Sale'],20)
}).to_csv(folder/"Dim_Promotion.csv",index=False)

pd.DataFrame({
    "Campaign_ID":range(1,31),
    "Channel":np.random.choice(['Social','Email','Search','Display'],30)
}).to_csv(folder/"Dim_Campaign.csv",index=False)

pd.DataFrame({"PaymentMethod_ID":[1,2,3],"Method":["Card","UPI","Cash"]}).to_csv(folder/"Dim_PaymentMethod.csv",index=False)
pd.DataFrame({"ShippingMethod_ID":[1,2,3],"Method":["Standard","Expedited","Overnight"]}).to_csv(folder/"Dim_ShippingMethod.csv",index=False)
pd.DataFrame({"Department_ID":[1,2,3,4],"Dept_Name":["Electronics","Apparel","Home","Grocery"]}).to_csv(folder/"Dim_Department.csv",index=False)

# Facts
pd.DataFrame({
    "Date":np.random.choice(dates,40000),
    "Product_ID":np.random.choice(range(1,2001),40000),
    "Warehouse_ID":np.random.choice(range(1,11),40000),
    "Stock_On_Hand":np.random.randint(0,500,40000),
    "Safety_Stock":np.random.randint(20,100,40000)
}).to_csv(folder/"Fact_Inventory.csv",index=False)

pd.DataFrame({
    "Date":np.random.choice(dates,20000),
    "Product_ID":np.random.choice(range(1,2001),20000),
    "Supplier_ID":np.random.choice(range(1,51),20000),
    "Warehouse_ID":np.random.choice(range(1,11),20000),
    "Purchase_Qty":np.random.randint(50,1000,20000),
    "Unit_Cost":np.round(np.random.uniform(5,400,20000),2)
}).to_csv(folder/"Fact_Purchase.csv",index=False)

pd.DataFrame({
    "Order_ID":np.random.choice(range(1,100001),30000,replace=False),
    "Date":np.random.choice(dates,30000),
    "ShippingMethod_ID":np.random.choice([1,2,3],30000),
    "Warehouse_ID":np.random.choice(range(1,11),30000),
    "Delivery_Days":np.random.randint(1,14,30000),
    "Shipping_Cost":np.round(np.random.uniform(2,50,30000),2),
    "Late_Flag":np.random.choice([0,1],30000,p=[0.85,0.15])
}).to_csv(folder/"Fact_Shipments.csv",index=False)

pd.DataFrame({
    "Order_ID":range(1,100001),
    "Date":np.random.choice(dates,100000),
    "PaymentMethod_ID":np.random.choice([1,2,3],100000,p=[0.6,0.3,0.1]),
    "Amount":np.round(np.random.uniform(10,1000,100000),2),
    "Failed_Flag":np.random.choice([0,1],100000,p=[0.98,0.02])
}).to_csv(folder/"Fact_Payments.csv",index=False)

pd.DataFrame({
    "Date":np.random.choice(dates,10000),
    "Employee_ID":np.random.choice(range(1,401),10000),
    "Store_ID":np.random.choice(range(1,101),10000),
    "Sales_Amount":np.round(np.random.uniform(500,5000,10000),2),
    "Target_Amount":np.round(np.random.uniform(1000,6000,10000),2)
}).to_csv(folder/"Fact_EmployeeSales.csv",index=False)

pd.DataFrame({
    "Date":np.random.choice(dates,20000),
    "Campaign_ID":np.random.choice(range(1,31),20000),
    "Sessions":np.random.randint(100,5000,20000),
    "Page_Views":np.random.randint(200,15000,20000),
    "Bounces":np.random.randint(10,500,20000)
}).to_csv(folder/"Fact_Website.csv",index=False)

pd.DataFrame({
    "Date":np.random.choice(dates,5000),
    "Campaign_ID":np.random.choice(range(1,31),5000),
    "Spend":np.round(np.random.uniform(100,2000,5000),2),
    "Impressions":np.random.randint(1000,50000,5000),
    "Clicks":np.random.randint(50,2000,5000),
    "Leads":np.random.randint(0,100,5000)
}).to_csv(folder/"Fact_Marketing.csv",index=False)

pd.DataFrame({
    "Ticket_ID":range(1,8001),
    "Date":np.random.choice(dates,8000),
    "Customer_ID":np.random.choice(range(1,5001),8000),
    "Department_ID":np.random.choice([1,2,3,4],8000),
    "Resolution_Time_Hrs":np.round(np.random.uniform(0.5,72,8000),1),
    "Satisfaction_Score":np.random.randint(1,6,8000)
}).to_csv(folder/"Fact_CustomerSupport.csv",index=False)

zip_path="/mnt/data/Enterprise_Retail_Data_Part2.zip"
with zipfile.ZipFile(zip_path,"w",zipfile.ZIP_DEFLATED) as z:
    for f in folder.iterdir():
        if f.is_file():
            z.write(f,f.name)
print(zip_path)