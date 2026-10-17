# Independent A review of active B

**PASS for the corrected narrow B1--B3 only.** The original all-six-cycle
claim failed; that review is preserved in REVIEW-B-initial.md. The active
proof now excludes the same-L_t mp branch and retains the crossed mq branch
as OPEN, requiring original c degree four and a degree at least seven.
It claims full six-cycle/six-cut exclusion only with the additional c>=5
hypothesis. This exactly addresses the identified source-lift failure.

The original outside p wedge consists of three consecutive actual faces
tpa,apb,bpq. Because a,b are original exterior vertices, it is the outside
wedge of the actual proper C5(t,p,q,h,w); the full p link therefore has no
extra outside neighbour. The actual bounded cap is empty or a single W5,
and both cases force p5,a4, excluded by the frozen low-p theorem. This
argument applies only to the mp same-sector branch. The active source-sector
records now distinguish that branch from the mq crossed residual.

The cyclic-six-cut bond argument is independently valid: a cycle-bearing
component has boundary >=4 when the other side contains a cycle, and any
additional component contributes >=3. The resulting simple primal six-cycle
receives exactly the corrected classification. Full reflection is also
kept honest: mask933 maps to940, and no unadmitted w5 claim is made.

The checker was read at its source_sector_cases and cap routines, then
independently replayed successfully. That replay validates local records;
the source-lift argument was checked separately above. All original full
fibres and empty v lifts remain in the claim. No source supplied, no finite
zero extrapolation, no positivity or completed-source descent is asserted.

Reviewed active SHA256 values:

- PROOF.md: `1aa870a0e957168de7f269d90e8ebad6c4c5c34ea9564a17d99fe01ff975f6b7`
- check.py: `099b0eb90b655e7b97aaeff15b7aa4ba372936b084d272a7aa6a4a2601c579c5`
- certificate.json: `6328d7235209ee52be3073b1ff1471b9cc3b76e27b3f6ff98cd235eec0f18c3b`
