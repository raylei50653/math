#!/usr/bin/env python3
"""Read-only connected replay of the J1 W5 C11 branch exclusion."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

D=Path(__file__).resolve().parent
COMMANDS=(
    ("inherited_source_zero_fibres",[
        "frozen/audits/2026-10-20-r6-941-j1-w5-9c36e3c/interface/check.py"]),
    ("literal_complete_caps",["review/check.py"]),
    ("compact_integer_balance",["counting/balance.py"]),
    ("independent_integer_separator",["review/dual_check.py","--certificate",
        "geometry/orbit-farkas-certificate.json"]),
)


def verify(rows,base):
    for row in rows:
        raw=(base/row["path"]).read_bytes()
        assert hashlib.sha256(raw).hexdigest()==row["sha256"],("sealed drift",row["path"])
        if "bytes" in row:
            assert len(raw)==row["bytes"],("sealed size drift",row["path"])


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--seal",type=Path,default=D/"OUTPUTS.json")
    args=ap.parse_args()
    inputs=json.loads((D/"INPUTS.json").read_text())
    outputs=json.loads(args.seal.read_text())
    verify(inputs,D/"frozen");verify(outputs,D)
    results=[]
    for name,relargs in COMMANDS:
        command=[sys.executable,"-B",str(D/relargs[0])]
        command += [str(D/a) if a.endswith(".json") else a for a in relargs[1:]]
        run=subprocess.run(command,capture_output=True,text=True)
        assert run.returncode==0,(name,run.stdout,run.stderr)
        try:
            events=[json.loads(run.stdout)]
        except json.JSONDecodeError:
            events=[json.loads(line) for line in run.stdout.splitlines() if line.strip()]
        assert events,("missing result",name)
        results.append({"checker":name,"result":events[-1],"progress":events[:-1]})
    verify(inputs,D/"frozen");verify(outputs,D)
    print(json.dumps({
        "status":"PASS","frozen_inputs":len(inputs),"sealed_outputs":len(outputs),
        "results":results,"n_ge_6_induced_C11_source_excluded":True,
        "original_W5_three_edge_branch_closed":True,
        "general_J1_J2_closed":False,"new_Lean":False,
    },sort_keys=True))


if __name__=="__main__":
    main()
