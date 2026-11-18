# Скачивает исходники фотосессий из папок Юли (документ «Ссылки на доступы к фото для сайта 2024 декабрь.docx»)
# в library/ish/<проект>/ — ужимает до 1920 px и дописывает в library/photos.json с типом «исходник».
import io, json, sys, pathlib, urllib.request, urllib.parse, re
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
LIB = ROOT / 'library'
src = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'))
NAMES = {'potapovsky': '«Потаповский»', 'radio': '«Радио»', 'aleon': '«Алеон»', 'kalyannaya': 'кальянная', 'kensington': '«Кенсингтон»',
         'losiny': '«Лосиный остров»', 'gostika': '«Гостика»', 'galereya': '«Галерея»', 'loft': '«Лофт»', 'slava': '«СЛАВА»', 'hostel-radio': 'хостел «Радио»'}
API = 'https://cloud-api.yandex.net/v1/disk/public/resources'
items = json.loads((LIB / 'photos.json').read_text(encoding='utf-8'))
have = {i['file'] for i in items}
for proj, d in src.items():
    key = 'https://disk.yandex.ru/d/' + d['key']
    out = LIB / 'ish' / proj
    out.mkdir(parents=True, exist_ok=True)
    for path, size, mt in d['files']:
        if mt != 'image':
            continue
        name = re.sub(r'[^\w\-]+', '_', pathlib.Path(path).stem)[:60] + '.jpg'
        f = out / name
        rel = str(f.relative_to(ROOT)).replace('\\', '/')
        if f.exists():
            continue
        try:
            href = json.load(urllib.request.urlopen(API + '/download?' + urllib.parse.urlencode({'public_key': key, 'path': path}), timeout=60))['href']
            data = urllib.request.urlopen(href, timeout=180).read()
            im = Image.open(io.BytesIO(data))
            w, h = im.size
            im = im.convert('RGB')
            im.thumbnail((1920, 1920))
            im.save(f, quality=84, optimize=True, progressive=True)
            if rel not in have:
                items.append({'file': rel, 'source': 'исходники: ' + NAMES.get(proj, proj), 'kind': 'исходники фотосессий', 'w': im.size[0], 'h': im.size[1], 'orig': f'{w}×{h}', 'note': key})
            print(proj, name, w, h, flush=True)
        except Exception as e:
            print('ошибка', proj, path, e, flush=True)
    (LIB / 'photos.json').write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding='utf-8')
print('готово', len(items))
