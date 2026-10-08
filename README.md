# Gauss from scratch

Code for the video **Become Carl Friedrich Gauss in 20 Minutes**.
In 1801 a new small planet, Ceres, was watched for 41 days and then lost behind the Sun. Gauss, 24 years old, said where it would come back.
These seven small programs rebuild the tools he used: 390 lines of Python 3, standard library only, nothing to install.

```bash
python3 tests.py      # checks every step
./run_all.sh          # runs all seven, about 40 seconds; expected output is in demo-output.txt
```

| File | Idea | What the run shows |
| --- | --- | --- |
| `step1_sum.py` | The schoolboy's sum | 1 + 2 + … + 100 as 50 pairs of 101 = 5,050. The same trick gives 1 + … + 10,000,000 = 50,000,005,000,000 without a loop. |
| `step2_sky.py` | A model sky | The Earth, one small planet, 22 nights of measurements inside 41 days, each wrong by about 3 arcseconds. In 41 days the planet covers 2.4% of one lap. If you guess it stood still, you miss it on day 340 by 116° (232 Moon widths). |
| `step3_line.py` | Least squares | Five readings of one angle: the value with the smallest sum of squared misses is the average, 52.94°. A straight line through the 22 nights (slope 0.06179° per day) misses day 340 by 94° (188 Moons). |
| `step4_bell.py` | Why squares: the bell | 30 small accidents per measurement, 100,000 measurements: the totals pile up as a bell. 68.0% fall within one spread, 95.5% within two, 99.8% within three. On a bell, the most likely answer is the one with the smallest squares. |
| `step5_elim.py` | Elimination | Problem 1 of chapter 8 of the *Nine Chapters* (three grades of grain) solved in exact fractions: 37/4, 17/4, 11/4. Then 6 equations with 6 unknowns, worst error 9e-16. |
| `step6_orbit.py` | The orbit | A circle (4 numbers) stops after 6 jumps with a leftover of 38 arcseconds and misses day 340 by 10.5° (21 Moons). An ellipse (6 numbers) takes 49 jumps, leaves 2.9 arcseconds (the size of the measurement errors) and misses by 0.32°: 0.6 of a Moon. With 200 fresh sets of errors, 187 land within one Moon; the worst is 1.9 Moons. From 60 blind first guesses, 49 end on the same orbit and 11 get stuck with a leftover of 1,700 arcseconds or more. |
| `step7_today.py` | The same tools today | A neuron with two numbers, trained by gradient descent on the same 22 nights, reaches the least-squares line to five digits in 1,000 steps. One row of a picture with bell noise added in 1,000 steps (linear schedule of Ho, Jain and Abbeel, 2020): 95% of the picture left at step 100, 28% at step 500, 0.6% at step 1,000. |

`save.py` writes each step's numbers to `runs/`; `values.py` collects them for the animation, so every number on screen comes from these runs.

## What this is not

- The sky is a model. The 22 nights are made by `step2_sky.py`, not copied from Piazzi's notebook.
- The planet feels only the Sun. The real Ceres is also pulled by Jupiter and the other planets.
- The fit is not the method of Gauss. He started from three observations and improved the orbit from there; `step6_orbit.py` fits all 22 nights at once by least squares. Whether Gauss used least squares on Ceres itself is not certain; he said he had known the rule since 1795, and printed it in 1809, four years after Legendre.

## One experiment not run

`step6_orbit.py` uses 22 nights. Gauss started from three. Take nights away in `step2_sky.py` and watch the miss on day 340: how few are enough to stay within one Moon?

MIT licence.
