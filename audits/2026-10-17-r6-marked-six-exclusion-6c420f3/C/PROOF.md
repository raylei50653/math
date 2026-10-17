# C: the frozen weak-premise control has two marked cyclic six-cuts

Frozen BASE: `6c420f3ca77d60952ed76f93dff7449c522715ca`.

This is a complete finite reconstruction of the previously archived twelve-
vertex control. It confirms the user's numerical claims and shows that the
new marked-six exclusion removes that control from a source argument. It is
not an arbitrary-size proof, an actual completed source, or a proof of
`W110+W101>0`. The arbitrary-source exclusion belongs to A and B of this audit.

## 1. Exact graph and marking

The input is the unchanged frozen
[`input_graph.json`](../frozen/audits/2026-10-16-r6-319-joint-parity-f1faf74/B/input_graph.json),
SHA256
`c07c851ee37e1f327d19042a6216a085e546aa27dd72f67366083b1dab7b60ca`.
It has twelve primal vertices, thirty edges, and twenty triangular faces.
Every edge and face keeps its original index. In particular, the marks are

| Mark | Original edge index | Primal endpoints | Actual dual endpoints |
| --- | ---: | --- | --- |
| e | 0 | 0,2 | 0,14 |
| f | 29 | 10,11 | 11,17 |
| g | 6 | 1,9 | 5,8 |

[check.py](check.py) imports no previous checker. It first checks the frozen
BASE, source paths, two frozen SHA256 values, graph identity, exact marking,
and the explicit `not triggered` source declaration. It rejects extra input
keys, including inherited named pins. It coherently orients the face complex,
checks that every edge has two opposite directed face incidences, verifies
that each vertex link is one cycle, and checks connectedness and Euler
characteristic two. It then reconstructs a full primal rotation and replays
all its faces. The actual dual uses these twenty original face IDs and the
same thirty edge IDs; it is simple, connected, and cubic.

The certificate retains the oriented faces, complete primal rotation, and
all actual dual edges. This does not assign the source's pins m,z,v,w,p,q to
this control. For either possible m in the actual g endpoints `{1,9}`, m is
adjacent to neither 0 nor 2. Consequently the source face mvw is already
impossible with the literal marks. Source applicability is **not triggered**.

## 2. Every ordinary matching and its entire complement

The checker recursively chooses the least unmatched dual vertex and every
possible available incident edge. This exhausts every perfect matching
exactly once. It finds 38 ordinary perfect matchings. Every complement is
checked to be two-regular and is traced into its full vertex and edge cycles;
no local segment or selected odd component substitutes for the complement.

| Mark status | Ordinary PM count | Even-complement weight W |
| --- | ---: | ---: |
| 000 | 13 | 28 |
| 001 | 3 | 2 |
| 010 | 1 | 2 |
| 011 | 6 | 16 |
| 100 | 9 | 18 |
| 101 | 3 | 0 |
| 110 | 0 | 0 |
| 111 | 3 | 6 |

Here W is computed directly as the sum of `2^number_of_complement_cycles`
over matchings whose entire complement is even. This audit does not rerun
the earlier colouring-fibre census and does not infer source realizability
from these weights.

The full joint family is exactly the following three 101 matchings:

| Matching edge IDs | Entire complement cycle lengths |
| --- | --- |
| 0,2,6,8,11,16,18,22,24,25 | 5,15 |
| 0,2,6,8,11,18,20,21,24,25 | 5,5,10 |
| 0,6,8,11,13,17,19,22,24,25 | 7,13 |

All three have two odd cycles. Thus this fixed graph still has joint minimum
oddness two. The certificate preserves all 38 matchings and every complete
complement cycle, including the three joint rows; it preserves neither an
incompatible second marking nor a partial complement.

## 3. Exhaustive marked six-cycle census and actual cut sides

Depth-first search enumerates every simple primal six-cycle. Canonical
rotation and reversal remove duplicate traversals only. There are 258 such
cycles in total, and exactly five contain both literal e and f.

For each of the five, the checker deletes precisely its six corresponding
dual edges, obtains two connected dual components, and independently checks
that the original edge boundary of **each** component is exactly those six
edges. It then records every induced edge on each side. A connected side
contains a cycle precisely when its induced edge count is at least its
vertex count. The result is:

| Simple primal six-cycle | Literal dual boundary edge IDs | Side sizes (V,E) | Cyclic cut? |
| --- | --- | --- | --- |
| 0,2,7,11,10,6 | 0,3,11,23,26,29 | (16,21); (4,3) | no |
| 0,2,11,10,5,4 | 0,2,12,16,22,29 | (14,18); (6,6) | yes |
| 0,2,11,10,5,6 | 0,3,12,20,22,29 | (16,21); (4,3) | no |
| 0,2,11,10,6,4 | 0,2,12,17,23,29 | (16,21); (4,3) | no |
| 0,2,11,10,9,4 | 0,2,12,19,28,29 | (12,15); (8,9) | yes |

The three noncyclic rows have a connected four-vertex, three-edge side, so
that side is a tree. The two remaining rows both have a cycle on each actual
side. In particular the user's two examples and all four claimed side
sizes are reproduced exactly. Every side's original face IDs and induced
edge IDs are retained in [certificate.json](certificate.json).

The new source restriction excludes this graph already through its five
marked primal six-cycles, and independently through either of its two
actual marked cyclic six-cuts. The control was already missing the literal
source layout; the present census isolates a further restriction that the
older four-/five-cut conditions did not impose on it.

It does not establish that every positive joint minimum forces such a cut.
No implication from a failed repair to a marked small cyclic cut, no strict
oddness descent, and no general positivity conclusion is claimed.

## 4. Replay, corruption controls, and boundary of authority

The certificate is created with exclusive file mode. `--check` recomputes
the complete result from frozen graph bytes and rejects any structured
certificate difference. The seeded run changes matching and primal-search
traversal order and also sets `PYTHONHASHSEED=17`; both replays produce the
same full certificate.

[run_checks.py](run_checks.py) records two successful replays, seven rejected
corruptions, and a separate exclusive-create preservation check in
[VERIFICATION.json](VERIFICATION.json). The corruptions respectively omit an
ordinary PM, change an actual complement vertex, change an induced side's
edge count, omit a marked cycle, change the literal f edge ID, invent source
authority, and change the frozen graph marking. In the last case, the input
hash fails before reconstruction. Trying to overwrite an existing certificate
fails and preserves its bytes.

Replay from the repository root:

```sh
python3 -B audits/2026-10-17-r6-marked-six-exclusion-6c420f3/C/check.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-17-r6-marked-six-exclusion-6c420f3/C/check.py --check --seed 17
python3 -B audits/2026-10-17-r6-marked-six-exclusion-6c420f3/C/run_checks.py --check
```

This certificate checks one finite weak-premise graph. It uses no 4CT,
external theorem, source replacement, or Lean theorem. It has no original
completed bad source to reduce and supplies no smaller-source closure.
`W110+W101>0`, `omega_e=0`, full319 exclusion, arbitrary-size repair, and new
Lean formalization remain OPEN. There is no commit or push authority here.
