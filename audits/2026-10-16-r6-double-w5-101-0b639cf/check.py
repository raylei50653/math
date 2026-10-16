#!/usr/bin/env python3
"""Exact finite sector algebra and complete local W5 matching fibres.

This does not verify the arbitrary-size source geometry or realize a source.
"""
import argparse
import hashlib
from itertools import product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def require(ok, message):
    if not ok:
        raise ValueError(message)


def custody():
    base = json.loads((HERE / 'BASE.json').read_text())
    for row in base['prior_audits']:
        require(hashlib.sha256((REPO / row['path']).read_bytes()).hexdigest()
                == row['sha256'], 'prior audit drift: ' + row['path'])
    for row in base['frozen_inputs']:
        require(hashlib.sha256((HERE / row['frozen_path']).read_bytes()).hexdigest()
                == row['sha256'], 'frozen input drift: ' + row['path'])
        if not row['path'].startswith(('docs/', 'README')):
            require(hashlib.sha256((REPO / row['path']).read_bytes()).hexdigest()
                    == row['sha256'], 'live authority drift: ' + row['path'])
    return len(base['prior_audits'])


def word_data(bits, final_singleton=False):
    if any(bits[i:i+2] == (0, 0) for i in range(len(bits)-1)):
        return None
    if final_singleton and bits[-2:] == (1, 1):
        return None
    runs = []
    i = 0
    while i < len(bits):
        if bits[i] == 0:
            i += 1
            continue
        j = i
        while j < len(bits) and bits[j] == 1:
            j += 1
        if j-i > 2:
            return None
        if not (final_singleton and j == len(bits)):
            runs.append(j-i)
        i = j
    return {'word': ''.join(map(str, bits)),
            'singletons': runs.count(1), 'wheels': runs.count(2)}


def sectors(kind):
    result = []
    for degree in range(6, 9) if kind == 'm' else range(4, 11):
        for inner in product((0, 1), repeat=degree-4):
            bits = (0,) + inner + ((0,) if kind == 'm' else (1,))
            row = word_data(bits, final_singleton=kind == 'z')
            if row is None:
                continue
            row['degree'] = degree
            offset = 3 if kind == 'm' else 4
            require(degree-offset == 2*row['singletons']+3*row['wheels'],
                    'sector count identity')
            result.append(row)
    return result


def sector_table():
    ms, zs = sectors('m'), sectors('z')
    preliminary_m = []
    for s, t in product(ms, repeat=2):
        nm = s['wheels']+t['wheels']
        if nm > 2:
            continue
        for overlap in range(2):
            if nm == 2 and overlap != 1:
                continue
            epsilon = int(nm == 1)
            if overlap+epsilon > 1:
                continue
            delta = 2*(1-overlap-epsilon)
            parity_m = 1 ^ (nm % 2)
            degree_m = s['degree']+t['degree']-5
            excess_m = degree_m-(8-parity_m)
            if excess_m < 0 or excess_m % 2 or excess_m > delta:
                continue
            require(excess_m == delta, 'all excess must be at m')
            preliminary_m.append({'s': s, 't': t, 'n_m': nm,
                                  'overlap': overlap, 'delta': delta,
                                  'degree_m': degree_m, 'excess_m': excess_m})
    require(len(preliminary_m) == 4, 'four oriented preliminary m types')
    z_candidates = []
    for a, c in product(zs, repeat=2):
        h = a['degree']+c['degree']-8
        nz = a['wheels']+c['wheels']
        if not 3 <= h <= 6 or nz > 1:
            continue
        if h+3 != 6+(1 ^ nz):
            continue
        inherited_h3_ok = h != 3 or (a['degree'], c['degree']) in ((5, 6), (6, 5))
        z_candidates.append({'a': a, 'c': c, 'n_z': nz, 'h': h,
                             'passes_inherited_h3_source_theorem': inherited_h3_ok})
    require(len(z_candidates) == 5, 'five preliminary z types')
    survivors = []
    for m in preliminary_m:
        if m['n_m'] == 2:  # Paper degree-four corner argument, not a computed topology.
            continue
        for z in z_candidates:
            if not z['passes_inherited_h3_source_theorem']:
                continue
            if m['s']['wheels'] and z['c']['degree'] == 4:
                continue  # beta=q cannot be on a wheel, by the paper f lemma.
            if m['t']['wheels'] and z['a']['degree'] == 4:
                continue  # alpha=p cannot be on a wheel.
            location = 'none' if m['n_m'] == 0 else ('s' if m['s']['wheels'] else 't')
            prefix = 'I' if location == 'none' else 'II-'+location
            name = prefix+'-'+str(z['a']['degree'])+str(z['c']['degree'])
            survivors.append({'type': name,
                              'original_degrees_s_t_a_c': [m['s']['degree'], m['t']['degree'],
                                                          z['a']['degree'], z['c']['degree']],
                              'm_wheel': location, 'm_words': [m['s']['word'], m['t']['word']],
                              'z_words': [z['a']['word'], z['c']['word']],
                              'original_degrees_v_w_p_q': [5 if location == 's' else 6,
                                                           5 if location == 't' else 6, 6, 6],
                              'h': z['h'], 'delta': m['delta'], 'wheel_overlap': 0})
    survivors.sort(key=lambda r: r['type'])
    require(len(survivors) == 7, 'seven final oriented sector types')
    return {'m_words': ms, 'z_words': zs, 'preliminary_m': preliminary_m,
            'preliminary_z': z_candidates, 'necessary_types': survivors}


def wheel_fibres():
    # Face i has boundary port i. Internal dual edges (i,i+1) are literal spokes.
    # F0=upq,F1=uqA,F2=uAB,F3=uBC,F4=uCp, spokes uA and uC are (1,2),(3,4).
    edges = [(i, (i+1) % 5) for i in range(5)]
    cells = []
    for mask in range(32):
        ports = [i for i in range(5) if mask & (1 << i)]
        lifts = []
        for selected in product((0, 1), repeat=5):
            counts = [int(i in ports) for i in range(5)]
            lift = []
            for use, (u, v) in zip(selected, edges):
                if use:
                    counts[u] += 1
                    counts[v] += 1
                    lift.append(sorted((u, v)))
            if counts == [1]*5:
                lifts.append(sorted(lift))
        cells.append({'ports': ports, 'all_internal_lifts': sorted(lifts)})
    require(len(cells) == 32, 'complete boundary port relation')
    empty = sum(not row['all_internal_lifts'] for row in cells)
    require(empty == 21, 'retain all 21 empty matching fibres')
    fcell = next(row for row in cells if row['ports'] == [0])
    require(fcell['all_internal_lifts'] == [[[1, 2], [3, 4]]], 'forced f-port spokes')
    return {'labelled_faces': ['upq', 'uqA', 'uAB', 'uBC', 'uCp'],
            'cells': cells, 'empty_cells': empty,
            'total_internal_lifts': sum(len(row['all_internal_lifts']) for row in cells),
            'scope': 'literal local W5 with boundary half-edges, not a whole source'}


def corner_words():
    rows = []
    for spoke in (1, 2, 3):
        valid = []
        for bits in product((0, 1), repeat=4):
            if bits[:2] != (0, 0) or (bits[spoke], bits[(spoke+1) % 4]) != (1, 1):
                continue
            if all(bits[i] != bits[(i+1) % 4] for i in range(4) if i not in (0, spoke)):
                valid.append(''.join(map(str, bits)))
        rows.append({'wheel_spoke_position': spoke, 'valid_words': valid})
    require(rows == [{'wheel_spoke_position': 1, 'valid_words': []},
                     {'wheel_spoke_position': 2, 'valid_words': ['0011']},
                     {'wheel_spoke_position': 3, 'valid_words': []}], 'opposite corner transitions')
    return rows


def compute():
    return {'schema': 'R6-DOUBLE-W5-101-finite-algebra-v1',
            'scope': 'exact finite sector algebra and complete local matching fibres',
            'source_coverage': {'status': 'not triggered', 'genuine_sources': 0,
                                'source_exclusion_by_this_checker': False},
            'paper_inputs_not_proved_by_enumeration': [
                'actual source sector rotations and inherited degree bounds',
                'common-111 saturation on the same graph',
                'Euler curvature identity and common-rim exclusion',
                'original double-low return theorem and f-singleton conclusion',
                'adopted original h=3 collar source classification'],
            'sectors': sector_table(), 'corner_words': corner_words(),
            'complete_local_W5_matching_fibres': wheel_fibres()}


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--write', type=Path)
    group.add_argument('--check', type=Path)
    args = parser.parse_args()
    prior = custody()
    data = compute()
    if args.write:
        with args.write.open('x') as stream:
            json.dump(data, stream, indent=2, sort_keys=True)
            stream.write('\n')
    else:
        require(json.loads(args.check.read_text()) == data, 'certificate mismatch')
    print(json.dumps({'status': 'PASS', 'necessary_sector_types': 7,
                      'complete_local_matching_cells': 32, 'empty_local_matching_cells': 21,
                      'prior_audit_files_unchanged': prior,
                      'source_coverage': 'not triggered', 'paper_proof_verified': False}, sort_keys=True))


if __name__ == '__main__':
    main()
