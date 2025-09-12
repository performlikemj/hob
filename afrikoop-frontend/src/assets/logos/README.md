Use this folder for logo and brand image assets that are imported in React components.

Recommended usage
- Import via modules so Vite optimizes: `import logoUrl from '../assets/logos/logo.svg'`
- Prefer SVG for crisp scaling. For raster, provide `@2x` where needed.
- Name examples: `logo.svg`, `logo-dark.svg`, `wordmark.svg`, `mark.png`.

Note: Favicon files should live in `public/favicons/` so they can be referenced by path (bypassing bundling).
