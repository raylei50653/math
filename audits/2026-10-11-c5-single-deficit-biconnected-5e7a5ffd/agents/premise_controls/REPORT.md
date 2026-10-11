# Named premise controls

BASE: `4dd11f422c6fa49265a412085116b088786d0344`.

This independent sub-audit reads `docs/HANDOFF.md`, `docs/STATUS.md`,
`docs/c5_weak_list_cores.md` and `docs/c5_degree5_guide.md`; it writes only this
fresh, exclusive directory. The hashes of those four inputs and this replay
program are retained in [certificates-final-v1.json](certificates-final-v1.json). The parent
audit records the literature PDF hashes. No source graphs are enumerated:
the controls are the six explicitly named graphs below.

The whole original-domain implication triggers in one named control and holds
there. Removing biconnectivity, allowing a second degree-5 point, or permitting
an improper row each has an explicit disk counterexample to the claimed
conclusion. The attachment control is a counterexample to an intermediate
minor inference, not a counterexample to the full theorem. Honest supergraph
degree bookkeeping is not shown necessary: the named comparison retains the
conclusion, and no counterexample is claimed.

All graphs have the ordered induced frame
`B=(b0,b1,b2,b3,b4)` with its five cycle edges and no frame chord.
Each neighborhood in the following table is an actual neighborhood in the
same named graph, not a prescribed list or marginal.

| ID | Interior graph and actual frame neighbors | beta | Result |
| --- | --- | --- | --- |
| original-domain-triangle | Triangle `sxy`; `s:{0,1,2}`, `x:{3,4}`, `y:{2,3}` | `(0,1,2,1,2)` | `triggered and holds`: full degrees `(5,4,4)`, rejected, `d_H(s)=2`, `H-s=K2` |
| biconnectivity-removed-path | Path `s-x-y`; `s:{0,1,2,3}`, `x:{0,3}`, `y:{0,3,4}` | `(0,1,2,3,1)` | `counterexample`: full degrees `(5,4,4)`, proper row rejected, `d_H(s)=1` |
| second-degree5-diamond | Cycle `s-x-t-y-s` and diagonal `s-t`; `s:{0,1}`, `x:{1,2}`, `t:{2,3}`, `y:{0,3}` | `(0,1,0,1,2)` | `counterexample`: full degrees `s,t=5`, `x,y=4`; biconnected and rejected, `d_H(s)=3` |
| improper-beta-diamond | Same interior diamond; `s:{0,1}`, `x:{1,2}`, `t:{3}`, `y:{0,4}` | `(0,0,0,0,0)` | `counterexample`: full degrees `s=5`, others `4`; biconnected, no extension, `d_H(s)=3` |
| actual-attachments-lost-k4 | `H=K4` on `s,x,t,y`; only frame attachment `s-b0` | `(0,1,0,1,2)` | `counterexample` to the unqualified intermediate inference `K4 in H + B implies K5 in M`; original theorem `not triggered` |
| honest-supergraph-degree-bookkeeping | Triangle control with `s-b0` deleted from `M`, retained in `G` | `(0,1,2,1,2)` | `triggered and holds` for correct degree bookkeeping: `d_G(s)=5`, `d_M(s)=4`, conclusion still holds; original theorem `not triggered` |

The final JSON also gives an `original_domain_status` for every row: only the first
control is `triggered and holds`, and the other five are `not triggered` in
the exact original domain. This prevents the altered-premise counterexamples
from being reported as counterexamples to the original theorem.

## Paper constructions and rejection arguments

For the path counterexample, draw `B`, add `s` joined to `b0,b1,b2,b3`, and
consider the remaining quadrilateral face `(s,b3,b4,b0)`. Insert `x` joined
to `s,b3,b0`. In the remaining quadrilateral `(x,b3,b4,b0)`, insert `y`
joined to all four corners. These face insertions directly produce a disk
with exactly the stated edges. The row is proper and uses four colors.
The four actual boundary neighbors of `s` use all four colors, so
`L_beta(s)=empty`. No coloring extends the row. The interior path has the
cut vertex `x`, and `d_H(s)=1`. This counterexample also retains connectivity;
merely assuming that `H` is connected does not repair the implication.

For the second-degree-5 control, place the interior cycle `s-x-t-y-s`
inside `B` and its diagonal `s-t` inside that cycle. Draw the specified
spokes in cyclic order through the annulus. Its inner annular faces are
`(b0,b1,s)`, `(s,b1,x)`, `(b1,b2,x)`, `(x,b2,t)`, `(b2,b3,t)`,
`(t,b3,y)`, `(y,b3,b4,b0)` and `(y,b0,s)`.
The two remaining interior faces are `(s,x,t)` and `(s,t,y)`.
Thus no edge crosses, and the outer face is the literal original `B`.
Every inner vertex sees boundary colors `{0,1}`, so every actual list is
`{2,3}`. The triangle `s-x-t-s` cannot be colored from two colors. The
diamond is biconnected and has `d_H(s)=d_H(t)=3`. This disproves the proposed
conclusion after allowing two degree-5 vertices; it does not show that
every two-degree-5 source violates it.

For the improper-row control, use the same interior cycle and diagonal and
the listed spokes. The annular faces are `(b0,b1,s)`, `(s,b1,x)`,
`(b1,b2,x)`, `(x,b2,b3,t)`, `(t,b3,b4,y)`, `(y,b4,b0)` and `(y,b0,s)`.
Its two inner triangles are again `(s,x,t)` and `(s,t,y)`.
The full-degree and biconnectivity premises are intact. A constant boundary
row cannot extend because each of its five frame edges is monochromatic.
In contrast, all actual interior lists are `{1,2,3}`, and the diamond has
six list colorings. One is `(s,x,t,y)=(1,3,2,3)`.
Hence failure of an improper row cannot be converted into nonchoosability
of the interior list instance; the conclusion fails because `d_H(s)=3`.

The original triangle control is the explicitly named source from
`docs/c5_weak_list_cores.md`, section 3. Its actual lists are
`L(s)={3}` and `L(x)=L(y)={0,3}`. Therefore `s=3` forces both adjacent
vertices `x,y` to be `0`, contradicting edge `xy`. The saved disk rotation
and its faces verify a genuine source control; it is not just an abstract
list obstruction.

The attachment control is a planar `K4` inside `B`, tethered from `b0` to
an outer vertex `s` of that `K4`. Its four singleton inner branch sets
give a `K4` minor. The original connected set `V(B)` is adjacent only to
`{s}`, and misses the other three branch sets. The graph is planar, so it
has no `K5` minor. Its beta has 18 extensions. In this control the degree
premise and rejection premise are absent. It demonstrates exactly why
the fifth branch set cannot be attached using omitted or independently
invented source attachments, without misclassifying it as a theorem
counterexample.

Finally, the degree-bookkeeping control is obtained from the original
triangle by deleting only `s-b0`. Let `G` be the original triangle disk
and `M=G-sb0`. Then `d_G(s)=5` but `d_M(s)=4`, while the two other inner
degrees are `4` in both graphs. The interior lists of `M` are all
`{0,3}`, so its triangle still rejects the proper row. Both conclusions
hold. For an honest subgraph `M subseteq G`, the elementary inequality
`d_M(v) <= d_G(v)` gives upper bounds from full source degrees, but it
does not justify equality of full degrees or actual frame-neighbor
counts. This control does not establish that replacing equality in the
theorem by appropriate upper bounds is false or true in general.

## Complete finite certificates and replay

[replay.py](replay.py) retains all `4^n` interior assignments of each named
source, all conflicting edges for every failed assignment, every list
coloring, full `M` and `H` degrees, actual frame neighborhoods and lists,
and properness of the literal row. There are 960 complete interior
assignments across the six fixed inputs. No quotienting or normalization
of frame labels occurs.

NetworkX `3.5` checks planarity of `M` with an outside apex joined to all
five frame vertices. The program then removes only that apex and
independently checks the saved cyclic rotation, all facial walks,
Euler's formula and the literal `C5` face. The JSON preserves both
rotations. The paper face constructions above directly substantiate the
three counterexamples without relying solely on the software check.

A second, list-restricted coloring search shuffles only traversal order
with seed `17` and agrees with the complete assignment counts. The two
negative controls, deleting the original attachment `s-b0` and replacing
the baseline row by a constant row, are each marked
`triggered and holds` for detecting the stated failed premise. A separate
corrupted-degree certificate is retained in
[corrupted-degree-certificate-v1.json](corrupted-degree-certificate-v1.json).
Read-only check mode rejects it with exit status `1`; the complete stderr,
exact command and `triggered and holds` result are preserved in
[corrupted-certificate-negative-check-v1.json](corrupted-certificate-negative-check-v1.json).

Replay from the repository root with the preexisting, read-only project
interpreter:

```bash
.venv/bin/python -B audits/2026-10-11-c5-single-deficit-biconnected-5e7a5ffd/agents/premise_controls/replay.py --check
```

The script's generation mode exclusively creates its own output with
`open('x')` and refuses to overwrite an existing certificate; its check mode
is read-only. The earlier own-output generation
[certificates.json](certificates.json) is retained as a pre-final snapshot
and is not the final replay target. The exact invocation uses
`/home/ray/developer/ai/math/.venv/bin/python`, resolving to
`/usr/bin/python3.14`, with the preexisting NetworkX `3.5`; no dependency
installation or dependency cache write was performed. These details and
the final certificate hash are recorded in
[environment-v1.json](environment-v1.json).
Successful finite controls do not establish the
unbounded theorem or any new Lean theorem. No Lean build or source-family
enumeration was performed for this subtask.
