#!/usr/bin/env python3
"""Shared-endpoint mixed K2, t_w=0 and (1,1,1): six spans on five edges.

The arbitrary-size cover is a paper annulus/Gallai argument. These finite
records certify necessary constraints, not disk realizations or a Lean theorem.
"""
import argparse
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path

from c5_adjacent_degree5_mixed_edge_shared import allowed, forbidden, schemas_for
from c5_adjacent_degree5_mixed_edge_shared_t1_pair import stable, stable_schema_ids
from c5_single_spoke_cores import Q, U, PERMS, PI, RHO

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts/c5_adjacent_degree5_mixed_edge_shared/observations.json"
OUT = ROOT / "artifacts/c5_adjacent_degree5_mixed_edge_shared_t0_singles/observations.json"
TABLE = OUT.with_name("exclusion_table.md")
NAMES = ("Cz", "Cw0", "Cw1", "Cw2", "u", "v")
SINGLETON_ORDERS = tuple(permutations(range(3)))
SUPPORTS = tuple(s for n in range(1, 6) for s in combinations(range(5), n))


def hulls(support):
    for start in support:
        span = max((i - start) % 5 for i in support)
        mask = sum(1 << ((start + j) % 5) for j in range(span))
        yield start, span, mask


def support_catalogue():
    result = []
    for size in (1, 2):
        for ban in combinations(range(4), size):
            supports = [s for s in SUPPORTS if len({Q[i] for i in s}) >= 2 and stable(s, ban)]
            lower = min(span for s in supports for _, span, _ in hulls(s))
            assert lower == (2 if ban == (3,) else 1)
            result.append(dict(forbidden=ban, supports=supports, min_span=lower))
    assert [s for s in SUPPORTS if stable(s, (3,))] == [
        s for s in SUPPORTS if len({Q[i] for i in s}) == 3]
    return result


def geometries():
    """Ordered lifts with gaps and shared endpoints allowed before saturation."""
    choices = {k: tuple(s for n in range(1, 6) for s in combinations(range(6), n)
                        if (len(s) == 1 if k == "u" else len(s) == 2 if k == "v" else len(s) >= 2)
                        and max(s) - min(s) < 5) for k in NAMES}
    result = {}
    for indices in SINGLETON_ORDERS:
        forward = ("Cz",) + tuple(f"Cw{i}" for i in indices) + ("u", "v")
        for reverse in (False, True):
            order = ("Cz",) + tuple(reversed(forward[1:])) if reverse else forward

            def visit(j, end, assigned):
                if j == len(NAMES):
                    for anchor in range(5):
                        supports = tuple(tuple(sorted((anchor + i) % 5 for i in assigned[k])) for k in NAMES)
                        result.setdefault(supports, []).append(dict(
                            order=order, anchor=anchor,
                            lifts={k: tuple(anchor + i for i in assigned[k]) for k in NAMES}))
                    return
                name = order[j]
                for support in choices[name]:
                    if min(support) >= end and (j or min(support) == 0):
                        visit(j + 1, max(support), assigned | {name: support})
            visit(0, 0, {})
    return result


def independent_geometries():
    """Disjoint hull masks first; recover the diamond order afterwards."""
    choices = tuple((s, h) for s in SUPPORTS if len(s) >= 2 for h in hulls(s))
    packed, found = {}, set()

    def visit(items, used):
        if len(items) == 5:
            supports = tuple(s for s, _ in items)
            assert supports not in packed
            packed[supports] = tuple(h for _, h in items)
            return
        for support, hull in choices:
            if not used & hull[2]:
                visit(items + ((support, hull),), used | hull[2])
    visit((), 0)
    for ss, hs in packed.items():
        cycle = tuple(sorted(range(5), key=lambda j: hs[j][0]))
        start = cycle.index(0)
        cycle = cycle[start:] + cycle[:start]
        if cycle[-1] == 4:
            u = hs[4][0]
        elif cycle[1] == 4:
            u = (hs[4][0] + hs[4][1]) % 5
        else:
            continue
        found.add((*ss[:4], (u,), ss[4]))
    assert len(packed) == 120
    return found, len(packed)


def source_key(r):
    return tuple(r[k] for k in ("h", "e", "d")) + (
        tuple(r["z"]["forbidden"][0]), tuple(f[0] for f in r["w"]["forbidden"]))


def bind_sources(inherited):
    records = [r for r in inherited["abstract_relations"]
               if r["w"]["ports"] == [1, 1, 1] and not r["w"]["spokes_colors"]]
    reconstructed = set()
    for h, e, d in permutations(range(3)):
        for fz in ((h,), tuple(sorted((h, d))), tuple(sorted((h, 3)))):
            for bans in permutations(sorted(U - {e})):
                reconstructed.add((h, e, d, fz, bans))
    assert len(records) == len(reconstructed) == 108
    assert {source_key(r) for r in records} == reconstructed
    for r in records:
        assert r["planar_necessary_retained"] and r["z"]["ports"] == [2]
        assert not r["z"]["spokes_colors"] and r["w"]["residual"] == [r["e"]]
        assert r["w_contact_relations"] == [[[f[0]]] for f in r["w"]["forbidden"]]
        assert len(schemas_for(set(r["z"]["forbidden"][0]))) == r["z_schema_count"]
    return records


def contact_words(placement):
    result = []
    for pair in (("zx0", "zx1"), ("zx1", "zx0")):
        expansion = dict(Cz=pair, Cw0=("wy0",), Cw1=("wy1",), Cw2=("wy2",),
                         u=("u_boundary",), v=("v_boundary_first", "v_boundary_last"))
        result.append(tuple(edge for unit in placement["order"] for edge in expansion[unit]))
    return result


def build():
    inherited = json.loads(SOURCE.read_text())
    assert sha256(SOURCE.read_bytes()).hexdigest() == "6b9b689c1f45b22feb182958c953b18989fe47655f69d5d2a17d8ed509555532"
    assert sha256((ROOT / "scripts/c5_adjacent_degree5_mixed_edge_shared.py").read_bytes()).hexdigest() == inherited["source_sha256"]
    for path, expected in inherited["inputs_sha256"].items():
        assert sha256((ROOT / path).read_bytes()).hexdigest() == expected, path
    abstract, catalogue, geometry = bind_sources(inherited), support_catalogue(), geometries()
    independent, packed_count = independent_geometries()
    assert set(geometry) == independent
    assert len(geometry) == sum(map(len, geometry.values())) == 60
    positive = ((0, 1), (1, 2), (2, 3), (3, 4), (4,), (0, 4))
    crossing = ((0, 2), (1, 2), (2, 3), (3, 4), (4,), (0, 4))
    assert positive in geometry and crossing not in geometry
    assert all(len(s) == (1 if k == "u" else 2) for ss in geometry for k, s in zip(NAMES, ss))
    lower = {tuple(c["forbidden"]): c["min_span"] for c in catalogue}
    sources = {source_key(r): r for r in abstract}
    geometries_out = [dict(id=i, supports=ss, placements=ps,
                           ordered_contact_words=[contact_words(p) for p in ps])
                      for i, (ss, ps) in enumerate(sorted(geometry.items()))]
    geometry_ids = {g["supports"]: g["id"] for g in geometries_out}
    for g in geometries_out:
        reflected = tuple(tuple(sorted(RHO[i] for i in s)) for s in g["supports"])
        g["reflected_id"] = geometry_ids[reflected]
        g["permuted_singleton_ids"] = [geometry_ids[(g["supports"][0],
            *(g["supports"][j + 1] for j in p), *g["supports"][4:])] for p in SINGLETON_ORDERS]
    records, frame_checks = [], 0
    for src in abstract:
        h, e, d, fz, fw = source_key(src)
        kind, key = ("singleton", str(fz[0])) if len(fz) == 1 else ("pair", str(fz))
        schemas = inherited["two_contact_schemas"][kind][key]
        third = fw.index(3) + 1
        spans = {k: lower[tuple(f)] for k, f in zip(NAMES[:4], [fz] + [(c,) for c in fw])}
        spans.update(u=0, v=1)
        assert sum(spans.values()) == 6 > 5
        checks = []
        for g in geometries_out:
            ss = g["supports"]
            missing = sorted({0, 1, 2} - {Q[i] for i in ss[third]})
            assert missing and not stable(ss[third], (3,))
            sigma = list(range(4))
            sigma[3], sigma[missing[0]] = missing[0], 3
            assert all(sigma[Q[i]] == Q[i] for i in ss[third])
            assert [[sigma[c] for c in t] for t in src["w_contact_relations"][third - 1]] != [[3]]
            failures = [k for k, s, f in zip(NAMES[:4], ss[:4], [fz] + [(c,) for c in fw])
                        if len({Q[i] for i in s}) < 2 or not stable(s, tuple(f))]
            assert NAMES[third] in failures
            mixed_ok = Q[ss[4][0]] == h and {Q[i] for i in ss[5]} == {h, e}
            checks.append(dict(geometry_id=g["id"], failed_unary_supports=failures,
                               mixed_q_support_matches=mixed_ok, missing_q_colors=missing,
                               support_fixing_permutation=sigma,
                               z_stable_schema_ids=stable_schema_ids(schemas, ss[0])))
        reflected = sources[(PI[h], PI[e], PI[d], tuple(sorted(PI[c] for c in fz)), tuple(PI[c] for c in fw))]
        local_ids = [r["id"] for r in inherited["actual_K2_supports"]
                     if all(r[k] == src[k] for k in ("h", "e", "d"))]
        assert local_ids
        for sigma in PERMS:
            ez, ew = U - {sigma[c] for c in fz}, U - {sigma[c] for c in fw}
            x, y = U - {sigma[h]}, U - {sigma[h], sigma[e]}
            assert ew == {sigma[e]} and not allowed(ez, ew, forbidden(x, y))
            assert sigma[3] not in {sigma[c] for c in Q}
            frame_checks += 1
        records.append(dict(source_id=src["id"], source_record=src, z_schema_key=(kind, key),
                            local_K2_support_ids=local_ids, third_color_component=NAMES[third],
                            span_lower_bounds=spans, total_span_lower_bound=6, boundary_length=5,
                            reason="six_required_spans_on_five_boundary_edges", support_record_ids=[],
                            geometry_checks=checks, reflected_source_id=reflected["id"],
                            permuted_singleton_source_ids=[sources[(h, e, d, fz, tuple(fw[j] for j in p))]["id"]
                                                          for p in SINGLETON_ORDERS]))
    by_id = {r["source_id"]: r for r in records}
    for r in records:
        assert by_id[r["reflected_source_id"]]["reflected_source_id"] == r["source_id"]
        for p, rid in zip(SINGLETON_ORDERS, r["permuted_singleton_source_ids"]):
            assert tuple(by_id[rid]["span_lower_bounds"][k] for k in NAMES[1:4]) == tuple(
                r["span_lower_bounds"][NAMES[j + 1]] for j in p)
    paths = [SOURCE, Path(__file__)] + [ROOT / "scripts" / f"{name}.py" for name in (
        "c5_adjacent_degree5_mixed_edge_shared", "c5_adjacent_degree5_mixed_edge_shared_t1_pair", "c5_single_spoke_cores")]
    paths += [ROOT / "docs" / f"{name}.md" for name in (
        "c5_adjacent_degree5_mixed_edge_shared_t0_singles", "c5_adjacent_degree5_mixed_edge_shared",
        "c5_adjacent_degree5_mixed_edge_shared_t0_pair_single", "c5_adjacent_degree5_mixed_edge_shared_t1_singles")]
    return dict(schema=1, scope="paper source exclusion and finite necessary supports; no target acceptance, realization or Lean theorem",
                inputs_sha256={str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in paths},
                inherited_inputs_sha256=inherited["inputs_sha256"],
                summary=dict(inherited_abstract_records=108, source_excluded_by_span=108,
                             necessary_support_records=0, empty_abstract_fibers=108,
                             minimum_required_span=6, boundary_length=5, support_geometries=60,
                             placement_witnesses=60, independent_five_unit_packings=packed_count,
                             source_geometry_comparisons=108 * 60, reflected_sources=108,
                             named_singleton_permutation_checks=108 * 6, reflected_geometries=60,
                             common_frame_q_checks=frame_checks, target_queries=0, T4_used=False,
                             root_spokes_used=False, new_pair_K5_exclusions=0),
                support_catalogue=catalogue, inherited_two_contact_schemas=inherited["two_contact_schemas"],
                singleton_permutations=SINGLETON_ORDERS, geometries=geometries_out, records=records,
                geometry_controls=dict(shared_endpoints_positive=positive, interleaving_negative=crossing))


def table(data):
    lines = ["# 共鄰端點 mixed K2：t_w=0、(1,1,1) 的來源排除", "",
             "原 108 筆逐一綁定；跨度至少 6 > 5，全部排除，不需 T4。", "",
             "60 份同序幾何是必要支援控制，不是 disk 實現；target 查詢數為零。", "",
             "| 原 ID | h/e/d | Fz | Fw0/Fw1/Fw2 | 禁 3 的原分量 | Cz/Cw0/Cw1/Cw2/u/v 跨度下界 | 反射原 ID |",
             "| ---: | --- | --- | --- | --- | --- | ---: |"]
    for r in data["records"]:
        s = r["source_record"]
        spans = "/".join(str(r["span_lower_bounds"][k]) for k in NAMES)
        lines.append(f"| {s['id']} | {s['h']}/{s['e']}/{s['d']} | {s['z']['forbidden'][0]} | "
                     f"{s['w']['forbidden']} | {r['third_color_component']} | {spans} | {r['reflected_source_id']} |")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = build()
    for path, payload in ((OUT, json.dumps(result, indent=2, sort_keys=True) + "\n"), (TABLE, table(result))):
        if args.check:
            assert path.read_bytes() == payload.encode(), f"certificate differs: {path}"
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(payload)
    print(json.dumps(result["summary"], sort_keys=True))


if __name__ == "__main__":
    main()
