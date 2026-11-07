#!/usr/bin/env python3
"""Builds the multi-page static site from src/site.html (the single-file source).
Run: python3 build.py   (set SITE below to the live domain, e.g. https://example.org)"""
import re, os, sys, hashlib

SITE = "https://jasmineinitiative.org"  # e.g. "https://jasmineinitiative.org" -- needed for absolute share-preview URLs
ROOT = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(ROOT, "src/site.html"), encoding="utf-8").read()

def between(a, b, s=src):
    i = s.index(a); j = s.index(b, i)
    return s[i + len(a):j]

css = between("<style>\n", "</style>")
sprite = src[src.index('<svg width="0"'):src.index('<a class="skip"')]
header = src[src.index('<header class="bar">'):src.index('<div id="content">')]
footer = src[src.index('<footer class="foot">'):src.index('<script>')]
script = between("<script>\n", "</script>")
fonts = re.search(r'<link rel="preconnect".*?rel="stylesheet">', src, re.S).group(0)

# --- script: drop hash router, guard optional elements
script = script[:script.index("  var VIEWS =")]
script = script.replace('''  var ct = document.getElementById("colorToggle");
  ct.addEventListener("click", function(){''', '''  var ct = document.getElementById("colorToggle");
  if (ct) ct.addEventListener("click", function(){''')
script += '''  var btn = document.getElementById("menuBtn"), menu = document.getElementById("menu");
  function setMenu(open){
    menu.hidden = !open;
    btn.setAttribute("aria-expanded", String(open));
    btn.textContent = open ? "Close" : "Menu";
    document.body.classList.toggle("menu-open", open);
  }
  btn.addEventListener("click", function(){ setMenu(menu.hidden); });
  document.addEventListener("keydown", function(e){ if (e.key === "Escape") setMenu(false); });
'''

VER = hashlib.md5((css + script).encode("utf-8")).hexdigest()[:8]  # cache-buster so edits show up right away

PAGES = [
  # key, folder, title, description, dark, nav label
  ("home", "", "Jasmine Initiative | Follow the story. Change the ending.",
   "Humanitarian work you can watch from start to finish, with every dollar tracked. A 501(c)(3) public charity.", False),
  ("initiative-one", "initiative-001", "Initiative 001: Clean water, documented | Jasmine Initiative",
   "Our first initiative puts clean water access in Pakistan, on camera and tracked to the dollar.", True),
  ("initiative-two", "initiative-002", "Initiative 002 | Jasmine Initiative",
   "Initiative 002: already started. More soon.", True),
  ("initiative-three", "initiative-003", "Initiative 003 | Jasmine Initiative",
   "Initiative 003 is in its final stages before we begin. More soon.", True),
  ("about", "about", "About | Jasmine Initiative",
   "Jasmine Initiative funds humanitarian projects and shows every step on camera, from the first dollar to the finished work.", False),
  ("donate", "donate", "Donate | Jasmine Initiative",
   "Fund the work. Jasmine Initiative Inc is a 501(c)(3) public charity.", False),
  ("contact", "contact", "Contact | Jasmine Initiative",
   "Questions, press, partnerships, or a note about a gift. Contact Jasmine Initiative.", False),
]
HREF = {"home": "", "initiative-one": "initiative-001/", "initiative-two": "initiative-002/",
        "initiative-three": "initiative-003/", "about": "about/", "donate": "donate/", "contact": "contact/"}
FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'%3E%3Crect width='40' height='40' fill='%230A0A0A'/%3E"
           "%3Cg fill='%23E02020'%3E%3Cellipse cx='20' cy='10' rx='4' ry='8'/%3E%3Cellipse cx='20' cy='10' rx='4' ry='8' transform='rotate(45 20 20)'/%3E"
           "%3Cellipse cx='20' cy='10' rx='4' ry='8' transform='rotate(90 20 20)'/%3E%3Cellipse cx='20' cy='10' rx='4' ry='8' transform='rotate(135 20 20)'/%3E"
           "%3Cellipse cx='20' cy='10' rx='4' ry='8' transform='rotate(180 20 20)'/%3E%3Cellipse cx='20' cy='10' rx='4' ry='8' transform='rotate(225 20 20)'/%3E"
           "%3Cellipse cx='20' cy='10' rx='4' ry='8' transform='rotate(270 20 20)'/%3E%3Cellipse cx='20' cy='10' rx='4' ry='8' transform='rotate(315 20 20)'/%3E%3C/g%3E"
           "%3Ccircle cx='20' cy='20' r='5' fill='%230A0A0A'/%3E%3Ccircle cx='20' cy='20' r='3' fill='%23E02020'/%3E%3C/svg%3E")

def fix_links(html, prefix, current=None, absolute=False):
    def sub(m):
        key = m.group(1)
        base = "/" if absolute else (prefix or "./")
        return 'href="%s"' % (base + HREF[key] if absolute else (prefix + HREF[key] or "./"))
    html = re.sub(r'href="#(home|initiative-one|initiative-two|initiative-three|about|donate|contact)"', sub, html)
    if current:
        target = ("/" if absolute else (prefix or "./")) if current == "home" else None
        want = (prefix + HREF[current]) or "./"
        html = re.sub(r'(<a [^>]*?href="%s"(?![^>]*class="btn"))' % re.escape(want),
                      lambda m: m.group(1) + ' aria-current="page"', html)
    return html

def head(title, desc, prefix, path, dark_img=None, absolute=False):
    a = "/" if absolute else prefix
    url = (SITE + "/" + path + ("/" if path and not path.endswith(".html") else "")) if SITE else ""
    og = ['<meta property="og:site_name" content="Jasmine Initiative">',
          '<meta property="og:type" content="website">',
          '<meta property="og:title" content="%s">' % title,
          '<meta property="og:description" content="%s">' % desc,
          '<meta name="twitter:card" content="summary_large_image">']
    if SITE:
        og.append('<meta property="og:url" content="%s">' % url)
        og.append('<meta property="og:image" content="%s/img/share.jpg">' % SITE)
        og.append('<link rel="canonical" href="%s">' % url)
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '<title>%s</title>\n<meta name="description" content="%s">\n<meta name="theme-color" content="#0A0A0A">\n%s\n'
            '<link rel="icon" href="%s">\n%s\n<link rel="stylesheet" href="%sassets/site.css?v=%s">\n</head>\n') % (
            title, desc, "\n".join(og), FAVICON, fonts, a, VER)

def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full) or ROOT, exist_ok=True)
    open(full, "w", encoding="utf-8").write(text)

write("assets/site.css", css)
write("assets/site.js", script)

for key, folder, title, desc, dark in PAGES:
    prefix = "../" if folder else ""
    main = between('<main id="view-%s" data-view="%s"' % (key, key), "</main>")
    main = main[main.index(">") + 1:]  # drop rest of opening-tag attrs (hidden)
    main = '<main id="main">' + main + "</main>"
    main = main.replace('src="img/', 'src="%simg/' % prefix)
    body = (sprite + '<a class="skip" href="#main">Skip to content</a>\n' + header + "\n" + main + "\n" + footer +
            '<script src="%sassets/site.js?v=%s"></script>\n' % (prefix, VER))
    body = fix_links(body, prefix, current=key)
    hd = head(title, desc, prefix, folder)
    if key == "donate":
        hd = hd.replace('</head>', '<link rel="preconnect" href="https://donorbox.org" crossorigin>\n<link rel="dns-prefetch" href="https://donorbox.org">\n</head>')
    page = hd + '<body%s>\n%s</body>\n</html>\n' % (' class="dark"' if dark else "", body)
    write((folder + "/" if folder else "") + "index.html", page)

# 404 (served from any path, so root-absolute URLs)
nf_main = ('<main id="main"><section class="sec" style="border-top:0"><div class="wrap">'
           '<p class="eyebrow">404</p><h1 class="h1">Page not <em>found.</em></h1>'
           '<p class="lede">That page doesn\'t exist, or it moved.</p>'
           '<div class="cta"><a class="btn" href="/">Back to home</a></div></div></section></main>\n')
body = sprite + '<a class="skip" href="#main">Skip to content</a>\n' + header + "\n" + nf_main + footer + '<script src="/assets/site.js?v=' + VER + '"></script>\n'
body = fix_links(body, "", absolute=True)
h = head("Page not found | Jasmine Initiative", "Page not found.", "", "404.html", absolute=True)
h = h.replace('<meta name="description"', '<meta name="robots" content="noindex">\n<meta name="description"')
write("404.html", h + "<body>\n" + body + "</body>\n</html>\n")

write("robots.txt", "User-agent: *\nAllow: /\n" + ("Sitemap: %s/sitemap.xml\n" % SITE if SITE else ""))
if SITE:
    urls = "".join("  <url><loc>%s/%s</loc></url>\n" % (SITE, f) for _, f, *_ in PAGES for f in [f + "/" if f else ""])
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")
write(".nojekyll", "")
print("built", len(PAGES) + 1, "pages")
