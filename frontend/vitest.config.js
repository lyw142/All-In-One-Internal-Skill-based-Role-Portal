import { defineConfig } from 'vitest/config'

export default defineConfig({
    test: {
        files: {
            include: ['**/test/**/*', 'src/**/*.*.test.js'],
        }
    }
})