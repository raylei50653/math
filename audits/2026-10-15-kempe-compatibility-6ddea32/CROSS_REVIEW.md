# Read-only cross-review: six-pin forcing paper argument

Reviewed the sibling PROOF.md, especially sections3--4, against the frozen
small-C4/proper-C5 theorem, low-p/q proof, original apex geometry and the
r6 collar-neighbour lemma. No files in the sibling audit were changed.

Reviewed proof SHA256: `94637ed0ee7ba0cf2c765dbd3d5abe48dc9697c279438cb355b16444e47b435b`.

1. For a second common s/t neighbour j, the cycle `(x,s,j,t,y)` uses the
   original boundary edge xy. The bounded x-sector is the one containing
   xr in the original order `(y,r,s,c)`. Therefore r is strictly inside;
   small-C5 gives degree5, contradicting r6. The later z common neighbour
   comes from identifying a,c, not from an original common B neighbour.
2. For a second s/p neighbour j distinct from q, `(s,c,b,p,j)` uses the
   original boundary edge bc. The bounded b-sector contains bq in order
   `(a,p,q,c)`, so q is strictly inside. Small-C5 forces q5 and qs;
   qs forces c4, contrary to the existing q5 implies c>=6 theorem.
3. When tp is absent, the bounded sector of `(t,a,p,j)` avoids ay and ab.
   The C4 interior is empty, so aj is the required diagonal; its two faces
   fill the original inner a-sector. This proves the exact a5 fan, not
   merely existence of an extra neighbour.
4. The exceptional indicators a5 and c4 cannot both hold: they would give
   h=(5-4)+(4-4)=1, whereas the inherited source has h>=3. The reflected
   statement has the same scope.
5. The counts for I_d and H_d suppress only the duplicates forced by the
   exact common-neighbour sets. The final K quotient is separately counted:
   z and e then have only the merged class as common neighbour, so exactly
   one further duplicate is suppressed; the added remaining forcing edge
   is an original nonedge. Thus final nonplanarity is established directly,
   not inferred from nonplanarity of an intermediate quotient.

No substantive gap was found in these paper steps. This review does not
claim a Lean verification or finite certification of arbitrary embeddings.
The sibling checker's whole-fibre tests are a separate verification layer.
