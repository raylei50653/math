#!/usr/bin/env python3
"""Extend the existing navigation check to the standalone D2 Markdown package."""
import argparse
import importlib.util
from pathlib import Path
from urllib.parse import unquote, urlsplit


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,required=True)
    args=parser.parse_args()
    root=args.repo.resolve()
    spec=importlib.util.spec_from_file_location('navigation',root/'scripts/check_docs.py')
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    files=sorted((root/'audits/2026-10-04-task-d2').rglob('*.md'))
    errors=[];count=0
    for source in files:
        for line,destination in module.links(source.read_text()):
            url=urlsplit(destination)
            if url.scheme or url.netloc: continue
            count+=1
            target=(source.parent/unquote(url.path)).resolve() if url.path else source
            if not target.exists():
                errors.append(f'{source.relative_to(root)}:{line}: missing {destination}')
            elif url.fragment and target.suffix=='.md' and unquote(url.fragment) not in module.anchors(target.read_text()):
                errors.append(f'{source.relative_to(root)}:{line}: missing anchor {destination}')
    for error in errors: print(error)
    print(f'{"FAIL" if errors else "OK"}: {len(files)} D2 Markdown files, {count} local links, {len(errors)} errors')
    assert not errors


if __name__=='__main__': main()
