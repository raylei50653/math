#!/usr/bin/env python3
"""Read-only T1 custody, bounded symbolic calibration and coverage check.

Worker modules are never imported. Minor graphs are fixed calibration
skeletons, not realizations of the research source contract. Raw coverage
omissions are reported without changing the delivered artifacts.
"""
from collections import Counter, deque
from copy import deepcopy
from itertools import combinations, permutations, product
import hashlib
import json
from pathlib import Path
import stat
import subprocess

TARGET = Path(__file__).resolve().parent.parent / "2026-10-11-n45-s-long-s-t1-rfibre"
REPO = TARGET.parent.parent
DISPATCH = REPO / "audits/2026-10-11-n45-s-long-s-rfibre-dispatch"
BASE = "f2692089ad4259808e27d9b7e882ac09505b180a"
COL = frozenset(range(4))
Q = ("01212", "01202", "01201", "01021", "01012")
UNTRIGGERED = {"executed": False, "trigger_count": None, "status": "not triggered"}


def require(condition, label):
    if not condition:
        raise ValueError(label)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def data(path):
    require(stat.S_ISREG(path.lstat().st_mode), "not regular file: " + str(path))
    return path.read_bytes()


def pin(path):
    value = data(path)
    return {"bytes": len(value), "sha256": sha(value)}


def read(name):
    return json.loads(data(TARGET / name))


def git(*args):
    return subprocess.check_output(["git", *args], cwd=REPO)


def snapshot():
    out = {}
    for path in sorted(TARGET.rglob("*")):
        mode = path.lstat().st_mode
        name = str(path.relative_to(TARGET))
        if stat.S_ISDIR(mode):
            out[name] = {"type": "directory"}
        elif stat.S_ISREG(mode):
            out[name] = {"type": "file", **pin(path)}
        else:
            raise ValueError("symlink/special file: " + name)
    return out


def custody(tree):
    delivery, inputs = read("delivery.json"), read("inputs.json")
    files = {name: record for name, record in tree.items() if record["type"] == "file"}
    require(delivery["metadata_exclusions"] == [{"path": "delivery.json", "reason": "Manifest self hash excluded."}], "root-only metadata exclusion")
    entries = delivery["files"]
    paths = [entry["path"] for entry in entries]
    require(len(paths) == len(set(paths)) == 54, "unique payload paths")
    require(set(paths) == set(files) - {"delivery.json"}, "exact payload set")
    for entry in entries:
        require(files[entry["path"]] == {"type": "file", "bytes": entry["bytes"], "sha256": entry["sha256"]}, "payload pin")
    require(sum(entry["bytes"] for entry in entries) == delivery["payload_bytes"] == 1938723, "payload byte count")
    require(delivery["payload_files"] == 54, "declared payload count")
    dispatch_pin = json.loads(data(DISPATCH / "input-pins.json"))
    require(inputs["dispatch_pin"] == pin(DISPATCH / "input-pins.json"), "dispatch pin")
    require(len(inputs["BASE_blobs"]) == 12 and len(inputs["sealed_audit_SHA256"]) == 11, "authority counts")
    records = inputs["BASE_blobs"] + inputs["sealed_audit_SHA256"]
    require({record["path"] for record in records} == {record["path"] for record in dispatch_pin["inputs"]}, "dispatch authority set")
    for record in records:
        original = next(r for r in dispatch_pin["inputs"] if r["path"] == record["path"])
        require(all(record[key] == value for key, value in original.items()), "preserved dispatch authority")
        expected = {"bytes": record["bytes"], "sha256": record["sha256"]}
        require(pin(REPO / record["path"]) == expected, "live authority pin")
        require(pin(REPO / record["dispatch_frozen_path"]) == expected, "frozen authority pin")
        if record["authority"] == "BASE Git blob":
            blob = git("show", BASE + ":" + record["path"])
            require(sha(blob) == record["sha256"] and len(blob) == record["bytes"], "BASE blob bytes")
            require(git("rev-parse", BASE + ":" + record["path"]).decode().strip() == record["git_blob"], "BASE blob identity")
        else:
            require(record["authority"] == "sealed audit physical SHA256", "sealed authority type")
            require(record["git_blob"] is None and record["included_in_BASE_claimed"] is False, "sealed authority is not BASE")
    require(len(inputs["external_theorem_pins"]) == 1, "external pin count")
    external = inputs["external_theorem_pins"][0]
    require(pin(REPO / external["path"]) == {"bytes": external["bytes"], "sha256": external["sha256"]}, "primary external PDF pin")
    require(external["git_blob"] is None and external["origin_refetched"] is False and "never BASE" in external["authority"], "external authority boundary")
    before, after = read("custody-before.json"), read("custody-after.json")
    require(len(before["immutable_inputs"]) == after["immutable_input_count"] == 49, "49 immutable distinct files")
    for path, record in before["immutable_inputs"].items():
        require(pin(REPO / path) == record, "immutable live input drift: " + path)
    require(after["immutable_input_drift"] == [] and after["protected_original_B_manifest_mismatches"] == [], "reported drift")
    require(before["HEAD"] == after["HEAD"] == git("rev-parse", "HEAD").decode().strip() == BASE, "current HEAD")
    require(before["tracked_diff_sha256"] == after["tracked_diff_sha256"] == sha(git("diff", "--binary", "HEAD")) == sha(b""), "current tracked diff")
    prior_root = REPO / "audits/2026-10-11-n45-s-long-s-fibre"
    prior_manifest_path = DISPATCH / "authority/sealed/audits/2026-10-11-n45-s-long-s-fibre/delivery.json"
    prior = json.loads(data(prior_manifest_path))
    require(data(prior_manifest_path) == data(prior_root / "delivery.json"), "original B manifest preserved")
    require(len(prior["files"]) == prior["file_count"] == after["protected_original_B_payload_files_verified"] == 846, "846 old B payload records")
    prior_paths = [record["path"] for record in prior["files"]]
    require(len(prior_paths) == len(set(prior_paths)), "old B unique paths")
    for record in prior["files"]:
        require(pin(prior_root / record["path"]) == {"bytes": record["bytes"], "sha256": record["sha256"]}, "old B payload drift")
    require(pin(prior_root / "certificate.json") == after["original_B_certificate"], "original B certificate identity")
    missing = []
    for finding in inputs["findings"]:
        native = subprocess.run(["git", "show", BASE + ":" + finding["path"]], cwd=REPO, capture_output=True)
        require(native.returncode == finding["git_exit"] == 128, "missing BASE native exit")
        require(finding["authority_admitted"] is False and finding["dependent_finite_replay"]["executed"] is False, "missing BASE excluded")
        missing.append({"path": finding["path"], "native_exit": native.returncode})
    require(len(missing) == 2, "missing BASE finding count")
    require(delivery["target_source"] == UNTRIGGERED, "target-source boundary")
    return {"delivery_sha256": sha(data(TARGET / "delivery.json")), "payload_files": 54,
            "payload_bytes": 1938723, "regular_files": len(files), "directories": len(tree) - len(files),
            "symlinks": 0, "special_files": 0, "metadata_exclusions": ["delivery.json"],
            "BASE_inputs": 12, "sealed_inputs": 11, "external_primary_PDFs": 1,
            "immutable_distinct_files": 49, "old_B_payload_files": 846,
            "all_authorities_and_old_files_zero_drift": True, "missing_BASE_blobs": missing}


def subsets(values):
    return [frozenset(part) for size in range(len(values) + 1) for part in combinations(values, size)]


def orbit(pair, fixed):
    return {frozenset(perm[value] for value in pair) for perm in permutations(range(4))
            if all(perm[value] == value for value in fixed)}


def normalized_edge(first, second):
    return tuple(sorted((first, second)))


def minor_check(edge_list, bag_list):
    edges = {normalized_edge(*edge) for edge in edge_list}
    bags = [set(bag) for bag in bag_list]
    require(len(bags) == 5 and all(bags), "five nonempty bags")
    require(len(set().union(*bags)) == sum(map(len, bags)), "disjoint bags")
    graph = {}
    for first, second in edges:
        graph.setdefault(first, set()).add(second)
        graph.setdefault(second, set()).add(first)
    disconnected = []
    for index, bag in enumerate(bags):
        queue = deque([min(bag)])
        reached = set(queue)
        while queue:
            for vertex in graph.get(queue.popleft(), set()) & bag - reached:
                reached.add(vertex)
                queue.append(vertex)
        if reached != bag:
            disconnected.append(index)
    missing, witnesses = [], []
    for first, second in combinations(range(5), 2):
        crossing = sorted(edge for edge in edges
                          if (edge[0] in bags[first] and edge[1] in bags[second])
                          or (edge[1] in bags[first] and edge[0] in bags[second]))
        if not crossing:
            missing.append([first, second])
        else:
            witnesses.append({"bags": [first, second], "original_edge": list(crossing[0])})
    return {"connected": not disconnected, "disjoint": True, "missing_adjacencies": missing,
            "disconnected_bags": disconnected, "adjacency_witnesses": witnesses}


def expected_path(kind, length, index):
    root = {"S": "r", "U": "s"}[kind]
    boundary = {normalized_edge("b" + str(i), "b" + str((i + 1) % 5)) for i in range(5)}
    vertices = ["x" + str(i) for i in range(length + 1)]
    edges = boundary | {normalized_edge(vertices[i], vertices[i + 1]) for i in range(length)}
    edges |= {normalized_edge(root, vertices[0]), normalized_edge(root, vertices[-1]),
              normalized_edge(root, "exterior"), normalized_edge("exterior", "b2" if kind == "S" else "b4")}
    left, right = vertices[index:index + 2]
    for vertex in (left, right):
        edges |= {normalized_edge(vertex, "b0"), normalized_edge(vertex, "b4" if kind == "S" else "b2")}
    last = {root, "exterior", *vertices} - {left, right}
    if kind == "S":
        last |= {"b1", "b2", "b3"}
        bags = [{left}, {right}, {"b0"}, {"b4"}, last]
    else:
        last |= {"b3", "b4"}
        bags = [{left}, {right}, {"b0"}, {"b1", "b2"}, last]
    return edges, bags


def expected_leaf(length):
    vertices = ["c" + str(i) for i in range(length)]
    edges = {normalized_edge("b" + str(i), "b" + str((i + 1) % 5)) for i in range(5)}
    edges |= {normalized_edge(vertices[i], vertices[(i + 1) % length]) for i in range(length)}
    edges |= {normalized_edge("c0", "path_root"), normalized_edge("path_root", "r"),
              normalized_edge("r", "exterior"), normalized_edge("exterior", "b2")}
    for vertex in ("c1", "c2"):
        edges |= {normalized_edge(vertex, "b0"), normalized_edge(vertex, "b4")}
    last = (set(vertices) - {"c1", "c2"}) | {"path_root", "r", "exterior", "b1", "b2", "b3"}
    return edges, [{"c1"}, {"c2"}, {"b0"}, {"b4"}, last]


def calibration():
    certificate = read("calibration-certificate.json")
    specification = read("calibration-input.json")
    require(specification["path_lengths"] == [1, 3, 5] and specification["leaf_cycle_lengths"] == [3, 5], "fixed minor calibration domain")
    require(specification["colours"] == [0, 1, 2, 3] and specification["permutations"] == "all 24 S4" and specification["graph_enumeration"] is False, "bounded palette domain")
    s_cases = {}
    for name in ("q3", "q4"):
        row = tuple(map(int, Q[int(name[-1])]))
        for support in subsets((0, 4)):
            for contact in (False, True):
                fixed = {row[i] for i in support} | ({1} if contact else set())
                for pair in combinations((0, 2, 3), 2):
                    s_cases[(name, tuple(sorted(support)), contact, pair)] = orbit(pair, fixed) == {frozenset(pair)}
    recorded_s = {(r["row"], tuple(r["actual_support"]), r["contains_fixed_s1_contact"], tuple(r["pair"])): r["stabilizer_holds"]
                  for r in certificate["S_palette_cases"]}
    require(recorded_s == s_cases and len(certificate["S_palette_cases"]) == 48, "48 independent S stabilizers")
    u_cases = {(tuple(sorted(support))): orbit((1, 3), {int(Q[1][i]) for i in support}) == {frozenset((1, 3))}
               for support in subsets((0, 1, 2))}
    require({tuple(r["actual_support"]): r["stabilizer_holds"] for r in certificate["U_palette_cases"]} == u_cases
            and len(certificate["U_palette_cases"]) == 8, "eight U stabilizers")
    beta_pairs = [list(pair) for pair in combinations((0, 2, 3), 2) if orbit(pair, {0, 1}) == {frozenset(pair)}]
    require(beta_pairs == [certificate["beta_q3_S_pair"]] == [[2, 3]], "unique beta S pair")
    widget_counts = []
    require(len(certificate["conditional_S_widget_queries"]) == 8, "eight widget queries")
    for widget in certificate["conditional_S_widget_queries"]:
        a, b = widget["r"], widget["s"]
        require(a in range(4) and b in (1, 3), "widget root pins")
        witnesses = [(u, v) for u, v in product(range(4), repeat=2)
                     if u != v and u not in {a, 0, 2} and v not in {a, b, 0}]
        require(witnesses and widget["one_conditional_template_witness"] == list(witnesses[0]), "conditional widget complete witness")
        widget_counts.append({"r": a, "s": b, "conditional_template_assignment_count": len(witnesses)})
    require({(w["r"], w["s"]) for w in widget_counts} == set(product(range(4), (1, 3))), "all widget pins")
    require(len(certificate["path_minor_skeletons"]) == 18 and len(certificate["leaf_minor_skeletons"]) == 2, "minor skeleton domain sizes")
    minor_results = []
    expected_path_ids = set(product(("S", "U"), (1, 3, 5)))
    recorded_ids = set()
    for record in certificate["path_minor_skeletons"]:
        kind, length, index = record["kind"], record["path_length"], record["chosen_edge_index"]
        require((kind, length) in expected_path_ids and index in range(length), "named path skeleton domain")
        recorded_ids.add((kind, length, index))
        edges, bags = expected_path(kind, length, index)
        require(record["edges"] == [list(e) for e in sorted(edges)] and record["bags"] == [sorted(b) for b in bags], "exact named path skeleton")
        checked = minor_check(record["edges"], record["bags"])
        require(checked["connected"] and not checked["missing_adjacencies"] and record["all_ten_original_adjacencies"], "path K5 bag witness")
        minor_results.append({"kind": kind, "length": length, "index": index, **checked})
    require(recorded_ids == {(kind, length, index) for kind, length in expected_path_ids for index in range(length)}, "all 18 path cases")
    for record in certificate["leaf_minor_skeletons"]:
        length = record["leaf_cycle_length"]
        require(length in (3, 5), "named leaf skeleton domain")
        edges, bags = expected_leaf(length)
        require(record["edges"] == [list(e) for e in sorted(edges)] and record["bags"] == [sorted(b) for b in bags], "exact named leaf skeleton")
        checked = minor_check(record["edges"], record["bags"])
        require(checked["connected"] and not checked["missing_adjacencies"] and record["all_ten_original_adjacencies"], "leaf K5 bag witness")
        minor_results.append({"kind": "leaf", "length": length, **checked})
    require({record["leaf_cycle_length"] for record in certificate["leaf_minor_skeletons"]} == {3, 5}, "both leaf lengths")
    good_edges, good_bags = expected_path("S", 1, 0)
    tether = minor_check([list(e) for e in good_edges - {normalized_edge("x0", "b4")}], good_bags)
    exterior = minor_check([list(e) for e in good_edges - {normalized_edge("r", "exterior")}], good_bags)
    require(tether["missing_adjacencies"] == [[0, 3]], "missing tether negative")
    require(exterior["disconnected_bags"] == [4] and not exterior["missing_adjacencies"], "missing exterior negative")
    require(certificate["negative_minor_skeletons"] == [
        {"case": "missing actual tether", "rejected": True, "reason": "missing adjacency"},
        {"case": "missing exterior connection", "rejected": True, "reason": "disconnected bag"}], "negative minor categories")
    corrupted = read("negative-corrupt-certificate.json")
    expected_bad = deepcopy(certificate)
    expected_bad["beta_q3_S_pair"] = [0, 2]
    require(corrupted == expected_bad, "exact corrupted certificate difference")
    require(certificate["target_source"] == UNTRIGGERED, "calibration source boundary")
    return {"S_palette_cases": 48, "U_palette_cases": 8, "S4_candidates_per_case": 24,
            "beta_q3_S_pair": [2, 3], "conditional_widget_queries": 8, "conditional_widget_counts": widget_counts,
            "path_minor_skeletons": 18, "leaf_minor_skeletons": 2, "connected_bags_checked": 100,
            "all_ten_adjacencies_per_minor": True, "total_adjacency_witnesses": 200,
            "minor_negative_failures": {"missing_tether": tether["missing_adjacencies"], "missing_exterior": exterior["disconnected_bags"]},
            "corrupted_certificate_exact_change": {"path": "beta_q3_S_pair", "before": [2, 3], "after": [0, 2]},
            "calibration_certificate_sha256": sha(data(TARGET / "calibration-certificate.json")),
            "scope": "fixed palette, conditional widget and minor skeleton calibration only"}


def coverage_check():
    coverage = read("coverage.json")
    prior = json.loads(data(DISPATCH / "authority/sealed/audits/2026-10-11-n45-s-long-s-fibre/obligations.json"))
    expected = {(s["SigmaG_orbit"], tuple(s["QG"]), s["beta_q"], h) for s in prior["schedules"] if s["t_s"] == 1 for h in (0, 2)}
    queries = coverage["queries"]
    require(len(queries) == 28 and len(expected) == 28, "28 source schedule/spoke queries")
    require({(q["SigmaG_orbit"], tuple(q["QG"]), q["beta_q"], q["original_s_spokes"][0]) for q in queries} == expected, "exact dispatched schedule/spoke domain")
    literals = sorted("".join(map(str, row)) for row in product(range(4), repeat=5)
                      if row[0] == 0 and all(row[i] != row[(i + 1) % 5] for i in range(5))
                      and all(row[j] <= max(row[:j]) + 1 for j in range(1, 5)))
    require(coverage["literal_order"] == literals and len(literals) == 10, "independent normalized boundary rows")
    require(len(coverage["C_ambient_template"]) == 64 and
            {(tuple(r["ordered_s_contact_tuple"]), r["original_r_colour"]) for r in coverage["C_ambient_template"]}
            == {(pair, a) for pair in product(range(4), repeat=2) for a in range(4)}, "full C tuple/r ambient domain")
    require(len(coverage["U_ambient_template"]) == 16 and
            {tuple(r["ordered_s_contact_tuple"]) for r in coverage["U_ambient_template"]} == set(product(range(4), repeat=2)), "full U contact tuple ambient domain")
    require(all(r["all_preimages"] is None for r in coverage["C_ambient_template"] + coverage["U_ambient_template"]), "no invented ambient preimages")
    totals = Counter()
    u_by_literal = {}
    g_by_literal = {}
    old_x_g_by_beta_spoke = Counter()
    t1_p22_spokes = []
    for query in queries:
        h = query["original_s_spokes"][0]
        beta = query["beta_q"]
        require(query["original_e"] == ["r", "b4"] and query["original_r_split"] == [2, 2] and query["profile"] == [1, 2, 2], "original coordinates/profile")
        require(query["beta_literal"] == Q[beta] and query["QX"] == [beta], "literal original beta")
        require(query["Delta"] == [q for q in query["QG"] if q != beta], "complete Delta")
        require(query["Delta_original_r_forcing"] == {str(q): int(Q[q][4]) for q in query["Delta"]}, "literal e forcing")
        if beta == 3:
            require(query["proved_restoration_rows"] == [0, 1], "q3 restoration rows")
            require(query["selected_Delta_restoration_row"] in set(query["Delta"]) & {0, 1} and query["source_minor"] is None, "selected restoration")
            totals["restoration_queries"] += 1
        else:
            require(beta == 4 and query["source_minor"] and query["selected_Delta_restoration_row"] is None, "q4 source minor")
            totals["minor_queries"] += 1
        if query["SigmaG_orbit"] == 941 and query["QG"] == [0, 1, 3] and beta == 3:
            require(query["selected_Delta_restoration_row"] == 0, "T1-P22 q0 restoration")
            t1_p22_spokes.append(h)
        require(query["actual_source"]["executed"] is False and query["actual_source"]["trigger_count"] is None and query["actual_source"]["preimages"] is None, "no actual source")
        rows = query["all_ten_literal_obligations"]
        require(["".join(map(str, row["literal"])) for row in rows] == literals, "ten rows each query")
        for row in rows:
            literal = row["literal"]
            q = Q.index("".join(map(str, literal))) if "".join(map(str, literal)) in Q else None
            require(row["q_position"] == q and row["gamma_b4"] == literal[4], "literal q/e coordinate")
            require(len(row["pins"]) == 16 and {(pin["r"], pin["s"]) for pin in row["pins"]} == set(product(range(4), repeat=2)), "all 16 ordered pins")
            totals["rows"] += 1
            for pin_record in row["pins"]:
                a, b = pin_record["r"], pin_record["s"]
                require(pin_record["source_preimages"] is None, "no supplied source preimages")
                old_x_empty = pin_record["X_fibre"].startswith("necessarily empty")
                old_g_empty = pin_record["G_fibre"].startswith("necessarily empty")
                basic_empty = q == beta or b == literal[h] or (q in query["QG"] and a != literal[4])
                require(not basic_empty or old_x_empty, "basic original beta/spoke/G-filter emptiness")
                if old_x_empty and not old_g_empty:
                    totals["old_X_to_new_G_empty_required"] += 1
                    old_x_g_by_beta_spoke[(beta, h)] += 1
                    g_by_literal.setdefault("".join(map(str, literal)), Counter())["old_X_to_new_G"] += 1
                if literal[:3] == [0, 1, 0] and b in (2, 3):
                    by_literal = u_by_literal.setdefault("".join(map(str, literal)), Counter())
                    state = "old_X_empty" if old_x_empty else "new_X_empty_required"
                    totals["U_identity_known_X_empty"] += 1
                    totals[state] += 1
                    by_literal[state] += 1
                    if not old_g_empty:
                        require(not old_x_empty, "disjoint new-U and old-X G corrections")
                        totals["new_U_to_new_G_empty_required"] += 1
                        by_literal["new_G_empty_required"] += 1
                        g_by_literal.setdefault("".join(map(str, literal)), Counter())["new_U_to_new_G"] += 1
                totals["pins"] += 1
                totals["diagonal_positions"] += a == b
    require((totals["restoration_queries"], totals["minor_queries"], totals["rows"], totals["pins"], totals["diagonal_positions"])
            == (14, 14, 280, 4480, 1120), "query and ambient pin counts")
    require(sorted(t1_p22_spokes) == [0, 2], "T1-P22 both original spokes")
    totals["new_G_empty_required"] = totals["old_X_to_new_G_empty_required"] + totals["new_U_to_new_G_empty_required"]
    require((totals["U_identity_known_X_empty"], totals["old_X_empty"], totals["new_X_empty_required"],
             totals["old_X_to_new_G_empty_required"], totals["new_U_to_new_G_empty_required"], totals["new_G_empty_required"])
            == (672, 320, 352, 540, 240, 780), "U010 identity and full X-to-G propagation omission counts")
    require(dict(old_x_g_by_beta_spoke) == {(3, 0): 135, (3, 2): 135, (4, 0): 135, (4, 2): 135}, "old X-to-G correction original domain")
    return {"schedules": 14, "original_spoke_variants": [0, 2], "queries": 28, **dict(totals),
            "C_ambient_slots": 64, "U_ambient_slots": 16, "T1_P22_covered_spokes": sorted(t1_p22_spokes),
            "coverage_overlay_required": True, "raw_complete_known_empty_classification": False,
            "U010_omissions_by_literal": {literal: dict(value) for literal, value in u_by_literal.items()},
            "G_empty_corrections_by_literal": {literal: dict(value) for literal, value in g_by_literal.items()},
            "old_X_to_G_correction_beta_spoke_counts": {str(key): value for key, value in old_x_g_by_beta_spoke.items()},
            "scope": "symbolic full-fibre obligations; actual source and preimage counts absent"}


def main():
    initial = snapshot()
    result = {"custody": custody(initial), "calibration": calibration(), "coverage": coverage_check()}
    require(snapshot() == initial, "target tree drift during review")
    print(json.dumps({"status": "passes with required coverage overlay", **result,
                      "worker_modules_imported": False, "target_tree_zero_drift": True,
                      "target_source": UNTRIGGERED, "old_19_controls_reexecuted": False,
                      "source_graphs_enumerated": 0}, sort_keys=True))


if __name__ == "__main__":
    main()
