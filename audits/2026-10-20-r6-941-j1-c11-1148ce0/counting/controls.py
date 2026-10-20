#!/usr/bin/env python3
"""Read-only positive/negative controls for the compact integer balance."""
from pathlib import Path
import copy
import importlib.util
import json

D=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("compact_balance",D/"balance.py")
b=importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)


def main():
    data=b.model()
    original=json.loads((D/"balance-certificate.json").read_text())
    b.verify(original,data)
    reordered=copy.deepcopy(original)
    reordered["half_row_weights"].reverse()
    b.verify(reordered,data)
    corruptions=[]
    changed=copy.deepcopy(original)
    pos=next(r for r in changed["half_row_weights"] if r["weight"]==1)
    neg=next(r for r in changed["half_row_weights"] if r["weight"]==-1)
    pos["weight"]=-1
    neg["weight"]=1
    corruptions.append(("swap_two_signs_preserving_64_68_totals",changed))
    changed=copy.deepcopy(original)
    changed["short_witness_ids"][0]+=1
    corruptions.append(("change_actual_witness",changed))
    changed=copy.deepcopy(original)
    changed["half_row_weights"].pop()
    corruptions.append(("omit_halfrow",changed))
    changed=copy.deepcopy(original)
    changed["half_row_weights"][0]["literal"][0]=3
    corruptions.append(("change_literal_frame",changed))
    records=[]
    for name,changed in corruptions:
        try:
            b.verify(changed,data)
        except AssertionError as exc:
            records.append({"name":name,"rejected":True,"reason":str(exc)})
        else:
            raise AssertionError(("accepted corrupt certificate",name))
    print(json.dumps({
        "status":"PASS",
        "original_valid":True,
        "reordered_semantically_identical_rows_valid":True,
        "negative_controls":records,
        "numeric_solver_used":False,
    },sort_keys=True))


if __name__=="__main__":
    main()
