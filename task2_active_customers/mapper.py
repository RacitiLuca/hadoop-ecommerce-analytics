#!/usr/bin/env python3
"""
Task 2 - Mapper: Most Active Customers
Input:  transactions.csv → transaction_id, customer_id, product_id, quantity, date
Output: customer_id \t 1
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

    # Emit: customer_id → 1 (count each transaction)
    print(f"{customer_id}\t1")
