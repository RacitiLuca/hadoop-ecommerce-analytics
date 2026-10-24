#!/usr/bin/env python3
"""
Task 5 - Reducer: Frequently Bought Together
Input:  customer_id,date \t product_id  (sorted by key)
Output: product_A,product_B \t co_purchase_count

For each shopping session (customer+date), collects all distinct products,
generates sorted pairs, and counts how often each pair appears together.
"""
import sys
from collections import defaultdict
from itertools import combinations

pair_counts = defaultdict(int)

current_session = None
session_products = set()

def process_session():
    """Generate all product pairs from a session and count them."""
    if len(session_products) >= 2:
        # Sort to ensure consistent pair ordering (A,B) not (B,A)
        sorted_prods = sorted(session_products)
        for p1, p2 in combinations(sorted_prods, 2):
            pair_counts[(p1, p2)] += 1

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue

    parts = line.split("\t")
    if len(parts) != 2:
        continue

    session_key, product_id = parts

    if current_session == session_key:
        session_products.add(product_id)
    else:
        # Process previous session
        if current_session is not None:
            process_session()
        current_session = session_key
        session_products = {product_id}

# Process the last session
if current_session is not None:
    process_session()

# Output top 30 most frequent pairs
print("=== TOP 30 FREQUENTLY BOUGHT TOGETHER ===")
sorted_pairs = sorted(pair_counts.items(), key=lambda x: -x[1])
for (p1, p2), count in sorted_pairs[:30]:
    print(f"{p1},{p2}\t{count}")
