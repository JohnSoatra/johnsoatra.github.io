/** @type {import('tailwindcss').Config} */

module.exports = {
    content: [
        './src/**/*.{js,jsx,ts,tsx}',
    ],
    theme: {
        extend: {
            screens: {
				'xs': '0px',
				'sm': '360px'
			},
            colors: {
                'low': '#f0f0f0'
            }
        },
    },
    plugins: [],
}

