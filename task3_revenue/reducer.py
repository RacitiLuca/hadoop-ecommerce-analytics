#!/usr/bin/env python3
"""
Task 3 - Reducer: Revenue per Category and per Product
Input:  category \t product_id \t product_name \t revenue (sorted by category)
Output: Two sections:
  - CATEGORY_REVENUE \t category \t total_revenue
  - PRODUCT_REVENUE  \t product_id \t product_name \t category \t total_revenue
"""
import sys
from collections import defaultdict

category_totals = defaultdict(float)
product_data = defaultdict(lambda: {"name": "", "category": "", "revenue": 0.0})

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    parts = line.split("\t")
    if len(parts) != 4:
        continue

    category, product_id, product_name, revenue = parts

    try:
        rev = float(revenue)
    except ValueError:
        continue

    category_totals[category] += rev
    product_data[product_id]["name"] = product_name
    product_data[product_id]["category"] = category
    product_data[product_id]["revenue"] += rev

# Output category revenues (sorted descending)
print("=== REVENUE BY CATEGORY ===")
for cat, rev in sorted(category_totals.items(), key=lambda x: -x[1]):
    print(f"CATEGORY\t{cat}\t{rev:.2f}")

print()
print("=== REVENUE BY PRODUCT (Top 20) ===")
sorted_products = sorted(product_data.items(), key=lambda x: -x[1]["revenue"])
for pid, info in sorted_products[:20]:
    print(f"PRODUCT\t{pid}\t{info['name']}\t{info['category']}\t{info['revenue']:.2f}")
