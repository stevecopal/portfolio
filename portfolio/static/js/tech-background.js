/**
 * Tech Background — réseau technologique statique (Canvas)
 * Couleur : vert électrique COPAL (#15A34A)
 * Grille en losanges, losanges remplis, points fixes, halos statiques, perspective fan
 * Pas d'animation : tout est dessiné une fois, redraw uniquement au resize / changement de thème
 */
(function () {
  const CONFIG = {
    color: "21, 163, 74", // rgb() de #15A34A
    gridStep: 70,
    gridOpacityLight: 0.08,
    gridOpacityDark: 0.14,
    pointCount: 42,
    glowCount: 3,
    mobileBreakpoint: 768,
    fanLines: 9,
    diamondFillOpacityLight: 0.04,
    diamondFillOpacityDark: 0.07,
    diamondSize: 6,
    // Static opacities (no pulse)
    pointOpacityLight: 0.35,
    pointOpacityDark: 0.55,
    glowOpacityLight: 0.08,
    glowOpacityDark: 0.16,
  };

  let canvas, ctx, width, height, dpr;
  let points = [];
  let glows = [];
  let diamonds = [];
  let isMobile = window.innerWidth < CONFIG.mobileBreakpoint;
  let isDark = document.documentElement.classList.contains("dark");

  function init() {
    canvas = document.createElement("canvas");
    canvas.id = "tech-background-canvas";
    document.body.prepend(canvas);
    ctx = canvas.getContext("2d");

    resize();
    generateAll();
    draw();
    bindEvents();
  }

  function resize() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    canvas.style.width = width + "px";
    canvas.style.height = height + "px";
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    isMobile = width < CONFIG.mobileBreakpoint;
  }

  function generateAll() {
    generatePoints();
    generateGlows();
    generateDiamonds();
  }

  function generatePoints() {
    const count = isMobile
      ? Math.round(CONFIG.pointCount / 2)
      : CONFIG.pointCount;
    points = Array.from({ length: count }, () => ({
      x: Math.random() * width,
      y: Math.random() * height,
      radius: Math.random() * 1.8 + 0.8,
      intensity: Math.random() * 0.5 + 0.5,
    }));
  }

  function generateGlows() {
    const count = isMobile ? 2 : CONFIG.glowCount;
    glows = Array.from({ length: count }, () => ({
      x: Math.random() * width,
      y: Math.random() * height,
      radius: Math.random() * 120 + 90,
    }));
  }

  function generateDiamonds() {
    diamonds = [];
    const diag = CONFIG.gridStep * 1.4;
    const s = CONFIG.diamondSize;
    for (let x = -height; x < width + height; x += diag) {
      for (let y = -height; y < height; y += diag) {
        const offsetX = (Math.round(y / diag) % 2 === 0) ? 0 : diag / 2;
        const px = x + offsetX;
        const py = y;
        if (px >= -diag && px <= width + diag && py >= -diag && py <= height + diag) {
          diamonds.push({ x: px, y: py, size: s });
        }
      }
    }
  }

  /* ── Drawing ──────────────────────────────────────────── */

  function drawGrid() {
    const opacity = isDark ? CONFIG.gridOpacityDark : CONFIG.gridOpacityLight;
    ctx.strokeStyle = `rgba(${CONFIG.color}, ${opacity})`;
    ctx.lineWidth = 1;
    const diag = CONFIG.gridStep * 1.4;
    const span = width + height;

    ctx.beginPath();
    for (let x = -height; x < span; x += diag) {
      ctx.moveTo(x, 0);
      ctx.lineTo(x + height, height);
    }
    for (let x = 0; x < span; x += diag) {
      ctx.moveTo(x, 0);
      ctx.lineTo(x - height, height);
    }
    ctx.stroke();
  }

  function drawFilledDiamonds() {
    const opacity = isDark ? CONFIG.diamondFillOpacityDark : CONFIG.diamondFillOpacityLight;
    ctx.fillStyle = `rgba(${CONFIG.color}, ${opacity})`;

    diamonds.forEach((d) => {
      const s = d.size;
      ctx.beginPath();
      ctx.moveTo(d.x, d.y - s);
      ctx.lineTo(d.x + s, d.y);
      ctx.lineTo(d.x, d.y + s);
      ctx.lineTo(d.x - s, d.y);
      ctx.closePath();
      ctx.fill();
    });
  }

  function drawPerspectiveFan() {
    const originX = width * (isMobile ? 0.9 : 0.85);
    const originY = height * 0.96;
    const opacity = isDark ? 0.16 : 0.08;
    const length = Math.max(width, height) * 0.55;

    ctx.strokeStyle = `rgba(${CONFIG.color}, ${opacity})`;
    ctx.lineWidth = 1;
    for (let i = 0; i < CONFIG.fanLines; i++) {
      const angle = Math.PI + (Math.PI / 2) * (i / (CONFIG.fanLines - 1));
      ctx.beginPath();
      ctx.moveTo(originX, originY);
      ctx.lineTo(
        originX + Math.cos(angle) * length,
        originY + Math.sin(angle) * length,
      );
      ctx.stroke();
    }

    // Points fixes le long de l'arc
    ctx.fillStyle = `rgba(${CONFIG.color}, ${opacity * 3})`;
    for (let i = 0; i < CONFIG.fanLines; i++) {
      const angle = Math.PI + (Math.PI / 2) * (i / (CONFIG.fanLines - 1));
      const r = length * 0.6;
      const px = originX + Math.cos(angle) * r;
      const py = originY + Math.sin(angle) * r;
      ctx.beginPath();
      ctx.arc(px, py, 1.8, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  function drawGlows() {
    const baseAlpha = isDark ? CONFIG.glowOpacityDark : CONFIG.glowOpacityLight;
    glows.forEach((g) => {
      const gradient = ctx.createRadialGradient(g.x, g.y, 0, g.x, g.y, g.radius);
      gradient.addColorStop(0, `rgba(${CONFIG.color}, ${baseAlpha})`);
      gradient.addColorStop(1, `rgba(${CONFIG.color}, 0)`);
      ctx.fillStyle = gradient;
      ctx.beginPath();
      ctx.arc(g.x, g.y, g.radius, 0, Math.PI * 2);
      ctx.fill();
    });
  }

  function drawPoints() {
    const baseAlpha = isDark ? CONFIG.pointOpacityDark : CONFIG.pointOpacityLight;
    points.forEach((p) => {
      const alpha = baseAlpha * p.intensity;

      // Small static halo
      ctx.beginPath();
      ctx.fillStyle = `rgba(${CONFIG.color}, ${alpha * 0.2})`;
      ctx.arc(p.x, p.y, p.radius * 3.5, 0, Math.PI * 2);
      ctx.fill();

      // Core dot
      ctx.beginPath();
      ctx.fillStyle = `rgba(${CONFIG.color}, ${alpha})`;
      ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
      ctx.fill();
    });
  }

  function draw() {
    ctx.clearRect(0, 0, width, height);
    drawGrid();
    drawFilledDiamonds();
    drawPerspectiveFan();
    drawGlows();
    drawPoints();
  }

  /* ── Events ───────────────────────────────────────────── */

  function bindEvents() {
    let resizeTimeout;
    window.addEventListener("resize", () => {
      clearTimeout(resizeTimeout);
      resizeTimeout = setTimeout(() => {
        resize();
        generateAll();
        draw();
      }, 150);
    });

    // Redraw on theme change
    const observer = new MutationObserver(() => {
      const newDark = document.documentElement.classList.contains("dark");
      if (newDark !== isDark) {
        isDark = newDark;
        draw();
      }
    });
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ["class"],
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
