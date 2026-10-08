#!/bin/bash
# Runs the seven steps, then the checks. About 40 seconds on a laptop; nothing to install.
set -e
cd "$(dirname "$0")"
for step in step1_sum step2_sky step3_line step4_bell step5_elim step6_orbit step7_today; do
  echo
  echo "=== $step.py"
  python3 $step.py
done
echo
python3 tests.py
