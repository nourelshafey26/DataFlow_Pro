# DataFlow Pro - NileMart ETL Engine

A high-performance Python ETL (Extract, Transform, Load) engine built for NileMart Inc.
This engine cleans, sorts, and structures raw sales data before it reaches Power BI dashboards.

---

## Project Structure

'''
dataflow_pro/
├── data/
│   ├── transactions.csv      # 10,000 simulated sales transactions
│   └── employees.csv         # NileMart corporate hierarchy
├── src/
│   ├── phase1_indexer.py     # Sorting & Searching algorithms
│   ├── phase2_tracker.py     # Linked List transformation tracker
│   ├── phase3_parser.py      # Stack-based DAX formula parser
│   ├── phase4_buffer.py      # Queue-based live data buffer
│   ├── phase5_trees.py       # BST + Org Chart with roll-up sales
│   ├── generate_data.py      # Script to regenerate transactions.csv
│   └── main.py               # Interactive CLI application
├── requirements.txt
└── README.md
'''

---

## Installation

1. Clone the repository:
'''
[git clone https://github.com/YOUR_USERNAME/dataflow_pro.git](https://github.com/nourelshafey26/DataFlow_Pro)
cd dataflow_pro
'''

2. Install dependencies:
'''
pip install -r requirements.txt
'''

---

## How to Run

### Run the full interactive CLI

'''
cd src
python main.py
'''

### Run each phase individually

'''
python src/phase1_indexer.py
python src/phase2_tracker.py
python src/phase3_parser.py
python src/phase4_buffer.py
python src/phase5_trees.py
'''

### Regenerate the transactions dataset

'''
python src/generate_data.py
'''

---

## Phase Overview

### Phase 1 - Query Optimizer (Sorting & Searching)

- Implements Bubble Sort, Insertion Sort, Selection Sort (O(n^2))
- Implements Merge Sort and Quick Sort (O(n log n))
- Benchmarks all algorithms against Python built-in Timsort
- Linear Search vs Binary Search on 10,000 transactions
- Uses bisect module to extract Q3 sales data instantly

### Phase 2 - Applied Steps Tracker (Linked Lists)

- Singly Linked List: records every data transformation step
- Doubly Linked List: full Undo/Redo engine in O(1) time
- Mimics Power BI Power Query's Applied Steps panel

### Phase 3 - DAX Formula Parser (Stacks)

- Array-based Stack and Linked List-based Stack implementations
- Parentheses checker for DAX expressions
- Postfix (Reverse Polish Notation) expression evaluator
- Supports +, -, *, / operations on NileMart KPI formulas

### Phase 4 - Live Data Buffer (Queues)

- List-based Queue (O(n) dequeue) - demonstrates the performance trap
- Linked List Queue (O(1) dequeue) - custom implementation
- collections.deque (O(1)) - production-grade solution
- Performance benchmark: deque is ~25x faster than list-based queue

### Phase 5 - Hierarchical Matrix Builder (Trees)

- Binary Search Tree (BST) for Customer National ID indexing
- O(log n) insert and search vs O(n) linear search on lists
- N-ary Org Chart using anytree library
- Recursive roll-up function to aggregate sales bottom-up

---

## Performance Report

### Why Quick Sort beat Bubble Sort?

Bubble Sort is O(n^2) in all cases - it compares every pair of adjacent
elements in every pass regardless of existing order.
Quick Sort is O(n log n) on average - it partitions data around a pivot,
eliminating half the search space at each step. On 10,000 records,
Quick Sort is roughly 200x faster than Bubble Sort.

### Why Merge Sort over Quick Sort for production?

Merge Sort guarantees O(n log n) in ALL cases (worst, average, best).
Quick Sort degrades to O(n^2) on already-sorted or reverse-sorted data
if pivot selection is poor. For financial data that may arrive pre-sorted,
Merge Sort is the safer choice.

### Why Timsort (built-in .sort()) beats both?

Python's Timsort is implemented in C, not Python. It also combines
Merge Sort and Insertion Sort, exploiting existing order in real-world
data. It runs at native machine speed vs interpreted Python speed.

### Why deque instead of list for the Live Buffer?

list.pop(0) is O(n) - it shifts every remaining element one position
to the left in memory after removing the first item.
collections.deque.popleft() is O(1) - it just moves a pointer.
On 10,000 transactions, deque was 25x faster in our benchmark.

### Why BST instead of a list for Customer ID lookup?

Linear search on an unsorted list = O(n): up to 10,000 comparisons.
Binary search on a BST = O(log n): at most 14 comparisons for 10,000 records.
As NileMart grows to millions of customers, the BST advantage compounds.

---

## Sample Output

'''
Sorting Benchmark (10,000 records):
  Bubble Sort    : 0.05s  (on 500 records only)
  Insertion Sort : 0.03s  (on 500 records only)
  Merge Sort     : 0.10s  (on 10,000 records)
  Quick Sort     : 0.08s  (on 10,000 records)
  Timsort        : 0.004s (on 10,000 records)

Search Benchmark:
  Linear Search  : 0.000030s
  Binary Search  : 0.000014s

Q3 Sales (Jul-Sep 2024):
  Records : 2,500
  Revenue : 62,450,000 EGP

Roll-Up Sales:
  Tarek (VP Cairo & Giza) : 420,000 EGP
  Salma (VP Alex & Delta) : 300,000 EGP
  Omar  (Global CEO)      : 720,000 EGP
'''

---

## Submission

- Course   : ITI PortSaid | PowerBI46R2
- Project  : DataFlow Pro
- Deadline : 2026-04-04
- Email    : hassanmeldash@gmail.com
- Subject  : ITI PortSaid | PowerBI46R2 | DSA Project | DataFlow Pro | Group No.2
