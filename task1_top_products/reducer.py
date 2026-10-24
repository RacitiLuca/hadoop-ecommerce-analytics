#!/usr/bin/env python3
"""
Task 1 - Reducer: Top-Selling Products
Input:  product_id \t quantity  (sorted by key)
Output: product_id \t total_quantity_sold
"""
import sys

current_product = None
current_total = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    parts = line.split("\t")
    if len(parts) != 2:
        continue

    product_id, quantity = parts

    try:
        qty = int(quantity)
    except ValueError:
        continue

    if current_product == product_id:
        current_total += qty
    else:
        if current_product is not None:
            print(f"{current_product}\t{current_total}")
        current_product = product_id
        current_total = qty

# Don't forget the last group
if current_product is not None:
    print(f"{current_product}\t{current_total}")
