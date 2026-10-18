#!/usr/bin/env python3
"""Import approved app copy and optimize real screenshots. Requires Pillow."""
import argparse
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
# App Store locales, HTML language tags, existing URL suffixes, native names,
# natural search phrases and localized interface copy. No browser translation required.
ROWS = '''ja|ja||日本語|アリ育成・巣作りシミュレーション × リアルタイム戦略|App Storeでダウンロード|無料・広告あり|ゲームを見る|サポート|プライバシーポリシー|言語|iPhone向け
 en-US|en|-en|English|Ant colony simulator & real-time strategy game|Download on the App Store|Free · Contains ads|Explore the game|Support|Privacy policy|Language|For iPhone
 ar-SA|ar|-ar|العربية|لعبة محاكاة مستعمرة النمل واستراتيجية بالوقت الحقيقي|تنزيل من App Store|مجاني · يتضمن إعلانات|اكتشف اللعبة|الدعم|سياسة الخصوصية|اللغة|لأجهزة iPhone
 ca|ca|-ca|Català|Joc de simulació de colònies de formigues i estratègia en temps real|Descarrega a l’App Store|Gratuït · Conté anuncis|Descobreix el joc|Assistència|Política de privadesa|Idioma|Per a iPhone
 cs|cs|-cs|Čeština|Simulátor mravenčí kolonie a strategická hra v reálném čase|Stáhnout v App Storu|Zdarma · Obsahuje reklamy|Prozkoumat hru|Podpora|Zásady ochrany soukromí|Jazyk|Pro iPhone
 da|da|-da|Dansk|Myrekoloni-simulator og strategispil i realtid|Hent i App Store|Gratis · Indeholder reklamer|Udforsk spillet|Support|Anonymitetspolitik|Sprog|Til iPhone
 de-DE|de|-de|Deutsch|Ameisenkolonie-Simulator und Echtzeit-Strategiespiel|Im App Store laden|Kostenlos · Enthält Werbung|Spiel entdecken|Support|Datenschutz|Sprache|Für iPhone
 el|el|-el|Ελληνικά|Προσομοίωση αποικίας μυρμηγκιών και στρατηγική σε πραγματικό χρόνο|Λήψη από το App Store|Δωρεάν · Περιέχει διαφημίσεις|Ανακάλυψε το παιχνίδι|Υποστήριξη|Πολιτική απορρήτου|Γλώσσα|Για iPhone
 es-ES|es|-es|Español|Simulador de colonias de hormigas y estrategia en tiempo real|Descargar en el App Store|Gratis · Contiene anuncios|Descubre el juego|Soporte|Política de privacidad|Idioma|Para iPhone
 es-MX|es-MX|-es-MX|Español (México)|Simulador de hormiguero y juego de estrategia en tiempo real|Descárgalo en el App Store|Gratis · Contiene anuncios|Descubre el juego|Soporte|Política de privacidad|Idioma|Para iPhone
 fi|fi|-fi|Suomi|Muurahaisyhdyskunnan simulaattori ja reaaliaikainen strategiapeli|Lataa App Storesta|Ilmainen · Sisältää mainoksia|Tutustu peliin|Tuki|Tietosuojakäytäntö|Kieli|iPhonelle
 fr-FR|fr|-fr|Français|Simulateur de colonie de fourmis et jeu de stratégie en temps réel|Télécharger dans l’App Store|Gratuit · Contient des publicités|Découvrir le jeu|Assistance|Politique de confidentialité|Langue|Pour iPhone
 he|he|-he|עברית|סימולטור מושבת נמלים ומשחק אסטרטגיה בזמן אמת|הורדה ב-App Store|חינם · כולל פרסומות|גלו את המשחק|תמיכה|מדיניות פרטיות|שפה|ל-iPhone
 hi|hi|-hi|हिन्दी|चींटी कॉलोनी सिम्युलेटर और रियल-टाइम रणनीति गेम|App Store से डाउनलोड करें|मुफ़्त · विज्ञापन शामिल हैं|गेम देखें|सहायता|गोपनीयता नीति|भाषा|iPhone के लिए
 hr|hr|-hr|Hrvatski|Simulator kolonije mrava i strateška igra u stvarnom vremenu|Preuzmi na App Storeu|Besplatno · Sadrži oglase|Istraži igru|Podrška|Pravila privatnosti|Jezik|Za iPhone
 hu|hu|-hu|Magyar|Hangyakolónia-szimulátor és valós idejű stratégiai játék|Letöltés az App Store-ból|Ingyenes · Hirdetéseket tartalmaz|Fedezd fel a játékot|Támogatás|Adatvédelmi irányelvek|Nyelv|iPhone-ra
 id|id|-id|Bahasa Indonesia|Simulator koloni semut dan game strategi waktu nyata|Unduh di App Store|Gratis · Berisi iklan|Jelajahi game|Dukungan|Kebijakan privasi|Bahasa|Untuk iPhone
 it|it|-it|Italiano|Simulatore di colonie di formiche e strategia in tempo reale|Scarica su App Store|Gratis · Contiene pubblicità|Scopri il gioco|Supporto|Informativa sulla privacy|Lingua|Per iPhone
 ko|ko|-ko|한국어|개미 군집 키우기 시뮬레이션 & 실시간 전략 게임|App Store에서 다운로드|무료 · 광고 포함|게임 살펴보기|지원|개인정보 처리방침|언어|iPhone용
 ms|ms|-ms|Bahasa Melayu|Simulator koloni semut dan permainan strategi masa nyata|Muat turun di App Store|Percuma · Mengandungi iklan|Terokai permainan|Sokongan|Dasar privasi|Bahasa|Untuk iPhone
 nl-NL|nl|-nl|Nederlands|Mierenkolonie-simulator en realtime strategiespel|Download in de App Store|Gratis · Bevat advertenties|Ontdek het spel|Ondersteuning|Privacybeleid|Taal|Voor iPhone
 no|nb|-no|Norsk bokmål|Maurkoloni-simulator og strategispill i sanntid|Last ned i App Store|Gratis · Inneholder annonser|Utforsk spillet|Brukerstøtte|Personvernerklæring|Språk|For iPhone
 pl|pl|-pl|Polski|Symulator kolonii mrówek i strategia czasu rzeczywistego|Pobierz w App Store|Za darmo · Zawiera reklamy|Odkryj grę|Wsparcie|Polityka prywatności|Język|Na iPhone’a
 pt-BR|pt-BR|-pt-BR|Português (Brasil)|Simulador de formigueiro e jogo de estratégia em tempo real|Baixe na App Store|Grátis · Contém anúncios|Conheça o jogo|Suporte|Política de privacidade|Idioma|Para iPhone
 pt-PT|pt-PT|-pt-PT|Português (Portugal)|Simulador de formigueiro e jogo de estratégia em tempo real|Descarregar na App Store|Grátis · Contém publicidade|Descobre o jogo|Suporte|Política de privacidade|Idioma|Para iPhone
 ro|ro|-ro|Română|Simulator de colonie de furnici și strategie în timp real|Descarcă din App Store|Gratuit · Conține reclame|Descoperă jocul|Asistență|Politica de confidențialitate|Limbă|Pentru iPhone
 ru|ru|-ru|Русский|Симулятор муравейника и стратегия в реальном времени|Загрузить в App Store|Бесплатно · Есть реклама|Узнать об игре|Поддержка|Политика конфиденциальности|Язык|Для iPhone
 sk|sk|-sk|Slovenčina|Simulátor mravčej kolónie a stratégia v reálnom čase|Stiahnuť v App Store|Zadarmo · Obsahuje reklamy|Preskúmaj hru|Podpora|Ochrana súkromia|Jazyk|Pre iPhone
 sv|sv|-sv|Svenska|Myrkoloni-simulator och strategispel i realtid|Hämta i App Store|Gratis · Innehåller annonser|Utforska spelet|Support|Integritetspolicy|Språk|För iPhone
 th|th|-th|ไทย|เกมจำลองอาณานิคมมดและวางกลยุทธ์แบบเรียลไทม์|ดาวน์โหลดบน App Store|ฟรี · มีโฆษณา|สำรวจเกม|ช่วยเหลือ|นโยบายความเป็นส่วนตัว|ภาษา|สำหรับ iPhone
 tr|tr|-tr|Türkçe|Karınca kolonisi simülatörü ve gerçek zamanlı strateji oyunu|App Store’dan indir|Ücretsiz · Reklam içerir|Oyunu keşfet|Destek|Gizlilik politikası|Dil|iPhone için
 uk|uk|-uk|Українська|Симулятор мурашника та стратегія в реальному часі|Завантажити в App Store|Безкоштовно · Містить рекламу|Дізнатися про гру|Підтримка|Політика конфіденційності|Мова|Для iPhone
 vi|vi|-vi|Tiếng Việt|Game mô phỏng đàn kiến và chiến thuật thời gian thực|Tải về trên App Store|Miễn phí · Có quảng cáo|Khám phá game|Hỗ trợ|Chính sách quyền riêng tư|Ngôn ngữ|Dành cho iPhone
 zh-Hans|zh-Hans|-zh-Hans|简体中文|蚂蚁养成与蚁巢模拟 · 即时策略游戏|在 App Store 下载|免费 · 含广告|探索游戏|支持|隐私政策|语言|适用于 iPhone
 zh-Hant|zh-Hant|-zh-Hant|繁體中文|螞蟻養成與蟻巢模擬 · 即時策略遊戲|在 App Store 下載|免費 · 含廣告|探索遊戲|支援|隱私權政策|語言|適用於 iPhone'''


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--app-root', type=Path, default=ROOT.parent)
    app = p.parse_args().app_root
    promo = json.loads((app / 'AntsDiary_Promo/localized_copy.json').read_text())
    locales = []
    for row in ROWS.splitlines():
        parts = row.strip().split('|')
        keys = ['id', 'lang', 'suffix', 'native', 'seo', 'download', 'free', 'explore', 'support', 'privacy', 'language', 'device']
        assert len(keys) == len(parts), parts
        d = dict(zip(keys, parts))
        meta = json.loads((app / f"fastlane/metadata_src/{d['id']}.json").read_text())
        d.update(name=meta['name'], subtitle=meta['subtitle'], intro=meta['description'].split('\n\n')[1],
                 paragraphs=[s.strip() for s in meta['description'].split('\n\n')], hero=promo[d['id']],
                 keywords=meta['keywords'])
        d['support_suffix'] = {'es-MX':'-es', 'pt-PT':'-pt-BR'}.get(d['id'], d['suffix'] if (ROOT / f"support{d['suffix']}.html").exists() else '-en')
        dest = ROOT / 'assets/screenshots' / d['id']
        dest.mkdir(parents=True, exist_ok=True)
        for name in ['2_gameplay', '1_nest_after', '4_combat', '5_victory']:
            source = app / f"fastlane/screenshots/{d['id']}/{name}.png"
            im = Image.open(source).convert('RGB')
            im.thumbnail((720, 1565), Image.Resampling.LANCZOS)
            im.save(dest / f'{name}.webp', quality=84, method=6)
        locales.append(d)
    (ROOT / 'content/locales.json').write_text(json.dumps(locales, ensure_ascii=False, indent=2) + '\n')
    for name, src, size in [
        ('icon', 'AppIcon.appiconset/AppIcon.png', (192,192)),
        ('ant', 'TitleAnt.imageset/TitleAnt.png', (384,384)),
        ('forest', 'SurfaceBackground.imageset/SurfaceBackground.png', (971,1620))]:
        im = Image.open(app / 'AntsDiary/Resources/Assets.xcassets' / src).convert('RGB')
        im.thumbnail(size)
        im.save(ROOT / f'assets/{name}.webp', quality=90, method=6)
        if name == 'icon':
            im.save(ROOT / 'assets/apple-touch-icon.png')
            im.resize((32,32)).save(ROOT / 'favicon.ico')
    print(f'Imported {len(locales)} locales and {len(locales)*4} actual screenshots.')

if __name__ == '__main__':
    main()
