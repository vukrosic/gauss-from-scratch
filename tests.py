"""Checks. run_all.sh runs them last, on the numbers the seven steps saved in runs/."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
r = {i: json.load(open(os.path.join(HERE, 'runs', 'step%d.json' % i))) for i in range(1, 8)}

# 1. the loop, the pairing and the formula agree
assert r[1]['slow'] == r[1]['fast'] == 5050 and r[1]['loop'] == r[1]['quick']
assert all(a + b == r[1]['each'] for a, b in r[1]['pairs'])

# 2. 22 nights inside 41 days; every error is small; the planet is far from where it was
assert len(r[2]['obs']) == 22 and r[2]['obs'][-1][0] == 41
assert all(abs(v) < 15 for pair in r[2]['errors'] for v in pair)          # arcseconds
assert r[2]['travel'] > 100                                                # degrees

# 3. the average has the smallest sum of squares; so does the fitted line; straight lines fail
sums = [s for g, s in r[3]['table']]
assert min(sums) == sums[2] and all(s >= sums[2] for g, s in r[3]['bowl'])
assert all(w > r[3]['best'] for w in r[3]['worse'])
assert r[3]['miss'] > 45

# 4. added-up small errors follow the bell; smallest squares = largest chance
assert all(abs(c - b) < 0.03 * b + 4 * b ** 0.5 for c, b in zip(r[4]['bins'][2:18], r[4]['bell'][2:18]))
assert abs(r[4]['within'][0] - 68.3) < 1 and abs(r[4]['within'][1] - 95.4) < 1
assert max(r[4]['table'], key=lambda row: row[2])[0] == min(r[4]['table'], key=lambda row: row[1])[0]

# 5. the 2,000-year-old answer, exactly; six unknowns to rounding error
assert r[5]['answer'] == ['37/4', '17/4', '11/4'] and r[5]['worst'] < 1e-12

# 6. each better model misses by less; the ellipse lands inside one Moon width (0.5 degrees)
assert r[6]['line']['miss'] > r[6]['circle']['miss'] > r[6]['ellipse']['miss']
assert r[6]['ellipse']['miss'] < 0.5 and r[6]['inside'] > 150
assert abs(r[6]['ellipse']['size'] - r[6]['truth']['size']) < 0.05

# 7. the trained neuron ends on the line from the formula; 1,000 noise steps leave almost nothing
last = r[7]['log'][-1]
assert abs(last[1] - r[7]['formula'][0]) < 1e-6 and abs(last[2] - r[7]['formula'][1]) < 1e-5
assert r[7]['rows'][0][1] == 1.0 and r[7]['rows'][-1][1] < 0.01
print("all checks passed")
