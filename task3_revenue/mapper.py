#!/usr/bin/env python3
"""
Task 3 - Mapper: Revenue per Product and Category
Uses distributed cache: products.csv must be passed via -files option.
Input:  transactions.csv → transaction_id, customer_id, product_id, quantity, date
Output: product_id \t product_name \t category \t revenue
"""
import sys
import os

# ── Load products from distributed cache ──
products = {}  # product_id → (product_name, category, price)

# In Hadoop streaming with -files, the file is in the current working directory
products_file = "products.csv"
if not os.path.exists(products_file):
    # Fallback: try common locations
    for path in ["./products.csv", "../products.csv"]:
        if os.path.exists(path):
            products_file = path
            break

try:
    with open(products_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("product_id"):
                continue
            parts = line.split(",")
            if len(parts) != 4:
                continue
            pid, pname, category, price = parts
            try:
                products[pid] = (pname, category, float(price))
            except ValueError:
                continue
except FileNotFoundError:
    sys.stderr.write("ERROR: products.csv not found in distributed cache\n")
    sys.exit(1)

# ── Process transactions ──
for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("transaction_id"):
        continue

    parts = line.split(",")
    if len(parts) != 5:
        continue

    transaction_id, customer_id, product_id, quantity, date = parts

    if product_id not in products:
        continue

    try:
        qty = int(quantity)
    except ValueError:
        continue

    pname, category, price = products[product_id]
    revenue = round(qty * price, 2)

    # Emit: category|product_id → revenue (for aggregation by category AND product)
    print(f"{category}\t{product_id}\t{pname}\t{revenue}")
