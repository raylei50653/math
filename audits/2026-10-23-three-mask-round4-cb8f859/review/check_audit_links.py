#!/usr/bin/env python3
"""Check new audit prose without treating frozen source excerpts as new prose."""
from pathlib import Path
import sys
from urllib.parse import unquote, urlsplit

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO))
from scripts.check_docs import anchors, links


def main():
    files = [p for p in AUDIT.rglob('*.md')
             if not {'frozen', 'entry-snapshot', 'routing-entry', 'runs'} & set(p.relative_to(AUDIT).parts)]
    errors = []
    count = 0
    for source in files:
        for line, destination in links(source.read_text()):
            url = urlsplit(destination)
            if url.scheme or url.netloc:
                continue
            count += 1
            target = (source.parent / unquote(url.path)).resolve() if url.path else source
            label = f'{source.relative_to(AUDIT)}:{line}: {destination}'
            if not target.exists():
                errors.append('missing path: ' + label)
            elif url.fragment and target.suffix == '.md' and unquote(url.fragment) not in anchors(target.read_text()):
                errors.append('missing anchor: ' + label)
    if errors:
        print('\n'.join(errors))
        return 1
    print(f'OK: {len(files)} new audit Markdown files, {count} local links')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
