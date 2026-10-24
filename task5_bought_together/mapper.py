#!/usr/bin/env python3
"""
Task 5 - Mapper: Frequently Bought Together
Strategy: Group transactions by (customer_id, date) to find products
          purchased in the same "shopping session".
Input:  transactions.csv → transaction_id, customer_id, product_id, quantity, date
Output: customer_id,date \t product_id
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

    # Key = customer + date (same shopping session)
    # Value = product purchased
    session_key = f"{customer_id},{date}"
    print(f"{session_key}\t{product_id}")
