import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        clara: {
          blue: "#1B5E7B",
          orange: "#D46A1E",
          green: "#2E7D4F",
          bg: "#FAFAFA",
          text: "#1A1A2E",
          "text-secondary": "#4A4A5A",
          error: "#C62828",
          warning: "#F9A825",
          info: "#E3F2FD",
          card: "#F5F5F5",
          border: "#E0E0E0",
        },
      },
      fontFamily: {
        display: ['"Atkinson Hyperlegible"', "system-ui", "sans-serif"],
        body: ["Inter", "system-ui", "sans-serif"],
      },
      fontSize: {
        body: ["20px", { lineHeight: "1.6" }],
        "body-sm": ["18px", { lineHeight: "1.6" }],
        h1: ["36px", { lineHeight: "1.3" }],
        h2: ["28px", { lineHeight: "1.3" }],
        button: ["20px", { lineHeight: "1.0" }],
        label: ["16px", { lineHeight: "1.4" }],
      },
      spacing: {
        touch: "64px",
        "touch-sm": "48px",
        "touch-lg": "96px",
      },
      borderRadius: {
        bubble: "16px",
      },
    },
  },
  plugins: [],
};

export default config;
