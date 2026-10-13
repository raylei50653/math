# Independent review: W3-TRANSPORT

Reviewed `../t1/REPORT.md` and `../t1/check.py` independently of their author.
All mathematical claims in Sections 1–6 are sound under the stated fixed-slot
and retained-pin hypotheses.

1. A proper C5 uses exactly three or four colours. Its centre extends exactly
   the three-colour cells, with the unique missing colour. This concerns the
   ordered named tuple, not an independently normalized U assignment.
2. Equality of three-colour support gives a total relation by the Cartesian
   product of the corresponding nonempty fibres; conversely totality in both
   directions forces equality of support. No bijection or equal cardinality
   is needed. A colour-preserving relation cannot manufacture equality of
   geometric slots; the report correctly makes embedding compatibility a
   separate hypothesis.
3. The restored count is exactly `6+r`. Hence `r<=6` plus support equality and
   legal geometry would connect to the frozen twelve-internal-vertex result.
   No representative existence is inferred from transport alone.
4. Equality of the existential B projection characterizes only outer Sigma.
   The prism/triangulated countercontrol separates it from full named support.
   The second countercontrol correctly separates the annulus's outer Sigma
   from the restored wheel's outer Sigma.
5. A two-choice degree-two decoration proves that fibre cardinality is not
   an invariant demanded by this theorem. The report retains complete source
   fibres and states how its forward/backward full-lift relation is obtained.
6. The statement about arbitrary contexts is restricted to contexts retaining
   the wheel and attaching only through preserved pins; absent pins are not
   silently forgotten.

The four controls are explicitly synthetic. They do not establish a minimum
933/941 source or a universal small representative. The report also correctly
does not claim a realizing annulus pair separating three-colour equality from
four-colour support equality.

`PYTHONHASHSEED=17` read-only replay passed. This checker has no `--check`
option: its default mode is read-only, which was used. In a temporary copy,
an impossible all-zero lift was inserted in the first empty cell. The checker
rejected it. SHA256 hashes of every original checker/certificate/summary file
were equal before and after. The exact commands, outcomes and hashes are in
[`review_checks.json`](review_checks.json), reproducible with
[`review_checks.py`](review_checks.py).

No requested change is necessary. This review is a paper/code check and a
negative-control replay, not Lean formal verification or a new external
catalogue computation.
