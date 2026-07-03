#!/usr/bin/env python3
"""
Static site generator for the Ansari Sami front-end recreation.
Renders Jinja2 templates into plain .html files, one per page/community/listing.
"""
import json
import os
import re
import shutil
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES = os.path.join(ROOT, "templates")
DATA = os.path.join(ROOT, "data")
OUT = ROOT  # output directly into project root (pages/ dirs alongside assets/)

env = Environment(
    loader=FileSystemLoader(TEMPLATES),
    autoescape=select_autoescape(["html"]),
    trim_blocks=True,
    lstrip_blocks=True,
)


def slugify(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def load_json(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return json.load(f)


def write(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", path)


def render(tpl_name, root_prefix, **ctx):
    tpl = env.get_template(tpl_name)
    return tpl.render(root=root_prefix, **ctx)


def main():
    communities = load_json("communities.json")

    # Compute a single, consistent real-estate URL for every listing
    # (overrides any originally-scraped path, which used different slugs).
    for c in communities:
        if c.get("listing"):
            cat_slug = slugify(c["category"])
            listing_slug = slugify(c["listing"]["name"])
            c["listing"]["url"] = f"/real-estate/{cat_slug}/{listing_slug}"

    # Group communities by category for cross-link rails + index page
    by_category = {}
    for c in communities:
        by_category.setdefault(c["category"], []).append(c)

    # ---------------- Home page ----------------
    write(
        "index.html",
        render(
            "home.html",
            "",
            title="Discover Your World",
            description="Ansari Sami creates private residential communities and resorts in the world's most beautiful settings.",
            communities=communities,
            featured=communities[:31],
        ),
    )

    # ---------------- Communities index ----------------
    write(
        "communities/index.html",
        render(
            "communities_index.html",
            "../",
            title="Our Worlds",
            description="Browse our private residential communities and resorts around the world.",
            communities=communities,
        ),
    )

    # ---------------- Individual community pages ----------------
    for c in communities:
        related = [x for x in by_category.get(c["category"], []) if x["slug"] != c["slug"]][:20]
        write(
            f"communities/{c['slug']}/index.html",
            render(
                "community_detail.html",
                "../../",
                title=c["name"],
                description=f"{c['name']} — {c['location']}. A Ansari Sami private residential community.",
                c=c,
                related=related,
                has_sub_nav=True,
            ),
        )
        # Real-estate sub-listing page for the community (simple listings page)
        write(
            f"communities/{c['slug']}/real-estate/index.html",
            render(
                "community_real_estate.html",
                "../../../",
                title=f"{c['name']} Real Estate",
                description=f"Browse real estate listings at {c['name']}, {c['location']}.",
                c=c,
                has_sub_nav=True,
            ),
        )

    # ---------------- Real estate index ----------------
    all_listings = [dict(c["listing"], community=c["name"], category=c["category"]) for c in communities if c.get("listing")]
    write(
        "real-estate/index.html",
        render(
            "real_estate_index.html",
            "../",
            title="Real Estate",
            description="Find your bespoke residence in one of our communities.",
            listings=all_listings,
            by_category=by_category,
        ),
    )

    # ---------------- Sample real-estate detail page ----------------
    for c in communities:
        if not c.get("listing"):
            continue
        l = c["listing"]
        slug = slugify(l["name"])
        cat_slug = slugify(c["category"])
        write(
            f"real-estate/{cat_slug}/{slug}/index.html",
            render(
                "listing_detail.html",
                "../../../",
                title=l["name"],
                description=f"{l['name']} — {l['location']}",
                c=c,
                l=l,
            ),
        )

    # ---------------- Static pages ----------------
    write("experiences.html", render("experiences.html", "", title="Experiences", description="Exclusive experiences at Ansari Sami communities."))
    write("about.html", render("about.html", "", title="About", description="About Ansari Sami."))
    write("contact.html", render("contact.html", "", title="Contact", description="Contact Ansari Sami."))
    write("careers.html", render("careers.html", "", title="Careers", description="Careers at Ansari Sami."))
    write("gallery.html", render("gallery.html", "", title="Gallery", description="Photo gallery of Ansari Sami communities.", communities=communities))

    print(f"\nDone. Generated {len(communities)} community pages + {len(all_listings)} listing pages + static pages.")


if __name__ == "__main__":
    main()
