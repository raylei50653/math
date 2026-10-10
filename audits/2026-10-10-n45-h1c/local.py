#!/usr/bin/env python3
"""Only this audit's authored top-level syntax, links, and whitespace."""
import ast
import json
from pathlib import Path
import re
from urllib.parse import urlsplit, unquote

HERE = Path(__file__).resolve().parent


def main():
    n = links = scripts = 0
    for p in sorted(HERE.iterdir()):
        if p.is_file() and p.suffix in ('.py','.json','.md'):
            text = p.read_text()
            for line_no,line in enumerate(text.splitlines(),1):
                assert line == line.rstrip() and not line.startswith('\t'), (p.name,line_no)
            if p.suffix == '.py':
                ast.parse(text,filename=str(p))
                scripts += 1
            n += 1
    for target in re.findall(r'\]\(([^\s)]+)\)',(HERE/'REPORT.md').read_text()):
        u = urlsplit(target)
        if not u.scheme:
            assert not u.fragment and (HERE/unquote(u.path)).exists(), target
            links += 1
    print(json.dumps(dict(status='PASS', authored_top_level_text_files=n,
                          Python_syntax_files=scripts, report_local_links=links,
                          copied_historical_documents='not repaired or claimed'),sort_keys=True))


if __name__ == '__main__':
    main()
