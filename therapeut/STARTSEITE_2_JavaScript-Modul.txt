/* JavaScript-Feld (ohne <script>-Tags einfügen):
   Einflug-Animationen beim Scrollen, Hover-Effekte, Bewertungs-Slider,
   FAQ-Accordion, Google-Maps-Klick. */
(function () {
  'use strict';

  var MAP_URL = 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2662.6316886934655!2d11.57133851564896!3d48.13662577922342!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x479e75dc90dbe7f1%3A0x4e197c42ae4d532a!2sPsychotherapeutische%20Praxis%20Rudolf%20Ritzinger!5e0!3m2!1sde!2sde!4v1649425925208!5m2!1sde!2sde';
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia && window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  function init() {
    var root = document.querySelector('.rr');
    if (!root || root.classList.contains('rr-js')) return;
    root.classList.add('rr-js');

    /* ---------- Scroll-Animationen: Elemente fliegen ein ---------- */
    function mark(selector, dir) {
      root.querySelectorAll(selector).forEach(function (el) {
        if (el.closest('.rr-hero')) return;                     /* Hero animiert per CSS */
        if (el.classList.contains('rr-reveal')) return;        /* erste Regel gewinnt */
        var p = el.parentElement;                              /* nicht doppelt in schon bewegten Blöcken */
        while (p && p !== root) { if (p.classList.contains('rr-reveal')) return; p = p.parentElement; }
        el.classList.add('rr-reveal', dir);
      });
    }
    /* Blöcke, die als Ganzes kommen */
    mark('.rr-termin, .rr-band', 'rr-from-zoom');
    /* Zwei-Spalten-Bereiche: links von links, rechts von rechts */
    mark('.rr-split > :first-child, .rr-intro2 > :first-child, .rr-eltern__grid > :first-child, .rr-spek__intro > :first-child, .rr-appro__grid > :first-child, .rr-faq__grid > :first-child, .rr-fit > :first-child, .rr-costs > :first-child', 'rr-from-left');
    mark('.rr-split > :last-child, .rr-intro2 > :last-child, .rr-eltern__grid > :last-child, .rr-spek__intro > :last-child, .rr-appro__grid > :last-child, .rr-fit > :last-child, .rr-costs > :last-child', 'rr-from-right');
    /* Überschriften von links */
    mark('.rr-sec h2, .rr-final h2, .rr-num', 'rr-from-left');
    /* Karten, Listen, Absätze von unten */
    mark('.rr-glance__item, .rr-pay, .rr-card, .rr-step, .rr-offer, .rr-rev, .rr-tile, .rr-acc details, .rr-pain, .rr-tl, .rr-note, .rr-ref, .rr-guide, .rr-rev__nav, .rr-lead, .rr-center p, .rr-actions, .rr-final p, .rr-final__cta, .rr-map__veil > div, .rr-disclaimer, .rr-topics li, .rr-qlist li, .rr-claim', 'rr-from-up');
    mark('.rr-quote-big', 'rr-from-zoom');

    /* gestaffelte Verzögerung für Karten in Rastern */
    root.querySelectorAll('.rr-glance, .rr-cards, .rr-steps, .rr-offers, .rr-bento, .rr-acc, .rr-pains, .rr-timeline, .rr-rev__track, .rr-topics, .rr-qlist, .rr-claims').forEach(function (list) {
      Array.prototype.forEach.call(list.children, function (child, i) {
        child.style.setProperty('--d', ((i % 4) * 0.12) + 's');
      });
    });

    var reveals = root.querySelectorAll('.rr-reveal');
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) { e.target.classList.add('rr-in'); io.unobserve(e.target); }
        });
      }, { threshold: 0.1, rootMargin: '0px 0px -5% 0px' });
      reveals.forEach(function (el) { io.observe(el); });
    } else {
      reveals.forEach(function (el) { el.classList.add('rr-in'); });
    }

    /* Sicherheitsnetz: Was sichtbar ist, wird nach kurzer Zeit auf jeden Fall eingeblendet */
    window.setTimeout(function () {
      root.querySelectorAll('.rr-reveal:not(.rr-in)').forEach(function (el) {
        var r = el.getBoundingClientRect();
        if (r.top < window.innerHeight && r.bottom > 0) el.classList.add('rr-in');
      });
    }, 2500);

    /* ---------- Scroll-Fortschritt ---------- */
    var bar = document.getElementById('rr-progress');
    if (bar) {
      var ticking = false;
      var update = function () {
        ticking = false;
        var r = root.getBoundingClientRect();
        var total = r.height - window.innerHeight;
        var p = total > 0 ? Math.min(Math.max(-r.top / total, 0), 1) : 0;
        bar.style.transform = 'scaleX(' + p.toFixed(4) + ')';
      };
      var onScroll = function () { if (!ticking) { ticking = true; window.requestAnimationFrame(update); } };
      window.addEventListener('scroll', onScroll, { passive: true });
      window.addEventListener('resize', onScroll);
      update();
    }

    /* ---------- Hover-Effekte (nur mit Maus) ---------- */
    if (fine && !reduce) {
      root.querySelectorAll('.rr-spot').forEach(function (el) {
        el.addEventListener('pointermove', function (e) {
          var r = el.getBoundingClientRect();
          el.style.setProperty('--x', (e.clientX - r.left) + 'px');
          el.style.setProperty('--y', (e.clientY - r.top) + 'px');
        });
      });
      root.querySelectorAll('.rr-btn').forEach(function (el) {
        el.addEventListener('pointermove', function (e) {
          var r = el.getBoundingClientRect();
          el.style.setProperty('--mx', ((e.clientX - r.left - r.width / 2) * 0.15) + 'px');
          el.style.setProperty('--my', ((e.clientY - r.top - r.height / 2) * 0.2) + 'px');
        });
        el.addEventListener('pointerleave', function () {
          el.style.setProperty('--mx', '0px');
          el.style.setProperty('--my', '0px');
        });
      });
      var photo = document.getElementById('rr-photo');
      var hero = root.querySelector('.rr-hero');
      if (photo && hero) {
        hero.addEventListener('pointermove', function (e) {
          var r = hero.getBoundingClientRect();
          photo.style.setProperty('--px', (((e.clientX - r.left) / r.width - 0.5) * 2).toFixed(3));
          photo.style.setProperty('--py', (((e.clientY - r.top) / r.height - 0.5) * 2).toFixed(3));
        });
      }
    }

    /* ---------- Bewertungen: Pfeile + Ziehen mit der Maus ---------- */
    var track = document.getElementById('rr-track');
    var prev = document.getElementById('rr-prev');
    var next = document.getElementById('rr-next');
    if (track && prev && next) {
      var step = function (dir) {
        var card = track.querySelector('.rr-rev');
        track.scrollBy({ left: dir * (card ? card.offsetWidth + 22 : 360), behavior: 'smooth' });
      };
      prev.addEventListener('click', function () { step(-1); });
      next.addEventListener('click', function () { step(1); });
      var down = false, startX = 0, startL = 0;
      track.addEventListener('pointerdown', function (e) {
        if (e.pointerType !== 'mouse') return;
        down = true; startX = e.clientX; startL = track.scrollLeft;
        track.classList.add('is-drag');
      });
      window.addEventListener('pointermove', function (e) { if (down) track.scrollLeft = startL - (e.clientX - startX); });
      window.addEventListener('pointerup', function () { if (down) { down = false; track.classList.remove('is-drag'); } });
    }

    /* ---------- Sprungmarken (?uid=2#name) zuverlässig anspringen ----------
       Das CMS lädt bei ?uid=…#… oft die Seite neu oder scrollt selbst, bevor
       alles fertig aufgebaut ist. Wir übernehmen das für unsere eigenen Anker. */
    var anchorOf = function (name) {
      if (!name) return null;
      return root.querySelector('a.rr-anchor[name="' + name.replace(/"/g, '') + '"]');
    };
    var jumpTo = function (target, smooth) {
      var y = target.getBoundingClientRect().top + window.pageYOffset;
      window.scrollTo({ top: Math.max(0, y), behavior: smooth && !reduce ? 'smooth' : 'auto' });
    };
    document.addEventListener('click', function (e) {
      var a = e.target.closest ? e.target.closest('a[href]') : null;
      if (!a) return;
      var m = (a.getAttribute('href') || '').match(/#([a-z0-9-]+)$/i);
      var target = m && anchorOf(m[1]);
      if (!target) return;                       /* z. B. #popup-terminanfrage → CMS macht weiter */
      e.preventDefault();
      e.stopPropagation();                       /* CMS-eigenes Anker-Scrollen nicht doppelt auslösen */
      jumpTo(target, true);
      if (history.replaceState) history.replaceState(null, '', '#' + m[1]);
    }, true);
    /* Seite wurde mit #anker aufgerufen: nach dem Aufbau genau hinspringen */
    var startHash = (location.hash || '').slice(1);
    var startTarget = anchorOf(startHash);
    if (startTarget) {
      var fix = function () { jumpTo(startTarget, false); };
      setTimeout(fix, 50);
      window.addEventListener('load', function () { setTimeout(fix, 50); });
      setTimeout(fix, 800);
    }

    /* ---------- Google Maps erst nach Klick laden ---------- */
    var map = document.getElementById('rr-map');
    var mapBtn = document.getElementById('rr-map-btn');
    if (map && mapBtn) {
      mapBtn.addEventListener('click', function () {
        var f = document.createElement('iframe');
        f.src = map.getAttribute('data-src') || MAP_URL;
        f.title = 'Google Maps: Rosenstr. 7, 80331 München';
        f.loading = 'lazy';
        f.referrerPolicy = 'no-referrer-when-downgrade';
        f.allowFullscreen = true;
        map.insertBefore(f, map.firstChild);
        var veil = map.querySelector('.rr-map__veil');
        if (veil) veil.parentNode.removeChild(veil);
      });
    }

    /* ---------- FAQ / Ratgeber: weiches Auf- und Zuklappen ---------- */
    root.querySelectorAll('.rr-acc details, .rr-guide details').forEach(function (d) {
      var sum = d.querySelector('summary');
      var body = d.querySelector('.rr-acc__body, .rr-guide__body');
      if (!sum || !body) return;
      sum.addEventListener('click', function (e) {
        if (reduce || !body.animate) return;
        e.preventDefault();
        if (d.open) {
          var h = body.offsetHeight;
          body.animate([{ height: h + 'px', opacity: 1 }, { height: '0px', opacity: 0 }],
            { duration: 320, easing: 'cubic-bezier(.4,0,.2,1)' }).onfinish = function () { d.open = false; };
        } else {
          d.open = true;
          var h2 = body.offsetHeight;
          body.animate([{ height: '0px', opacity: 0 }, { height: h2 + 'px', opacity: 1 }],
            { duration: 420, easing: 'cubic-bezier(.22,1,.36,1)' });
        }
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
