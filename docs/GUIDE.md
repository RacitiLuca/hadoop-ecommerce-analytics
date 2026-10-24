# Big Data Project: E-commerce Analysis using Hadoop
## Complete Step-by-Step Guide

---

## PHASE 0: Prerequisites Check

Before anything, make sure your environment is ready.

```bash
# 1. Check Hadoop is installed
hadoop version

# 2. Check HDFS is running
hdfs dfs -ls /

# If HDFS is not running, start it:
start-dfs.sh
start-yarn.sh

# 3. Check Java
java -version

# 4. Check Python 3
python3 --version
```

If any of these fail, you need to fix your Hadoop installation first.

---

## PHASE 1: Generate the Dataset

### Step 1.1 — Create your project workspace

```bash
# Create a folder on your LOCAL filesystem
mkdir -p ~/bigdata_project
cd ~/bigdata_project
```

### Step 1.2 — Create the data generator script

Create a file called `generate_data.py` and paste the script provided in `data_gen/generate_data.py`.

```bash
nano generate_data.py
# Paste the content, then Ctrl+O to save, Ctrl+X to exit
```

### Step 1.3 — Run the generator

```bash
python3 generate_data.py
```

Expected output:
```
✅ customers.csv  → 1000 rows
✅ products.csv   → 56 rows
⏳ Generating 1,050,000 transactions...
✅ transactions.csv → 1,050,000 rows
🎉 Dataset generation complete!
```

### Step 1.4 — Verify the files

```bash
# Check file sizes
ls -lh *.csv

# Check headers and first rows
head -5 customers.csv
head -5 products.csv
head -5 transactions.csv

# Count rows
wc -l *.csv
```

Expected: `customers.csv` ~1001 lines, `products.csv` ~57 lines, `transactions.csv` ~1,050,001 lines.

---

## PHASE 2: Upload Data to HDFS

### Step 2.1 — Create the HDFS directory

```bash
hdfs dfs -mkdir -p /ecommerce_project
```

### Step 2.2 — Upload the CSV files

```bash
hdfs dfs -put customers.csv /ecommerce_project/
hdfs dfs -put products.csv /ecommerce_project/
hdfs dfs -put transactions.csv /ecommerce_project/
```

### Step 2.3 — Verify upload

```bash
hdfs dfs -ls /ecommerce_project/

# Check file sizes on HDFS
hdfs dfs -du -h /ecommerce_project/

# Quick sanity check (first 5 lines of transactions)
hdfs dfs -cat /ecommerce_project/transactions.csv | head -5
```

---

## PHASE 3: MapReduce Tasks

**Important:** For each task, you need to:
1. Create the `mapper.py` and `reducer.py` files
2. Make them executable (`chmod +x`)
3. Test locally first (optional but recommended)
4. Run on Hadoop using streaming

### How Hadoop Streaming Works

```
Input (HDFS) → Mapper (stdin/stdout) → Shuffle & Sort → Reducer (stdin/stdout) → Output (HDFS)
```

The mapper reads lines from stdin, processes them, and outputs `key\tvalue` pairs.
Hadoop sorts all mapper output by key.
The reducer reads the sorted `key\tvalue` pairs and aggregates them.

---

### TASK 1: Top-Selling Products

**Goal:** Identify which products sold the most units.

#### Step 3.1.1 — Create the mapper

```bash
mkdir -p ~/bigdata_project/task1
nano ~/bigdata_project/task1/mapper.py
```

**Paste the mapper code** (from `task1_top_products/mapper.py` in the project files).

**Logic explained:**
- Reads each transaction line
- Skips the CSV header
- Extracts `product_id` and `quantity`
- Emits: `product_id \t quantity`

#### Step 3.1.2 — Create the reducer

```bash
nano ~/bigdata_project/task1/reducer.py
```

**Paste the reducer code** (from `task1_top_products/reducer.py`).

**Logic explained:**
- Reads sorted `product_id \t quantity` pairs
- Groups consecutive lines with the same product_id
- Sums up all quantities per product
- Emits: `product_id \t total_quantity`

#### Step 3.1.3 — Make executable and test locally

```bash
chmod +x ~/bigdata_project/task1/mapper.py
chmod +x ~/bigdata_project/task1/reducer.py

# LOCAL TEST (simulates what Hadoop does)
cat ~/bigdata_project/transactions.csv \
  | python3 ~/bigdata_project/task1/mapper.py \
  | sort \
  | python3 ~/bigdata_project/task1/reducer.py \
  | sort -t$'\t' -k2 -rn \
  | head -10
```

#### Step 3.1.4 — Run on Hadoop

```bash
# Remove output directory if it exists from a previous run
hdfs dfs -rm -r /ecommerce_project/output_task1

# Run MapReduce
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -input /ecommerce_project/transactions.csv \
  -output /ecommerce_project/output_task1 \
  -mapper "python3 mapper.py" \
  -reducer "python3 reducer.py" \
  -file ~/bigdata_project/task1/mapper.py \
  -file ~/bigdata_project/task1/reducer.py
```

#### Step 3.1.5 — View results

```bash
# List output files
hdfs dfs -ls /ecommerce_project/output_task1/

# View results (sorted by quantity descending → Top 10)
hdfs dfs -cat /ecommerce_project/output_task1/part-00000 \
  | sort -t$'\t' -k2 -rn \
  | head -10
```

---

### TASK 2: Most Active Customers

**Goal:** Find customers with the highest number of transactions.

#### Step 3.2.1 — Create mapper and reducer

```bash
mkdir -p ~/bigdata_project/task2
nano ~/bigdata_project/task2/mapper.py   # Paste from task2_active_customers/mapper.py
nano ~/bigdata_project/task2/reducer.py  # Paste from task2_active_customers/reducer.py
chmod +x ~/bigdata_project/task2/*.py
```

**Mapper logic:** Emits `customer_id \t 1` for each transaction (counting pattern).
**Reducer logic:** Sums all 1s per customer → total transaction count.

#### Step 3.2.2 — Test locally

```bash
cat ~/bigdata_project/transactions.csv \
  | python3 ~/bigdata_project/task2/mapper.py \
  | sort \
  | python3 ~/bigdata_project/task2/reducer.py \
  | sort -t$'\t' -k2 -rn \
  | head -10
```

#### Step 3.2.3 — Run on Hadoop

```bash
hdfs dfs -rm -r /ecommerce_project/output_task2

hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -input /ecommerce_project/transactions.csv \
  -output /ecommerce_project/output_task2 \
  -mapper "python3 mapper.py" \
  -reducer "python3 reducer.py" \
  -file ~/bigdata_project/task2/mapper.py \
  -file ~/bigdata_project/task2/reducer.py
```

#### Step 3.2.4 — View results

```bash
hdfs dfs -cat /ecommerce_project/output_task2/part-00000 \
  | sort -t$'\t' -k2 -rn \
  | head -10
```

---

### TASK 3: Revenue Analysis

**Goal:** Calculate total revenue per product and per category.

This task is more complex because it requires a **join** — transactions have `product_id` and `quantity`, but the `price` is in `products.csv`. We use Hadoop's **distributed cache** to pass `products.csv` as a side file to the mapper.

#### Step 3.3.1 — Create mapper and reducer

```bash
mkdir -p ~/bigdata_project/task3
nano ~/bigdata_project/task3/mapper.py   # Paste from task3_revenue/mapper.py
nano ~/bigdata_project/task3/reducer.py  # Paste from task3_revenue/reducer.py
chmod +x ~/bigdata_project/task3/*.py
```

**Mapper logic:**
1. Loads `products.csv` from the distributed cache (the `-files` flag makes it available locally)
2. For each transaction, looks up the product's price and category
3. Calculates `revenue = quantity × price`
4. Emits: `category \t product_id \t product_name \t revenue`

**Reducer logic:** Aggregates revenue by category and by product, outputs sorted results.

#### Step 3.3.2 — Test locally

```bash
# Copy products.csv to the task3 directory (simulates distributed cache)
cp ~/bigdata_project/products.csv ~/bigdata_project/task3/products.csv

cd ~/bigdata_project/task3
cat ~/bigdata_project/transactions.csv \
  | python3 mapper.py \
  | sort \
  | python3 reducer.py
```

#### Step 3.3.3 — Run on Hadoop

```bash
hdfs dfs -rm -r /ecommerce_project/output_task3

hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -input /ecommerce_project/transactions.csv \
  -output /ecommerce_project/output_task3 \
  -mapper "python3 mapper.py" \
  -reducer "python3 reducer.py" \
  -file ~/bigdata_project/task3/mapper.py \
  -file ~/bigdata_project/task3/reducer.py \
  -file ~/bigdata_project/products.csv
```

**Note the extra `-file ~/bigdata_project/products.csv`** — this puts `products.csv` in the distributed cache so the mapper can access it.

#### Step 3.3.4 — View results

```bash
hdfs dfs -cat /ecommerce_project/output_task3/part-00000
```

---

### TASK 4: Monthly Sales Trends

**Goal:** Analyze how sales evolve month by month over 2 years.

#### Step 3.4.1 — Create mapper and reducer

```bash
mkdir -p ~/bigdata_project/task4
nano ~/bigdata_project/task4/mapper.py   # Paste from task4_monthly_trends/mapper.py
nano ~/bigdata_project/task4/reducer.py  # Paste from task4_monthly_trends/reducer.py
chmod +x ~/bigdata_project/task4/*.py
```

**Mapper logic:** Extracts `YYYY-MM` from the date, emits `month \t quantity`.
**Reducer logic:** Sums quantity and counts transactions per month.

#### Step 3.4.2 — Test locally

```bash
cat ~/bigdata_project/transactions.csv \
  | python3 ~/bigdata_project/task4/mapper.py \
  | sort \
  | python3 ~/bigdata_project/task4/reducer.py
```

#### Step 3.4.3 — Run on Hadoop

```bash
hdfs dfs -rm -r /ecommerce_project/output_task4

hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -input /ecommerce_project/transactions.csv \
  -output /ecommerce_project/output_task4 \
  -mapper "python3 mapper.py" \
  -reducer "python3 reducer.py" \
  -file ~/bigdata_project/task4/mapper.py \
  -file ~/bigdata_project/task4/reducer.py
```

#### Step 3.4.4 — View results

```bash
hdfs dfs -cat /ecommerce_project/output_task4/part-00000
```

---

### TASK 5: Frequently Bought Together (Advanced)

**Goal:** Find product pairs that customers often buy in the same session.

**Strategy:** A "shopping session" = same customer + same date. For each session with 2+ distinct products, generate all product pairs and count co-occurrences.

#### Step 3.5.1 — Create mapper and reducer

```bash
mkdir -p ~/bigdata_project/task5
nano ~/bigdata_project/task5/mapper.py   # Paste from task5_bought_together/mapper.py
nano ~/bigdata_project/task5/reducer.py  # Paste from task5_bought_together/reducer.py
chmod +x ~/bigdata_project/task5/*.py
```

**Mapper logic:** Emits `customer_id,date \t product_id` (groups by shopping session).
**Reducer logic:**
1. Collects all products per session
2. Generates all (sorted) pairs using combinations
3. Counts pair occurrences globally
4. Outputs the top 30 most frequent pairs

#### Step 3.5.2 — Test locally

```bash
cat ~/bigdata_project/transactions.csv \
  | python3 ~/bigdata_project/task5/mapper.py \
  | sort \
  | python3 ~/bigdata_project/task5/reducer.py
```

#### Step 3.5.3 — Run on Hadoop

```bash
hdfs dfs -rm -r /ecommerce_project/output_task5

hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -input /ecommerce_project/transactions.csv \
  -output /ecommerce_project/output_task5 \
  -mapper "python3 mapper.py" \
  -reducer "python3 reducer.py" \
  -file ~/bigdata_project/task5/mapper.py \
  -file ~/bigdata_project/task5/reducer.py
```

#### Step 3.5.4 — View results

```bash
hdfs dfs -cat /ecommerce_project/output_task5/part-00000
```

---

## PHASE 4: Interpretation & Business Insights

### Task 1 — Top-Selling Products

**What it means:** Products ranked by total units sold across all transactions.

**Key insights:**
- Identifies which products drive the most volume
- High-volume products may need better supply chain management
- Low-selling products might need marketing or discontinuation

**Recommendations:**
- Ensure top sellers are always in stock
- Negotiate better supplier prices for high-volume items
- Consider bundle deals with low-selling products

### Task 2 — Most Active Customers

**What it means:** Customers ranked by total number of purchases.

**Key insights:**
- Reveals the "power users" of the platform
- Top 10% of customers likely generate a disproportionate share of revenue (Pareto principle)
- Activity patterns help segment customers

**Recommendations:**
- Create a loyalty program for top customers
- Personalized offers and early access for VIP customers
- Analyze why some customers are inactive → re-engagement campaigns

### Task 3 — Revenue Analysis

**What it means:** Total money generated per product and per category.

**Key insights:**
- Electronics dominates revenue (high unit prices)
- Some high-volume products may not be top revenue generators
- Category-level view helps strategic resource allocation

**Recommendations:**
- Invest marketing budget proportionally to revenue-generating categories
- Identify high-margin products for promotion
- Cross-sell products from weaker categories

### Task 4 — Monthly Sales Trends

**What it means:** How sales volume evolves over 24 months.

**Key insights:**
- Reveals seasonality patterns (holiday spikes, summer dips)
- Year-over-year comparison shows growth or decline
- Helps forecast inventory needs

**Recommendations:**
- Stock up before high-demand months
- Plan promotional campaigns during low-demand periods
- Use trend data for financial forecasting

### Task 5 — Frequently Bought Together

**What it means:** Product pairs that appear together in the same shopping session.

**Key insights:**
- Reveals natural product affinities
- "Customers who bought X also bought Y" recommendation engine data
- Can optimize store layout (physical or digital)

**Recommendations:**
- Create bundle deals for top pairs
- Place frequently co-purchased items near each other on the website
- Use pairs for cross-sell recommendations at checkout

---

## PHASE 5: Troubleshooting

### Common Errors and Fixes

| Problem | Fix |
|---------|-----|
| `Permission denied` on mapper/reducer | `chmod +x mapper.py reducer.py` |
| `No such file or directory` | Check paths, ensure files exist |
| `hadoop streaming jar not found` | Run `find $HADOOP_HOME -name "hadoop-streaming*.jar"` |
| Job fails with `PipeMapRed.waitOutputThreads()` | Check mapper/reducer for Python errors. Test locally first! |
| `Output directory already exists` | Delete it: `hdfs dfs -rm -r /ecommerce_project/output_taskX` |
| Empty output | Check if the CSV has `\r\n` line endings: `file transactions.csv` |
| `python3 not found` in Hadoop | Use full path: `-mapper "/usr/bin/python3 mapper.py"` |

### Useful HDFS Commands

```bash
hdfs dfs -ls /ecommerce_project/          # List directory
hdfs dfs -cat /path/to/file | head -20    # View file content
hdfs dfs -du -h /ecommerce_project/       # Check sizes
hdfs dfs -rm -r /ecommerce_project/output_taskX  # Delete output
hdfs dfs -get /ecommerce_project/output_task1/part-00000 ~/results_task1.txt  # Download
```

---

## Summary: Complete File Structure

```
~/bigdata_project/
├── generate_data.py          ← Run this first
├── customers.csv             ← Generated (1,000 rows)
├── products.csv              ← Generated (56 rows)
├── transactions.csv          ← Generated (1,050,000 rows)
├── task1/
│   ├── mapper.py             ← Top-selling products
│   └── reducer.py
├── task2/
│   ├── mapper.py             ← Most active customers
│   └── reducer.py
├── task3/
│   ├── mapper.py             ← Revenue analysis (needs products.csv)
│   ├── reducer.py
│   └── products.csv          ← Copy here for local testing
├── task4/
│   ├── mapper.py             ← Monthly sales trends
│   └── reducer.py
└── task5/
    ├── mapper.py             ← Frequently bought together
    └── reducer.py
```
