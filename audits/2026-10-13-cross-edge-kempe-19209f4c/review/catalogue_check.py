#!/usr/bin/env python3
"""Independent finite catalogue and abstract one-swap calibration; stdlib only."""
from itertools import combinations, product
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'frozen/audits/2026-10-12-cofacial-uniform-separation-eb6b2303/controls/certificate.v2.json'


def partitions(items):
    if not items:
        yield ()
        return
    first, *rest = items
    for parts in partitions(rest):
        yield ((first,),) + parts
        for i in range(len(parts)):
            yield parts[:i] + ((first,) + parts[i],) + parts[i+1:]


def main():
    raw = SOURCE.read_bytes()
    data = json.loads(raw)
    keys = sorted(map(int, data['catalogue']['witness_recolouring']))
    assert len(keys) == 132
    targets = {}
    for target in (933, 941):
        supersets = [s for s in keys if s & target == target]
        new = [s & ~target for s in supersets]
        common = 1023
        for mask in new:
            common &= mask
        assert common == 0
        targets[str(target)] = {
            'catalogue_supersets': supersets,
            'new_masks': new,
            'intersection_new_rows': common,
            'rejected_patterns': [''.join(map(str, p)) for i, p in enumerate(data['pattern_order']) if not (target >> i) & 1],
        }

    # Abstract partitions encode only whether rim occurrences belong to the
    # same bichromatic component; boundary-hit flags are retained separately.
    # This is not a claim that every such partition is plane-realizable.
    wheel_cells = 0
    wheel_nonempty = 0
    proper_rims = 0
    for rim in product(range(4), repeat=5):
        if any(rim[i] == rim[(i+1) % 5] for i in range(5)):
            continue
        proper_rims += 1
        a_class = next((i for i in range(5) if len(set(rim)) == 4 and rim[(i-1) % 5] == rim[(i+1) % 5]), None)
        t_class = next((i for i in range(5) if len(set(rim)) == 3 and rim.count(rim[i]) == 1), None)
        for i in range(5):
            for old_unequal, opposite_unequal in product((0, 1), repeat=2):
                actual = [centre for centre in range(4)
                          if all(centre != rim[j] for j in range(5) if j != i)
                          and int(centre != rim[i]) == old_unequal
                          and int(rim[(i-1) % 5] != rim[(i+1) % 5]) == opposite_unequal]
                if (old_unequal, opposite_unequal) == (0, 0):
                    predicted = a_class == i
                elif (old_unequal, opposite_unequal) == (0, 1):
                    predicted = a_class in ((i+2) % 5, (i+3) % 5) or t_class == i
                elif (old_unequal, opposite_unequal) == (1, 0):
                    predicted = t_class in ((i+2) % 5, (i+3) % 5)
                else:
                    predicted = t_class in ((i-1) % 5, i, (i+1) % 5)
                assert len(actual) == int(predicted), (rim, i, old_unequal, opposite_unequal, actual)
                wheel_cells += 1
                wheel_nonempty += bool(actual)
    assert proper_rims == 240

    checked = 0
    escapes = 0
    rim4 = 0
    for rim in product(range(4), repeat=5):
        if len(set(rim)) != 4 or any(rim[i] == rim[(i+1) % 5] for i in range(5)):
            continue
        rim4 += 1
        singleton = {i for i in range(5) if rim.count(rim[i]) == 1}
        for x, y in combinations(range(4), 2):
            occurs = tuple(i for i in range(5) if rim[i] in (x, y))
            required_edges = [(i, (i+1) % 5) for i in range(5)
                              if rim[i] in (x, y) and rim[(i+1) % 5] in (x, y)]
            for parts in partitions(occurs):
                component = {i: k for k, part in enumerate(parts) for i in part}
                if any(component[i] != component[j] for i, j in required_edges):
                    continue
                for hits_boundary in product((False, True), repeat=len(parts)):
                    for k, part in enumerate(parts):
                        swapped = tuple((x+y-value if i in part else value) for i, value in enumerate(rim))
                        actual = not hits_boundary[k] and len(set(swapped)) == 3
                        singleton_pair = len(occurs) == 2 and set(occurs) <= singleton
                        predicted = (singleton_pair
                                     and (occurs[0]-occurs[1]) % 5 not in (1, 4)
                                     and component[occurs[0]] != component[occurs[1]]
                                     and not hits_boundary[k])
                        assert actual == predicted, (rim, x, y, parts, hits_boundary, k)
                        checked += 1
                        escapes += actual
    assert rim4 == 120
    print(json.dumps({
        'frozen_certificate_sha256': hashlib.sha256(raw).hexdigest(),
        'catalogue_size': len(keys),
        'targets': targets,
        'abstract_wheel_four_cell_control': {
            'proper_literal_rims': proper_rims,
            'rim_spoke_four_cell_cases': wheel_cells,
            'nonempty_cells_with_unique_centre': wheel_nonempty,
            'status': 'triggered and holds',
        },
        'abstract_one_swap_control': {
            'rim4_literal_colourings': rim4,
            'component_partition_boundary_flag_swap_cases': checked,
            'escapes': escapes,
            'status': 'triggered and holds',
            'realizability': 'abstract partitions are calibration only',
        },
        'target_minimum_source': 'not triggered',
    }, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
