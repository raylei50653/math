# C independent review of B full-colouring transport

2026-10-18. Reviewed [B/PROOF.md](../B/PROOF.md), its complete lift cases,
and [B/check.py](../B/check.py). Replayed the checker successfully: first
stages 3/3, second stages 12/12, eight rho domains with 12 partitions each,
and all 84 proper literal C4 assignments; negative controls passed.

**Pass.** The following points were checked separately from B's finite output.

- The quotient restriction really determines the full E colouring and b:
  `b=n`. Recovering that E colouring recovers the quotient colouring, even
  when the quotient identifies an interior vertex with original boundary b.
- In the tau map, the q-component switch in `{2,3}` and the a-component
  switch in `{0,2}` are uniquely named actual components. Undoing the second
  switch first reconstructs the precise intermediate colouring on all
  private E vertices; only then is the first switch inverted. The two
  displayed image boundary patterns differ and cannot collide.
- In the rho map, n and q are separated before switching. The `q=3` branch
  lands in the other original forbidden row regardless of whether the
  anchor with colour i moves. In the surviving `{0,1}` switch, edge xy makes
  the two anchor colours move together. The contact bit H is computed from
  the target's actual component, not chosen separately. The palette-induced
  graph is unchanged by the component switch and by global 0/1 renaming,
  so `i=t XOR H` recovers the source row. The distinct Q1/Q2 image patterns
  recover the other domain label. Thus the four-domain injection preserves
  full-colouring multiplicities; it does not assume boundary marginals are
  injective.
- Each topology claim is within one current full colouring, with two
  disjoint palettes and ordered contacts. No path is carried from one
  unrelated colouring to another.
- The degree-four equation counts the overlap twice because a two-colour
  C4 has two h lifts. It is an exact count sum, not a disjoint support sum.
- The standalone `A_b>0` consequence under global minimum badness is valid:
  the same accepted quotient receives all three empty-fibre conclusions,
  retains the original frame, and has the proved completed size k-4.
  Its use of the four-row outside-K132 test must retain the frozen catalogue.

Integration observation: together with C's independently proved count
inequality, `A_b>0` for 932/933 does not need minimum badness. If `A_b=0`,
B's rho injection empties both rho fibres of Q1 and Q2. Every original
accepted witness is then in the h=a sector, so the earlier same-witness
cover makes Q1 or Q2 accept. C forces that same quotient's `01212` count
positive, a contradiction. This observation strengthens the combined
source-level conclusion and does not invalidate B's standalone argument.

No actual E is constructed by the partition checker. Original source
existence, smaller bad descent, and the 941 residual remain separate.
