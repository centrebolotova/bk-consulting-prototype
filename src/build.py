# Собирает цельные страницы: стили и скрипты вшиваются в каждый HTML,
# чтобы файл открывался сам по себе (в окне просмотра, на GitHub Pages, по ссылке).
import pathlib

src = pathlib.Path(__file__).parent
out = src.parent
css = (src / 'style.css').read_text(encoding='utf-8') + (src / 'variants.css').read_text(encoding='utf-8')
js = (src / 'app.js').read_text(encoding='utf-8') + (src / 'variants.js').read_text(encoding='utf-8')

NOINDEX = '<meta name="robots" content="noindex, nofollow">'

for f in sorted(src.glob('*.html')):
    s = f.read_text(encoding='utf-8')
    s = s.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n' + NOINDEX, 1)  # прототип не должен попадать в поиск
    s = s.replace('<link rel="stylesheet" href="style.css">', '<style>\n' + css + '\n</style>')
    s = s.replace('<script src="app.js"></script>', '<script>\n' + js + '\n</script>')
    # свои фото из img/ вшиваем в страницу, чтобы файл открывался без папки рядом
    import base64
    for img in (out / 'img').glob('*.jpg'):
        ref = 'img/' + img.name
        if ref in s:
            s = s.replace(ref, 'data:image/jpeg;base64,' + base64.b64encode(img.read_bytes()).decode())
    (out / f.name).write_text(s, encoding='utf-8')
    print('собрано', f.name, len(s))
