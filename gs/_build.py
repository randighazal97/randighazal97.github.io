"""Build Google Sites 'Embed code' snippets from the GitHub Pages portfolio."""
import re, sys, os, pathlib

SRC = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(sys.argv[2]); OUT.mkdir(exist_ok=True)
GH = "https://randighazal97.github.io/"
GS = sys.argv[3].rstrip("/") + "/"   # e.g. https://sites.google.com/view/randighazal-portfolio/
PAGES = {"index.html": "home", "fyp.html": "final-year-project", "internship.html": "internship",
         "projects.html": "projects", "highlights.html": "highlights"}

css = (SRC / "style.css").read_text(encoding="utf8")
css += """
body{background:#fff;margin:0}
main{padding:0 16px 24px}
.hero{padding:16px 0 28px;margin-bottom:28px}
"""

for f, slug in PAGES.items():
    html = (SRC / f).read_text(encoding="utf8")
    main = re.search(r"<main>(.*)</main>", html, re.S).group(1)
    extra_style = re.search(r"<style>(.*?)</style>", html, re.S)
    main = main.replace('src="assets/', f'src="{GH}assets/').replace('href="assets/', f'href="{GH}assets/')
    def link(m):
        page, anchor = m.group(1), m.group(2) or ""
        return f'href="{GS}{PAGES[page]}{anchor}" target="_top"'
    main = re.sub(r'href="((?:index|fyp|internship|projects|highlights)\.html)(#[\w-]+)?"', link, main)
    main = re.sub(r'href="(#[\w-]+)"', r'href="\1" target="_self"', main)
    main = re.sub(r'href="(https?://(?!sites\.google)[^"]+)"(?! target)', r'href="\1" target="_blank" rel="noopener"', main)
    snippet = ("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
               "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
               f"<style>{css}{extra_style.group(1) if extra_style else ''}</style></head>"
               f"<body><main>{main}</main></body></html>")
    snippet = re.sub(r"\n\s*", "\n", snippet)
    (OUT / f"{slug}.html").write_text(snippet, encoding="utf8")
    print(slug, len(snippet))
