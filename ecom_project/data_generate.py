import csv
import random
from datetime import date, timedelta
from pathlib import Path


random.seed(42)

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)


def daterange(start: date, end: date) -> date:
    """Return a random date between start and end (inclusive)."""
    delta_days = (end - start).days
    return start + timedelta(days=random.randint(0, delta_days))


def build_customers(total: int = 50):
    first_names = [
        "Alice",
        "Bob",
        "Carol",
        "David",
        "Emma",
        "Frank",
        "Grace",
        "Henry",
        "Irene",
        "Jack",
        "Karen",
        "Liam",
        "Mia",
        "Noah",
        "Olivia",
        "Paul",
        "Quinn",
        "Riley",
        "Sophia",
        "Thomas",
        "Uma",
        "Victor",
        "Willow",
        "Xavier",
        "Yara",
        "Zane",
    ]
    last_names = [
        "Johnson",
        "Smith",
        "Davis",
        "Lee",
        "Wilson",
        "Garcia",
        "Kim",
        "Brown",
        "Patel",
        "Nguyen",
        "Lopez",
        "Martin",
        "Clark",
        "Walker",
        "Hall",
        "Young",
        "Allen",
        "Scott",
        "Turner",
        "Baker",
    ]
    cities_states = [
        ("Seattle", "WA"),
        ("Portland", "OR"),
        ("San Francisco", "CA"),
        ("Los Angeles", "CA"),
        ("San Diego", "CA"),
        ("Sacramento", "CA"),
        ("Denver", "CO"),
        ("Austin", "TX"),
        ("Dallas", "TX"),
        ("Houston", "TX"),
        ("Chicago", "IL"),
        ("Columbus", "OH"),
        ("Detroit", "MI"),
        ("Miami", "FL"),
        ("Orlando", "FL"),
        ("Atlanta", "GA"),
        ("Raleigh", "NC"),
        ("Charlotte", "NC"),
        ("Nashville", "TN"),
        ("New York", "NY"),
    ]

    customers = []
    signup_start = date(2023, 11, 1)
    signup_end = date(2024, 9, 30)
    for cid in range(1, total + 1):
        first = first_names[(cid - 1) % len(first_names)]
        last = last_names[(cid - 1) % len(last_names)]
        city, state = cities_states[(cid - 1) % len(cities_states)]
        customers.append(
            {
                "customer_id": cid,
                "first_name": first,
                "last_name": last,
                "email": f"{first.lower()}.{last.lower()}{cid}@example.com",
                "phone": f"555-{1000 + cid:04d}",
                "city": city,
                "state": state,
                "signup_date": daterange(signup_start, signup_end).isoformat(),
            }
        )
    return customers


def build_products():
    base_products = [
        ("Laptop 15\"", "Computers", 999.99),
        ("Smartphone X", "Mobile", 699.99),
        ("Noise-Canceling Headphones", "Audio", 129.99),
        ("Smartwatch Pro", "Wearables", 199.99),
        ("Gaming Console", "Entertainment", 399.99),
        ("Tablet 10\"", "Mobile", 329.99),
        ("Bluetooth Speaker", "Audio", 89.99),
        ("External SSD 1TB", "Storage", 149.99),
        ("27\" 4K Monitor", "Computers", 249.99),
        ("Mechanical Keyboard", "Peripherals", 59.99),
        ("Wireless Mouse", "Peripherals", 39.99),
        ("HD Webcam", "Peripherals", 79.99),
        ("All-in-One Printer", "Peripherals", 199.99),
        ("Wi-Fi 6 Router", "Networking", 129.99),
        ("Camera Drone", "Electronics", 499.99),
        ("VR Headset", "Electronics", 299.99),
        ("Smart Home Hub", "Home", 149.99),
        ("Fitness Tracker", "Wearables", 99.99),
        ("Portable Charger 20k", "Accessories", 49.99),
        ("E-reader", "Electronics", 119.99),
    ]
    products = []
    for idx, (name, category, price) in enumerate(base_products, start=1):
        stock = random.randint(80, 500)
        products.append(
            {
                "product_id": idx,
                "product_name": name,
                "category": category,
                "price": round(price, 2),
                "stock_qty": stock,
            }
        )
    return products


def build_orders(customers, total: int = 100):
    start = date(2024, 1, 1)
    end = date(2024, 10, 31)
    statuses = ["processing", "shipped", "delivered"]
    orders = []
    for oid in range(1, total + 1):
        customer = random.choice(customers)
        orders.append(
            {
                "order_id": 5000 + oid,
                "customer_id": customer["customer_id"],
                "order_date": daterange(start, end).isoformat(),
                "status": random.choice(statuses),
                "total_amount": 0.0,  # to be filled after order items
                "shipping_city": customer["city"],
            }
        )
    return orders


def build_order_items(orders, products):
    order_items = []
    for order in orders:
        num_items = random.randint(1, 4)
        chosen_products = random.sample(products, num_items)
        order_total = 0.0
        for pid in chosen_products:
            quantity = random.randint(1, 3)
            unit_price = pid["price"]
            line_total = quantity * unit_price
            order_total += line_total
            order_items.append(
                {
                    "order_item_id": len(order_items) + 1,
                    "order_id": order["order_id"],
                    "product_id": pid["product_id"],
                    "quantity": quantity,
                    "unit_price": round(unit_price, 2),
                }
            )
        order["total_amount"] = round(order_total, 2)
    return order_items


def build_payments(orders):
    methods = ["credit_card", "debit_card", "paypal", "apple_pay", "google_pay"]
    statuses = ["completed", "pending"]
    payments = []
    for order in orders:
        payments.append(
            {
                "payment_id": 9000 + len(payments) + 1,
                "order_id": order["order_id"],
                "payment_date": order["order_date"],
                "amount": order["total_amount"],
                "payment_method": random.choice(methods),
                "payment_status": random.choices(
                    statuses, weights=[0.8, 0.2], k=1
                )[0],
            }
        )
    return payments


def write_csv(path: Path, headers, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def main():
    customers = build_customers(50)
    products = build_products()
    orders = build_orders(customers, 100)
    order_items = build_order_items(orders, products)
    payments = build_payments(orders)

    write_csv(
        DATA_DIR / "customers.csv",
        [
            "customer_id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "city",
            "state",
            "signup_date",
        ],
        customers,
    )
    write_csv(
        DATA_DIR / "products.csv",
        ["product_id", "product_name", "category", "price", "stock_qty"],
        products,
    )
    write_csv(
        DATA_DIR / "orders.csv",
        [
            "order_id",
            "customer_id",
            "order_date",
            "status",
            "total_amount",
            "shipping_city",
        ],
        orders,
    )
    write_csv(
        DATA_DIR / "order_items.csv",
        ["order_item_id", "order_id", "product_id", "quantity", "unit_price"],
        order_items,
    )
    write_csv(
        DATA_DIR / "payments.csv",
        [
            "payment_id",
            "order_id",
            "payment_date",
            "amount",
            "payment_method",
            "payment_status",
        ],
        payments,
    )


if __name__ == "__main__":
    main()

