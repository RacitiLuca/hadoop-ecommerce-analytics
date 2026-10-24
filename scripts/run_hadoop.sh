#!/usr/bin/env bash
# Charge les données dans HDFS puis lance les 5 jobs Hadoop Streaming.
# Prérequis : HDFS et YARN démarrés (start-dfs.sh && start-yarn.sh), HADOOP_HOME défini.
# Usage : ./scripts/run_hadoop.sh [dossier_données]   (par défaut : data_gen, après generate_data.py)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DATA="${1:-$ROOT/data_gen}"
HDFS_DIR=/ecommerce_project
STREAMING_JAR=$(ls "$HADOOP_HOME"/share/hadoop/tools/lib/hadoop-streaming-*.jar | head -1)

hdfs dfs -mkdir -p "$HDFS_DIR"
hdfs dfs -put -f "$DATA"/customers.csv "$DATA"/products.csv "$DATA"/transactions.csv "$HDFS_DIR"/

i=1
for task in task1_top_products task2_active_customers task3_revenue task4_monthly_trends task5_bought_together; do
  out="$HDFS_DIR/output_task$i"
  hdfs dfs -rm -r -f "$out" >/dev/null
  extra=()
  [ "$task" = "task3_revenue" ] && extra=(-file "$DATA/products.csv")   # cache distribué
  hadoop jar "$STREAMING_JAR" \
    -input "$HDFS_DIR/transactions.csv" \
    -output "$out" \
    -mapper "python3 mapper.py" \
    -reducer "python3 reducer.py" \
    -file "$ROOT/$task/mapper.py" \
    -file "$ROOT/$task/reducer.py" \
    "${extra[@]}"
  echo "=== $task ==="
  hdfs dfs -cat "$out/part-00000" | head -25
  i=$((i+1))
done
