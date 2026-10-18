# Independent review of A's local-context obstruction

2026-10-18, BASE `9f1fe84f73aabfa87a33d28754633bae6bf0b707`.
Reviewed A/PROOF.md and A/check_hexagon_obstruction.py, and independently
replayed the frozen certificate. Its reproduced SHA-256 is
`f2cad7410cc0a7a444838613847c839bd631f12d92bfedbccf235823bb2a226d`.

The two-rejected-context lemma is valid with its stated restricted exterior
information. Every proper rim has a!=b and q!=b. If q=a, one common colour
permutation sends a to 0 and b to 2; choose c=1 and the complete outer row
01021. If q differs from a, the three colours are distinct; send
(a,b,q) to (2,0,1), choose c=a, and obtain outer row 01202. Both cases
satisfy qc. Any local old-patch lift pulls back by the inverse of that
same common permutation. Thus safety on both partial contexts implies
full local containment. This does not infer anything about whether the
same tuples occur in the actual complete exterior.

The direct old-fibre formula, the pair of fan constructions, the accepted
row cover and the rainbow gate agree with independent B/C calculations.
The literal counts 732 proper rims and 300 old accepted rims also agree
with B's canonical-fibre data after one common rim permutation.

The zero/one-centre equality/inequality family is correctly limited to its
stated noncrossing maximal shape construction. A nonempty assignment has
no equality chain collapsing an inequality edge, since that would force
an empty colouring relation. Allowing equality is a larger relation
family than ordinary fixed-distinct-pin patches; the no-go statement does
not claim that every quotient automatically retains all original source
geometry. The numbers 14/84 maximal shapes and 112/545 signed assignments
were reproduced, with 70/365 nonempty and zero sound nonempty candidates.

The three-centre and four-centre examples have the stated degree-five
vertices and admit planar hexagon realizations from their cyclic rim
neighbour arcs. The two-centre replacement annex is an explicit named
finite family; A does not claim it exhausts every possible two-centre
gadget. Its stored complete fibres and leaking witnesses replayed.

One documentation custody clarification was requested: the opening text
originally said the root INPUTS freezes active-f-seven/B/PROOF.md, whereas
that additional authority was not in the root manifest. A can either
freeze that exact file locally or cite the same site facts from the
already frozen active-f-seven/A/PROOF.md in B/C. This does not affect the
independently reconstructed graph or fibre calculations.

Replay:

```
python3 -B audits/2026-10-18-smaller-source-9f1fe84/A/check_hexagon_obstruction.py
```

Conclusion: mathematical claims accepted in their stated domains; actual
source occurrence and globally empty rejected fibres remain OPEN.
