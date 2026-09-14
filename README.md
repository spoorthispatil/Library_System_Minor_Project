# Library Management System — DSA Project (Python)

A console-based library management system built to showcase core data
structures and algorithms rather than a production storage layer.

## How to run

```bash
python main.py
```

This runs a full demo: seeding sample books/members, then exercising every
feature (catalog lookup, sorting comparison, binary search, issuing/returning
books, undo, genre browsing, recommendations, and the DP fine optimizer).

## Project structure

```
library_system/
├── models.py           # Book, Member, Transaction data classes
├── catalog.py           # Hash map storage + bubble/merge/quick/heap/counting sort + binary search
├── linked_list.py        # Singly linked list for per-member borrowing history
├── stack_ops.py           # Stack-based undo for issue/return actions
├── queue_waitlist.py       # FIFO queue for book reservations
├── genre_tree.py            # Tree of genres/subgenres + recursive DFS browsing
├── graph.py                  # Co-borrow graph + BFS/DFS recommendations
├── dp_fines.py                 # 0/1 knapsack DP for optimal fine-saving return plans
├── library.py                   # Orchestrator class wiring everything together
├── main.py                       # CLI demo entry point
└── README.md
```

## DSA concept → feature mapping

| Data Structure / Algorithm | Where it's used |
|---|---|
| Hash Map (dict) | O(1) book lookup by ISBN, grouping by author |
| Linked List | Each member's borrowing history (`linked_list.py`) |
| Stack | Undo last issue/return action (`stack_ops.py`) |
| Queue | FIFO waitlist when a book is unavailable (`queue_waitlist.py`) |
| Tree + DFS | Genre/subgenre hierarchy and recursive browsing (`genre_tree.py`) |
| Graph + BFS/DFS | "Related books" recommendations from co-borrow history (`graph.py`) |
| Sorting (bubble, merge, quick, heap, counting) | Catalog sorting, with a benchmark comparing all four (`catalog.py`) |
| Binary Search | Fast title lookup once the catalog is sorted (`catalog.py`) |
| Recursion | Merge sort, quicksort, DFS traversals, undo backtracking all use recursion |
| Dynamic Programming | 0/1 knapsack to choose which overdue books to prioritize returning within a limited grace-day budget (`dp_fines.py`) |

## Extending it

- Swap the in-memory dicts in `Catalog` for a real database if you want persistence.
- Add a `Trie` module for title/author autocomplete if your course covers Tries.
- Add unit tests per module (`test_catalog.py`, `test_graph.py`, etc.) — the
  functions are all pure/stateless where possible, which makes them easy to test.
- For the report, use `Catalog.benchmark_sorts()` on a larger randomly generated
  book list (hundreds/thousands of entries) to get more meaningful timing
  differences between the sorting algorithms.
