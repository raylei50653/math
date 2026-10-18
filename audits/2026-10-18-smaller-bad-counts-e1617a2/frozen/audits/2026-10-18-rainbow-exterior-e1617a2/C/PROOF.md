# C. Same completed graph, full fibres, and exterior Kempe joins

Frozen BASE `e1617a2756813327d7ad333cfdd0fd92fa9efc38`.
The three exact input digests are embedded in [check.py](check.py): the
preceding smaller-source `C/check_bridge.py`, `C/certificate.json`, and
independent `B/REVIEW-C-FULL-FIBRES.json`, all read from this audit's frozen
directory. No earlier checker is imported or executed, and no new disk or
exterior is searched. The original completed twelve-vertex graph is rebuilt
from its oriented triangular faces; the same two fan constructors are then
applied to its unchanged exterior.

## Full-fibre replay

Independent sequential backtracking recovers every full colouring in the ten
literal outer rows, including every empty fibre. The results agree exactly
with the preceding independent B full-fibre certificate and the C hashes:

| Graph | Counts in the frozen ten-row order |
| --- | --- |
| G | `5,13,8,5,1,0,1,0,8,4` |
| G_a | `0,1,1,0,1,0,1,0,1,2` |
| G_b | `1,12,11,1,0,0,0,0,11,10` |

The order is `01012,01021,01023,01201,01202,01203,01212,01213,01231,01232`.
The output [certificate-v2.json](certificate-v2.json) contains the complete full
fibres, not just counts or pin marginals. For each of the 53 candidate full
colourings, all sixteen `(p,h)` choices are checked against the actual
original edge set. The resulting full lift set agrees exactly with the
corresponding same-row original extensions. It is empty exactly when
`(a,b,q,n)` is rainbow.

## Actual components as joins through the unchanged exterior

Write `E` for all original edges surviving deletion of `p,h`, including the
six rim edges; write `P_a` or `P_b` for the rim and the three fan chords.
For one fixed full colouring chi and colour pair ij, take all actual maximal
ij components of E, including isolated vertices, and all actual ij components
of the appropriate fan. Regard both as partitions on their actual vertex
sets. Their partition join is exactly the ij-component partition of
`E union P_s`.

This identity follows because every completed-graph path splits into
alternating subpaths inside the two edge sets, while every join step is
realized by such a subpath. The rim overlap is literal; repeated rim edges
do not change connectedness. No exterior relation from another colouring
can be substituted in this identity.

The checker saves and replays all six colour pairs for all 53 candidate
colourings: **318 joins**, comprising 42 for G_a and 276 for G_b. Each record
contains the graph name, literal outer row, full colouring, exterior
partition, fan partition, joined partition, and independently computed
maximal components. Every recorded maximal component can actually be
switched: the resulting full colouring is proper, and switching it again
recovers the original full colouring.

## Fan-A transport and its precise conditional consequences

In G_a, the complete neighbour set of b is `{a,c,q}`. Every accepted
`01232` full colouring has `q in {0,1}`. Recolour only b from 3 to `1-q`.
This gives row `01202` with q=1 or row `01212` with q=0. The inverse recolours
only b to 3. Thus, unconditionally and on the same fixed graph,

```
F_01232(G_a)
  ≅ F_01202(G_a; q=1) disjoint-union F_01212(G_a; q=0).
```

The fixed completed control exercises this full-colouring bijection:
`2 = 1 + 1`. In particular an accepting G_a always accepts at least one
of the two queried negative rows; no accepting G_a can satisfy this fixed
four-query smaller-bad certificate. The criterion is sufficient, not
necessary, for being outside K132: other rows or orientations are not
excluded by this no-go statement.

If the two original negative fibres are empty, the old lift criterion makes
both candidate negative fibres rainbow. A rainbow `01202` colouring with
q=3 necessarily has n=1; recolouring b from 0 to 1 gives a nonrainbow
`01212` colouring and an explicit original lift, a contradiction. The
reverse argument eliminates q=3,n=0 from `01212`. Hence both q=3 sectors
are absent under the paired original emptiness assumption. The displayed
bijection then uses the two entire candidate negative fibres, and all
accepted G_a colourings have n=3. The old six-contact interface supplies
**38** explicit transfer checks, including six q=3 cross-row lift controls.
These are checks of the existing interface identities, not realizations of
a target completed source.

For a pair-row colouring with q in `{0,1}`, b and q lie in the same actual
01 component. If that component misses x and y, switching it gives the
other literal pair row. If it meets either x or y, edge xy forces both,
and this switch does not preserve the fixed outer frame. The frozen control
positively exercises the first case: its 01 component is
`{L,R,b,n,q}`, and switching it exchanges its two full pair-row colourings.
These two witnesses are nonrainbow; their original fibres are nonempty.
Recolouring b to 3 first leaves the q-component `{L,R,n,q}` and gives the
equivalent transport through the accepted fibre.

## Forced contacts require the original empty fibre

For a rainbow candidate colouring, let K be the actual component of n with
colours `chi(n),chi(T)`, for T in `{a,b,q}`. If K contains neither T nor any
original outer vertex, its switch fixes the entire original outer row and
creates a nonrainbow gate. The checker constructs and verifies every
resulting original full lift. Consequently the stated contacts are forced
only when that same original full fibre is empty. The fan-A refinements
`01021: n -> {y,c}`, `01202: n -> x`, `01212: n -> y` are checked with the
same condition and the same actual components.

All twelve general contact records in this completed control are explicitly
**not-triggered**, because the relevant original negative fibre is nonempty.
Two records actually fail the contact alternative; the saved original lifts
after the permitted switch show why dropping the emptiness hypothesis would
be false. The paired-empty n=3 consequence is likewise not-triggered here.
No zero count is recorded as a theorem excluding a target source.

For fan B the paired-endpoint conditions are sharper and all use original
exterior edges. In row `01202`, the q/n palette is 13 and the only outer
anchor of that palette is y; in `01212` the palette is 03 and the only
outer anchor is x. If q and n were in different components, at least one
component would miss the entire original boundary. Switching it makes
q=n, giving a same-row original lift. Thus the paired endpoints must be
connected when the respective original fibre is empty.

In `01021`, rainbow forces q=3,n=1. The q-containing 03 component must
meet `{a,x}`; otherwise its switch makes q=a while fixing the outer row.
For palette 13, either q and n are connected or their separate components
contain c and y respectively: q is already connected to c by the actual
edge qc, and a separate n-component missing y could be switched to make
n=q. Every violating control is accompanied by the complete switched
colouring and its same-row original lifts. All these palettes avoid b, so
the added fan-B edges contribute nothing: the recorded components agree
exactly with the original exterior components. The fixed control exercises
six such `01021` records; its two other candidate fibres are empty, and
none of these controls realizes the assumed empty original fibres.
Five of those six records violate the proposed conditional contact;
their saved full lifts make the missing original-emptiness hypothesis
explicitly testable rather than implicit.

## Negative controls and boundary

Three deterministic mutations must be rejected by recomputation: changing
the claimed outer row, borrowing an exterior partition from another row on
the same graph, and falsely joining distinct actual components. A separately
corrupted output certificate must also fail `--check`. These controls retain
the requirement for one graph, one literal frame, and one complete witness.

Replay from the repository root:

```
python3 -B audits/2026-10-18-rainbow-exterior-e1617a2/C/check.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-18-rainbow-exterior-e1617a2/C/check.py --check
```

[validation.json](validation.json) records both successful replays and
rejection of a certificate whose first component record has a false row.

The earlier [certificate.json](certificate.json) is retained unchanged as
the v1 draft; the checker defaults to v2, which adds the fan-B paired
endpoint checks. This supplies a fixed-graph component replay and an
obstruction to using an accepting fan A for this four-query certificate.
It does not exclude the three rainbow fibres of
the fixed fan B, realize the hypothetical minimum source, prove smaller
badness or global closure, or establish a new Lean theorem.
