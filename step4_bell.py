"""Step 4. Why squares? Many small accidents add up to a bell, and the bell punishes squares."""
import math, random
from save import save
from step3_line import READINGS, sum_squares

NUDGES = 30          # small accidents inside one measurement: air, eye, clock, screw ...
TRIES = 100_000

def one_error(rnd):
    return sum(rnd.uniform(-1, 1) for _ in range(NUDGES))

def bell(x, spread):
    """Height of the bell curve at x."""
    return math.exp(-x * x / (2 * spread * spread)) / (spread * math.sqrt(2 * math.pi))

def chance(guess, values=READINGS, spread=0.02):
    """Chance of seeing these readings if the true value were `guess` and errors follow the bell."""
    p = 1.0
    for v in values:
        p *= bell(v - guess, spread)
    return p

rnd = random.Random(1809)
ERRORS = [one_error(rnd) for _ in range(TRIES)]
SPREAD = math.sqrt(sum(e * e for e in ERRORS) / TRIES)
BINS = [sum(1 for e in ERRORS if b <= e < b + 1) for b in range(-10, 10)]

if __name__ == "__main__":
    print(TRIES, "errors, each the sum of", NUDGES, "small nudges. spread %.2f" % SPREAD)
    for b, count in zip(range(-10, 10), BINS):
        if -8 <= b < 8:
            print("%4d to %3d  %6d  bell says %6.0f  %s" % (b, b + 1, count, TRIES * bell(b + 0.5, SPREAD), "#" * (count // 400)))
    within = [100 * sum(1 for e in ERRORS if abs(e) < k * SPREAD) / TRIES for k in (1, 2, 3)]
    for k in (1, 2, 3):
        print("within %d spread: %.1f%%" % (k, within[k - 1]))
    top = chance(sum(READINGS) / len(READINGS))
    for guess in (52.92, 52.93, 52.94, 52.95, 52.96):
        print("guess %.2f  sum of squares %.4f  chance %.3f of the best" % (guess, sum_squares(guess), chance(guess) / top))
    walks = [[round(rnd.uniform(-1, 1), 3) for _ in range(NUDGES)] for _ in range(8)]      # eight errors, nudge by nudge
    save(4, nudges=NUDGES, tries=TRIES, spread=SPREAD, bins=BINS, bell=[TRIES * bell(b + 0.5, SPREAD) for b in range(-10, 10)],
         within=within, walks=walks, table=[[g, sum_squares(g), chance(g) / top] for g in (52.92, 52.93, 52.94, 52.95, 52.96)],
         hill=[[52.9 + i / 500, chance(52.9 + i / 500) / top] for i in range(41)])
