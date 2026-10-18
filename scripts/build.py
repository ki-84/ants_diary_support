#!/usr/bin/env python3
"""Render all locale pages with crawlable content; Python standard library only."""
import json
import html
import argparse
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://ki-84.github.io/ants_diary_support/'
STORE = 'https://apps.apple.com/app/id6760652790'
DATA = json.loads((ROOT / 'content/locales.json').read_text())
E = html.escape
OG_LOCALES = dict(zip(
    ['ja','en-US','ar-SA','ca','cs','da','de-DE','el','es-ES','es-MX','fi','fr-FR','he','hi','hr','hu','id','it','ko','ms','nl-NL','no','pl','pt-BR','pt-PT','ro','ru','sk','sv','th','tr','uk','vi','zh-Hans','zh-Hant'],
    ['ja_JP','en_US','ar_SA','ca_ES','cs_CZ','da_DK','de_DE','el_GR','es_ES','es_MX','fi_FI','fr_FR','he_IL','hi_IN','hr_HR','hu_HU','id_ID','it_IT','ko_KR','ms_MY','nl_NL','nb_NO','pl_PL','pt_BR','pt_PT','ro_RO','ru_RU','sk_SK','sv_SE','th_TH','tr_TR','uk_UA','vi_VN','zh_CN','zh_TW']
))


def filename(d):
    return f"index{d['suffix']}.html"


def url(d):
    return BASE if d['id'] == 'ja' else BASE + filename(d)


def lines(text):
    return '<br>'.join(E(x) for x in text.split('\n'))


def section(d, i):
    text = d['paragraphs'][i].split('\n')
    return text[0], text[1:]


def bodytext(text):
    return ''.join(f'<p>{E(t.lstrip("• "))}</p>' for t in text)


def store_link(d):
    # A country-neutral URL lets Apple choose the visitor's own storefront.
    # Use Apple's language code while retaining region-specific page content.
    lang = {'en-US':'en-US', 'ar-SA':'ar', 'no':'nb', 'es-MX':'es-MX'}.get(d['id'], d['lang'])
    return STORE + '?l=' + lang


def button(d, location, small=False):
    return f'<a class="store-button {"small" if small else ""}" data-cta="{location}" href="{E(store_link(d))}"><span>{E(d["download"])}</span><span aria-hidden="true">↗</span></a>'


def picture(d, name, alt, cls='', eager=False):
    return f'<img class="{cls}" src="assets/screenshots/{d["id"]}/{name}.webp" alt="{E(alt)}" width="720" height="1564" loading="{"eager" if eager else "lazy"}" decoding="async" {"fetchpriority=high" if eager else ""}>'


ICONS = [
 '<path d="M5 21C3 10 12 4 24 5c1 10-5 20-14 16M7 24 20 10M13 18l-1-6m5 2 6-1"/>',
 '<path d="M16 26S3 19 3 10a7 7 0 0 1 13-3 7 7 0 0 1 13 3c0 9-13 16-13 16Z"/>',
 '<path d="m16 3 11 4v8c0 7-11 14-11 14S5 22 5 15V7Z"/>',
 '<path d="m6 27 17-18M12 4c7-2 13 1 16 8M16 4l12 12"/>'
]


def render(d):
    roles_title, role_lines = section(d, 2)
    nest_title, nest_lines = section(d, 4)
    worlds_title, world_lines = section(d, 5)
    combat_title, combat_lines = section(d, 6)
    time_title, time_lines = section(d, 7)
    rank_title, rank_lines = section(d, 8)
    queen_title, queen_lines = section(d, 9)
    title = d['name'] + ' | ' + d['seo']
    desc = d['seo'] + '。' + d['paragraphs'][0] if d['lang'].startswith(('ja', 'zh')) else d['seo'] + '. ' + d['paragraphs'][0]
    alternates = '\n'.join(f'<link rel="alternate" hreflang="{x["lang"]}" href="{url(x)}">' for x in DATA)
    # Region-neutral Portuguese is also useful outside Portugal and Brazil.
    alternates += f'\n<link rel="alternate" hreflang="pt" href="{BASE}index-pt-PT.html">'
    alternates += f'\n<link rel="alternate" hreflang="x-default" href="{BASE}index-en.html">'
    schema = {'@context':'https://schema.org', '@type':'SoftwareApplication', 'name':d['name'], 'url':url(d),
              'description':desc, 'applicationCategory':'GameApplication', 'applicationSubCategory':'Strategy',
              'operatingSystem':'iOS 17.0 or later', 'inLanguage':d['lang'], 'installUrl':store_link(d),
              'image':BASE+'assets/icon.webp', 'screenshot':[BASE+f'assets/screenshots/{d["id"]}/{n}.webp' for n in ['2_gameplay','1_nest_after','5_victory']],
              'author':{'@type':'Person','name':'Nobuaki Kuwabara'},
              'offers':{'@type':'Offer','price':'0','priceCurrency':'USD','url':store_link(d)}}
    # Do not fabricate reviews or ratings to qualify for search rich results.
    schema_json = json.dumps(schema, ensure_ascii=False).replace('<','\\u003c')
    locale_links = ''.join(f'<a lang="{x["lang"]}" hreflang="{x["lang"]}" href="{filename(x)}" {"aria-current=page" if x["id"]==d["id"] else ""}>{E(x["native"])}</a>' for x in DATA)
    roles = ''
    for i, role in enumerate(role_lines):
        text = role.lstrip('• ')
        # Keep language-specific punctuation and approved role explanations intact.
        parts = text.replace('：', ':').split(':', 1)
        name = parts[0]
        detail = parts[1].strip() if len(parts)>1 else ''
        roles += f'<article class="role role-{i}"><svg viewBox="0 0 32 32" aria-hidden="true">{ICONS[i]}</svg><span class="role-number">0{i+1}</span><h3>{E(name)}</h3><p>{E(detail)}</p></article>'
    hero = d['hero'][0].split('\n')
    suffix=d['support_suffix']
    return f'''<!doctype html>
<html lang="{d['lang']}" dir="{'rtl' if d['lang'] in ['ar','he'] else 'ltr'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="theme-color" content="#0d1c18">
<meta name="apple-itunes-app" content="app-id=6760652790">
<link rel="canonical" href="{url(d)}">
<link rel="sitemap" type="application/xml" href="{BASE}sitemap.xml">
{alternates}
<meta property="og:type" content="website">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{url(d)}">
<meta property="og:image" content="{BASE}assets/og-{d['id']}.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{E(d['name']+' — '+d['seo'])}">
<meta property="og:locale" content="{OG_LOCALES[d['id']]}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="stylesheet" href="assets/site.css?v=20261018">
<script type="application/ld+json">{schema_json}</script>
<script src="assets/site.js?v=20261018" defer></script>
</head>
<body>
<a class="skip-link" href="#main">{E(d['explore'])}</a>
<header class="header"><div class="nav wrap">
<a class="brand" href="{filename(d)}" aria-label="{E(d['name'])}"><img src="assets/icon.webp" alt="" width="40" height="40"><span>{E(d['name'])}</span></a>
<nav aria-label="{E(d['explore'])}"><a class="nav-explore" href="#worlds">{E(d['explore'])}</a>
<details class="languages"><summary><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18"/></svg><span>{E(d['native'])}</span><span aria-hidden="true">⌄</span></summary><div class="language-menu" aria-label="{E(d['language'])}">{locale_links}</div></details>
</nav></div></header>
<main id="main">
<section class="hero"><div class="hero-glow" aria-hidden="true"></div><div class="fireflies" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div>
<div class="wrap hero-grid"><div class="hero-copy">
<p class="eyebrow"><span class="live-dot"></span>{E(d['name'])} <span class="eyebrow-line"></span> iOS</p>
<h1>{E(hero[0])}<br><em>{E(hero[1])}</em></h1>
<p class="hero-category">{E(d['seo'])}</p>
<p class="hero-intro">{E(d['intro'])}</p>
<div class="hero-actions">{button(d,'hero')}<a class="text-link" href="#worlds">{E(d['explore'])}<span aria-hidden="true"> ↓</span></a></div>
<p class="requirements">{E(d['free'])}<span> / </span>{E(d['device'])}<span> / </span>iOS 17.0+</p>
</div><div class="hero-visual">
<span class="giant-number" aria-hidden="true">100</span>
<div class="phone phone-back">{picture(d,'1_nest_after',nest_title,eager=True)}</div>
<div class="phone phone-front">{picture(d,'2_gameplay',worlds_title,eager=True)}</div>
<div class="orbit-label"><span aria-hidden="true">↗</span> {E(d['subtitle'])}</div>
</div></div><a class="scroll-cue" href="#worlds" aria-label="{E(d['explore'])}"><span></span>↓</a></section>
<div class="fact-strip"><div class="wrap facts">
<div><strong>100</strong><span>{E(d['subtitle'])}</span></div>
<div><strong>04</strong><span>{E(roles_title)}</span></div>
<div><strong>02</strong><span>{E(worlds_title)}</span></div>
<div><strong>06</strong><span>{E(rank_title)}</span></div>
</div></div>
<section id="worlds" class="section wrap worlds">
<div class="section-heading"><div><p class="eyebrow">01 <span class="eyebrow-line"></span> {E(worlds_title)}</p><h2>{lines(d['hero'][2])}</h2></div><div class="section-lead"><h3>{E(nest_title)}</h3><p>{E(nest_lines[0].lstrip('• '))}</p></div></div>
<div class="world-grid"><figure class="world-card surface"><div class="world-image">{picture(d,'2_gameplay',world_lines[0].lstrip('• '))}</div><figcaption><span class="world-index">01 /</span><p>{E(world_lines[0].lstrip('• '))}</p></figcaption></figure>
<figure class="world-card underground"><div class="world-image">{picture(d,'1_nest_after',world_lines[1].lstrip('• '))}</div><figcaption><span class="world-index">02 /</span><p>{E(world_lines[1].lstrip('• '))}</p></figcaption></figure></div>
<p class="world-footnote">{E(nest_lines[1].lstrip('• '))}</p>
</section>
<section id="strategy" class="strategy-section"><div class="wrap section">
<p class="eyebrow">02 <span class="eyebrow-line"></span> {E(roles_title)}</p><div class="section-heading"><h2>{lines(d['hero'][3])}</h2><p class="section-lead">{E(d['paragraphs'][3])}</p></div>
<div class="roles">{roles}</div>
<div class="queen"><span class="queen-symbol" aria-hidden="true">♛</span><div><h3>{E(queen_title)}</h3>{bodytext(queen_lines)}</div><div class="queen-numbers" aria-hidden="true"><b>3×</b><span>↔</span><b>8×</b></div></div>
</div></section>
<section class="section wrap combat"><div class="combat-art">{picture(d,'4_combat',combat_title)}<span class="combat-ring" aria-hidden="true"></span></div><div class="combat-copy"><p class="eyebrow">03 <span class="eyebrow-line"></span> {E(combat_title)}</p><h2>{lines(d['hero'][1])}</h2><p>{E(combat_lines[0])}</p><div class="combat-rule"></div><h3>{E(d['paragraphs'][0])}</h3><p>{E(d['paragraphs'][3])}</p>{button(d,'combat')}</div></section>
<section id="challenge" class="challenge-section"><div class="section wrap challenge-grid"><div><p class="eyebrow">04 <span class="eyebrow-line"></span> {E(time_title)}</p><h2>{lines(d['hero'][4])}</h2><h3>{E(rank_title)}</h3>{bodytext(rank_lines)}<h3>{E(time_title)}</h3>{bodytext(time_lines)}<div class="goal-number" aria-hidden="true">100<span> / ANTS</span></div></div><div class="victory-art"><div class="victory-halo" aria-hidden="true"></div><div class="phone">{picture(d,'5_victory',rank_title)}</div></div></div></section>
<section class="download-section wrap"><img class="ant-portrait" src="assets/ant.webp" width="192" height="192" alt="" loading="lazy"><p class="eyebrow">{E(d['name'])}</p><h2>{lines(d['hero'][1])}</h2><p>{E(d['paragraphs'][0])}</p>{button(d,'footer')}<p class="requirements">{E(d['free'])} / {E(d['device'])} / iOS 17.0+</p></section>
</main>
<footer class="footer wrap"><a class="brand" href="{filename(d)}"><img src="assets/icon.webp" alt="" width="32" height="32"><span>{E(d['name'])}</span></a><div class="footer-links"><a href="support{suffix}.html" {'lang="en"' if suffix=='-en' and d['lang']!='en' else ''}>{E(d['support'])}{' (English)' if suffix=='-en' and d['lang']!='en' else ''}</a><a href="privacy-policy{suffix}.html" {'lang="en"' if suffix=='-en' and d['lang']!='en' else ''}>{E(d['privacy'])}{' (English)' if suffix=='-en' and d['lang']!='en' else ''}</a><a href="#languages">{E(d['language'])}</a></div><small>© 2026 Nobuaki Kuwabara</small></footer>
<div id="languages" class="all-languages wrap" aria-label="{E(d['language'])}">{locale_links}</div>
<div class="mobile-download"><img src="assets/icon.webp" width="40" height="40" alt=""><div><strong>{E(d['name'])}</strong><small>{E(d['free'])}</small></div>{button(d,'mobile',True)}</div>
</body></html>
'''


def artifacts():
    files={filename(d): render(d) for d in DATA}
    ns='http://www.sitemaps.org/schemas/sitemap/0.9'
    ET.register_namespace('', ns)
    root=ET.Element('{'+ns+'}urlset')
    for d in DATA:
        item=ET.SubElement(root,'{'+ns+'}url')
        ET.SubElement(item,'{'+ns+'}loc').text=url(d)
    # Existing legal/support pages remain crawlable and are also discoverable here.
    for p in sorted(ROOT.glob('*.html')):
        if p.name.startswith(('support', 'privacy-policy')):
            item=ET.SubElement(root,'{'+ns+'}url')
            ET.SubElement(item,'{'+ns+'}loc').text=BASE+p.name
    ET.indent(root)
    files['sitemap.xml']='<?xml version="1.0" encoding="utf-8"?>\n'+ET.tostring(root,encoding='unicode')+'\n'
    return files


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    generated=artifacts()
    if args.check:
        stale=[f for f,content in generated.items() if not (ROOT/f).exists() or (ROOT/f).read_text()!=content]
        if stale:
            raise SystemExit('Regenerate pages: '+', '.join(stale))
    else:
        for f,content in generated.items():
            (ROOT/f).write_text(content)
        (ROOT/'.nojekyll').touch()
    print(f'{len(DATA)} locale pages and sitemap {"verified" if args.check else "generated"}.')

if __name__=='__main__':
    main()
