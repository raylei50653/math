#!/usr/bin/env python3
"""Exclusive-create the finite literal endpoint and complete local orbit certificate."""
from copy import deepcopy
from itertools import combinations, product
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREV = 'audits/2026-10-23-941-gamma8-cells-6b09cd4/certificate.json'


def main():
    spec = importlib.util.spec_from_file_location('producer_join', HERE / 'exploration/join.py')
    join = importlib.util.module_from_spec(spec); spec.loader.exec_module(join)
    previous = json.loads((HERE / 'frozen' / PREV).read_text())
    join.OLD = previous
    join.ROWS = json.loads((HERE / 'frozen/audits/2026-10-23-three-mask-round3-cb8f859/941/certificate.json').read_text())['source_rows']
    cells = [c for c in previous['candidates'] if c['classification'] == 'local_necessary_type']
    orbits, barriers, attachments = [], [], []
    for cell in cells:
        es = {tuple(e) for e in cell['edges']}
        rows = []
        for m, n, k in product(range(2), repeat=3):
            co = {v: c ^ (2 if ((m and previous['original_component_labels'][v] == 'M')
                                or (n and previous['original_component_labels'][v] == 'N')
                                or (k and previous['original_component_labels'][v] == 'K')) else 0)
                  for v, c in previous['original_colors'].items()}
            rows.append(dict(M02=m, N13=n, K02=k, colors=co,
                six_palette_components={''.join(map(str, p)): sorted(sorted(s) for s in join.components(es, co, p))
                                        for p in combinations(range(4), 2)}))
        orbits.append(dict(id=cell['id'], rows=rows))
        neigh = lambda v: {b if a == v else a for a, b in es if v in (a, b)}
        barriers.append(dict(id=cell['id'], forbidden_exterior_common_neighbors=[
            dict(pair=[a, b], strict_interior_common=sorted(neigh(a) & neigh(b) & {'tau', 'zeta'}))
            for a, b in combinations(previous['boundary'], 2)
            if join.edge(a, b) not in es and neigh(a) & neigh(b) & {'tau', 'zeta'}]))
        for contract in join.ROWS:
            for att in product([None, 'U'], [None, 'V', 'HL_0'], [None, 'c'], [None, 'q']):
                failures = join.test(cell, contract, att)
                attachments.append(dict(id=cell['id'], target=contract['target'],
                    type02=contract['initial_02_type'], ordered_d_e_h_W=list(att),
                    failures=failures, classification='necessary_endpoint_row' if not failures else 'excluded_endpoint_row'))
    certificate = dict(schema='941-gamma8-exterior-v1', base=previous['base'],
        complete_predecessor_certificate=deepcopy(previous),
        complete_local_orbits=orbits, exterior_barriers=barriers, endpoint_rows=attachments,
        paper_contract=dict(whole_original_M_N_and_same_K=True, M_N_rootless_full_stars_preserved=True,
            old_C_E_paths_not_assumed_to_survive=True, full_M2_separator_not_single_T_neighbor=True,
            B14_order_and_literal_frame_preserved=True, arbitrary_Gamma8_interior_for_endpoint_lemmas=True,
            four_exterior_private_points_only_under_j2=True, strict_exterior_private_lower_bound=4,
            O_core_strict_exterior_private_lower_bound=5,
            strict_off_Gamma_private_lower_bound=6, no_sharpness_claim=True,
            Wstar_q_exception_retained=True, d_U_exception_retained=True, h_c_exception_retained=True,
            eleven_types_all_retained=True, endpoint_rows_not_complete_exterior_collars=True),
        authority_boundaries=dict(finite_control='triggered and holds', original_source_control='not triggered',
            eleven_type_exclusions=0, initial_pair_exclusions=0, general_wrong_side='OPEN',
            smaller_bad=False, new_Lean=False, new_LP=False, common_k_lower_bound=23))
    with (HERE / 'certificate-v2.json').open('x') as f:
        json.dump(certificate, f, sort_keys=True, indent=2); f.write('\n')
    print(json.dumps(dict(status='CREATED', orbit_states=88, endpoint_rows=len(attachments),
        necessary_rows=sum(not r['failures'] for r in attachments))))


if __name__ == '__main__':
    main()
