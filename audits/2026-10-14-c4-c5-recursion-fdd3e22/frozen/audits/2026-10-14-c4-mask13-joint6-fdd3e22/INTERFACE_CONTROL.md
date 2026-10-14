# Necessary Kempe control on the six original pins

This finite control strengthens the old support-only negative control and
tests the joint conditions in the frozen [ADJACENT4](frozen/audits/2026-10-14-c4-triangle-core-b66f592/ADJACENT4.md).
It confirms the exclusion of the ABCB rows with pq=BC or CB. The other eight
fixed-Q rows survive the stated necessary conditions. This is not a graph
construction, a source-realizability claim, or a proof that the residual exists.

## 1. Complete finite domain

The six original pins have order `(z,s,r,t,p,q)`. The mandatory skeleton edges
are `zs,sr,rt,tz,zp,pq,qz`. All `4^6` labelled assignments are checked directly.
Retain exactly the assignments that satisfy these edges and the old joint
obstruction:

| Fixed Q | Retained ordered pq before Kempe filtering |
| --- | --- |
| ABAB | CD, DC |
| ABAC | none |
| ABCB | BC, BD, CB, CD, DB, DC |
| ABCD | BD, DB |

There are 216 labelled assignments, or nine orbits under one global S4
renaming on all six pins. Every retained assignment uses at least three
colours, so its S4 stabilizer is trivial and each orbit has 24 members. The
ten entries in the fixed-Q table differ from
the nine full orbits because the two ABAB entries are globally equivalent by
swapping the unused boundary colours C and D.

For each row and each of the three partitions of the four colours into two
complementary pairs, enumerate every set partition of the terminals bearing
each pair. Such a partition records the intersections of Kempe components
with the six pins. A component meeting no pin can be omitted because switching
it leaves the six-pin row unchanged.

Reject a partition if it separates the ends of a mandatory skeleton edge
whose endpoint colours belong to the same pair. Reject the combined pair of
partitions if it connects z to r in one block and s to t in a distinct block.
The latter is impossible for vertex-disjoint paths in a disk with Jordan
boundary `(z,s,r,t)`. The test also applies when the two blocks belong to the
same colour pair. Internal p and q remain in their actual component blocks;
their location inside the disk supplies no additional noncrossing constraint
in the adopted control.

## 2. Switch closure and exact quantifiers

For a candidate combined partition, switch any subset of its components.
The two complementary colour pairs are disjoint, so these switches commute.
Enumerating all subsets gives its entire six-pin switch orbit, with one
global colour normalization per resulting row.

Starting with the nine possible full orbits, repeatedly remove a row if
there is some complementary colour-pair split for which **no** candidate
partition has its **entire** switch orbit inside the current relation.
Equivalently, a surviving row satisfies:

`for every complementary-pair split, there exists a permitted terminal
partition, for which every subset switch remains in the surviving relation`.

The existence of an actual full colouring gives the actual component
partition for each split, and every switch is another full colouring of that
same graph. Thus this fixed-point condition is necessary. The converse is not
proved. The choices for different splits and rows need not arise from one
graph, and the control does not store full interior colourings or multiplicities.
In particular, it must not be read as a replacement theorem for full fibres.

The procedure removes `ABCBBC` and `ABCBCB` on its first pass and then stops.
The resulting table is:

| Fixed Q | Surviving ordered pq |
| --- | --- |
| ABAB | CD, DC |
| ABAC | none |
| ABCB | BD, CD, DB, DC |
| ABCD | BD, DB |

This is eight fixed-Q rows, seven global S4 orbits, and 168 labelled
assignments. All three required outer types remain present. Every surviving
row has at least one retained partition for every complementary-pair split.
The [certificate](controls/interface.json) records **all** such partitions and
their complete switch successor sets, using pin indices 0 through 5 in the
order above.

This replaces the old three-row abstract negative control at this stronger
level: its ABCB row with pq=BC fails a necessary Kempe condition. The full
surviving relation is an abstract countercontrol to deriving emptiness from
these specified conditions alone.

## 3. Replay and negative controls

Run:

```sh
python3 -B audits/2026-10-14-c4-mask13-joint6-fdd3e22/controls/check_interface.py --check
```

The checker enumerates the finite domain, every component partition, every
subset switch, and the fixed point. It compares the complete deterministic
output and script hash with the saved certificate. It also checks the 203
set partitions of a six-element set as an enumeration sanity check.

Its deliberate negative controls reject the removed BC row, an alternating
outer partition, a partition splitting a mandatory edge, and an ABAB row
with the wrong pq palette. `--certificate PATH` permits an independent replay
against a deliberately altered certificate. The preserved
[stale-certificate log](controls/interface_stale_negative.log) changes the
surviving labelled count from 168 to 169 and confirms the replay rejects it.

## 4. Rejected pinched-boundary model

The initial exploratory model treated the weak boundary walk
`z,s,r,t,z,p,q` as an ordinary Jordan boundary and identified the two z
occurrences in every component partition. It incorrectly removed all rows.
Cutting at z can split the Kempe component containing z between the two
copies; the naive test forbids that possibility and is too strong.

The script, output and log are retained under [rejected](rejected/README.md).
They are labelled rejected and are excluded from the adopted finite result.
The authoritative control uses only the honest outer C4 boundary. No
conclusion about impossibility follows from the rejected empty survivor set.

Status: necessary finite control PASS; actual target sources 0. Source
realizability, the full joint residual, arbitrary-size extension, and Lean
formalization remain unproved by this control.

## 5. All subrelations and the optional original edges

The complete seven-orbit upper relation is not forced. The additional
[subrelation checker](controls/check_subrelations.py) tests all 128 subsets
of its seven orbits, requiring outer support exactly 13 and the same
necessary component-switch closure for every included row. Write

```text
C = {ABABCD, ABCBCD, ABCBDC}
U = {ABCBBD, ABCBDB}
V = {ABCDBD, ABCDDB}
```

Here every word records `(z,s,r,t,p,q)` under a single global colour
normalization. Exactly nine subsets pass. They are precisely

`C union U' union V'`, with nonempty `U' subset U` and nonempty `V' subset V`.

There are four minimal sets of five orbits, four sets of six orbits, and the
full seven-orbit set. Thus the necessary abstract closure forces both ordered
CD assignments in ABCB, but does not force both BD assignments in ABCB or
both assignments in ABCD. This agrees with the precise transport rule in
[JOINT_FIBRES](JOINT_FIBRES.md), whose second bijection can reverse pq order.

The original geometry permits the extra edge tp or qs in certain degree
subdomains. The checker separately requires its endpoints to differ and
puts them in one component whenever their colours belong to the same pair.
It then redoes the fixed point and all 128 subset tests for each edge case:

| Additional mandatory edges | Closed mask13 subrelations |
| --- | --- |
| none | the nine sets above |
| tp | uniquely `C union {ABCBDB, ABCDBD}` |
| qs | uniquely `C union {ABCBBD, ABCDBD}` |
| tp and qs | none; the greatest surviving relation is C and lacks ABCD |

The last case is already outside the source geometry because both edges
would force h=0. It is retained as a consistency control, not a new source
exclusion. None of these abstract subrelations is asserted to be realized
by a plane graph, a common system of maximal components, or the target source.

The original interface checker and certificate remain unchanged. The new
[certificate](controls/subrelations.json) records both of their hashes, the
four finite domains and iterations, every accepted subset, and the minimal
sets. Its helper functions are imported from the interface checker, so this
is a further exhaustive finite calculation rather than an independent
implementation of component-switch semantics.

```sh
python3 -B audits/2026-10-14-c4-mask13-joint6-fdd3e22/controls/check_subrelations.py --check
```
