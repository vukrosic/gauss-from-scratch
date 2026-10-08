"""Step 5. Elimination: many equations, many unknowns, solved one column at a time."""
from fractions import Fraction
import random
from save import save

# Problem 1, chapter 8 of the Nine Chapters (China, about 2,000 years ago): three grades of grain.
GRAIN = [[3, 2, 1], [2, 3, 1], [1, 2, 3]]
YIELD = [39, 34, 26]

def solve(A, b, log=None):
    """Solve A x = b. Clear one column at a time, then work back up from the last row."""
    n = len(b)
    rows = [list(A[i]) + [b[i]] for i in range(n)]
    for col in range(n):
        big = max(range(col, n), key=lambda r: abs(rows[r][col]))    # the safest row to divide by
        rows[col], rows[big] = rows[big], rows[col]
        for r in range(col + 1, n):
            factor = rows[r][col] / rows[col][col]
            for k in range(col, n + 1):
                rows[r][k] -= factor * rows[col][k]
        if log is not None:
            log.append([row[:] for row in rows])      # keep a copy of the table after each column
    x = [0] * n
    for r in range(n - 1, -1, -1):
        x[r] = (rows[r][n] - sum(rows[r][k] * x[k] for k in range(r + 1, n))) / rows[r][r]
    return x

if __name__ == "__main__":
    exact = [[Fraction(v) for v in row] for row in GRAIN]
    log = []
    answer = solve(exact, [Fraction(v) for v in YIELD], log)
    for col, rows in enumerate(log):
        print("after column", col + 1)
        for row in rows:
            print("   ", "  ".join("%6s" % v for v in row))
    print("one bundle of each grade gives:", ", ".join(str(v) for v in answer), "=", [float(v) for v in answer])
    for row, total in zip(GRAIN, YIELD):
        print("  check", row, "->", sum(c * v for c, v in zip(row, answer)), "should be", total)
    rnd = random.Random(8)
    n = 6
    A = [[rnd.uniform(-5, 5) for _ in range(n)] for _ in range(n)]
    truth = [rnd.uniform(-5, 5) for _ in range(n)]
    b = [sum(A[i][j] * truth[j] for j in range(n)) for i in range(n)]
    found = solve(A, b)
    worst = max(abs(f - t) for f, t in zip(found, truth))
    print("six equations, six unknowns: largest error %.1e" % worst)
    save(5, grain=GRAIN, total=YIELD, tables=[[[str(v) for v in row] for row in rows] for rows in log],
         answer=[str(v) for v in answer], decimal=[float(v) for v in answer], worst=worst)
