/* ============================================================
   HOME REVEAL
   Section / hero animation system
   ============================================================

   Drives all data-reveal-* attributes on the homepage.
   Progressive enhancement: gated behind `html.hr`.
   If JS never runs, content stays fully visible.

   API:
     HomeReveal.init()      — (re)initialize
     HomeReveal.refresh()   — re-scan DOM for new elements
     HomeReveal.reveal(el)  — force-reveal one element
     HomeReveal.revealAll() — force-reveal everything
   ============================================================ */

(function () {
  "use strict";

  /* ── Config ──────────────────────────────────────── */
  var CFG = {
    sectionDelay: 200,
    defaultStagger: 80,
    cardStagger: 100,
    wordStagger: 40,
    observerThreshold: 0.08,
    observerRootMargin: "0px 0px -8% 0px",
  };

  var _rm = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var _obs = null;
  var _ready = false;

  /* ── Helpers ──────────────────────────────────────── */

  function on(el) {
    el.classList.add("hr-in");
  }

  function off(el) {
    el.classList.remove("hr-in");
  }

  function getStagger(section) {
    var v = parseInt(section.getAttribute("data-reveal-stagger"), 10);
    return isNaN(v) ? CFG.defaultStagger : v;
  }

  /** Execute fn after ms (immediately if reduced motion). */
  function after(ms, fn) {
    _rm ? fn() : setTimeout(fn, ms);
  }

  /* ── Hero (load-time, timed) ─────────────────────── */

  function initHero() {
    var els = document.querySelectorAll("[data-hero-reveal]");
    for (var i = 0; i < els.length; i++) {
      (function (el) {
        var d = parseInt(el.getAttribute("data-hero-reveal"), 10) || 0;
        after(d, function () {
          on(el);
        });
      })(els[i]);
    }
  }

  /* ── Sections (scroll-triggered) ─────────────────── */

  function initSections() {
    var secs = document.querySelectorAll("[data-reveal-section]");
    if (!secs.length) return;

    /* No observer available or reduced motion → reveal immediately. */
    if (_rm || !("IntersectionObserver" in window)) {
      for (var i = 0; i < secs.length; i++) {
        revealSection(secs[i], true);
      }
      return;
    }

    _obs = new IntersectionObserver(
      function (entries) {
        for (var i = 0; i < entries.length; i++) {
          var e = entries[i];
          var s = e.target;
          var rep = s.getAttribute("data-reveal-repeat") === "true";

          if (e.isIntersecting) {
            /* Already revealed and not repeatable → stop watching. */
            if (!rep && s.classList.contains("hr-in")) {
              _obs.unobserve(s);
              continue;
            }
            revealSection(s, false);
            if (!rep) _obs.unobserve(s);
          } else if (rep) {
            /* Left viewport → reset for re-entry. */
            hideSection(s);
          }
        }
      },
      { threshold: CFG.observerThreshold, rootMargin: CFG.observerRootMargin }
    );

    for (var i = 0; i < secs.length; i++) {
      _obs.observe(secs[i]);
    }
  }

  function revealSection(s, immediate) {
    on(s);
    if (immediate) {
      staggerChildren(s, 0);
    } else {
      after(CFG.sectionDelay, function () {
        staggerChildren(s, 0);
      });
    }
  }

  function hideSection(s) {
    off(s);
    var els = s.querySelectorAll(".hr-in");
    for (var i = 0; i < els.length; i++) {
      els[i].classList.remove("hr-in");
    }
  }

  /* ── Children stagger (items + cards in DOM order) ─ */

  function staggerChildren(section, base) {
    var sg = getStagger(section);
    var d = base;

    /*
     * Walk all revealable elements in DOM order.
     * Cards inside grids are handled by their parent grid,
     * so we skip them here.
     */
    var all = section.querySelectorAll(
      "[data-reveal-item], [data-reveal-grid], [data-reveal-card], [data-reveal-decoration]"
    );

    for (var i = 0; i < all.length; i++) {
      var el = all[i];

      /* Skip cards that live inside a grid (handled by grid logic). */
      if (
        (el.hasAttribute("data-reveal-card") ||
          el.hasAttribute("data-reveal-item")) &&
        el.closest("[data-reveal-grid]")
      ) {
        continue;
      }

      if (el.hasAttribute("data-reveal-grid")) {
        /* Grid → cascade its cards. */
        var cards = el.querySelectorAll("[data-reveal-card]");
        for (var c = 0; c < cards.length; c++) {
          (function (card, delay) {
            after(delay, function () {
              on(card);
            });
          })(cards[c], d + c * CFG.cardStagger);
        }
        if (cards.length) {
          d += (cards.length - 1) * CFG.cardStagger + sg;
        }
      } else {
        /* Standalone item or decoration → stagger. */
        (function (item, delay) {
          after(delay, function () {
            on(item);
          });
        })(el, d);
        d += sg;
      }
    }
  }

  /* ── Word text split ─────────────────────────────── */

  function initWords() {
    var els = document.querySelectorAll("[data-reveal-text]");
    for (var i = 0; i < els.length; i++) {
      splitWords(els[i]);
    }
  }

  function splitWords(el) {
    var txt = el.textContent.trim();
    if (!txt) return;
    el.setAttribute("aria-label", txt);
    el.innerHTML = "";
    var words = txt.split(/\s+/);
    for (var i = 0; i < words.length; i++) {
      var s = document.createElement("span");
      s.className = "hr-word";
      s.textContent = words[i] + (i < words.length - 1 ? " " : "");
      el.appendChild(s);
    }
  }

  /* ── Init ─────────────────────────────────────────── */

  function initHomeReveal() {
    if (_ready) return;
    _ready = true;

    document.documentElement.classList.add("hr");

    initHero();
    initSections();
    initWords();
  }

  /* ── Global API ──────────────────────────────────── */

  window.HomeReveal = {
    /** Initialize (safe to call multiple times). */
    init: initHomeReveal,

    /** Re-scan the DOM after dynamic content injection. */
    refresh: function () {
      if (_obs) {
        _obs.disconnect();
        _obs = null;
      }
      _ready = false;
      initHomeReveal();
    },

    /** Force-reveal a single element. */
    reveal: function (el) {
      on(el);
    },

    /** Force-reveal every animatable element on the page. */
    revealAll: function () {
      var all = document.querySelectorAll(
        "[data-reveal-section],[data-reveal-item],[data-reveal-card],[data-hero-reveal],[data-reveal-decoration]"
      );
      for (var i = 0; i < all.length; i++) {
        on(all[i]);
      }
    },
  };

  /* ── Auto-init ──────────────────────────────────── */
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initHomeReveal);
  } else {
    initHomeReveal();
  }
})();
