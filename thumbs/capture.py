#!/usr/bin/env python3
"""Capture a thumbnail for a landing-page project card.

Usage:
    python3 thumbs/capture.py "Project Name" "https://project-url/"

Captures a screenshot via the microlink free API, downscales it to an
800px-wide JPEG, and writes it to thumbs/<slug>.jpg. On success it prints
the line to add to the `const THUMBS = { ... }` map in index.html:

    'https://project-url/': 'thumbs/<slug>.jpg',

Exit code 0 = thumbnail written, 1 = failed (card falls back to emoji).
"""
import os, re, sys, subprocess, tempfile, urllib.request, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))


def slug(name):
    return re.sub(r'(^-|-$)', '', re.sub(r'[^a-z0-9]+', '-', name.lower()))


def capture(name, url):
    s = slug(name)
    out = os.path.join(HERE, f'{s}.jpg')
    api = "https://api.microlink.io/?" + urllib.parse.urlencode({
        'url': url, 'screenshot': 'true', 'meta': 'false',
        'embed': 'screenshot.url',
        'viewport.width': '1280', 'viewport.height': '800',
        'waitUntil': 'networkidle2',
    })
    req = urllib.request.Request(api, headers={'User-Agent': 'Mozilla/5.0'})
    data = urllib.request.urlopen(req, timeout=45).read()
    if data[:8] != b'\x89PNG\r\n\x1a\n' or len(data) < 2000:
        raise RuntimeError(f'no valid screenshot returned ({len(data)} bytes)')
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
        f.write(data); png = f.name
    try:
        subprocess.run(['sips', '-Z', '800', '-s', 'format', 'jpeg',
                        '-s', 'formatOptions', '78', png, '--out', out],
                       check=True, capture_output=True)
    finally:
        os.unlink(png)
    return s, out


def main():
    if len(sys.argv) != 3:
        print(__doc__); sys.exit(2)
    name, url = sys.argv[1], sys.argv[2].strip()
    try:
        s, out = capture(name, url)
        kb = os.path.getsize(out) // 1024
        print(f"  '{url}': 'thumbs/{s}.jpg',")
        print(f"# wrote thumbs/{s}.jpg ({kb}KB)", file=sys.stderr)
    except Exception as e:
        print(f"# FAILED to capture {name}: {e} — card will use emoji fallback", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
