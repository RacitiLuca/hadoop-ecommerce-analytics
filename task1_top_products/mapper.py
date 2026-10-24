#!/usr/bin/env python3
"""
Task 1 - Mapper: Top-Selling Products
Input:  transactions.csv → transaction_id, customer_id, product_id, quantity, date
Output: product_id \t quantity
"""
import sys

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("transaction_id"):
        continue  # skip header

    parts = line.split(",")
    if len(parts) != 5:
        continue

    transaction_id, customer_id, product_id, quantity, date = parts

    try:
        qty = int(quantity)
    except ValueError:
        continue

    # Emit: product_id → quantity
    print(f"{product_id}\t{qty}")
