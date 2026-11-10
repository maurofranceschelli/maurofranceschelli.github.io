"""Render the first page of each homepage paper as its thumbnail (requires PyMuPDF: pip install pymupdf).

Run from any directory: python generate_paper_previews.py
For each label in "selected" of site.json, the thumbnail images/selected/<label>.png is rendered from
files/published/<LABEL>.pdf if present (e.g. the open-access publisher version), otherwise from the
paper's "Manuscript" link in Publications.html. Publisher PDFs may be shown only if their licence allows
it (e.g. CC BY): add the attribution in the homepage credits. Then the homepage is synchronized.
"""

import html
import json
import re
from pathlib import Path
from urllib.parse import unquote

import fitz
from sync_site import sync_site

ROOT = Path(__file__).resolve().parent


def main():
    selected = json.loads((ROOT / 'site.json').read_text(encoding='utf-8')).get('selected', [])
    publications = (ROOT / 'Publications.html').read_text(encoding='utf-8')
    output = ROOT / 'images' / 'selected'
    output.mkdir(parents=True, exist_ok=True)
    for label in selected:
        source = ROOT / 'files' / 'published' / f'{label}.pdf'
        if not source.exists():
            entry = re.search(r'<article\b[^>]*id="section-' + re.escape(label) + r'".*?</article>', publications, re.S)
            link = entry and re.search(r'<a\b[^>]*href="([^"]+)"[^>]*>Manuscript</a>', entry.group(0))
            if not link:
                print(f'{label}: no Manuscript link and no files/published/{label}.pdf, skipped')
                continue
            source = ROOT / unquote(html.unescape(link.group(1)))
        with fitz.open(source) as document:
            page = document[0]
            scale = 440 / page.rect.width
            pixmap = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
            target = output / f'{label.lower()}.png'
            pixmap.save(target)
            print(f'{target.relative_to(ROOT)}: {pixmap.width} x {pixmap.height} from {source.relative_to(ROOT)}')
    sync_site()


if __name__ == '__main__':
    main()
