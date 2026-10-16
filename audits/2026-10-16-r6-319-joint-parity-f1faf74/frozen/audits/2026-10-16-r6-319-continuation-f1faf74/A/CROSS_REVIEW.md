# A worker cross-review

The review is read-only outside A/. No actual minimum source is supplied.

## B: protected outside arc

PASS on B/PROOF.md Sections 1--6 and an independent replay:

```
python3 -B audits/2026-10-16-r6-319-continuation-f1faf74/B/verify.py --check audits/2026-10-16-r6-319-continuation-f1faf74/B/certificate.json
```

The one-port case has two internal M0 edges. Removing them from the one
simple Q rules out pairing12/34; Jordan separation in the exterior disk
rules out13/24. Thus the exterior arcs are14/23. The23 arc starts and
ends with non-M0 ports, so replacing it with edge23 preserves actual
alternation, one simple cycle, and avoidance of e,g. It strictly shortens
Q because the removed path has at least three edges. If it retained f,
it would contradict the actual minimum-length choice. This proves the
protected-f conclusion and does not prove even complement or repair.

Replay returned32 port fibres,11 nonempty,30 local complete Tait rows,
186 one-port cases and193 three-port cases. Full fixed-alpha empty
fibres and source `not triggered` are retained.

## C: induced-five-cycle theorem

C1.1--C1.4 have the stated literal original-cycle lifts and cap argument.
For C1.5, a J star centre adjacent to both hubs must be alpha or beta.
Its link has the compatible sector incidence unless the literal
endpoint equals p or q. In that case it loses exactly the original b
edge, giving J degree5 and original degree6. This is the essential
exception; replacing it by original degree5 would be wrong.

The chorded-C5 ear/core argument in C2 is sound for an actual selected
chord: all triangles facial, removal of its dual leaf preserves cyclicity,
and a chorded four-core would have a tree side. The initial final
marked-ear corollary required extra justification: two chords can expose
opposite facial ears. This was reported to root and C before adoption.
The source's old exact common-neighbour identities provide a stronger
route: no C5 contains e,g, while f,g cases need either a direct small-cap
argument or explicit noncyclic-core analysis. This note records the issue,
not approval of any later revision not yet read.

### Final revised C and C3: PASS

The revised C2 argument and C/MARKED_CUTS.md were subsequently read and
accepted. The ear statement now asserts existence. If neither zp nor
zq is a C5 edge, the three actual faces zAp,zpq,zmq form a pentagon
disk with a dual tree side; otherwise the zpq ear gives the required
cyclic C4 core. In the core `(m,z,q,A)`, inducedness excludes mq and
zA. The exact common-neighbour formula leaves only repeated z/p or
the fan midpoint j_c adjacent to z, all excluded; reflection handles
the other orientation. C3's no-eg-C5 proof correctly uses the sole
common neighbour m. Thus every source cyclic five-cut crosses at most
one marked edge. The earlier initial wording concern is resolved.

Independent successful replays:

```
python3 -B audits/2026-10-16-r6-319-continuation-f1faf74/C/check.py
python3 -B audits/2026-10-16-r6-319-continuation-f1faf74/C/check_marked_cuts.py
```

The active main C certificate is v2. Its alpha=p/beta=q crossed-star
controls preserve original degree6/J degree5. The added hash custody
uses ADDITIONAL_INPUTS.json and leaves the original BASE unchanged.
Neither C3 nor these controls assert even-complement repair or source
realizability; source checking remains not triggered.
