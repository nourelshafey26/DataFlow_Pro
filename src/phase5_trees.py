# Phase 5: The Hierarchical Matrix Builder (Trees)
# - BST for Customer ID lookups
# - N-ary Org Chart with recursive roll-up sales

from anytree import Node, RenderTree

# PART 1: Binary Search Tree (Dimension Index)
# -------------------------------------------------


class BSTNode:
    # Simple BST node to store Customer National ID and Name
    def __init__(self, national_id, name):
        self.national_id = national_id
        self.name = name
        self.left = None
        self.right = None


class DimensionIndex:
    """
    BST to store unique Customer National IDs.
    insert : O(log n) average
    search : O(log n) average
    """

    def __init__(self):
        self.root = None

    def insert(self, national_id, name):
        # Inserts a new customer into the BST based on
        # their National ID.
        if self.root is None:
            self.root = BSTNode(national_id, name)
        else:
            self._insert(self.root, national_id, name)

    def _insert(self, node, national_id, name):
        # Recursively finds the correct position for the
        # new node based on National ID.
        if national_id < node.national_id:
            if node.left is None:
                node.left = BSTNode(national_id, name)
            else:
                self._insert(node.left, national_id, name)
        elif national_id > node.national_id:
            if node.right is None:
                node.right = BSTNode(national_id, name)
            else:
                self._insert(node.right, national_id, name)

    def search(self, national_id):
        # Searches for a customer by their National
        # ID and returns their name.
        return self._search(self.root, national_id)

    def _search(self, node, national_id):
        # Recursively traverses the BST to find the node with
        if node is None:
            return None
        if national_id == node.national_id:
            return node.name
        elif national_id < node.national_id:
            return self._search(node.left, national_id)
        else:
            return self._search(node.right, national_id)

    def inorder(self):
        # Returns a list of (National ID, Name) tuples in sorted order.
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        # Recursively performs an inorder traversal to
        # collect nodes in sorted order.
        if node:
            self._inorder(node.left, result)
            result.append((node.national_id, node.name))
            self._inorder(node.right, result)


# PART 2: N-ary Org Chart (anytree)
# -------------------------------------------------

class OrgChartAnalyzer:
    """
    Uses anytree to model NileMart's corporate hierarchy.
    Supports recursive roll-up sales aggregation.
    """

    def __init__(self):
        # Corporate Hierarchy
        self.ceo = Node("Omar (Global CEO)", sales=0)

        self.vp_cairo = Node("Tarek (VP Cairo & Giza)", parent=self.ceo, sales=0)
        self.vp_alex = Node("Salma (VP Alex & Delta)",
                            parent=self.ceo, sales=0)

        # Cairo & Giza branches
        Node("Aya (Maadi Branch Rep)", parent=self.vp_cairo, sales=150000)
        Node("Mahmoud (Zayed Branch Rep)", parent=self.vp_cairo, sales=270000)

        # Alex & Delta branches
        Node("Kareem (Smouha Branch Rep)", parent=self.vp_alex, sales=180000)
        Node("Nour (Mansoura Branch Rep)", parent=self.vp_alex, sales=120000)

    def display_chart(self):
        # Displays the organizational chart with sales figures for each node.
        print("\n  [Org Chart] NileMart Hierarchy:")
        for pre, _, node in RenderTree(self.ceo):
            print(f"  {pre}{node.name}  (Direct Sales: {node.sales:,} EGP)")

    def roll_up_sales(self, node):
        """
        Recursively calculates total sales for a manager
        by summing their own sales + all descendants' sales.
        """
        return node.sales + sum(self.roll_up_sales(child)
                                for child in node.children)


# TEST
# -------------------------------------------------

if __name__ == "__main__":

    print("=" * 55)
    print("  PART 1: BST - Customer Dimension Index")
    print("=" * 55)

    bst = DimensionIndex()

    customers = [
        (29801154321, "Ahmed Hassan"),
        (30105223456, "Sara Mohamed"),
        (28907334521, "Khaled Nour"),
        (30512445678, "Mona Ali"),
        (29203556789, "Omar Tarek"),
        (31001667890, "Nour Salma"),
        (28604778901, "Kareem Mahmoud"),
    ]

    print("\n  Inserting customers into BST...")
    for national_id, name in customers:
        bst.insert(national_id, name)
        print(f"  [+] {national_id} -> {name}")

    print("\n  Inorder traversal (sorted by National ID):")
    for nid, name in bst.inorder():
        print(f"  {nid} : {name}")

    print("\n  Searching for customers:")
    search_ids = [30105223456, 28604778901, 99999999999]
    for sid in search_ids:
        result = bst.search(sid)
        if result:
            print(f"  [FOUND] {sid} -> {result}")
        else:
            print(f"  [NOT FOUND] {sid}")

    print()
    print("=" * 55)
    print("  PART 2: Org Chart + Roll-Up Sales")
    print("=" * 55)

    org = OrgChartAnalyzer()
    org.display_chart()

    print("\n  [Roll-Up] Calculating total sales per region...")

    cairo_total = org.roll_up_sales(org.vp_cairo)
    alex_total = org.roll_up_sales(org.vp_alex)
    ceo_total = org.roll_up_sales(org.ceo)

    print(f"\n  Tarek (VP Cairo & Giza) total : {cairo_total:,} EGP")
    print(f"  Salma (VP Alex & Delta) total : {alex_total:,} EGP")
    print(f"  Omar  (Global CEO)      total : {ceo_total:,} EGP")

    print()
    print("[Phase 5] Complete")
