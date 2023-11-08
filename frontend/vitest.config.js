import { defineConfig } from 'vitest'

export default defineConfig({
    test: {
        files: {
            include: ['**/test/**/*', 'src/**/*.*.test.js'],
        }
    }
})