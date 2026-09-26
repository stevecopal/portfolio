/* ============================================================
   TESTIMONIAL DECK
   Carrousel témoignages : carte centrale + cartes en éventail.
   Flèches prev/next, clavier et swipe tactile.
   ============================================================ */

(function () {
  "use strict";

  function pad(n) {
    return n < 10 ? "0" + n : String(n);
  }

  function initDeck(root) {
    if (!root || root.getAttribute("data-deck-ready") === "1") return;

    var cards = Array.prototype.slice.call(
      root.querySelectorAll("[data-deck-card]")
    );
    if (!cards.length) return;

    root.setAttribute("data-deck-ready", "1");

    var prevBtn = root.querySelector("[data-deck-prev]");
    var nextBtn = root.querySelector("[data-deck-next]");
    var currentEl = root.querySelector("[data-deck-current]");
    var totalEl = root.querySelector("[data-deck-total]");
    var nav = root.querySelector(".tdeck__nav");
    var index = 0;
    var total = cards.length;

    if (totalEl) totalEl.textContent = pad(total);

    /* Un seul avis : pas de navigation. */
    if (total < 2 && nav) {
      nav.style.display = "none";
    }

    function render() {
      for (var i = 0; i < total; i++) {
        var card = cards[i];
        var forward = (i - index + total) % total; // 0..total-1
        var backward = total - forward;

        card.classList.remove(
          "is-active",
          "is-prev-1",
          "is-prev-2",
          "is-next-1",
          "is-next-2"
        );

        if (forward === 0) {
          card.classList.add("is-active");
          card.setAttribute("aria-hidden", "false");
        } else {
          if (forward === 1) card.classList.add("is-next-1");
          else if (forward === 2) card.classList.add("is-next-2");
          else if (backward === 1) card.classList.add("is-prev-1");
          else if (backward === 2) card.classList.add("is-prev-2");
          card.setAttribute("aria-hidden", "true");
        }
      }

      if (currentEl) currentEl.textContent = pad(index + 1);
    }

    /* Rotation automatique : avis suivant toutes les 2 secondes
       (desktop et mobile). Chaque navigation manuelle redémarre le minuteur. */
    var autoTimer = null;

    function restartAuto() {
      if (autoTimer) clearInterval(autoTimer);
      autoTimer = setInterval(function () {
        index = (index + 1) % total;
        render();
      }, 10000);
    }

    function go(delta) {
      index = (index + delta + total) % total;
      render();
      restartAuto();
    }

    if (prevBtn) {
      prevBtn.addEventListener("click", function () {
        go(-1);
      });
    }
    if (nextBtn) {
      nextBtn.addEventListener("click", function () {
        go(1);
      });
    }

    /* Clavier (flèches gauche/droite) quand le carrousel a le focus. */
    root.setAttribute("tabindex", "-1");
    root.addEventListener("keydown", function (e) {
      if (e.key === "ArrowLeft") {
        e.preventDefault();
        go(-1);
      } else if (e.key === "ArrowRight") {
        e.preventDefault();
        go(1);
      }
    });

    /* Swipe tactile. */
    var startX = null;
    var startY = null;
    root.addEventListener(
      "touchstart",
      function (e) {
        if (e.touches.length !== 1) return;
        startX = e.touches[0].clientX;
        startY = e.touches[0].clientY;
      },
      { passive: true }
    );
    root.addEventListener(
      "touchend",
      function (e) {
        if (startX === null) return;
        var touch = e.changedTouches[0];
        var dx = touch.clientX - startX;
        var dy = touch.clientY - startY;
        startX = null;
        startY = null;
        if (Math.abs(dx) > 45 && Math.abs(dx) > Math.abs(dy)) {
          go(dx < 0 ? 1 : -1);
        }
      },
      { passive: true }
    );

    render();

    /* Lancer la rotation automatique (si plus d'un avis). */
    if (total > 1) restartAuto();
  }

  function initAll() {
    var decks = document.querySelectorAll("[data-deck]");
    for (var i = 0; i < decks.length; i++) {
      initDeck(decks[i]);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initAll);
  } else {
    initAll();
  }
})();
