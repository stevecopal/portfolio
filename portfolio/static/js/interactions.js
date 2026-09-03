/* ============================================================
   SHADOW SIGNAL
   Global loader page-transition system
   Django / Vanilla JS
   ============================================================

   CONCEPT
   -------
   CLICK
      ↓
   loader appears instantly (covers the current page)
      ↓
   phase words cycle / progress fill
      ↓
   native browser navigation fires UNDER the cover
      ↓
   new page loads behind the loader (no white flash,
   no visible browser loading)
      ↓
   loader finishes to 100% → READY
      ↓
   loader lifts, content staggers in
      ↓
   page reveal

   IMPORTANT
   ---------
   Replaces the previous "Shadow Doors" / "Shadow Fold"
   implementations.

   Navigation is NATIVE (window.location.assign): every Django
   page boots its own scripts and context, so nothing breaks.
   The loader simply covers the swap so the user never sees the
   browser's own loading state.

   The two pages hand off through sessionStorage: the outgoing
   page sets a flag, the incoming page detects it and plays the
   second half of the transition.
*/

(function () {
  "use strict";

  /* =========================================================
       CONFIGURATION
       ========================================================= */

  var CONFIG = {
    // Initial cover hold on a fresh load (ms)
    firstPaintDelay: 650,

    // Delay before native navigation fires after a click (ms)
    navigationDelay: 240,

    // Progress fill duration (ms)
    progressDuration: 900,

    // READY flash before the loader lifts (ms)
    readyHold: 280,

    // Stagger between revealed content elements (ms)
    revealStagger: 45,

    reducedMotion: window.matchMedia("(prefers-reduced-motion: reduce)")
      .matches,
  };

  var PHASES = ["ANALYZE", "DESIGN", "BUILD", "DEPLOY", "EVOLVE"];

  /* =========================================================
       STATE
       ========================================================= */

  var isTransitioning = false;
  var loader = null;
  var phaseEl = null;
  var fillEl = null;
  var destEl = null;
  var phaseTimer = null;
  var phaseIndex = 0;

  /* =========================================================
       INITIALIZATION
       ========================================================= */

  function init() {
    loader = document.getElementById("pageLoader");

    if (!loader) {
      document.body.classList.remove("is-loading");
      return;
    }

    phaseEl = loader.querySelector("[data-loader-phase]");
    fillEl = loader.querySelector("[data-loader-fill]");
    destEl = loader.querySelector("[data-loader-dest]");

    /*
     * If the previous page started a transition,
     * the new document continues the second half.
     */
    if (sessionStorage.getItem("shadowSignalPending") === "1") {
      sessionStorage.removeItem("shadowSignalPending");
      sessionStorage.removeItem("shadowSignalDestination");

      window.setTimeout(playIncoming, 30);
    } else {
      window.setTimeout(playInitial, 30);
    }

    setupNavigation();
    setupExitProtection();
  }

  /* =========================================================
       LOADER STATE
       ========================================================= */

  function cover() {
    document.body.classList.add("is-loading");
    loader.classList.remove("is-ready", "is-done");
  }

  function reveal() {
    document.body.classList.remove("is-loading");
    loader.classList.add("is-ready");

    window.setTimeout(function () {
      loader.classList.add("is-done");
    }, 800);
  }

  function setPhase(text) {
    if (phaseEl) phaseEl.textContent = text;
  }

  function startPhases() {
    stopPhases();
    phaseIndex = 0;
    setPhase(PHASES[0]);
    phaseTimer = window.setInterval(function () {
      phaseIndex = (phaseIndex + 1) % PHASES.length;
      setPhase(PHASES[phaseIndex]);
    }, 420);
  }

  function stopPhases() {
    if (phaseTimer) {
      window.clearInterval(phaseTimer);
      phaseTimer = null;
    }
  }

  function setDestination(label) {
    if (destEl) {
      destEl.textContent = label ? "/ " + label.toUpperCase() : "";
    }
  }

  /* =========================================================
       PROGRESS FILL
       ========================================================= */

  function animateProgress(duration, from, to, onDone) {
    if (!fillEl) {
      if (onDone) onDone();
      return;
    }

    if (CONFIG.reducedMotion) {
      fillEl.style.width = to + "%";
      if (onDone) onDone();
      return;
    }

    var start = null;

    function frame(timestamp) {
      if (start === null) start = timestamp;
      var progress = Math.min((timestamp - start) / duration, 1);
      fillEl.style.width = (from + (to - from) * progress) + "%";
      if (progress < 1) {
        window.requestAnimationFrame(frame);
      } else if (onDone) {
        onDone();
      }
    }

    window.requestAnimationFrame(frame);
  }

  /* =========================================================
       FRESH LOAD (no pending transition)
       ========================================================= */

  function playInitial() {
    /*
     * The server already rendered the page covered
     * (body.is-loading + visible loader).
     * Hold briefly, fill to 100%, flash READY, lift.
     */
    if (CONFIG.reducedMotion) {
      window.setTimeout(finish, 60);
      return;
    }

    startPhases();

    window.setTimeout(function () {
      animateProgress(CONFIG.progressDuration, 0, 100, function () {
        setPhase("READY");
        window.setTimeout(finish, CONFIG.readyHold);
      });

      /*
       * Safety fallback: never leave the cover stuck even if
       * requestAnimationFrame is throttled or unavailable.
       */
      window.setTimeout(
        finish,
        CONFIG.progressDuration + CONFIG.readyHold + 500
      );
    }, CONFIG.firstPaintDelay);
  }

  /* =========================================================
       INCOMING PAGE (transition started on the previous page)
       ========================================================= */

  function playIncoming() {
    /*
     * The screen is already covered by the loader.
     * Finish the fill, flash READY, lift.
     */
    if (CONFIG.reducedMotion) {
      window.setTimeout(finish, 60);
      return;
    }

    startPhases();

    animateProgress(600, 0, 100, function () {
      setPhase("READY");
      window.setTimeout(finish, CONFIG.readyHold);
    });

    /*
     * Safety fallback: never leave the cover stuck even if
     * requestAnimationFrame is throttled or unavailable.
     */
    window.setTimeout(finish, 600 + CONFIG.readyHold + 500);
  }

  /* =========================================================
       FINISH — lift the loader and reveal content
       ========================================================= */

  function finish() {
    stopPhases();
    reveal();
    revealContent();
  }

  function revealContent() {
    var content = document.querySelector(".page-content");
    if (!content) return;

    var elements = content.querySelectorAll("[data-reveal-element]");
    if (!elements.length) return;

    elements.forEach(function (element, index) {
      element.setAttribute("data-page-enter", "");
      element.style.transitionDelay =
        Math.min(60 + index * CONFIG.revealStagger, 380) + "ms";

      /*
       * Timer-based (not rAF) so the reveal works even in
       * throttled / background / headless contexts.
       */
      window.setTimeout(function () {
        element.classList.add("page-enter-visible");
      }, 20);
    });
  }

  /* =========================================================
       INTERNAL LINK DETECTION
       ========================================================= */

  function shouldIntercept(link, event) {
    if (!link) return false;
    if (isTransitioning) return false;

    var href = link.getAttribute("href");
    if (!href) return false;

    /* Skip anchors (navigation.js handles smooth scroll). */
    if (href.charAt(0) === "#") return false;

    /* Skip javascript pseudo-links. */
    if (href.indexOf("javascript:") === 0) return false;

    /* Skip mail / tel. */
    if (href.indexOf("mailto:") === 0 || href.indexOf("tel:") === 0) {
      return false;
    }

    /* Skip downloads. */
    if (link.hasAttribute("download")) return false;

    /* Skip new tabs. */
    if (link.getAttribute("target") === "_blank") return false;

    /* Respect modifier keys. */
    if (
      event &&
      (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey)
    ) {
      return false;
    }

    /* Only a normal left click. */
    if (event && event.button !== undefined && event.button !== 0) {
      return false;
    }

    /* Explicit opt-out. */
    if (link.getAttribute("data-transition") === "none") return false;

    /* Pagination / filter links stay native. */
    if (
      href.indexOf("?page=") !== -1 ||
      href.indexOf("&page=") !== -1 ||
      href.indexOf("?tech=") !== -1 ||
      href.indexOf("&tech=") !== -1
    ) {
      return false;
    }

    var url;
    try {
      url = new URL(href, window.location.href);
    } catch (error) {
      return false;
    }

    /* External link. */
    if (url.origin !== window.location.origin) return false;

    /* Same page. */
    if (
      url.pathname === window.location.pathname &&
      url.search === window.location.search
    ) {
      return false;
    }

    return true;
  }

  /* =========================================================
       GLOBAL INTERNAL NAVIGATION
       ========================================================= */

  function setupNavigation() {
    /*
     * Capture phase: react before any other click handler.
     */
    document.addEventListener(
      "click",
      function (event) {
        var link = event.target.closest ? event.target.closest("a") : null;
        if (!link) return;

        if (!shouldIntercept(link, event)) return;

        event.preventDefault();
        event.stopPropagation();

        var href = link.href;
        var label =
          link.getAttribute("data-transition-label") ||
          getDestinationLabel(link);

        startNavigation(href, label);
      },
      true
    );
  }

  function getDestinationLabel(link) {
    var text = (link.textContent || "").trim().replace(/\s+/g, " ");
    if (text) return text.slice(0, 32);

    try {
      return new URL(link.href)
        .pathname.replace(/^\/|\/$/g, "")
        .replace(/[-_]/g, " ")
        .toUpperCase()
        .slice(0, 32);
    } catch (error) {
      return "";
    }
  }

  /* =========================================================
       START NAVIGATION
       ========================================================= */

  function startNavigation(href, label) {
    if (isTransitioning) return;
    isTransitioning = true;

    /*
     * Lock scroll + cover the current page immediately.
     */
    cover();
    setDestination(label);
    startPhases();

    /*
     * Animate the progress a little while the click response
     * plays; the incoming page finishes it on arrival.
     */
    animateProgress(CONFIG.progressDuration, 0, 82, null);

    /*
     * Mark the next page BEFORE navigation: it will detect the
     * flag and perform the reveal half of the transition.
     */
    sessionStorage.setItem("shadowSignalPending", "1");
    sessionStorage.setItem("shadowSignalDestination", href);

    /*
     * Fire native navigation under the cover.
     */
    window.setTimeout(function () {
      window.location.assign(href);
    }, CONFIG.reducedMotion ? 20 : CONFIG.navigationDelay);
  }

  /* =========================================================
       PAGE EXIT PROTECTION
       ========================================================= */

  function setupExitProtection() {
    /*
     * When the browser restores a page from its back/forward
     * cache mid-transition, never leave the body locked —
     * force the loader to a finished state.
     *
     * Only act on persisted restores: pageshow also fires on
     * the initial load, where the loader legitimately covers.
     */
    window.addEventListener("pageshow", function (event) {
      if (!event.persisted) return;

      document.body.classList.remove("is-loading");
      if (loader) loader.classList.add("is-ready", "is-done");
      isTransitioning = false;
    });

    window.addEventListener("popstate", function () {
      sessionStorage.removeItem("shadowSignalPending");
      sessionStorage.removeItem("shadowSignalDestination");
    });
  }

  /* =========================================================
       PUBLIC API
       ========================================================= */

  window.ShadowSignal = {
    navigate: function (href, label) {
      if (!href || isTransitioning) return;
      startNavigation(href, label || "");
    },

    isTransitioning: function () {
      return isTransitioning;
    },
  };

  /* =========================================================
       START
       ========================================================= */

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();