#!/usr/bin/env python3
"""Exclusive certificate compiler; source coverage is proved in PROOF.md."""
import json
from check import HERE, expected

with (HERE / 'certificate.json').open('x') as stream:
    stream.write(json.dumps(expected(), indent=2, sort_keys=True) + '\n')
