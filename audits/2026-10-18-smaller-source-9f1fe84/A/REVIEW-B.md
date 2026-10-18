# Independent review of B's fixed-rim construction

2026-10-18; reviewed B/PROOF.md, B/check_patches.py and the replayed B/patches.json.
The replayed checker SHA-256 was
`a2015fe9193e2402992d33f8bc85393b4dff21339c95181d0d33af9b366a9dde`.

**Accepted within its stated scope.** The two-centre five-rim patch has support
567 and the zero-centre fan 13,14 has support 564. The explicit lift h=beta(1),
u outside the colours of beta(0),beta(1),beta(2) checks every actual edge and
fixes the complete rim. This establishes arbitrary-exterior rejection safety;
accepted-query preservation still needs the stated original full witness.

The paper classification for arbitrary zero/one-interior C5 patches is valid.
The two absent three-colour rows force `(03 or 14)` and `(13 or 24)`. The
crossing pair 03,24 is impossible. With 14 absent, the remaining 03,13 leave
01231 alive: its only repeated nonadjacent colour pair is 1,4, and its unique
colours at 0,2 are separated by chord 13. With 13 absent, the symmetric
14,24 leave 01213 alive, using separation by chord 14. If both fan chords
are present, every interior vertex lies in one triangle and cannot kill any
fan colouring. The argument includes nontriangulated patches and isolated
interior vertices; it does not include identifying distinct rim pins.

The C6 finite completeness argument also checks. Adding edges to a fixed plane
patch gives a maximal triangulated disk on the same labelled rim and vertices.
With one interior centre, its cyclic neighbour set and independently
triangulated outside sectors describe every maximal embedding. The checker
keeps all edge subsets, deduplicates only identical labelled graphs, and uses
their actual complete colouring relations. Canonical rows expand by one common
S4 permutation of the entire lift. All 45 zero-interior and 1,148 one-interior
graphs have stored leaks.

A's independently written literal-tuple checker obtains the same 14 and 84
maximal hexagon shapes and zero nonempty sound replacements, and additionally
tests noncrossing equality assignments. The two original C6 caps agree after
the common rim permutation `(2,1,0,5,4,3)` from A coordinates to B coordinates.
Both have 300 literal accepted rim tuples. This is an independent relation
calculation; neither A nor B imports the other checker.

The source distinction is necessary and retained: B's (4,5) cap is in J,
whereas the original source has the larger (5,5) cap and an additional b
constraint. B does not claim its fan already lifts to a smaller original bad
source. C's separate completed k-2 pair construction is compatible with B's
no-go because C has not proved local or complete-exterior rejection safety.

Replay completed successfully:

```
python3 -B audits/2026-10-18-smaller-source-9f1fe84/B/check_patches.py --check audits/2026-10-18-smaller-source-9f1fe84/B/patches.json
```

No correctness finding requiring a change was found. The unsolved original
source gate and source occurrence obligations must remain explicit.
