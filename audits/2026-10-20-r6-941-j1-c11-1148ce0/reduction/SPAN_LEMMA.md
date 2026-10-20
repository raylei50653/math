# Same-source signed planar span: independent derivation

Fix the actual C11 disk `F'=G-{b,p,h,R,x,y,r}` and its ordered rim
`(a,n,u2,u1,L,q,c,s,v,w,t)`. For every proper rim colouring `t` by the
four fixed labelled colours, let `z(t)` be the number of complete proper
colourings of every remaining original vertex that restrict to `t`.
All original attachments and private vertices are included in this count.
Global colour permutations give bijections between the corresponding fibres;
therefore a canonical orbit representative indexes the same common count.

Let `E*` consist of every edge of F' except the eleven rim edges. The latter
are already proper in every `t` under consideration. Expand the product of
properness indicators on `E*` by inclusion and exclusion. For an edge subset
`A ⊆ E*`, let `π(A)` be the partition of the eleven rim vertices induced by
connectivity in `(V(F'),A)`, and let `q(A)` be its number of connected
components meeting no rim vertex. Then, exactly,

```
z(t) = Σ_{A ⊆ E*} (-1)^|A| 4^q(A) 1[t is constant on each block of π(A)].
```

This identity retains all vertices: even an isolated private vertex is one
of the `q(A)` components. Distinct blocks are allowed to receive the same
colour; the indicator imposes equalities only, exactly as the matrix `P`
in the counting discovery script does. The coefficients may be negative.
It would be incorrect to constrain them to be nonnegative.

The actual plane embedding makes `π(A)` noncrossing: connected components
are pairwise disjoint plane subgraphs, and alternating boundary contacts
of two different components would force an intersection inside the disk.
If any block contains consecutive rim vertices (including indices10,0),
its indicator vanishes on every proper rim colouring and it can be deleted
from the sum. Grouping all other subsets A by their partition gives

```
z = P c,      c_π ∈ Z,
P[t,π] = 1 iff t is constant on every block of π.
```

The partition set is the unrestricted noncrossing partitions of11 rim
positions with no adjacent equal block labels. It has1585 members in the
frozen enumerator. These are connectivity partitions, so they may have
more than four blocks. The state set, in contrast, consists of the7381
proper colour orbits using at most four colours. This proves the exact
signed-span equation for an arbitrary-size actual F', without a bounded
realizability assumption or any matching premise.

For the selected original W5 short path the source contract supplies one
complete F' colouring whose literal rim is
`(0,1,2,1,2,3,1,2,e0,e1,2)` with `(e0,e1)=(0,1)` or `(1,0)`.
The frozen canonical IDs are5093 and5100. Hence the actual count vector
satisfies `z[5093]+z[5100]>0`. Neither term separately is assumed positive,
and these counts are not replaced by the possibility of a local cap lift.

This lemma alone does not assert infeasibility. A numerical optimizer status
also does not establish a source exclusion; that requires a separately
checked exact algebraic separating certificate against all source equations
and inequalities.
