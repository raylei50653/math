#!/usr/bin/env python3
"""Check the actual output of the explicit LC axiom audit."""
import argparse
import hashlib
import json
from pathlib import Path
import re


def expected_names(source):
    namespaces = []
    names = []
    for line in source.splitlines():
        if line.startswith('namespace '):
            namespaces.extend(line.split()[1].split('.'))
        elif line.startswith('end '):
            count = len(line.split()[1].split('.'))
            del namespaces[-count:]
        elif line.startswith('#print axioms '):
            name = line.split()[-1]
            names.append(name if name.startswith('FiveBoundary.') else '.'.join(namespaces + [name]))
    return names


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--log', type=Path, required=True)
    parser.add_argument('--source', type=Path, default=Path('/tmp/math-m3-ba0b447/Math/ExcessTwoCertificatesAudit.lean'))
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    text = args.log.read_text()
    matches = re.findall(r"^'([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)", text, re.MULTILINE)
    names = expected_names(args.source.read_text())
    assert len(names) == 558 and len(set(names)) == 558
    assert [name for name, _ in matches] == names, 'missing, duplicate, or out-of-order axiom output'
    declarations = {name: [value.strip() for value in axioms.split(',') if value.strip()]
                    for name, axioms in matches}
    sorry = [name for name, axioms in declarations.items() if any('sorryAx' in ax for ax in axioms)]
    assert not sorry, sorry
    standard = {'propext', 'Classical.choice', 'Quot.sound'}
    unexpected = {name: [ax for ax in axioms if ax not in standard and '.native_decide.' not in ax]
                  for name, axioms in declarations.items()}
    unexpected = {name: axioms for name, axioms in unexpected.items() if axioms}
    assert not unexpected, unexpected
    groups = {}
    for suffix in ('positive', 'rejected', 'valid'):
        group = {name: axioms for name, axioms in declarations.items()
                 if name.startswith('FiveBoundary.ExcessTwo.Generated.cert_') and name.endswith('_' + suffix)}
        assert len(group) == 179, (suffix, len(group))
        native_counts = [sum('.native_decide.' in ax for ax in axioms) for axioms in group.values()]
        assert set(native_counts) == ({0} if suffix == 'positive' else {1}), (suffix, set(native_counts))
        if suffix != 'positive':
            for name, axioms in group.items():
                certificate = name.rsplit('.', 1)[-1].removesuffix('_' + suffix)
                assert [ax for ax in axioms if '.native_decide.' in ax] == [certificate + '_rejected._native.native_decide.ax_1'], name
        groups[suffix] = {'count': len(group), 'native_axioms_per_declaration': sorted(set(native_counts))}
    cover = declarations['FiveBoundary.color_orbits_cover']
    assert [ax for ax in cover if '.native_decide.' in ax] == ['color_orbits_cover._native.native_decide.ax_1']
    aggregate_counts = {name: sum('.native_decide.' in ax for ax in declarations[name])
                        for name in ('FiveBoundary.ExcessTwo.Generated.all_certificates_valid',
                                     'FiveBoundary.ExcessTwo.Generated.all_certificates_sound')}
    assert list(aggregate_counts.values()) == [179, 180]
    result = {'declaration_count': len(declarations), 'sorryAx': sorry,
              'unexpected_axioms': unexpected, 'groups': groups,
              'S4_cover_axioms': cover, 'aggregate_native_counts': aggregate_counts,
              'declarations': declarations,
              'source_sha256': hashlib.sha256(args.source.read_bytes()).hexdigest(),
              'log_sha256': hashlib.sha256(args.log.read_bytes()).hexdigest(),
              'trust_boundary': 'rejected/valid use native_decide; raw Sigma inherits S4 native cover; no enumeration completeness or topological disk theorem'}
    with args.output.open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(json.dumps({key: value for key, value in result.items() if key != 'declarations'}, sort_keys=True))


if __name__ == '__main__':
    main()
