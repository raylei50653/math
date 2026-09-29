#!/usr/bin/env python3
"""Independent per-root transport/interface audit; existing sources are read-only.

Only stdlib is used. No source graph, geometry, or relation catalogue is generated.
Saved complete ordered schemas are checked as relations, never as marginals.
The paper argument is in docs/c5_no_mixed_hypothesis_audit.md, section 3.1.
"""

import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts/c5_no_mixed_root_transport/observations.json"
U = frozenset(range(4))
Q = (0, 1, 0, 1, 2)
TARGETS = ((0, 1, 0, 2, 1), (0, 1, 2, 1, 2))
PERMS = tuple(permutations(range(4)))
ROOTS = ("z", "w")
FAMILIES = {
    "AA": ("t2_path_palettes", 322), "AB": ("t2_t1_endpoints", 560),
    "AC": ("t2_t0_pairs", 24), "AE": ("t2_t0_singles", 120),
    "BB": ("bb", 888), "BC": ("bc", 24), "BE": ("be", 144),
}
# (number of spokes, contact counts, sorted source ban sizes, omega)
SIDES = {
    "A": (2, (2,), (1,), 2), "B": (1, (2, 1), (1, 1), 2),
    "C": (0, (2, 2), (1, 2), 3), "D": (0, (2, 2), (2, 2), 4),
    "E": (0, (2, 1, 1), (1, 1, 1), 3),
}
CLASSES = ("EMPTY_BOTH", "EMPTY_Z_ONLY", "EMPTY_W_ONLY", "SAME_SINGLETON", "PASS")


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def artifact(suffix):
    return f"artifacts/c5_adjacent_degree5_no_mixed_{suffix}/observations.json"


def resolve(data, pointer):
    for part in pointer.strip("/").split("/"):
        data = data[int(part)] if isinstance(data, list) else data[part]
    return data


class Inputs:
    def __init__(self):
        self.hashes = {}

    def read(self, path):
        raw = (ROOT / path).read_bytes()
        self.hashes[path] = sha256(raw).hexdigest()
        return json.loads(raw)

    def ref(self, path, data, pointer):
        return {"path": path, "json_pointer": pointer, "value_sha256": digest(resolve(data, pointer))}


@lru_cache(None)
def compatible(support, row):
    result = tuple(pi for pi in PERMS if all(pi[Q[h]] == row[h] for h in support))
    partition_equal = all((Q[i] == Q[j]) == (row[i] == row[j])
                          for i, j in combinations(support, 2))
    assert bool(result) == partition_equal
    return result


def elementary_controls():
    assert all(all(row[i] != row[(i + 1) % 5] for i in range(5)) for row in (Q, *TARGETS))
    rows = []
    for bits in range(32):
        support = tuple(i for i in range(5) if bits >> i & 1)
        # Every injective lift into one traversal, including either copy of the cut.
        lifts = [(a, ll) for a in range(5) for ll in combinations(range(6), len(support))
                 if len({(a + x) % 5 for x in ll}) == len(support)
                 and {(a + x) % 5 for x in ll} == set(support)]
        spans = sorted({max(ll) - min(ll) if ll else 0 for _, ll in lifts})
        shortest = next(n for n in range(5) if any(
            set(support) <= {(a + x) % 5 for x in range(n + 1)} for a in range(5)))
        assert shortest == min(spans)
        for ti, row in enumerate(TARGETS, 1):
            pp = compatible(support, row)
            if not pp:
                assert shortest >= 2 and all(n >= 2 for n in spans)
            if shortest <= 1:
                assert pp
            rows.append(dict(support=support, target=ti, permutations=pp,
                             shortest_arc=shortest, all_lift_hull_spans=spans,
                             lifts_checked=len(lifts)))
    # Exhaust all root lists to check exclusivity and completeness of failure labels.
    classes = Counter()
    subsets = [set(i for i in U if mask >> i & 1) for mask in range(16)]
    for z, w in product(subsets, repeat=2):
        label = classify({"z": z, "w": w})
        assert (label == "PASS") == any(a != b for a, b in product(z, w))
        classes[label] += 1
    lambdas = {t: max(s[3], len(s[1]) + 1) for t, s in SIDES.items()}
    allowed = [a + b for i, a in enumerate(SIDES) for b in list(SIDES)[i:]
               if lambdas[a] + lambdas[b] <= 5]
    assert lambdas == dict(A=2, B=3, C=3, D=4, E=4)
    assert allowed == ["AA", "AB", "AC"]
    return dict(support_target_controls=rows, failure_partition_controls=dict(classes),
                lambda_by_side=lambdas, double_nontransportable_types=allowed)


def classify(E):
    z, w = E["z"], E["w"]
    if not z and not w:
        return "EMPTY_BOTH"
    if not z:
        return "EMPTY_Z_ONLY"
    if not w:
        return "EMPTY_W_ONLY"
    if len(z) == 1 and z == w:
        return "SAME_SINGLETON"
    return "PASS"


def flatten(record, pointer):
    while "original_record" in record or "inherited_record" in record:
        key = "original_record" if "original_record" in record else "inherited_record"
        record, pointer = record[key], pointer + "/" + key
    return record, pointer


def context(rec, source, family):
    components, units = [], []
    for root, side_type in zip(ROOTS, family, strict=True):
        side = source[root]
        t, ports, sizes, _ = SIDES[side_type]
        assert (len(side["root_boundary"]), tuple(side["ports"]),
                tuple(sorted(map(len, side["forbidden"])))) == (t, ports, sizes)
        for j, (k, F) in enumerate(zip(side["ports"], side["forbidden"], strict=True)):
            name = "CDE"[j] + root
            c = dict(name=name, root=root, ports=k, contacts=[f"{name}_{i}" for i in range(k)],
                     support=rec["supports"][len(units)], support_index=len(units), Fq=F)
            components.append(c)
            units.append(c)
        for j, h in enumerate(side["root_boundary"]):
            assert rec["supports"][len(units)] == [h]
            units.append(dict(name=f"{root}{j}", root=root, support=[h],
                              support_index=len(units)))
    assert len(units) == len(rec["supports"])
    for root in ROOTS:
        used = {Q[h] for h in source[root]["root_boundary"]}
        assert len(used) == len(source[root]["root_boundary"])
        for c in components:
            if c["root"] == root:
                assert not used.intersection(c["Fq"])
                used.update(c["Fq"])
        assert U - used == {source[root]["common"]}
    assert source["z"]["common"] == source["w"]["common"]
    return components, units


def placement_audit(pl, units, components, family):
    lifts, anchor, names = pl["lifts"], pl["anchor"], pl["order"]
    assert 0 <= anchor < 5 and len(lifts) == len(units)
    by_name = {u["name"]: u for u in units}
    assert len(names) == len(set(names)) and set(names) == set(by_name)
    for u, ll in zip(units, lifts, strict=True):
        assert ll and 0 <= min(ll) <= max(ll) <= 5
        assert len(ll) == len(set(ll)) == len(u["support"])
        assert sorted({(anchor + x) % 5 for x in ll}) == u["support"]
    order = [by_name[n]["support_index"] for n in names]
    assert all(max(lifts[a]) <= min(lifts[b]) for a, b in zip(order, order[1:]))
    rr = [by_name[n]["root"] for n in names]
    assert sum(rr[i] != rr[(i + 1) % len(rr)] for i in range(len(rr))) == 2
    spans, masks = {}, {}
    for c in components:
        ll = lifts[c["support_index"]]
        span = max(ll) - min(ll)
        assert 1 <= span < 5
        if len(c["Fq"]) == 2:
            assert span >= 2
        spans[c["name"]] = span
        masks[c["name"]] = sum(1 << ((anchor + x) % 5) for x in range(min(ll), max(ll)))
    assert all(not a & b for a, b in combinations(masks.values(), 2))
    # Rotate the SAME saved order at a root transition. Lift the wrapped suffix
    # by five, instead of independently minimizing the two sides' circular hulls.
    start = next(i for i in range(len(rr)) if rr[i] != rr[i - 1])
    cyclic = []
    for j in range(len(order)):
        i = (start + j) % len(order)
        ll = [x + (5 if start + j >= len(order) else 0) for x in lifts[order[i]]]
        cyclic.append((rr[i], ll))
    assert all(max(a[1]) <= min(b[1]) for a, b in zip(cyclic, cyclic[1:]))
    assert max(cyclic[-1][1]) <= min(cyclic[0][1]) + 5
    intervals, side_masks = {}, {}
    for root, typ in zip(ROOTS, family, strict=True):
        values = [x for r, ll in cyclic if r == root for x in ll]
        lo, hi = min(values), max(values)
        ell = hi - lo
        assert ell >= SIDES[typ][3]
        assert ell >= sum(spans[c["name"]] for c in components if c["root"] == root)
        intervals[root] = dict(lift_interval=[lo, hi], span=ell)
        side_masks[root] = sum(1 << ((anchor + x) % 5) for x in range(lo, hi))
    assert not side_masks["z"] & side_masks["w"]
    assert sum(v["span"] for v in intervals.values()) <= 5
    return dict(saved_placement=pl, component_spans=spans, component_edge_masks=masks,
                side_intervals=intervals, side_edge_masks=side_masks)


def forbidden(relation):
    assert relation
    return frozenset.intersection(*(frozenset(t) for t in relation))


def moved(relation, pi):
    return frozenset(tuple(pi[c] for c in t) for t in relation)


@lru_cache(None)
def relation_controls(relation, support, Fq):
    """Check whole ordered relations and pi-independence for each saved schema."""
    assert forbidden(relation) == frozenset(Fq)
    for pi in compatible(support, Q):
        assert moved(relation, pi) == frozenset(relation)
    checks = 0
    for row in TARGETS:
        pp = compatible(support, row)
        if pp:
            images = [moved(relation, pi) for pi in pp]
            assert all(image == images[0] for image in images)
            for pi, image in zip(pp, images, strict=True):
                assert forbidden(image) == frozenset(pi[x] for x in Fq)
                inverse = tuple(pi.index(x) for x in range(4))
                assert moved(image, inverse) == frozenset(relation)
                checks += 1
    return checks


def source_relations(data, rec, components):
    catalog_key = "q_complete_schemas" if "q_complete_schemas" in data else "q_complete_binary_schemas"
    catalog = data[catalog_key]
    checks = schemas = 0
    for j, c in enumerate(components):
        if c["ports"] == 1:
            if "q_single_contact_relations" in rec:
                relation = rec["q_single_contact_relations"][c["name"]]
            else:
                relation = rec.get("q_single_contact_relation", rec.get("q_unary_relation"))
            assert relation == [[c["Fq"][0]]]
            rels = [relation]
        else:
            ids = rec["q_schema_ids"]
            ids = ids[j] if isinstance(ids, list) else ids[c["name"]]
            assert ids and len(ids) == len(set(ids))
            key = ",".join(map(str, c["Fq"]))
            rels = [catalog[key][i] for i in ids]
            c["source_schema_ids"] = ids
            c["source_schema_catalog"] = f"/{catalog_key}/{key}"
        for rel in rels:
            assert all(len(t) == c["ports"] for t in rel)
            checks += relation_controls(tuple(map(tuple, rel)), tuple(c["support"]), tuple(c["Fq"]))
            schemas += 1
    return schemas, checks


def component_options(c, row):
    pp = compatible(tuple(c["support"]), row)
    if pp:
        images = {tuple(sorted(pi[x] for x in c["Fq"])) for pi in pp}
        assert len(images) == 1
        opts = sorted(images)
    else:
        stabilizer = [pi for pi in PERMS if all(pi[row[h]] == row[h] for h in c["support"])]
        opts = [F for n in range(c["ports"] + 1) for F in combinations(range(4), n)
                if all({pi[x] for x in F} == set(F) for pi in stabilizer)]
    return dict(name=c["name"], permutations=pp, exact=bool(pp), options=opts)


def set_dict(values):
    return {r: sorted(values[r]) for r in ROOTS}


def certificate(inputs, family, data, path, ri, ti, ji, join, aa_previous):
    """Resolve old exclusion entries; this does not rerun their geometry proofs."""
    base = f"/records/{ri}"
    if family in ("AA", "AB"):
        cases = data["records"][ri]["targets"][ti]["cases"]
        ci, case = next((i, c) for i, c in enumerate(cases) if c["original_join_index"] == ji)
        assert case["original_join"] == join and case["eliminated"]
        entry = inputs.ref(path, data, base + f"/targets/{ti}/cases/{ci}")
        if family == "AB":
            pointer = base + f"/targets/{ti}/cases/{ci}/endpoint_evidence"
            mechanism = "original_endpoints"
            if not case["endpoint_evidence"]["eliminated"]:
                prior = data["records"][ri]["inherited_record"]["targets"][ti]["cases"][ji]
                assert prior["original_join"] == join and prior["evidence"]["eliminated"]
                pointer = base + f"/inherited_record/targets/{ti}/cases/{ji}/evidence"
                mechanism = "original_bridge"
            return dict(entry=entry, evidence=inputs.ref(path, data, pointer), mechanism=mechanism)
        if case["path_evidence"]:
            assert case["path_evidence"]["eliminated"]
            return dict(entry=entry, evidence=inputs.ref(path, data, base + f"/targets/{ti}/cases/{ci}/path_evidence"),
                        mechanism="whole_original_path_palette_switch")
        old_path, old = aa_previous
        old_rec = old["records"][ri]
        oi, oc = next((i, c) for i, c in enumerate(old_rec["targets"][ti]["cases"])
                      if c["original_join_index"] == ji)
        assert oc["original_join"] == join and oc["eliminated"]
        pointer = base + f"/targets/{ti}/cases/{oi}/endpoint_evidence"
        mechanism = "original_endpoints"
        if not oc["endpoint_evidence"]["eliminated"]:
            bi, bc = next((i, c) for i, c in enumerate(old_rec["inherited_record"]["targets"][ti]["cases"])
                          if c["original_join_index"] == ji)
            assert bc["original_join"] == join and bc["evidence"]["eliminated"]
            pointer = base + f"/inherited_record/targets/{ti}/cases/{bi}/evidence"
            mechanism = "original_bridge"
        return dict(entry=entry, evidence=inputs.ref(old_path, old, pointer), mechanism=mechanism)
    if family == "AC":
        assert join["evidence"]["eliminated"]
        return dict(entry=inputs.ref(path, data, base + f"/targets/{ti}/joins/{ji}/evidence"),
                    mechanism="source_saturated_component_target_K5")
    assert family == "BB"
    cases = data["records"][ri]["final_targets"][ti]["failing_candidate_cases"]
    ci, case = next((i, c) for i, c in enumerate(cases) if c["join_index"] == ji)
    assert case["original_join"] == join and case["evidence"]["eliminated"]
    return dict(entry=inputs.ref(path, data, base + f"/final_targets/{ti}/failing_candidate_cases/{ci}"),
                mechanism=case["evidence"]["stage"])


def build():
    inputs = Inputs()
    controls = elementary_controls()
    anchor_path = "artifacts/c5_no_mixed_hypothesis_audit/anchor.json"
    old_anchor = inputs.read(anchor_path)
    anchors = {(x["cell"], x["record_id"], x["target"]): (i, x)
               for i, x in enumerate(old_anchor["queries"])}
    assert len(anchors) == len(old_anchor["queries"]) == 4164
    aa_path = artifact("t2_endpoints")
    aa_previous = (aa_path, inputs.read(aa_path))
    records, failures, families = [], [], {}
    total = Counter()
    nontransportable, doubles, labels, hit_roots = Counter(), Counter(), Counter(), Counter()
    for family, (suffix, expected) in FAMILIES.items():
        path = artifact(suffix)
        data = inputs.read(path)
        geo_path = artifact("t2") if family == "AA" else path
        geo_data = inputs.read(geo_path) if family == "AA" else data
        sources = data.get("original_records", data.get("original_frontier"))
        count, family_labels, family_bad = Counter(), Counter(), Counter()
        for ri, final in enumerate(data["records"]):
            rec, pointer = flatten(final, f"/records/{ri}")
            if rec.get("status") in ("excluded", "source_excluded"):
                continue
            source = sources[rec["source_id"]]
            components, units = context(rec, source, family)
            n, checks = source_relations(data, rec, components)
            count.update(source_relation_instances=n, whole_relation_permutation_checks=checks)
            geo = geo_data["geometries"][rec["geometry_id"]]
            assert geo["supports"] == rec["supports"] and geo["placements"]
            placements = [placement_audit(pl, units, components, family) for pl in geo["placements"]]
            count["placements"] += len(placements)
            entry = dict(family=family, record_id=rec["id"], source_id=rec["source_id"],
                         source_side_ids=source["side_ids"], components=components,
                         root_boundary={r: source[r]["root_boundary"] for r in ROOTS},
                         original_root_edge=["z", "w"],
                         units=[{k: u[k] for k in ("name", "root", "support_index", "support")} for u in units],
                         placements=placements,
                         original_record=inputs.ref(path, data, pointer),
                         geometry=inputs.ref(geo_path, geo_data, f"/geometries/{rec['geometry_id']}"),
                         targets=[])
            count["retained_supports"] += 1
            final_targets = final.get("final_targets", final.get("targets"))
            assert len(rec["targets"]) == len(final_targets) == 2
            for ti, row in enumerate(TARGETS):
                target = rec["targets"][ti]
                assert target["row"] == final_targets[ti]["row"] == list(row)
                assert final_targets[ti]["status"] == "accept"
                ai, prior = anchors.pop((family, rec["id"], ti + 1))
                h, sigma = (1, (0, 2, 1, 3)) if ti == 0 else (2, (0, 1, 2, 3))
                assert [i for i in range(5) if sigma[Q[i]] != row[i]] == [h]
                hit = [c["name"] for c in components if h in c["support"]]
                options = [component_options(c, row) for c in components]
                bad = [c["name"] for c, o in zip(components, options) if not o["exact"]]
                bad_roots = {r: [c["name"] for c in components if c["root"] == r and c["name"] in bad]
                             for r in ROOTS}
                assert set(bad) <= set(hit) and len(hit) <= 2
                assert all(len(bad_roots[r]) <= 1 for r in ROOTS)
                if len(hit) == 2:
                    hit_roots["same_root" if hit[0][-1] == hit[1][-1] else "opposite_roots"] += 1
                if len(bad) == 2:
                    assert family in controls["double_nontransportable_types"]
                    assert all(len(bad_roots[r]) == 1 for r in ROOTS)
                    doubles[family] += 1
                for pl in placements:
                    for c in components:
                        if c["name"] in bad:
                            assert pl["component_spans"][c["name"]] >= 2
                    for r, typ in zip(ROOTS, family):
                        if bad_roots[r]:
                            assert pl["side_intervals"][r]["span"] >= controls["lambda_by_side"][typ]
                for o, old in zip(options, target["components"], strict=True):
                    assert o["exact"] == old["exact"]
                    assert set(o["options"]) == set(map(tuple, old["options"]))
                    assert len(old["options"]) == len(o["options"])
                root_lists = {r: U - {row[i] for i in source[r]["root_boundary"]} for r in ROOTS}
                R, anchor_R = dict(root_lists), dict(root_lists)
                for c, o in zip(components, options):
                    if o["exact"]:
                        R[c["root"]] -= set(o["options"][0])
                    if c["name"] not in hit:
                        assert sigma in o["permutations"]
                        anchor_R[c["root"]] -= {sigma[x] for x in c["Fq"]}
                assert prior["bad"] == bad and prior["hit"] == hit
                assert prior["fixed_base"] == set_dict(R) and prior["anchor_base"] == set_dict(anchor_R)
                # Full product, with unique ordered component F-tuples as the key.
                domain = set(product(*(o["options"] for o in options)))
                joins = target.get("joins", [target] if "forbidden_sets" in target else [])
                saved_keys = [tuple(map(tuple, j["forbidden_sets"])) for j in joins]
                assert len(saved_keys) == len(set(saved_keys)) == len(domain)
                assert set(saved_keys) == domain, (family, rec["id"], ti, "candidate domain changed")
                candidates, old_failures = [], []
                for ji, (join, Fs) in enumerate(zip(joins, saved_keys, strict=True)):
                    # Three independently arranged expressions, with the same named F values.
                    direct = {r: {a for a in U if all(a != row[h] for h in source[r]["root_boundary"])
                                      and all(a not in F for c, F in zip(components, Fs) if c["root"] == r)}
                              for r in ROOTS}
                    anchored = dict(anchor_R)
                    reduced = dict(R)
                    for c, F in zip(components, Fs):
                        if c["name"] in hit:
                            anchored[c["root"]] -= set(F)
                        if c["name"] in bad:
                            reduced[c["root"]] -= set(F)
                    assert direct == anchored == reduced
                    assert [sorted(direct[r]) for r in ROOTS] == join["residuals"]
                    pairs = sorted([a, b] for a, b in product(direct["z"], direct["w"]) if a != b)
                    assert pairs == join["root_pairs"]
                    label = classify(direct)
                    assert (label == "PASS") == bool(pairs)
                    candidate = dict(original_join_index=ji, F_by_component={c["name"]: F for c, F in zip(components, Fs)},
                                     E=set_dict(direct), classification=label)
                    candidates.append(candidate)
                    labels[label] += 1
                    family_labels[label] += 1
                    count["candidate_joins"] += 1
                    if label != "PASS":
                        cert = certificate(inputs, family, data, path, ri, ti, ji, join, aa_previous)
                        failure = dict(family=family, record_id=rec["id"], source_id=rec["source_id"],
                                       target=ti + 1, row=row, unknown_by_root=bad_roots,
                                       unknown_components=[c for c in components if c["name"] in bad],
                                       R=set_dict(R), exclusion_certificate=cert, **candidate)
                        candidate["failure_index"] = len(failures)
                        failures.append(failure)
                        old_failures.append(dict(Fs=[list(F) for c, F in zip(components, Fs) if c["name"] in bad],
                                                 residuals=set_dict(direct)))
                        count["failing_joins"] += 1
                assert sorted(map(digest, old_failures)) == sorted(map(digest, prior["candidate_failures"]))
                if old_failures:
                    count["queries_with_failing_joins"] += 1
                count["queries"] += 1
                nontransportable[len(bad)] += 1
                family_bad[len(bad)] += 1
                entry["targets"].append(dict(target=ti + 1, row=row, anchor=h, A_h=hit, D_p=bad_roots,
                                             R=set_dict(R), anchor_available=set_dict(anchor_R),
                                             components=options, candidates=candidates,
                                             previous_anchor=inputs.ref(anchor_path, old_anchor, f"/queries/{ai}"),
                                             inherited_final_status=final_targets[ti]["status"]))
            records.append(entry)
        assert count["retained_supports"] == expected
        assert count["queries"] == data["summary"]["target_queries"]
        families[family] = dict(count, nontransportable=dict(family_bad),
                                classifications={k: family_labels[k] for k in CLASSES})
        total.update(count)
    assert not anchors
    assert nontransportable == {0: 2936, 1: 1184, 2: 44}
    assert doubles == dict(AA=24, AB=12, AC=8)
    assert total["queries"] == 4164 and len(failures) == total["failing_joins"] == 434
    assert {k: families[k].get("failing_joins", 0) for k in FAMILIES} == dict(AA=160, AB=146, AC=8, AE=0, BB=120, BC=0, BE=0)
    assert hit_roots == dict(same_root=880, opposite_roots=1396)
    assert total["placements"] == old_anchor["summary"]["saved_placements_checked"]
    # Inputs must still be byte-identical after the replay, including old proof entries.
    for path, expected in inputs.hashes.items():
        assert sha256((ROOT / path).read_bytes()).hexdigest() == expected
    representatives = {label: next((i for i, f in enumerate(failures) if f["classification"] == label), None)
                       for label in CLASSES[:-1]}
    preserved_controls = {key: [i for i, f in enumerate(failures) if f["family"] == family
                               and f["record_id"] == rid and f["target"] == target]
                          for key, family, rid, target in [("AB22_p2", "AB", 22, 2), ("AA54_p1", "AA", 54, 1)]}
    assert all(preserved_controls.values())
    return dict(schema=1, scope="paper reduction plus finite interface replay; no new source exclusions, target accepts, disk realizability, repair theorem or Lean theorem",
                candidate_semantics="one ordered F tuple per retained record and literal target; preserve saved join indices; no symmetry or target deduplication",
                q=Q, targets=TARGETS, inputs_sha256=inputs.hashes,
                script_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                elementary_controls=controls, families=families,
                summary=dict(total, nontransportable=dict(nontransportable), double_nontransportable=doubles,
                             two_anchor_incident_roots=hit_roots, classifications={k: labels[k] for k in CLASSES}),
                representative_failure_indices=representatives, preserved_control_failure_indices=preserved_controls,
                records=records, failures=failures)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="compare bytes; never write inputs or output")
    args = parser.parse_args()
    data = build()
    raw = (json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()
    if args.check:
        assert OUT.read_bytes() == raw, f"stale certificate: {OUT}"
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_bytes(raw)
    print(json.dumps({k: data[k] for k in ("summary", "families", "representative_failure_indices",
                                         "preserved_control_failure_indices")}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
