#!/usr/bin/env python3
"""
Generate synthetic e-commerce datasets:
  - customers.csv  (~1,000 customers)
  - products.csv   (~200 products)
  - transactions.csv (~1,050,000 transactions)
"""

import csv
import random
import os
from datetime import datetime, timedelta

random.seed(42)

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Customers ────────────────────────────────────────────────
FIRST_NAMES = [
    "Ahmed", "Fatma", "Mohamed", "Amira", "Youssef", "Nour", "Omar", "Sara",
    "Ali", "Mariem", "Khaled", "Ines", "Hamza", "Rania", "Amine", "Lina",
    "Sami", "Hana", "Bilel", "Dorra", "Tarek", "Sonia", "Wael", "Maha",
    "Rami", "Yasmine", "Fares", "Salma", "Zied", "Rim", "James", "Emma",
    "Luca", "Sophie", "Carlos", "Maria", "Chen", "Yuki", "Raj", "Priya"
]
LAST_NAMES = [
    "Ben Ali", "Trabelsi", "Bouazizi", "Gharbi", "Jebali", "Hammami",
    "Chaabane", "Maalej", "Sfar", "Lahmar", "Smith", "Johnson", "Garcia",
    "Rossi", "Müller", "Tanaka", "Kumar", "Wang", "Dupont", "Martin"
]
CITIES_COUNTRIES = [
    ("Tunis", "Tunisia"), ("Sfax", "Tunisia"), ("Sousse", "Tunisia"),
    ("Paris", "France"), ("Lyon", "France"), ("London", "UK"),
    ("Rome", "Italy"), ("Milan", "Italy"), ("Berlin", "Germany"),
    ("New York", "USA"), ("Los Angeles", "USA"), ("Tokyo", "Japan"),
    ("Dubai", "UAE"), ("Cairo", "Egypt"), ("Casablanca", "Morocco"),
    ("Istanbul", "Turkey"), ("Barcelona", "Spain"), ("Montreal", "Canada"),
    ("Mumbai", "India"), ("Shanghai", "China")
]

NUM_CUSTOMERS = 1000

customers = []
for i in range(1, NUM_CUSTOMERS + 1):
    cid = f"C{i:04d}"
    name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    city, country = random.choice(CITIES_COUNTRIES)
    customers.append((cid, name, city, country))

with open(os.path.join(OUTPUT_DIR, "customers.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["customer_id", "customer_name", "city", "country"])
    w.writerows(customers)

print(f"✅ customers.csv  → {NUM_CUSTOMERS} rows")

# ── Products ─────────────────────────────────────────────────
CATEGORIES = {
    "Electronics":   [("Smartphone", 299), ("Laptop", 899), ("Tablet", 449),
                      ("Headphones", 79), ("Smartwatch", 199), ("Camera", 549),
                      ("Speaker", 129), ("Monitor", 349), ("Keyboard", 59),
                      ("Mouse", 39), ("USB Hub", 25), ("Charger", 19)],
    "Clothing":      [("T-Shirt", 25), ("Jeans", 49), ("Jacket", 89),
                      ("Sneakers", 79), ("Dress", 59), ("Hoodie", 45),
                      ("Cap", 15), ("Scarf", 20), ("Belt", 29), ("Socks Pack", 12)],
    "Books":         [("Novel", 14), ("Textbook", 45), ("Comic", 9),
                      ("Cookbook", 22), ("Biography", 18), ("Self-Help", 16),
                      ("Science Book", 28), ("Art Book", 35)],
    "Home & Garden": [("Lamp", 39), ("Rug", 69), ("Cushion", 19),
                      ("Vase", 29), ("Candle Set", 15), ("Plant Pot", 12),
                      ("Wall Art", 45), ("Blanket", 35), ("Shelf", 55)],
    "Sports":        [("Football", 29), ("Basketball", 35), ("Yoga Mat", 25),
                      ("Dumbbells", 49), ("Jump Rope", 12), ("Boxing Gloves", 45),
                      ("Running Shoes", 89), ("Water Bottle", 15), ("Resistance Band", 18)],
    "Food & Drinks": [("Coffee Beans", 12), ("Tea Set", 19), ("Chocolate Box", 15),
                      ("Olive Oil", 9), ("Honey Jar", 11), ("Protein Bar Pack", 22),
                      ("Dried Fruits", 14), ("Spice Set", 18)],
}

products = []
pid = 1
for category, items in CATEGORIES.items():
    for name, base_price in items:
        # Add slight price variation
        price = round(base_price * random.uniform(0.9, 1.15), 2)
        products.append((f"P{pid:04d}", name, category, price))
        pid += 1

NUM_PRODUCTS = len(products)

with open(os.path.join(OUTPUT_DIR, "products.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["product_id", "product_name", "category", "price"])
    w.writerows(products)

print(f"✅ products.csv   → {NUM_PRODUCTS} rows")

# ── Transactions ─────────────────────────────────────────────
NUM_TRANSACTIONS = 1_050_000

# Date range: 2023-01-01 to 2024-12-31 (2 years)
start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)
date_range_days = (end_date - start_date).days

# Make some products more popular (power-law-ish distribution)
product_ids = [p[0] for p in products]
product_weights = [random.paretovariate(1.5) for _ in product_ids]

# Make some customers more active
customer_ids = [c[0] for c in customers]
customer_weights = [random.paretovariate(1.2) for _ in customer_ids]

def weighted_choice(items, weights):
    return random.choices(items, weights=weights, k=1)[0]

print(f"⏳ Generating {NUM_TRANSACTIONS:,} transactions...")

with open(os.path.join(OUTPUT_DIR, "transactions.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["transaction_id", "customer_id", "product_id", "quantity", "transaction_date"])

    for i in range(1, NUM_TRANSACTIONS + 1):
        tid = f"T{i:07d}"
        cid = weighted_choice(customer_ids, customer_weights)
        pid = weighted_choice(product_ids, product_weights)
        qty = random.choices([1, 2, 3, 4, 5], weights=[50, 25, 15, 7, 3], k=1)[0]
        day_offset = random.randint(0, date_range_days)
        date = (start_date + timedelta(days=day_offset)).strftime("%Y-%m-%d")
        w.writerow([tid, cid, pid, qty, date])

        if i % 200000 == 0:
            print(f"   ... {i:,} / {NUM_TRANSACTIONS:,}")

print(f"✅ transactions.csv → {NUM_TRANSACTIONS:,} rows")
print("\n🎉 Dataset generation complete!")
