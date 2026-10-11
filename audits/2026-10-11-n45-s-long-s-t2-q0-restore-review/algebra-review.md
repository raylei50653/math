# Independent algebra and code review

Date: 2026-10-11. Target: `../2026-10-11-n45-s-long-s-t2-q0-restore/`.
This review uses the delivered REPORT §§3–4, `audit.py`, proof-calibration,
coverage, and the two negative-control certificates. It does not import the
delivered checker to derive independent answers, read other current workers'
conclusions, enumerate source graphs, or rerun the historical 19 controls.

## Judgment

The new conditional argument in REPORT §§3–4 and its bounded arithmetic/code
calibration have no blocking defect. Mathematical acceptance of the three
schedules additionally relies on the separate paper review of the inherited
zero-slack, N-diagonal, and accepted SF-QX premises. The arithmetic check does
not prove these premises, construct a source, or supply actual assignments.

At fixed s=3, exhaustive search over all 24 permutations of the four colours
gives exactly one transport for each ordered support:

| Piece | Ordered actual support | β values → target values | Unique map fixing 3 |
| --- | --- | --- | --- |
| L | 234 | 212 → q1:202 | π01=(0 1) |
| S | 40 | 20 → q2:10 | π12=(1 2) |

Both complete ordered pin bijections have all 16 positions, including diagonal
positions; together there are 32 maps. Applying a common permutation to every
vertex of the actual piece preserves all internal edge inequalities, actual
boundary attachments, and both root-contact inequalities. A contact shared by
r and s remains the same vertex. At s=3 the permutation fixes the s coordinate
and moves the r coordinate as stated. Thus the formal assignment transport
also preserves tuples, all preimages, and empty fibres for arbitrary piece size.

The three possible β columns from the inherited disjoint size-two partition
and `3∉D_S(β;3)` independently recompute as follows:

| β D_S | β D_L | q1 D_L | q1 permitted r | q2 D_S |
| --- | --- | --- | --- | --- |
| {0,1} | {2,3} | {2,3} | empty | {0,2} |
| {0,2} | {1,3} | {0,3} | {1} | {0,1} |
| {1,2} | {0,3} | {1,3} | {0} | {1,2} |

The first row makes every full q1 X pin empty. This contradicts the original
G(q1) acceptance, followed by restriction to X, for each of the assigned three
schedules. Both surviving rows have `2∈D_S(β;3)`, and their complete S transport
has `1∈D_S(q2;3)`. Since actual U and the retained s-spokes force s=3, all q2
r=1 fibres are empty. Conditional on accepted `Q(X)={β}`, a full q2 X lift
exists and every such lift restores the unique original `rb4`, because q2(b4)=1.
The use of original G(q1) acceptance avoids any claim that q1 is a new Δ recovery.

## Coverage and exact negative controls

The independent script enumerates the ten normalized proper boundary colour
rows and checks all ordered pin positions of all three delivered schedules.
Counts are 3 schedules, 30 rows, 480 pins, and 120 diagonal positions. Across
the three q2 rows there are 39 necessarily empty positions and 9 positions in
the collectively nonempty recovery pools: per schedule, 13 empty positions
and `(r,s)=(0,3),(2,3),(3,3)` in the recovery pool. These are metadata positions,
not actual fibre or assignment counts. No individual pool fibre is declared
nonempty.

The two corrupted artifacts differ from their originals precisely as follows:

1. `bad-q2-column.json`: `/cases/1/q2_D_S/1` changes 1 to 2. It removes the
   proved r=1 blocker from the second case, with no other mutation.
2. `missing-diagonal.json`: only the `(3,3)` pin is removed from schedule
   `B-933-0234`, literal `01012`; its pin list has length 15 rather than 16.

Read-only direct replays performed by this reviewer returned exit0 for ordinary
and seed17 checks, with identical output. The first negative returned exit1 at
`audit.py:256`, the equality with the recomputed calibration certificate, with
`calibration certificate mismatch`. The second returned exit1 at `audit.py:268`,
the equality with recomputed coverage metadata, with `coverage mismatch`.
These rejection stages check exact bounded certificates and coverage metadata;
they are not source-realizability rejection tests. Root supervision captures
fresh native replay logs separately in this review directory.

## Reproducible independent check and scope

Run `python3 -B independent-algebra.py` from this directory, or use its full
path. The script only reads target artifacts and prints JSON; it creates no
files. It uses independent S4 enumeration and set arithmetic rather than the
delivered checker implementation. Target source remains unexecuted,
`trigger_count=null`, status `not triggered`. No new source, source search,
Lean proof, general N45/N2/E closure, or conclusion for the other 21 necessary
schedules follows from this calibration.
