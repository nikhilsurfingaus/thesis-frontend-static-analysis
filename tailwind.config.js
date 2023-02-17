/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./src/**/*.{js,jsx,ts,tsx}",
    ],
    theme: {
        extend: {
            screens: {
                'xsm': '400px',
                '3xl': '1680px',
            },
        },
    },
    plugins: [],
}