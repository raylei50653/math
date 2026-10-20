#!/usr/bin/env python3
"""Independent verification of the union K23(s) U K23(t) involution."""
import argparse
import json
from pathlib import Path

from check import D, OLD, allowed, noncrossing, partitions, proper


def switched(u, p):
    chosen = {p[6], p[9]}
    return tuple(5 - value if value in (2, 3) and p[i] in chosen else value
                 for i, value in enumerate(u))


def calculate():
    frozen = json.loads((OLD / "J2/certificate.json").read_text())
    states = [u for u in partitions(10, 4) if proper(u)]
    index = {u: i for i, u in enumerate(states)}
    all_parts = [p for p in partitions(10) if noncrossing(p)]
    targets = {tuple(row["literal_core"]): row for row in frozen["forms"]}
    records = []
    for u, row in targets.items():
        pair_parts = allowed(u, (0, 1), all_parts, index, set(frozen["live"]))
        assert set(pair_parts) == {
            tuple(p["partition"]) for p in row["pair_records"][0]["partitions"]}
        outputs = []
        for p in pair_parts:
            out = switched(u, p)
            assert out in targets
            assert out[6] == out[9] == 5 - u[6]
            assert out[7:9] == u[7:9]
            assert switched(out, p) == u
            # Check inverse partition remains explicitly allowed at the target.
            assert p in {
                tuple(p["partition"])
                for p in targets[out]["pair_records"][0]["partitions"]}
            if row["family"] == 3:
                assert targets[out]["family"] == 3
                assert out[:6] == u[:6]
            else:
                assert targets[out]["family"] in (1, 2)
                assert out[4] == u[4] == 3
                assert p[4] not in {p[6], p[9]}
            outputs.append({"partition": list(p), "target": list(out),
                            "target_family": targets[out]["family"],
                            "selected_component_count": len({p[6], p[9]})})
        records.append({"source": list(u), "family": row["family"],
                        "partition_outputs": outputs})
    return {"status": "PASS", "map": "switch distinct 23 components meeting {s,t} once",
            "fibres": len(records),
            "partitions": sum(len(r["partition_outputs"]) for r in records),
            "records": records,
            "identity": "N01021(J2)=2*sum(six literal d=2 complete F fibre counts)",
            "source_realized": False, "last_rejection": "OPEN"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--certificate", type=Path, default=D / "j2-transport-certificate.json")
    args = parser.parse_args()
    result = calculate()
    if args.build:
        with args.certificate.open("x") as stream:
            json.dump(result, stream, indent=2)
            stream.write("\n")
    else:
        assert json.loads(args.certificate.read_text()) == result
    print(json.dumps({key: value for key, value in result.items() if key != "records"},
                     sort_keys=True))


if __name__ == "__main__":
    main()
