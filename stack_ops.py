"""
Stack-based undo functionality -- directly analogous to the
"undo/redo" browser-navigation style stack session.
"""


class UndoStack:
    def __init__(self):
        self._stack = []

    def push_action(self, action):
        """
        action: a tuple describing what happened, e.g.
            ('issue', member_id, isbn)
            ('return', member_id, isbn)
        so it can be reversed later.
        """
        self._stack.append(action)

    def undo(self):
        """Pop and return the most recent action, or None if empty."""
        if not self._stack:
            return None
        return self._stack.pop()

    def peek(self):
        return self._stack[-1] if self._stack else None

    def __len__(self):
        return len(self._stack)

    def __repr__(self):
        return f"UndoStack({self._stack})"
