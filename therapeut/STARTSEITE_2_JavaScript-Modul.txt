(function () {
  var root = document.querySelector('.rr');
  if (!root) return;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  /* Scroll-Fortschritt */
  var bar = document.getElementById('rr-progress');
  function progress() {
    if (!bar) return;
    var r = root.getBoundingClientRect();
    var total = r.height - window.innerHeight;
    var p = total > 0 ? Math.min(Math.max(-r.top / total, 0), 1) : 0;
    bar.style.transform = 'scaleX(' + p + ')';
  }
  window.addEventListener('scroll', progress, { passive: true });
  window.addEventListener('resize', progress);
  progress();

  /* Spotlight, das dem Mauszeiger folgt */
  root.querySelectorAll('.rr-spot').forEach(function (el) {
    el.addEventListener('pointermove', function (e) {
      var r = el.getBoundingClientRect();
      el.style.setProperty('--x', (e.clientX - r.left) + 'px');
      el.style.setProperty('--y', (e.clientY - r.top) + 'px');
    });
  });

  /* Magnetische Buttons */
  if (fine && !reduce) {
    root.querySelectorAll('[data-magnet]').forEach(function (el) {
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect();
        el.style.setProperty('--mx', ((e.clientX - r.left - r.width / 2) * 0.18) + 'px');
        el.style.setProperty('--my', ((e.clientY - r.top - r.height / 2) * 0.25) + 'px');
      });
      el.addEventListener('pointerleave', function () {
        el.style.setProperty('--mx', '0px');
        el.style.setProperty('--my', '0px');
      });
    });

    /* Hero-Bild reagiert leicht auf die Maus */
    var orb = document.getElementById('rr-photo');
    var hero = root.querySelector('.rr-hero');
    if (orb && hero) {
      hero.addEventListener('pointermove', function (e) {
        var r = hero.getBoundingClientRect();
        orb.style.setProperty('--px', ((e.clientX - r.left) / r.width - 0.5) * 2);
        orb.style.setProperty('--py', ((e.clientY - r.top) / r.height - 0.5) * 2);
      });
    }
  }

  /* Bewertungen: Pfeile + Ziehen mit der Maus */
  var track = document.getElementById('rr-track');
  if (track && document.getElementById('rr-prev')) {
    function step(dir) {
      var card = track.querySelector('.rr-rev');
      track.scrollBy({ left: dir * (card ? card.offsetWidth + 22 : 360), behavior: 'smooth' });
    }
    document.getElementById('rr-prev').addEventListener('click', function () { step(-1); });
    document.getElementById('rr-next').addEventListener('click', function () { step(1); });
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
      map.querySelector('.rr-map__veil').remove();
    });
  }

  /* FAQ: weiches Auf- und Zuklappen */
  root.querySelectorAll('.rr-acc details, .rr-guide details').forEach(function (d) {
    var sum = d.querySelector('summary');
    var body = d.querySelector('.rr-acc__body, .rr-guide__body');
    if (!sum || !body) return;
    sum.addEventListener('click', function (e) {
      if (reduce || !body.animate) return;
      e.preventDefault();
      if (d.open) {
        var h = body.offsetHeight;
        body.animate([{ height: h + 'px', opacity: 1 }, { height: '0px', opacity: 0 }], { duration: 380, easing: 'cubic-bezier(.16,1,.3,1)' })
          .onfinish = function () { d.open = false; };
      } else {
        d.open = true;
        var h2 = body.offsetHeight;
        body.animate([{ height: '0px', opacity: 0 }, { height: h2 + 'px', opacity: 1 }], { duration: 520, easing: 'cubic-bezier(.16,1,.3,1)' });
      }
    });
  });

  /* Scroll-Animationen */
  if (reduce || !('IntersectionObserver' in window)) return;
  root.querySelectorAll('[data-split]').forEach(function (h) {
    h.innerHTML = '<span class="rr-line"><span>' + h.innerHTML + '</span></span>';
    h.setAttribute('data-rv', '');
  });
  root.classList.add('rr-js');
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      e.target.classList.add('is-in');
      io.unobserve(e.target);
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -60px 0px' });
  root.querySelectorAll('[data-rv]').forEach(function (el) { io.observe(el); });
})();
