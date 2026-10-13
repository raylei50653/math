# Independent review of the common-joint matrix paper

Reviewed `../paper/REPORT.md`, Sections 1-5, against the frozen original55
capacity and partition inputs. This is an independent paper review, separate
from runtime checks of `../joint/matrix.py` and from the author's review of the
zero/one-spoke topology proof.

**Verdict: the stated implications are sound with their explicit necessary-only
and full-source boundaries.**

The two conditional capacity bounds refer to complete original fibres and
retain actual repeated root incidences. Restricting the pins to the legal
external rectangle cannot increase forbidden-color counts. The collision
theorems use actual boundary neighbors of actual contacts; one piece accepts
the entire selected row or column by strict degree-list slack. The other
piece's conditional capacity then supplies a complete lift at the same ordered
pins. The signature closures are literal three-row constraints, not independent
piece normalizations.

For Theorem M, a one is correctly assigned to P's rejected cell. Therefore
P-certified accepting cells are forced zero and Q-certified accepting cells
are forced one. A fixed r row has at most `k_P^s` ones and at most `k_Q^s`
zeros, so its lower bound is `|E_s|-k_Q^s=k_P^s-1`. The column argument uses
the r incidences. Arbitrary choices on cells rejected by both pieces still
obey these bounds: every assigned cell is contained in the corresponding
actual forbidden set. Conversely, feasibility is not presented as sufficient
for the original rejection or for source realization.

After forced-one counts are removed, the four residual bounds in Section 4
are correct. In the first cut inequality, required ones in rows R either use
columns T or free cells in `R x (E_s-T)`; in the second, required ones in
columns T either use rows R or free cells in `(E_r-R) x T`. The complements
and the use of opposite upper bounds are correct. A negative upper bound
is already an impossibility. Joint sufficiency of these inequalities is
explicitly not asserted, so no additional flow theorem has been silently used.

LL-CUT is a precise stronger route to a common joint because its unstrengthened
S sets depend only on named incidence/attachment data and shared contacts.
Its `+diag` variant is distinct and requires reconstruction of actual complete
lifts before a cell is certified. The paper correctly requires a single
qualified original source and three literal-row feasible matrices to refute
the full-source proposition. Matrices from different graphs, finite relaxed
controls, or marginals of different lifts would not do so.

The new zero/one-spoke exclusions leave only the following canonical source
residual, in addition to all original full hypotheses:

| Original actual support sizes | Total root spokes |
| --- | --- |
| `{3,3}` | `t=2` or `t=3` |
| `{3,4}` | `t=2` |

At least one long still has at least four original root incidences. Neither
this review nor the matrix theorem closes those cases. The finite controls
and the existing all-diagonal-failure four-contact path cannot replace a
full-source proof or refutation of LL-CUT on this residual.
