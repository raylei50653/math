#!/usr/bin/env python3
"""Check newly authored text and Markdown destinations without writing files."""
import ast,importlib.util,json
from urllib.parse import unquote,urlsplit
from review import ROOT,OUT
def main():
    spec=importlib.util.spec_from_file_location('navigation',ROOT/'scripts/check_docs.py')
    nav=importlib.util.module_from_spec(spec);spec.loader.exec_module(nav)
    shared=list(json.loads((OUT/'acceptance.json').read_text())['adopted_shared_sha256'])
    files=sorted(list(OUT.glob('*.md'))+list(OUT.glob('*.py'))+
                 [ROOT/r for r in shared]+[ROOT/'docs/history/2026-10-10-n45-low2-adoption.md'])
    errors=[];links=0;python=0
    for f in files:
        text=f.read_text()
        for line,value in enumerate(text.splitlines(),1):
            if value.rstrip()!=value:errors.append(f'{f.relative_to(ROOT)}:{line}: trailing whitespace')
        if f.suffix=='.py':ast.parse(text);python+=1
        if f.suffix!='.md':continue
        for line,destination in nav.links(text):
            url=urlsplit(destination)
            if url.scheme or url.netloc:continue
            links+=1;target=(f.parent/unquote(url.path)).resolve() if url.path else f
            if not target.exists():errors.append(f'{f.relative_to(ROOT)}:{line}: missing {destination}')
            elif url.fragment and target.suffix=='.md' and unquote(url.fragment) not in nav.anchors(target.read_text()):
                errors.append(f'{f.relative_to(ROOT)}:{line}: missing anchor {destination}')
    if errors:raise SystemExit('\n'.join(errors))
    print(json.dumps({'authored_text_files':len(files),'files':[str(f.relative_to(ROOT)) for f in files],
                      'local_markdown_links':links,'Python_syntax_files':python,'whitespace_and_destinations':'hold'},sort_keys=True))
if __name__=='__main__':main()
