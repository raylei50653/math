#!/usr/bin/env python3
"""Copied-certificate failures; no authority output is changed."""
import copy
import json
from independent import ROOT, load_cert, run


def remove_lift(graph):
    for row in graph['rows']:
        for cell in row['cells']:
            if cell:
                cell.pop()
                return
    raise RuntimeError('negative control needs a nonempty cell')


def false_empty(graph):
    for row in graph['rows']:
        for cell in row['cells']:
            if cell:
                cell.clear()
                return
    raise RuntimeError('negative control needs a nonempty cell')


def main():
    construction = load_cert(ROOT / 'construction/certificate.json.gz')
    contract = load_cert(ROOT / 'contract/certificate.json.gz')
    mutations = [
        ('drop-full-cap-lift', lambda c, p: remove_lift(c['representatives'][0]['capped'])),
        ('false-empty-cell', lambda c, p: false_empty(c['representatives'][0]['annulus'])),
        ('drop-catalogue-target', lambda c, p: c['representatives'].pop()),
        ('wrong-U-pin-order', lambda c, p: c['representatives'][0]['annulus']['U'].reverse()),
        ('wrong-original-edge', lambda c, p: c['representatives'][0]['annulus']['edges'].pop()),
        ('reverse-inner-face', lambda c, p: c['representatives'][0]['annulus']['faces'][-1].reverse()),
        ('drop-prism-source-lift', lambda c, p: remove_lift(p['graphs'][-1]['capped'])),
    ]
    results = []
    for name, mutate in mutations:
        c, p = copy.deepcopy(construction), copy.deepcopy(contract)
        mutate(c, p)
        try:
            run(c, p)
        except AssertionError:
            results.append({'control': name, 'rejected': True})
        else:
            raise RuntimeError('accepted corrupt certificate: ' + name)
    print(json.dumps({'status': 'PASS', 'negative_controls': results}, indent=2))


if __name__ == '__main__':
    main()
