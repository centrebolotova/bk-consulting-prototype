# Собирает блок «География проектов» (src/_geo.html) из карты geo-map.svg, точек geo-pins.json и списка проектов ниже.
# build.py вставляет блок вместо метки <!--GEO--> в страницах.
import json, pathlib, html

HERE = pathlib.Path(__file__).parent
svg = (HERE / 'geo-map.svg').read_text(encoding='utf-8')
pins = json.loads((HERE / 'geo-pins.json').read_text(encoding='utf-8'))
TODO = '<mark class="todo" title="Уточнить у Юлии">{}</mark>'

# type: hotel — отели; glamp — глэмпинги и базы; research — исследования и концепции
P = [
    {'id': 'msk', 'type': 'hotel', 'region': 'Москва', 'title': 'Девять городских отелей и апарт-отелей',
     'img': 'library/sait/DSC_8919-1.jpg', 'items': [
         ('«Кенсингтон»', 'офис → отель, 20 номеров, 2021'), ('«Алеон»', '15 номеров за 3 месяца, 2020'),
         ('«Галерея»', '15 номеров, бюджет 21 млн ₽, 2019'), ('«СЛАВА»', '10 апартаментов в управлении, 2024'),
         ('«Лофт» на Бауманской', '500 м², бюджет 15 млн ₽'), ('«Гостика», «Радио», «Гринвич», «Потаповский»', '2016–2017')]},
    {'id': 'mo', 'type': 'glamp', 'region': 'Подмосковье · нацпарк «Лосиный остров»', 'title': 'Глэмпинг в национальном парке',
     'img': 'library/sait/DSC_5337.jpg', 'items': [('Аудит и сертификация', '2023'), ('Брендбук и сайт', ''), ('Обучение персонала', '')]},
    {'id': 'mo200', 'type': 'research', 'region': TODO.format('Подмосковье') + ' · участок 200 га', 'title': 'Исследование показало: выгоднее велнес-отель',
     'img': 'img/case-wellness.jpg', 'items': [('Сравнили форматы', 'парк-отель, велнес и др.'), ('Выбран велнес-отель', 'по экономике'), ('Видеопрезентация', 'для инвесторов')]},
    {'id': 'sochi', 'type': 'research', 'region': 'Сочи', 'title': 'Концепция на сложном рельефе',
     'img': 'library/sait/__-_page-0001.jpg', 'items': [('«Парк слонов»', 'участок 3 га, перепад 150 м'), ('Концепция и финмодель', ''), (TODO.format('Апарт-отель на 24 номера'), 'уточнить')]},
    {'id': 'krd', 'type': 'glamp', 'region': 'Краснодарский край', 'title': TODO.format('Глэмпинг под кредит 50 млн ₽'),
     'img': 'library/sait/DSC_5339.jpg', 'items': [('Бизнес-план для банка', TODO.format('уточнить детали'))]},
    {'id': 'karelia', 'type': 'hotel', 'region': 'Карелия', 'title': TODO.format('Мини-отель'),
     'img': 'library/sait/DSC_7900-1_1.jpg', 'items': [('Концепция и расчёт', TODO.format('уточнить детали'))]},
    {'id': 'altai', 'type': 'research', 'region': 'Республика Алтай · Усть-Сема', 'title': 'Участок 2 га у реки → концепция для инвестора',
     'img': 'library/altai-koncept/Image1.jpg', 'items': [('Концепция и планировка', '2025'), ('Архитектура и 29 визуализаций', ''), ('Буклет с бизнес-планом', 'для инвесторов')]},
    {'id': 'ga', 'type': 'research', 'region': 'Горно-Алтайск', 'title': 'Вместо глэмпинга — отель на 30 номеров',
     'img': 'library/altai-koncept/Image20.jpg', 'items': [('Маркетинговое исследование', 'спрос и конкуренты'), ('Рекомендация формата', 'отель с велнес-зоной')]},
]
OFFS = {'mo': 'translate(16px,-14px)', 'mo200': 'translate(-16px,12px)'}
OFFS = {k: 'transform:' + v for k, v in OFFS.items()}
TYPES = [('', 'Все'), ('hotel', 'Отели'), ('glamp', 'Глэмпинги и базы'), ('research', 'Исследования и концепции')]

pins_html = ''.join(
    f'<button class="geo-pin" data-id="{p["id"]}" data-type="{p["type"]}" style="left:{pins[p["id"]][0]}%;top:{pins[p["id"]][1]}%;{OFFS.get(p["id"], "")}" '
    f'aria-label="{html.escape(p["region"].replace(TODO.format(""), ""))}"><i></i></button>' for p in P)
cards = ''
for p in P:
    lis = ''.join(f'<li><b>{a}</b>{f"<span>{b}</span>" if b else ""}</li>' for a, b in p['items'])
    cards += (f'<article class="geo-card" data-id="{p["id"]}"><div class="ph"><img loading="lazy" src="{p["img"]}" alt=""></div>'
              f'<div class="eyebrow">{p["region"]}</div><h3>{p["title"]}</h3><ul>{lis}</ul></article>')
chips = ''.join(f'<button class="{"on" if not k else ""}" data-f="{k}">{n}</button>' for k, n in TYPES)

block = f'''<!-- География проектов -->
<section class="geo" id="geo">
  <div class="wrap">
    <div class="head">
      <div><div class="eyebrow rv">От Карелии до Алтая</div><h2 class="serif rv" style="margin-top:14px">География проектов</h2></div>
      <p class="rv">Городские отели в Москве, загородные проекты и исследования по всей стране. Наведите на точку — покажем, что там сделано.</p>
    </div>
    <div class="geo-stats rv"><div><b>8</b>точек на карте</div><div><b>5</b>регионов</div><div><b>30+</b>проектов</div></div>
    <div class="geo-chips rv">{chips}</div>
    <div class="geo-grid">
      <div class="geo-map rv"><div class="geo-canvas">{svg}{pins_html}</div></div>
      <div class="geo-side rv">{cards}</div>
    </div>
  </div>
</section>
'''
(HERE / '_geo.html').write_text(block, encoding='utf-8')
print('_geo.html', len(block) // 1024, 'КБ')
