#!/usr/bin/env python3
"""
Task 4 - Reducer: Monthly Sales Trends
Input:  YYYY-MM \t quantity  (sorted by key)
Output: YYYY-MM \t total_quantity \t num_transactions
"""
import sys

current_month = None
total_qty = 0
num_transactions = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    parts = line.split("\t")
    if len(parts) != 2:
        continue

    month, quantity = parts

    try:
        qty = int(quantity)
    except ValueError:
        continue

    if current_month == month:
        total_qty += qty
        num_transactions += 1
    else:
        if current_month is not None:
            print(f"{current_month}\t{total_qty}\t{num_transactions}")
        current_month = month
        total_qty = qty
        num_transactions = 1

if current_month is not None:
    print(f"{current_month}\t{total_qty}\t{num_transactions}")
