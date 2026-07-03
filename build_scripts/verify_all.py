#!/usr/bin/env python3
"""Full sweep: visit EVERY generated page, check console errors + failed network requests."""
import json
import os
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "http://localhost:8833"

pages = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    if "build_scripts" in dirpath or "templates" in dirpath or "data" in dirpath:
        continue
    for fn in filenames:
        if fn.endswith(".html"):
            full = os.path.join(dirpath, fn)
            rel = "/" + os.path.relpath(full, ROOT)
            pages.append(rel)

pages.sort()
print(f"Total pages to check: {len(pages)}")

problems = {}

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 800})

    for path in pages:
        console_errors = []
        failed_requests = []

        def on_console(msg, ce=console_errors):
            if msg.type == "error":
                ce.append(msg.text)

        def on_response(resp, fr=failed_requests):
            if resp.status >= 400:
                fr.append(f"{resp.status} {resp.url}")

        page.on("console", on_console)
        page.on("response", on_response)

        try:
            page.goto(BASE + path, wait_until="load", timeout=20000)
            page.wait_for_timeout(300)
        except Exception as e:
            failed_requests.append(f"NAVIGATION ERROR: {e}")

        if console_errors or failed_requests:
            problems[path] = {"console_errors": console_errors, "failed_requests": failed_requests}

        page.remove_listener("console", on_console)
        page.remove_listener("response", on_response)

    browser.close()

print(f"\nPages with issues: {len(problems)} / {len(pages)}")
print(json.dumps(problems, indent=2))
