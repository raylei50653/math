#!/usr/bin/env python3
"""Build/query the exact same-C5 conditional forcing library.

uv run --with networkx==3.5 python scripts/c5_relation_library.py build
python scripts/c5_relation_library.py query 767 --given b1=b4 --given b0!=b2
python scripts/c5_relation_library.py meet 91 935

Integers are exact ten-bit Sigma identifiers in the recorded pattern order.
Meet is colour semantics only; the build separately checks the showcased
inside/outside union's actual graph and records its planar rotation.
"""
import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path
import re

from boundary_relations import Literal, Relation, c5_universe, extra_forcings

ROOT = Path(__file__).resolve().parents[1]
FAN = ROOT / 'artifacts/fan_pentagon'
OUT = ROOT / 'artifacts/boundary_relations'


def dump(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')


def relation(bits):
    base = c5_universe()
    return Relation.of(base.ports, [p for j, p in enumerate(sorted(base.patterns)) if bits >> j & 1])


def literals(texts):
    result = []
    for text in texts:
        match = re.fullmatch(r'(b[0-4])(!=|=)(b[0-4])', text)
        if not match:
            raise ValueError(f'Expected b0=b2 or b0!=b2, got {text!r}')
        a, op, b = match.groups()
        result.append(Literal(a, b, op == '='))
    return result


def query_all(rel, guards):
    selected = rel.condition(guards)
    return dict(feasible=bool(selected.patterns), patterns=sorted(selected.patterns),
                pairs={f'{a},{b}': rel.query(a, b, guards) for a, b in combinations(rel.ports, 2)},
                geometry='not inferred from colour operations')


def build():
    import networkx as nx
    data = json.loads((FAN / 'states.json').read_text())
    summary = json.loads((FAN / 'summary.json').read_text())
    replay = json.loads((FAN / 'replay.json').read_text())
    for name, digest in replay['input_sha256'].items():
        assert hashlib.sha256((FAN / name).read_bytes()).hexdigest() == digest
    base = c5_universe()
    assert [list(p) for p in sorted(base.patterns)] == data['pattern_order']
    entries = []
    for row in data['states']:
        bits = row['sigma_bits']
        rel = relation(bits)
        entries.append(dict(id=bits, relation=rel.as_dict(), three_profile=row['three_profile'],
                            new_vs_triangle=row['new_vs_triangle'],
                            unconditional=query_all(rel, []), extra_forcings=extra_forcings(rel),
                            realization=dict(source='artifacts/fan_pentagon/states.json',
                                             mask=row['mask'], attachment_count=row['mask'].bit_count(),
                                             geometry='apex rotation replayed; C5 facial after apex deletion',
                                             sigma_evidence=('Math/FanPentagon.lean: sigma_exact (native certificate)'
                                                             if bits == 767 else 'independent full-colouring replay'))))
    # A real inside/outside example; interiors are disjoint and boundary labels identical.
    left, right = (next(r for r in data['states'] if r['sigma_bits'] == b) for b in (91, 935))
    combined = relation(91).meet(relation(935))
    assert relation(91).query('b0', 'b2')['status'] == 'free'
    assert relation(935).query('b0', 'b2')['status'] == 'free'
    assert combined.query('b0', 'b2')['status'] == 'forced_equal'
    assert combined.patterns == relation(3).patterns
    graph = nx.Graph()
    graph.add_nodes_from(range(15))
    graph.add_edges_from(left['edges'])
    graph.add_edges_from((u if u < 5 else u + 5, v if v < 5 else v + 5) for u, v in right['edges'])
    ok, rotation = nx.check_planarity(graph)
    assert ok
    rotation.check_structure()
    apex = graph.copy()
    apex.add_edges_from((15, i) for i in range(5))
    same_side = nx.check_planarity(apex)[0]
    example = dict(left=91, right=935, left_mask=left['mask'], right_mask=right['mask'],
                   combined_sigma_bits=3, relation=combined.as_dict(),
                   forced='b0=b2', left_query=relation(91).query('b0', 'b2'),
                   right_query=relation(935).query('b0', 'b2'),
                   joint_query=combined.query('b0', 'b2'),
                   graph_edges=sorted(tuple(sorted(e)) for e in graph.edges),
                   planar_rotation={str(v): list(rotation.neighbors_cw_order(v)) for v in range(15)},
                   outer_C5_cofacial=same_side,
                   geometry_status='actual union planar; each side has its own disk witness; topology not Lean proved')
    dump(OUT / 'inside_outside.json', example)
    library = dict(schema='c5-conditional-relations-v1', ports=base.ports,
                   pattern_order=sorted(base.patterns),
                   semantics='one global S4 orbit per row; ordered ports; independent interiors for meet',
                   infeasible='empty guarded relation reports infeasible, never a forced literal',
                   geometry='realization evidence is separate; meet/project do not certify a layout',
                   distinct_relations=len(entries), entries=entries,
                   source_sha256={name: hashlib.sha256((FAN / name).read_bytes()).hexdigest()
                                  for name in ('states.json', 'summary.json', 'replay.json')})
    dump(OUT / 'library.json', library)
    print(json.dumps(dict(entries=len(entries), extra_forcings=sum(len(e['extra_forcings']) for e in entries),
                          forcing_count_histogram=dict(sorted(Counter(len(e['extra_forcings']) for e in entries).items())),
                          inside_outside_same_side_possible=same_side,
                          catalog=str(OUT / 'library.json')), indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('build')
    for command in ('query', 'meet'):
        cmd = sub.add_parser(command)
        cmd.add_argument('ids', type=int, nargs='+' if command == 'meet' else 1)
        cmd.add_argument('--given', action='append', default=[])
    args = parser.parse_args()
    if args.command == 'build':
        build()
        return
    catalog = json.loads((OUT / 'library.json').read_text())
    entries = {e['id']: e['relation'] for e in catalog['entries']}
    if any(i not in entries for i in args.ids):
        parser.error('Every ID must have a witnessed entry in the library')
    def load_relation(bits):
        row = entries[bits]
        return Relation.of(row['ports'], row['patterns'])
    rel = load_relation(args.ids[0])
    for bits in args.ids[1:]:
        rel = rel.meet(load_relation(bits))
    try:
        result = query_all(rel, literals(args.given))
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
