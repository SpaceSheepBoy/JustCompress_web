"""Preserve the published Mac-only app in existing directory languages.

The product page remains English; each localized link labels that destination.
Product facts and assets come from the maintained, verified portfolio snapshot.
"""
from pathlib import Path
from html import escape as E
import json
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
# Short directory labels, not new translated articles or product pages.
COPY = {
    'en': ('Record your screen and camera together on Mac', 'Product details', 'Download for Mac'),
    'fr': ('Enregistrez votre écran et votre caméra ensemble sur Mac', 'Détails en anglais', 'Télécharger pour Mac'),
    'ja': ('Macの画面とカメラを同時に録画', '製品情報（英語）', 'Mac版をダウンロード'),
    'es': ('Graba la pantalla y la cámara a la vez en Mac', 'Información en inglés', 'Descargar para Mac'),
    'zh-Hans': ('在 Mac 上同步录制屏幕与摄像头', '产品详情（英文）', '下载 Mac 版'),
    'zh-Hant': ('在 Mac 上同步錄製螢幕與攝影機', '產品詳情（英文）', '下載 Mac 版'),
    'de': ('Bildschirm und Kamera auf dem Mac gleichzeitig aufnehmen', 'Produktdetails auf Englisch', 'Für Mac laden'),
    'pt': ('Grave a tela e a câmera ao mesmo tempo no Mac', 'Detalhes em inglês', 'Baixar para Mac'),
    'it': ('Registra schermo e videocamera insieme sul Mac', 'Dettagli in inglese', 'Scarica per Mac'),
    'ko': ('Mac에서 화면과 카메라를 동시에 녹화', '제품 정보(영어)', 'Mac용 다운로드'),
}


def apply():
    app = next(a for a in json.loads((ROOT/'scripts/app-portfolio.json').read_text())['apps']
               if a['id'] == '6820696330')
    home = ROOT/'index.html'
    soup = BeautifulSoup(home.read_text(), 'html.parser')
    for old in soup.select('[data-camrecorder-release]'):
        old.decompose()
    announcement = BeautifulSoup(
        '<section class="guide-enhancement" data-camrecorder-release>'
        '<h2>Record your screen and camera on Mac</h2>'
        '<p>CamRecorder is now on the Mac App Store. Record a window or full screen with your camera, computer audio and microphone.</p>'
        '<a class="guide-button" href="/apps/camrecorder/">Meet CamRecorder for Mac →</a></section>', 'html.parser')
    footer = soup.main.find('footer', recursive=False)
    if footer:
        footer.insert_before(announcement)
    else:
        soup.main.append(announcement)
    home.write_text(str(soup))
    for lang, (benefit, details, download) in COPY.items():
        path = ROOT/'apps'/('index.html' if lang == 'en' else lang+'/index.html')
        if not path.exists():
            continue
        soup = BeautifulSoup(path.read_text(), 'html.parser')
        catalog = soup.select_one('.app-catalog')
        if not catalog:
            continue
        intro = json.loads((ROOT/'locales/directory-platform.json').read_text())[lang]
        heading = soup.select_one('.catalog-heading')
        paragraph = heading.find('p', recursive=False)
        if paragraph:
            paragraph.string = intro
        else:
            paragraph = soup.new_tag('p')
            paragraph.string = intro
            heading.h1.insert_after(paragraph)
        for meta in soup.select('meta[name="description"],meta[property="og:description"]'):
            meta['content'] = intro
        for card in catalog.select('.app-card'):
            if card.select_one('a[href*="id6820696330"]'):
                card.decompose()
        icon = app['icon']
        shots = ''.join(f'<img src="{E(s["src"])}" width="{s["width"]}" height="{s["height"]}" alt="CamRecorder" loading="lazy" class="catalog-shot">'
                        for s in app['screenshots'])
        card = (f'<article class="app-card" id="camrecorder" data-app="6820696330">'
                f'<a class="catalog-identity" href="/apps/camrecorder/" lang="en"><img class="app-icon" src="{E(icon["src"])}" width="{icon["width"]}" height="{icon["height"]}" alt="" loading="lazy">'
                f'<div><h2>{E(app["name"])}</h2></div></a><p class="benefit">{E(benefit)}</p>'
                f'<figure class="catalog-gallery"><div class="catalog-shots">{shots}</div></figure>'
                f'<input id="name-6820696330" type="hidden" value="{E(app["name"])}">'
                f'<div class="actions"><a class="portfolio-button" href="{E(app["store_url"])}">{E(download)} ↗</a></div>'
                f'<p><a href="/apps/camrecorder/" lang="en">{E(details)} →</a></p></article>')
        catalog.append(BeautifulSoup(card, 'html.parser'))
        # Match the visible directory in structured data without inventing offers.
        for node in soup.select('script[type="application/ld+json"]'):
            data = json.loads(node.string or node.get_text())
            if data.get('@type') == 'CollectionPage':
                entries = data['mainEntity']['itemListElement']
                if not any(e.get('url', '').endswith('/apps/camrecorder/') for e in entries):
                    entries.append({'@type': 'ListItem', 'position': len(entries)+1,
                                    'name': app['name'], 'url': app['website']})
                node.string = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
        path.write_text(str(soup))


if __name__ == '__main__':
    apply()
