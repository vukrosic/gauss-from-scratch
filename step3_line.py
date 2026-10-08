"""Step 3. Least squares: which single value, and which straight line, fits wrong measurements best?"""
from step2_sky import OBS, DEG, RETURN, PLANET, look, apart
from save import save

READINGS = [52.94, 52.91, 52.97, 52.93, 52.95]       # five readings of one angle, in degrees

def sum_squares(guess, values=READINGS):
    return sum((v - guess) ** 2 for v in values)

def fit_line(ts, ys):
    """The line y = slope * t + start with the smallest sum of squared misses."""
    n, st, sy = len(ts), sum(ts), sum(ys)
    stt, sty = sum(t * t for t in ts), sum(t * y for t, y in zip(ts, ys))
    slope = (n * sty - st * sy) / (n * stt - st * st)        # two equations, two unknowns
    return slope, (sy - slope * st) / n

def line_squares(slope, start, ts, ys):
    return sum((slope * t + start - y) ** 2 for t, y in zip(ts, ys))

DAYS = [o[0] for o in OBS]
LON = [o[1] / DEG for o in OBS]
LAT = [o[2] / DEG for o in OBS]
LAT_LINE = fit_line(DAYS, LAT)
LON_LINE = fit_line(DAYS, LON)

def line_guess(day):
    return (LON_LINE[0] * day + LON_LINE[1]) * DEG, (LAT_LINE[0] * day + LAT_LINE[1]) * DEG

if __name__ == "__main__":
    mean = sum(READINGS) / len(READINGS)
    for guess in (52.92, 52.93, mean, 52.95, 52.96):
        print("guess %.3f  sum of squares %.5f" % (guess, sum_squares(guess)))
    print("the average is %.3f" % mean)
    slope, start = LAT_LINE
    best = line_squares(slope, start, DAYS, LAT)
    print("latitude line: %.5f degrees per day, start %.4f, sum of squares %.3e" % (slope, start, best))
    for factor in (0.98, 1.02):
        print("  slope x %.2f -> sum of squares %.3e" % (factor, line_squares(slope * factor, start, DAYS, LAT)))
    guess = line_guess(RETURN)
    print("straight lines say day %d: longitude %.1f, latitude %.1f" % (RETURN, guess[0] / DEG, guess[1] / DEG))
    print("miss: %.1f degrees" % apart(guess, look(PLANET, RETURN)))
    save(3, readings=READINGS, mean=mean, table=[[g, sum_squares(g)] for g in (52.92, 52.93, mean, 52.95, 52.96)],
         bowl=[[52.9 + i / 500, sum_squares(52.9 + i / 500)] for i in range(41)], days=DAYS, lat=LAT, lon=LON,
         lat_line=LAT_LINE, lon_line=LON_LINE, best=best,
         worse=[line_squares(slope * factor, start, DAYS, LAT) for factor in (0.98, 1.02)],
         guess=[guess[0] / DEG, guess[1] / DEG], miss=apart(guess, look(PLANET, RETURN)))
