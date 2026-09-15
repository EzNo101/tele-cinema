import type { Config } from 'tailwindcss'

export default <Partial<Config>>{
    theme: {
        extend: {
            colors: {
                brand: {
                    DEFAULT: '#4f46e5',
                    dark: '#3730a3',
                    light: '#6366f1',
                    soft: '#eef2ff'
                },
                surface: {
                    DEFAULT: '#ffffff',
                    alt: '#f4f4f5'
                }
            }
        }
    }
}