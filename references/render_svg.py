#!/usr/bin/env python3
"""Render a .tldr file to SVG (vector) via the same Playwright harness."""
from __future__ import annotations
import json, pathlib, sys
from playwright.sync_api import sync_playwright

TEMPLATE = pathlib.Path(__file__).parent / "render_template.html"

def render(tldr_path_str, out_path_str=None):
    tldr_path = pathlib.Path(tldr_path_str).expanduser().resolve()
    tldr_json = json.loads(tldr_path.read_text(encoding="utf-8"))
    out_path = pathlib.Path(out_path_str).expanduser().resolve() if out_path_str else tldr_path.with_suffix(".svg")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_context(viewport={"width": 1600, "height": 1200}).new_page()
        page.goto(f"file://{TEMPLATE}", wait_until="load")
        page.wait_for_function("window.__editorReady === true", timeout=60_000)
        page.set_default_timeout(60_000)
        svg = page.evaluate("(json) => window.__renderTldr(json, {format: 'svg'})", tldr_json)
        browser.close()
    if isinstance(svg, str) and svg.startswith("data:image/svg"):
        import base64
        _, b64 = svg.split(",", 1)
        out_path.write_bytes(base64.b64decode(b64))
        print(f"Rendered SVG to: {out_path}")
    else:
        sys.exit(f"Unexpected: {svg[:200] if isinstance(svg, str) else type(svg).__name__}")

if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2] if len(sys.argv) == 3 else None)
