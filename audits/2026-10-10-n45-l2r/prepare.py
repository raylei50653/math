#!/usr/bin/env python3
"""Freeze named inputs and emit a scoped independent paper judgment."""
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
WORKER = ROOT / 'audits/2026-10-10-n45-s-low2'
BASE = 'dc8e9aa7d6fccb51f63d30aa3f9c132296d44744'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def write(name, value):
    (HERE / name).write_text(json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + '\n')

assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() == BASE
dest = HERE / 'frozen/worker'
dest.parent.mkdir()
shutil.copytree(WORKER, dest, symlinks=True)
worker_files = []
for path in sorted(WORKER.rglob('*')):
    if path.is_file() and not path.is_symlink():
        relative = path.relative_to(WORKER).as_posix()
        assert (dest / relative).read_bytes() == path.read_bytes()
        worker_files.append({'path': relative, 'sha256': sha(path.read_bytes())})
    elif path.is_symlink():
        raise AssertionError('Unexpected worker symlink; stop rather than silently normalize')

base_inputs = json.loads((dest / 'base-inputs.json').read_text())
for item in base_inputs['inputs']:
    blob = subprocess.check_output(['git', 'show', BASE + ':' + item['path']], cwd=ROOT)
    assert sha(blob) == item['sha256']
    assert blob == (dest / 'frozen/BASE' / item['path']).read_bytes()
pins = json.loads((dest / 'inputs-initial.json').read_text())['pins']
for item in pins:
    assert sha((ROOT / item['path']).read_bytes()) == item['expected']
    assert (ROOT / item['path']).read_bytes() == (dest / 'frozen/current' / item['path']).read_bytes()

write('inputs.json', {
    'task': 'N45-L2R', 'BASE': BASE, 'worker': WORKER.relative_to(ROOT).as_posix(),
    'worker_files': worker_files, 'worker_file_count': len(worker_files),
    'BASE_inputs': base_inputs['inputs'], 'current_pins_initial': pins,
    'scope': 'All worker bytes copied; four BASE blobs checked against Git; eight live pins checked at audit start. Replay thereafter uses these frozen inputs, not mutable shared adoption documents.',
    'no_peer_judgments_read': True,
})

claims = json.loads((dest / 'claims.json').read_text())
proof = {
    'LOW2-CORE': 'Delete only rb_i. r retains rx1,rx2,rp_r,rq_r: degree_X(r)=4, no boundary spoke and no rs edge. s retains degree5. Every piece vertex keeps all its degree4 incident edges. X=M supplies its own beta minimality; original Sigma-criticality alone would not supply it.',
    'LOW2-COMP': 'C is the induced original union {r}+U+P+Q with exactly the piece internal edges and four retained r contacts. Three connected pieces each meet the same r, so C is the sole effective component. Both U contacts and every U path remain. s contacts are three distinct original neighbors ordered by inherited rotation, with shared root-contact vertices kept as one coordinate. degree_C(v)=4-d_B(v)-1[v in K], hence degree_C(r)=4.',
    'LOW2-JOIN': 'The same complete f_U must simultaneously satisfy f_U(x1)!=c and f_U(x2)!=c; its ordered pair fibres are not multiplied marginals. All piece assignments and the same r color c union bijectively to full C assignments. Phi_gamma(c,t) is defined for every c and all 64 ambient t, including empty fibres. A single shared original vertex supplies both r and s constraints. X lifts join one a in A_s(gamma) with C assignments avoiding a on all contacts; G adds exactly f(r)!=gamma(b_i) for every gamma. Isolated original vertices multiply both lift sets freely. Boundary lists give strict slack at all three K contacts, so unpinned R_C(gamma) is nonempty without claiming nonempty pinned fibres.',
    'LOW2-F': 'If the two s-spokes have the same beta color, deleting either leaves beta constraints unchanged and contradicts X minimality. With distinct u,v, rejection gives Col-{u,v} subset F. X minus each s-spoke has a full beta witness, necessarily using the released spoke color at s, giving complete C witnesses outside F. Thus F_C(beta)=Col-{u,v}, with nonempty R_C(beta).',
    'LOW2-MAP': 'BASE sections1-5 apply to X itself, with z=s and actual full boundary lists. Common S4 merely names two retained spoke colors 0,1. For pin colors2,3, every vertex is a degree-list vertex, and rejection forces tightness. Theorem10 gives palettes on the same block tree; column independence forces one active triangle and three arbitrary or zero-length bridge arms terminating at the original contacts. Each triangle vertex has exactly one additional original edge. An inactive branch without boundary or s constraints, even if it contains r, has entry degree3 and all other degrees4; greedy slack plus one permutation of its entire coloring contradicts M_2 rejection. Thus it has a real retained X boundary tether. Five disjoint connected bags {s}, three triangle-plus-arm bags, and B plus tether interiors have all ten pair adjacencies in X; no witness uses omitted rb_i.',
    'LOW2-EXCLUSION': 'For every arbitrary-size finite original G satisfying all twelve LOW2 premises, the preceding same-X original-edge K5 minor contradicts disk planarity. This scoped paper exclusion does not independently close all LOW, HIGH, long, any other core, general N2/E, source realization or Lean.'
}
judgments = []
for claim in claims['claims']:
    judgments.append({
        'id': claim['id'], 'source_contract': claim['source_contract'],
        'dependencies': claim['dependencies'], 'external_dependencies': claim['external_dependencies'],
        'additional_premises': [], 'quantifier': claim['quantifier'],
        'verdict': 'accepted_with_full_stated_LOW2_contract',
        'evidence_layer': 'independent arbitrary-size paper review; external Gallai dependency explicit',
        'independent_reason': proof[claim['id']], 'machine_proved': False,
    })
write('independent-judgment.json', {
    'task': 'N45-L2R', 'BASE': BASE, 'review_scope': 'Original graph, both U contacts, complete relations and full lifts, BASE theorem mapping; only LOW2.',
    'full_source_contract': claims['full_source_contract'], 'claims': judgments,
    'findings': [], 'additional_premises': [], 'no_peer_judgments_read': True,
    'source_control_evaluation': 'not established; not executed; no trigger count',
    'calibration': 'An abstract fixed graph is used only for joint/fibre/full-lift semantics. It has no claimed embedding, Sigma, rejecting minimality, source realization or LOW2 contract.',
    'external_trust': claims['trust_boundary'],
    'remaining_OPEN': ['whole LOW independent composition', 'HIGH', 'long', 'other cores', 'original55', 'nonminimal derivative identities', 'general N2/E', 'epsilon>=3', 'Lean'],
    'shared_edits': False, 'commit_push_PR_external_messages': False,
})
print(json.dumps({'worker_files': len(worker_files), 'BASE_inputs': len(base_inputs['inputs']), 'pins': len(pins), 'claims': len(judgments)}, sort_keys=True))
