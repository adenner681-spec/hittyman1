# Einbau – Rudolf Ritzinger

Quelltexte liegen in `src/`, gebaut wird mit `python3 build.py`. Ins CMS kommen nur die fertigen Dateien:

| Seite | Modul „Sourcecode“ | Modul „JavaScript“ |
|---|---|---|
| Startseite | `startseite/modul-sourcecode.html` | `modul-javascript.js` |
| Mehr als Therapie – Intensivprogramm | `mehr-als-therapie-intensivprogramm/modul-sourcecode.html` | `modul-javascript.js` |

Die `vorschau-*.html` dienen nur zum Ansehen im Browser.

## Startseite im CMS
1. **Header-Banner (specific_banner) verschlanken:** Logo, Menü und Telefon bleiben. Die alte H1 „Kinder- und Jugendlichenpsychotherapeut“, „Mehr als Therapie…“, die Häkchen-Liste und den Button entfernen – sonst gibt es zwei H1.
2. **Alle alten Inhaltsblöcke** der Startseite durch die zwei Module ersetzen. **Das Popup-Modul „terminanfrage“ (Gesetzlich / Privat) unbedingt behalten.** Jeder Anfrage-Button auf allen Seiten öffnet dieses Popup über `?uid=2#popup-terminanfrage` (zentral in `build.py` als `ANFRAGE` hinterlegt). Auf Unterseiten wie der Landingpage führt der Button zur Startseite und öffnet dort das Popup.
3. **JSON-LD im Seitenkopf löschen.** Das neue, vollständige JSON-LD (WebSite, WebPage, Praxis, Person, FAQ) steckt im Sourcecode-Modul. Die FAQ darin wird beim Build automatisch aus dem sichtbaren Text erzeugt und ist 1:1 synchron.
4. **Meta** (Seiteneinstellungen):
   - Title: `Kinder- und Jugendlichenpsychotherapeut München | Rudolf Ritzinger`
   - Description: `Rudolf Ritzinger – approbierter Kinder- und Jugendlichenpsychotherapeut in München. Tiefenpsychologisch fundierte Psychotherapie für Jugendliche und junge Erwachsene von 12 bis 21 Jahren, auch online.`
5. Im eingefügten Seitenquelltext stand `<meta name="robots" content="noindex">` und als Canonical `…/?uid=2`. Auf der Live-Domain muss die Startseite **indexierbar** sein und als Canonical `https://www.rudolf-ritzinger.com/` haben.

## Neue Menüstruktur (im CMS anlegen)
Bestehende Seiten **nicht löschen** und ihre URLs nicht ändern (Rankings & interne Links).

- **Startseite** – `?uid=2`
- **Psychotherapie** – `?uid=95`
  - Psychotherapie für Jugendliche – `?uid=77` (Jugendpsychologie)
  - Elternarbeit & Feeling Seen – *neu* (oder vorerst `?uid=84` Elterncoaching)
  - Online-Psychotherapie – *neu*
  - Tiefenpsychologisch fundierte Therapie – `?uid=96`
  - Kinderpsychologie – `?uid=83` (+ Entwicklungsstufen `?uid=85`)
  - Verhaltenstherapie (Information) – `?uid=86`
- **Ablauf & Kosten** – *neu* (bis dahin Anker `#ablauf-kosten` auf der Startseite)
  - Gesetzlich versichert – `?uid=93`
  - Privat / Selbstzahler – `?uid=92`
- **Über mich** – `?uid=70`
- **Mehr als Therapie** (Eltern & Familie) – *neu*
  - Vier-Monats-Intensivprozess für Familien – *neu*, Vorschlag `/mehr-als-therapie/familien-intensivprogramm/`
  - Online-Kurs (499 €) – *neu*, Vorschlag `/mehr-als-therapie/online-kurs/`
- **Kontakt** – `?uid=72`

„Dienstleistungen“ (`?uid=75`) bleibt als Seite bestehen (Buttons „Therapeutisches Angebot“ verlinken darauf), muss aber nicht mehr im Hauptmenü stehen.

## Offene Punkte (im Code mit „PRÜFEN“ markiert)
- Texte „Ablauf & Kosten“ (Richtlinien / integratives Konzept) und FAQ „Online“ und „Verhaltenstherapie“ fachlich gegenlesen.
- URLs der neuen Seiten in den Buttons „Zum Intensivprogramm“ und „Zum Online-Kurs“ eintragen.
- Online-Kurs: Kurzbeschreibung, Landingpage-Struktur.
- Intensivprogramm: Bausteine, Ablauf je Monat, Preis, Starttermin, Bild.
- „Ergänzende Elemente“ nur behalten, wenn weiterhin angeboten.

## Sprungmarken (Anker) auf der Startseite
Format wie im CMS üblich: Link `?uid=2#name`, Ziel `<a name="name"></a>`.

| Bereich | Link |
|---|---|
| Start / Header | `?uid=2#start` |
| Mein Angebot auf einen Blick | `?uid=2#angebot` |
| Praxis für Jugendlichenpsychotherapie | `?uid=2#praxis` |
| Therapeutisches Angebot | `?uid=2#therapeutisches-angebot` |
| Ablauf und Kosten | `?uid=2#ablauf-kosten` |
| Für Eltern | `?uid=2#eltern` |
| Terminblock | `?uid=2#termin` |
| Mehr als Therapie | `?uid=2#mehr-als-therapie` |
| Erfahrungen / Bewertungen | `?uid=2#erfahrungen` |
| Karte / Anfahrt | `?uid=2#anfahrt` |
| Angebotsspektrum | `?uid=2#angebotsspektrum` |
| Zweiter Terminblock | `?uid=2#termin-vereinbaren` |
| Approbation | `?uid=2#approbation` |
| FAQ | `?uid=2#faq` |
| Ratgeber | `?uid=2#ratgeber` |
| Kinder unter 12 | `?uid=2#unter-12` |
| Abschluss / Termin anfragen | `?uid=2#termin-anfragen` |

Landingpage Intensivprogramm: Anker `start`, `ausgangslage`, `programm`, `ablauf`, `fuer-wen`, `begleitung`, `anfrage`. Sobald die Seite im CMS angelegt ist, ihre uid in `build.py` statt `UID-LANDINGPAGE` eintragen.

## Landingpages „Mehr als Therapie“ (Platzhalter)
Domain bzw. Unterseite stehen noch nicht fest. Bis dahin:
- Die Buttons „Mehr zu Family Zen Flow Disziplin“ und „Mehr zum Online-Kurs“ auf der Startseite springen zum Bereich „Mehr als Therapie“. Ziel später in `build.py` bei `LINK_FAMILY_ZEN` / `LINK_ONLINE_KURS` eintragen.
- Die Landingpage selbst ist domain-unabhängig gebaut: Bilder und Links zur Praxis sind absolut (`https://www.rudolf-ritzinger.com/…`), Sprunglinks innerhalb der Seite sind reine `#anker`.
- Anfrage-Button der Landingpage: vorerst das Popup der Praxis-Startseite (`ANFRAGE_LANDING` in `build.py`) – PRÜFEN, ob ein eigenes Formular sinnvoller ist.
