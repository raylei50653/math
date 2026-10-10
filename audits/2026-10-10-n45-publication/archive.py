#!/usr/bin/env python3
"""Restore or verify byte-exact N45 payload, with bounded gzip parts and symlinks.

All original paths remain intact. The publication index records each original
SHA256, size and mode, deduplicated compressed bytes, and literal link targets.
Existing legacy archive blobs are reused by their verified metadata.
"""
import argparse
from contextlib import contextmanager
import gzip
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1<<20),b''):h.update(block)
    return h.hexdigest()


def safe(root, relative):
    parts=PurePosixPath(relative)
    if parts.is_absolute() or '..' in parts.parts or not parts.parts:
        raise ValueError('unsafe archive path: '+relative)
    path=root/relative
    if not path.parent.resolve().is_relative_to(root.resolve()):
        raise ValueError('archive parent escapes destination: '+relative)
    return path


class PartsReader(io.RawIOBase):
    def __init__(self, paths):
        super().__init__();self.paths=iter(paths);self.current=None

    def readable(self):
        return True

    def readinto(self, buffer):
        while True:
            if self.current is None:
                try:self.current=next(self.paths).open('rb')
                except StopIteration:return 0
            count=self.current.readinto(buffer)
            if count:return count
            self.current.close();self.current=None

    def close(self):
        if self.current is not None:self.current.close()
        super().close()


@contextmanager
def uncompressed(root, record):
    paths=[safe(root,p['path']) for p in record['parts']]
    with PartsReader(paths) as raw, io.BufferedReader(raw) as stream:
        with gzip.GzipFile(fileobj=stream,mode='rb') as incoming:yield incoming


def check_blobs(root, data):
    for sha, record in data['blobs'].items():
        combined=hashlib.sha256();size=0
        for part in record['parts']:
            path=safe(root,part['path'])
            if path.stat().st_size!=part['bytes'] or digest(path)!=part['sha256']:
                raise ValueError('compressed part mismatch: '+part['path'])
            with path.open('rb') as f:
                for block in iter(lambda:f.read(1<<20),b''):combined.update(block);size+=len(block)
        if combined.hexdigest()!=record['compressed_sha256'] or size!=record['compressed_bytes']:
            raise ValueError('combined gzip mismatch: '+sha)
        plain=hashlib.sha256();plain_size=0
        with uncompressed(root,record) as f:
            for block in iter(lambda:f.read(1<<20),b''):plain.update(block);plain_size+=len(block)
        if plain.hexdigest()!=sha or plain_size!=record['raw_bytes']:
            raise ValueError('uncompressed blob mismatch: '+sha)


def verify_files(destination, data):
    for relative, record in data['files'].items():
        path=safe(destination,relative)
        if record['kind']=='symlink':
            if not path.is_symlink() or os.readlink(path)!=record['target']:
                raise ValueError('literal symlink mismatch: '+relative)
        else:
            if path.is_symlink() or not path.is_file() or path.stat().st_size!=record['bytes'] or digest(path)!=record['sha256'] or stat.S_IMODE(path.stat().st_mode)!=record['mode']:
                raise ValueError('original bytes/mode mismatch: '+relative)


def restore(root, destination, data):
    # Validate all compressed bytes before writing any original path.
    check_blobs(root,data)
    for relative, record in data['files'].items():
        path=safe(destination,relative)
        if os.path.lexists(path):
            verify_files(destination,{'files':{relative:record}})
            continue
        path.parent.mkdir(parents=True,exist_ok=True)
        if record['kind']=='symlink':
            target=(path.parent/record['target']).resolve()
            if not target.is_relative_to(destination.resolve()):raise ValueError('symlink target escapes destination: '+relative)
            path.symlink_to(record['target'])
            continue
        fd,temp=tempfile.mkstemp(prefix='.n45-restore-',dir=path.parent)
        temporary=Path(temp)
        try:
            with os.fdopen(fd,'wb') as outgoing,uncompressed(root,data['blobs'][record['sha256']]) as incoming:
                shutil.copyfileobj(incoming,outgoing,1<<20)
            if temporary.stat().st_size!=record['bytes'] or digest(temporary)!=record['sha256']:
                raise ValueError('restored content mismatch: '+relative)
            temporary.chmod(record['mode']);os.replace(temporary,path)
        finally:temporary.unlink(missing_ok=True)
    verify_files(destination,data)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['restore','verify'])
    parser.add_argument('--destination',type=Path,default=ROOT)
    args=parser.parse_args()
    data=json.loads((HERE/'archive.json').read_text())
    if args.action=='restore':restore(ROOT,args.destination.resolve(),data)
    else:check_blobs(ROOT,data);verify_files(args.destination.resolve(),data)
    print(json.dumps({'action':args.action,'files':len(data['files']),'unique_blobs':len(data['blobs']),'all_checks_passed':True},sort_keys=True))


if __name__=='__main__':main()
