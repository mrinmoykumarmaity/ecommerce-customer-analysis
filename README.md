# E-commerce Customer Analysis Project

## Project Objective
This project analyzes an e-commerce business dataset to understand customer behavior, revenue performance, and customer segments. It is suitable for a Data Analyst portfolio and demonstrates Python, SQL, data cleaning, KPI analysis, and business insight generation.

## Business Questions
1. Which customers generate the highest lifetime value?
2. How many customers are repeat buyers?
3. Which product categories generate the most revenue?
4. How can customers be segmented using buying behavior?

## Tools Used
- Python
- Pandas
- Matplotlib
- SQL
- CSV dataset

## Dataset Files
The `data/` folder contains:
- `customers.csv`
- `products.csv`
- `orders.csv`
- `order_items.csv`

## Key Analysis
### 1. Customer Lifetime Value
Calculated total revenue, number of orders, total items purchased, and average order value for each customer.

### 2. Repeat Customer Analysis
Customers were classified as:
- Repeat Customers: More than 1 completed order
- One-time Customers: Only 1 completed order

### 3. Revenue by Category
Revenue was grouped by product category to identify top-performing categories.

### 4. Customer Segmentation
RFM analysis was used:
- Recency: How recently the customer purchased
- Frequency: How often the customer purchased
- Monetary: How much the customer spent

Customer segments include:
- High Value
- Loyal
- At Risk
- New / One-time
- Needs Attention

## How to Run
1. Install Python libraries:
```bash
pip install pandas matplotlib
```

2. Run the analysis script:
```bash
python notebooks/ecommerce_customer_analysis.py
```

3. Check the `outputs/` folder for result CSV files and charts.

## Output Files
- `customer_lifetime_value.csv`
- `repeat_customer_summary.csv`
- `revenue_by_category.csv`
- `customer_segments.csv`
- `revenue_by_category.png`
- `customer_segments.png`

## Resume Description
E-commerce Customer Analysis Project: Analyzed customer purchase behavior using Python and SQL. Calculated customer lifetime value, repeat customer rate, revenue by category, and built RFM-based customer segmentation to identify high-value, loyal, at-risk, and one-time customers.

## Interview Explanation
This project shows how an analyst can use transactional data to help an e-commerce business understand customer value and improve marketing decisions. The analysis identifies top customers, best-selling categories, repeat customer patterns, and customer groups that need different business strategies.
