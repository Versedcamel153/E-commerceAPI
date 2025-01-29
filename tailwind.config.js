/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./developer_auth/templates/developer_auth/**/*.{html,js}",
    "./static/css/styles/*.css",
  ],
  theme: {
    daisyui: {
      themes: [
        {
          mytheme: {
            
  "primary": "#e800ff",
            
  "secondary": "#0090ff",
            
  "accent": "#84a100",
            
  "neutral": "#241b0c",
            
  "base-200": "#e6ffff",
            
  "info": "#00d8ff",
            
  "success": "#7be162",
            
  "warning": "#da5c00",
            
  "error": "#f30044",
            },
          },
        ],
      },
  },
  plugins: [
    require('daisyui'),
  ],
}

