# Рисует карту России (регионы) в SVG для блока «География проектов».
# Источник контуров: click_that_hood/russia.geojson (лежит в scratchpad, путь — аргумент).
# Проекция — равнопромежуточная коническая, центральный меридиан 100°, параллели 50° и 70°.
import json, math, sys, pathlib

src = sys.argv[1]
out = pathlib.Path(__file__).parent / 'geo-map.svg'
d = json.load(open(src, encoding='utf-8'))

L0, P1, P2, P0 = math.radians(100), math.radians(50), math.radians(70), math.radians(60)
n = (math.cos(P1) - math.cos(P2)) / (P2 - P1)
G = math.cos(P1) / n + P1
r0 = G - P0


def proj(lon, lat):
    if lon < 0:
        lon += 360  # Чукотка за 180-м меридианом
    lam, phi = math.radians(lon), math.radians(lat)
    r = G - phi
    th = n * (lam - L0)
    return r * math.sin(th), r0 - r * math.cos(th)


rings = []
for f in d['features']:
    g = f['geometry']
    polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
    for poly in polys:
        ring = [proj(*pt[:2]) for pt in poly[0]]
        rings.append(ring)

xs = [p[0] for r in rings for p in r]
ys = [p[1] for r in rings for p in r]
minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
PAD = 30
W = 1000
S = (W - 2 * PAD) / (maxx - minx)
H = (maxy - miny) * S + 2 * PAD


def tr(p):
    return (p[0] - minx) * S + PAD, (maxy - p[1]) * S + PAD


paths = []
for ring in rings:
    pts = [tr(p) for p in ring]
    simp = [pts[0]]
    for p in pts[1:]:
        if abs(p[0] - simp[-1][0]) + abs(p[1] - simp[-1][1]) > 2.2:
            simp.append(p)
    if len(simp) < 4:
        continue
    # совсем мелкие острова не рисуем
    bx = max(p[0] for p in simp) - min(p[0] for p in simp)
    by = max(p[1] for p in simp) - min(p[1] for p in simp)
    if bx * by < 12:
        continue
    paths.append('M' + 'L'.join(f'{x:.1f},{y:.1f}' for x, y in simp) + 'Z')

svg = f'<svg class="geo-svg" viewBox="0 0 {W} {H:.0f}" preserveAspectRatio="xMidYMid meet" aria-hidden="true"><path d="{"".join(paths)}"/></svg>'
out.write_text(svg, encoding='utf-8')

# координаты точек проектов → проценты от размеров карты
PINS = {
    'msk': (37.62, 55.75), 'mo': (37.75, 55.86), 'mo200': (36.9, 55.4), 'sochi': (39.72, 43.6),
    'krd': (39.6, 44.9), 'karelia': (34.3, 62.0), 'altai': (85.8, 51.4), 'ga': (86.4, 52.4),
}
pins = {k: (round(tr(proj(*v))[0] / W * 100, 2), round(tr(proj(*v))[1] / H * 100, 2)) for k, v in PINS.items()}
(pathlib.Path(__file__).parent / 'geo-pins.json').write_text(json.dumps(pins), encoding='utf-8')
print(len(paths), 'контуров', f'{W}x{H:.0f}', len(svg) // 1024, 'КБ', pins)
