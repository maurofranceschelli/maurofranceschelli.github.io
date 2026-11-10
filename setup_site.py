"""One-time setup of the academic website template: run  python setup_site.py  once, after copying it.

It asks for the owner's name, the name as written in author lists, the GitHub user name (the site is
published at https://<user>.github.io/), the e-mail address and an optional GoatCounter code; then it
replaces the template placeholders in every page, redraws the favicons with the owner's initials and
synchronizes the site (sync_site.py). Everything else (photo, CV, texts, publications) is edited afterwards:
see README.md and AGENTS.md. Uses the Python standard library (Pillow, if installed, for the favicons).
"""

import json
import re
from pathlib import Path

from sync_site import sync_site

ROOT = Path(__file__).resolve().parent
PAGES = ('index.html', 'Biography.html', 'Projects.html', 'Publications.html', 'Teachings.html', 'Team.html', 'News.html', '404.html')


def ask(prompt, default=''):
    answer = input(prompt + (f' [{default}]' if default else '') + ': ').strip()
    return answer or default


def redraw_favicons(initials):
    svg = ROOT / 'favicon.svg'
    svg.write_text(re.sub(r'>[^<>]*</text>', f'>{initials}</text>', svg.read_text(encoding='utf-8')),
                   encoding='utf-8', newline='\n')
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print('  Pillow is not installed: favicon.ico and apple-touch-icon.png keep the placeholder initials.')
        return
    for size, name in ((48, 'favicon.ico'), (180, 'apple-touch-icon.png')):
        icon = Image.new('RGB', (size, size), (184, 56, 62))
        font = None
        for candidate in ('arialbd.ttf', 'Arial Bold.ttf', 'DejaVuSans-Bold.ttf', 'LiberationSans-Bold.ttf'):
            try:
                font = ImageFont.truetype(candidate, int(size * 0.47))
                break
            except OSError:
                continue
        ImageDraw.Draw(icon).text((size / 2, size / 2), initials, fill='white',
                                  font=font or ImageFont.load_default(), anchor='mm' if font else None)
        icon.save(ROOT / name)


def main():
    config = json.loads((ROOT / 'site.json').read_text(encoding='utf-8'))
    if 'username.github.io' not in config['site_url']:
        if not ask('This site seems already set up. Run the setup again? (y/n)', 'n').lower().startswith('y'):
            return
    print('Setup of the academic website. Press Enter to accept the value in brackets.')
    full = ask('Full name (e.g., Mario Rossi)')
    parts = full.split()
    if len(parts) < 2:
        print('Please write first name and surname. Exiting.')
        return
    first, last = parts[0], parts[-1]
    short = ask('Name as written in author lists', f'{first[0]}. {" ".join(parts[1:])}')
    user = ask('GitHub user name (the site will be https://<user>.github.io/)').lower()
    email = ask('E-mail address')
    goat = ask('GoatCounter code for visit statistics (blank for none; see README.md)')

    replacements = [('Name Surname', full), ('N. Surname', short), ('Surname, Name', f'{last}, {first}'),
                    ('username.github.io', f'{user}.github.io'), ('name.surname@university.edu', email),
                    ('Name-Surname', '-'.join(parts)), ('name-surname', '-'.join(parts).lower())]
    for name in PAGES + ('robots.txt', 'site.json'):
        path = ROOT / name
        text = path.read_text(encoding='utf-8')
        for old, new in replacements:
            text = text.replace(old, new)
        if name.endswith('.html'):
            if goat:
                text = text.replace('YOURCODE', goat)
            else:
                text = re.sub(r'  <!-- GoatCounter:[^\n]*\n  <script data-goatcounter=[^\n]*\n', '', text)
        path.write_text(text, encoding='utf-8', newline='\n')
    redraw_favicons((first[0] + last[0]).upper())
    sync_site()
    print(f'''
Done: {full}'s website will be published at https://{user}.github.io/
Next steps (README.md):
  1. replace images/photo.jpg (portrait, about 600x750 px) and files/CV.pdf;
  2. fill in the pages (by hand or asking your AI assistant to read AGENTS.md);
  3. run  python sync_site.py  after every change, preview with  python -m http.server 8000 ,
     then commit and push.''')


if __name__ == '__main__':
    main()
