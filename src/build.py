# Собирает цельные страницы: стили и скрипты вшиваются в каждый HTML,
# чтобы страница не зависела от отдельных css/js. Фото и видео лежат в img/ рядом.
import pathlib

src = pathlib.Path(__file__).parent
out = src.parent
css = (src / 'style.css').read_text(encoding='utf-8') + (src / 'variants.css').read_text(encoding='utf-8')
js = (src / 'app.js').read_text(encoding='utf-8') + (src / 'variants.js').read_text(encoding='utf-8')

import json as _json
# фото с Тильды → локальные копии из библиотеки (поле note в photos.json — исходный адрес)
CDN_MAP = {i['note']: i['file'] for i in _json.loads((out / 'library' / 'photos.json').read_text(encoding='utf-8')) if i.get('note', '').startswith('http')}

# первый экран выбран сразу при загрузке (без чёрной вспышки до запуска скриптов)
EARLY_HERO = "<script>try{var h=localStorage.getItem('bk-hero')||'forest';document.body.dataset.hero=h.split(':')[0];document.body.dataset.heroFull=h}catch(e){document.body.dataset.hero='forest'}</script>"

# ссылки из карточек кейсов на страницы проектов (порядок важен: частные раньше общих)
CASE_KEYS = [('Горно-Алтайск', 'gorno-altaysk'), ('200 га', 'velnes-200-ga'), ('Оздоровительный', 'velnes-200-ga'), ('велнес', 'velnes-200-ga'),
             ('Парк слонов', 'park-slonov'), ('посёлок', 'poselok-otel'), ('Галере', 'galereya'), ('Кенсингтон', 'kensington'),
             ('Алеон', 'aleon'), ('Гостик', 'gostika'), ('Лофт', 'loft'), ('СЛАВА', 'slava'), ('Лосин', 'losiny-ostrov'),
             ('Усть-Сем', 'altai'), ('Алтай', 'altai')]


def link_cases(s, name):
    if name.startswith('proekt-'):
        return s
    def art(m):
        blk = m.group(0)
        if 'case-link' in blk:
            return blk
        text = re.sub(r'<[^>]+>', ' ', blk)
        slug = next((v for k, v in CASE_KEYS if k in text), None)
        if not slug:
            return blk
        return blk[:blk.rindex('</article>')] + f'<a class="case-link" href="proekt-{slug}.html">Подробнее о проекте →</a></article>'
    return re.sub(r'<article class="(?:case|vid)[^"]*"[^>]*>.*?</article>', art, s, flags=re.S)


NOINDEX = '<meta name="robots" content="noindex, nofollow">'

import re

# Единый подвал и ссылки меню для всех страниц (в исходниках местами стоят заглушки «#»)
FOOTER_COLS = '''<div><h4>Глэмпинги и базы</h4><a href="glamping-marketing.html">Исследование и окупаемость</a><a href="proverka-uchastka.html">Проверка участка</a><a href="glamping-conception.html">Концепция и мастер-план</a><a href="glamping-business-plan.html">Бизнес-план</a><a href="granty.html">Гранты и субсидии</a><a href="glamping-pod-kluch.html">Под ключ</a><a href="baza-otdyha.html">База отдыха</a></div>
      <div><h4>Отели</h4><a href="marketing.html">Исследование рынка</a><a href="conception.html">Концепция</a><a href="business-plan.html">Бизнес-план</a><a href="design.html">Дизайн-проект</a><a href="hotel-pod-kluch.html">Под ключ</a><a href="hotel-upravlenie.html">Управление</a><a href="modulnaya-gostinica.html">Модульная гостиница</a></div>
      <div><h4>Компания</h4><a href="proekty.html">Проекты</a><a href="o-kompanii.html">О компании</a><a href="strategicheskaya-sessiya.html">Стратегическая сессия</a><a href="photos.html">Библиотека фото</a><a href="tel:+74996505134">+7 499 650-51-34</a></div>'''
SVC = {'Проверка участка': 'proverka-uchastka.html', 'Концепция и мастер-план': 'glamping-conception.html',
       'Бизнес-план и финмодель': 'glamping-business-plan.html', 'Гранты и субсидии': 'granty.html',
       'Дизайн и архитектура': 'glamping-design.html', 'Загрузка и управление': 'glamping-zagruzka.html',
       'Концепция отеля': 'conception.html', 'Бизнес-план гостиницы': 'business-plan.html', 'Дизайн-проект': 'design.html',
       'Управление и загрузка': 'hotel-upravlenie.html', 'Модульная гостиница': 'modulnaya-gostinica.html'}


def fix_links(s, name):
    s = re.sub(r'(<footer>.*?<div class="grid">\s*<div>.*?</div>)\s*<div><h4>.*?(?=</div>\s*<div class="legal">)',
               lambda m: m.group(1) + '\n      ' + FOOTER_COLS + '\n    ', s, count=1, flags=re.S)
    s = s.replace('href="index.html#cases">Проекты', 'href="proekty.html">Проекты').replace('href="#cases">Проекты', 'href="proekty.html">Проекты')
    s = s.replace('href="index.html#founder">О компании', 'href="o-kompanii.html">О компании').replace('href="#founder">О компании', 'href="o-kompanii.html">О компании')
    s = s.replace('href="index.html#glamping">Глэмпинги', 'href="glamping.html">Глэмпинги').replace('href="index.html#hotel">Отели', 'href="hotel.html">Отели')
    if name == 'index.html':
        # карточки услуг: ссылка по названию; «Открытие под ключ» — своя для каждой вкладки
        def card(m):
            t = m.group(2)
            href = SVC.get(t)
            if t == 'Открытие под ключ':
                href = 'hotel-pod-kluch.html' if m.start() > s.find('data-pane="hotel"') > 0 else 'glamping-pod-kluch.html'
            return m.group(0).replace('href="#"', f'href="{href}"', 1) if href else m.group(0)
        s = re.sub(r'<a class="svc rv" href="#">(<span class="n">\d+</span>)<h4>([^<]+)</h4>', card, s)
        pane_h = s.find('data-pane="hotel"')
        first = s.find('<a class="link" href="#">Подробнее')
        if first != -1:
            s = s[:first] + s[first:].replace('<a class="link" href="#">Подробнее', '<a class="link" href="glamping-marketing.html">Подробнее', 1)
        second = s.find('<a class="link" href="#">Подробнее', pane_h)
        if second != -1:
            s = s[:second] + s[second:].replace('<a class="link" href="#">Подробнее', '<a class="link" href="marketing.html">Подробнее', 1)
        s = s.replace('<a class="link" href="#">Все проекты', '<a class="link" href="proekty.html">Все проекты')
    return s

for f in sorted(p for p in src.glob('*.html') if not p.name.startswith('_')):
    s = f.read_text(encoding='utf-8')
    s = s.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n' + NOINDEX, 1)  # прототип не должен попадать в поиск
    s = s.replace('<link rel="stylesheet" href="style.css">', '<style>\n' + css + '\n</style>')
    s = s.replace('<script src="app.js"></script>', '<script>\n' + js + '\n</script>')
    s = s.replace('<!--GEO-->', (src / '_geo.html').read_text(encoding='utf-8'))
    s = re.sub(r'<nav class="menu">.*?</nav>', lambda m: (src / '_nav.html').read_text(encoding='utf-8'), s, count=1, flags=re.S)
    for u, loc in CDN_MAP.items():
        s = s.replace(u, loc)
    if 'hero-media' in s:
        s = s.replace('<body>', '<body>' + EARLY_HERO, 1)
    s = link_cases(s, f.name)
    s = fix_links(s, f.name)
    (out / f.name).write_text(s, encoding='utf-8')
    print('собрано', f.name, len(s))
