# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A static personal landing page — no build step, deploys directly to Vercel.

- `index.html` — the whole site: CSS inlined in `<style>`, JavaScript inline in `<script>`. This is the authoritative file.
- `style.css` — an older duplicate of some styles, kept only for reference. **Out of date** vs. the inlined version; do not rely on it.
- `thumbs/` — committed screenshot thumbnails for each project card (`<slug>.jpg`, ~50–100KB) plus `capture.py` (generates them).
- `favicon.svg`, `.gitignore`.

## Deploying

Push to GitHub and Vercel auto-deploys on every commit. No build command or output directory needed — set the Vercel root to `/`. Repo: https://github.com/aidanlconnolly/landing-page

## Updating the projects list

Run `/update-landing-page` in any Claude Code chat. It reads `Website links to share.docx`, parses `Project Name: URL` lines, updates the `const LIVE = [...]` array in `index.html`, and **auto-captures a thumbnail** for each added/changed project (via `thumbs/capture.py`, adding the entry to the `THUMBS` map). Push to redeploy.

## Architecture

All logic lives in `index.html`. Key data structures and renders:

- **`const LIVE`** — project cards, each `{ name, category, url, icon, desc }` (or `modal` instead of `url` for the Chrome-extensions card). `category` is one of: `startup_full`, `prof`, `games`, `finance`, `sports`, `startup`, `learning`, `personal`. This is what `/update-landing-page` rewrites.
- **`const SOON`** — coming-soon cards (no URL), currently empty. Edit manually.
- **`const THUMBS`** — maps each project `url` → `thumbs/<slug>.jpg`. Cards fall back to the emoji icon when a URL has no entry. See [thumbnail pipeline in memory] / `thumbs/capture.py`.
- **`const CAT_META`** — per-category accent color + pill label. **`SECTIONS`** lists the eight category grids; a loop renders `LIVE`/`SOON` into each `#<id>Grid` and sets the section's `--accent`.
- **`FLAGSHIP`** — currently an empty `Set` (flagship tiles were removed; every card is equal-sized).

### Visual / interaction features (all vanilla JS + CSS, no libraries)

- **Dark only.** `<html class="dark">` is hard-set; there is no light mode or toggle. CSS custom properties (`--navy`, `--bg`, `--card`, …) still drive theming.
- **Space header** — transparent background so the global constellation shows through (no separate block); three CSS `.planet`s that fade + parallax on scroll; gradient/shimmer wordmark; spinning conic-gradient avatar ring; typewriter `.rotator` tagline.
- **Constellation** — a fixed full-page `<canvas>` of drifting, cursor-reactive nodes behind everything (`#constellation`, z-index 0). `main` is transparent so it shows through the gutters.
- **Toolbar** — sticky filter pills (by category) + live search + 🎲 Surprise me + ⌘K hint.
- **Command palette** — `#cmdk`, opened with ⌘K / Ctrl+K, fuzzy-jumps to any project (arrow/enter nav).
- **Cards** — per-category accent, cursor-following spotlight glow, staggered scroll-reveal via `IntersectionObserver`.

Scroll-driven effects (hero parallax, planet fade) and all CSS animations respect `prefers-reduced-motion`.

## Source of truth for projects

`Website links to share.docx` in this folder. Format must be `Project Name: https://url` (one per line) for `/update-landing-page` to parse it correctly.
