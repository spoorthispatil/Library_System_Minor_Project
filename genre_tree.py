"""
Tree structure for browsing books by genre/subgenre, with recursive DFS
traversal to list books under any node. Maps to the Tree Traversal / DFS
sessions.
"""


class GenreNode:
    def __init__(self, name):
        self.name = name
        self.children = {}   # genre name -> GenreNode
        self.books = []      # books directly under this exact node

    def __repr__(self):
        return f"GenreNode({self.name}, books={len(self.books)}, children={list(self.children.keys())})"


class GenreTree:
    def __init__(self):
        self.root = GenreNode("All")

    def add_book(self, genre_path, book):
        """
        genre_path: list like ["Fiction", "Fantasy"].
        Creates intermediate nodes as needed.
        """
        node = self.root
        for genre in genre_path:
            node = node.children.setdefault(genre, GenreNode(genre))
        node.books.append(book)

    def find_node(self, genre_path):
        node = self.root
        for genre in genre_path:
            if genre not in node.children:
                return None
            node = node.children[genre]
        return node

    def dfs_list_books(self, genre_path=None):
        """
        Recursively (DFS) collects every book at or below the given genre path.
        If genre_path is None, lists the entire catalog via the tree.
        """
        start = self.find_node(genre_path) if genre_path else self.root
        if start is None:
            return []
        return self._dfs(start)

    def _dfs(self, node):
        result = list(node.books)
        for child in node.children.values():
            result.extend(self._dfs(child))
        return result

    def print_tree(self, node=None, depth=0):
        """Simple recursive printer for visualizing the genre hierarchy."""
        node = node or self.root
        print("  " * depth + f"- {node.name} ({len(node.books)} books)")
        for child in node.children.values():
            self.print_tree(child, depth + 1)
