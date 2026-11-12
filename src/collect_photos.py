# Собирает все фото BK consulting в library/ (для страницы-библиотеки photos.html):
#  - сайт consulting-hotel.ru: все картинки со страниц из sitemap;
#  - Яндекс Диск Юли: «САЙТ 2025», «Алтай Усть-Сема» (фото участка), «Алтай. Усть-Сема» (визуализации);
#  - docx «Пример работы Галерея отель» из загрузок.
# Картинки ужимаются до 1920 px по длинной стороне. Метаданные — library/photos.json.
import io, json, re, sys, zipfile, hashlib, pathlib, urllib.request, urllib.parse
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
LIB = ROOT / 'library'
LIB.mkdir(exist_ok=True)
UA = {'User-Agent': 'Mozilla/5.0'}
items, seen = [], set()


def fetch(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()


def save(data, folder, name, source, kind, note=''):
    h = hashlib.md5(data).hexdigest()
    if h in seen:
        return
    try:
        im = Image.open(io.BytesIO(data))
        im.load()
    except Exception:
        return
    w, h0 = im.size
    if max(w, h0) < 500:  # иконки, логотипы, миниатюры
        return
    seen.add(h)
    im = im.convert('RGB')
    im.thumbnail((1920, 1920))
    d = LIB / folder
    d.mkdir(exist_ok=True)
    stem = re.sub(r'[^\w\-]+', '_', pathlib.Path(name).stem)[:60] or h[:10]
    out = d / (stem + '.jpg')
    i = 2
    while out.exists():
        out = d / f'{stem}_{i}.jpg'
        i += 1
    im.save(out, quality=82, optimize=True, progressive=True)
    items.append({'file': str(out.relative_to(ROOT)).replace('\\', '/'), 'source': source, 'kind': kind,
                  'w': im.size[0], 'h': im.size[1], 'orig': f'{w}×{h0}', 'note': note})
    print(len(items), out.name, im.size, flush=True)


# 1. сайт
pages = set(re.findall(r'<loc>([^<]+)</loc>', fetch('https://consulting-hotel.ru/sitemap.xml').decode('utf-8', 'ignore')))
pages.add('https://consulting-hotel.ru/')
urls = {}
for p in sorted(pages):
    try:
        html = fetch(p).decode('utf-8', 'ignore')
    except Exception as e:
        print('нет страницы', p, e)
        continue
    for u in re.findall(r'https://static\.tildacdn\.com/[^"\'\s\)]+?\.(?:jpe?g|png|webp)', html, re.I):
        urls.setdefault(u, p.replace('https://consulting-hotel.ru', '') or '/')
for u, page in urls.items():
    try:
        save(fetch(u), 'sait', urllib.parse.unquote(u.rsplit('/', 1)[-1]), 'сайт ' + page, 'сайт', u)
    except Exception as e:
        print('ошибка', u, e)


# 2. Яндекс Диск
def disk(key, folder, kind):
    api = 'https://cloud-api.yandex.net/v1/disk/public/resources'

    def walk(path):
        q = {'public_key': key, 'limit': 500}
        if path:
            q['path'] = path
        d = json.load(urllib.request.urlopen(api + '?' + urllib.parse.urlencode(q)))
        for it in d.get('_embedded', {}).get('items', []):
            if it['type'] == 'dir':
                walk(it['path'])
            elif it.get('media_type') == 'image':
                href = json.load(urllib.request.urlopen(api + '/download?' + urllib.parse.urlencode({'public_key': key, 'path': it['path']})))['href']
                save(fetch(href), folder, it['name'], 'Диск: ' + d.get('name', '') + it['path'], kind, key)
    walk(None)


disk('https://disk.yandex.ru/d/sGmP60wE-IGb_A', 'disk-sait-2025', 'Диск «САЙТ 2025»')
disk('https://disk.yandex.ru/d/60a99AAr139kdQ', 'altai-uchastok', 'фото участка')
disk('https://disk.yandex.ru/d/9PcMKolF1p6bNg', 'altai-koncept', 'визуализация концепции')

# 3. docx с примерами работ
for docx in pathlib.Path(r'D:\Перенесено с C\Downloads').glob('Пример работ*.docx'):
    with zipfile.ZipFile(docx) as z:
        for n in z.namelist():
            if n.startswith('word/media/'):
                save(z.read(n), 'docx-' + re.sub(r'\W+', '-', docx.stem)[:30], n.rsplit('/', 1)[-1], 'docx ' + docx.name, 'из документа')

(LIB / 'photos.json').write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding='utf-8')
print('всего', len(items))
