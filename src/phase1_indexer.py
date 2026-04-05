import random
import time
import bisect


# STEP 1: Generate 10,000 Transaction Records
# =========================================

def generate_transactions(n=10000):
    # Each transaction record is a dictionary with the following fields:
    # - "txn_id"   : A unique transaction ID (random integer)
    # - "branch"   : The branch where the transaction occurred
    #                (randomly chosen from a list of branches)
    # - "amt_egp"  : The amount of the transaction in Egyptian Pounds
    #                (random float)
    # - "date"     : The date of the transaction in the format YYYYMMDD
    branches = ["Maadi", "Zayed", "Smouha", "Mansoura", "Heliopolis", "Aswan"]
    transactions = []
    for i in range(n):
        # Generate random data for each transaction
        record = {
            "txn_id": random.randint(
                100000, 999999
            ),  # random integer between 100000 and 999999
            # randomly select a branch from the list
            "branch": random.choice(branches),
            "amt_egp": round(
                random.uniform(50, 50000), 2
            ),  # random float between 50 and 50000,
                # rounded to 2 decimal places
            "date": random.randint(
                20240101, 20241231
            ),  # random integer representing a date in the format
            # YYYYMMDD, between January 1, 2024 and December 31, 2024
        }
        transactions.append(record)
    return transactions


# STEP 2: Slow Sorting Algorithms
# ======================================


def bubble_sort(arr):
    # Bubble Sort: O(n^2) time complexity, stable, in-place
    arr = arr.copy()  # Work on a copy to avoid modifying the original data
    n = len(arr)
    for i in range(n):
        # Last i elements are already in place, so we can skip them
        for j in range(0, n - i - 1):
            # Compare adjacent elements and swap if they are in the wrong order
            if arr[j]["txn_id"] > arr[j + 1]["txn_id"]:
                # Swap arr[j] and arr[j + 1]
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def insertion_sort(arr):
    # Insertion Sort: O(n^2) time complexity, stable, in-place
    arr = arr.copy()
    for i in range(1, len(arr)):
        # The key is the current element we want to position
        # correctly in the sorted portion of the array
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j]["txn_id"] > key["txn_id"]:
            # Move elements of arr[0..i-1], that are greater than
            # key, to one position ahead of their current position
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def selection_sort(arr):
    # Selection Sort: O(n^2) time complexity, unstable, in-place
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        # Find the minimum element in the unsorted portion of the array
        min_idx = i
        for j in range(i + 1, n):
            # Compare the current element with the minimum element found so far
            if arr[j]["txn_id"] < arr[min_idx]["txn_id"]:
                # Update the index of the minimum element
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


# STEP 3: Fast Sorting Algorithms
# ===================================


def merge_sort(arr):
    # Merge Sort: O(n log n) time complexity, stable, not in-place
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)


def _merge(left, right):
    # Merge two sorted lists into a single sorted list
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        # Compare the current elements of both lists and append
        # the smaller one to the result list
        if left[i]["txn_id"] <= right[j]["txn_id"]:
            # If the current element of the left list is smaller or
            # equal, append it to the result list and move the
            # pointer for the left list
            result.append(left[i])
            i += 1
        else:
            # If the current element of the right list is smaller,
            # append it to the result list and move the pointer for
            # the right list
            result.append(right[j])
            j += 1
    # If there are remaining elements in the left / right list,
    # append them to the result list
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def quick_sort(arr):
    # Quick Sort: O(n log n) average time complexity, unstable,
    # in-place (with careful implementation)
    if len(arr) <= 1:
        # Base case: an array of zero or one elements is already sorted
        return arr
    # Choose the middle element as the pivot for better performance on average
    pivot = arr[len(arr) // 2]["txn_id"]
    left = [
        x for x in arr if x["txn_id"] < pivot
    ]  # Create a list of elements less than the pivot
    middle = [
        x for x in arr if x["txn_id"] == pivot
    ]  # Create a list of elements equal to the pivot (to handle duplicates)
    right = [
        x for x in arr if x["txn_id"] > pivot
    ]  # Create a list of elements greater than the pivot
    return (
        quick_sort(left) + middle + quick_sort(right)
    )  # Recursively sort the left and right lists and
    # concatenate them with the middle list to form the
    # sorted array


# STEP 4: Benchmark All Algorithms
# ==================================


# Benchmarking function to measure the execution time of each
# sorting algorithm. For the slower algorithms (Bubble Sort,
# Insertion Sort, Selection Sort), we will only benchmark them on
# the first 500 records to avoid excessively long execution times.
def benchmark(label, sort_fn, data, slow_limit=500):
    sample = (
        data[:slow_limit]
        if label in ("Bubble Sort", "Insertion Sort", "Selection Sort")
        else data
    )
    start = time.time()  # Measure the start time before sorting
    # Call the sorting function with the appropriate sample of data
    sort_fn(sample)
    # Measure the elapsed time after sorting and print the results
    elapsed = time.time() - start
    # For the slower algorithms, we will indicate that the
    # benchmark was run on a limited number of records (500) to
    # avoid confusion about the execution time. For the faster
    # algorithms, we will indicate that the benchmark was run on
    # the full dataset (10,000 records).
    note = (
        f"(on {slow_limit} records - too slow for 10k)"
        if sample is not data
        else "(on 10,000 records)"
    )
    print(f"  {label:20s}: {elapsed:.4f}s  {note}")


def run_benchmarks(data):

    print("\n[Phase 1] Sorting Benchmark")
    print("=" * 55)
    # We will benchmark each sorting algorithm and print the results
    # in a formatted manner. For the slower algorithms, we will
    # indicate that the benchmark was run on a limited number of
    # records (500) to avoid confusion about the execution time. For
    # the faster algorithms, we will indicate that the benchmark was
    # run on the full dataset (10,000 records).
    benchmark("Bubble Sort", bubble_sort, data)
    benchmark("Insertion Sort", insertion_sort, data)
    benchmark("Selection Sort", selection_sort, data)
    benchmark("Merge Sort", merge_sort, data)
    benchmark("Quick Sort", quick_sort, data)

    # Timsort (built-in)
    # We will use a copy of the original data to ensure that we are
    # sorting the same dataset as the other algorithms, and to avoid
    # modifying the original data for subsequent benchmarks.
    sample = data.copy()
    start = time.time()  # Measure the start time before sorting
    sample.sort(
        key=lambda x: x["txn_id"]
    )  # Use the built-in sort method, which implements Timsort,
    # and sort the data by the "txn_id" field using a lambda
    # function as the key
    elapsed = (
        time.time() - start
    )  # Measure the elapsed time after sorting and print the
    # results. We will indicate that the benchmark was run on the
    # full dataset (10,000 records) since Timsort is efficient
    # enough to handle it without issues.
    print(f"  {'Timsort (built-in)':20s}: {elapsed:.4f}s  (on 10,000 records)")


# STEP 5: Search Algorithms
# ==============================


def linear_search(data, target_id):
    # Linear Search: O(n) time complexity, works on unsorted data
    for i, record in enumerate(data):
        # Compare the "txn_id" field of the current record with the
        # target_id. If they match, return the index of the record. If
        # we reach the end of the data without finding a match, return
        # -1 to indicate that the target_id was not found.
        if record["txn_id"] == target_id:
            return i
    return -1


def binary_search(sorted_data, target_id):
    # Binary Search: O(log n) time complexity, requires sorted data
    low, high = 0, len(sorted_data) - 1
    while low <= high:
        # Calculate the midpoint index and compare the "txn_id" field
        # of the record at the midpoint with the target_id. If they
        # match, return the midpoint index. If the "txn_id" at the
        # midpoint is less than the target_id, we know that the
        # target_id must be in the upper half of the sorted data, so we
        # update low to mid + 1. If it is greater, we know that the
        # target_id must be in the lower half, so we update high to
        # mid - 1. If we exit the loop without finding a match, we
        # return -1 to indicate that the target_id was not found.
        mid = (low + high) // 2
        if sorted_data[mid]["txn_id"] == target_id:
            return mid
        elif sorted_data[mid]["txn_id"] < target_id:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def run_search_benchmark(unsorted_data, sorted_data):
    # For the search benchmark, we will pick a target transaction ID
    # from the middle of the unsorted data to ensure that it is
    # present in the dataset. We will then run both the linear search
    # on the unsorted data and the binary search on the sorted data,
    # measuring and printing the execution time for each.
    target_id = unsorted_data[500]["txn_id"]

    print("\n[Phase 1] Search Benchmark")
    print("=" * 55)
    print(f"  Searching for txn_id: {target_id}")

    start = time.time()
    # Perform a linear search on the unsorted data to find the
    # index of the record with the target transaction ID. We will
    # measure the time taken for this search and print the results,
    # including the index where the target was found.
    idx = linear_search(unsorted_data, target_id)
    elapsed = time.time() - start
    print(f"  Linear Search : {elapsed:.6f}s  -> found at index {idx}")

    start = time.time()
    # Perform a binary search on the sorted data to find the index
    # of the record with the target transaction ID. We will measure
    # the time taken for this search and print the results, including
    # the index where the target was found.
    idx = binary_search(sorted_data, target_id)
    elapsed = time.time() - start
    print(f"  Binary Search : {elapsed:.6f}s  -> found at index {idx}")


# STEP 6: bisect — Extract Q3 Sales
# =================================


def extract_q3_sales(sorted_data):
    # To extract all transactions that occurred in Q3 (July 1 to
    # September 30), we can use the bisect module to efficiently find
    # the range of records that fall within these dates. We will define
    # the start and end dates for Q3, and then use bisect.bisect_left
    # and bisect.bisect_right to find the indices of the first record
    # that is greater than or equal to the Q3 start date, and the first
    # record that is greater than the Q3 end date, respectively. This
    # will give us the range of records that occurred in Q3, which we
    # can then sum up to calculate the total revenue for that period.
    Q3_START = 20240701
    Q3_END = 20240930

    dates = [r["date"] for r in sorted_data]
    left = bisect.bisect_left(dates, Q3_START)
    right = bisect.bisect_right(dates, Q3_END)

    # The records that fall within the Q3 date range will be those
    # between the indices left (inclusive) and right (exclusive) in the
    # sorted data. We can then sum up the "amt_egp" field for these
    # records to calculate the total revenue for Q3.
    q3_records = sorted_data[left:right]

    # Calculate the total revenue for Q3 by summing the
    # "amt_egp" field for all records in the q3_records list.
    # We will print the number of records found and the total
    # revenue in a formatted manner.
    total = sum(r["amt_egp"] for r in q3_records)
    print("\n[Phase 1] Q3 Sales Extraction (bisect)")
    print("=" * 55)
    print(f"  Q3 records found : {len(q3_records):,}")
    print(f"  Q3 total revenue : {total:,.2f} EGP")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("Generating 10,000 transactions...")
    data = generate_transactions(10000)

    run_benchmarks(data)

    sorted_by_id = merge_sort(data)
    sorted_by_date = sorted(data, key=lambda x: x["date"])

    run_search_benchmark(data, sorted_by_id)
    extract_q3_sales(sorted_by_date)

    print("\n[Phase 1] Complete ")
