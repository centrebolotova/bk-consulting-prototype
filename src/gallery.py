# Строит photos.html — библиотеку всех фото BK consulting из library/photos.json.
import json, pathlib, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
items = json.loads((ROOT / 'library' / 'photos.json').read_text(encoding='utf-8'))
ORDER = ['сайт', 'Диск «САЙТ 2025»', 'фото участка', 'визуализация концепции', 'из документа']
kinds = [k for k in ORDER if any(i['kind'] == k for i in items)] + sorted({i['kind'] for i in items} - set(ORDER))
items.sort(key=lambda i: (kinds.index(i['kind']), i['source'], i['file']))

cards = []
for n, i in enumerate(items, 1):
    name = i['file'].rsplit('/', 1)[-1]
    orient = 'гориз.' if i['w'] >= i['h'] else 'верт.'
    cards.append(
        f'<figure data-k="{html.escape(i["kind"])}"><a href="{i["file"]}" target="_blank"><img loading="lazy" src="{i["file"]}" alt=""></a>'
        f'<figcaption><b>{n:03d}</b> · {html.escape(i["kind"])} · {orient} {i["orig"]}<br><span>{html.escape(i["source"])} · {html.escape(name)}</span></figcaption></figure>')

chips = ''.join(f'<button data-k="{html.escape(k)}">{html.escape(k)} · {sum(1 for i in items if i["kind"] == k)}</button>' for k in kinds)
page = f'''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="robots" content="noindex, nofollow"><meta name="description" content="Библиотека фото и визуализаций BK consulting: проекты отелей, глэмпингов и концепций.">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Библиотека фото — BK consulting</title>
<style>
:root{{--cream:#F4EFE6;--ink:#1E1D1B;--stone:#8A847A;--line:#D9D1C3}}
*{{box-sizing:border-box;margin:0}}body{{background:var(--cream);color:var(--ink);font:15px/1.5 -apple-system,"Segoe UI",sans-serif;padding:32px 16px 80px}}
.wrap{{max-width:1600px;margin:0 auto}}h1{{font:300 40px/1.1 Georgia,serif;margin-bottom:10px}}p.lead{{color:#3A3834;max-width:760px;margin-bottom:22px}}
.chips{{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:26px;position:sticky;top:0;background:var(--cream);padding:10px 0;z-index:2}}
.chips button{{font:inherit;font-size:13px;padding:8px 14px;border:1px solid var(--line);border-radius:999px;background:none;cursor:pointer}}
.chips button.on{{background:var(--ink);color:#fff;border-color:var(--ink)}}
.grid{{columns:4 300px;column-gap:14px}}figure{{break-inside:avoid;margin:0 0 14px;background:#fff;border-radius:6px;overflow:hidden}}
figure img{{width:100%;display:block}}figcaption{{padding:10px 12px;font-size:12px;color:#3A3834}}figcaption span{{color:var(--stone);word-break:break-all}}
a.back{{font-size:14px;color:var(--ink)}}
</style></head><body><div class="wrap">
<a class="back" href="index.html">← Прототип сайта</a>
<h1>Библиотека фото</h1>
<p class="lead">Все фото и визуализации, которые есть у BK consulting: с текущего сайта, с Яндекс Диска Юли (ссылки из писем) и из документов. Всего {len(items)}. Номер слева — чтобы сказать «берём 014 на первый экран». Клик открывает фото в полном размере. Часть картинок на Диске сделана нейросетью — их не выдаём за реальные объекты.</p>
<div class="chips"><button class="on" data-k="">Все · {len(items)}</button>{chips}</div>
<div class="grid">{''.join(cards)}</div></div>
<script>
document.querySelectorAll('.chips button').forEach(b=>b.onclick=()=>{{document.querySelectorAll('.chips button').forEach(x=>x.classList.toggle('on',x===b));document.querySelectorAll('figure').forEach(f=>f.style.display=!b.dataset.k||f.dataset.k===b.dataset.k?'':'none')}});
</script></body></html>'''
(ROOT / 'photos.html').write_text(page, encoding='utf-8')
print('photos.html', len(items))
