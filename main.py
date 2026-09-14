"""
CLI demo for the Library Management System.
Run with: python main.py

This script sets up sample data and walks through every feature so you
can see (and screen-record, if needed) each data structure in action.
"""

from library import Library
from models import Book
from dp_fines import max_fine_saved
from catalog import Catalog


def print_header(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def seed_data(lib: Library):
    books = [
        Book("001", "The Hobbit", "J.R.R. Tolkien", ["Fiction", "Fantasy"], copies=2),
        Book("002", "The Fellowship of the Ring", "J.R.R. Tolkien", ["Fiction", "Fantasy"], copies=1),
        Book("003", "Dune", "Frank Herbert", ["Fiction", "Sci-Fi"], copies=1),
        Book("004", "Foundation", "Isaac Asimov", ["Fiction", "Sci-Fi"], copies=2),
        Book("005", "A Brief History of Time", "Stephen Hawking", ["Non-Fiction", "Science"], copies=1),
        Book("006", "Sapiens", "Yuval Noah Harari", ["Non-Fiction", "History"], copies=1),
    ]
    for b in books:
        lib.add_book(b)

    for member_id, name in [("M1", "Asha"), ("M2", "Ravi"), ("M3", "Kiran")]:
        lib.register_member(member_id, name)


def main():
    lib = Library()
    seed_data(lib)

    print_header("1. CATALOG + HASH MAP LOOKUP")
    print(lib.catalog.get_book("001"))
    print(lib.catalog.books_by_author_name("J.R.R. Tolkien"))

    print_header("2. SORTING ALGORITHM COMPARISON (bubble/merge/quick/heap)")
    timings = Catalog.benchmark_sorts(lib.catalog.all_books(), key_func=lambda b: b.title)
    for name, t in timings.items():
        print(f"  {name:12s}: {t:.8f} sec")

    print_header("3. BINARY SEARCH ON SORTED CATALOG")
    result = lib.search_by_title("Dune")
    print(f"  Found: {result}")

    print_header("4. ISSUE / RETURN BOOKS (with linked-list history + fines)")
    print(" ", lib.issue_book("M1", "001"))
    print(" ", lib.issue_book("M2", "002"))
    print(" ", lib.issue_book("M3", "002"))  # triggers waitlist (only 1 copy)
    print("  M1 history:", lib.histories["M1"].to_list())
    print(" ", lib.return_book("M2", "002"))  # should auto-issue to M3 from waitlist

    print_header("5. UNDO (STACK)")
    print(" ", lib.issue_book("M1", "003"))
    print(" ", lib.undo_last_action("M1"))
    print("  Dune copies after undo:", lib.catalog.get_book("003").available_copies)

    print_header("6. GENRE TREE + DFS BROWSE")
    lib.genre_tree.print_tree()
    print("  All Fantasy books:", lib.browse_genre(["Fiction", "Fantasy"]))

    print_header("7. RECOMMENDATION GRAPH (BFS over co-borrowed books)")
    lib.record_session_borrow(["001", "002"])   # Hobbit + Fellowship borrowed together
    lib.record_session_borrow(["003", "004"])   # Dune + Foundation borrowed together
    lib.record_session_borrow(["002", "004"])   # cross-link
    print("  Recommended alongside 'The Hobbit' (001):", lib.recommend_related("001"))

    print_header("8. DYNAMIC PROGRAMMING: OPTIMAL FINE-SAVING RETURN PLAN")
    overdue = [
        {"isbn": "010", "days_cost": 2, "fine_saved": 20},
        {"isbn": "011", "days_cost": 3, "fine_saved": 30},
        {"isbn": "012", "days_cost": 4, "fine_saved": 50},
        {"isbn": "013", "days_cost": 1, "fine_saved": 10},
    ]
    best_value, chosen = max_fine_saved(overdue, grace_days=5)
    print(f"  With 5 grace-days budget: save ${best_value} by prioritizing {chosen}")


if __name__ == "__main__":
    main()
