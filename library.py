"""
Library: the main orchestrator class that ties together every data
structure module into one cohesive system.
"""

from datetime import date, timedelta

from catalog import Catalog
from linked_list import BorrowHistory
from stack_ops import UndoStack
from queue_waitlist import ReservationQueue
from genre_tree import GenreTree
from graph import CoBorrowGraph
from dp_fines import calculate_fine
from models import Member, Transaction


class Library:
    def __init__(self):
        self.catalog = Catalog()
        self.genre_tree = GenreTree()
        self.reservation_queue = ReservationQueue()
        self.recommender = CoBorrowGraph()

        self.members = {}                 # member_id -> Member
        self.histories = {}               # member_id -> BorrowHistory
        self.undo_stacks = {}             # member_id -> UndoStack
        self.active_transactions = {}     # (member_id, isbn) -> Transaction

    # ---------- setup ----------

    def add_book(self, book):
        self.catalog.add_book(book)
        self.genre_tree.add_book(book.genre_path, book)

    def register_member(self, member_id, name):
        member = Member(member_id, name)
        self.members[member_id] = member
        self.histories[member_id] = BorrowHistory()
        self.undo_stacks[member_id] = UndoStack()
        return member

    # ---------- core operations ----------

    def issue_book(self, member_id, isbn, loan_days=14):
        book = self.catalog.get_book(isbn)
        if not book:
            return f"No such book: {isbn}"

        if book.available_copies <= 0:
            self.reservation_queue.add_request(isbn, member_id)
            return f"'{book.title}' unavailable -- {member_id} added to waitlist " \
                   f"(position {self.reservation_queue.queue_length(isbn)})"

        book.available_copies -= 1
        issue_date = date.today()
        due_date = issue_date + timedelta(days=loan_days)
        txn = Transaction(member_id, isbn, issue_date, due_date)

        self.histories[member_id].add(txn)
        self.active_transactions[(member_id, isbn)] = txn
        self.undo_stacks[member_id].push_action(("issue", member_id, isbn))

        return f"Issued '{book.title}' to {member_id}, due {due_date}"

    def return_book(self, member_id, isbn):
        book = self.catalog.get_book(isbn)
        txn = self.active_transactions.pop((member_id, isbn), None)

        if not book or not txn:
            return f"No active loan of {isbn} for {member_id}"

        txn.return_date = date.today()
        book.available_copies += 1
        self.undo_stacks[member_id].push_action(("return", member_id, isbn))

        fine = 0
        if txn.is_overdue():
            fine = calculate_fine(txn.days_late())

        # serve next person on the waitlist, if any
        next_member = self.reservation_queue.next_in_line(isbn)
        msg = f"'{book.title}' returned by {member_id}."
        if fine:
            msg += f" Fine due: ${fine}."
        if next_member:
            issue_msg = self.issue_book(next_member, isbn)
            msg += f" Auto-issued to next in line: {issue_msg}"

        return msg

    def undo_last_action(self, member_id):
        stack = self.undo_stacks.get(member_id)
        if not stack:
            return "No such member"
        action = stack.undo()
        if not action:
            return "Nothing to undo"

        kind, m_id, isbn = action
        book = self.catalog.get_book(isbn)
        if kind == "issue":
            # reverse an issue: put the copy back, remove the transaction
            book.available_copies += 1
            self.active_transactions.pop((m_id, isbn), None)
            self.histories[m_id].remove_active_for_isbn(isbn)
            return f"Undid issue of '{book.title}' to {m_id}"
        elif kind == "return":
            # reverse a return: take the copy back out
            book.available_copies -= 1
            return f"Undid return of '{book.title}' by {m_id}"
        return "Unknown action"

    # ---------- browsing / discovery ----------

    def browse_genre(self, genre_path):
        return self.genre_tree.dfs_list_books(genre_path)

    def recommend_related(self, isbn, limit=5):
        return self.recommender.recommend_bfs(isbn, depth=2, limit=limit)

    def record_session_borrow(self, isbn_list):
        """Feed a completed multi-book checkout into the recommendation graph."""
        self.recommender.record_borrow_session(isbn_list)

    def sorted_catalog_by_title(self):
        return self.catalog.merge_sort(self.catalog.all_books(), key_func=lambda b: b.title)

    def search_by_title(self, title):
        sorted_books = self.sorted_catalog_by_title()
        return self.catalog.binary_search_by_title(sorted_books, title)
