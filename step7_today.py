"""Step 7. The same tools today: a neuron that learns by squares, and bell noise that hides a picture."""
import math, random
from save import save
from step3_line import DAYS, LAT, fit_line, line_squares

def train_neuron(ts, ys, steps=2000, rate=0.5):
    """One neuron, y = weight * t + bias. Lower the average squared miss a little, again and again."""
    scale = max(ts)
    xs = [t / scale for t in ts]
    weight, bias, log = 0.0, 0.0, []
    for step in range(steps + 1):
        miss = [weight * x + bias - y for x, y in zip(xs, ys)]
        if step in (0, 10, 100, 1000, steps):
            log.append((step, weight / scale, bias, sum(m * m for m in miss)))
        weight -= rate * 2 * sum(m * x for m, x in zip(miss, xs)) / len(xs)
        bias -= rate * 2 * sum(miss) / len(xs)
    return weight / scale, bias, log

# Diffusion models train on pictures drowned in bell noise, a little more at each of 1,000 steps.
STEPS = 1000
BETAS = [1e-4 + (0.02 - 1e-4) * i / (STEPS - 1) for i in range(STEPS)]      # the 2020 schedule

def signal_left(step):
    keep = 1.0
    for beta in BETAS[:step]:
        keep *= 1 - beta
    return math.sqrt(keep)

def noised(picture, step, rnd):
    s = signal_left(step)
    return [s * p + math.sqrt(1 - s * s) * rnd.gauss(0, 1) for p in picture]

def alike(u, v):
    """Correlation: 1 = same shape, 0 = nothing in common."""
    mu, mv = sum(u) / len(u), sum(v) / len(v)
    top = sum((a - mu) * (b - mv) for a, b in zip(u, v))
    return top / math.sqrt(sum((a - mu) ** 2 for a in u) * sum((b - mv) ** 2 for b in v))

PICTURE = [math.sin(i / 32 * 2 * math.pi) * 1.4 for i in range(256)]       # one row of a "picture"

if __name__ == "__main__":
    slope, start = fit_line(DAYS, LAT)
    w, b, log = train_neuron(DAYS, LAT)
    for step, lw, lb, sq in log:
        print("step %5d  slope %.5f  start %.4f  sum of squares %.4e" % (step, lw, lb, sq))
    print("formula from step 3:   slope %.5f  start %.4f  sum of squares %.4e" % (slope, start, line_squares(slope, start, DAYS, LAT)))
    rnd = random.Random(2020)
    rows = []
    for step in (0, 100, 250, 500, 1000):
        row = noised(PICTURE, step, rnd)
        rows.append([step, signal_left(step), alike(PICTURE, row), [round(v, 3) for v in row]])
        print("noise step %4d: signal left %.3f, still alike %.2f" % (step, rows[-1][1], rows[-1][2]))
    save(7, log=log, formula=[slope, start, line_squares(slope, start, DAYS, LAT)], rows=rows)
