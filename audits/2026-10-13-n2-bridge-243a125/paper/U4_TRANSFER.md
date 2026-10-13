# U4-3R: nonadjacent two-mixed 44 exclusion without a complete target mask

BASE `243a125a80e4d8de40957f59d8da0bdbc974cf69`. This is a new portability
proof. It leaves the archived U4 statement, certificate, and failures unchanged.
All graph names below belong to one original disk and one ordered boundary.

## Statement and exact scope

Let G be finite and simple, with ordered induced disk boundary
B=(b0,b1,b2,b3,b4). Assume T4 is accepted; every nonboundary edge is
complete-Sigma-critical; epsilon=2; the effective H is connected and touches
all five boundary vertices. Let r,s be nonadjacent original vertices of full
G-degree five, with all other effective interior vertices of full G-degree
four. Assume H-{r,s} has exactly two original mixed components, all other
components being unary. Assume that at least the three literal rows
q0=01212, q1=01202, q3=01021 are rejected. Do not prescribe q2 or q4.

**U4-3R.** No rejected row of G has an inclusion-minimal core M containing
both r,s with their M-degrees both four. This includes a core for q2 or q4
if that additional row is actually rejected.

The source-criticality and M's own selected-row minimality are different
premises. G is not assumed minimal for any one row. Free isolated coordinates
are omitted only from H; their independent four-color factors remain in every
full coloring.

The proof below uses the same upstream all-degree-four classification and
finite terminal theorem as historical U4. It removes the target-mask
hypothesis by checking what each step actually reads; it does not claim an
independent proof of the entire older Gallai/classification chain.

## 1. The original omission identity is mask independent

Take a rejected row beta and such a minimal beta-core M. Every effective
vertex of M has degree at least four. An original nonroot has full degree
four, so if M contains it effectively, M contains all its original incident
edges. This propagates along each original component of H-{r,s}.

By the all-degree-four theorem, M's effective interior is connected and is a
path, one triangle with nonbranching path arms, or two vertex-disjoint
triangles joined by a direct original bridge and no tails. In particular all
its simple cycles are triangles. If M retained both mixed components, their
two internally disjoint r-s paths would give a cycle of length at least four.
M cannot retain neither, because r,s are nonadjacent and its interior is
connected. Thus M retains precisely one mixed P and omits the other O.

Each root loses exactly one original incidence. Consequently O has original
incidences (1,1), and M omits no other edge or component:

`M = G - V(O)`.

The retained P has one or two contacts at each root. Two contacts at a root
form its original triangle; two such triangles must be disjoint. This is
E3 nonadjacent §5 / E4 §6, not a consequence of Sigma933 or Sigma941.

Sources: [E3 §5](../frozen/artifacts/c5_excess_two_e3/REPORT.md),
[all-four classification §4](../frozen/docs/c5_k4_blocks.md),
[historical U4 §1, lines 17–36](../frozen/docs/c5_excess_two_nonadjacent_two_mixed_core44.md).

## 2. Every source-to-domain restriction survives

The next table accounts for the entire domain reduction in historical U4
§§2–3. None of these steps needs an accepted q2 or q4.

| Step | Actual premise and reason |
| --- | --- |
| Every original piece is one-sided | After deleting either mixed, the other still connects r,s; deleting a unary also leaves the roots connected. |
| O touches at least two boundary vertices | A critical witness for an original root-O edge gives a full exterior coloring which O cannot extend. Degree lists on the complete original O are therefore tight and Gallai. If O touched at most one boundary vertex, each leaf bridge consumes at least two root incidences, and each leaf odd cycle at least two; single bridge/cycle cases likewise need more than O's two incidences. A singleton has degree at most three. K4 is excluded by the original exterior hub and four tethers. |
| P touches at least two boundary vertices | The actual all-four core has at most two vertices of interior degree three and none of interior degree four. If P touched at most one boundary point, every P vertex would have interior degree at least three, so P has at most two vertices. A singleton cannot have full degree four; two vertices would make a forbidden diamond block. |
| `ell + 2u <= 3` | Both mixed supports now have at least two vertices, so each short pays one shield edge and each long pays at least two; each unary pays at least two. Original shields are mutually edge-disjoint in B. Thus `2 + ell + 2u <= 5`. |
| u=2 impossible | Immediate from the preceding inequality. |
| u=0 and both mixed short impossible | Both roots take the unused color of any rejected three-color row. Original N-diagonal gives two same-row complete component lifts. One rejected T3 row suffices. |
| u=1 forces retained incidences 12/21 | The root without a unary cannot have retained incidence one: its three original spokes form a star with one long face of three boundary edges, while the two mixed and the unary require at least four shield edges there. The other incidence cannot be two: actual all-four triangle/tail classification forbids the required branch or extra tail. |
| u=0 and retained incidences 11 impossible | Each root then has three original spokes. Full B-touch makes each triple consecutive. The two long star faces intersect in 024 or 023 after one common transport; neither contains three consecutive boundary vertices, so neither mixed can be long. The all-short case was already excluded. |
| Remaining M shapes | One triangle with the incidence-two root noncutting in that triangle and the incidence-one root on its path arm; or the direct-bridge double triangle with all nonadjacent root markings. |

The O critical witness is allowed to lie in any actually rejected row; this
causes no hidden three-row assumption. Full B-touch is available in the E4
parent from two distinct rejected singleton positions, by E2/E3, and is also
an explicit theorem premise above. The shields charge the actual original
pieces, not a chosen relation realization or a contracted surrogate.

Source: [historical U4 §2, lines 38–87](../frozen/docs/c5_excess_two_nonadjacent_two_mixed_core44.md).

## 3. Retain the roots through the unbounded path reduction

For a single triangle, the upstream original attachment theorem gives 18
uniform contexts or eight two-run contexts. The original marked root is
kept as a singleton. Split its path run immediately before and after this
vertex. An unmarked positive odd run reduces to length one; a positive even
run to length two; a zero run stays zero. This follows for every literal
boundary row from its common available color set: a two-color run alternates;
a run with at least three available colors admits every pair of endpoint
colors. Thus the entire triangle-plus-marked-root joint is preserved.

The corresponding operation is an original path minor with fixed boundary
and root. It is not an equality of all full contact tuples between different
graphs: retain the appropriate lifting relation and the original full
colorings on each side. In particular, the collision of two root pairs in
the reduced core lifts to two full colorings of the same original M in the
same row and root coordinates.

The necessary finite domain is:

| Marked family | Count |
| --- | ---: |
| Single triangle, uniform run, marked root retained | 220 |
| Single triangle, two runs, marked root retained | 96 |
| Direct-bridge double triangle, retained22 and no unary | 256 |
| Direct-bridge double triangle, retained12/21 and binary unary | 256 |
| Total | 828 |

Four of the 316 single-triangle entries are harmless excess entries already
forbidden by the star argument. Leaving them in the domain weakens the
necessary screen; it does not omit a source. There is no target-mask filter
in this domain definition.

Sources: [path-run theorem §§2–5](../frozen/docs/c5_triangle_path_reduction.md),
[historical U4 §3, lines 89–125](../frozen/docs/c5_excess_two_nonadjacent_two_mixed_core44.md).

## 4. Extract the mask-free finite statement

For each of the 828 cores, normalize its one rejected row by **one common
transport of the whole graph** to q=01012. The stored normalized core has
complete Sigma1022. This transport moves B, every attachment, root order,
all contact coordinates, and the omitted original O as well. It is not an
independent normalization of M and O, and it does not assert that the original
three selected rows retain their original indices in the temporary frame.

Let K_M(beta) be the exact root-pair projection of M's full same-row contact
joint. The finite statement used is

`for every marked M and every three-color beta != q,`
`K_M(beta) contains distinct (a,b),(a',b') with a=a' or b=b'.`  (FC)

This is precisely the 3,312=`828*4` collision statement of historical U4 §4,
not its separate 8,280 exact-target comparisons. The four other T3 rows are
accepted; the result gives two compatible same-coordinate root pairs in
each. It imposes no acceptance condition on the original source G.

The existing primary and independent checkers were both rerun read-only on
2026-10-13 and exited zero:

```text
python scripts/c5_excess_two_nonadjacent_two_mixed_core44.py --check
python scripts/c5_excess_two_nonadjacent_two_mixed_core44_audit.py --check
```

Both report 828 marked cores, 3,312 non-q T3 collisions, 8,280 full row joints,
and 15,460 q-edge-deletion witnesses. The independent checker reconstructs
the marked domain without importing the producer and uses fixed-order full
coloring enumeration; it checks 98,096 complete contact witnesses, 102,536
empty and 29,944 nonempty root fibres, and 316 marked long-path controls.
The audit's new checker provides the additional mask-free extraction record.

These finite results are a necessary terminal theorem after the paper
reduction. They are not a search for source graphs, and zero target-source
triggers play no role in (FC).

Source: [historical U4 §4, lines 127–164](../frozen/docs/c5_excess_two_nonadjacent_two_mixed_core44.md).

## 5. Same-row restoration gives the contradiction

Keep the complete original relation of O, including a shared contact as one
vertex coordinate if present. Define F_O(beta) as the root pairs for which
the original O has no full coloring. With s pinned to b and r free, removing
the r-O inequality leaves strict list slack at the original r-contact, even
when the two root contacts coincide. Connectedness gives a full O coloring.
Its r-contact has a single color, so all r colors except possibly this one
extend that same full coloring. Thus each column of F_O has size at most one.
Exchanging the roots gives each row size at most one.

For every beta != q of T3, (FC) supplies two same-coordinate pairs in K_M.
F_O cannot contain both. Choose one pair outside F_O, one full coloring of
the original M witnessing that pair, and one full coloring of original O
at those same pins. Their only common vertices are B,r,s, with identical
colors; all original attachments and contact edges are satisfied. They glue
to a complete coloring of original G, including every free-coordinate factor.

Consequently G can reject at most the one T3 row q. It actually rejects
q0,q1,q3. This contradiction proves U4-3R. No q2/q4 acceptance is used. ∎

Do not strengthen the intermediate claim to equality of all ten rows between
G and M: the retained finite negative control Sigma1018 shows that a T4 row
can be lost on restoration. The conclusion needed here concerns T3 only.

## 6. Immediate generalized-N2 consequences

By the original root-deletion theorem, two mixed components force every
minimal rejected-row core to contain both roots. U4-3R excludes its 44 case.
Therefore Z(G), the set of rejected rows with an excess-zero minimal core,
is empty. The mask-free pair-critical theorem applies with `|Z(G)|=0<=1`:

`every proper B-preserving subgraph S satisfies |Q(S)| <= 1.`  (P)

This step is valid for Sigma932 as well. It does not say that S accepts all
ten rows or that every edge is critical for each selected row. The stronger
all-row deletion conclusion requires the subsequent bridge argument.

Sources: [root-deletion §3, lines 115–152](../frozen/docs/c5_excess_two_root_deletions.md),
[pair-critical §§2–3, lines 49–116](../frozen/docs/c5_excess_two_arc_pair_critical.md).

## Trust boundary

The new contribution is an explicit mask-free transfer of U4 and its P
corollary. The all-four original-graph classification, its unbounded
triangle/path reduction, the finite marked-core terminal theorem, and the
external degree-list/Gallai theorem remain named dependencies. There is no
new Lean theorem. This theorem does not address N1, adjacent roots, a
different criticality contract, or epsilon greater than two.
