#!/usr/bin/env python3
"""Exclusive-create the exhaustive local-star audit transcript.

This compiler invokes the local exhaustive enumerator.  Independence is from
the immutable earlier certificates: no new local-star verdict or source
completion is imported from them.  check.py reconstructs every recorded row
and also checks the complete preserved predecessor and frozen bytes.
"""
import json
from pathlib import Path
import check

HERE = Path(__file__).resolve().parent

if __name__ == '__main__':
    check.custody()
    record = check.expected()
    with (HERE / 'certificate.json').open('x') as handle:
        json.dump(record, handle, indent=2, sort_keys=True)
        handle.write('\n')
    print(json.dumps(dict(status='CREATED', full_star_trials=len(record['complete_original_star_trials']))))
