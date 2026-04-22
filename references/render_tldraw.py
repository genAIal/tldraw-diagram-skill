#!/usr/bin/env python3
"""Render a .tldr file to PNG via a headless tldraw editor in Playwright."""

from __future__ import annotations

import base64
import json
import pathlib
import sys
from typing import Optional

from playwright.sync_api import sync_playwright


TEMPLATE = pathlib.Path(__file__).parent / "render_template.html"


def render(tldr_path_str: str, out_path_str: Optional[str] = None) -> pathlib.Path:
    tldr_path = pathlib.Path(tldr_path_str).expanduser().resolve()
    if not tldr_path.exists():
        sys.exit(f"File not found: {tldr_path}")

    tldr_json = json.loads(tldr_path.read_text(encoding="utf-8"))
    out_path = pathlib.Path(out_path_str).expanduser().resolve() if out_path_str else tldr_path.with_suffix(".png")

    if not TEMPLATE.exists():
        sys.exit(f"Template missing: {TEMPLATE}")

    template_url = f"file://{TEMPLATE}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1600, "height": 1200})
        page = context.new_page()

        errors: list[str] = []
        page.on("pageerror", lambda exc: errors.append(f"pageerror: {exc}"))
        page.on("console", lambda msg: msg.type == "error" and errors.append(f"console.error: {msg.text}"))

        page.goto(template_url, wait_until="load")
        try:
            page.wait_for_function("window.__editorReady === true", timeout=60_000)
        except Exception:
            browser.close()
            if errors:
                print("Browser errors:\n" + "\n".join(errors), file=sys.stderr)
            sys.exit("tldraw editor never became ready (check network — esm.sh must be reachable)")

        page.set_default_timeout(60_000)
        data_url = page.evaluate("(json) => window.__renderTldr(json)", tldr_json)
        browser.close()

    if not isinstance(data_url, str) or not data_url.startswith("data:image/"):
        sys.exit(f"Unexpected render result: {type(data_url).__name__}")

    _, b64 = data_url.split(",", 1)
    out_path.write_bytes(base64.b64decode(b64))
    print(f"Rendered to: {out_path}")
    return out_path


def main() -> None:
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        sys.exit("Usage: render_tldraw.py <path-to-file.tldr> [<output.png>]")
    render(sys.argv[1], sys.argv[2] if len(sys.argv) == 3 else None)


if __name__ == "__main__":
    main()
