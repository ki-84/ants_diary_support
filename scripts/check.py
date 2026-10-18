#!/usr/bin/env python3
"""Validate published pages, locale relationships, assets and existing legal links."""
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
from xml.etree import ElementTree as ET
from build import ROOT, BASE, DATA, filename, url

class Page(HTMLParser):
    def __init__(self,text):
        super().__init__(convert_charrefs=True)
        self.tags=[]; self.ids=[]; self.h1=0; self.in_ld=False; self.ld=''
        self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs); self.tags.append((tag,a))
        if 'id' in a:self.ids.append(a['id'])
        if tag=='h1':self.h1+=1
        if tag=='script' and a.get('type')=='application/ld+json':self.in_ld=True
    def handle_endtag(self,tag):
        if tag=='script':self.in_ld=False
    def handle_data(self,data):
        if self.in_ld:self.ld+=data

errors=[]
expected={(d['lang'],url(d)) for d in DATA}|{('pt',BASE+'index-pt-PT.html'),('x-default',BASE+'index-en.html')}
canonicals=[]
for d in DATA:
    name=filename(d); text=(ROOT/name).read_text(); page=Page(text)
    def require(ok,message):
        if not ok:errors.append(name+': '+message)
    require(page.h1==1,'exactly one H1 required')
    require(len(page.ids)==len(set(page.ids)),'duplicate IDs')
    html=next(a for t,a in page.tags if t=='html')
    require(html['lang']==d['lang'],'HTML language mismatch')
    require(html['dir']==('rtl' if d['lang'] in ['ar','he'] else 'ltr'),'text direction')
    alternate={(a['hreflang'],a['href']) for t,a in page.tags if t=='link' and a.get('rel')=='alternate'}
    require(alternate==expected,'incomplete reciprocal hreflang')
    canonical=[a['href'] for t,a in page.tags if t=='link' and a.get('rel')=='canonical']
    require(canonical==[url(d)],'self canonical missing')
    canonicals+=canonical
    schema=json.loads(page.ld)
    require(schema['offers']['price']=='0' and schema['installUrl'].startswith('https://apps.apple.com/app/id6760652790'),'App Store identity/price')
    require('aggregateRating' not in schema,'unverified rating')
    downloads=[a for t,a in page.tags if t=='a' and 'data-cta' in a]
    require(len(downloads)==4,'download CTA missing')
    require(len({a['href'] for a in downloads})==1,'inconsistent CTA destination')
    for tag,a in page.tags:
        if tag=='img':require('alt' in a and 'width' in a and 'height' in a,'image accessibility/dimensions')
        ref=a.get('src') if tag in ['img','script'] else a.get('href') if tag in ['a','link'] else a.get('content') if a.get('property')=='og:image' else None
        if not ref:continue
        if ref.startswith(BASE):ref=ref[len(BASE):] or 'index.html'
        parts=urlsplit(ref)
        if parts.scheme or parts.netloc:continue
        dest=ROOT/(unquote(parts.path) or name)
        require(dest.is_file(),'missing local file '+ref)
        if parts.fragment and (not parts.path or parts.path==name):require(parts.fragment in page.ids,'missing anchor '+ref)
    # No credentials or build dependency is shipped to the static site.
    require('ASC_KEY' not in text and 'AuthKey_' not in text,'credential reference')
require_unique=len(canonicals)==len(set(canonicals))
if not require_unique:errors.append('duplicate canonical URLs')
sitemap=ET.parse(ROOT/'sitemap.xml')
locations=[e.text for e in sitemap.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
if not set(canonicals).issubset(locations):errors.append('locale missing from sitemap')
if len(locations)!=len(set(locations)):errors.append('duplicate sitemap URLs')
for loc in locations:
    path=loc[len(BASE):] or 'index.html'
    if not (ROOT/path).is_file():errors.append('sitemap URL missing '+loc)
if errors:raise SystemExit('\n'.join(errors))
print(f'PASS: {len(DATA)} locale pages, {len(locations)} sitemap URLs, reciprocal hreflang, local links, images, structured data, and 140 download links.')
