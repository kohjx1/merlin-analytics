/** @type {import('jest').Config} */
const config = {
    verbose: true,
    transform: {
        "^.+\\.svelte$": ["svelte-jester", { preprocess: true }],
        "^.+\\.js$": "babel-jest",
        "^.+\\.ts$": ["ts-jest", {
            babelConfig: true,
            useESM: true,
            compiler: "ttypescript"
        }]
    },
    transformIgnorePatterns: [
        "/node_modules/.pnpm/(?!jose)"
    ],
    moduleFileExtensions: ["js", "ts", "svelte"],
    setupFiles: [
        "<rootDir>config.ts",
    ],
    setupFilesAfterEnv: ["@testing-library/jest-dom/extend-expect"],
    reporters: ["default", ["jest-junit", { usePathForSuiteName: true, outputDirectory: 'coverage' }]],
    coverageReporters: ["clover", "json", "lcov", "text", "cobertura"],
};

module.exports = config;
