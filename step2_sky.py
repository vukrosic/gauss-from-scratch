"""Step 2. A model sky: the Earth, a small planet, and 41 days of slightly wrong measurements."""
import math, random
from save import save

DEG = math.pi / 180
ARCSEC = DEG / 3600

def solve_kepler(M, e):
    """Kepler's equation E - e sin E = M, solved by Newton's method."""
    E = M
    for _ in range(30):
        E -= (E - e * math.sin(E) - M) / (1 - e * math.cos(E))
    return E

def position(orbit, day):
    """Where a body is, in 3-D, from six numbers that describe its orbit."""
    a, h, k, tilt, node, L0 = orbit                 # a = size; (h, k) = how stretched, and which way
    e, long_peri = math.hypot(h, k), math.atan2(k, h)
    M = L0 - long_peri + 2 * math.pi * day / (365.25 * a ** 1.5)     # Kepler's third law
    E = solve_kepler(M, e)
    x, y = a * (math.cos(E) - e), a * math.sqrt(1 - e * e) * math.sin(E)
    w = long_peri - node
    cw, sw, cn, sn = math.cos(w), math.sin(w), math.cos(node), math.sin(node)
    ci, si = math.cos(tilt), math.sin(tilt)
    return ((cw * cn - sw * sn * ci) * x - (sw * cn + cw * sn * ci) * y,
            (cw * sn + sw * cn * ci) * x - (sw * sn - cw * cn * ci) * y,
            sw * si * x + cw * si * y)

def orbit(a, e, tilt, node, peri, M0):
    """Textbook elements (in degrees) -> the six numbers used above."""
    lp = (node + peri) * DEG
    return (a, e * math.cos(lp), e * math.sin(lp), tilt * DEG, node * DEG, lp + M0 * DEG)

EARTH = orbit(1.0, 0.0168, 0.0, 0.0, 99.5, 0.5)
PLANET = orbit(2.767, 0.0785, 10.6, 80.9, 69.0, 287.1)      # the truth. The fit never reads this.

def look(orb, day):
    """Direction from the Earth to the body: two angles on the sky (longitude, latitude)."""
    px, py, pz = position(orb, day)
    ex, ey, ez = position(EARTH, day)
    dx, dy, dz = px - ex, py - ey, pz - ez
    return math.atan2(dy, dx), math.atan2(dz, math.hypot(dx, dy))

def apart(p, q):
    """Angle between two directions on the sky, in degrees."""
    c = math.sin(p[1]) * math.sin(q[1]) + math.cos(p[1]) * math.cos(q[1]) * math.cos(p[0] - q[0])
    return math.acos(max(-1.0, min(1.0, c))) / DEG

NIGHTS = [0, 1, 2, 3, 9, 10, 12, 13, 17, 18, 20, 21, 22, 27, 29, 30, 31, 32, 33, 36, 39, 41]
NOISE = 3.0          # typical error of one measurement, in arcseconds
RETURN = 340         # 7 December 1801 is day 340 when 1 January is day 0

def observe(seed=1801, noise=NOISE):
    """What the astronomer writes down: the true direction plus a small random error."""
    rnd = random.Random(seed)
    return [(d,) + tuple(v + rnd.gauss(0, noise * ARCSEC) for v in look(PLANET, d)) for d in NIGHTS]

OBS = observe()

if __name__ == "__main__":
    print(len(OBS), "nights over", NIGHTS[-1], "days, error about", NOISE, "arcseconds each")
    for d, lon, lat in OBS[:3] + OBS[-1:]:
        print("  day %2d  longitude %8.4f  latitude %7.4f" % (d, lon / DEG, lat / DEG))
    print("it moved %.2f degrees across the sky" % apart(OBS[0][1:], OBS[-1][1:]))
    year = 365.25 * PLANET[0] ** 1.5
    print("one trip round the Sun: %.0f days, so 41 days is %.1f%% of the orbit" % (year, 4100 / year))
    print("true place on day %d: longitude %.2f, latitude %.2f" % ((RETURN,) + tuple(v / DEG for v in look(PLANET, RETURN))))
    print("it moves %.1f degrees between day 41 and day %d" % (apart(look(PLANET, 41), look(PLANET, RETURN)), RETURN))
    sun = lambda d: apart(look(PLANET, d), look((1e-9, 0, 0, 0, 0, 0), d))       # angle between planet and Sun
    print("angle from the Sun: day 0 %.0f, day 41 %.0f, smallest %.0f on day %d, day %d %.0f"
          % (sun(0), sun(41), min(sun(d) for d in range(RETURN)), min(range(RETURN), key=sun), RETURN, sun(RETURN)))
    deg = lambda p: [round(v / DEG, 5) for v in p]
    flat = lambda orb, days: [[round(v, 4) for v in position(orb, d)[:2]] for d in days]
    save(2, nights=NIGHTS, noise=NOISE, back=RETURN, obs=[[d] + deg((lon, lat)) for d, lon, lat in OBS],
         errors=[[round((lon - look(PLANET, d)[0]) * math.cos(lat) / ARCSEC, 2), round((lat - look(PLANET, d)[1]) / ARCSEC, 2)]
                 for d, lon, lat in OBS],
         moved=apart(OBS[0][1:], OBS[-1][1:]), year=year, share=4100 / year, there=deg(look(PLANET, RETURN)),
         travel=apart(look(PLANET, 41), look(PLANET, RETURN)), sky=[deg(look(PLANET, d)) for d in range(0, RETURN + 1, 5)],
         sun=[round(sun(d), 2) for d in range(0, RETURN + 1, 5)],
         closest=[min(range(RETURN), key=sun), round(min(sun(d) for d in range(RETURN)), 2)], earth=flat(EARTH, range(0, 371, 5)),
         planet=flat(PLANET, range(0, int(year) + 21, 20)), earth_nights=flat(EARTH, NIGHTS + [RETURN]),
         planet_nights=flat(PLANET, NIGHTS + [RETURN]))
