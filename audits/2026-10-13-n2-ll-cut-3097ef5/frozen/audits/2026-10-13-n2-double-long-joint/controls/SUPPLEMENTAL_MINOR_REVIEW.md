# Original K5 leaf-cycle pair: independent minor review and four controls

2026-10-13. This supplement creates new files only. The prior complete-fibre
artifact, checker, report and receipt remain unchanged. The original
`observations.json` still has SHA256
`724a540c00a8248d2b45b48acdb1cd9d702f26ab68053d8926a3d3d31c406658`.

## General conditional minor

The proposed original K5 construction is valid under these explicit premises:

1. C and Q are distinct connected original mixed components of `H-{r,s}`;
   in the `(2,0)` branch, `H-C` is exactly the connected graph on `r,s,Q`.
2. Vertices p,z are adjacent **private vertices of the same original leaf
   cycle block** of C. Both are original root contacts, have actual boundary
   attachment h, and have no other boundary attachments.
3. C and Q each have at least one actual boundary attachment outside `{h}`.
   Both being long supplies this premise.
4. There is an actual original root spoke `rh` or `sh`.

The five branch sets are

```
A={h}, R=V(H)-V(C), P={p}, Z={z},
F=(V(C)-{p,z}) union (V(B)-{h}).
```

They are pairwise disjoint. R is connected through the other original mixed Q.
Removing two adjacent private vertices from a leaf cycle leaves the rest of C
connected: the remaining cycle vertices form a nonempty path and retain the
block's attachment cutvertex when one exists. The original boundary `B-h` is a
connected path. Since p,z have no boundary attachments outside h, C's outside
attachment survives in `C-{p,z}` and joins these two connected sets, proving F
connected. This argument also covers a single cycle block.

All ten adjacencies use original edges:

| Pair | Original edge witness |
| --- | --- |
| A–R | the assumed original root spoke at h |
| A–P, A–Z | the actual attachments ph and zh |
| A–F | either boundary-cycle edge incident with h |
| R–P, R–Z | the actual root contacts of p and z; owners may agree or differ |
| R–F | an actual Q attachment outside h |
| P–Z | the original cycle edge pz |
| P–F, Z–F | each vertex's other incident edge in the original leaf cycle |

Thus these are original K5 branch sets, contradicting planarity. The proof is
independent of C or Q size, uses no quotient coloring or relation transfer, and
does not require the root owners of p and z to agree. Extra original edges are
harmless to this minor argument.

The minor does **not** prove that a failed diagonal list coloring produces p,z.
That palette implication is a separate proof obligation being reviewed by the
theory author. Nor does the minor apply merely because two contacts occur
somewhere in C: adjacency and private leaf-cycle placement establish the
remaining connectivity and the P–Z adjacency.

## Four fixed controls and exact applicability

The explicit controls retain B0..4, roots5,6, triangle7,8,9 and bridge9,10 in C,
and the Q edge11,12. Attachments are `7→0`, `8→0`, `9→1`, `10→2,3`,
`11→3,4`, `12→4,0`; Q contacts are `5–11,6–12`; root spoke is `5–0`.
The owners of7 and8 take all four ordered pairs in `{5,6}²`. Vertex10 is owned
by the opposite root if those two owners agree, and by root5 otherwise.

All C/Q vertices have full degree four; both pieces are mixed and long, and
there are no shared C contacts. For every owner variant the certified branch
sets are

```
{0}, {5,6,11,12}, {7}, {8}, {9,10,1,2,3,4}.
```

[The supplemental artifact](supplemental_minors.json) saves the complete
original graph, degrees, literal contacts, actual attachments, branch sets,
an original spanning tree for every bag and all ten original cross edges.
[The checker](supplemental_minor_checker.py) recomputes all of these using only
standard Python. Each K5 minor is `triggered and holds`.

These controls deliberately certify the **minor implication only**. Because
vertex10 is a root contact with actual attachments2,3, their
`W_C^r union W_C^s` is `{0,2,3}`, not `{h}={0}`. Therefore the proposed T1 lemma's
full palette premise is `not triggered`. Root degrees are not required to be
five, the graphs are nonplanar by their certified K5 minors, and no full Sigma
relation or criticality is asserted. Full original N2 target status remains
`not triggered`.

## Replay

```
python3 -B audits/2026-10-13-n2-double-long-joint/controls/supplemental_minor_checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-n2-double-long-joint/controls/supplemental_minor_checker.py --check
```

Artifact size is 24,345 bytes; SHA256
`4fa487989869cf81077e09354cad593e9352992d587ae09a117181e285abe057`.
Normal and seed17 replay are identical. A deliberately falsified original
adjacency is rejected. The replay receipt is
[supplemental_verification.json](supplemental_verification.json).
No existing evidence was modified; no source search, Lean theorem, commit or
push is supplied by this supplement.
