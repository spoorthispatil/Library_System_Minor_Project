"""
FIFO reservation queue for books that are currently unavailable.
Maps to the Queue Types sessions.
"""

from collections import deque


class ReservationQueue:
    def __init__(self):
        self._queues = {}  # isbn -> deque of member_ids

    def add_request(self, isbn, member_id):
        self._queues.setdefault(isbn, deque()).append(member_id)

    def next_in_line(self, isbn):
        q = self._queues.get(isbn)
        if q:
            return q.popleft()
        return None

    def queue_length(self, isbn):
        return len(self._queues.get(isbn, []))

    def is_waiting(self, isbn, member_id):
        return member_id in self._queues.get(isbn, [])

    def __repr__(self):
        return f"ReservationQueue({dict(self._queues)})"
