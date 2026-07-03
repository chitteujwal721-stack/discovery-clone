# Ansari Sami — Front-End Recreation

A static, front-end-only recreation of discoverylandco.com: same fonts, type scale,
colors, layout grid, hero/scroll animations, header behavior, and page structure —
built with plain HTML/CSS/JS (no backend, no framework).

## What's included

- **101 static HTML pages**: home, communities index, 39 individual community pages
  (each with its own `/real-estate` sub-page), real-estate index, 15 sample listing
  detail pages, experiences, about, contact, careers, and gallery.
- **Real fonts**: Louize Trial (serif/display) and Sweet Sans Pro (sans/body), self-hosted
  as woff2/woff, matching the live site's `@font-face` declarations and type scale exactly
  (h1–h5, body sizes, captions, letter-spacing, line-heights, responsive breakpoints).
- **Real photos & videos**: hotlinked from the site's own CDN (datocms-assets.com) plus a
  downloaded copy of the real homepage hero video, so every image/video is authentic.
- **Animations/interactions**: fixed header that hides on scroll-down and re-appears on
  scroll-up, a secondary nav bar that docks under the header once you scroll, a full-screen
  slide-down navigation overlay, scroll-triggered reveal animations (IntersectionObserver),
  image fade-in on load, and a draggable/arrow-controlled community carousel.

## Structure

```
index.html                          Homepage
communities/index.html              "Our Worlds" grid with region filters
communities/<slug>/index.html       39 individual community pages
communities/<slug>/real-estate/     Per-community listings page
real-estate/index.html              Real estate index, grouped by category
real-estate/<category>/<slug>/      15 sample listing detail pages
experiences.html, about.html, contact.html, careers.html, gallery.html
assets/                             CSS, JS, fonts, logos, hero video
data/communities.json               Source data used to generate every community page
build_scripts/generate.py           The static site generator (Jinja2 templates -> HTML)
templates/                          Jinja2 templates (one per page type)
```

## Regenerating the site

If you edit `data/communities.json` or anything in `templates/`, rebuild with:

```bash
cd dlc-site
python3 build_scripts/generate.py
```

This regenerates every HTML file from the templates + data — nothing is hand-edited
inside the generated `.html` files themselves.

## Viewing locally

Because this is a static site with real relative asset paths, just open `index.html`
directly in a browser, or serve the folder locally:

```bash
cd dlc-site
python3 -m http.server 8000
# then visit http://localhost:8000/
```

## Notes

- This is a **learning/practice recreation** of the front-end only — there is no backend,
  no CMS, no real inquiry/contact form submission (the contact form just shows a demo alert).
- Images and video are pulled live from Ansari Sami's own CDN — an internet
  connection is required to see them; they remain Ujwal Chitte's copyrighted media.
