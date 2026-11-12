# Автопроверка собранных страниц: ссылки, фото/видео, заглушки, заголовки, квиз, меню, пустые alt.
import re, pathlib, sys, json
sys.stdout.reconfigure(encoding='utf-8')
root = pathlib.Path(__file__).resolve().parent.parent
pages = sorted(p for p in root.glob('*.html') if not p.name.startswith('_'))
names = {p.name for p in pages}
issues = []
for p in pages:
    s = p.read_text(encoding='utf-8')
    body = s[s.find('<body'):]
    bad = lambda m: issues.append(f'{p.name}: {m}')
    # ссылки
    for h in re.findall(r'href="([^"]+)"', body):
        if h in ('#', ''):
            bad('ссылка-заглушка "#"')
        elif h.endswith('.html') or '.html#' in h:
            if h.split('#')[0] not in names:
                bad(f'нет страницы {h}')
        elif h.startswith('#') and len(h) > 1 and f'id="{h[1:]}"' not in s:
            bad(f'якорь {h} не найден')
    # файлы
    for a in re.findall(r'(?:src|data-src|poster)="([^"]+)"', body):
        if a.startswith(('http', 'data:', 'img/hero-\'')) or "'" in a:
            continue
        if not (root / a).exists():
            bad(f'нет файла {a}')
    for a in re.findall(r'src="(https?://[^"]+)"', body):
        if 'tildacdn' in a:
            bad(f'фото с чужого CDN (Тильда): {a[-40:]}')
    # структура
    h1 = len(re.findall(r'<h1[\s>]', body))
    if h1 != 1:
        bad(f'H1 на странице: {h1}')
    if 'class="quiz"' not in body:
        bad('нет окна заявки')
    if body.count('data-quiz') < 2:
        bad('мало кнопок заявки')
    if 'class="dd"' not in body:
        bad('нет выпадающего меню')
    t = re.search(r'<title>(.*?)</title>', s)
    d = re.search(r'<meta name="description" content="([^"]*)"', s)
    if not t or len(t.group(1)) > 70:
        bad(f'title {len(t.group(1)) if t else 0} знаков')
    if not d or not 70 <= len(d.group(1)) <= 170:
        bad(f'description {len(d.group(1)) if d else 0} знаков')
    for m in re.findall(r'<img[^>]*>', body):
        if 'alt=' not in m:
            bad('img без alt')
    for w in ['lorem', 'TODO', 'XXX', 'Html code', 'undefined', 'гаранти', '27 %', '98 %']:
        if w.lower() in re.sub(r'<[^>]+>', ' ', body).lower():
            bad(f'слово «{w}» в тексте')
print(len(pages), 'страниц;', len(issues), 'замечаний')
for i in issues:
    print(' -', i)
