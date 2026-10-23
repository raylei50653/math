#!/usr/bin/env python3
"""Exclusive certificate compiler; mathematical coverage is in PROOF.md."""
import json
from check import HERE,expected

data=expected()
with (HERE/'certificate.json').open('x') as stream:
    stream.write(json.dumps(data,indent=2,sort_keys=True)+'\n')
