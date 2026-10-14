# Independent review: the entire original r-degree-five branch is impossible

2026-10-14. Independently checked against the frozen source geometry and
the frozen complete-fibre refinement. This is stronger than the local
degree-three deletion lemma in [PROOF](PROOF.md).

## Reviewed implication

Let R' be the actual plane disk with outer cycle `(z,s,v,t)` produced by
the frozen original `d_G(r)=5` deletion. Its exact mask is 7, and in every
complete colouring its prescribed pq palettes are ABAB/CD, ABAC/BC,
ABCB/CD. In particular ABAC has a complete lift and ABCD has none.

Fix any complete ABAC colouring f:

`f(z)=f(v)=A, f(s)=B, f(t)=C, {f(p),f(q)}={B,C}`.

1. The vertices z,v lie in the same maximal AD component. Otherwise,
   switching the entire AD component of v leaves z,s,t unchanged and
   gives boundary `(A,B,D,C)`, a forbidden four-colour boundary. This
   proves actual same-colouring connectivity, not a separate existence
   statement. Since p,q have colours B,C, that switch would also fix them,
   though the rainbow contradiction needs no pq information.
2. The vertices s,t cannot lie in the same BC component. If they did,
   an AD z-v path and a BC s-t path would be vertex-disjoint paths with
   alternating endpoints on the actual outer Jordan cycle. Planarity
   prohibits this. This argument uses four original boundary vertices;
   the internal pins are not treated as a fictitious outer boundary.
3. Switch the entire BC component containing t. By step 2 it avoids s;
   it automatically avoids z,v because they have colour A. The new
   boundary is exactly `(A,B,A,B)`.
4. The actual edge pq puts p and q in one BC component. The switch in
   step 3 therefore changes either neither endpoint or both endpoints.
   In both cases their unordered palette remains `{B,C}`. The resulting
   ABAB colouring contradicts the universal required palette `{C,D}`.

This is a contradiction within one actual full colouring and its Kempe
images. It does not count colourings, identify colourings, replace a
source by a support representative, or require Kempe graph connectivity.
Every component switch is proper and invertible on its own component.

## Premise and dependency check

- The frozen SOURCE_GEOMETRY section 5 supplies the simple induced outer
  cycle, actual edge pq, strict original size, and mask 7 using the
  source-relative C4 classification.
- Its ABAC/BC condition comes from all original r lifts and the original
  cap failure condition. Its ABAB/CD condition additionally uses the
  compulsory-missing-colour theorem in frozen JOINT_FIBRES section 3.
  Omitting that theorem would leave the starting premises unproved.
- Exact mask 7 guarantees the ABAC lift. The contradiction itself only
  needs an ABAC lift, no rainbow lifts, ABAC/BC and ABAB/CD universally,
  the edge pq, and the Jordan disk embedding.
- No degree conditions on s,t,p,q beyond those used to construct R'
  enter the Kempe proof. No claim about all abstract six-pin relations
  or arbitrary drawings follows.
- All original interior degrees are at least five. Therefore excluding
  degree five gives **`d_G(r)>=6`**, conditional only on the original
  `d_G(x)=d_G(y)=d_G(b)=4` no4ct minimum-source branch. The previous
  `r=5 => s,t>=6` lemma is consequently superseded at source level.

Review verdict: the proof is valid under the frozen named-source
premises. It closes the original r-degree-five subbranch. It does not
exclude the remaining mask13 branch with r of degree at least six, prove
a general returning injection, or establish the unbounded catalogue
theorem.
