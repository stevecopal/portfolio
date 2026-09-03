/* ============================================================
   HOME REVEAL
   Section / hero animation system
   Django / Vanilla JS
   ============================================================

   Drives:
   · [data-hero-reveal="<delay ms>"]   — hero elements fade/rise
                                          in on load, staggered
   · [data-reveal-item="fade|slide-up"] — headers/items revealed
                                          on scroll into view
   · [data-reveal-card]                 — cards revealed on scroll,
                                          with sibling stagger
   · [data-reveal-section] / [data-reveal-grid] — markers used
                                          to group reveals

   Progressive enhancement: the initial hidden state in
   home-reveal.css is gated behind `html.hr`, a class added
   here — if this script never runs, content stays visible.
*/

(function () {
  "use strict";

  var reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)")
    .matches;

  var REVEAL_SELECTOR =
    "[data-reveal-item], [data-reveal-card]";

  function revealNow(element) {
    element.classList.add("hr-in");
  }

  function revealAll() {
    var elements = document.querySelectorAll(
      "[data-hero-reveal], " + REVEAL_SELECTOR
    );
    for (var i = 0; i < elements.length; i++) {
      revealNow(elements[i]);
    }
  }

  function init() {
    /* Enable the hidden states only once JS is guaranteed. */
    document.documentElement.classList.add("hr");

    /* ── Hero: staggered fade/rise on load ─────────────── */
    var heroElements = document.querySelectorAll("[data-hero-reveal]");
    for (var i = 0; i < heroElements.length; i++) {
      (function (element) {
        var delay = parseInt(element.getAttribute("data-hero-reveal"), 10) || 0;
        window.setTimeout(function () {
          revealNow(element);
        }, delay);
      })(heroElements[i]);
    }

    if (reducedMotion) {
      revealAll();
      return;
    }

    /* ── Scroll reveals ────────────────────────────────── */
    var targets = document.querySelectorAll(REVEAL_SELECTOR);

    if (!("IntersectionObserver" in window) || !targets.length) {
      revealAll();
      return;
    }

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;

          var element = entry.target;

          /* Small stagger relative to siblings for a wave effect. */
          var index = 0;
          var previous = element.previousElementSibling;
          while (previous) {
            index++;
            previous = previous.previousElementSibling;
          }
          element.style.transitionDelay = Math.min(index * 70, 420) + "ms";

          revealNow(element);
          observer.unobserve(element);
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );

    targets.forEach(function (element) {
      observer.observe(element);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();