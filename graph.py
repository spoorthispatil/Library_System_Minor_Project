"""
Graph of co-borrowed books, used to recommend related books via BFS/DFS
traversal. Maps to the Graph Fundamentals / Traversal sessions.
"""

from collections import defaultdict, deque


class CoBorrowGraph:
    def __init__(self):
        self.adj = defaultdict(set)  # isbn -> set of co-borrowed isbns

    def record_borrow_session(self, isbn_list):
        """
        Call this with all the isbns a single member has checked out
        (e.g. over one session/visit) to build edges between books that
        tend to be borrowed together.
        """
        for i, isbn_a in enumerate(isbn_list):
            for isbn_b in isbn_list[i + 1:]:
                self.adj[isbn_a].add(isbn_b)
                self.adj[isbn_b].add(isbn_a)

    def recommend_bfs(self, isbn, depth=2, limit=5):
        """
        BFS out from `isbn` up to `depth` hops, returning nearby co-borrowed
        books as recommendations (closer books are more strongly related).
        """
        visited = {isbn}
        queue = deque([(isbn, 0)])
        recs = []
        while queue and len(recs) < limit:
            node, d = queue.popleft()
            if d >= depth:
                continue
            for neighbor in self.adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    recs.append(neighbor)
                    queue.append((neighbor, d + 1))
                    if len(recs) >= limit:
                        break
        return recs

    def recommend_dfs(self, isbn, depth=2, limit=5):
        """DFS variant of the same idea, for comparison in your report."""
        visited = {isbn}
        recs = []

        def dfs(node, d):
            if d >= depth or len(recs) >= limit:
                return
            for neighbor in self.adj[node]:
                if neighbor not in visited and len(recs) < limit:
                    visited.add(neighbor)
                    recs.append(neighbor)
                    dfs(neighbor, d + 1)

        dfs(isbn, 0)
        return recs

    def __repr__(self):
        return f"CoBorrowGraph({dict(self.adj)})"
