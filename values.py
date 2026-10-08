"""Film data only (not part of the public repo): the steps' saved numbers.  python3 values.py -> ../src/values.json"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
v = {}
for i in range(1, 8):
    with open(os.path.join(HERE, 'runs', 'step%d.json' % i)) as f:
        v['step%d' % i] = json.load(f)
with open(os.path.join(HERE, '..', 'src', 'values.json'), 'w') as f:
    json.dump(v, f)
print({k: sorted(x) for k, x in v.items()})
