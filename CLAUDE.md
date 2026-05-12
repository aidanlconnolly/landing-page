# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A static personal landing page — two files, no build step, deploys directly to Vercel.

- `index.html` — full page, CSS inlined in `<style>`, JavaScript inline in `<script>`
- `style.css` — duplicate of the inlined styles (kept for reference; the inlined version in index.html is authoritative)

## Deploying

Push to GitHub and Vercel auto-deploys on every commit. No build command or output directory needed — set the Vercel root to `/`.

## Updating the projects list

Run `/update-landing-page` in any Claude Code chat. It reads `Website links to share.docx`, parses `Name: URL` lines, and updates the `const LIVE = [...]` array in `index.html`. Redeploy to Vercel after.

## Architecture

All logic lives in `index.html`:

- **`const LIVE`** — live project cards (name, url, icon emoji, desc). This is what `/update-landing-page` rewrites.
- **`const SOON`** — coming-soon cards (no URL). Edit these manually.
- Two `innerHTML` renders at the bottom populate `#liveGrid` and `#soonGrid`.
- Dark mode toggled via class `dark` on `<html>`, persisted in `localStorage`.

The CSS uses CSS custom properties (`--navy`, `--bg`, `--card`, etc.) so dark mode is a single class swap with no JS style manipulation.

## Source of truth for projects

`Website links to share.docx` in this folder. Format must be `Project Name: https://url` (one per line) for `/update-landing-page` to parse it correctly.
