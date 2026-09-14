"""
Dynamic Programming module.

Scenario: a member has several overdue books, each with a "fine saved" value
if returned soon, and a "days needed" cost (how long returning/processing
that book realistically takes, or how many grace days it would consume).
Given a limited number of grace days, choose the subset of books to
prioritize returning that maximizes total fine saved -- a classic 0/1
knapsack, directly reusing the DP session's techniques.
"""


def max_fine_saved(overdue_books, grace_days):
    """
    overdue_books: list of dicts like
        {"isbn": "123", "days_cost": 2, "fine_saved": 15}
    grace_days: total budget of days available across all prioritized returns.

    Returns (best_value, chosen_isbns) via 0/1 knapsack DP.
    """
    n = len(overdue_books)
    # dp[i][w] = max fine saved using first i books with w grace days budget
    dp = [[0] * (grace_days + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        book = overdue_books[i - 1]
        cost = book["days_cost"]
        value = book["fine_saved"]
        for w in range(grace_days + 1):
            dp[i][w] = dp[i - 1][w]  # don't take this book
            if cost <= w:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - cost] + value)

    # backtrack to find which books were chosen
    chosen = []
    w = grace_days
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            book = overdue_books[i - 1]
            chosen.append(book["isbn"])
            w -= book["days_cost"]

    chosen.reverse()
    return dp[n][grace_days], chosen


def calculate_fine(days_late, rate_per_day=5, max_fine=100):
    """Simple fine calculation, capped at max_fine."""
    return min(days_late * rate_per_day, max_fine)
