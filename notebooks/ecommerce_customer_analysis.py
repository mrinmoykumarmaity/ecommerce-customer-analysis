import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data"
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)

customers = pd.read_csv(DATA / "customers.csv", parse_dates=["signup_date"])
orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
items = pd.read_csv(DATA / "order_items.csv")
products = pd.read_csv(DATA / "products.csv")

completed_orders = orders[orders["order_status"] == "Completed"].copy()
sales = completed_orders.merge(items, on="order_id").merge(products[["product_id", "category"]], on="product_id").merge(customers, on="customer_id")

# 1. Customer Lifetime Value
clv = sales.groupby("customer_id").agg(
    total_revenue=("revenue", "sum"),
    total_orders=("order_id", "nunique"),
    total_items=("quantity", "sum"),
    first_order=("order_date", "min"),
    last_order=("order_date", "max")
).reset_index()
clv["avg_order_value"] = clv["total_revenue"] / clv["total_orders"]
clv = clv.merge(customers, on="customer_id", how="left")
clv.to_csv(OUT / "customer_lifetime_value.csv", index=False)

# 2. Repeat Customers
repeat_summary = clv.assign(customer_type=clv["total_orders"].apply(lambda x: "Repeat Customer" if x > 1 else "One-time Customer"))
repeat_summary.groupby("customer_type").agg(
    customers=("customer_id", "count"),
    revenue=("total_revenue", "sum"),
    avg_revenue_per_customer=("total_revenue", "mean")
).reset_index().to_csv(OUT / "repeat_customer_summary.csv", index=False)

# 3. Revenue by Category
category_revenue = sales.groupby("category").agg(
    revenue=("revenue", "sum"),
    orders=("order_id", "nunique"),
    quantity_sold=("quantity", "sum")
).reset_index().sort_values("revenue", ascending=False)
category_revenue.to_csv(OUT / "revenue_by_category.csv", index=False)

# 4. Customer Segmentation using RFM
snapshot_date = sales["order_date"].max() + pd.Timedelta(days=1)
rfm = sales.groupby("customer_id").agg(
    recency=("order_date", lambda x: (snapshot_date - x.max()).days),
    frequency=("order_id", "nunique"),
    monetary=("revenue", "sum")
).reset_index()
rfm["r_score"] = pd.qcut(rfm["recency"], 4, labels=[4,3,2,1], duplicates="drop").astype(int)
rfm["f_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 4, labels=[1,2,3,4], duplicates="drop").astype(int)
rfm["m_score"] = pd.qcut(rfm["monetary"], 4, labels=[1,2,3,4], duplicates="drop").astype(int)
rfm["rfm_score"] = rfm["r_score"] + rfm["f_score"] + rfm["m_score"]

def segment(row):
    if row["rfm_score"] >= 10:
        return "High Value"
    if row["r_score"] <= 2 and row["f_score"] >= 3:
        return "At Risk"
    if row["frequency"] == 1:
        return "New / One-time"
    if row["rfm_score"] >= 7:
        return "Loyal"
    return "Needs Attention"

rfm["segment"] = rfm.apply(segment, axis=1)
rfm.to_csv(OUT / "customer_segments.csv", index=False)

# Charts
category_revenue.plot(kind="bar", x="category", y="revenue", legend=False)
plt.title("Revenue by Product Category")
plt.xlabel("Category")
plt.ylabel("Revenue")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(OUT / "revenue_by_category.png")
plt.close()

rfm["segment"].value_counts().plot(kind="bar")
plt.title("Customer Segments")
plt.xlabel("Segment")
plt.ylabel("Number of Customers")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(OUT / "customer_segments.png")
plt.close()

print("Analysis complete. Check the outputs folder.")
