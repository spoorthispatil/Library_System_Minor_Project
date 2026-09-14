"""
Core data models for the Library Management System.
"""

from datetime import date


class Book:
    def __init__(self, isbn, title, author, genre_path, copies=1):
        """
        genre_path: list of genres from broad -> specific, e.g. ["Fiction", "Fantasy"]
        used to place the book in the GenreTree.
        """
        self.isbn = isbn
        self.title = title
        self.author = author
        self.genre_path = genre_path
        self.total_copies = copies
        self.available_copies = copies

    def __repr__(self):
        return f"Book({self.isbn}, '{self.title}' by {self.author}, avail={self.available_copies}/{self.total_copies})"


class Member:
    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name

    def __repr__(self):
        return f"Member({self.member_id}, {self.name})"


class Transaction:
    def __init__(self, member_id, isbn, issue_date, due_date, return_date=None):
        self.member_id = member_id
        self.isbn = isbn
        self.issue_date = issue_date
        self.due_date = due_date
        self.return_date = return_date

    def is_overdue(self, on_date=None):
        on_date = on_date or date.today()
        if self.return_date:
            return self.return_date > self.due_date
        return on_date > self.due_date

    def days_late(self, on_date=None):
        on_date = self.return_date or on_date or date.today()
        return max(0, (on_date - self.due_date).days)

    def __repr__(self):
        status = f"returned {self.return_date}" if self.return_date else "active"
        return f"Transaction(member={self.member_id}, isbn={self.isbn}, due={self.due_date}, {status})"
