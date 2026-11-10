# Mauro Franceschelli: personal academic website

Source of **https://mauro-franceschelli.github.io**, the personal website of Mauro Franceschelli,
Associate Professor of Automatic Control at the Department of Electrical and Electronic Engineering,
University of Cagliari, Italy.

The site contains:
- biography;
- research projects;
- publications, with BibTeX, abstracts and manuscripts;
- teaching;
- research team;
- news.

## How it works

- A static site (plain HTML, CSS and JavaScript) published with GitHub Pages from the `main` branch. There is no
  build step.
- After every change run `python sync_site.py`: it refreshes the homepage news and selected publications, the
  "Last update" date and `sitemap.xml`.
- Local preview: `python -m http.server 8000`, then open http://localhost:8000
- The conventions for editing the pages are in `AGENTS.md`.

## Licence

The code (HTML, CSS, JavaScript, Python scripts) is released under the MIT licence (`LICENSE`).
The fonts in `fonts/` are under the SIL Open Font License (`fonts/OFL-*.txt`).
Journal and conference logos in `images/` belong to their respective owners.
Texts, photos and papers are © Mauro Franceschelli and co-authors.
