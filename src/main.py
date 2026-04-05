# main.py - DataFlow Pro ETL Engine
# Connects all 5 phases into one interactive CLI application

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from phase1_indexer import (generate_transactions,
                            run_benchmarks, run_search_benchmark,
                            extract_q3_sales, merge_sort)
from phase2_tracker import AppliedStepsTracker
from phase3_parser import DAXEvaluator, check_parentheses
from phase4_buffer import LiveIngestionQueue
from phase5_trees import DimensionIndex

try:
    from phase5_trees import OrgChartAnalyzer
    ANYTREE_AVAILABLE = True
except Exception:
    ANYTREE_AVAILABLE = False


def print_header():
    print("=" * 55)
    print("   Welcome to DataFlow Pro - NileMart ETL Engine")
    print("=" * 55)


def menu_phase1():
    print("\n  [Phase 1] Query Optimizer")
    print("  " + "-" * 40)
    print("  Generating 10,000 transactions...")
    data = generate_transactions(10000)
    run_benchmarks(data)
    sorted_by_id = merge_sort(data)
    sorted_by_date = sorted(data, key=lambda x: x["date"])
    run_search_benchmark(data, sorted_by_id)
    extract_q3_sales(sorted_by_date)


def menu_phase2(tracker):
    while True:
        print("\n  [Phase 2] Applied Steps Tracker")
        print("  " + "-" * 40)
        print("  a. Add transformation step")
        print("  b. Undo last step")
        print("  c. Redo step")
        print("  d. Print pipeline")
        print("  e. Back to main menu")
        choice = input("  Select: ").strip().lower()

        if choice == "a":
            step = input("  Enter step name (e.g. 'Removed Nulls'): ").strip()
            tracker.add_step(step)
        elif choice == "b":
            tracker.undo()
        elif choice == "c":
            tracker.redo()
        elif choice == "d":
            tracker.print_steps()
        elif choice == "e":
            break
        else:
            print("  Invalid choice.")


def menu_phase3():
    while True:
        print("\n  [Phase 3] DAX Formula Parser")
        print("  " + "-" * 40)
        print("  a. Check parentheses")
        print("  b. Evaluate postfix expression")
        print("  c. Back to main menu")
        choice = input("  Select: ").strip().lower()

        if choice == "a":
            expr = input("  Enter DAX expression: ").strip()
            valid, msg = check_parentheses(expr)
            print(f"  Result: {msg}")

        elif choice == "b":
            print("  Example: '15000 5000 + 2 *'  means (15000 + 5000) * 2")
            expr = input("  Enter postfix expression: ").strip()
            engine = DAXEvaluator()
            try:
                result = engine.evaluate_postfix(expr)
                print(f"  Result: {result:,} EGP")
            except Exception as e:
                print(f"  Error: {e}")

        elif choice == "c":
            break
        else:
            print("  Invalid choice.")


def menu_phase4(buffer):
    while True:
        print("\n  [Phase 4] Live Data Buffer")
        print("  " + "-" * 40)
        print(f"  Current buffer size: {buffer.size()}")
        print("  a. Enqueue live transaction")
        print("  b. Process batch")
        print("  c. Back to main menu")
        choice = input("  Select: ").strip().lower()

        if choice == "a":
            try:
                txn = int(input("  Transaction ID : "))
                branch = input("  Branch         : ").strip()
                amt = float(input("  Amount (EGP)   : "))
                buffer.enqueue_row({"txn": txn, "branch": branch,
                                    "amt_egp": amt})
            except ValueError:
                print("  Invalid input.")

        elif choice == "b":
            try:
                size = int(input("  Batch size: "))
                batch = buffer.process_batch(size)
                for item in batch:
                    print(f"  Processed: {item}")
            except ValueError:
                print("  Invalid input.")

        elif choice == "c":
            break
        else:
            print("  Invalid choice.")


def menu_phase5(bst):
    while True:
        print("\n  [Phase 5] Hierarchical Matrix Builder")
        print("  " + "-" * 40)
        print("  a. Insert customer into BST")
        print("  b. Search customer by National ID")
        print("  c. Print all customers (sorted)")
        if ANYTREE_AVAILABLE:
            print("  d. Display Org Chart")
            print("  e. Calculate Roll-Up Sales")
        print("  f. Back to main menu")
        choice = input("  Select: ").strip().lower()

        if choice == "a":
            try:
                nid = int(input("  National ID : "))
                name = input("  Name        : ").strip()
                bst.insert(nid, name)
                print(f"  [+] Inserted: {nid} -> {name}")
            except ValueError:
                print("  Invalid input.")

        elif choice == "b":
            try:
                nid = int(input("  National ID to search: "))
                result = bst.search(nid)
                if result:
                    print(f"  [FOUND] {nid} -> {result}")
                else:
                    print(f"  [NOT FOUND] {nid}")
            except ValueError:
                print("  Invalid input.")

        elif choice == "c":
            customers = bst.inorder()
            if customers:
                print("  Customers (sorted by National ID):")
                for nid, name in customers:
                    print(f"  {nid} : {name}")
            else:
                print("  No customers inserted yet.")

        elif choice == "d" and ANYTREE_AVAILABLE:
            org = OrgChartAnalyzer()
            org.display_chart()

        elif choice == "e" and ANYTREE_AVAILABLE:
            org = OrgChartAnalyzer()
            cairo_total = org.roll_up_sales(org.vp_cairo)
            alex_total = org.roll_up_sales(org.vp_alex)
            ceo_total = org.roll_up_sales(org.ceo)
            print(f"\n  Tarek (VP Cairo & Giza) : {cairo_total:,} EGP")
            print(f"  Salma (VP Alex & Delta) : {alex_total:,} EGP")
            print(f"  Omar  (Global CEO)      : {ceo_total:,} EGP")

        elif choice == "f":
            break
        else:
            print("  Invalid choice.")


def main():
    print_header()

    tracker = AppliedStepsTracker()
    buffer = LiveIngestionQueue()
    bst = DimensionIndex()

    while True:
        print("\n  Main Menu:")
        print("  " + "-" * 40)
        print("  1. Query Optimizer       (Phase 1 - Sorting & Search)")
        print("  2. Applied Steps Tracker (Phase 2 - Linked Lists)")
        print("  3. DAX Formula Parser    (Phase 3 - Stacks)")
        print("  4. Live Data Buffer      (Phase 4 - Queues)")
        print("  5. Hierarchical Matrix   (Phase 5 - Trees)")
        print("  6. Exit")
        print()
        choice = input("  Select an option: ").strip()

        if choice == "1":
            menu_phase1()
        elif choice == "2":
            menu_phase2(tracker)
        elif choice == "3":
            menu_phase3()
        elif choice == "4":

            menu_phase4(buffer)
        elif choice == "5":
            menu_phase5(bst)
        elif choice == "6":
            print("\n  Shutting down DataFlow Pro. Masalama!")
            sys.exit()
        else:
            print("  Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
