module.exports = {
    content: [
        './app/**/*.html',
        './app/**/*.js',
        './app/**/*.vue',
        './app/**/*.ts',
        './app/**/*.jsx',
        './app/**/*.tsx',
        './app/**/*.svelte'
    ],
    theme: {
        extend: {
            colors: {
                primary: '#4F46E5', // Indigo 600
                secondary: '#9333EA', // Purple 600
                accent: '#F59E0B', // Amber 500
                background: '#F3F4F6', // Gray 100
                text: '#111827', // Gray 900
            },
            fontFamily: {
                sans: ['Inter', 'sans-serif'],
                serif: ['Merriweather', 'serif'],
            },
        },
    },
    plugins: [],
};

tailwind.config = {
            theme: {
                extend: {
                    animation: {
                        'fade-in': 'fadeIn 0.5s ease-out forwards',
                        'fade-in-up': 'fadeInUp 0.6s ease-out forwards',
                        'scale-in': 'scaleIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards',
                        'slide-in': 'slideIn 0.5s ease-out forwards',
                    },
                    keyframes: {
                        fadeIn: {
                            '0%': { opacity: '0' },
                            '100%': { opacity: '1' }
                        },
                        fadeInUp: {
                            '0%': { opacity: '0', transform: 'translateY(20px)' },
                            '100%': { opacity: '1', transform: 'translateY(0)' }
                        },
                        scaleIn: {
                            '0%': { opacity: '0', transform: 'scale(0.95)' },
                            '100%': { opacity: '1', transform: 'scale(1)' }
                        },
                        slideIn: {
                            '0%': { opacity: '0', transform: 'translateX(-20px)' },
                            '100%': { opacity: '1', transform: 'translateX(0)' }
                        }
                    }
                }
            }
        }

tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        primary: {
                            50: '#f0fdf9',
                            100: '#ccfbef',
                            200: '#99f6e0',
                            300: '#5eead0',
                            400: '#2dd4bc',
                            500: '#14b8a6',
                            600: '#0d9488',
                            700: '#0f766e',
                            800: '#115e59',
                            900: '#134e4a',
                        }
                    },
                    fontFamily: {
                        sans: ['Inter', 'sans-serif'],
                    },
                }
            }
        }
