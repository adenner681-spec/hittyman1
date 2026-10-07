# Einbau Startseite Rudolf Ritzinger

## Module
- **Sourcecode-Modul:** kompletter Inhalt von `modul-sourcecode.html` (beginnt mit `<style>`, enthält auch das JSON-LD).
- **JavaScript-Modul:** Inhalt von `modul-javascript.js` (reines JS, ohne `<script>`-Tags).
- `vorschau.html` dient nur zur Ansicht im Browser.

## Meta (im CMS unter „Einstellungen“ der Seite eintragen)
- **Title:** Kinder- und Jugendlichenpsychotherapeut München | Rudolf Ritzinger
- **Meta Description:** Rudolf Ritzinger – approbierter Kinder- und Jugendlichenpsychotherapeut in München. Tiefenpsychologisch fundierte Psychotherapie für Jugendliche und junge Erwachsene von 12 bis 21 Jahren.

## Vor dem Livegang prüfen (im Code mit „PRÜFEN“ markiert)
1. Bewertungen 2–5: Originalzitate wortwörtlich von der alten Seite einsetzen, danach Klasse `rr-rev--todo` entfernen.
2. Sternezahl je Bewertung (aktuell jeweils 5).
3. Portrait-URL einsetzen.
4. Unsichere Links abgleichen: `/elterncoaching/`, `/dienstleistungen/psychotherapie/`, Feeling-Seen-Link, `/dienstleistungen/psychotherapie/systemische-therapie/`, Jugendtherapie-Karte (`/jugendpsychologie/` oder `/dienstleistungen/jugendpsychologie/`).
5. Google-Maps: ggf. bisherige Embed-URL in `data-src` einsetzen.
6. Ergänzende Elemente nur behalten, wenn weiterhin angeboten.
7. Bestehendes JSON-LD der alten Seite: alte FAQ-Daten entfernen, damit keine zweite, abweichende FAQPage existiert.
8. Falls das CMS den Seitentitel schon als H1 ausgibt, diese H1 ausblenden – es darf nur eine H1 geben.
