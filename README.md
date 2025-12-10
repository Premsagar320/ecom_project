# ecom_project
It generates synthetic e-commerce data, loads it into an SQLite database, and runs SQL JOIN queries

Generates synthetic e-commerce CSV datasets
(i) customers
(ii) products
(iii) orders
(iv) order_items
(v) payments
Creates an SQLite database (ecommerce.db)
then it imports all CSV files into database tables
Includes JOIN-based SQL queries:
(i) Orders with customer + product + payment details
(ii) Top 5 customers by total spend
(iii) Category-wise revenue 
