"""
Singly linked list used to track each member's borrowing history in order.
Maps to the Linked List sessions (including traversal/deletion concepts).
"""


class TransactionNode:
    def __init__(self, transaction):
        self.transaction = transaction
        self.next = None


class BorrowHistory:
    def __init__(self):
        self.head = None
        self.size = 0

    def add(self, transaction):
        """Append a transaction to the end of the history (O(n))."""
        node = TransactionNode(transaction)
        self.size += 1
        if not self.head:
            self.head = node
            return
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = node

    def remove_active_for_isbn(self, isbn):
        """
        Removes (deletes) the node representing an active (not yet returned)
        transaction for a given isbn -- used when correcting a mistaken issue.
        Demonstrates linked list deletion.
        """
        prev, curr = None, self.head
        while curr:
            if curr.transaction.isbn == isbn and curr.transaction.return_date is None:
                if prev:
                    prev.next = curr.next
                else:
                    self.head = curr.next
                self.size -= 1
                return curr.transaction
            prev, curr = curr, curr.next
        return None

    def to_list(self):
        curr, out = self.head, []
        while curr:
            out.append(curr.transaction)
            curr = curr.next
        return out

    def __len__(self):
        return self.size

    def __repr__(self):
        return f"BorrowHistory({self.to_list()})"
