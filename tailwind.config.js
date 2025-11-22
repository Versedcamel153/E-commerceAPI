/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./developer_auth/templates/developer_auth/**/*.{html,js}",
    "./static/css/styles/*.css",
  ],
  plugins: [
    require('daisyui'),
  ]
}

