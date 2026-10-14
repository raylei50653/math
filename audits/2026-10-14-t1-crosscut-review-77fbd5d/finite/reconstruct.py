#!/usr/bin/env python3
"""Reconstruct the essential 32 double-C6 calculations from frozen prose.

Implemented before consulting the subsequently supplied candidate output data;
this program reads neither candidate programs nor candidate certificates. The
only source-specific constants are BROWS and QUERIES, transcribed from the
frozen 77fbd5d named-edge audit. All colors are literal in one shell before
taking either C6 orbit. Unattained matrix entries remain zero and hence safe.

Usage: python3 reconstruct.py [--output-dir DIR]
The gzip certificate and summary JSON exclude elapsed time and have fixed order.
"""
import argparse
from collections import Counter
from functools import lru_cache
import gzip
from itertools import product
import json
from pathlib import Path
import time

BROWS = ('01012','01021','01023','01201','01202','01203','01212','01213','01231','01232')
QUERIES = (
    ('c15-933',(0,1,2,0,0),933),('c18-933',(0,2,1,0,0),933),
    ('c04-941',(0,0,1,0,2),941),('c07-941',(0,0,2,0,1),941),
    ('c15-941',(0,1,2,0,0),941),('c18-941',(0,2,1,0,0),941),
    ('c20-941',(1,0,0,0,2),941),('c30-941',(2,0,0,0,1),941))
SPLITS = (((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2)))


def canonical(word):
    names = {}
    return ''.join(str(names.setdefault(c,len(names))) for c in word)


ROWS = tuple(sorted({canonical(w) for w in product(range(4), repeat=6)
                     if all(w[i] != w[(i+1)%6] for i in range(6))}))
ROW_INDEX = {r:i for i,r in enumerate(ROWS)}
ALL_ROWS = (1 << len(ROWS)) - 1


def bits(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length()-1
        mask -= bit


def partitions(n):
    """Every set partition exactly once, as a restricted-growth word."""
    def extend(word, largest):
        if len(word) == n:
            yield tuple(word)
            return
        for block in range(largest+2):
            word.append(block)
            yield from extend(word,max(largest,block))
            word.pop()
    if not n:
        yield ()
    else:
        yield from extend([0],0)


def noncrossing(partition):
    """Disjoint blocks cannot contain alternating endpoints on the circle."""
    n = len(partition)
    for a in range(n):
        for b in range(a+1,n):
            if partition[a] == partition[b]:
                continue
            for c in range(b+1,n):
                if partition[c] != partition[a]:
                    continue
                for d in range(c+1,n):
                    if partition[d] == partition[b]:
                        return False
    return True


def kempe_rules():
    """Return row -> split -> full swap orbit masks of admissible partitions.

    Components with no boundary contact do not change a boundary row and need
    no block. Adjacent boundary points in the same complementary color pair
    are connected by an original boundary edge and must share a block.
    """
    candidate_partitions = [p for p in partitions(6) if noncrossing(p)]
    assert len(candidate_partitions) == 132
    rules, evidence = [], []
    for word in ROWS:
        colors = tuple(map(int,word))
        row_rules, row_evidence = [], []
        for split in SPLITS:
            pair_of = {color:j for j,pair in enumerate(split) for color in pair}
            mate = {a:b for a,b in split} | {b:a for a,b in split}
            options, records = set(), []
            for partition in candidate_partitions:
                groups = tuple(tuple(i for i,b in enumerate(partition) if b == block)
                               for block in range(max(partition)+1))
                if any(len({pair_of[colors[i]] for i in group}) > 1 for group in groups):
                    continue
                if any(pair_of[colors[i]] == pair_of[colors[(i+1)%6]]
                       and partition[i] != partition[(i+1)%6] for i in range(6)):
                    continue
                orbit = 0
                for exchange in range(1 << len(groups)):
                    changed = tuple(mate[color] if exchange & (1 << partition[i]) else color
                                    for i,color in enumerate(colors))
                    assert all(changed[i] != changed[(i+1)%6] for i in range(6))
                    orbit |= 1 << ROW_INDEX[canonical(changed)]
                assert orbit & (1 << ROW_INDEX[word])
                options.add(orbit)
                records.append([list(partition),orbit])
            assert options
            row_rules.append(tuple(sorted(options)))
            row_evidence.append(records)
        rules.append(tuple(row_rules))
        evidence.append(row_evidence)
    return tuple(rules),evidence


def make_kappa(rules):
    @lru_cache(maxsize=None)
    def kappa(support):
        """Synchronous greatest-fixed-point deletion, preserving actual disks."""
        current = support
        while True:
            keep = 0
            for row in bits(current):
                if all(any(orbit & current == orbit for orbit in alternatives)
                       for alternatives in rules[row]):
                    keep |= 1 << row
            if keep == current:
                return current
            current = keep
    return kappa


def construct(collar,pair):
    """Original named annulus, single shared x, and original two spokes."""
    B = ['b'+str(i) for i in range(5)]
    C = ['c'+str(i) for i in range(8)]
    original = ['a0']
    for i in range(1,5):
        original += ['y%d_%d'%(i,j) for j in range(1,collar[i]+1)] + ['a'+str(i)]
    original += ['y0_'+str(j) for j in range(1,collar[0]+1)]
    assert len(original) == 8 and sum(collar) == 3
    image = dict(zip(original,C))
    edges = set()
    def edge(a,b):
        assert a != b
        edges.add(tuple(sorted((a,b))))
    def cycle(vertices):
        for a,b in zip(vertices,vertices[1:]+vertices[:1]):
            edge(a,b)
    cycle(B)
    cycle(C)
    for i in range(5):
        edge(B[i],image['a'+str(i)])
        edge(B[(i+1)%5],image['a'+str(i)])
        for j in range(1,collar[i]+1):
            edge(B[i],image['y%d_%d'%(i,j)])
    edge('x',C[pair])
    edge('x',C[(pair+4)%8])
    Dplus = ['x'] + [C[(pair+j)%8] for j in range(5)]
    Dminus = ['x'] + [C[(pair+4+j)%8] for j in range(5)]
    return B+C+['x'],sorted(edges),(Dplus,Dminus),image


def colour_lifts(vertices,edges,beta):
    """All literal four-color lifts of one fixed original B row, sorted DFS."""
    index = {v:i for i,v in enumerate(vertices)}
    earlier = [[] for v in vertices]
    for a,b in edges:
        i,j = sorted((index[a],index[b]))
        earlier[j].append(i)
    colors = [-1]*len(vertices)
    colors[:5] = map(int,beta)
    assert all(colors[i] != colors[j] for j in range(5) for i in earlier[j])
    output = []
    def visit(j):
        if j == len(vertices):
            output.append(''.join(map(str,colors)))
            return
        used = {colors[i] for i in earlier[j]}
        for color in range(4):
            if color not in used:
                colors[j] = color
                visit(j+1)
        colors[j] = -1
    visit(5)
    return output


def transfer(vertices,edges,interfaces):
    index = {v:i for i,v in enumerate(vertices)}
    di = [[index[v] for v in d] for d in interfaces]
    matrix = [[0]*len(ROWS) for _ in ROWS]
    full_lifts = []
    for bi,beta in enumerate(BROWS):
        lifts = colour_lifts(vertices,edges,beta)
        full_lifts.append(lifts)
        for colors in lifts:
            q,r = [ROW_INDEX[canonical([colors[j] for j in d])] for d in di]
            matrix[q][r] |= 1 << bi
    return matrix,full_lifts


def maximal_rectangles(matrix,target):
    """All formal concepts via the complete intersection family of N(q)."""
    forbidden = ((1 << len(BROWS))-1) ^ target
    neighbors = [sum(1 << r for r,mask in enumerate(row) if not mask & forbidden)
                 for row in matrix]
    family = {ALL_ROWS}
    for n in neighbors:
        family.update(tuple(b & n for b in family))
    answer = []
    for b in sorted(family):
        a = sum(1 << q for q,n in enumerate(neighbors) if b & n == b)
        # A' = B and B' = A certify inclusion maximality, including empty sides.
        closure = ALL_ROWS
        for q in bits(a):
            closure &= neighbors[q]
        assert closure == b
        answer.append((a,b))
    return answer,neighbors


def output_mask(matrix,a,b):
    result = 0
    for q in bits(a):
        for r in bits(b):
            result |= matrix[q][r]
    return result


def dump_json(path,data):
    encoded = (json.dumps(data,sort_keys=True,separators=(',',':'))+'\n').encode()
    if path.suffix == '.gz':
        encoded = gzip.compress(encoded,compresslevel=9,mtime=0)
    with path.open('xb') as output:
        output.write(encoded)


def run(output_dir):
    started = time.monotonic()
    output_dir.mkdir(parents=True,exist_ok=True)
    assert len(ROWS) == 31
    rules,rule_evidence = kempe_rules()
    kappa = make_kappa(rules)
    cache,records,summaries = {},[],[]
    counts = Counter()
    all_possible = set()
    for query,collar,target in QUERIES:
        for pair in range(4):
            cache_key = (collar,pair)
            if cache_key not in cache:
                vertices,edges,interfaces,image = construct(collar,pair)
                matrix,full_lifts = transfer(vertices,edges,interfaces)
                cache[cache_key] = vertices,edges,interfaces,image,matrix,full_lifts
            vertices,edges,interfaces,image,matrix,full_lifts = cache[cache_key]
            rectangles,neighbors = maximal_rectangles(matrix,target)
            rows,distribution = [],Counter()
            for a,b in rectangles:
                ka,kb = kappa(a),kappa(b)
                possible = output_mask(matrix,ka,kb)
                assert possible & target == possible
                missing = target ^ possible
                assert missing & (1 << 9), (query,pair,a,b,ka,kb,possible)
                rows.append([a,b,ka,kb,possible,missing])
                distribution[possible] += 1
                all_possible.add(possible)
            name = f'CROSSCUT-{pair}-{query}'
            lift_counts = [len(x) for x in full_lifts]
            summary = dict(name=name,query=query,collar=collar,pair=pair,target=target,
                           rectangle_count=len(rows),possible_distribution=dict(distribution),
                           full_lift_counts=lift_counts,total_full_lifts=sum(lift_counts),
                           zero_transfer_pairs=sum(mask == 0 for row in matrix for mask in row),
                           missing_01232_in_every_rectangle=True)
            record = dict(summary,vertices=vertices,edges=edges,interfaces=interfaces,
                          original_to_C8=image,matrix=matrix,full_lifts=full_lifts,
                          safe_neighbors=neighbors,rectangles=rows)
            records.append(record)
            summaries.append(summary)
            counts['cases'] += 1
            counts['maximal_safe_rectangles'] += len(rows)
            counts['full_lifts_with_named_query_multiplicity'] += sum(lift_counts)
            print(name, 'rectangles',len(rows),'possible',sorted(distribution),
                  'seconds',round(time.monotonic()-started,2),flush=True)
    assert counts['cases'] == 32
    assert counts['maximal_safe_rectangles'] == 512568, dict(counts)
    assert all_possible <= {0,165,424,429},all_possible
    metadata = dict(method='independent reconstruction from frozen prose and original named collar definitions; no candidate archive imported',
                    base='77fbd5da7ba273f0af7c75175dc08376d2282f46',
                    scope='32 essential single opposite vertex double-C6 shells only',
                    B_rows=BROWS,C6_rows=ROWS,complementary_color_pairs=SPLITS)
    certificate = dict(metadata,kempe_rules=rules,kempe_partition_evidence=rule_evidence,cases=records)
    summary = dict(metadata,counts=dict(counts),possible_masks=sorted(all_possible),
                   missing_row='01232',all_cases_exclude_target=True,cases=summaries,
                   kappa_distinct_inputs=kappa.cache_info().currsize)
    dump_json(output_dir/'certificate.json.gz',certificate)
    dump_json(output_dir/'summary.json',summary)
    print(json.dumps(summary['counts'],sort_keys=True),flush=True)
    print('possible masks',sorted(all_possible),'kappa inputs',kappa.cache_info().currsize,
          'seconds',round(time.monotonic()-started,2),flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path,default=Path(__file__).resolve().parent)
    run(parser.parse_args().output_dir)
