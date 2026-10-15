# Round4: a complete common-graph two-sheet cover

[PROOF.md](PROOF.md) gives a genuine connected75-vertex,353-edge graph with
exactly864 complete four-colourings. They project two-to-one onto the old
432-state Layer0; all six component partitions, every actual visible switch,
whole cubes and global S4 action agree on the same original graph. All seven
pins are distinct and **no two-colour component is hidden**. A second121-vertex,
711-edge graph independently realizes the same kind of cover.

A six-switch closed base walk exchanges the two full colourings above state0.
There is therefore no compatible section. This answers the main new question:
the preceding single-valued25-type obstruction cannot be lifted to all finite
covers by presuming a section. Here a real graph supplies the cover despite
that obstruction.

The two graphs' complete normalized colourings were exhaustively enumerated
(36 each) and compared tuple-for-tuple with the864 lifted states after S4
expansion. Original-edge BFS checks8,160 component switches and26,112 cube
masks per graph. Separate root/geometry implementations confirm the complete
colouring sets and all components. The main witness is [graph-75.json](graph-75.json),
with full replay in [check.py](check.py) and [certificate.json](certificate.json).

Further paper results give the exact hidden-component bound
`m_pin >= sum_P 2^(h_ab+h_cd) - 2` and a complete linear parametrization of
abstract two-sheet visible-cube/S4 covers. The bound refers to the entire
literal-pin-row fibre unless hidden switches are explicitly required to stay
in an abstract-state fibre. There are2^117 abstract cover classes for the full
720 table; the additional zero-hidden-product subdomain has2^13 classes.
Those numbers are not graph-realizability counts.

Both displayed graphs are nonplanar and cover only Layer0's18 canonical rows,
with outer mask319. They do not settle the full720/22-row relation, any planar
alternative, the original degree/collar source, omega=0 or the general main
claim. Those remain OPEN. No commit/push was performed.
