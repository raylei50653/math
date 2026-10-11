#!/usr/bin/env python3
"""Read-only independent delivery custody, S4 arithmetic and pin metadata check.

No worker modules are imported. No source graphs or assignments are enumerated.
The original incomplete coverage classification is reported as requiring an
acceptance overlay, rather than silently being upgraded to complete metadata.
"""
from collections import Counter
from copy import deepcopy
from itertools import combinations, permutations, product
import hashlib
import json
from pathlib import Path
import stat
import subprocess

REVIEW = Path(__file__).resolve().parent
TARGET = REVIEW.parent / "2026-10-11-n45-s-long-s-t2-q2-restore"
REPO = TARGET.parent.parent
BASE = "f2692089ad4259808e27d9b7e882ac09505b180a"
BETA = (0, 1, 2, 0, 1)
Q = ((0, 1, 2, 1, 2), (0, 1, 2, 0, 2), BETA, (0, 1, 0, 2, 1), (0, 1, 0, 1, 2))
SUPPORTS = {"U": (0, 1, 2), "L": (2, 3, 4), "S": (4, 0)}
SCHEDULES = (("933", "0123"), ("933", "0124"), ("933", "0234"),
             ("933", "1234"), ("941", "023"), ("941", "024"), ("941", "124"))
PINS = list(product(range(4), repeat=2))
UNTRIGGERED = {"executed": False, "trigger_count": None, "status": "not triggered"}


def require(condition, label):
    if not condition:
        raise ValueError(label)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(relative):
    return json.loads((TARGET / relative).read_text())


def regular_bytes(path):
    require(stat.S_ISREG(path.lstat().st_mode), "not a regular file: " + str(path))
    return path.read_bytes()


def tree_snapshot():
    result = {}
    for path in sorted(TARGET.rglob("*")):
        mode = path.lstat().st_mode
        relative = str(path.relative_to(TARGET))
        if stat.S_ISDIR(mode):
            result[relative] = {"type": "directory"}
        elif stat.S_ISREG(mode):
            data = path.read_bytes()
            result[relative] = {"type": "file", "bytes": len(data), "sha256": sha(data)}
        else:
            raise ValueError("symlink or special file: " + relative)
    return result


def git(*args):
    return subprocess.check_output(["git", *args], cwd=REPO)


def custody(tree):
    delivery = read("delivery.json")
    exclusions = delivery["metadata_exclusions"]
    require(exclusions == ["delivery.json", "seal-receipt.json"], "exact root metadata exclusions")
    files = {key: value for key, value in tree.items() if value["type"] == "file"}
    payload = delivery["payload"]
    paths = [record["path"] for record in payload]
    require(len(paths) == len(set(paths)), "duplicate payload path")
    require(set(paths) == set(files) - set(exclusions), "exact payload set")
    for record in payload:
        require(not Path(record["path"]).is_absolute() and ".." not in Path(record["path"]).parts,
                "payload path scope")
        require(files[record["path"]] == {"type": "file", "bytes": record["bytes"], "sha256": record["sha256"]},
                "payload hash: " + record["path"])
    require(len(payload) == delivery["payload_files"] == 90, "payload count")
    require(sum(record["bytes"] for record in payload) == delivery["payload_bytes"] == 5015240, "payload bytes")
    inputs = read("inputs.json")
    dispatch_path = REPO / inputs["dispatch_source"]
    dispatch = json.loads(regular_bytes(dispatch_path))
    require(len(inputs["inputs"]) == len(dispatch["inputs"]) == 23, "authority input count")
    require({r["path"] for r in inputs["inputs"]} == {r["path"] for r in dispatch["inputs"]}, "dispatch input set")
    counts = Counter()
    for record in inputs["inputs"]:
        counts[record["authority"]] += 1
        original = next(r for r in dispatch["inputs"] if r["path"] == record["path"])
        require(all(record[key] == value for key, value in original.items()), "dispatch record preservation")
        frozen = regular_bytes(TARGET / record["local_frozen_path"])
        require(sha(frozen) == record["sha256"] and len(frozen) == record["bytes"], "frozen authority hash")
        require(regular_bytes(REPO / record["path"]) == frozen, "live authority bytes")
        require(regular_bytes(dispatch_path.parent / record["frozen_path"]) == frozen, "dispatch frozen bytes")
        if record["authority"] == "BASE Git blob":
            require(git("show", BASE + ":" + record["path"]) == frozen, "BASE blob bytes")
            require(git("rev-parse", BASE + ":" + record["path"]).decode().strip() == record["git_blob"], "BASE blob identity")
        else:
            require(record["authority"] == "sealed audit physical SHA256", "unknown authority type")
            require(record["git_blob"] is None and record["included_in_BASE_claimed"] is False, "sealed is not BASE")
    require(dict(counts) == {"BASE Git blob": 12, "sealed audit physical SHA256": 11}, "authority separation")
    external = inputs["external_theorem_pins"]
    require(len(external) == 1, "external theorem pin count")
    for record in external:
        frozen = regular_bytes(TARGET / record["local_frozen_path"])
        require(sha(frozen) == record["sha256"] and len(frozen) == record["bytes"], "external PDF pin")
        require(regular_bytes(REPO / record["path"]) == frozen, "external original bytes")
        require(record["origin_refetched"] is False and "not BASE Git blob" in record["authority"], "external authority boundary")
    before, after = read("custody-before.json"), read("custody-after.json")
    require(before == after, "before/after custody equality")
    frequency = Counter(record["path"] for record in before["files"])
    require(len(before["files"]) == 1037 and len(frequency) == 1036, "custody records versus distinct files")
    duplicate = {path: count for path, count in frequency.items() if count > 1}
    require(duplicate == {"audits/2026-10-11-n45-s-long-s-fibre/external/gallai.pdf": 2}, "exact duplicate custody record")
    for record in before["files"]:
        require(sha(regular_bytes(REPO / record["path"])) == record["sha256"], "old-file live drift: " + record["path"])
    head = git("rev-parse", "HEAD").decode().strip()
    diff_hash = sha(git("diff", "--binary", "HEAD"))
    require(head == before["head"] == BASE, "current HEAD")
    require(diff_hash == before["tracked_diff_sha256"] == sha(b""), "current tracked diff")
    missing = []
    require(len(inputs["missing_BASE_findings"]) == 2, "missing BASE finding count")
    for record in inputs["missing_BASE_findings"]:
        native = subprocess.run(["git", "show", BASE + ":" + record["path"]], cwd=REPO, capture_output=True)
        require(native.returncode == 128 and not native.stdout, "missing BASE blob")
        require(record["authority_admitted"] is False and record["replay_executed"] is False, "missing blob excluded")
        missing.append({"path": record["path"], "native_exit": native.returncode})
    receipt = read("seal-receipt.json")
    delivery_sha = sha(regular_bytes(TARGET / "delivery.json"))
    require(receipt["delivery_sha256"] == delivery_sha and receipt["exit_code"] == 0, "receipt binds current manifest")
    require(delivery["target_source"] == UNTRIGGERED, "delivery target-source boundary")
    return {
        "delivery_sha256": delivery_sha, "payload_files": len(payload), "payload_bytes": delivery["payload_bytes"],
        "regular_files": len(files), "directories": len(tree) - len(files), "symlinks": 0, "special_files": 0,
        "metadata_exclusions": exclusions, "authority_counts": dict(counts), "external_theorem_pins": 1,
        "custody_records": 1037, "custody_distinct_files": 1036, "duplicate_custody_record": duplicate,
        "authority_live_frozen_BASE_match": True, "old_files_live_zero_drift": True,
        "HEAD": head, "tracked_diff_sha256": diff_hash, "missing_BASE_blobs": missing,
    }


def algebra():
    certificate, coverage = read("calibration.json"), read("coverage.json")
    literals = sorted("".join(map(str, row)) for row in product(range(4), repeat=5)
                      if row[0] == 0 and all(row[i] != row[(i + 1) % 5] for i in range(5))
                      and all(row[j] <= max(row[:j]) + 1 for j in range(1, 5)))
    require(len(literals) == 10, "ten normalized proper C5 boundary rows")
    queries = []
    for literal in literals:
        for piece, support in SUPPORTS.items():
            maps = [list(perm) for perm in permutations(range(4))
                    if all(perm[BETA[i]] == int(literal[i]) for i in support)]
            queries.append({"literal": literal, "piece": piece, "ordered_support": list(support),
                            "beta_query": [BETA[i] for i in support], "query": [int(literal[i]) for i in support],
                            "colour_maps": maps})
    require(queries == certificate["queries"], "independent S4 query maps")
    partitions = []
    for pair in combinations(range(4), 2):
        s_bad = set(pair)
        partitions.append({"S_beta_forbidden_r": sorted(s_bad), "L_beta_forbidden_r": sorted(set(range(4)) - s_bad),
                           "satisfies_proved_S_r0_r1_nonempty": not bool(s_bad & {0, 1})})
    require(partitions == certificate["beta_two_colour_partitions"], "six beta partitions")
    require(sum(row["satisfies_proved_S_r0_r1_nonempty"] for row in partitions) == 1, "unique surviving partition")
    transports, slices = [], []
    for q in (3, 4):
        literal = "".join(map(str, Q[q]))
        maps = {}
        for piece, seed in (("L", (2, 3)), ("S", (0, 3))):
            support = SUPPORTS[piece]
            candidates = [perm for perm in permutations(range(4)) if perm[3] == 3
                          and all(perm[BETA[i]] == int(literal[i]) for i in support)
                          and [perm[value] for value in seed] == [0, 3]]
            require(len(candidates) == 1, "unique proof transport")
            maps[piece] = list(candidates[0])
            require({(candidates[0][a], candidates[0][b]) for a, b in PINS} == set(PINS), "full ordered pin bijection")
        transports.append({"target_q": q, "literal": literal, "L_colour_map": maps["L"], "S_colour_map": maps["S"],
                           "L_beta_pins": [2, 3], "S_beta_pins": [0, 3], "target_pins": [0, 3],
                           "gamma_b4": Q[q][4], "restores_e": True})
        require([Q[q][i] for i in SUPPORTS["U"]] == [0, 1, 0], "target U actual query")
        require(Q[q][0] == Q[q][2] == 0 and Q[q][4] != 0, "actual retained spokes and original e colour")
        l_bad = {maps["L"][a] for a in (0, 1)}
        s_bad = {maps["S"][a] for a in (2, 3)}
        require(set(range(4)) - (l_bad | s_bad) == {0}, "complete s3 slice")
        slices.append({"q": q, "L_forbidden_r": sorted(l_bad), "S_forbidden_r": sorted(s_bad), "s3_nonempty_r": [0]})
    require(transports == certificate["proof_transports"], "proof transport metadata")
    require(certificate["source_relation_values"] is None and certificate["source_preimage_counts"] is None,
            "no source relation or preimage counts supplied")
    require(certificate["target_source"] == UNTRIGGERED, "calibration target-source boundary")
    schedules = coverage["schedules"]
    expected_pairs = {(orbit, tuple(map(int, mask))) for orbit, mask in SCHEDULES}
    require(len(schedules) == 7 and {(s["Sigma_orbit"], tuple(s["QG"])) for s in schedules} == expected_pairs, "exact schedule domain")
    cells = diagonals = new_nonempty = new_empty = contradictions = 0
    selected = Counter()
    u_known = Counter()
    u_by_literal = {}
    for schedule in schedules:
        require(schedule["beta_q"] == 2 and schedule["beta_literal"] == "01201", "original beta identity")
        require(schedule["Delta"] == [q for q in schedule["QG"] if q != 2], "full original Delta")
        require(schedule["Delta_literals"] == ["".join(map(str, Q[q])) for q in schedule["Delta"]], "literal Delta")
        require(schedule["original_s_spoke_variants"] == [[0, 2]], "same-source spoke variant")
        restored = [q for q in (3, 4) if q in schedule["Delta"]]
        selected_q = 4 if 4 in restored else 3
        require(schedule["selected_restored_row"] == selected_q, "selected restoration row")
        require([proof["q"] for proof in schedule["restored_rows"]] == restored, "all proved Delta rows")
        require(not schedule["remaining_schedule_obligations"], "assigned schedule residual")
        selected[selected_q] += 1
        for proof in schedule["restored_rows"]:
            require(proof["pins"] == [0, 3] and proof["gamma_b4"] == Q[proof["q"]][4], "full restore pin coordinates")
        rows = schedule["all_ten_literal_obligations"]
        require([row["literal"] for row in rows] == literals, "all ten coverage rows")
        for row in rows:
            literal = tuple(map(int, row["literal"]))
            q = Q.index(literal) if literal in Q else None
            require(row["q"] == q and row["gamma_b4"] == literal[4], "literal q/b4 identity")
            require(len(row["pins"]) == 16 and {(p["r"], p["s"]) for p in row["pins"]} == set(PINS), "complete ordered pin positions")
            for pin in row["pins"]:
                a, b = pin["r"], pin["s"]
                require(pin["diagonal"] == (a == b), "diagonal flag")
                require(all(pin[key] is None for key in ("counts", "all_preimages", "contact_tuples", "full_assignments", "full_lifts")), "symbolic rather than actual values")
                require(pin["G_edge_filter_empty"] == (a == literal[4]), "original rb4 filter")
                require(pin["G_row_rejection_empty"] == (q in schedule["QG"]), "original full G rejection")
                expected_contradiction = q in (3, 4) and q in schedule["Delta"] and (a, b) == (0, 3)
                require(pin["contradiction"] == expected_contradiction, "same-frame restoration contradiction")
                if q in (3, 4) and b == 3:
                    expected_derivation = "nonempty full fibre" if a == 0 else "empty full fibre"
                    require(pin["new_paper_fibre_derivation"] == expected_derivation, "new full s3 fibre derivation")
                    new_nonempty += a == 0
                    new_empty += a != 0
                if [literal[i] for i in SUPPORTS["U"]] == [0, 1, 2] and b == 1:
                    state = "old_empty" if pin["X_necessary_under_true_source"] == "empty" else "new_empty_required"
                    u_known[state] += 1
                    by_literal = u_by_literal.setdefault(row["literal"], Counter())
                    by_literal[state] += 1
                    if state == "new_empty_required":
                        require(q is None and row["literal"] in ("01203", "01213", "01231", "01232"), "precise U omission domain")
                        require(pin["necessary_empty_reasons"] == [] and b not in {literal[0], literal[2]}, "new emptiness rather than reason-only addition")
                cells += 1
                diagonals += a == b
                contradictions += expected_contradiction
    require((cells, diagonals, new_nonempty, new_empty, contradictions) == (1120, 280, 14, 42, 9), "symbolic pin/fibre metadata counts")
    require(dict(selected) == {3: 2, 4: 5}, "selected coverage count")
    require(dict(u_known) == {"old_empty": 84, "new_empty_required": 112}, "U identity coverage omissions")
    wrong_map = read("negative-controls/wrong-L-map.json")
    expected_bad = deepcopy(certificate)
    expected_bad["proof_transports"][1]["L_colour_map"] = [0, 2, 1, 3]
    require(wrong_map == expected_bad, "exact wrong-map negative-control mutation")
    wrong_diagonal = read("negative-controls/missing-diagonal.json")
    expected_bad = deepcopy(certificate)
    expected_bad["schedules"][0]["ambient_cells"][0]["pins"].remove([3, 3])
    require(wrong_diagonal == expected_bad, "exact missing-diagonal mutation")
    # Also independently check the certificate's ambient grid and domain.
    require({(s["orbit"], tuple(s["QG"])) for s in certificate["schedules"]} == expected_pairs, "calibration schedules")
    for schedule in certificate["schedules"]:
        require([r["literal"] for r in schedule["ambient_cells"]] == literals, "calibration rows")
        for row in schedule["ambient_cells"]:
            require(row["pins"] == [list(pin) for pin in PINS] and row["gamma_b4"] == int(row["literal"][4]), "calibration ambient cells")
    return {
        "literal_rows": literals, "row_piece_queries": 30, "S4_query_comparisons": 720,
        "matching_colour_maps": sum(len(query["colour_maps"]) for query in queries),
        "query_map_count_histogram": dict(Counter(len(query["colour_maps"]) for query in queries)),
        "beta_partitions": 6, "surviving_partition": {"S": [2, 3], "L": [0, 1]},
        "proof_transports": transports, "complete_proof_pin_maps": 64, "new_s3_slices": slices,
        "schedules": 7, "coverage_rows": 70, "ambient_pin_cells": cells, "diagonal_cells": diagonals,
        "symbolic_new_nonempty_cells": new_nonempty, "symbolic_new_empty_s3_cells": new_empty,
        "Delta_contradiction_cells": contradictions, "selected_restoration_counts": dict(selected),
        "negative_wrong_map_exact": {"q": 4, "piece": "L", "before": [1, 2, 0, 3], "after": [0, 2, 1, 3]},
        "negative_missing_diagonal_exact": {"schedule": "933/0123", "literal": "01012", "pin": [3, 3]},
        "coverage_overlay_required": True, "raw_coverage_complete_known_empty_classification": False,
        "U_s1_known_empty": dict(u_known), "U_s1_by_literal": {key: dict(value) for key, value in u_by_literal.items()},
        "new_U_empty_coordinates": {"schedules": [s["id"] for s in schedules],
                                    "literals": ["01203", "01213", "01231", "01232"], "r": [0, 1, 2, 3], "s": 1},
        "scope": "bounded literal/pin and symbolic full-fibre metadata; no actual assignments or preimage counts",
    }


def main():
    initial = tree_snapshot()
    custody_result = custody(initial)
    algebra_result = algebra()
    require(tree_snapshot() == initial, "target tree drift during independent check")
    print(json.dumps({"status": "passes with required coverage overlay", "custody": custody_result,
                      "algebra": algebra_result, "checker_imported": False,
                      "source_graphs_enumerated": 0, "old_19_controls_reexecuted": False,
                      "target_source": UNTRIGGERED, "target_tree_zero_drift": True}, sort_keys=True))


if __name__ == "__main__":
    main()
