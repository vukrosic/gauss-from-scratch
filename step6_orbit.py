"""Step 6. The hunt: fit an orbit to 41 days of measurements and say where the planet is on day 340."""
import math, random
from step2_sky import OBS, PLANET, RETURN, DEG, ARCSEC, look, apart, observe
from step3_line import line_guess
from step5_elim import solve
from save import save

def misses(orb, obs):
    """For every night: how far the orbit's prediction is from the measurement (two angles each)."""
    out = []
    for day, lon, lat in obs:
        p_lon, p_lat = look(orb, day)
        turn = (p_lon - lon + math.pi) % (2 * math.pi) - math.pi
        out += [turn * math.cos(lat), p_lat - lat]
    return out

def squares(orb, obs):
    return sum(m * m for m in misses(orb, obs))

def fit(obs, start, free, rounds=400, trail=None):
    """Least squares for a curved problem: pretend it is straight, solve, step, repeat."""
    orb, caution, done = list(start), 1e-3, 0
    for done in range(1, rounds + 1):
        base = misses(orb, obs)
        before = sum(m * m for m in base)
        slopes = []                                   # how every miss changes when one number is nudged
        for j in free:
            nudged = orb[:]; nudged[j] += 1e-6
            slopes.append([(m2 - m) / 1e-6 for m2, m in zip(misses(nudged, obs), base)])
        A = [[sum(p * q for p, q in zip(si, sj)) for sj in slopes] for si in slopes]
        b = [-sum(p * m for p, m in zip(si, base)) for si in slopes]
        while caution < 1e12:
            careful = [[A[i][j] * (1 + caution if i == j else 1) for j in range(len(free))] for i in range(len(free))]
            change = solve(careful, b)                # step 5: elimination
            trial = orb[:]
            for j, c in zip(free, change):
                trial[j] += c
            if 0.5 < trial[0] < 10 and math.hypot(trial[1], trial[2]) < 0.9 and squares(trial, obs) < before:
                break
            caution *= 10                             # worse? take a shorter, safer step
        else:
            return orb, done
        orb, caution = trial, caution / 5             # better? be bolder next time
        if trail is not None:
            trail.append(orb)
        if before - squares(orb, obs) < 1e-12 * before:
            break
    return orb, done

def leftover(orb, obs):
    """Typical miss that remains after the fit, in arcseconds."""
    return math.sqrt(squares(orb, obs) / (2 * len(obs))) / ARCSEC

START = [2.8, 0.0, 0.0, 10 * DEG, 80 * DEG, 50 * DEG]      # a rough first guess: a circle near 2.8

def hunt(obs, trail=None, start=START):
    circle, r1 = fit(obs, start, [0, 3, 4, 5], trail=trail)               # a circle: 4 numbers free
    ellipse, r2 = fit(obs, circle, [0, 1, 2, 3, 4, 5], trail=trail)       # an ellipse: all 6 free
    return circle, r1, ellipse, r2

if __name__ == "__main__":
    truth = look(PLANET, RETURN)
    print("straight lines: miss %.1f degrees" % apart(line_guess(RETURN), truth))
    trail = []
    circle, r1, ellipse, r2 = hunt(OBS, trail)
    print("circle:  size %.3f, leftover %.1f arcsec, %d rounds, miss %.2f degrees"
          % (circle[0], leftover(circle, OBS), r1, apart(look(circle, RETURN), truth)))
    print("ellipse: size %.3f, stretch %.4f, tilt %.2f, leftover %.1f arcsec, %d rounds, miss %.3f degrees"
          % (ellipse[0], math.hypot(ellipse[1], ellipse[2]), ellipse[3] / DEG, leftover(ellipse, OBS), r2,
             apart(look(ellipse, RETURN), truth)))
    print("truth:   size %.3f, stretch %.4f, tilt %.2f" % (PLANET[0], math.hypot(PLANET[1], PLANET[2]), PLANET[3] / DEG))
    runs = sorted(apart(look(hunt(observe(seed))[2], RETURN), truth) for seed in range(200))
    print("200 skies with different errors: half miss by less than %.2f, 9 in 10 by less than %.2f, worst %.2f degrees"
          % (runs[100], runs[180], runs[-1]))
    print("inside one Moon width (0.5 degrees): %d of 200" % sum(1 for r in runs if r < 0.5))
    rnd = random.Random(5)                            # was the first guess lucky? 60 blind ones, anywhere round the Sun
    blind = [hunt(OBS, start=[rnd.uniform(2, 3.6), 0, 0, rnd.uniform(2, 20) * DEG, rnd.uniform(0, 360) * DEG,
                              rnd.uniform(0, 360) * DEG])[2] for _ in range(60)]
    same = [o for o in blind if apart(look(o, RETURN), look(ellipse, RETURN)) < 0.01]
    lost = sorted(leftover(o, OBS) for o in blind if o not in same)
    print("60 blind first guesses: %d end on the same orbit; the other %d stop with a leftover of %.0f arcsec or more"
          % (len(same), len(lost), lost[0]))
    from step2_sky import position
    deg = lambda p: [round(v / DEG, 4) for v in p]
    card = lambda o: dict(size=o[0], stretch=math.hypot(o[1], o[2]), tilt=o[3] / DEG, leftover=leftover(o, OBS),
                          miss=apart(look(o, RETURN), truth), there=deg(look(o, RETURN)),
                          sky=[deg(look(o, d)) for d in range(0, RETURN + 1, 5)],
                          path=[[round(v, 4) for v in position(o, d)[:2]] for d in range(0, 1721, 20)],
                          at=[round(v, 4) for v in position(o, RETURN)[:2]])
    save(6, line=dict(miss=apart(line_guess(RETURN), truth), there=deg(line_guess(RETURN))), circle=card(circle), r1=r1,
         ellipse=card(ellipse), r2=r2, truth=card(list(PLANET)), start=card(START),
         trail=[[round(apart(look(o, RETURN), truth), 4), round(leftover(o, OBS), 3)] for o in trail],
         runs=[round(r, 4) for r in runs], blind=[len(same), len(lost), lost[0]], inside=sum(1 for r in runs if r < 0.5), half=runs[100], most=runs[180], worst=runs[-1])
