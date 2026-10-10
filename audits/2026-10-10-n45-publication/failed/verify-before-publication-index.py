#!/usr/bin/env python3
"""Read-only publication replay at the research BASE or a real descendant.

This does not call, alter, or impersonate the sealed HEAD==BASE historical main.
It checks real ancestry, complete immutable bytes, and the sealed custody
functions at their original scope. Historical execution receipts stay historical.
"""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent


def load_module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


archive=load_module('n45_publication_archive',HERE/'archive.py')


def inventory(root, relative):
    result={}
    for directory,dirs,names in os.walk(root/relative,followlinks=False):
        dirs[:]=sorted(d for d in dirs if d not in {'__pycache__','.lake'} and not (Path(directory)/d).is_symlink())
        link_dirs=[p for p in Path(directory).iterdir() if p.is_symlink() and p.is_dir()]
        for p in sorted([Path(directory)/n for n in names if not n.endswith('.pyc')]+link_dirs):
            key=p.relative_to(root).as_posix()
            if key in result:continue
            record={'mode':stat.S_IMODE(p.lstat().st_mode)}
            if p.is_symlink():record.update(kind='symlink',target=os.readlink(p))
            else:record.update(kind='regular',bytes=p.stat().st_size,sha256=archive.digest(p))
            result[key]=record
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inputs-stdin',action='store_true',help='Probe a formal input inventory without mutations')
    args=parser.parse_args()
    try:
        official=json.loads((HERE/'inputs.json').read_text())
        data=json.load(sys.stdin) if args.inputs_stdin else official
        scope=json.loads((HERE/'scope.json').read_text())
        if data['BASE']!=scope['BASE'] or data['audit_roots']!=scope['audit_roots']:
            raise ValueError('complete declared research BASE and roots mismatch')
        subprocess.run(['git','merge-base','--is-ancestor',data['BASE'],'HEAD'],cwd=ROOT,check=True,capture_output=True)
        actual={}
        for relative in data['audit_roots']:actual.update(inventory(ROOT,relative))
        if actual!=data['files']:
            raise ValueError('complete immutable inputs inventory/hash/mode/link mismatch; nested metadata is required')
        if data['current_and_historical_documents']!=official['current_and_historical_documents']:
            raise ValueError('official current document inventory binding')
        for relative,record in data['current_and_historical_documents'].items():
            path=ROOT/relative
            if path.stat().st_size!=record['bytes'] or stat.S_IMODE(path.stat().st_mode)!=record['mode'] or archive.digest(path)!=record['sha256']:
                raise ValueError('adopted document mismatch: '+relative)
        frozen=json.loads((HERE/'archive.json').read_text())
        for relative,record in frozen['files'].items():
            expected={k:v for k,v in record.items() if k!='reason'}
            if expected!=data['files'].get(relative):raise ValueError('archive/input exact binding: '+relative)
        archive.verify_files(ROOT,frozen)
        # First all complete input bytes bind this module and its exact metadata.
        parent=load_module('sealed_high23',ROOT/data['HIGH23_fulltree']/'verify.py')
        parent.verify_manifest(parent.read(parent.HERE/'manifest.json'))
        parent_files=parent.verify_trees()
        documents=parent.verify_documentation()
        historic_commands=parent.verify_actual_replays()
        parent.verify_boundaries()
        parent.verify_delivery_if_present()
        print(json.dumps({'status':'publication custody checks hold','BASE_is_real_HEAD_ancestor':True,
                          'connected_audit_roots':len(data['audit_roots']),'original_files':len(actual),
                          'HIGH23_named_original_and_frozen_files':parent_files,'HIGH23_adopted_documents':documents,
                          'historical_commands_bound':historic_commands,'new_finite_source':False,'new_Lean':False,
                          'paper_reproved':False,'whole_worktree_custody':'not claimed'},sort_keys=True))
    except (ValueError,KeyError,OSError,subprocess.CalledProcessError) as exc:
        print('REJECT: '+str(exc),file=sys.stderr);return 2
    return 0


if __name__=='__main__':sys.exit(main())
