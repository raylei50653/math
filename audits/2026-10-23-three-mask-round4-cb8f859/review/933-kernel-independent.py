#!/usr/bin/env python3
"""D-first independent fixed-cap kernel replay. No 933 code is imported."""
import argparse,hashlib,itertools,json
from collections import Counter
from pathlib import Path

HERE=Path(__file__).resolve().parent
CERT=HERE.parent/'933/certificate.json'
SRC=HERE.parent/'933/frozen/audits/2026-10-18-smaller-bad-counts-e1617a2/frozen/audits/2026-10-18-smaller-bad-e1617a2/kempe-consistency.json'
E=('a','n','R','L','q','c','x','y')
D=('a','n','R','L','q','c','s','v','w','t')
FULL=D+('r','x','y')
FACES=(('x','y','r'),('y','t','r'),('t','w','r'),('w','v','r'),('v','s','r'),('s','x','r'),('x','s','c'),('y','a','t'))

def require(ok,message):
    if not ok:raise AssertionError(message)

def canonical(word):
    labels={};return tuple(labels.setdefault(c,len(labels)) for c in word)

def proper_rows(n):
    result=[]
    def visit(word):
        if len(word)==n:
            if word[-1]!=word[0]:result.append(tuple(word))
            return
        for color in range(min(4,max(word,default=-1)+2)):
            if not word or word[-1]!=color:visit(word+[color])
    visit([]);return result

def digest(data):return hashlib.sha256(data).hexdigest()

def run():
    raw= CERT.read_bytes();cert=json.loads(raw);source=json.loads(SRC.read_bytes())
    require(cert['original_E_order']==list(E) and cert['actual_D_order']==list(D),'original ordered contacts')
    require(cert['original_r_rotation']==['x','y','t','w','v','s'],'original rotation')
    require(cert['cap_oriented_faces']==[list(f) for f in FACES],'all eight original cap faces')
    edges=sorted({tuple(sorted((u,v))) for face in FACES for u,v in zip(face,face[1:]+face[:1])})
    require(cert['cap_edges']==[list(e) for e in edges],'all original cap edges')
    ew=proper_rows(8);dw=proper_rows(10);ei={w:i for i,w in enumerate(ew)};di={w:i for i,w in enumerate(dw)}
    require(len(ew)==274 and [list(w) for w in ew]==source['tuples'],'all canonical E rows/order')
    require(len(dw)==2461 and [list(w) for w in dw]==cert['D_words'],'all canonical D rows/order')
    positions={v:i for i,v in enumerate(FULL)};ep=[positions[v] for v in E];edge_positions=[(positions[u],positions[v]) for u,v in edges]
    group=list(itertools.permutations(range(4)));images=set();single_restoration_images=set();raw_images=[];valid_cap_count=0;stabilizers=Counter();D_color_counts=Counter()
    for did,dword in enumerate(dw):
        for private in itertools.product(range(4),repeat=3):
            full=dword+private
            if any(full[a]==full[b] for a,b in edge_positions):continue
            valid_cap_count+=1;D_color_counts[len(set(dword))]+=1
            literal_E=tuple(full[i] for i in ep);canonical_E=canonical(literal_E);expected_eid=ei[canonical_E]
            restorations=[g for g in group if tuple(g[c] for c in literal_E)==canonical_E]
            require(len(restorations)==(2 if len(set(literal_E))==2 else 1),'unused E-color stabilizer')
            stabilizers[len(restorations)]+=1
            single_restoration_images.add(tuple(restorations[0][c] for c in full))
            for g in restorations:
                restored=tuple(g[c] for c in full)
                require(tuple(restored[i] for i in ep)==canonical_E,'one common full-tuple S4 restoration')
                require(di[canonical(restored[:10])]==did,'whole D identity after restoration')
                require(ei[tuple(restored[i] for i in ep)]==expected_eid,'E identity after restoration')
                # Both D-unused-color and E-unused-color stabilizers can cause
                # duplicates. De-duplicate the entire literal thirteen-tuple.
                images.add(restored);raw_images.append(restored)
    fibres=[]
    for eword in ew:
        line=[]
        for tail in itertools.product(range(4),repeat=4):
            dword=eword[:6]+tail
            did=di[canonical(dword)] if all(dword[i]!=dword[(i+1)%10] for i in range(10)) else None
            line.append([did,[]])
        fibres.append(line)
    kernel=[Counter() for _ in ew];naive_kernel=[Counter() for _ in ew]
    for full in sorted(images):
        eword=tuple(full[i] for i in ep);eid=ei[eword];did=di[canonical(full[:10])]
        tail=full[6:10];tail_id=sum(c*4**(3-i) for i,c in enumerate(tail));r=full[10]
        require(fibres[eid][tail_id][0]==did,'literal tail maps to wrong complete D row')
        require(r not in fibres[eid][tail_id][1],'full-lift duplicate retained')
        fibres[eid][tail_id][1].append(r);kernel[eid][did]+=1
    for line in fibres:
        for _,lifts in line:lifts.sort()
    for full in raw_images:
        eid=ei[tuple(full[i] for i in ep)];did=di[canonical(full[:10])];naive_kernel[eid][did]+=1
    sparse=[{str(k):v for k,v in sorted(row.items())} for row in kernel]
    require(sparse==cert['generic_E_to_D_sparse_kernel'],'D-first complete 274x2461 kernel mismatch')
    require(fibres==cert['complete_274_by_256_tail_fibres'],'D-first full 70144 literal tail fibres mismatch')
    entries=sum(len(row) for row in kernel);full_lifts=sum(sum(row.values()) for row in kernel)
    require(full_lifts==len(images)==sum(len(lifts) for line in fibres for _,lifts in line),'complete full-lift multiplicity')
    require(len(single_restoration_images)<len(images),'unused E-color stabilizer was not exercised')
    naive_overcount=sum(sum(row.values()) for row in naive_kernel)-full_lifts
    return {'status':'PASS','method':'D-first:2461 canonical D rows x64 rxy; common full-thirteen-tuple S4 restoration and global literal dedup',
            'imports_933_code':False,'source_graph_enumeration':False,'scope':'fixed original cap finite kernel only',
            'certificate_sha256':digest(raw),'source_sha256':digest(SRC.read_bytes()),'script_sha256':digest(Path(__file__).read_bytes()),
            'ordered_E':list(E),'ordered_D':list(D),'full_tuple_order':list(FULL),'cap_edges':len(edges),'cap_faces':len(FACES),
            'canonical_E_rows':274,'canonical_D_rows':2461,'rxy_assignments_per_D':64,'D_first_candidates':2461*64,
            'proper_canonical_D_cap_lifts':valid_cap_count,'proper_cap_lifts_by_D_color_count':dict(sorted(D_color_counts.items())),
            'E_restoration_stabilizer_sizes':dict(sorted(stabilizers.items())),
            'common_S4_images_before_global_literal_dedup':len(raw_images),
            'duplicate_full_literal_images_removed':len(raw_images)-len(images),'complete_restored_full_lifts':full_lifts,
            'kernel_shape':[274,2461],'nonzero_kernel_entries':entries,'kernel_coefficients':dict(sorted(Counter(v for row in kernel for v in row.values()).items())),
            'kernel_full_lift_multiplicity_sum':full_lifts,'all_kernel_entries_equal':True,
            'complete_tail_fibres':274*256,'empty_tail_fibres':sum(not lifts for line in fibres for _,lifts in line),
            'nonempty_tail_fibres':sum(bool(lifts) for line in fibres for _,lifts in line),
            'improper_D_tail_fibres':sum(did is None for line in fibres for did,_ in line),'all_empty_and_full_tail_fibres_equal':True,
            'rebuilt_kernel_sha256':digest(json.dumps(sparse,sort_keys=True,separators=(',',':')).encode()),
            'rebuilt_tail_fibres_sha256':digest(json.dumps(fibres,separators=(',',':')).encode()),
            'global_literal_dedup_control':{'status':'triggered and holds','excess_multiplicity_removed':naive_overcount},
            'naive_only_one_E_restoration':{'status':'counterexample','missing_full_literal_lifts':len(images)-len(single_restoration_images)},
            'full_original_933_source':'not triggered','source_realization_claimed':False}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--write',action='store_true');args=parser.parse_args();result=run()
    if args.write:
        with (HERE/'933-kernel-independent.json').open('x') as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':main()
