# Phase 3: The DAX Formula Parser (Stacks)
# Evaluates postfix mathematical expressions using:
# - Array-based Stack  (Python list)
# - Linked List-based Stack (custom)


# PART 1: Array-Based Stack
# -------------------------------------------------

class ArrayStack:
    # Simple stack implementation using Python's built-in list.
    def __init__(self):
        self.stack = []

    def push(self, item):
        # Python's list append() is O(1) on average,
        # #making it efficient for stack push operations.
        self.stack.append(item)

    def pop(self):
        # pop() removes and returns the last item,
        # which is the top of the stack.
        # Raises IndexError if empty.
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.stack.pop()

    def peek(self):
        # peek() returns the top item without removing it.
        # Raises IndexError if empty.
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.stack[-1]

    def is_empty(self):
        # A stack is empty if its length is zero.
        return len(self.stack) == 0

    def size(self):
        # The size of the stack is simply the length of the underlying list.
        return len(self.stack)


# PART 2: Linked List-Based Stack
# -------------------------------------------------

class StackNode:
    # A node in the linked list stack,
    # containing data and a reference to the next node.
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedStack:
    # Stack implementation using a linked list.
    # The top of the stack is the head of the list.
    def __init__(self):
        self.top = None
        self.size = 0

    def push(self, item):
        # To push an item, we create a new node
        # and set it as the new top of the stack.
        new_node = StackNode(item)
        new_node.next = self.top
        self.top = new_node
        self.size += 1

    def pop(self):
        # To pop an item,
        # we return the data from the top node and update the top
        # reference to the next node.
        # Raises IndexError if empty.
        if self.is_empty():
            raise IndexError("Stack is empty")
        data = self.top.data
        self.top = self.top.next
        self.size -= 1
        return data

    def peek(self):
        # peek() returns the data from the top node without modifying stack.
        # Raises IndexError if empty.
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.top.data

    def is_empty(self):
        # A stack is empty if the top reference is None.
        return self.top is None


# PART 3: Parentheses Checker
# -------------------------------------------------

def check_parentheses(expression):
    """
    Checks if parentheses in a DAX expression are balanced.
    Uses ArrayStack.
    """
    stack = ArrayStack()
    matching = {')': '(', ']': '[', '}': '{'}

    for char in expression:
        # Only consider parentheses characters.
        # Ignore others (like letters, numbers, operators).
        if char in "([{":
            stack.push(char)
        elif char in ")]}":
            if stack.is_empty():
                return False, f"Extra closing '{char}' found"
            top = stack.pop()
            if top != matching[char]:
                return False, f"Mismatched: '{top}' closed by '{char}'"

    if not stack.is_empty():
        # If there are still items in the stack,
        # it means there are unmatched opening parentheses.
        return False, "Unclosed opening bracket"

    return True, "Parentheses are balanced"


# PART 4: Postfix Expression Evaluator
# -------------------------------------------------

class DAXEvaluator:
    """
    Evaluates postfix (Reverse Polish Notation) expressions.
    Example: "15000 5000 + 2 *"  means (15000 + 5000) * 2 = 40000

    Why postfix? Computers cannot read infix (human math) directly.
    Postfix removes the need for parentheses and operator precedence rules.
    """

    def __init__(self):
        self.stack = LinkedStack()

    def evaluate_postfix(self, expression):
        # Split the expression into tokens.
        # We expect numbers and operators separated by spaces.
        tokens = expression.strip().split()
        operators = {'+', '-', '*', '/'}

        for token in tokens:
            # If the token is not an operator,
            # we assume it's a number and push it onto the stack.
            if token not in operators:
                self.stack.push(float(token))
            else:
                # For an operator,
                # we need to pop the top two operands from the stack,
                # apply the operator, and push the result back.
                if self.stack.size < 2:
                    raise ValueError(
                        "Invalid expression - not enough operands")
                b = self.stack.pop()
                a = self.stack.pop()

                if token == '+':
                    self.stack.push(a + b)
                elif token == '-':
                    self.stack.push(a - b)
                elif token == '*':
                    self.stack.push(a * b)
                elif token == '/':
                    if b == 0:
                        raise ZeroDivisionError("Cannot divide by zero")
                    self.stack.push(a / b)

        result = self.stack.pop()
        return int(result) if result == int(result) else round(result, 2)


# MAIN
# -------------------------------------------------

if __name__ == "__main__":

    print("=" * 55)
    print("  PART 1 & 2: Stack Implementations")
    print("=" * 55)

    print("\n  Array-Based Stack:")
    a_stack = ArrayStack()
    a_stack.push(10)
    a_stack.push(20)
    a_stack.push(30)
    print(f"  Peek: {a_stack.peek()}")
    print(f"  Pop : {a_stack.pop()}")
    print(f"  Size: {a_stack.size()}")

    print("\n  Linked List-Based Stack:")
    l_stack = LinkedStack()
    l_stack.push(10)
    l_stack.push(20)
    l_stack.push(30)
    print(f"  Peek: {l_stack.peek()}")
    print(f"  Pop : {l_stack.pop()}")
    print(f"  Size: {l_stack.size}")

    print()
    print("=" * 55)
    print("  PART 3: Parentheses Checker")
    print("=" * 55)

    expressions = [
        "(Revenue - Cost) * Tax_Rate",
        "((Sales + Refunds) / Units",
        "(Profit * [Growth Rate])",
        "((Net_Income - Tax)) * 2)",
    ]

    for expr in expressions:
        valid, msg = check_parentheses(expr)
        status = "OK " if valid else "ERR"
        print(f"  [{status}] {expr}")
        if not valid:
            print(f"        -> {msg}")

    print()
    print("=" * 55)
    print("  PART 4: DAX Postfix Evaluator")
    print("=" * 55)

    test_cases = [
        ("15000 5000 + 2 *",   "(15000 + 5000) * 2"),
        ("50000 10000 - 4 /",  "(50000 - 10000) / 4"),
        ("1200 0.15 *",        "1200 * 0.15 (Tax)"),
        ("80000 20000 - 2 * 4 /", "((80000 - 20000) * 2) / 4"),
    ]

    for postfix, description in test_cases:
        evaluator = DAXEvaluator()
        result = evaluator.evaluate_postfix(postfix)
        print(f"  Formula : {description}")
        print(f"  Postfix : {postfix}")
        print(f"  Result  : {result:,} EGP")
        print()

    print("[Phase 3] Complete")
