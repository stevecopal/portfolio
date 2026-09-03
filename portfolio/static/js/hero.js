/* ============================================================
   COPAL HERO — "THE CORE"
   A looping organic-technological matter that builds itself in
   the dark, peaks in green light, collapses, and starts again.

   Cycle (~10.5s):
     DORMANT → AWAKEN → BUILD → PEAK → COLLAPSE → SHADOW
   Interactions: mouse parallax + proximity, click → #work.

   Performance:
     - requestAnimationFrame, paused when off-screen / hidden tab
     - devicePixelRatio capped at 2, particle count scaled
     - prefers-reduced-motion → single elegant static frame
   ============================================================ */

(function () {
  'use strict';

  var hero = document.getElementById('hero');
  var core = document.getElementById('theCore');
  var canvas = document.getElementById('coreCanvas');
  if (!hero || !core || !canvas) return;
  var ctx = canvas.getContext('2d');
  if (!ctx) return;

  var REDUCED = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ── Palette ────────────────────────────────────────────────
  var GREEN = '21,163,74';     // #15A34A — the light
  var GREEN_L = '46,213,115';  // #2ED573 brighter nucleus
  var WHITE = '255,255,255';
  var GREY = '173,181,189';

  // ── Cycle envelopes (phase fraction → value) ──────────────
  var CYCLE = 10.5;
  var KF_INTENSITY = [[0, 0.14], [0.18, 0.14], [0.32, 0.55], [0.50, 1.0], [0.62, 0.92], [0.74, 0.30], [1, 0.14]];
  var KF_STRUCTURE = [[0, 0], [0.18, 0], [0.32, 0.55], [0.50, 1.0], [0.62, 0.88], [0.74, 0.15], [1, 0]];
  var KF_CONNECT   = [[0, 0], [0.26, 0], [0.44, 1.0], [0.62, 0.92], [0.74, 0.22], [1, 0]];

  // ── State ──────────────────────────────────────────────────
  var W = 0, H = 0, DPR = 1, CX = 0, CY = 0, R = 0;
  var particles = [], nodes = [], connections = [], labels = [];
  var mouse = { inside: false, nx: 0, ny: 0 };
  var parallax = { x: 0, y: 0 };
  var prox = 0, speedBoost = 0, extraGlow = 0;
  var clickState = { active: false, t0: 0 };
  var running = false, rafId = null, lastT = 0, elapsed = 0;
  var onResize = null;

  // ── Helpers ────────────────────────────────────────────────
  function smoothstep(a, b, x) {
    x = Math.max(0, Math.min(1, (x - a) / (b - a)));
    return x * x * (3 - 2 * x);
  }
  function env(kf, p) {
    for (var i = 0; i < kf.length - 1; i++) {
      if (p >= kf[i][0] && p <= kf[i + 1][0]) {
        return kf[i][1] + (kf[i + 1][1] - kf[i][1]) * smoothstep(kf[i][0], kf[i + 1][0], p);
      }
    }
    return kf[kf.length - 1][1];
  }
  function noise(angle, t, seed) {
    return Math.sin(angle * 3 + t * 0.8 + seed) * 0.5
         + Math.sin(angle * 5 - t * 0.5 + seed * 2.7) * 0.3
         + Math.sin(angle * 7 + t * 0.35 + seed * 4.3) * 0.2;
  }
  function clamp(v, lo, hi) { return v < lo ? lo : (v > hi ? hi : v); }

  // ── Setup ──────────────────────────────────────────────────
  function setup() {
    DPR = Math.min(window.devicePixelRatio || 1, 2);
    var rect = core.getBoundingClientRect();
    W = Math.max(1, Math.round(rect.width));
    H = Math.max(1, Math.round(rect.height));
    canvas.width = Math.round(W * DPR);
    canvas.height = Math.round(H * DPR);
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    CX = W / 2;
    CY = H / 2;
    R = Math.min(W, H) / 2 * 0.92;

    buildParticles();
    buildNodes();
    buildConnections();
    locateLabels();
  }

  function buildParticles() {
    var count = W < 640 ? 34 : (W < 1100 ? 60 : 100);
    particles = [];
    for (var i = 0; i < count; i++) {
      var green = Math.random() < 0.22;
      particles.push({
        a: Math.random() * Math.PI * 2,
        d: 0.5 + Math.random() * 0.68,
        speed: (Math.random() - 0.5) * 0.09,
        size: 0.5 + Math.random() * 1.3,
        baseAlpha: (green ? 0.16 : 0.09) + Math.random() * 0.14,
        pull: 0.25 + Math.random() * 0.35,
        green: green,
        seed: Math.random() * 100
      });
    }
  }

  function buildNodes() {
    var defs = [
      { a: 0.15, r: 0.40, seed: 1, green: 1, size: 2.0 },
      { a: 0.55, r: 0.52, seed: 2, green: 0, size: 1.5 },
      { a: 0.95, r: 0.38, seed: 3, green: 0, size: 1.4 },
      { a: 1.35, r: 0.56, seed: 4, green: 1, size: 1.7 },
      { a: 1.75, r: 0.44, seed: 5, green: 0, size: 1.5 },
      { a: 2.15, r: 0.58, seed: 6, green: 0, size: 1.3 },
      { a: 2.55, r: 0.36, seed: 7, green: 1, size: 1.8 },
      { a: 2.95, r: 0.52, seed: 8, green: 0, size: 1.4 },
      { a: 3.35, r: 0.42, seed: 9, green: 0, size: 1.5 },
      { a: 3.85, r: 0.55, seed: 10, green: 1, size: 1.6 },
      { a: 4.30, r: 0.40, seed: 11, green: 0, size: 1.4 },
      { a: 4.80, r: 0.50, seed: 12, green: 0, size: 1.3 },
      { a: 5.25, r: 0.62, seed: 13, green: 1, size: 1.5 },
      { a: 5.80, r: 0.34, seed: 14, green: 0, size: 1.4 }
    ];
    nodes = defs.map(function (d) {
      return {
        a: d.a, r: d.r, seed: d.seed * 1.9,
        green: d.green, size: d.size,
        x: 0, y: 0
      };
    });
  }

  function buildConnections() {
    connections = [];
    var n = nodes.length;
    // node → node links
    for (var i = 0; i < 11; i++) {
      var a = Math.floor(Math.random() * n);
      var b = Math.floor(Math.random() * n);
      if (b === a) b = (b + 1) % n;
      connections.push({ i: a, j: b, seed: Math.random() * 100, green: Math.random() < 0.4 });
    }
    // node → core links
    for (var k = 0; k < 6; k++) {
      connections.push({
        i: Math.floor(Math.random() * n), j: -1,
        seed: Math.random() * 100, green: Math.random() < 0.6
      });
    }
  }

  function locateLabels() {
    labels = [];
    var els = core.querySelectorAll('[data-core-label]');
    var cr = core.getBoundingClientRect();
    for (var i = 0; i < els.length; i++) {
      var r = els[i].getBoundingClientRect();
      labels.push({
        el: els[i],
        x: r.left + r.width / 2 - cr.left,
        y: r.top + r.height / 2 - cr.top
      });
    }
  }

  function updateNodePositions(t) {
    for (var i = 0; i < nodes.length; i++) {
      var nd = nodes[i];
      var a = nd.a + t * 0.10 * nd.seed * 0.35;
      var rad = R * nd.r * (1 + 0.045 * noise(a, t * 0.5, nd.seed));
      nd.x = Math.cos(a) * rad;
      nd.y = Math.sin(a) * rad;
    }
  }

  // ── Draw layers ────────────────────────────────────────────
  function drawCore(t, bright) {
    var pulse = 1 + 0.045 * Math.sin(t * 2.2);
    var r0 = R * 0.155 * pulse;

    // wide soft glow
    var glow = ctx.createRadialGradient(0, 0, 0, 0, 0, R * 0.55);
    glow.addColorStop(0, 'rgba(' + GREEN + ',' + (0.17 * bright).toFixed(3) + ')');
    glow.addColorStop(0.45, 'rgba(' + GREEN + ',' + (0.07 * bright).toFixed(3) + ')');
    glow.addColorStop(1, 'rgba(' + GREEN + ',0)');
    ctx.fillStyle = glow;
    ctx.beginPath();
    ctx.arc(0, 0, R * 0.55, 0, Math.PI * 2);
    ctx.fill();

    // irregular nucleus
    var seg = 64;
    ctx.beginPath();
    for (var i = 0; i <= seg; i++) {
      var a = (i / seg) * Math.PI * 2;
      var rad = r0 * (1 + 0.20 * noise(a, t * 1.5, 3.1));
      var x = Math.cos(a) * rad, y = Math.sin(a) * rad;
      if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.closePath();
    var cg = ctx.createRadialGradient(0, 0, 0, 0, 0, r0 * 1.5);
    cg.addColorStop(0, 'rgba(' + GREEN_L + ',' + (0.85 * bright).toFixed(3) + ')');
    cg.addColorStop(0.45, 'rgba(' + GREEN + ',' + (0.5 * bright).toFixed(3) + ')');
    cg.addColorStop(1, 'rgba(' + GREEN + ',0)');
    ctx.fillStyle = cg;
    ctx.fill();

    // hot center
    ctx.beginPath();
    ctx.arc(0, 0, r0 * 0.34, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(' + GREEN_L + ',' + (0.9 * bright).toFixed(3) + ')';
    ctx.fill();

    // contained-energy rings
    for (var ring = 0; ring < 3; ring++) {
      var rr = r0 * (1.6 + ring * 0.85);
      var rot = t * (0.16 + ring * 0.08);
      var useGreen = ring !== 1;
      ctx.beginPath();
      for (var j = 0; j <= 44; j++) {
        var aj = (j / 44) * Math.PI * 2 + rot;
        var radj = rr * (1 + 0.24 * noise(aj, t * 0.9, ring + 5));
        var xj = Math.cos(aj) * radj, yj = Math.sin(aj) * radj;
        if (j === 0) ctx.moveTo(xj, yj); else ctx.lineTo(xj, yj);
      }
      ctx.closePath();
      ctx.strokeStyle = 'rgba(' + (useGreen ? GREEN : WHITE) + ',' + ((0.08 + 0.10 * ring) * bright).toFixed(3) + ')';
      ctx.lineWidth = 1;
      ctx.stroke();
    }
  }

  function drawShell(t, structure, bright) {
    var shells = [
      { rr: 0.80, amp: 0.06, seed: 11, green: 0 },
      { rr: 0.63, amp: 0.085, seed: 23, green: 1 }
    ];
    for (var s = 0; s < shells.length; s++) {
      var sh = shells[s];
      var N = 90;
      var pts = [];
      for (var i = 0; i < N; i++) {
        var a = (i / N) * Math.PI * 2;
        var rad = R * sh.rr * (1 + sh.amp * noise(a, t * 0.55, sh.seed));
        pts.push([Math.cos(a) * rad, Math.sin(a) * rad]);
      }
      var alpha = (0.05 + 0.30 * structure) * bright;

      // faint continuous ring
      ctx.beginPath();
      for (var k = 0; k <= N; k++) {
        var pt = pts[k % N];
        if (k === 0) ctx.moveTo(pt[0], pt[1]); else ctx.lineTo(pt[0], pt[1]);
      }
      ctx.closePath();
      ctx.strokeStyle = 'rgba(' + (sh.green ? GREEN : WHITE) + ',' + (alpha * 0.4).toFixed(3) + ')';
      ctx.lineWidth = 1;
      ctx.stroke();

      // broken polygonal facets
      ctx.beginPath();
      for (var c = 0; c < N; c += 6) {
        var v1 = pts[c], v2 = pts[(c + 6) % N];
        if (noise(c, t * 0.4, sh.seed + 7) > -0.35) {
          ctx.moveTo(v1[0], v1[1]);
          ctx.lineTo(v2[0], v2[1]);
        }
      }
      ctx.strokeStyle = 'rgba(' + (sh.green ? GREEN_L : WHITE) + ',' + (alpha * 0.6).toFixed(3) + ')';
      ctx.lineWidth = 0.75;
      ctx.stroke();

      // radial struts toward the core
      ctx.beginPath();
      for (var st = 0; st < N; st += 15) {
        var sp = pts[st];
        if (noise(st, t * 0.3, sh.seed + 13) > -0.1) {
          ctx.moveTo(sp[0], sp[1]);
          ctx.lineTo(sp[0] * 0.82, sp[1] * 0.82);
        }
      }
      ctx.strokeStyle = 'rgba(' + (sh.green ? GREEN : GREY) + ',' + (alpha * 0.35).toFixed(3) + ')';
      ctx.lineWidth = 0.6;
      ctx.stroke();
    }
  }

  function drawOrbits(t, bright, spin, p, pass) {
    var defs = [
      // [rx, ry, tilt0, speed, dash, alpha, dots, pass]
      [1.16, 0.44, 0.55, 0.10, [1, 11], 0.10, 0, -1],
      [1.02, 0.98, 1.25, -0.07, [2, 15], 0.08, 0, -1],
      [1.32, 0.52, 0.90, 0.13, [3, 18], 0.15, 2, 0],
      [0.56, 1.08, -0.40, -0.09, [1, 13], 0.11, 1, 0],
      [1.22, 0.62, -1.15, 0.08, [2, 20], 0.13, 3, 1]
    ];
    for (var i = 0; i < defs.length; i++) {
      var o = defs[i];
      if (o[7] !== pass) continue;
      var rot = t * o[3] * spin + o[2];
      ctx.save();
      ctx.rotate(rot);
      // partial arcs — orbits breathe
      var frac = 0.70 + 0.30 * (0.5 + 0.5 * Math.sin(p * Math.PI * 2 + i * 2.1));
      ctx.beginPath();
      ctx.ellipse(0, 0, R * o[0], R * o[1], 0, 0, Math.PI * 2 * frac);
      ctx.setLineDash(o[4]);
      ctx.strokeStyle = 'rgba(' + (i % 2 ? GREEN : WHITE) + ',' + (o[5] * bright).toFixed(3) + ')';
      ctx.lineWidth = 1;
      ctx.stroke();
      ctx.setLineDash([]);
      // luminous dots riding the orbit
      for (var d = 0; d < o[6]; d++) {
        var da = (t * 0.9 * spin + d * 2.1 + i) % (Math.PI * 2);
        var dx = Math.cos(da) * R * o[0];
        var dy = Math.sin(da) * R * o[1];
        var tw = 0.55 + 0.45 * Math.sin(t * 3 + d * 5 + i);
        ctx.beginPath();
        ctx.arc(dx, dy, 1.7, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(' + GREEN_L + ',' + (0.55 * tw * bright).toFixed(3) + ')';
        ctx.fill();
        ctx.beginPath();
        ctx.arc(dx, dy, 4.2, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(' + GREEN + ',' + (0.12 * tw * bright).toFixed(3) + ')';
        ctx.fill();
      }
      ctx.restore();
    }
  }

  function drawParticles(t, bright, connect) {
    for (var i = 0; i < particles.length; i++) {
      var pt = particles[i];
      var ang = pt.a + t * pt.speed;
      var dist = R * pt.d * (1 - 0.22 * connect * pt.pull) * (1 + 0.05 * Math.sin(t * 0.7 + pt.seed));
      var x = Math.cos(ang) * dist;
      var y = Math.sin(ang) * dist;
      var tw = 0.45 + 0.55 * Math.sin(t * 2.4 + pt.seed * 7);
      var alpha = pt.baseAlpha * bright * (0.35 + 0.65 * tw);
      ctx.beginPath();
      ctx.arc(x, y, pt.size, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(' + (pt.green ? GREEN_L : WHITE) + ',' + alpha.toFixed(3) + ')';
      ctx.fill();
      if (pt.green) {
        ctx.beginPath();
        ctx.arc(x, y, pt.size * 2.6, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(' + GREEN + ',' + (alpha * 0.25).toFixed(3) + ')';
        ctx.fill();
      }
    }
  }

  function drawConnections(t, connect, bright, p) {
    if (connect < 0.02) return;
    for (var i = 0; i < connections.length; i++) {
      var c = connections[i];
      var blink = 0.5 + 0.5 * Math.sin(t * 1.3 + c.seed);
      var on = blink > 0.55 ? 1 : smoothstep(0.45, 0.55, blink);
      // staggered windows so links flicker in and out organically
      var win = (p + (c.seed % 10) * 0.023) % 1;
      if (win > 0.75) on *= smoothstep(0.75, 0.68, win);
      var alpha = connect * bright * on * 0.5;
      if (alpha < 0.01) continue;
      var n1 = nodes[c.i];
      var x2 = c.j === -1 ? 0 : nodes[c.j].x;
      var y2 = c.j === -1 ? 0 : nodes[c.j].y;
      ctx.beginPath();
      ctx.moveTo(n1.x, n1.y);
      ctx.lineTo(x2, y2);
      ctx.strokeStyle = 'rgba(' + (c.green ? GREEN : WHITE) + ',' + alpha.toFixed(3) + ')';
      ctx.lineWidth = 0.75;
      ctx.stroke();
    }
    // node dots
    for (var k = 0; k < nodes.length; k++) {
      var nd = nodes[k];
      var tw = 0.4 + 0.6 * Math.sin(t * 1.7 + nd.seed * 3);
      var a = connect * bright * (0.15 + 0.5 * Math.max(0, tw)) + extraGlow * 0.35;
      ctx.beginPath();
      ctx.arc(nd.x, nd.y, nd.size, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(' + (nd.green ? GREEN_L : WHITE) + ',' + clamp(a, 0, 0.9).toFixed(3) + ')';
      ctx.fill();
      if (nd.green) {
        ctx.beginPath();
        ctx.arc(nd.x, nd.y, nd.size * 2.4, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(' + GREEN + ',' + (clamp(a, 0, 0.9) * 0.3).toFixed(3) + ')';
        ctx.fill();
      }
    }
  }

  function drawLabelLines(t, alpha, p) {
    if (alpha < 0.02) return;
    for (var i = 0; i < labels.length; i++) {
      var L = labels[i];
      var dx = CX - L.x, dy = CY - L.y;
      var len = Math.sqrt(dx * dx + dy * dy);
      if (len < 10) continue;
      var ux = dx / len, uy = dy / len;
      var lw = alpha * (0.5 + 0.5 * Math.sin(t * 1.1 + i * 2.4));
      var fx = L.x + ux * (len - 10);
      var fy = L.y + uy * (len - 10);
      ctx.beginPath();
      ctx.moveTo(fx, fy);
      ctx.lineTo(CX - ux * R * 0.36, CY - uy * R * 0.36);
      ctx.strokeStyle = 'rgba(' + GREEN + ',' + (lw * 0.45).toFixed(3) + ')';
      ctx.lineWidth = 0.75;
      ctx.stroke();
      ctx.beginPath();
      ctx.arc(fx, fy, 1.5, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(' + GREEN_L + ',' + (lw * 0.85).toFixed(3) + ')';
      ctx.fill();
    }
    // sync DOM label opacity (subtle breathing)
    for (var j = 0; j < labels.length; j++) {
      labels[j].el.style.opacity = (0.15 + 0.85 * alpha).toFixed(3);
    }
  }

  // ── Click sequence ─────────────────────────────────────────
  function clickProgress() {
    return clamp((performance.now() - clickState.t0) / 1250, 0, 1);
  }
  function drawClickFx(t, click) {
    // converging lines during contraction
    var conv = click < 0.55 ? Math.sin((click / 0.55) * Math.PI) : 0;
    if (conv > 0.02) {
      ctx.beginPath();
      for (var i = 0; i < 26; i++) {
        var a = (i / 26) * Math.PI * 2 + t * 0.3;
        var r1 = R * (0.55 + 0.35 * Math.sin(i * 2.7));
        ctx.moveTo(Math.cos(a) * r1, Math.sin(a) * r1);
        ctx.lineTo(0, 0);
      }
      ctx.strokeStyle = 'rgba(' + GREEN + ',' + (conv * 0.22).toFixed(3) + ')';
      ctx.lineWidth = 0.75;
      ctx.stroke();
    }
  }

  function scrollToWork() {
    var el = document.getElementById('work');
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  // ── Master draw ────────────────────────────────────────────
  function draw(t, click) {
    ctx.clearRect(0, 0, W, H);

    var p = (t % CYCLE) / CYCLE;
    var intensity = env(KF_INTENSITY, p);
    var structure = env(KF_STRUCTURE, p);
    var connect = env(KF_CONNECT, p);
    var bright = intensity * (1 + extraGlow * 0.6);
    var spin = 1 + speedBoost * 0.5;

    // click envelope
    var scale = 1;
    if (click > 0 && click < 1) {
      if (click < 0.35) scale = 1 + 0.13 * Math.sin((click / 0.35) * Math.PI * 0.5);
      else if (click < 0.6) scale = 1.13 - 0.23 * ((click - 0.35) / 0.25);
      else scale = 0.9 + 0.1 * smoothstep(0.6, 1, click);
      bright *= 1 + 0.35 * Math.sin(Math.PI * click);
      spin *= 1 + 0.5 * Math.sin(Math.PI * click);
    }

    updateNodePositions(t);

    ctx.save();
    ctx.translate(CX, CY);
    ctx.scale(scale, scale);

    // far layers — most parallax
    ctx.save();
    ctx.translate(parallax.x * R * 0.07, parallax.y * R * 0.07);
    drawOrbits(t, bright, spin, p, -1);
    ctx.restore();

    ctx.save();
    ctx.translate(parallax.x * R * 0.045, parallax.y * R * 0.045);
    drawShell(t, structure, bright);
    ctx.restore();

    ctx.save();
    ctx.translate(parallax.x * R * 0.03, parallax.y * R * 0.03);
    drawOrbits(t, bright, spin, p, 0);
    drawCore(t, bright);
    ctx.restore();

    // near layer — least parallax
    ctx.save();
    ctx.translate(parallax.x * R * 0.015, parallax.y * R * 0.015);
    drawOrbits(t, bright, spin, p, 1);
    drawParticles(t, bright, connect);
    drawConnections(t, connect, bright, p);
    ctx.restore();

    drawClickFx(t, click);
    ctx.restore();

    // labels follow the cycle
    drawLabelLines(t, connect * (0.35 + 0.65 * bright), p);

    // subtle green flash at click peak
    if (click > 0 && click < 1) {
      var fl = Math.sin(Math.PI * click) * 0.10;
      ctx.save();
      ctx.translate(CX, CY);
      var fg = ctx.createRadialGradient(0, 0, 0, 0, 0, R * 0.9);
      fg.addColorStop(0, 'rgba(' + GREEN + ',' + fl.toFixed(3) + ')');
      fg.addColorStop(1, 'rgba(' + GREEN + ',0)');
      ctx.fillStyle = fg;
      ctx.beginPath();
      ctx.arc(0, 0, R * 0.9, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }
  }

  // ── Loop ───────────────────────────────────────────────────
  function frame(now) {
    if (!running) { rafId = null; return; }
    var dt = Math.min((now - lastT) / 1000, 0.1);
    lastT = now;
    if (!document.hidden) elapsed += dt;
    var t = elapsed;

    // smooth mouse states
    var tx = mouse.inside ? mouse.nx : 0;
    var ty = mouse.inside ? mouse.ny : 0;
    parallax.x += (tx - parallax.x) * 0.045;
    parallax.y += (ty - parallax.y) * 0.045;
    var sbTarget = mouse.inside ? Math.abs(mouse.nx) * 0.6 + Math.abs(mouse.ny) * 0.4 : 0;
    speedBoost += (sbTarget - speedBoost) * 0.04;
    extraGlow += (prox - extraGlow) * 0.05;

    var click = 0;
    if (clickState.active) {
      click = clickProgress();
      if (click >= 1) {
        clickState.active = false;
        scrollToWork();
        click = 0;
      }
    }

    draw(t, click);
    rafId = requestAnimationFrame(frame);
  }

  function start() {
    if (running || REDUCED) return;
    running = true;
    lastT = performance.now();
    rafId = requestAnimationFrame(frame);
  }
  function stop() {
    running = false;
    if (rafId) cancelAnimationFrame(rafId);
    rafId = null;
  }

  // ── Events ─────────────────────────────────────────────────
  hero.addEventListener('mousemove', function (e) {
    var r = hero.getBoundingClientRect();
    mouse.inside = true;
    mouse.nx = ((e.clientX - r.left) / r.width) * 2 - 1;
    mouse.ny = ((e.clientY - r.top) / r.height) * 2 - 1;

    var cr = core.getBoundingClientRect();
    var dx = e.clientX - (cr.left + cr.width / 2);
    var dy = e.clientY - (cr.top + cr.height / 2);
    prox = Math.sqrt(dx * dx + dy * dy) < cr.width * 0.72 ? 1 : 0;
  });
  hero.addEventListener('mouseleave', function () {
    mouse.inside = false;
    prox = 0;
  });

  canvas.addEventListener('click', function (e) {
    if (clickState.active) return;
    var r = core.getBoundingClientRect();
    var dx = e.clientX - (r.left + r.width / 2);
    var dy = e.clientY - (r.top + r.height / 2);
    if (Math.sqrt(dx * dx + dy * dy) > r.width * 0.58) return;
    clickState.active = true;
    clickState.t0 = performance.now();
  });

  onResize = function () {
    setup();
    if (REDUCED) drawStatic();
  };
  window.addEventListener('resize', onResize);

  // pause when off-screen
  if ('IntersectionObserver' in window && !REDUCED) {
    var io = new IntersectionObserver(function (entries) {
      if (entries[0].isIntersecting) start();
      else stop();
    }, { threshold: 0.03 });
    io.observe(hero);
  }

  // ── Init ───────────────────────────────────────────────────
  function drawStatic() {
    setup();
    // a quiet mid-build moment, frozen
    draw(5.1, 0);
    for (var i = 0; i < labels.length; i++) {
      labels[i].el.style.opacity = 0.6;
    }
  }

  if (REDUCED) {
    drawStatic();
  } else {
    setup();
    start();
  }
})();