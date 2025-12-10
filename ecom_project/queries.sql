-- Query 1: List all orders with customer and product details
SELECT
    c.first_name || ' ' || c.last_name AS customer_name,
    p.product_name,
    p.category,
    o.order_date,
    oi.quantity,
    pay.amount AS payment_amount,
    pay.payment_method
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
LEFT JOIN payments pay ON o.order_id = pay.order_id
ORDER BY o.order_date DESC, o.order_id, oi.order_item_id;

-- Query 2: Top 5 customers by total amount spent
SELECT
    c.first_name || ' ' || c.last_name AS customer_name,
    SUM(pay.amount) AS total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN payments pay ON o.order_id = pay.order_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total_spent DESC
LIMIT 5;

-- Query 3: Category-wise revenue summary
SELECT
    p.category,
    SUM(oi.quantity * oi.unit_price) AS category_revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY category_revenue DESC;

