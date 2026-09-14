"""
Catalog: array/hash-map based book storage, plus classic sorting algorithms
(bubble, merge, quick, heap) and binary search over the catalog.

Keeping several sort implementations side by side lets you benchmark and
compare them directly, which maps to the Sorting Algorithms sessions.
"""

import heapq
import time


class Catalog:
    def __init__(self):
        self.books_by_isbn = {}      # O(1) lookup by ISBN
        self.books_by_author = {}    # author -> list of isbns

    # ---------- basic CRUD ----------

    def add_book(self, book):
        self.books_by_isbn[book.isbn] = book
        self.books_by_author.setdefault(book.author, []).append(book.isbn)

    def remove_book(self, isbn):
        book = self.books_by_isbn.pop(isbn, None)
        if book and book.author in self.books_by_author:
            if isbn in self.books_by_author[book.author]:
                self.books_by_author[book.author].remove(isbn)
        return book

    def get_book(self, isbn):
        return self.books_by_isbn.get(isbn)

    def all_books(self):
        return list(self.books_by_isbn.values())

    def books_by_author_name(self, author):
        return [self.books_by_isbn[isbn] for isbn in self.books_by_author.get(author, [])]

    # ---------- sorting algorithms (operate on a list of Book, by key_func) ----------

    @staticmethod
    def bubble_sort(books, key_func=lambda b: b.title):
        arr = books[:]
        n = len(arr)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if key_func(arr[j]) > key_func(arr[j + 1]):
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
            if not swapped:
                break
        return arr

    @staticmethod
    def merge_sort(books, key_func=lambda b: b.title):
        arr = books[:]
        if len(arr) <= 1:
            return arr

        def merge(left, right):
            result = []
            i = j = 0
            while i < len(left) and j < len(right):
                if key_func(left[i]) <= key_func(right[j]):
                    result.append(left[i]); i += 1
                else:
                    result.append(right[j]); j += 1
            result.extend(left[i:])
            result.extend(right[j:])
            return result

        def sort(lst):
            if len(lst) <= 1:
                return lst
            mid = len(lst) // 2
            return merge(sort(lst[:mid]), sort(lst[mid:]))

        return sort(arr)

    @staticmethod
    def quick_sort(books, key_func=lambda b: b.title):
        arr = books[:]

        def sort(lst):
            if len(lst) <= 1:
                return lst
            pivot = key_func(lst[len(lst) // 2])
            left = [x for x in lst if key_func(x) < pivot]
            mid = [x for x in lst if key_func(x) == pivot]
            right = [x for x in lst if key_func(x) > pivot]
            return sort(left) + mid + sort(right)

        return sort(arr)

    @staticmethod
    def heap_sort(books, key_func=lambda b: b.title):
        arr = books[:]
        heap = [(key_func(b), i, b) for i, b in enumerate(arr)]
        heapq.heapify(heap)
        return [heapq.heappop(heap)[2] for _ in range(len(heap))]

    @staticmethod
    def counting_sort_by_year(books, key_func):
        """
        Counting sort works only on integer keys within a known range,
        e.g. sorting by publication year. key_func should return an int.
        """
        arr = books[:]
        if not arr:
            return arr
        keys = [key_func(b) for b in arr]
        min_k, max_k = min(keys), max(keys)
        buckets = [[] for _ in range(max_k - min_k + 1)]
        for b in arr:
            buckets[key_func(b) - min_k].append(b)
        result = []
        for bucket in buckets:
            result.extend(bucket)
        return result

    # ---------- searching ----------

    @staticmethod
    def binary_search_by_title(sorted_books, target_title):
        """
        Requires sorted_books to already be sorted by title (see merge_sort/quick_sort above).
        Returns the Book or None.
        """
        lo, hi = 0, len(sorted_books) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            title = sorted_books[mid].title
            if title == target_title:
                return sorted_books[mid]
            elif title < target_title:
                lo = mid + 1
            else:
                hi = mid - 1
        return None

    # ---------- benchmarking helper ----------

    @staticmethod
    def benchmark_sorts(books, key_func=lambda b: b.title):
        """
        Runs each sort implementation on the same dataset and returns timings (seconds).
        Useful for the report/demo comparing sorting algorithms.
        """
        results = {}
        algorithms = {
            "bubble_sort": Catalog.bubble_sort,
            "merge_sort": Catalog.merge_sort,
            "quick_sort": Catalog.quick_sort,
            "heap_sort": Catalog.heap_sort,
        }
        for name, func in algorithms.items():
            start = time.perf_counter()
            func(books, key_func)
            results[name] = time.perf_counter() - start
        return results
