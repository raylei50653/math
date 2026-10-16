# C final step: compulsory complete H fibres which cannot restore v

This addendum leaves the sealed `PROOF.md`, `check.py` and `certificate.json`
unchanged. It uses the same source, actual H, two genuine C5 completions and
the58-row necessary H relation established there. No larger graph search is
performed. Full319 and the original-v-degree-five exclusion remain OPEN.

## 1. Six compulsory rows, with actual complete witnesses

**Theorem C6 (same-source existence, via finite necessary exhaustion).**
Assume the same source has original v degree five. In the fixed literal colour
frame with `z=A`, `s=t=B`, each of the following12 local assignments has a
nonempty fibre of **complete** H colourings:

* `(j,i,w)` is any permutation of `(A,C,D)`;
* the ordered `(p,q)` is either `(C,D)` or `(D,C)`.

Every one of these complete H colourings has an empty v lift fibre, since
s,j,i,w use all four colours. This is an existence theorem for genuine
complete H colourings conditional on the source; the finite model is not
being declared realizable on its own.

Proof. In canonical order `(z,s,j,i,w,t,p,q)`, the12 literal rows modulo one
common C/D exchange are the following six distinct rows:

```
ABACDBCD   ABACDBDC
ABCADBCD   ABCADBDC
ABCDABCD   ABCDABDC
```

Suppose any one canonical row is absent from the actual complete H relation.
The true relation then lies in the previously proved58-row upper relation
with that row deleted. Repeat exactly the sound six-boundary maximal
component exhaustion from the sealed proof. In all six cases the stable
necessary relation has40 rows and these three complete-support upper bounds:

`(Sigma(V_i), Sigma(V_j), all-v-lift Sigma(U)) <= (1022,1022,63)`.

Each original source mask932,933,941 was fixed separately before taking
the common58-row upper relation. No row-by-row source-mask choice occurs.
The contradiction below uses only the third support bound and U bit8; it
does not need an additional assumption of independent cap witnesses.

The third bound omits bit8, the actual original U row ABCDB. But full
`Sigma(U)=319` includes that row. Any of its actual complete colourings
restricts to an H colouring and appears in its complete v fibre, contradiction.
Thus each of the six canonical rows has a complete H witness. Applying the
single global C/D exchange gives the12 fixed-A/B assignments stated above.
No private vertices from different witnesses are combined, and no equality
of the twelve complete-fibre cardinalities is asserted. QED.

All58 single-row deletion tests, including the52 that do not force a
contradiction, are retained in `final-step-certificate.json`. The six
positive existence conclusions therefore follow from explicit infeasibility
of their respective absences; they are not selected rows of a surviving
abstract relation.

## 2. The final actual quadrilateral quotient remains open

The same H slice s=t is exactly the complete-colouring relation of

`K=J-v`, with original boundary `(m,j,i,w)`.

The old exact s/t common-neighbour formula ensures the quotient only
suppresses the duplicate mz edge. Since v has degree four in J, deleting
its star exposes this actual four-cycle. The vertices z,p,q remain inside,
and the edges mz,zp,zq,pq all survive. The local ordered K pins are
`(m,j,i,w,z,p,q)`.

Projecting the full58-row H necessary relation to this genuine K slice
leaves34 canonical rows. A fresh necessary maximal-component screen uses
K's actual four-point Jordan boundary and the retained mz/zpq edges. It
deletes no row; all14 rows whose K boundary uses four colours survive.
Pulling that result back to H consequently leaves all58
rows, both1022 cap supports, and U support319.

This is the requested last same-source quotient check. In particular the
compulsory all-four-colour holes do not automatically yield a violating J
colouring: they are precisely empty v fibres. A full Kempe switch may make
v restorable, but the surviving quadrilateral options still allow the
restored colouring to satisfy the source relation. No oddness decrease,
W110/W101 endpoint, smaller bad source, or complete319 exclusion follows.
The source reconstruction cost remains k+5; no new external theorem or
Lean claim is made.

## 3. Verification and stopping boundary

`check_final_step.py` first verifies the preceding C seal, then replays all
58 absence tests and the separate K boundary calculation. It records the
full necessary K relation, including its empty v fibres, in
`final-step-certificate.json`. Default and seed17 replay, corrupted-result
rejection and exclusive-create rejection are recorded in
`FINAL_STEP_VERIFICATION.json`. The finite engine is explicitly reused;
this addendum does not claim to be an independent audit of that engine.
Actual minimum source instances supplied: zero, not triggered. The source
existence conclusions above are conditional proofs, not supplied instances.
