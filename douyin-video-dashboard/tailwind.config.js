/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        douyin: {
          primary: '#FE2C55',    // 抖音红
          secondary: '#25F4EE',  // 抖音青
          dark: '#000000',       // 背景黑
          darkGray: '#161823',   // 卡片背景
          lightGray: '#1F1F1F',  // 次级背景
          text: '#FFFFFF',       // 主文字
          textSecondary: '#8A8B91' // 次级文字
        }
      },
      fontFamily: {
        sans: ['-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'sans-serif']
      }
    },
  },
  plugins: [],
}
