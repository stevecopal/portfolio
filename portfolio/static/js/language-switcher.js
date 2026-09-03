/* ============================================================
   LANGUAGE SWITCHER
   Seamless language change without full page reload.
   Posts the language cookie, fetches the new page content,
   and swaps the DOM while preserving scroll position.
   ============================================================ */

(function () {
  "use strict";

  var _busy = false;

  function init() {
    document.querySelectorAll("form[action*='set_language']").forEach(function (form) {
      form.addEventListener("submit", handleSubmit);
    });
  }

  function handleSubmit(e) {
    e.preventDefault();
    if (_busy) return;
    _busy = true;

    var form = e.target;
    var formData = new FormData(form);

    // 1. POST language change to set the cookie
    fetch(form.action, {
      method: "POST",
      body: formData,
      headers: { "X-Requested-With": "XMLHttpRequest" },
    })
      .then(function () {
        // 2. Fetch the current page in the new language
        return fetch(window.location.href, {
          headers: { "X-Requested-With": "XMLHttpRequest" },
        });
      })
      .then(function (res) { return res.text(); })
      .then(function (html) {
        swapContent(html);
        _busy = false;
      })
      .catch(function () {
        // Fallback: reload if fetch fails
        window.location.reload();
        _busy = false;
      });
  }

  function swapContent(html) {
    var parser = new DOMParser();
    var doc = parser.parseFromString(html, "text/html");

    // Preserve scroll position
    var scrollY = window.scrollY;

    // Swap the <html> lang attribute
    var newLang = doc.documentElement.getAttribute("lang");
    if (newLang) document.documentElement.setAttribute("lang", newLang);

    // Swap main content
    var newMain = doc.querySelector("main");
    var oldMain = document.querySelector("main");
    if (newMain && oldMain) {
      oldMain.innerHTML = newMain.innerHTML;
    }

    // Swap navbar
    var newNav = doc.querySelector(".navbar, #navbar");
    var oldNav = document.querySelector(".navbar, #navbar");
    if (newNav && oldNav) {
      oldNav.innerHTML = newNav.innerHTML;
    }

    // Swap mobile menu
    var newMobile = doc.querySelector("#mobileMenu");
    var oldMobile = document.querySelector("#mobileMenu");
    if (newMobile && oldMobile) {
      oldMobile.innerHTML = newMobile.innerHTML;
    }

    // Swap mobile overlay
    var newOverlay = doc.querySelector("#mobileOverlay");
    var oldOverlay = document.querySelector("#mobileOverlay");
    if (newOverlay && oldOverlay) {
      oldOverlay.className = newOverlay.className;
    }

    // Restore scroll position
    window.scrollTo(0, scrollY);

    // Re-initialize language switcher forms
    init();

    // Re-initialize navigation (mobile menu, smooth scroll, etc.)
    if (typeof initMobileMenu === "function") initMobileMenu();
    if (typeof initActiveNavLinks === "function") initActiveNavLinks();
    if (typeof initSmoothScroll === "function") initSmoothScroll();

    // Re-initialize home reveal if on home page
    if (window.HomeReveal && typeof HomeReveal.refresh === "function") {
      HomeReveal.refresh();
    }
  }

  // Auto-init
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
