# Repository Guidelines

This Astro site is fairly small, but contributors still benefit from a shared playbook. Use these notes to stay aligned with the current layout, commands, and workflow.

## Project Structure & Module Organization
- `src/pages/` holds routed content. Markdown (`.md`) files map directly to routes, while `.astro` pages handle richer layouts.
- Shared UI lives in `src/components/`, and page shells sit in `src/layouts/`. Reuse existing layouts before introducing new ones.
- Global styles load from `src/styles/global.css`. Keep component-scoped styles inline within the relevant `.astro` file.
- Binary assets (images, favicons) go under `public/` so Astro copies them verbatim at build time. Long-form data (e.g., rotating quotes) belongs in `src/data/`.

## Build, Test, and Development Commands
- `npm run dev` (or `make dev`) installs dependencies and starts Astro with hot reload.
- `npm run build` (or `make build`) produces the static site in `dist/`; run before submitting PRs.
- `npm run preview` serves the production build locally—helpful for sanity checks.
- `npm run astro check` runs Astro’s type-aware diagnostics; use it after editing layouts or server code.
- Issue submissions call an external proxy. Point `.env.techjournals` at that proxy’s base URL; the `make` targets source it automatically.

## Coding Style & Naming Conventions
- Follow the existing mix of 2-space script blocks and tab-indented markup within `.astro` files; maintain the current spacing when editing.
- Use PascalCase for components (`Navbar.astro`) and layouts, kebab-case for routes (`src/pages/homelab/index.astro`), and lowercase folders.
- Prefer module-relative imports (`../components/Navbar.astro`) and keep frontmatter code concise.
- CSS lives in `global.css` unless styles are truly component-specific; in that case, add `<style>` blocks scoped to the component.

## Testing Guidelines
- There is no automated test suite yet; rely on `npm run build` and `npm run preview` as regression checks.
- When you add interactive logic, include manual test notes in the PR and consider writing content-driven checks (e.g., screenshot diffs) before merging.

## Commit & Pull Request Guidelines
- Existing commits are short, lowercase summaries (`add arch & debian logos`, `fixes #1 and #5`). Emulate that style: imperative mood, ≤50 characters when possible, append issue references as needed.
- For PRs, provide: what changed, why, screenshots of visual updates, commands run, and linked issues. Include any manual test steps so reviewers can reproduce them quickly.
