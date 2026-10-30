#!/usr/bin/env python3
"""Complete two-reference parity controls on the frozen 16 disks and one F4 failure.

Keeps original edge/vertex identities, all alpha/gamma references and every
complete cycle-subset exchange. Does not use 4CT or extend the F4 search domain.
"""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import random

import c5_parity_shared_cut_verification as base

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT/'audits/2026-10-29-parity-shared-cut-e1a90fe/verification.json'
TARGET = set(base.TARGET)


def traces(edges, selected):
    ids = sorted(selected)
    return [dict(s, edges=[ids[e] for e in s['edges']])
            for s in base.surgery.strands([edges[e] for e in ids])]


def exposed(edges, n, matching):
    return tuple(i for i,x in enumerate(base.word(edges,n,matching)) if not x)


def graph_pm(edges,n):
    return {p:base.matchings(edges,n,p) for p in base.PAIRS}


def frozen_graph(index,nv,raw):
    faces=base.oriented_faces(raw)
    primal_edges=sorted(base.forms.edges_of(faces))
    base.surgery.check_faces(nv,primal_edges,faces)
    edges=base.surgery.dual(primal_edges,faces)
    return dict(index=index,primal_vertices=nv,primal_edges=primal_edges,
                oriented_faces=faces,network_internal_vertices=len(faces),network_edges=edges)


def pair_audit(edges,n,alpha,gamma):
    assert base.odd(edges,alpha)==base.odd(edges,gamma)==0
    difference=traces(edges,alpha^gamma)
    paths=[i for i,c in enumerate(difference) if c['ends']]
    cycles=[i for i,c in enumerate(difference) if not c['ends']]
    assert len(paths)==2
    owner={v:i for i,c in enumerate(difference) for v in set(c['vertices'])}
    assert sum(len(set(c['vertices'])) for c in difference)==len(owner)
    keep=set(range(len(edges)))-(alpha|gamma)
    retained=traces(edges,keep)
    degree=Counter(v for e in keep for v in edges[e])
    for v in range(n):
        assert degree[v]==(1 if v in owner else 2)
    assert all(degree[n+i]==0 for i in range(5))
    for sid,s in enumerate(retained):
        s['id']=sid
        s['parity']=len(s['edges'])%2
        if s['ends']:
            assert len(s['ends'])==2 and all(v<n and v in owner for v in s['ends'])
            s['difference_components']=[owner[v] for v in s['ends']]
        else:
            assert s['parity']==0
            s['difference_components']=[]
    candidates=[]
    for pa in paths:
        for mask in range(1<<len(cycles)):
            selected={pa}|{c for j,c in enumerate(cycles) if mask>>j&1}
            toggled=frozenset(e for i in selected for e in difference[i]['edges'])
            matching=alpha^toggled
            assert base.saturated(edges,n,matching)
            exp=exposed(edges,n,matching)
            assert len(exp)==2
            ahit=alpha-matching
            ghit=gamma-matching
            assert ahit==frozenset(e for i in selected for e in difference[i]['edges'] if e in alpha)
            assert ghit==frozenset(e for i,c in enumerate(difference) if i not in selected for e in c['edges'] if e in gamma)
            complement=traces(edges,set(range(len(edges)))-matching)
            odd_rows=[]
            for c in complement:
                if c['ends'] or len(c['edges'])%2==0:
                    continue
                ce=set(c['edges'])
                ha=sorted(ce&ahit);hg=sorted(ce&ghit)
                assert ha and hg
                used=[s for s in retained if set(s['edges'])<=ce]
                assert all(not(set(s['edges'])&ce) or set(s['edges'])<=ce for s in retained)
                assert ce==set(e for s in used for e in s['edges'])|(ce&(alpha^gamma))
                cross=[s['id'] for s in used if s['ends'] and
                       ((s['difference_components'][0] in selected)!=(s['difference_components'][1] in selected))]
                assert len(cross)>=2 and len(cross)%2==0
                connector_ids=sorted(ce&(alpha^gamma))
                parity=(sum(s['parity'] for s in used)+len(connector_ids))%2
                assert parity==1
                if not cycles:
                    assert all(set(retained[sid]['difference_components'])==set(paths) for sid in cross)
                odd_rows.append(dict(cycle=c,alpha_removed_hits=ha,gamma_removed_hits=hg,
                                     retained_segment_ids=[s['id'] for s in used],
                                     selected_to_unselected_segments=cross,
                                     difference_connector_edges=connector_ids,compressed_parity=parity))
            candidates.append(dict(selected_path=pa,selected_cycles=[i for i in cycles if i in selected],
                                   matching=sorted(matching),exposed=exp,target=exp in TARGET,
                                   alpha_removed=sorted(ahit),gamma_removed=sorted(ghit),
                                   full_complement=complement,odd_cycles=odd_rows,
                                   odd=len(odd_rows),no_difference_cycles=not cycles))
    return dict(alpha=sorted(alpha),gamma=sorted(gamma),
                alpha_exposed=exposed(edges,n,alpha),gamma_exposed=exposed(edges,n,gamma),
                difference_components=difference,path_components=paths,cycle_components=cycles,
                common_retained_segments=retained,candidates=candidates,
                target_success=any(c['target'] and c['odd']==0 for c in candidates))


def audit_graph(g,full_families=True):
    edges=g['network_edges'];n=g['network_internal_vertices']
    pm=graph_pm(edges,n)
    good={p:[m for m in ms if base.odd(edges,m)==0] for p,ms in pm.items()}
    pairs=[pair_audit(edges,n,a,r) for a,r in product(good[(1,4)],good[(0,2)]+good[(0,3)])]
    targets=[dict(exposed=p,matching=sorted(m)) for p in base.TARGET for m in good[p]]
    return dict(graph=g,complete_pm_families={''.join(map(str,p)):[sorted(m) for m in ms] for p,ms in pm.items()} if full_families else None,
                even_counts={''.join(map(str,p)):len(ms) for p,ms in good.items()},
                triggered=bool(pairs),status='triggered and holds' if pairs else 'not triggered',
                reference_pairs=pairs,graph_one_swap_failure=bool(pairs) and not any(p['target_success'] for p in pairs),
                independently_existing_good_targets=targets)


def multi_reference_hits(row):
    """All same-graph star-reference pairs against each odd target candidate."""
    g=row['graph'];edges=g['network_edges'];n=g['network_internal_vertices']
    pm={tuple(map(int,p)):[frozenset(m) for m in ms] for p,ms in row['complete_pm_families'].items()}
    good={p:[m for m in pm[p] if base.odd(edges,m)==0] for p in base.STAR}
    output=[]
    for pair in row['reference_pairs']:
        for candidate in pair['candidates']:
            if not candidate['target'] or not candidate['odd']:
                continue
            m=frozenset(candidate['matching']);tests=[]
            for p,q in combinations(base.STAR,2):
                refs=[]
                for a,r in product(good[p],good[q]):
                    hits=[]
                    for cycle in candidate['odd_cycles']:
                        ce=set(cycle['cycle']['edges'])
                        ha=sorted(ce&(a-m));hr=sorted(ce&(r-m))
                        assert ha and hr
                        hits.append(dict(alpha_hits=ha,gamma_hits=hr))
                    refs.append(dict(first=sorted(a),second=sorted(r),odd_cycle_hits=hits))
                tests.append(dict(exposed_pairs=[p,q],reference_products=refs,
                                  status='triggered and holds' if refs else 'not triggered'))
            output.append(dict(matching=sorted(m),exposed=candidate['exposed'],pairs=tests))
    return output


def summary(rows):
    pairs=[p for r in rows for p in r['reference_pairs']]
    candidates=[c for p in pairs for c in p['candidates']]
    return dict(graphs=len(rows),triggered_graphs=sum(r['triggered'] for r in rows),
                not_triggered_graphs=sum(not r['triggered'] for r in rows),
                reference_pairs=len(pairs),all_path_subset_candidates=len(candidates),
                target_candidates=sum(c['target'] for c in candidates),
                odd_target_candidates=sum(c['target'] and bool(c['odd']) for c in candidates),
                no_difference_cycle_odd_target_candidates=sum(c['target'] and bool(c['odd']) and c['no_difference_cycles'] for c in candidates),
                checked_odd_cycles=sum(len(c['odd_cycles']) for c in candidates),
                graph_one_swap_failures=sum(r['graph_one_swap_failure'] for r in rows))


def report():
    old=json.loads(INPUT.read_text())
    controls=[]
    for old_g in old['graphs']:
        g={k:old_g[k] for k in ('index','primal_vertices','primal_edges','oriented_faces','network_internal_vertices','network_edges')}
        base.surgery.check_faces(g['primal_vertices'],g['primal_edges'],[tuple(f) for f in g['oriented_faces']])
        assert [list(e) for e in base.surgery.dual([tuple(e) for e in g['primal_edges']],g['oriented_faces'])]==g['network_edges']
        row=audit_graph(g)
        assert row['complete_pm_families']=={p:ms for p,ms in old_g['complete_pm_families'].items() if len(p)==2}
        controls.append(row)
    rng=random.Random(5)
    prefix=[];failure=None
    for index in range(200):
        steps=rng.randrange(2,12)
        nv,raw=base.forms.random_near_triangulation(rng,steps)
        g=frozen_graph(index,nv,raw)
        row=audit_graph(g)
        prefix.append(dict(generator_index=index,requested_steps=steps,raw_faces=raw,
                           graph=g,even_counts=row['even_counts'],triggered=row['triggered'],
                           reference_pairs=len(row['reference_pairs']),one_swap_failure=row['graph_one_swap_failure']))
        if row['graph_one_swap_failure']:
            failure=row
            break
    assert failure is not None
    assert failure['graph']['index']==14 and failure['graph']['primal_vertices']==10
    assert failure['independently_existing_good_targets']
    multi=multi_reference_hits(failure)
    failure['five_reference_ten_pair_hits']=multi
    assert all(len(c['pairs'])==10 for c in multi)
    deps=['scripts/c5_two_reference_parity_verification.py','scripts/c5_parity_shared_cut_verification.py',
          'scripts/c5_parity_swap_probe.py','scripts/c5_equivalent_forms_check.py','scripts/c5_dual_path_surgery.py',
          str(INPUT.relative_to(ROOT))]
    return dict(base='e1a90fea41702d7c98747716a5960198aecbecb3',
                scope='Exact reuse of 16 previous disks plus first failure in pre-existing F4 seed5/200 prefix. No broad P4 extension or general exclusion.',
                reused_controls=controls,reused_totals=summary(controls),
                directed_f4=dict(seed=5,original_graph_budget=200,generated_prefix=len(prefix),
                                 prefix=prefix,first_graph_wide_failure=failure,totals=summary([failure])),
                source_sha256={p:sha256((ROOT/p).read_bytes()).hexdigest() for p in deps})


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path)
    parser.add_argument('--check',type=Path)
    args=parser.parse_args()
    result=report()
    payload=json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    if args.check:
        assert args.check.read_text()==payload,'two-reference certificate differs'
    if args.out:
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_text(payload)
    print(json.dumps(dict(reused=result['reused_totals'],
                          directed_f4=result['directed_f4']['totals'],
                          directed_f4_prefix=result['directed_f4']['generated_prefix']),sort_keys=True))


if __name__=='__main__':
    main()
