(function () {
  /* Startet erst, wenn die Seite steht – egal, ob das CMS das Modul im Kopf
     oder am Ende der Seite einbindet. */
  function init() {
    var root = document.querySelector('.rr');
    if (!root || root.getAttribute('data-rr-init')) return;
    root.setAttribute('data-rr-init', '1');

    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
    var raf = window.requestAnimationFrame || function (f) { return setTimeout(f, 16); };

    /* Scroll-Fortschritt (max. einmal pro Frame) */
    var bar = document.getElementById('rr-progress');
    var ticking = false;
    function progress() {
      ticking = false;
      if (!bar) return;
      var r = root.getBoundingClientRect();
      var total = r.height - window.innerHeight;
      var p = total > 0 ? Math.min(Math.max(-r.top / total, 0), 1) : 0;
      bar.style.transform = 'scaleX(' + p.toFixed(4) + ')';
    }
    function onScroll() { if (!ticking) { ticking = true; raf(progress); } }
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    progress();

    if (fine && !reduce) {
      /* Lichtschein folgt der Maus */
      root.querySelectorAll('.rr-spot').forEach(function (el) {
        el.addEventListener('pointermove', function (e) {
          var r = el.getBoundingClientRect();
          el.style.setProperty('--x', (e.clientX - r.left) + 'px');
          el.style.setProperty('--y', (e.clientY - r.top) + 'px');
        });
      });

      /* Buttons ziehen sich leicht zur Maus */
      root.querySelectorAll('[data-magnet]').forEach(function (el) {
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

      /* Hero-Bild reagiert leicht auf die Maus */
      var photo = document.getElementById('rr-photo');
      var hero = root.querySelector('.rr-hero');
      if (photo && hero) {
        var px = 0, py = 0, pending = false;
        hero.addEventListener('pointermove', function (e) {
          var r = hero.getBoundingClientRect();
          px = ((e.clientX - r.left) / r.width - 0.5) * 2;
          py = ((e.clientY - r.top) / r.height - 0.5) * 2;
          if (!pending) {
            pending = true;
            raf(function () {
              pending = false;
              photo.style.setProperty('--px', px.toFixed(3));
              photo.style.setProperty('--py', py.toFixed(3));
            });
          }
        });
      }
    }

    /* Bewertungen: Pfeile + Ziehen mit der Maus */
    var track = document.getElementById('rr-track');
    var prev = document.getElementById('rr-prev');
    var next = document.getElementById('rr-next');
    if (track && prev && next) {
      function step(dir) {
        var card = track.querySelector('.rr-rev');
        track.scrollBy({ left: dir * (card ? card.offsetWidth + 22 : 360), behavior: 'smooth' });
      }
      prev.addEventListener('click', function () { step(-1); });
      next.addEventListener('click', function () { step(1); });
      var down = false, startX = 0, startL = 0;
      track.addEventListener('pointerdown', function (e) {
        if (e.pointerType !== 'mouse') return;
        down = true; startX = e.clientX; startL = track.scrollLeft;
        track.classList.add('is-drag');
      });
      window.addEventListener('pointermove', function (e) {
        if (down) track.scrollLeft = startL - (e.clientX - startX);
      });
      window.addEventListener('pointerup', function () {
        if (!down) return;
        down = false; track.classList.remove('is-drag');
      });
    }

    /* Google Maps erst nach Klick laden */
    var map = document.getElementById('rr-map');
    var mapBtn = document.getElementById('rr-map-btn');
    if (map && mapBtn) {
      mapBtn.addEventListener('click', function () {
        var f = document.createElement('iframe');
        f.src = map.getAttribute('data-src');
        f.title = 'Google Maps: Rosenstr. 7, 80331 München';
        f.loading = 'lazy';
        f.referrerPolicy = 'no-referrer-when-downgrade';
        f.allowFullscreen = true;
        map.insertBefore(f, map.firstChild);
        var veil = map.querySelector('.rr-map__veil');
        if (veil) veil.parentNode.removeChild(veil);
      });
    }

    /* FAQ / Ratgeber: weiches Auf- und Zuklappen */
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

    /* Einblenden beim Scrollen */
    function showAll() {
      root.querySelectorAll('[data-rv]').forEach(function (el) { el.classList.add('is-in'); });
      root.classList.add('rr-ready');
    }
    if (reduce || !('IntersectionObserver' in window)) { showAll(); return; }

    root.querySelectorAll('[data-split]').forEach(function (h) {
      if (h.querySelector('.rr-line')) return;
      h.innerHTML = '<span class="rr-line"><span>' + h.innerHTML + '</span></span>';
      h.setAttribute('data-rv', '');
    });

    var io = new IntersectionObserver(function (entries) {
      /* Elemente, die gleichzeitig ins Bild kommen, nacheinander einblenden */
      var batch = entries.filter(function (e) { return e.isIntersecting; })
        .sort(function (a, b) { return a.boundingClientRect.top - b.boundingClientRect.top || a.boundingClientRect.left - b.boundingClientRect.left; });
      batch.forEach(function (e, i) {
        var el = e.target;
        if (!el.style.getPropertyValue('--d')) el.style.setProperty('--d', Math.min(i * 0.08, 0.4) + 's');
        el.classList.add('is-in');
        io.unobserve(el);
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -8% 0px' });

    /* Erst ab dem nächsten Frame verstecken + beobachten → kein Flackern */
    raf(function () {
      root.classList.add('rr-js', 'rr-ready');
      root.querySelectorAll('[data-rv]').forEach(function (el) { io.observe(el); });
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
