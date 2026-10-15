#!/usr/bin/env python3
"""Exact seven-pin relation, all-r-lifts, projection and F4 certificate audit.

No imported source solver, catalogue enumeration, CAS, or source realizability claim.
"""
import argparse
import ast
from collections import Counter, defaultdict
import hashlib
from itertools import combinations, permutations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
ROOT = HERE.parent.parent
BASE = "6ddea32a81349821ad3724ae1652bddb9c6a7b04"
PINS = ("z", "s", "v", "w", "t", "p", "q")
Q = tuple(range(4))
EDGES = ((0,1),(1,2),(2,3),(3,4),(0,4),(0,5),(0,6),(5,6))
FAN = (1,2,3,4)
SEARCH = "audits/2026-10-14-r6-319-enumeration-676b102/src/search.py"
TRANSFER = "audits/2026-10-14-c4-c5-recursion-fdd3e22/degree4/transfer.json"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def compact(rows):
    return ["".join(map(str, row)) for row in sorted(rows)]


def norm(row):
    d = {}
    return tuple(d.setdefault(x, len(d)) for x in row)


def mul(a, b):
    result = 0
    while b:
        if b & 1:
            result ^= a
        b >>= 1
        a <<= 1
        if a & 4:
            a ^= 7  # omega^2 + omega + 1
    return result


def cube(a):
    return mul(mul(a,a),a)


def eq(a, b):
    return 1 ^ cube(a ^ b)


def forbidden6(row):
    z,s,v,w,t,p,q = row
    f = eq(s,t)
    for a,b in ((p,v),(p,w),(q,v),(q,w)):
        f = mul(f,cube(a ^ b))
    return f


def r_accepted(row, r):
    z,s,v,w,t,p,q = row
    if z == r:
        return s == t and {p,q} == set(Q)-{z,s}
    if s == t:
        return bool({p,q} & (set(Q)-{z,s,r,t}))
    return {p,q} == {s,t}


def proper(row):
    return all(row[i] != row[j] for i,j in EDGES)


def lifts(row):
    return tuple(r for r in Q if all(r != row[i] for i in FAN))


def seal():
    manifest = json.loads((HERE/"INPUTS.json").read_text())
    assert manifest["base"] == BASE
    assert (HERE/"BASE").read_text().strip() == BASE
    for item in manifest["inputs"]:
        frozen = (HERE/"frozen"/item["path"]).read_bytes()
        assert sha(frozen) == item["sha256"], "frozen input drift: " + item["path"]
        assert (ROOT/item["path"]).read_bytes() == frozen, "live authority drift: " + item["path"]
    return sha((HERE/"INPUTS.json").read_bytes())


def source_table():
    module = ast.parse((HERE/"frozen"/SEARCH).read_text())
    constants = {}
    for stmt in module.body:
        if isinstance(stmt,ast.Assign) and len(stmt.targets)==1 and isinstance(stmt.targets[0],ast.Name):
            if stmt.targets[0].id in ("WORDS","PQ"):
                constants[stmt.targets[0].id] = ast.literal_eval(stmt.value)
    words, palettes = constants["WORDS"], constants["PQ"]
    rows = {tuple(map(int, word+pq)) for word,ps in zip(words,palettes,strict=True) for pq in ps.split()}
    trans = json.loads((HERE/"frozen"/TRANSFER).read_text())
    assert trans["pins"] == list(PINS)
    assert {tuple(ord(c)-65 for c in row) for row in trans["orbits"]} == rows
    assert trans["labelled_rows"] == 624
    assert trans["allowed_outer_mask"] == 319
    return words, rows


def projected(relation, scope):
    return {tuple(row[i] for i in scope) for row in relation}


def indicator_index(relation):
    index = defaultdict(list)
    for row in sorted(relation):
        index[row[:2]].append(row[2:])
    return index


def indicator(row, index):
    # Evaluate sum_{a in R} product_i [1-(x_i-a_i)^3] in F4.
    # Terms with mismatching first two coordinates are zero and omitted.
    value = 0
    for term in index[row[:2]]:
        delta = 1
        for x,a in zip(row[2:],term,strict=True):
            delta = mul(delta,eq(x,a))
            if not delta:
                break
        value ^= delta
    return value


def build():
    input_sha = seal()
    words,canonical = source_table()
    universe = list(product(Q,repeat=7))
    local = {row for row in universe if proper(row)}
    relation = {row for row in local if all(r_accepted(row,r) for r in lifts(row))}
    expanded = {tuple(perm[x] for x in row) for perm in permutations(Q) for row in canonical}
    assert relation == expanded and len(relation)==624 and len(canonical)==26
    assert {norm(row) for row in relation} == canonical
    assert all(cube(a)==int(a!=0) for a in Q)
    assert all(eq(a,b)==int(a==b) for a,b in product(Q,repeat=2))
    idx = indicator_index(relation)
    assert all(indicator(row,idx)==int(row in relation) for row in universe)
    polynomial_values = Counter(forbidden6(row) for row in universe)
    assert set(polynomial_values) <= {0,1}
    assert all(forbidden6(row)==0 for row in relation)

    projections = {}
    closure_rows = {}
    closure_counts = []
    for k in range(1,8):
        scopes = list(combinations(range(7),k))
        for scope in scopes:
            projections[scope] = projected(relation,scope)
        closed = {row for row in universe if all(tuple(row[i] for i in s) in projections[s] for s in scopes)}
        closure_rows[k] = closed
        closure_counts.append({"arity":k,"full_universe_closure":len(closed),
                               "local_proper_closure":len(closed & local),
                               "local_false_positives":len((closed & local)-relation)})
    assert [x["local_proper_closure"] for x in closure_counts]==[1440,1440,1440,720,720,624,624]
    assert closure_rows[4] == closure_rows[5]
    assert closure_rows[6] == relation
    assert {row for row in closure_rows[4] if forbidden6(row)==0} == relation
    false5 = closure_rows[5]-relation
    assert len(false5)==96
    false_can = sorted({norm(row) for row in false5})
    assert len(false_can)==4 and all(forbidden6(row)==1 for row in false5)
    witness5=[]
    for row in false_can:
        witnesses=[]
        for scope in combinations(range(7),5):
            witness = min(a for a in relation if all(a[i]==row[i] for i in scope))
            witnesses.append({"scope":[PINS[i] for i in scope],"allowed_full_seven_tuple":compact([witness])[0],
                              "all_r_lifts":list(lifts(witness))})
        witness5.append({"forbidden_seven_tuple":compact([row])[0],"all_r_lifts":list(lifts(row)),
                         "bad_r_lifts":[r for r in lifts(row) if not r_accepted(row,r)],
                         "five_pin_projection_witnesses":witnesses})
    # Two six-contact projections suffice as a relation identity over all 4^7 assignments.
    a=(0,1,2,3,5,6); b=(1,2,3,4,5,6)
    joined={row for row in universe if tuple(row[i] for i in a) in projections[a]
            and tuple(row[i] for i in b) in projections[b]}
    assert joined == relation

    local_rows=[]
    for row in sorted({norm(row) for row in local}):
        rs=lifts(row)
        for r in rs:
            full=row+(r,)
            assert all(full[i]!=full[j] for i,j in EDGES+tuple((7,i) for i in FAN))
        local_rows.append({"row":compact([row])[0],"allowed":row in relation,
                           "all_r_lifts":list(rs),"bad_r_lifts":[r for r in rs if not r_accepted(row,r)]})
    assert len(local_rows)==60
    empty_lift_rows={row for row in relation if not lifts(row)}
    assert len(empty_lift_rows)==288
    all_eight={row+(r,) for row in relation for r in lifts(row)}
    fibres=[]
    for word in words:
        outer=tuple(map(int,word))
        rows={r for r in relation if r[:5]==outer}
        total=0
        for row in rows:
            total ^= indicator(row,idx)
        fibres.append({"outer":word,"pq":compact({r[5:] for r in rows}),"integer_count":len(rows),
                       "boolean_exists":bool(rows),"F4_sum":total})
    assert [f["integer_count"] for f in fibres]==[2,4,6,4,2,6,0,0,2,0]
    assert all(f["F4_sum"]==0 for f in fibres)
    projection_meta=[]
    for scope,rows in sorted(projections.items(),key=lambda x:(len(x[0]),x[0])):
        enc=json.dumps(compact(rows),separators=(",",":"))
        projection_meta.append({"scope":[PINS[i] for i in scope],"size":len(rows),"rows_sha256":sha(enc.encode())})
    return {"schema":1,"base":BASE,"input_seal_sha256":input_sha,"checker_sha256":sha(Path(__file__).read_bytes()),
            "source_status":"not triggered: no genuine source graph supplied",
            "pins":list(PINS),"local_edges":[[PINS[i],PINS[j]] for i,j in EDGES],
            "allowed_canonical_rows":compact(canonical),"allowed_literal_rows":compact(relation),
            "all_local_canonical_rows_with_all_r_lifts":local_rows,
            "allowed_literal_eight_tuples":compact(all_eight),"retained_no_r_lift_literal_rows":compact(empty_lift_rows),
            "outer_fibres_including_empty":fibres,"projection_closures":closure_counts,"projection_metadata":projection_meta,
            "projection_arity":6,"five_projection_false_literals":compact(false5),"five_projection_negative_controls":witness5,
            "six_polynomial":{"formula":"(1-(s-t)^3)*(p-v)^3*(p-w)^3*(q-v)^3*(q-w)^3", "variables":["s","v","w","t","p","q"],
                              "field":"F2[omega]/(omega^2+omega+1)","zero_on_all_allowed":True,
                              "one_on_all_five_projection_false_rows":True,"all_4_power_7_value_counts":dict(sorted(polynomial_values.items()))},
            "exact_decompositions":{"all_four_projections_and_six_polynomial":True,
                                    "two_six_scopes":[[PINS[i] for i in s] for s in (a,b)]},
            "indicator_certificate":{"formula":"P_R=sum_{a in R} product_i(1-(x_i-a_i)^3)",
                                     "ideal_generators":"x_i^4-x_i for all seven pins; 1-P_R",
                                     "exhaustive_F4_evaluations":len(universe),"matches_all_r_lifts_relation":True},
            "counts":{"local_proper_literal_rows":len(local),"allowed_literal_rows":len(relation),
                      "allowed_canonical_rows":len(canonical),"no_r_lift_literal_rows":len(empty_lift_rows),
                      "all_legal_eight_tuples_for_allowed_rows":len(all_eight)}}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--generate",action="store_true")
    parser.add_argument("--check",action="store_true")
    parser.add_argument("--certificate",type=Path,default=HERE/"certificate.json")
    args=parser.parse_args()
    expected=build()
    if args.generate:
        with args.certificate.open("x") as stream:
            json.dump(expected,stream,indent=2,sort_keys=True)
            stream.write("\n")
        mode="generated exclusively"
    else:
        actual=json.loads(args.certificate.read_text())
        # JSON object keys for field-value counters are strings.
        assert actual==json.loads(json.dumps(expected)),"certificate mismatch with complete recomputation"
        mode="checked read-only"
    print(json.dumps({"status":"PASS","mode":mode,"certificate":str(args.certificate),
                      "certificate_sha256":sha(args.certificate.read_bytes()),"counts":expected["counts"],
                      "projection_arity":expected["projection_arity"],"frozen_input_drift":0,
                      "source_status":expected["source_status"]},sort_keys=True))


if __name__=="__main__":
    main()
