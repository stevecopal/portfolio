/** @type {import('tailwindcss').Config} */

const ink = {
  DEFAULT: "#0A0A0A",
  950: "#050505",
  900: "#0A0A0A",
  800: "#141414",
  700: "#1F1F1F",
  600: "#2B2B2B",
  500: "#454545",
  400: "#666666",
  300: "#8C8C8C",
  200: "#B0B0AE",
  100: "#D4D4D0",
  50: "#E8E8E4",
};

const bone = {
  DEFAULT: "#F7F7F5",
  50: "#FBFBF9",
  100: "#F7F7F5",
  200: "#EFEFEC",
  300: "#E5E5E1",
  400: "#D8D8D3",
  500: "#C3C3BE",
};

module.exports = {
  content: [
    "./portfolio/templates/**/*.html",
    "./portfolio/static/js/**/*.js",
  ],
  theme: {
    container: {
      center: true,
      padding: {
        DEFAULT: "1.25rem",
        sm: "1.5rem",
        md: "2.5rem",
        xl: "3.5rem",
        "2xl": "4.5rem",
      },
    },
    extend: {
      colors: { ink, bone },
      boxShadow: {
        soft: "0 1px 2px rgba(10,10,10,.04), 0 14px 34px -20px rgba(10,10,10,.28)",
        lift: "0 2px 4px rgba(10,10,10,.05), 0 32px 64px -32px rgba(10,10,10,.5)",
        inset: "inset 0 0 0 1px rgba(10,10,10,.08)",
      },
      opacity: {
        15: "0.15",
        35: "0.35",
        45: "0.45",
        55: "0.55",
        65: "0.65",
        85: "0.85",
      },
      fontFamily: {
        display: [
          '"Bricolage Grotesque"',
          "ui-sans-serif",
          "system-ui",
          "sans-serif",
        ],
        sans: [
          '"Instrument Sans"',
          "ui-sans-serif",
          "system-ui",
          "sans-serif",
        ],
      },
      letterSpacing: {
        label: "0.22em",
        tightest: "-0.045em",
      },
      transitionDuration: {
        400: "400ms",
      },
      transitionTimingFunction: {
        out: "cubic-bezier(0.16, 1, 0.3, 1)",
      },
      keyframes: {
        marquee: {
          "0%": { transform: "translateX(0)" },
          "100%": { transform: "translateX(-50%)" },
        },
        blink: {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.25" },
        },
      },
      animation: {
        marquee: "marquee 42s linear infinite",
        blink: "blink 2.4s ease-in-out infinite",
      },
    },
  },
  plugins: [],
};
