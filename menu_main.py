"""
Interactive, menu-driven CLI for the Library Management System.
Run with: python menu_main.py

Unlike main.py (which auto-runs a scripted demo), this lets you drive
the system yourself: add books/members, issue/return, browse, search,
undo, get recommendations, etc.
"""

from library import Library
from models import Book
from catalog import Catalog
from dp_fines import max_fine_saved


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


MENU = """
LIBRARY MANAGEMENT SYSTEM
--------------------------------
 1. View full catalog
 2. Search book by title
 3. Browse by genre
 4. Add a new book
 5. Register a new member
 6. Issue a book to a member
 7. Return a book
 8. Undo my last action
 9. View a member's borrow history
10. Recommend books related to a title
11. Compare sorting algorithms
12. Optimal fine-saving return plan (DP)
13. List members
 0. Exit
--------------------------------
"""


def input_nonempty(prompt):
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print("  (this can't be empty, try again)")


def choose_member(lib):
    mid = input_nonempty("Member ID: ")
    if mid not in lib.members:
        print(f"  No member with ID '{mid}'. Use option 5 to register one first.")
        return None
    return mid


def choose_book(lib):
    isbn = input_nonempty("ISBN: ")
    book = lib.catalog.get_book(isbn)
    if not book:
        print(f"  No book with ISBN '{isbn}'.")
        return None
    return isbn


def action_view_catalog(lib):
    print_header("CATALOG")
    books = lib.sorted_catalog_by_title()
    if not books:
        print("  (catalog is empty)")
    for b in books:
        print(f"  {b}")


def action_search(lib):
    print_header("SEARCH BY TITLE")
    title = input_nonempty("Title (exact match): ")
    result = lib.search_by_title(title)
    print(f"  Found: {result}" if result else "  Not found.")


def action_browse_genre(lib):
    print_header("GENRE TREE")
    lib.genre_tree.print_tree()
    path_str = input("Enter genre path to browse (e.g. Fiction/Fantasy), or blank for all: ").strip()
    genre_path = [g.strip() for g in path_str.split("/") if g.strip()] or None
    results = lib.browse_genre(genre_path)
    print(f"\n  {len(results)} book(s):")
    for b in results:
        print(f"    {b}")


def action_add_book(lib):
    print_header("ADD A NEW BOOK")
    isbn = input_nonempty("ISBN: ")
    if lib.catalog.get_book(isbn):
        print("  A book with that ISBN already exists.")
        return
    title = input_nonempty("Title: ")
    author = input_nonempty("Author: ")
    path_str = input_nonempty("Genre path (e.g. Fiction/Fantasy): ")
    genre_path = [g.strip() for g in path_str.split("/") if g.strip()]
    copies_str = input("Number of copies [1]: ").strip()
    copies = int(copies_str) if copies_str.isdigit() else 1
    lib.add_book(Book(isbn, title, author, genre_path, copies=copies))
    print(f"  Added: {lib.catalog.get_book(isbn)}")


def action_register_member(lib):
    print_header("REGISTER A NEW MEMBER")
    mid = input_nonempty("Member ID: ")
    if mid in lib.members:
        print("  A member with that ID already exists.")
        return
    name = input_nonempty("Name: ")
    lib.register_member(mid, name)
    print(f"  Registered: {lib.members[mid]}")


def action_issue(lib):
    print_header("ISSUE A BOOK")
    mid = choose_member(lib)
    if not mid:
        return
    isbn = choose_book(lib)
    if not isbn:
        return
    print(" ", lib.issue_book(mid, isbn))


def action_return(lib):
    print_header("RETURN A BOOK")
    mid = choose_member(lib)
    if not mid:
        return
    isbn = choose_book(lib)
    if not isbn:
        return
    print(" ", lib.return_book(mid, isbn))


def action_undo(lib):
    print_header("UNDO LAST ACTION")
    mid = choose_member(lib)
    if not mid:
        return
    print(" ", lib.undo_last_action(mid))


def action_history(lib):
    print_header("BORROW HISTORY")
    mid = choose_member(lib)
    if not mid:
        return
    history = lib.histories[mid].to_list()
    if not history:
        print("  No transactions yet.")
    for txn in history:
        print(f"  {txn}")


def action_recommend(lib):
    print_header("RECOMMEND RELATED BOOKS")
    isbn = choose_book(lib)
    if not isbn:
        return
    recs = lib.recommend_related(isbn)
    if not recs:
        print("  No recommendations yet -- borrow some books together first "
              "(this builds from co-borrow history in this session).")
        return
    print(f"  Related to '{lib.catalog.get_book(isbn).title}':")
    for rec_isbn in recs:
        print(f"    {lib.catalog.get_book(rec_isbn)}")


def action_benchmark(lib):
    print_header("SORTING ALGORITHM COMPARISON")
    books = lib.catalog.all_books()
    if not books:
        print("  Catalog is empty -- nothing to sort.")
        return
    timings = Catalog.benchmark_sorts(books, key_func=lambda b: b.title)
    for name, t in timings.items():
        print(f"  {name:12s}: {t:.8f} sec")


def action_dp_fines(lib):
    print_header("OPTIMAL FINE-SAVING RETURN PLAN (0/1 KNAPSACK)")
    print("Enter overdue books one at a time. Leave ISBN blank to finish.")
    overdue = []
    while True:
        isbn = input(f"  Overdue book #{len(overdue) + 1} ISBN (blank to stop): ").strip()
        if not isbn:
            break
        try:
            days_cost = int(input("    Days cost to return/process: ").strip())
            fine_saved = int(input("    Fine saved if returned: ").strip())
        except ValueError:
            print("    Please enter whole numbers. Skipping this entry.")
            continue
        overdue.append({"isbn": isbn, "days_cost": days_cost, "fine_saved": fine_saved})

    if not overdue:
        print("  No overdue books entered.")
        return

    grace_str = input("Grace-day budget: ").strip()
    grace_days = int(grace_str) if grace_str.isdigit() else 0
    best_value, chosen = max_fine_saved(overdue, grace_days)
    print(f"\n  With {grace_days} grace-days: save ${best_value} by prioritizing {chosen}")


def action_list_members(lib):
    print_header("MEMBERS")
    if not lib.members:
        print("  (no members registered)")
    for m in lib.members.values():
        print(f"  {m}")


ACTIONS = {
    "1": action_view_catalog,
    "2": action_search,
    "3": action_browse_genre,
    "4": action_add_book,
    "5": action_register_member,
    "6": action_issue,
    "7": action_return,
    "8": action_undo,
    "9": action_history,
    "10": action_recommend,
    "11": action_benchmark,
    "12": action_dp_fines,
    "13": action_list_members,
}


def main():
    lib = Library()
    seed_data(lib)
    print("Welcome! Sample books and members (M1/Asha, M2/Ravi, M3/Kiran) are pre-loaded.")

    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        action = ACTIONS.get(choice)
        if not action:
            print("  Invalid option, try again.")
            continue
        try:
            action(lib)
        except Exception as e:
            print(f"  Something went wrong: {e}")


if __name__ == "__main__":
    main()
