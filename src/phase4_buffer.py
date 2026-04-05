# Phase 4: The Live Data Buffer (Queues)
# Handles live streaming sales data using 3 Queue implementations:
# 1. List-based Queue       - O(n) dequeue (slow)
# 2. Linked List Queue      - O(1) dequeue (better)
# 3. collections.deque      - O(1) dequeue (production)

import time
from collections import deque


# PART 1: List-Based Queue (Slow - O(n))
# -------------------------------------------------

class ListQueue:
    """
    Queue using a standard Python list.
    enqueue: O(1) - append to end
    dequeue: O(n) - pop(0) shifts all elements left
    """

    def __init__(self):
        self.queue = []

    def enqueue(self, item):
        # O(1) - append to end of list
        self.queue.append(item)

    def dequeue(self):
        # O(n) - pop(0) removes first element and shifts all others left
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.queue.pop(0)    # O(n) - shifts every element left

    def peek(self):
        # O(1) - just look at the first element
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.queue[0]

    def is_empty(self):
        # O(1) - check if list is empty
        return len(self.queue) == 0

    def size(self):
        # O(1) - return length of list
        return len(self.queue)


# PART 2: Linked List Queue (Better - O(1))
# -------------------------------------------------

class QueueNode:
    # Node for Linked List Queue
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedQueue:
    """
    Queue using a Linked List.
    enqueue: O(1) - insert at tail
    dequeue: O(1) - remove from head
    """

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def enqueue(self, item):
        # O(1) - create new node and update tail
        new_node = QueueNode(item)
        if self.tail is None:
            self.head = new_node
            self.tail = new_node
        else:
            # O(1) - link new node at tail and update tail pointer
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def dequeue(self):
        # O(1) - remove head node and update head pointer
        if self.is_empty():
            raise IndexError("Queue is empty")
        data = self.head.data
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self.size -= 1
        return data

    def peek(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.head.data

    def is_empty(self):
        return self.head is None

    def size(self):
        return self.size


# PART 3: collections.deque (Production - O(1))
# -------------------------------------------------

class LiveIngestionQueue:
    """
    Buffers live streaming sales data from NileMart branches
    before pushing to Power BI.
    Uses collections.deque for O(1) enqueue and dequeue.
    """

    def __init__(self):
        self.buffer = deque()

    def enqueue_row(self, row_data):
        # O(1) - append to right end of deque
        self.buffer.append(row_data)
        print(f"  [Buffer] Enqueued: {row_data}")

    def process_batch(self, batch_size):
        # O(batch_size) - pop from left end of deque up to batch_size times
        processed_data = []
        for _ in range(batch_size):
            # O(1) - popleft removes and returns leftmost item
            if not self.buffer:
                # Buffer is empty, no more data to process
                break
            processed_data.append(self.buffer.popleft())   # O(1)
        print(f"[Buffer] Processed {len(processed_data)} transactions ->Pushing to Power BI")
        return processed_data

    def is_empty(self):
        return len(self.buffer) == 0

    def size(self):
        return len(self.buffer)


# PART 4: Benchmark - List vs Linked vs deque
# -------------------------------------------------

def run_benchmark(n=10000):
    # Benchmark the performance of ListQueue,
    # LinkedQueue, and collections.deque
    print(f"  Benchmarking with {n:,} transactions...\n")
    data = [{"txn": i, "amt": i * 10} for i in range(n)]

    # List Queue
    q = ListQueue()
    start = time.time()
    for item in data:
        q.enqueue(item)
    while not q.is_empty():
        q.dequeue()
    list_time = time.time() - start
    print(f"List Queue : {list_time:.4f}s (dequeue is O(n) - shifts all elements)")

    # Linked Queue
    q = LinkedQueue()
    start = time.time()
    for item in data:
        q.enqueue(item)
    while not q.is_empty():
        q.dequeue()
    linked_time = time.time() - start
    print(f"Linked Queue:{linked_time:.4f}s(dequeue is O(1) - just moves head pointer)")

    # deque
    q = deque()
    start = time.time()
    for item in data:
        q.append(item)
    while q:
        q.popleft()
    deque_time = time.time() - start
    print(f"  collections.deque: {deque_time:.4f}s  (O(1) - implemented in C)")

    print(f"\n  deque is {list_time / deque_time:.1f}x faster than List Queue")


# TEST
# -------------------------------------------------

if __name__ == "__main__":

    print("=" * 55)
    print("  PART 1: List Queue (O(n) dequeue)")
    print("=" * 55)
    lq = ListQueue()
    lq.enqueue({"txn": 1001, "branch": "Maadi",  "amt": 850})
    lq.enqueue({"txn": 1002, "branch": "Smouha", "amt": 3200})
    lq.enqueue({"txn": 1003, "branch": "Zayed",  "amt": 1500})
    print(f"  Size  : {lq.size()}")
    print(f"  Peek  : {lq.peek()}")
    print(f"  Dequeue: {lq.dequeue()}")
    print(f"  Size after dequeue: {lq.size()}")

    print()
    print("=" * 55)
    print("  PART 2: Linked List Queue (O(1) dequeue)")
    print("=" * 55)
    llq = LinkedQueue()
    llq.enqueue({"txn": 1004, "branch": "Maadi",  "amt": 920})
    llq.enqueue({"txn": 1005, "branch": "Smouha", "amt": 4100})
    llq.enqueue({"txn": 1006, "branch": "Zayed",  "amt": 700})
    print(f"  Size  : {llq.size}")
    print(f"  Peek  : {llq.peek()}")
    print(f"  Dequeue: {llq.dequeue()}")
    print(f"  Size after dequeue: {llq.size}")

    print()
    print("=" * 55)
    print("  PART 3: Live Ingestion Queue (collections.deque)")
    print("=" * 55)
    live_q = LiveIngestionQueue()
    live_q.enqueue_row({"txn": 1045, "branch": "Maadi",  "amt_egp": 850})
    live_q.enqueue_row({"txn": 1046, "branch": "Smouha", "amt_egp": 3200})
    live_q.enqueue_row({"txn": 1047, "branch": "Zayed",  "amt_egp": 1750})
    live_q.enqueue_row({"txn": 1048, "branch": "Mansoura", "amt_egp": 600})
    print(f"  Buffer size: {live_q.size()}")
    print()
    batch = live_q.process_batch(3)
    print(f"  Remaining in buffer: {live_q.size()}")

    print()
    print("=" * 55)
    print("  PART 4: Performance Benchmark")
    print("=" * 55)
    run_benchmark(10000)

    print()
    print("[Phase 4] Complete")
