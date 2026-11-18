# Каталог всех посадочных «объект × услуга» — src/obekty.html
import json, pathlib
SRC = pathlib.Path(__file__).parent
L = json.loads((SRC / '_landings.json').read_text(encoding='utf-8'))
base = (SRC / 'proverka-uchastka.html').read_text(encoding='utf-8')
head = base[:base.index('<title>')]
links_head = base[base.index('<link rel="preconnect"'):base.index('</head>')]
after_head = base[base.index('</head>'):base.index('<!-- 1.')].replace('data-quiz="1">Проверить участок', 'data-quiz>Обсудить проект')
tail = base[base.index('<footer>'):].replace('data-quiz="1">Проверить участок', 'data-quiz>Обсудить проект')
groups = {}
for x in L:
    groups.setdefault(x['type'], []).append(x)
CORE = {'глэмпинг': [('glamping-marketing.html', 'Исследование и окупаемость'), ('proverka-uchastka.html', 'Проверка участка'), ('glamping-conception.html', 'Концепция и мастер-план'), ('glamping-business-plan.html', 'Бизнес-план'), ('glamping-pod-kluch.html', 'Под ключ')],
        'база отдыха': [('baza-otdyha.html', 'Обзор направления')],
        'гостиница': [('marketing.html', 'Исследование рынка'), ('conception.html', 'Концепция'), ('business-plan.html', 'Бизнес-план'), ('hotel-pod-kluch.html', 'Под ключ'), ('hotel-upravlenie.html', 'Управление отелем')],
        'модульная гостиница': [('modulnaya-gostinica.html', 'Расчёт и концепция')]}
for k in CORE:
    groups.setdefault(k, [])
order = ['глэмпинг', 'база отдыха', 'турбаза', 'кемпинг', 'туристический комплекс', 'парк-отель', 'эко-отель', 'загородный отель', 'гостиница', 'мини-гостиница', 'гостевой дом', 'апарт-отель', 'модульная гостиница', 'хостел']
cards = ''
for k in order:
    if k not in groups:
        continue
    links = ''.join(f'<a href="{u}">{n}</a>' for u, n in CORE.get(k, [])) + ''.join(f'<a href="l-{x["slug"]}.html">{x["service"]}</a>' for x in groups[k])
    cards += f'<div class="ocard rv"><h3>{k.capitalize()}</h3><div>{links}</div></div>'
page = head + '<title>Объекты и услуги — BK consulting</title>\n<meta name="description" content="Консалтинг для глэмпингов, баз отдыха, турбаз, кемпингов, загородных отелей, гостиниц, гостевых домов, апарт-отелей и хостелов: проект, бизнес-план, открытие, управление.">\n' + links_head + after_head + f'''<section class="svc-hero" style="padding:0;min-height:60svh">
  <img src="library/altai-koncept/Image1.jpg" alt="">
  <div class="wrap">
    <div class="crumbs"><a href="index.html">Главная</a> · Объекты и услуги</div>
    <h1 class="serif">Объекты и услуги</h1>
    <p class="lead">От кемпинга до туристического комплекса. Выберите свой тип объекта — покажем, что мы делаем именно для него.</p>
  </div>
</section>
<section><div class="wrap"><div class="ogrid">{cards}</div></div></section>
''' + tail
(SRC / 'obekty.html').write_text(page, encoding='utf-8')
print('obekty.html', len(order))
