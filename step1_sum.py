"""Step 1. The schoolroom sum: add 1 + 2 + ... + 100 without adding a hundred numbers."""
import time
from save import save

N = 100
slow = 0
for number in range(1, N + 1):
    slow += number

# Write the row forwards and backwards. Every column adds up to the same thing.
pairs = [(k, N + 1 - k) for k in range(1, N // 2 + 1)]
each = pairs[0][0] + pairs[0][1]
fast = len(pairs) * each

def formula(n):
    return n * (n + 1) // 2

if __name__ == "__main__":
    print("adding one by one:", slow)
    print("first pairs:", pairs[:3], "... last pair:", pairs[-1])
    print(len(pairs), "pairs, each", each, "->", fast)
    big = 10_000_000
    t = time.time(); loop = sum(range(1, big + 1)); t_loop = time.time() - t
    print("1 to", big, "one by one:", loop, "in %.2f s" % t_loop)
    print("1 to", big, "by the pairing:", formula(big), "in one multiplication")
    save(1, n=N, slow=slow, pairs=pairs, each=each, fast=fast, big=big, loop=loop, quick=formula(big), seconds=t_loop)
