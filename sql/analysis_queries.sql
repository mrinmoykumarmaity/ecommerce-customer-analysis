-- E-commerce Customer Analysis SQL Queries
-- Use these queries after loading the CSV files into a SQL database.

-- 1. Customer Lifetime Value
SELECT
    c.customer_id,
    c.customer_name,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(oi.revenue), 2) AS customer_lifetime_value,
    ROUND(SUM(oi.revenue) / COUNT(DISTINCT o.order_id), 2) AS average_order_value
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'Completed'
GROUP BY c.customer_id, c.customer_name
ORDER BY customer_lifetime_value DESC;

-- 2. Repeat Customers vs One-time Customers
WITH customer_orders AS (
    SELECT
        customer_id,
        COUNT(DISTINCT order_id) AS total_orders
    FROM orders
    WHERE order_status = 'Completed'
    GROUP BY customer_id
)
SELECT
    CASE WHEN total_orders > 1 THEN 'Repeat Customer' ELSE 'One-time Customer' END AS customer_type,
    COUNT(*) AS total_customers
FROM customer_orders
GROUP BY customer_type;

-- 3. Revenue by Category
SELECT
    p.category,
    ROUND(SUM(oi.revenue), 2) AS total_revenue,
    SUM(oi.quantity) AS quantity_sold,
    COUNT(DISTINCT oi.order_id) AS total_orders
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status = 'Completed'
GROUP BY p.category
ORDER BY total_revenue DESC;

-- 4. Region-wise Revenue
SELECT
    c.region,
    ROUND(SUM(oi.revenue), 2) AS total_revenue,
    COUNT(DISTINCT o.customer_id) AS customers,
    COUNT(DISTINCT o.order_id) AS orders
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'Completed'
GROUP BY c.region
ORDER BY total_revenue DESC;
