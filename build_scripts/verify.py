#!/usr/bin/env python3
"""Verification: visit key pages headlessly, capture console errors + failed requests + screenshots."""
import json
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8833"
PAGES = [
    "/index.html",
    "/communities/index.html",
    "/communities/gozzer-ranch/index.html",
    "/communities/gozzer-ranch/real-estate/index.html",
    "/real-estate/index.html",
    "/real-estate/golf-countryside/estate-89/index.html",
    "/experiences.html",
    "/about.html",
    "/contact.html",
    "/careers.html",
    "/gallery.html",
]

results = {}

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})

    for path in PAGES:
        console_errors = []
        failed_requests = []

        def on_console(msg):
            if msg.type == "error":
                console_errors.append(msg.text)

        def on_response(resp):
            if resp.status >= 400:
                failed_requests.append(f"{resp.status} {resp.url}")

        page.on("console", on_console)
        page.on("response", on_response)

        page.goto(BASE + path, wait_until="load", timeout=30000)
        page.wait_for_timeout(1200)

        shot_name = path.strip("/").replace("/", "_").replace(".html", "") or "home"
        page.screenshot(path=f"/home/user/dlc-site/build_scripts/shots/{shot_name}.png", full_page=False)

        results[path] = {
            "console_errors": console_errors,
            "failed_requests": failed_requests,
        }

        page.remove_listener("console", on_console)
        page.remove_listener("response", on_response)

    browser.close()

print(json.dumps(results, indent=2))
