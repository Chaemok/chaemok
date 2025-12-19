/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      // 필요시 여기서 세부 수치 조절 가능
    },
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: [
      {
        smartants: {
          "primary": "#4f46e5",    // Indigo 600 (메인 브랜드 컬러)
          "secondary": "#8b5cf6",  // Violet 500 (포인트 컬러)
          "accent": "#0ea5e9",     // Sky 500 (강조 컬러)
          "neutral": "#1e293b",    // Slate 800 (텍스트/어두운 배경)
          "base-100": "#ffffff",    // 기본 배경 (흰색)
          "base-200": "#f8fafc",    // 보조 배경 (연한 그레이 - 아주 중요!)
          "info": "#3abff8",
          "success": "#36d399",
          "warning": "#fbbd23",
          "error": "#f87171",
        },
      },
    ],
  },
}