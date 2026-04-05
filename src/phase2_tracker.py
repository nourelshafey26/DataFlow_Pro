# PART 1: Singly Linked List — Step History
# =======================================

class StepNode:
    # Represents a single transformation step in the pipeline.
    def __init__(self, step_name):
        self.step_name = step_name
        self.next = None  # Pointer to the next step in the history


class StepHistory:
    """Singly Linked List — records every transformation step in order."""
    def __init__(self):
        self.head = None
        self.size = 0

    def add_step(self, step_name):
        # Add a new transformation step to the end of the history.
        new_node = StepNode(step_name)
        if self.head is None:
            # First step in the history
            self.head = new_node
        else:
            # Traverse to the end of the list and append the new step
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1
        print(f"  [+] Step added: '{step_name}'")

    def print_steps(self):
        # Print the current transformation steps in the history.
        if self.head is None:
            print("  No steps recorded.")
            return
        current = self.head
        steps = []
        while current:
            # Collect step names for display
            steps.append(current.step_name)
            current = current.next
        print("  Pipeline: " + " -> ".join(steps))

    def remove_last(self):
        # Remove the last transformation step from the history.
        if self.head is None:
            print("  No steps to remove.")
            return
        if self.head.next is None:
            # Only one step in the history
            removed = self.head.step_name
            self.head = None
            self.size -= 1
            print(f"  [-] Removed: '{removed}'")
            return
        current = self.head
        while current.next.next:
            # Traverse to the second-to-last node
            current = current.next
        removed = current.next.step_name

        current.next = None  # Remove the last node
        self.size -= 1
        print(f"  [-] Removed: '{removed}'")


# PART 2: Doubly Linked List — Undo/Redo Engine
# =============================================

class DoublyStepNode:
    def __init__(self, step_name):
        self.step_name = step_name
        self.next = None
        self.prev = None


class AppliedStepsTracker:
    """
    Doubly Linked List — allows analysts to navigate
    forward and backward through transformation history in O(1).
    """

    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None
        self.size = 0

    def add_step(self, step_name):
        new_node = DoublyStepNode(step_name)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            self.current = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
            self.current = new_node
        self.size += 1
        print(f"  [+] Applied: '{step_name}'")

    def undo(self):
        # Move backward one step — O(1).
        if self.current is None:
            print("  Nothing to undo.")
            return
        if self.current.prev is None:
            # Already at the first step, can't go back further.
            print("  Already at the beginning.")
            return
        print(f"  [Undo] '{self.current.step_name}'")
        # Print the step being undone
        self.current = self.current.prev

    def redo(self):
        # Move forward one step — O(1).
        if self.current is None:
            print("  Nothing to redo.")
            return
        if self.current.next is None:
            print("  Already at the latest step.")
            return
        self.current = self.current.next
        print(f"  [Redo] '{self.current.step_name}'")

    def print_steps(self):
        # Print the current transformation steps, marking the current position.
        if self.head is None:
            print("  No steps recorded.")
            return
        current = self.head
        parts = []
        while current:
            # Mark the current step with brackets for clarity.
            if current == self.current:
                parts.append(f"[{current.step_name}]")  # current step marked
            else:
                parts.append(current.step_name)
            current = current.next
        print("  Pipeline: " + " <-> ".join(parts))
        print(f"  Current : '{self.current.step_name}'")


# MAIN
# =============================================================

if __name__ == "__main__":

    print("=" * 55)
    print(" PART 1: Singly Linked List — Step History")
    print("=" * 55)

    history = StepHistory()
    history.add_step("Connected to Source")
    history.add_step("Removed Nulls")
    history.add_step("Changed Type")
    history.add_step("Renamed Columns")
    history.print_steps()
    history.remove_last()
    history.print_steps()

    print()
    print("=" * 55)
    print("  PART 2: Doubly Linked List — Undo/Redo Engine")
    print("=" * 55)

    tracker = AppliedStepsTracker()
    tracker.add_step("Connected to Source")
    tracker.add_step("Removed Nulls")
    tracker.add_step("Changed Type")
    tracker.add_step("Renamed Columns")
    tracker.add_step("Filtered Rows")

    print()
    print("  Current state:")
    tracker.print_steps()

    print()
    print("  Undoing 2 steps:")
    tracker.undo()
    tracker.undo()
    tracker.print_steps()

    print()
    print("  Redoing 1 step:")
    tracker.redo()
    tracker.print_steps()

    print()
    print("[Phase 2] Complete ")
