import type { Config } from "tailwindcss";

export default {
  content: ["./app/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        parchment: "#f5f0e1",
        ink: "#16110d",
        verdict: "#0f5b4a",
        brief: "#9b5c2e",
      },
      fontFamily: {
        display: ["Georgia", "serif"],
        body: ["ui-sans-serif", "system-ui"],
      },
    },
  },
  plugins: [],
} satisfies Config;
