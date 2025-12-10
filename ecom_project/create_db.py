import sqlite3
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = BASE_DIR / "ecommerce.db"

SCHEMA = """
PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    phone TEXT,
    city TEXT,
    state TEXT,
    signup_date TEXT
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    price REAL,
    stock_qty INTEGER
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date TEXT,
    status TEXT,
    total_amount REAL,
    shipping_city TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER,
    unit_price REAL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE payments (
    payment_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    payment_date TEXT,
    amount REAL,
    payment_method TEXT,
    payment_status TEXT,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
"""


def load_csv(name: str) -> pd.DataFrame:
    path = DATA_DIR / name
    return pd.read_csv(path)


def main():
    DATA_DIR.mkdir(exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(SCHEMA)

        tables = {
            "customers": load_csv("customers.csv"),
            "products": load_csv("products.csv"),
            "orders": load_csv("orders.csv"),
            "order_items": load_csv("order_items.csv"),
            "payments": load_csv("payments.csv"),
        }

        for table, df in tables.items():
            df.to_sql(table, conn, if_exists="append", index=False)

        # Preview first few rows of each table
        for table in tables:
            preview = pd.read_sql_query(f"SELECT * FROM {table} LIMIT 5;", conn)
            print(f"\n=== {table} (first 5 rows) ===")
            print(preview.to_string(index=False))


if __name__ == "__main__":
    main()

