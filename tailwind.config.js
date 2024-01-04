/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./index.html"],
    theme: {
        extend: {
            screens: {
				'xs': '0px',
				'sm': '400px'
			},
        },
    },
    plugins: [],
}