#!/usr/bin/env python3
"""
Task 4 - Mapper: Monthly Sales Trends
Input:  transactions.csv → transaction_id, customer_id, product_id, quantity, date
Output: YYYY-MM \t quantity
"""
import sys

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("transaction_id"):
        continue

    parts = line.split(",")
    if len(parts) != 5:
        continue

    transaction_id, customer_id, product_id, quantity, date = parts

    try:
        qty = int(quantity)
    except ValueError:
        continue

    # Extract YYYY-MM from date (format: YYYY-MM-DD)
    month_key = date[:7]  # "2023-01"

    # Emit: month → quantity
    print(f"{month_key}\t{qty}")
