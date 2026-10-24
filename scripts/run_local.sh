#!/usr/bin/env bash
# Exécute les 5 jobs en local en simulant MapReduce : cat | mapper | sort | reducer
# Usage : ./scripts/run_local.sh [dossier_données]   (par défaut : data/sample)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DATA="${1:-$ROOT/data/sample}"
OUT="$ROOT/output"
mkdir -p "$OUT"

for task in task1_top_products task2_active_customers task3_revenue task4_monthly_trends task5_bought_together; do
  echo "▶ $task"
  # task3 lit products.csv dans le répertoire courant (équivalent du cache distribué Hadoop)
  (cd "$DATA" && cat transactions.csv \
     | python3 "$ROOT/$task/mapper.py" \
     | LC_ALL=C sort \
     | python3 "$ROOT/$task/reducer.py") > "$OUT/$task.txt"
  echo "  → output/$task.txt ($(wc -l < "$OUT/$task.txt") lignes)"
done
