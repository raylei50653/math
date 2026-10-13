#!/usr/bin/env python3
"""Independent C9/932 h=4 identity and degree-three support checker.

No producer imports.  Rebuilds rows by literal enumeration and Kempe choices
by all Bell partitions followed by crossing rejection.  Checks every joint
D5 transport, including complete literal annulus fibres and their empties.
"""
import argparse
from collections import Counter
import copy
from functools import lru_cache
import gzip
import hashlib
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FROZEN = ROOT / 'frozen/audits/2026-10-13-c5-no4ct-frontier-6943561'


def normal(word):
    names = {}
    for c in word:
        names.setdefault(c, len(names))
    return tuple(names[c] for c in word)


def words(n):
    return sorted({normal((0,) + tail) for tail in product(range(4), repeat=n-1)
                   if all(a != b for a, b in zip((0,) + tail, tail + (0,)))})


def bitmask(indices):
    result = 0
    for i in indices:
        result |= 1 << i
    return result


def partitions(n):
    def grow(prefix):
        if len(prefix) == n:
            yield tuple(prefix)
            return
        for value in range(max(prefix)+2):
            yield from grow(prefix + [value])
    return list(grow([0]))


def kempe_table(rows):
    every = partitions(9)
    assert len(every) == 21147
    quadruples = list(combinations(range(9), 4))
    nc = [p for p in every if not any(p[a] == p[c] and p[b] == p[d]
                                     and p[a] != p[b] for a,b,c,d in quadruples)]
    assert len(nc) == 4862
    cycles = [(i, (i+1)%9) for i in range(9)]
    packed = [(p, [tuple(i for i in range(9) if p[i] == c)
                   for c in range(max(p)+1)]) for p in nc]

    @lru_cache(None)
    def allowed(side):
        return [blocks for p,blocks in packed
                if all(side[a] != side[b] or p[a] == p[b] for a,b in cycles)
                and all(len({side[i] for i in block}) == 1 for block in blocks)]

    row_index = {p:i for i,p in enumerate(rows)}
    table = []
    for row in rows:
        entry = []
        for mate in ((1,0,3,2), (2,3,0,1), (3,2,1,0)):
            side = tuple(int(c not in (0,mate[0])) for c in row)
            orbits = set()
            for blocks in allowed(side):
                orbit = set()
                for flips in product((False,True), repeat=len(blocks)):
                    changed = list(row)
                    for flip,block in zip(flips,blocks):
                        if flip:
                            for vertex in block:
                                changed[vertex] = mate[changed[vertex]]
                    orbit.add(row_index[normal(changed)])
                orbits.add(bitmask(orbit))
            assert orbits
            entry.append(sorted(orbits))
        table.append(entry)
    return table


def vertex_map(extras, sign, shift):
    mapping = {}
    for i in range(5):
        j = (sign*i+shift)%5
        mapping[f'b{i}'] = f'b{j}'
        mapping[f'a{i}'] = f'a{j if sign == 1 else (j-1)%5}'
        for t in range(1,extras[i]+1):
            mapping[f'y{i}_{t}'] = f'y{j}_{t if sign == 1 else extras[i]+1-t}'
    return mapping


def oriented(face):
    face = tuple(face)
    return min(face[i:]+face[:i] for i in range(len(face)))


def geometry_group(e):
    if e.count(2) == 2:
        return '22-nonadjacent'
    center = next(i for i in range(5) if e[i] and e[(i-1)%5] and e[(i+1)%5])
    return '121-center-two' if e[center] == 2 else '211-end-two'


def check_transports(payload, residuals, rows, outer):
    cases = {c['id']:c for c in payload['cases']}
    by_extras = {tuple(q['extras']):q for q in residuals}
    ri = {p:i for i,p in enumerate(rows)}
    oi = {p:i for i,p in enumerate(outer)}
    ledger = []
    for q in residuals:
        c = cases[q['case_id']]
        e = q['extras']
        actions = []
        for sign,shift in product((1,-1), range(5)):
            destination = [None]*5
            for i in range(5):
                destination[(sign*i+shift)%5] = e[i]
            dq = by_extras[tuple(destination)]
            dc = cases[dq['case_id']]
            vm = vertex_map(e,sign,shift)
            assert {tuple(sorted(vm[v] for v in edge)) for edge in c['annulus_edges']} == {
                tuple(sorted(edge)) for edge in dc['annulus_edges']}
            assert {oriented([vm[v] for v in face][::sign]) for face in c['annulus_faces']} == {
                oriented(face) for face in dc['annulus_faces']}
            for v,path in c['annulus_rotation_paths'].items():
                assert [vm[x] for x in path][::sign] == dc['annulus_rotation_paths'][vm[v]]
            cp = [dc['boundary_order'].index(vm[v]) for v in c['boundary_order']]
            bp = [(sign*i+shift)%5 for i in range(5)]
            row_action, outer_action = [], []
            for p in outer:
                raw = [None]*5
                for i,j in enumerate(bp):
                    raw[j] = p[i]
                outer_action.append(oi[normal(raw)])
            assert bitmask(outer_action[i] for i in range(10) if 932>>i&1) == 932
            for i,p in enumerate(rows):
                raw = [None]*9
                for a,b in enumerate(cp):
                    raw[b] = p[a]
                color = {}
                for value in raw:
                    color.setdefault(value,len(color))
                for value in range(4):
                    color.setdefault(value,len(color))
                dp = tuple(color[x] for x in raw)
                j = ri[dp]
                row_action.append(j)
                expected = [[] for _ in range(10)]
                for outer_row,fibre in enumerate(c['full_lifts_by_inner_then_outer_row'][i]):
                    for lift in fibre:
                        out = [None]*5
                        for a,b in enumerate(bp):
                            out[b] = color[lift[a]]
                        new_lift = out + list(dp)
                        expected[outer_action[outer_row]].append(new_lift)
                assert [sorted(f) for f in expected] == [sorted(f) for f in dc['full_lifts_by_inner_then_outer_row'][j]]
                assert bitmask(outer_action[t] for t in range(10) if c['column_masks'][i]>>t&1) == dc['column_masks'][j]
            assert len(set(row_action)) == 820
            assert bitmask(row_action[i] for i in range(820) if q['fixed_point']>>i&1) == dq['fixed_point']
            actions.append({'sign':sign,'shift':shift,'destination_query':dq['query_id'],
                            'original_vertex_map':vm,'C9_position_map':cp,
                            'outer_row_map':outer_action,'inner_row_map':row_action})
        ledger.append({'query_id':q['query_id'],'extras':e,'group':geometry_group(e),
                       'C9_order':c['boundary_order'],'supports':c['supports'],
                       'annulus_faces':c['annulus_faces'],'fixed_point':q['fixed_point'],
                       'joint_D5_actions':actions})
    assert Counter(x['group'] for x in ledger) == {'22-nonadjacent':5,'121-center-two':5,'211-end-two':10}
    return ledger


def triples(rows, apex):
    index = {p:i for i,p in enumerate(rows)}
    answer = set()
    for p in rows:
        if p[(apex-1)%9] != p[(apex+1)%9]:
            continue
        entries = []
        for color in range(4):
            if color != p[(apex-1)%9]:
                changed = list(p)
                changed[apex] = color
                entries.append(index[normal(changed)])
        answer.add(tuple(sorted(entries)))
    return sorted(answer)


def eliminate(initial, tri, table):
    current = initial
    trace = []
    while current:
        singleton = {}
        for i,t in enumerate(tri):
            live = [p for p in t if current>>p&1]
            if len(live) == 1:
                singleton.setdefault(live[0],i)
        after_triangle = current & ~bitmask(singleton)
        kempe = {}
        for p in range(820):
            if after_triangle>>p&1:
                failed = [s for s,choices in enumerate(table[p])
                          if not any(orbit & after_triangle == orbit for orbit in choices)]
                if failed:
                    kempe[p] = failed
        after = after_triangle & ~bitmask(kempe)
        trace.append({'before':current,'triangle_removals':sorted(singleton.items()),
                      'after_triangle':after_triangle,'kempe_removals':sorted(kempe.items()),'after':after})
        if after == current:
            break
        current = after
    return current,trace


def check_count_certificate(cert, frozen, residuals, rows, outer, table, tri):
    assert cert['schema'] == 'c9-932-h4-apex-d3-support-v1'
    assert cert['inner_pattern_order'] == [list(p) for p in rows]
    assert cert['outer_pattern_order'] == [list(p) for p in outer]
    assert cert['quotient_masks'] == frozen['quotient_masks']
    assert cert['quotient_partitions'] == frozen['quotient_partitions']
    assert cert['base'] == json.loads((ROOT/'INPUTS.json').read_text())['base']
    assert cert['source_certificate_sha256'] == hashlib.sha256((FROZEN/'c9/finite/certificate.v2.json.gz').read_bytes()).hexdigest()
    index = {p:i for i,p in enumerate(rows)}
    for a,provided in enumerate(cert['degree3_triples_by_boundary_position']):
        assert [t['row_indices'] for t in provided] == [list(t) for t in tri[a]]
        for t in provided:
            fixed = t['fixed_other_eight_colors']
            assert len(fixed)==9 and fixed[a] is None
            common = fixed[(a-1)%9]
            assert common == fixed[(a+1)%9] == t['common_neighbor_color']
            colors = [c for c in range(4) if c!=common]
            assert t['apex_color_options'] == colors
            members = []
            for c in colors:
                raw = list(fixed)
                raw[a] = c
                members.append(index[normal(raw)])
            assert t['row_indices_by_apex_color'] == members
            assert t['row_indices'] == sorted(members)
    assert len(cert['degree3_triples_by_boundary_position']) == 9
    qs = {q['query_id']:q for q in residuals}
    cases = {c['id']:c for c in frozen['cases']}
    systems = cert['same_H_count_systems']
    assert len(systems)==20 and {s['query_id'] for s in systems} == set(qs)
    for s in systems:
        q = qs[s['query_id']]
        c = cases[q['case_id']]
        assert s['case_id']==q['case_id'] and s['extras']==q['extras']
        assert s['boundary_order']==c['boundary_order'] and s['initial_support']==q['fixed_point']
        assert s['accepted_outer_rows']==[2,5,7,8,9] and s['rejected_outer_rows']==[0,1,3,4,6]
        # Both C5 and C9 proper S4 row orbits have size 24.  Double counting
        # all literal annulus lifts gives these fixed-outer transfer entries.
        expected = [[len(c['full_lifts_by_inner_then_outer_row'][i][j])
                     for i in range(820)] for j in range(10)]
        assert s['outer_transfer']==expected
    checked = set()
    triangle_steps = kempe_steps = removals_total = 0
    for hyp in cert['hypotheses']:
        key = (hyp['query_id'],hyp['apex'])
        assert key not in checked
        checked.add(key)
        q = qs[hyp['query_id']]
        c = cases[q['case_id']]
        a = hyp['apex_position']
        assert c['boundary_order'][a]==hyp['apex']
        assert hyp['apex'] in [f'a{i}' for i in range(5)]
        current = q['fixed_point']
        assert hyp['initial_support']==current
        for step in hyp['steps']:
            assert step['before']==current
            deleted = [r['row_index'] for r in step['removals']]
            assert len(deleted)==len(set(deleted)) and deleted
            assert all(current>>i&1 for i in deleted)
            for removal in step['removals']:
                p = removal['row_index']
                if step['rule']=='degree3_triangle':
                    t = tri[a][removal['triple_index']]
                    assert [i for i in t if current>>i&1]==[p]
                else:
                    assert step['rule']=='generic_c9_kempe'
                    options = table[p][removal['split_index']]
                    assert len(removal['first_missing_row_per_orbit'])==len(options)
                    for orbit,missing in zip(options,removal['first_missing_row_per_orbit']):
                        omitted = orbit & ~current
                        assert omitted and missing==(omitted & -omitted).bit_length()-1
            triangle_steps += step['rule']=='degree3_triangle'
            kempe_steps += step['rule']=='generic_c9_kempe'
            removals_total += len(deleted)
            current &= ~bitmask(deleted)
            assert step['after']==current
        assert current==hyp['final_support']==0
        assert hyp['missing_accepted_outer_rows']==[2,5,7,8,9]
        assert hyp['missing_quotient_indices']==list(range(232))
        assert hyp['result']=='degree3_hypothesis_excluded'
    assert checked=={(q,f'a{a}') for q in qs for a in range(5)}
    assert cert['summary']['whole_source_queries_excluded']==0
    assert cert['summary']['general_932_status']==cert['summary']['h_ge_5_status']=='OPEN'
    assert cert['summary']['four_colour_theorem_used'] is False
    assert cert['summary']['C8_equalities_or_conclusion_used'] is False
    return {'hypotheses':len(checked),'triangle_steps':triangle_steps,
            'kempe_steps':kempe_steps,'individual_deletions':removals_total,
            'complete_transfer_entries':20*10*820}


def negative_controls(cert, verify):
    def wrong_triangle(d):
        d['degree3_triples_by_boundary_position'][0][0]['row_indices'][0] = 0
    def wrong_apex(d):
        d['hypotheses'][0]['apex_position'] = 1
    def wrong_transfer(d):
        d['same_H_count_systems'][0]['outer_transfer'][0][0] += 1
    def wrong_chain(d):
        d['hypotheses'][0]['steps'][0]['after'] ^= 1
    def wrong_omitted(d):
        step = next(s for s in d['hypotheses'][0]['steps'] if s['rule']=='generic_c9_kempe')
        step['removals'][0]['first_missing_row_per_orbit'][0] = 819
    def wrong_scope(d):
        d['summary']['whole_source_queries_excluded'] = 20
    rejected = []
    for label,mutate in [('changed_actual_recoloring_triple',wrong_triangle),
                         ('wrong_original_apex_position',wrong_apex),
                         ('changed_full_annulus_count',wrong_transfer),
                         ('broken_support_deletion_chain',wrong_chain),
                         ('false_missing_kempe_row',wrong_omitted),
                         ('overclaimed_whole_source_exclusion',wrong_scope)]:
        bad = copy.deepcopy(cert)
        mutate(bad)
        try:
            verify(bad)
        except AssertionError:
            rejected.append(label)
        else:
            raise AssertionError('accepted corrupted main certificate: '+label)
    return rejected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--negative', action='store_true')
    args = parser.parse_args()
    cert_path = FROZEN/'c9/finite/certificate.v2.json.gz'
    payload = json.loads(gzip.decompress(cert_path.read_bytes()))
    rows,outer = words(9),words(5)
    assert payload['inner_pattern_order'] == [list(p) for p in rows]
    assert payload['outer_pattern_order'] == [list(p) for p in outer]
    assert [i for i in range(10) if 932>>i&1] == [i for i,p in enumerate(outer) if len(set(p)) == 4]
    residuals = [q for q in payload['queries'] if q['target']==932 and q['status']=='necessary_condition_residual']
    assert len(residuals)==20 and all(q['geometry_id']=='induced' for q in residuals)
    identities = check_transports(payload,residuals,rows,outer)
    table = kempe_table(rows)
    assert table == payload['kempe_obligations']
    rebuilt_triples = [triples(rows,a) for a in range(9)]
    cases = {c['id']:c for c in payload['cases']}
    exclusions = []
    for q in residuals:
        case = cases[q['case_id']]
        for a in range(5):
            pos = case['boundary_order'].index(f'a{a}')
            final,trace = eliminate(q['fixed_point'],rebuilt_triples[pos],table)
            assert final == 0,(q['query_id'],a,final.bit_count())
            exclusions.append({'query_id':q['query_id'],'apex':f'a{a}',
                               'C9_position':pos,'trace':trace,'final_support':final})
    result = {'schema':'c9-932-d3-independent-v1','status':'PASS',
              'frozen_certificate_sha256':hashlib.sha256(cert_path.read_bytes()).hexdigest(),
              'row_count':len(rows),'named_residuals':20,'joint_D5_transports':200,
              'group_sizes':dict(Counter(x['group'] for x in identities)),
              'triples_by_position':[len(t) for t in rebuilt_triples],
              'hypotheses_excluded':100,'round_histogram':dict(Counter(len(x['trace']) for x in exclusions)),
              'algorithm':'literal row enumeration; all Bell partitions with crossing rejection; multiplicity-aware D3 triangles',
              'scope':'same globally minimal no4ct source; target 932; h=4 only'}
    if args.write:
        with (HERE/'identities.json').open('x') as stream:
            json.dump({'rows':rows,'outer_rows':outer,'identities':identities},stream,sort_keys=True)
            stream.write('\n')
        with (HERE/'independent-certificate.json.gz').open('xb') as stream:
            raw=json.dumps({'summary':result,'triples':rebuilt_triples,'exclusions':exclusions},sort_keys=True).encode()
            stream.write(gzip.compress(raw,mtime=0))
    else:
        saved_identities = json.loads((HERE/'identities.json').read_text())
        expected_identities = {'rows':rows,'outer_rows':outer,'identities':identities}
        assert saved_identities==json.loads(json.dumps(expected_identities))
        saved_cert = json.loads(gzip.decompress((HERE/'independent-certificate.json.gz').read_bytes()))
        expected_cert = {'summary':result,'triples':rebuilt_triples,'exclusions':exclusions}
        assert saved_cert==json.loads(json.dumps(expected_cert))
    main_path = ROOT/'counts/certificate.json.gz'
    main_cert = json.loads(gzip.decompress(main_path.read_bytes()))
    verify = lambda c:check_count_certificate(c,payload,residuals,rows,outer,table,rebuilt_triples)
    result['main_certificate_replay'] = verify(main_cert)
    result['main_certificate_sha256'] = hashlib.sha256(main_path.read_bytes()).hexdigest()
    if args.negative:
        result['negative_controls_rejected'] = negative_controls(main_cert,verify)
    print(json.dumps(result,sort_keys=True))


if __name__ == '__main__':
    main()
