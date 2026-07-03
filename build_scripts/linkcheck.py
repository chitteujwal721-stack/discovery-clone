#!/usr/bin/env python3
"""Walk every generated HTML file, resolve every internal href/src, and report anything missing."""
import os
import re
from urllib.parse import urljoin, urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

missing = []
checked = 0

for dirpath, dirnames, filenames in os.walk(ROOT):
    if "build_scripts" in dirpath or "templates" in dirpath or "data" in dirpath:
        continue
    for fn in filenames:
        if not fn.endswith(".html"):
            continue
        full = os.path.join(dirpath, fn)
        rel_dir = os.path.dirname(full)
        html = open(full, encoding="utf-8").read()
        for m in re.finditer(r'(?:href|src)="([^"]+)"', html):
            url = m.group(1)
            if url.startswith(("http://", "https://", "mailto:", "#", "data:")):
                continue
            checked += 1
            target = os.path.normpath(os.path.join(rel_dir, url.split("?")[0].split("#")[0]))
            if not os.path.exists(target):
                missing.append((full.replace(ROOT + "/", ""), url))

print(f"Checked {checked} internal links across all pages.")
if missing:
    print(f"\n{len(missing)} BROKEN LINKS FOUND:\n")
    for src, url in missing:
        print(f"  {src}  ->  {url}")
else:
    print("No broken internal links found.")
