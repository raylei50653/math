#!/usr/bin/env python3
"""Create deliberately invalid certificates exclusively; never edit good input."""
import copy
import gzip
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'controls/certificate.json.gz'


def main():
    original = json.loads(gzip.decompress(SOURCE.read_bytes()))
    fixtures = []

    def emit(name, candidate, reason):
        payload = (json.dumps(candidate, sort_keys=True, separators=(',', ':')) + '\n').encode()
        encoded = gzip.compress(payload, mtime=0)
        with (HERE / (name + '.json.gz')).open('xb') as handle:
            handle.write(encoded)
        fixtures.append(dict(name=name, path='negative/' + name + '.json.gz',
                             reason=reason, sha256=hashlib.sha256(encoded).hexdigest()))

    c = copy.deepcopy(original)
    ti = c['graphs'][0]['rows'][0]['r3_tau_indices'].pop(0)
    c['graphs'][0]['r3_support'].remove([0, ti])
    emit('drop_true_r3', c, 'Delete a genuine three-color cell from both support indices.')

    c = copy.deepcopy(original)
    ti = next(t for t, cell in enumerate(c['graphs'][0]['rows'][0]['cells'])
              if cell and len(set(c['tau_domain'][t])) == 4)
    c['graphs'][0]['rows'][0]['r3_tau_indices'].append(ti)
    c['graphs'][0]['rows'][0]['r3_tau_indices'].sort()
    c['graphs'][0]['r3_support'].append([0, ti])
    c['graphs'][0]['r3_support'].sort()
    emit('promote_four_colors', c, 'Claim an actual four-color H fibre is center-extendible.')

    c = copy.deepcopy(original)
    c['graphs'][0]['rows'][0]['r3_tau_indices'].append(274)
    c['graphs'][0]['rows'][0]['r3_tau_indices'].sort()
    c['graphs'][0]['r3_support'].append([0, 274])
    c['graphs'][0]['r3_support'].sort()
    emit('mix_beta_tau_marginals', c, 'Add beta0/tau274 by joining two different actual cells.')

    c = copy.deepcopy(original)
    row = c['graphs'][-1]['rows'][0]
    cell = next(cell for cell in row['cells'] if len(cell) == 2)
    cell.pop()
    row['h_count'] -= 1
    emit('drop_private_lift', c, 'Keep support but erase one private assignment of a two-element fibre.')

    c = copy.deepcopy(original)
    row = c['graphs'][0]['rows'][0]
    source = row['cells'][275]
    normalized_tau = [0, 1, 0, 1, 2]
    index = c['tau_domain'].index(normalized_tau)
    row['cells'][index] = [lift[:5] + normalized_tau for lift in source]
    row['cells'][275] = []
    emit('normalize_u_alone', c, 'Independently normalize U and thereby violate original spoke edges.')

    c = copy.deepcopy(original)
    witness = c['witnesses']['separate_quotient_row_join']
    witness['common_h_lifts'] = witness['left_all_h_lifts'][:1]
    emit('mix_equality_witnesses', c, 'Pretend a left-only equality witness is a common witness.')

    c = copy.deepcopy(original)
    transfer = c['pair_controls']['directional_selectors'][0]['rows'][0]['transfers'][0]
    target = next(g for g in c['graphs'] if g['id'] ==
                  c['pair_controls']['directional_selectors'][0]['target_graph'])
    ci = target['g_vertices'].index(c['v'])
    transfer['target_g_lift'][ci] = transfer['target_g_lift'][5]
    emit('wrong_center_transfer', c, 'Change the selected center to a neighbor color.')

    c = copy.deepcopy(original)
    c['graphs'][0]['h_faces'][-1].reverse()
    emit('reverse_inner_slot', c, 'Reverse only the inner face while retaining all other darts and rotations.')

    with (HERE / 'fixtures.json').open('x') as handle:
        json.dump(dict(source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                       fixtures=fixtures), handle, indent=2)
        handle.write('\n')
    print(json.dumps(dict(fixtures=len(fixtures), source_unchanged=True)))


if __name__ == '__main__':
    main()
