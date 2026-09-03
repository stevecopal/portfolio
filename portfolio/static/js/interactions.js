/* ============================================================
   SHADOW FOLD
   Global page transition system
   Django / Vanilla JS
   ============================================================

   CONCEPT
   -------
   CLICK
      ↓
   interaction response
      ↓
   shadow origin
      ↓
   folding black planes
      ↓
   green signal
      ↓
   browser navigation
      ↓
   new page loads behind transition
      ↓
   shadow planes unfold
      ↓
   page reveal

   IMPORTANT
   ----------
   This intentionally replaces the previous "Shadow Doors"
   implementation.

   The old system:
       animation → fetch → replace DOM → reinitialize scripts

   This system:
       fetch/browser navigation + animation happen together

   This makes navigation much more reliable for Django pages.
*/

(function () {
  "use strict";

  /* =========================================================
       CONFIGURATION
       ========================================================= */

  const CONFIG = {
    closeDuration: 620,
    openDuration: 760,

    // Small delay before the transition visibly starts.
    // Gives the clicked element time to react.
    clickResponse: 90,

    // Green signal duration.
    signalDuration: 170,

    // Small maximum time used only as a safety fallback.
    navigationSafetyTimeout: 2200,

    easing: "cubic-bezier(0.16, 1, 0.3, 1)",
    easingSoft: "cubic-bezier(0.22, 1, 0.36, 1)",

    reducedMotion: window.matchMedia("(prefers-reduced-motion: reduce)")
      .matches,
  };

  /* =========================================================
       STATE
       ========================================================= */

  let isTransitioning = false;
  let transitionRoot = null;
  let leftPanel = null;
  let rightPanel = null;
  let centerSignal = null;
  let signalCore = null;
  let transitionLabel = null;

  /* =========================================================
       INITIALIZATION
       ========================================================= */

  function init() {
    createTransitionDOM();
    injectStyles();
    setupInitialPageReveal();
    setupInternalNavigation();
    setupAnchorNavigation();
    setupPageExitProtection();

    /*
     * If the previous page started a transition,
     * the new document continues the second half.
     */
    if (sessionStorage.getItem("shadowFoldPending") === "1") {
      sessionStorage.removeItem("shadowFoldPending");

      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          playIncomingTransition();
        });
      });
    } else {
      hideInitialOverlay();
    }
  }

  /* =========================================================
       DOM CREATION
       ========================================================= */

  function createTransitionDOM() {
    /*
     * Avoid duplicate initialization.
     */
    if (document.querySelector("[data-shadow-fold]")) {
      transitionRoot = document.querySelector("[data-shadow-fold]");

      leftPanel = transitionRoot.querySelector(".shadow-fold__panel--left");

      rightPanel = transitionRoot.querySelector(".shadow-fold__panel--right");

      centerSignal = transitionRoot.querySelector(".shadow-fold__signal");

      signalCore = transitionRoot.querySelector(".shadow-fold__signal-core");

      transitionLabel = transitionRoot.querySelector(".shadow-fold__label");

      return;
    }

    transitionRoot = document.createElement("div");

    transitionRoot.className = "shadow-fold";

    transitionRoot.setAttribute("data-shadow-fold", "");

    transitionRoot.setAttribute("aria-hidden", "true");

    transitionRoot.innerHTML = `
            <div class="shadow-fold__ambient"></div>

            <div class="shadow-fold__panel shadow-fold__panel--left">
                <div class="shadow-fold__edge"></div>
                <div class="shadow-fold__texture"></div>
            </div>

            <div class="shadow-fold__panel shadow-fold__panel--right">
                <div class="shadow-fold__edge"></div>
                <div class="shadow-fold__texture"></div>
            </div>

            <div class="shadow-fold__signal">

                <div class="shadow-fold__signal-line"></div>

                <div class="shadow-fold__signal-core">
                    <span></span>
                </div>

                <div class="shadow-fold__label">
                    <span class="shadow-fold__label-main">
                        BUILDING
                    </span>

                    <span class="shadow-fold__label-destination"></span>
                </div>

            </div>
        `;

    document.body.appendChild(transitionRoot);

    leftPanel = transitionRoot.querySelector(".shadow-fold__panel--left");

    rightPanel = transitionRoot.querySelector(".shadow-fold__panel--right");

    centerSignal = transitionRoot.querySelector(".shadow-fold__signal");

    signalCore = transitionRoot.querySelector(".shadow-fold__signal-core");

    transitionLabel = transitionRoot.querySelector(".shadow-fold__label");
  }

  /* =========================================================
       STYLES
       ========================================================= */

  function injectStyles() {
    if (document.getElementById("shadow-fold-styles")) {
      return;
    }

    const style = document.createElement("style");

    style.id = "shadow-fold-styles";

    style.textContent = `

        /* =====================================================
           ROOT
           ===================================================== */

        .shadow-fold {
            position: fixed;
            inset: 0;
            z-index: 999999;

            width: 100vw;
            height: 100dvh;

            pointer-events: none;

            overflow: hidden;

            visibility: hidden;

            background: #0B0D0F;
        }


        .shadow-fold.is-active {
            visibility: visible;
            pointer-events: all;
        }


        /* =====================================================
           AMBIENT
           ===================================================== */

        .shadow-fold__ambient {
            position: absolute;
            inset: 0;

            background:
                radial-gradient(
                    circle at 50% 50%,
                    rgba(21, 163, 74, 0.055),
                    transparent 30%
                );

            opacity: 0;

            transition:
                opacity 500ms ${CONFIG.easing};
        }


        .shadow-fold.is-active
        .shadow-fold__ambient {
            opacity: 1;
        }


        /* =====================================================
           PANELS
           ===================================================== */

        .shadow-fold__panel {
            position: absolute;

            top: 0;

            width: 50.5%;
            height: 100%;

            background:
                linear-gradient(
                    90deg,
                    #080A0B 0%,
                    #0B0D0F 75%,
                    #0A0C0D 100%
                );

            will-change: transform;

            transform: translate3d(0, 0, 0);

            overflow: hidden;

            box-shadow:
                0 0 80px rgba(0, 0, 0, 0.55);

            transition:
                transform ${CONFIG.closeDuration}ms ${CONFIG.easing};
        }


        .shadow-fold__panel--left {
            left: 0;

            transform:
                translate3d(-101%, 0, 0);
        }


        .shadow-fold__panel--right {
            right: 0;

            background:
                linear-gradient(
                    270deg,
                    #080A0B 0%,
                    #0B0D0F 75%,
                    #0A0C0D 100%
                );

            transform:
                translate3d(101%, 0, 0);
        }


        /* =====================================================
           PANEL TEXTURE
           ===================================================== */

        .shadow-fold__texture {
            position: absolute;
            inset: 0;

            opacity: 0.08;

            background-image:
                linear-gradient(
                    rgba(255,255,255,0.025) 1px,
                    transparent 1px
                ),
                linear-gradient(
                    90deg,
                    rgba(255,255,255,0.025) 1px,
                    transparent 1px
                );

            background-size:
                80px 80px;

            mask-image:
                linear-gradient(
                    to bottom,
                    transparent,
                    black 20%,
                    black 80%,
                    transparent
                );
        }


        /* =====================================================
           PANEL EDGES
           ===================================================== */

        .shadow-fold__edge {
            position: absolute;

            top: 0;
            bottom: 0;

            width: 1px;

            background:
                linear-gradient(
                    to bottom,
                    transparent,
                    rgba(21, 163, 74, 0.12),
                    transparent
                );

            opacity: 0.65;
        }


        .shadow-fold__panel--left
        .shadow-fold__edge {
            right: 0;
        }


        .shadow-fold__panel--right
        .shadow-fold__edge {
            left: 0;
        }


        /* =====================================================
           SIGNAL
           ===================================================== */

        .shadow-fold__signal {
            position: absolute;

            inset: 0;

            display: flex;

            align-items: center;
            justify-content: center;

            flex-direction: column;

            opacity: 0;

            pointer-events: none;
        }


        .shadow-fold__signal-line {
            position: absolute;

            top: 50%;
            left: 50%;

            width: 1px;
            height: 0;

            transform:
                translate(-50%, -50%);

            background:
                rgba(21, 163, 74, 0.85);

            box-shadow:
                0 0 18px
                rgba(21, 163, 74, 0.35);
        }


        .shadow-fold__signal-core {
            position: relative;

            width: 9px;
            height: 9px;

            border-radius: 999px;

            background: #15A34A;

            box-shadow:
                0 0 0 1px
                rgba(21,163,74,0.18),

                0 0 22px
                rgba(21,163,74,0.65);

            transform: scale(0.35);

            opacity: 0;
        }


        .shadow-fold__signal-core span {
            position: absolute;

            inset: -12px;

            border: 1px solid
                rgba(21,163,74,0.18);

            border-radius: 999px;

            animation:
                shadowFoldPulse
                1.8s ease-out infinite;
        }


        @keyframes shadowFoldPulse {

            0% {
                transform: scale(0.65);
                opacity: 0.75;
            }

            100% {
                transform: scale(1.5);
                opacity: 0;
            }

        }


        /* =====================================================
           LABEL
           ===================================================== */

        .shadow-fold__label {
            margin-top: 38px;

            display: flex;

            flex-direction: column;

            align-items: center;

            gap: 7px;

            opacity: 0;

            transform:
                translateY(8px);

            font-family:
                ui-monospace,
                SFMono-Regular,
                Menlo,
                Monaco,
                Consolas,
                monospace;

            letter-spacing:
                0.18em;

            text-transform:
                uppercase;

            font-size:
                9px;

            color:
                rgba(255,255,255,0.42);
        }


        .shadow-fold__label-destination {
            color:
                rgba(21,163,74,0.85);
        }


        /* =====================================================
           ACTIVE CLOSE
           ===================================================== */

        .shadow-fold.is-closing
        .shadow-fold__panel--left {

            transform:
                translate3d(0, 0, 0);

        }


        .shadow-fold.is-closing
        .shadow-fold__panel--right {

            transform:
                translate3d(0, 0, 0);

        }


        .shadow-fold.is-signal
        .shadow-fold__signal {

            opacity: 1;

        }


        .shadow-fold.is-signal
        .shadow-fold__signal-core {

            opacity: 1;

            transform:
                scale(1);

            transition:
                transform 180ms ${CONFIG.easing},
                opacity 120ms ease;
        }


        .shadow-fold.is-signal
        .shadow-fold__label {

            opacity: 1;

            transform:
                translateY(0);

            transition:
                opacity 220ms ${CONFIG.easing},
                transform 220ms ${CONFIG.easing};
        }


        /* =====================================================
           OPENING
           ===================================================== */

        .shadow-fold.is-opening
        .shadow-fold__panel--left {

            transform:
                translate3d(-101%, 0, 0);

            transition-duration:
                ${CONFIG.openDuration}ms;

        }


        .shadow-fold.is-opening
        .shadow-fold__panel--right {

            transform:
                translate3d(101%, 0, 0);

            transition-duration:
                ${CONFIG.openDuration - 70}ms;

        }


        .shadow-fold.is-opening
        .shadow-fold__signal {

            opacity: 0;

            transition:
                opacity 180ms ease;
        }


        /* =====================================================
           CLICKED ELEMENT
           ===================================================== */

        .shadow-fold-clicked {
            transform:
                scale(0.985);

            transition:
                transform 90ms ${CONFIG.easing};
        }


        /* =====================================================
           PAGE ENTER
           ===================================================== */

        [data-page-enter] {
            opacity: 0;

            transform:
                translateY(18px);

            transition:
                opacity 650ms ${CONFIG.easing},
                transform 800ms ${CONFIG.easing};
        }


        [data-page-enter].page-enter-visible {
            opacity: 1;

            transform:
                translateY(0);
        }


        /* =====================================================
           REDUCED MOTION
           ===================================================== */

        @media
        (prefers-reduced-motion: reduce) {

            .shadow-fold__panel {
                transition-duration: 1ms !important;
            }

            .shadow-fold__ambient,
            .shadow-fold__signal,
            .shadow-fold__signal-core,
            .shadow-fold__label {
                transition-duration: 1ms !important;
            }

            .shadow-fold-clicked {
                transform: none;
            }

            [data-page-enter] {
                opacity: 1;
                transform: none;
                transition: none;
            }
        }


        /* =====================================================
           MOBILE
           ===================================================== */

        @media (max-width: 768px) {

            .shadow-fold__texture {
                background-size: 55px 55px;
                opacity: 0.05;
            }

            .shadow-fold__panel {
                width: 51%;
            }

            .shadow-fold__label {
                font-size: 8px;
            }

        }

        `;

    document.head.appendChild(style);
  }

  /* =========================================================
       INITIAL PAGE REVEAL
       ========================================================= */

  function setupInitialPageReveal() {
    /*
     * Do not hide the entire page.
     * Only mark relevant content for a subtle entrance.
     */
    const pageContent = document.querySelector(".page-content");

    if (!pageContent) return;

    const candidates = pageContent.querySelectorAll("[data-reveal-element]");

    if (!candidates.length) {
      return;
    }

    candidates.forEach((element, index) => {
      element.setAttribute("data-page-enter", "");

      element.style.transitionDelay = `${Math.min(index * 45, 260)}ms`;
    });

    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        candidates.forEach((element) => {
          element.classList.add("page-enter-visible");
        });
      });
    });
  }

  /* =========================================================
       HIDE INITIAL OVERLAY
       ========================================================= */

  function hideInitialOverlay() {
    if (!transitionRoot) return;

    transitionRoot.classList.remove(
      "is-active",
      "is-closing",
      "is-signal",
      "is-opening",
    );

    document.body.style.overflow = "";
  }

  /* =========================================================
       INTERNAL LINK DETECTION
       ========================================================= */

  function shouldIntercept(link, event) {
    if (!link) return false;

    if (isTransitioning) return false;

    const href = link.getAttribute("href");

    if (!href) return false;

    /*
     * Skip anchors.
     */
    if (href.startsWith("#")) {
      return false;
    }

    /*
     * Skip javascript pseudo-links.
     */
    if (href.startsWith("javascript:")) {
      return false;
    }

    /*
     * Skip mail / tel.
     */
    if (href.startsWith("mailto:") || href.startsWith("tel:")) {
      return false;
    }

    /*
     * Skip downloads.
     */
    if (link.hasAttribute("download")) {
      return false;
    }

    /*
     * Skip new tabs.
     */
    if (link.getAttribute("target") === "_blank") {
      return false;
    }

    /*
     * Respect modifier keys.
     */
    if (
      event &&
      (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey)
    ) {
      return false;
    }

    /*
     * Only normal left click.
     */
    if (event && event.button !== undefined && event.button !== 0) {
      return false;
    }

    /*
     * Explicit opt-out.
     */
    if (link.dataset.transition === "none") {
      return false;
    }

    /*
     * Pagination/filter links can remain native.
     */
    if (
      href.includes("?page=") ||
      href.includes("&page=") ||
      href.includes("?tech=") ||
      href.includes("&tech=")
    ) {
      return false;
    }

    let url;

    try {
      url = new URL(href, window.location.href);
    } catch (error) {
      return false;
    }

    /*
     * External link.
     */
    if (url.origin !== window.location.origin) {
      return false;
    }

    /*
     * Same page.
     */
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

  function setupInternalNavigation() {
    /*
     * Capture phase allows the transition system
     * to react before other click handlers.
     */
    document.addEventListener(
      "click",
      function (event) {
        const link = event.target.closest("a");

        if (!link) return;

        if (!shouldIntercept(link, event)) {
          return;
        }

        /*
         * Stop the native navigation.
         */
        event.preventDefault();
        event.stopPropagation();

        const href = link.href;

        const type = link.dataset.transition || "page";

        const label =
          link.dataset.transitionLabel || getDestinationLabel(link, href);

        startNavigation(href, type, label, link);
      },
      true,
    );
  }

  /* =========================================================
       DESTINATION LABEL
       ========================================================= */

  function getDestinationLabel(link, href) {
    if (link.dataset.transitionLabel) {
      return link.dataset.transitionLabel;
    }

    const aria = link.getAttribute("aria-label");

    if (aria) {
      return aria;
    }

    const text = link.textContent.trim().replace(/\s+/g, " ");

    if (text) {
      return text.slice(0, 32);
    }

    try {
      const url = new URL(href);

      return url.pathname
        .replace(/^\/|\/$/g, "")
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

  function startNavigation(href, type, label, clickedElement) {
    if (isTransitioning) {
      return;
    }

    isTransitioning = true;

    /*
     * Block accidental second clicks.
     */
    document.body.classList.add("is-shadow-fold-transitioning");

    document.body.style.overflow = "hidden";

    /*
     * Tiny immediate feedback.
     */
    if (clickedElement) {
      clickedElement.classList.add("shadow-fold-clicked");
    }

    /*
     * Set destination label.
     */
    const destinationElement = transitionRoot.querySelector(
      ".shadow-fold__label-destination",
    );

    if (destinationElement) {
      destinationElement.textContent = label ? `/ ${label.toUpperCase()}` : "";
    }

    /*
     * IMPORTANT:
     *
     * Mark the next page BEFORE navigation.
     *
     * The new page will detect this flag and
     * automatically perform the reveal.
     */
    sessionStorage.setItem("shadowFoldPending", "1");

    sessionStorage.setItem("shadowFoldDestination", href);

    /*
     * Start animation immediately.
     */
    transitionRoot.classList.add("is-active");

    /*
     * Slight click response.
     */
    setTimeout(
      () => {
        /*
         * Begin closing.
         */
        playClosingAnimation();
      },
      CONFIG.reducedMotion ? 0 : CONFIG.clickResponse,
    );

    /*
     * IMPORTANT:
     *
     * We DO NOT wait for the animation
     * to finish before navigation.
     *
     * The browser starts loading the next page
     * as soon as the visual cover is sufficiently
     * established.
     */
    const navigationDelay = CONFIG.reducedMotion ? 20 : 260;

    setTimeout(() => {
      navigateNormally(href);
    }, navigationDelay);
  }

  /* =========================================================
       CLOSING ANIMATION
       ========================================================= */

  function playClosingAnimation() {
    transitionRoot.classList.remove("is-opening");

    transitionRoot.classList.add("is-closing");

    /*
     * Signal appears near the end of closure.
     */
    setTimeout(
      () => {
        if (!transitionRoot) {
          return;
        }

        transitionRoot.classList.add("is-signal");

        animateSignal();
      },
      CONFIG.reducedMotion ? 0 : CONFIG.closeDuration - 130,
    );
  }

  /* =========================================================
       GREEN SIGNAL
       ========================================================= */

  function animateSignal() {
    const line = transitionRoot.querySelector(".shadow-fold__signal-line");

    if (!line) return;

    line.style.transition = `
            height ${CONFIG.signalDuration}ms
            ${CONFIG.easing}
            `;

    line.style.height = "110px";

    setTimeout(() => {
      line.style.opacity = "0";
    }, CONFIG.signalDuration);
  }

  /* =========================================================
       NAVIGATION
       ========================================================= */

  function navigateNormally(href) {
    /*
     * Use native navigation.
     *
     * This is intentional.
     *
     * It avoids:
     * - replacing only .page-content
     * - broken page-specific scripts
     * - duplicated event listeners
     * - stale DOM
     * - incorrect forms
     * - broken hero initialization
     * - broken Django context
     */
    window.location.assign(href);
  }

  /* =========================================================
       INCOMING PAGE
       ========================================================= */

  function playIncomingTransition() {
    if (!transitionRoot) {
      return;
    }

    /*
     * Start with screen covered.
     */
    transitionRoot.classList.add("is-active");

    transitionRoot.classList.remove("is-closing", "is-signal");

    /*
     * Make sure panels are physically closed
     * before starting the reveal.
     */
    leftPanel.style.transition = "none";

    rightPanel.style.transition = "none";

    leftPanel.style.transform = "translate3d(0, 0, 0)";

    rightPanel.style.transform = "translate3d(0, 0, 0)";

    /*
     * Force browser to commit closed state.
     */
    void transitionRoot.offsetWidth;

    /*
     * Restore transitions.
     */
    leftPanel.style.transition = `
            transform
            ${CONFIG.openDuration}ms
            ${CONFIG.easing}
            `;

    rightPanel.style.transition = `
            transform
            ${CONFIG.openDuration - 70}ms
            ${CONFIG.easing}
            `;

    /*
     * Small green pulse before opening.
     */
    if (!CONFIG.reducedMotion) {
      transitionRoot.classList.add("is-signal");

      setTimeout(() => {
        transitionRoot.classList.remove("is-signal");
      }, 120);
    }

    /*
     * Open the shadow.
     */
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        transitionRoot.classList.add("is-opening");

        /*
         * Scroll must be reset BEFORE
         * the page becomes visible.
         */
        window.scrollTo(0, 0);

        /*
         * Reveal page content while
         * the panels move away.
         */
        revealCurrentPage();

        /*
         * Cleanup after transition.
         */
        setTimeout(() => {
          finishIncomingTransition();
        }, CONFIG.openDuration + 120);
      });
    });
  }

  /* =========================================================
       PAGE REVEAL
       ========================================================= */

  function revealCurrentPage() {
    const content = document.querySelector(".page-content");

    if (!content) {
      return;
    }

    /*
     * Elements explicitly marked by the
     * existing templates.
     */
    const elements = content.querySelectorAll("[data-reveal-element]");

    if (!elements.length) {
      return;
    }

    elements.forEach((element, index) => {
      element.setAttribute("data-page-enter", "");

      element.style.transitionDelay = `${Math.min(80 + index * 55, 400)}ms`;
    });

    /*
     * Let the browser render the covered state.
     */
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        elements.forEach((element) => {
          element.classList.add("page-enter-visible");
        });
      });
    });
  }

  /* =========================================================
       FINISH INCOMING TRANSITION
       ========================================================= */

  function finishIncomingTransition() {
    if (!transitionRoot) {
      return;
    }

    transitionRoot.classList.remove(
      "is-active",
      "is-closing",
      "is-opening",
      "is-signal",
    );

    leftPanel.style.transition = "none";

    rightPanel.style.transition = "none";

    leftPanel.style.transform = "translate3d(-101%, 0, 0)";

    rightPanel.style.transform = "translate3d(101%, 0, 0)";

    document.body.style.overflow = "";

    document.body.classList.remove("is-shadow-fold-transitioning");

    isTransitioning = false;
  }

  /* =========================================================
       ANCHOR NAVIGATION
       ========================================================= */

  function setupAnchorNavigation() {
    document.addEventListener(
      "click",
      function (event) {
        const link = event.target.closest("a");

        if (!link) return;

        const href = link.getAttribute("href");

        if (!href) return;

        if (!href.startsWith("#")) {
          return;
        }

        const target = document.querySelector(href);

        if (!target) {
          return;
        }

        event.preventDefault();

        const header = document.querySelector("header, nav");

        const headerHeight = header ? header.offsetHeight : 0;

        const top =
          target.getBoundingClientRect().top +
          window.scrollY -
          headerHeight -
          20;

        window.scrollTo({
          top,
          behavior: CONFIG.reducedMotion ? "auto" : "smooth",
        });

        /*
         * Update URL without causing
         * another navigation.
         */
        if (history.pushState) {
          history.pushState(null, "", href);
        }
      },
      false,
    );
  }

  /* =========================================================
       PAGE EXIT PROTECTION
       ========================================================= */

  function setupPageExitProtection() {
    /*
     * Prevent accidental page unload from leaving
     * body locked if browser navigation happens
     * unexpectedly.
     */
    window.addEventListener("pageshow", function () {
      document.body.style.overflow = "";

      document.body.classList.remove("is-shadow-fold-transitioning");
    });

    /*
     * If user uses browser back/forward,
     * do not attempt to hijack it.
     *
     * Native navigation is safer here.
     */
    window.addEventListener("popstate", function () {
      sessionStorage.removeItem("shadowFoldPending");

      sessionStorage.removeItem("shadowFoldDestination");
    });
  }

  /* =========================================================
       PUBLIC API
       ========================================================= */

  window.ShadowFold = {
    navigate: function (href, label) {
      if (!href || isTransitioning) {
        return;
      }

      startNavigation(href, "page", label || "", null);
    },

    isTransitioning: function () {
      return isTransitioning;
    },
  };

  /* =========================================================
       START
       ========================================================= */

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, {
      once: true,
    });
  } else {
    init();
  }
})();
