#!/usr/bin/env python3
"""
Task 2 - Reducer: Most Active Customers
Input:  customer_id \t 1  (sorted by key)
Output: customer_id \t transaction_count
"""
import sys

current_customer = None
current_count = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    parts = line.split("\t")
    if len(parts) != 2:
        continue

    customer_id, count = parts

    try:
        c = int(count)
    except ValueError:
        continue

    if current_customer == customer_id:
        current_count += c
    else:
        if current_customer is not None:
            print(f"{current_customer}\t{current_count}")
        current_customer = customer_id
        current_count = c

if current_customer is not None:
    print(f"{current_customer}\t{current_count}")
