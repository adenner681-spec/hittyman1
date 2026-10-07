#!/usr/bin/env python3
"""Baut die CMS-Module aus src/ zusammen.

Ausgabe pro Seite: <ordner>/modul-sourcecode.html (beginnt mit <style>) und
eine Vorschau. Das JavaScript-Modul ist für alle Seiten gleich.
"""
import json, os, re, html

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
SITE = "https://www.rudolf-ritzinger.com"
IMG_MODULE = "/incms_files/filebrowser"
IMG_PREVIEW = SITE + "/incms_files/filebrowser"
# Jede Anfrage öffnet das CMS-Popup „terminanfrage“ (Auswahl gesetzlich / privat).
ANFRAGE = "?uid=2#popup-terminanfrage"

# PLATZHALTER – sobald die Landingpages stehen (eigene Domain oder Unterseite), hier eintragen.
# Bis dahin springen die Buttons auf der Startseite zum Bereich „Mehr als Therapie“.
LINK_FAMILY_ZEN = "?uid=2#mehr-als-therapie"
LINK_ONLINE_KURS = "?uid=2#mehr-als-therapie"
# Anfrage-Ziel auf der Landingpage: absolut, damit es auch auf einer eigenen Domain funktioniert.
ANFRAGE_LANDING = "https://www.rudolf-ritzinger.com/?uid=2#popup-terminanfrage"

SYMBOLS = {}

def svg(body, w="2", fill="none"):
    """Icon als Referenz auf ein Sprite-Symbol (spart viel HTML)."""
    key = "rr-i%d" % (len(SYMBOLS) + 1)
    for k, v in SYMBOLS.items():
        if v == (body, w, fill):
            key = k
            break
    SYMBOLS[key] = (body, w, fill)
    return '<svg viewBox="0 0 24 24" aria-hidden="true"><use href="#%s"/></svg>' % key

def sprite():
    out = []
    for key, (body, w, fill) in SYMBOLS.items():
        out.append('<symbol id="%s" viewBox="0 0 24 24"><g fill="%s" stroke="%s" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round">%s</g></symbol>'
                   % (key, fill, "none" if fill == "currentColor" else "currentColor", w, body))
    return '<svg class="rr-sprite" aria-hidden="true" focusable="false">' + "".join(out) + "</svg>"

def _old_svg(body, w="2", fill="none"):
    return ('<svg viewBox="0 0 24 24" fill="%s" stroke="currentColor" stroke-width="%s" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % (fill, w, body))

STAR = svg('<path d="M12 2l3 6.9 7.5.6-5.7 4.9 1.8 7.3L12 17.8 5.4 21.7l1.8-7.3L1.5 9.5 9 8.9z"/>', "0", "currentColor")
ICONS = {
    "arrow": svg('<path d="M5 12h14M13 6l6 6-6 6"/>', "2.2"),
    "arrow-s": svg('<path d="M5 12h14M13 6l6 6-6 6"/>', "2.2"),
    "arrow-l": svg('<path d="M19 12H5M11 6l-6 6 6 6"/>', "2.2"),
    "check": svg('<path d="M5 12l5 5L20 7"/>', "3"),
    "check-o": svg('<circle cx="12" cy="12" r="10"/><path d="M8 12l3 3 5-6"/>', "2"),
    "stars5": '<div class="rr-stars" aria-label="5 von 5 Sternen">' + STAR * 5 + '</div>',
    "i-user": svg('<circle cx="12" cy="7" r="4"/><path d="M5 21v-1a7 7 0 0 1 14 0v1"/>', "1.8"),
    "i-family": svg('<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>', "1.8"),
    "i-brain": svg('<path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24A2.5 2.5 0 0 1 9.5 2z"/><path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24A2.5 2.5 0 0 0 14.5 2z"/>', "1.8"),
    "i-globe": svg('<circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15 15 0 0 1 0 20M12 2a15 15 0 0 0 0 20"/>', "1.8"),
    "i-shield": svg('<path d="M12 2l8 4v6c0 5-3.5 8.5-8 10-4.5-1.5-8-5-8-10V6z"/><path d="M9 12l2 2 4-4"/>', "1.8"),
    "i-spark": svg('<path d="M12 3l1.9 5.8L20 9.3l-4.8 3.7 1.7 6-4.9-3.6L7.1 19l1.7-6L4 9.3l6.1-.5z"/>', "1.8"),
    "i-screen": svg('<rect x="2" y="4" width="20" height="13" rx="2"/><path d="M8 21h8M12 17v4"/><path d="M10 8.5l4 2-4 2z"/>', "1.8"),
    "i-info": svg('<circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/>', "1.8"),
    "i-pin": svg('<path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>', "2"),
    "i-eye": svg('<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>', "1.8"),
    "i-pulse": svg('<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>', "1.8"),
    "i-vr": svg('<path d="M3 8a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2h-4l-1.5-2.5a1.7 1.7 0 0 0-3 0L9 17H5a2 2 0 0 1-2-2z"/><circle cx="8" cy="11" r="1.5"/><circle cx="16" cy="11" r="1.5"/>', "1.8"),
    "i-tablet": svg('<rect x="4" y="2" width="16" height="20" rx="2.5"/><path d="M8 9l2 2-2 2M12 13h4"/>', "1.8"),
    "i-bolt": svg('<path d="M13 2L3 14h9l-1 8 10-12h-9z"/>', "1.8"),
    "i-system": svg('<circle cx="12" cy="5" r="2.5"/><circle cx="5" cy="18" r="2.5"/><circle cx="19" cy="18" r="2.5"/><path d="M10.8 7.2L6.2 15.8M13.2 7.2l4.6 8.6M7.5 18h9"/>', "1.8"),
    "i-heart": svg('<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8l1 1.1L12 21l7.8-7.5 1-1.1a5.5 5.5 0 0 0 0-7.8z"/>', "1.8"),
    "i-chat": svg('<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>', "1.8"),
    "i-phone": svg('<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>', "2"),
}

def faq_html(items):
    out = []
    for i, it in enumerate(items, 1):
        body = "".join("<p>%s</p>" % p for p in it["a"])
        out.append('        <details><summary><span class="rr-acc__n">%02d</span><h3>%s</h3><span class="rr-acc__pm"></span></summary>'
                   '<div class="rr-acc__body">%s</div></details>' % (i, html.escape(it["q"], quote=False), body))
    return "\n".join(out)

def faq_ld(items):
    def absolutize(t):
        return t.replace('href="?uid=97"', 'href="%s/gruenwald/"' % SITE)
    return {"@type": "FAQPage", "@id": SITE + "/#faq", "inLanguage": "de-DE",
            "mainEntity": [{"@type": "Question", "name": it["q"],
                            "acceptedAnswer": {"@type": "Answer", "text": absolutize("".join("<p>%s</p>" % p for p in it["a"]))}}
                           for it in items]}

def home_ld(items):
    return {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/",
         "name": "Rudolf Ritzinger – Kinder- und Jugendlichenpsychotherapeut München", "inLanguage": "de-DE",
         "publisher": {"@id": SITE + "/#praxis"}},
        {"@type": "WebPage", "@id": SITE + "/#webpage", "url": SITE + "/",
         "name": "Kinder- und Jugendlichenpsychotherapeut München | Rudolf Ritzinger",
         "description": "Psychotherapie für Jugendliche ab 12 und junge Erwachsene in München und online für deutschsprachige Familien weltweit. Tiefenpsychologisch fundiert, Eltern werden bei Bedarf einbezogen.",
         "inLanguage": "de-DE", "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": SITE + "/#praxis"},
         "primaryImageOfPage": {"@type": "ImageObject", "url": SITE + "/incms_files/filebrowser/Rudolf-Ritzinger-Jugendspychologe-Munchen.jpg"},
         "mainEntity": {"@id": SITE + "/#faq"},
         "author": {"@id": SITE + "/#rudolf-ritzinger"},
         "reviewedBy": {"@id": SITE + "/#rudolf-ritzinger"},
         "lastReviewed": "2026-10-07"},
        {"@type": "MedicalBusiness", "@id": SITE + "/#praxis",
         "name": "Psychotherapeutische Praxis Rudolf Ritzinger", "alternateName": "Rudolf Ritzinger",
         "description": "Praxis für Jugendlichenpsychotherapie in München. Tiefenpsychologisch fundierte Psychotherapie für Jugendliche und junge Erwachsene von 12 bis 21 Jahren – in der Praxis und online für deutschsprachige Familien weltweit. Gesetzlich Versicherte: Psychotherapie nach den Psychotherapie-Richtlinien; Selbstzahler: integratives Konzept.",
         "url": SITE + "/",
         "image": SITE + "/incms_files/filebrowser/cache/Kinderpsychologe-Jugendpsychologe-Munchen-Ritzinger_ecc5974d1d42cc16d2be6ed51aa32b3a.png",
         "logo": SITE + "/incms_files/filebrowser/cache/Kinderpsychologe-Jugendpsychologe-Munchen-Ritzinger_ecc5974d1d42cc16d2be6ed51aa32b3a.png",
         "telephone": "+491634663072", "priceRange": "$$$-$$$$",
         "address": {"@type": "PostalAddress", "streetAddress": "Rosenstr. 7", "addressLocality": "München",
                     "postalCode": "80331", "addressRegion": "Bayern", "addressCountry": "DE"},
         "geo": {"@type": "GeoCoordinates", "latitude": 48.1366759, "longitude": 11.5733421},
         "openingHoursSpecification": {"@type": "OpeningHoursSpecification",
                                       "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                                       "opens": "09:00", "closes": "20:00"},
         "areaServed": [{"@type": "City", "name": "München"},
                        {"@type": "AdministrativeArea", "name": "Landkreis München"},
                        {"@type": "Place", "name": "Online – deutschsprachige Familien weltweit"}],
         "knowsAbout": ["Tiefenpsychologisch fundierte Psychotherapie", "Jugendpsychotherapie", "Elternarbeit", "Feeling Seen"],
         "employee": {"@id": SITE + "/#rudolf-ritzinger"},
         "sameAs": ["https://www.facebook.com/RudolfRitzinger.de/",
                    "https://www.doctolib.de/kinder-und-jugendlichenpsychotherapeut/muenchen/rudolf-ritzinger"]},
        {"@type": "Person", "@id": SITE + "/#rudolf-ritzinger", "name": "Rudolf Ritzinger",
         "honorificPrefix": "Dipl. Soz. Päd.", "jobTitle": "Kinder- und Jugendlichenpsychotherapeut",
         "image": SITE + "/incms_files/filebrowser/cache/Rudolf-Ritzinger-Munchen-Kinderpsychologe-und-Jugentherapeut_39aa931c6ba3121ccd953dc7099be0d7.png",
         "url": SITE + "/", "worksFor": {"@id": SITE + "/#praxis"},
         "hasCredential": {"@type": "EducationalOccupationalCredential",
                           "name": "Approbation als Kinder- und Jugendlichenpsychotherapeut",
                           "credentialCategory": "Approbation",
                           "recognizedBy": {"@type": "Organization", "name": "Regierung von Oberbayern"}},
         "knowsAbout": ["Tiefenpsychologisch fundierte Psychotherapie", "Jugendpsychotherapie", "Elternarbeit", "Feeling Seen"]},
        faq_ld(items)]}

def intensiv_ld():
    return {"@context": "https://schema.org", "@type": "Service",
            "name": "Family Zen Flow Disziplin",
            "serviceType": "4-Monats-Intensivprogramm für Eltern von Teenagern",
            "description": "Ein konkret anwendbares 4-Monats-Intensivprogramm für Eltern, das hilft, den eigenen Teenager zu verstehen, sich selbst klar zu sehen und sicher zu handeln – bei Streit, Rückzug, Schule, Handy, Motivation und Grenzen. Klar getrennt von der psychotherapeutischen Praxis; keine Psychotherapie und kein Ersatz für eine notwendige Psychotherapie.",
            "provider": {"@id": SITE + "/#praxis"},
            "areaServed": [{"@type": "City", "name": "München"}, {"@type": "Place", "name": "Online"}]}

def minify_css(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{};,>])\s*", r"\1", css)
    css = css.replace(";}", "}")
    return css.strip() + "\n"

JS_CLASSES = {"rr-js", "rr-reveal", "rr-in", "rr-from-left", "rr-from-right", "rr-from-up", "rr-from-zoom", "is-drag"}

def prune_css(css, page_html):
    """Entfernt CSS-Regeln, deren Klassen auf der Seite nicht vorkommen (kleinere Datei)."""
    used = set(JS_CLASSES)
    for m in re.finditer(r'class="([^"]*)"', page_html):
        used.update(m.group(1).split())
    def keep_sel(sel):
        return all(c in used for c in re.findall(r"\.([A-Za-z0-9_-]+)", sel))
    def walk(block):
        out, i = [], 0
        while i < len(block):
            j = block.find("{", i)
            if j < 0:
                break
            head = block[i:j].strip()
            depth, k = 1, j + 1
            while depth:
                if block[k] == "{": depth += 1
                elif block[k] == "}": depth -= 1
                k += 1
            body = block[j + 1:k - 1]
            if head.startswith("@media") or head.startswith("@supports"):
                inner = walk(body)
                if inner:
                    out.append(head + "{" + inner + "}")
            elif head.startswith("@"):
                out.append(head + "{" + body + "}")
            else:
                sels = [x for x in head.split(",") if keep_sel(x)]
                if sels:
                    out.append(",".join(sels) + "{" + body + "}")
            i = k
        return "".join(out)
    return walk(css) + "\n"

def _text(h):
    t = re.sub(r"<[^>]+>", " ", h)
    t = html.unescape(re.sub(r"\s+", " ", t)).strip()
    return t.replace('"', "'")

def enhance(s):
    """SEO/Barrierefreiheit: title an Links und Bildern, Sektionen als benannte Regionen."""
    def link(m):
        tag, inner = m.group(1), m.group(2)
        if " title=" in tag:
            return m.group(0)
        t = _text(inner)
        if not t:
            return m.group(0)
        if 'href="tel:' in tag:
            t = "Anrufen: " + t
        return tag[:-1] + ' title="%s">' % html.escape(t, quote=True).replace("&#x27;", "'") + inner + "</a>"
    s = re.sub(r"(<a\b[^>]*\bhref=[^>]*>)(.*?)</a>", link, s, flags=re.S)
    def img(m):
        tag = m.group(0)
        if " title=" in tag:
            return tag
        alt = re.search(r'alt="([^"]*)"', tag)
        return tag[:-1] + ' title="%s">' % alt.group(1) if alt and alt.group(1) else tag
    s = re.sub(r"<img\b[^>]*>", img, s)
    # <section> mit erster h2 verknüpfen → role="region" + aria-labelledby
    counter = [0]
    def sec(m):
        start = m.end()
        end = s.find("</section>", start)
        h = re.search(r"<h2\b([^>]*)>", s[start:end])
        if not h:
            return m.group(0)
        counter[0] += 1
        return m.group(0)[:-1] + ' role="region" aria-labelledby="rr-h-%d">' % counter[0]
    s2 = re.sub(r"<section\b[^>]*>", sec, s)
    n = [0]
    def h2(m):
        n[0] += 1
        return '<h2 id="rr-h-%d"' % n[0] + m.group(1)
    # Reihenfolge der h2 entspricht den Sektionen mit h2
    out, pos = [], 0
    for sm in re.finditer(r"<section\b[^>]*aria-labelledby=\"(rr-h-\d+)\"[^>]*>", s2):
        out.append(s2[pos:sm.end()])
        rest = s2[sm.end():]
        hm = re.search(r"<h2\b", rest)
        out.append(rest[:hm.start()] + '<h2 id="%s"' % sm.group(1))
        pos = sm.end() + hm.end()
    out.append(s2[pos:])
    return "".join(out)

def render(page_src, ld, img, uid):
    s = open(os.path.join(SRC, page_src), encoding="utf-8").read()
    if "{{faq}}" in s:
        s = s.replace("{{faq}}", faq_html(FAQ))
    s = (s.replace("{{img}}", img).replace("{{anfrage-landing}}", ANFRAGE_LANDING).replace("{{anfrage}}", ANFRAGE)
           .replace("{{link-family-zen}}", LINK_FAMILY_ZEN).replace("{{link-online-kurs}}", LINK_ONLINE_KURS))
    # Sprunglinks im CMS-Format: ?uid=<Seite>#<Anker> (wegen <base href> im CMS)
    s = re.sub(r"\{\{anker:([a-z0-9-]+)\}\}", lambda m: ("?uid=%s#%s" % (uid, m.group(1))) if uid else "#" + m.group(1), s)
    for k, v in ICONS.items():
        s = s.replace("{{%s}}" % k, v)
    left = re.findall(r"\{\{[^}]+\}\}", s)
    assert not left, "Unbekannte Platzhalter: %s" % left
    s = enhance(s)
    s = s.replace('<main class="rr"', sprite() + '\n<main class="rr"', 1)
    css = prune_css(minify_css(open(os.path.join(SRC, "base.css"), encoding="utf-8").read()), s)
    ld_json = json.dumps(ld, ensure_ascii=False, indent=2)
    return "<style>\n" + css + "</style>\n\n" + s + '\n<script type="application/ld+json">\n' + ld_json + "\n</script>\n"

FAQ = json.load(open(os.path.join(SRC, "faq_startseite.json"), encoding="utf-8"))
JS = open(os.path.join(SRC, "main.js"), encoding="utf-8").read()

PAGES = [
    ("startseite", "startseite.html", "2", home_ld(FAQ),
     "Kinder- und Jugendlichenpsychotherapeut München | Rudolf Ritzinger",
     "Rudolf Ritzinger – approbierter Kinder- und Jugendlichenpsychotherapeut in München. Tiefenpsychologisch fundierte Psychotherapie für Jugendliche und junge Erwachsene von 12 bis 21 Jahren, auch online."),
    # Landingpage: Domain/uid noch offen → Sprunglinks als reines #anker (funktioniert überall)
    ("mehr-als-therapie-intensivprogramm", "intensivprogramm.html", None, intensiv_ld(),
     "Family Zen Flow Disziplin – Intensivprogramm für Eltern von Teenagern | Rudolf Ritzinger",
     "Family Zen Flow Disziplin: das 4-Monats-Intensivprogramm für Eltern, deren Teenager ihnen Sorgen macht – bei Streit, Rückzug, Schule, Handy, Motivation und Grenzen. Verstehe dein Kind. Verstehe dich selbst. Handle neu."),
]

for folder, src, uid, ld, title, desc in PAGES:
    os.makedirs(os.path.join(ROOT, folder), exist_ok=True)
    with open(os.path.join(ROOT, folder, "modul-sourcecode.html"), "w", encoding="utf-8") as f:
        f.write(render(src, ld, IMG_MODULE if uid else IMG_PREVIEW, uid))
    preview = render(src, ld, IMG_PREVIEW, uid).replace('href="?uid=', 'href="%s/?uid=' % SITE)
    with open(os.path.join(ROOT, "vorschau-%s.html" % folder), "w", encoding="utf-8") as f:
        f.write('<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
                "<title>%s</title><meta name=\"description\" content=\"%s\"></head><body style=\"margin:0\">\n%s<script>\n%s</script></body></html>\n"
                % (html.escape(title), html.escape(desc), preview, JS))

with open(os.path.join(ROOT, "modul-javascript.js"), "w", encoding="utf-8") as f:
    f.write(JS)
print("ok")

# Klar benannte Kopien der Startseite für das CMS
import shutil
shutil.copy(os.path.join(ROOT, "startseite", "modul-sourcecode.html"), os.path.join(ROOT, "STARTSEITE_1_Sourcecode-Modul.html"))
shutil.copy(os.path.join(ROOT, "modul-javascript.js"), os.path.join(ROOT, "STARTSEITE_2_JavaScript-Modul.js"))
# Zusätzlich als .txt, damit der Browser/Viewer nichts drumherum rendert
shutil.copy(os.path.join(ROOT, "STARTSEITE_1_Sourcecode-Modul.html"), os.path.join(ROOT, "STARTSEITE_1_Sourcecode-Modul.txt"))
shutil.copy(os.path.join(ROOT, "STARTSEITE_2_JavaScript-Modul.js"), os.path.join(ROOT, "STARTSEITE_2_JavaScript-Modul.txt"))
# Landingpage Family Zen Flow Disziplin, klar benannt
shutil.copy(os.path.join(ROOT, "mehr-als-therapie-intensivprogramm", "modul-sourcecode.html"), os.path.join(ROOT, "FAMILY-ZEN-FLOW_1_Sourcecode-Modul.txt"))
shutil.copy(os.path.join(ROOT, "modul-javascript.js"), os.path.join(ROOT, "FAMILY-ZEN-FLOW_2_JavaScript-Modul.txt"))
