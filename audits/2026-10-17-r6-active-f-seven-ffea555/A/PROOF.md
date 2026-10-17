# A: original-degree exclusions for an active f nonfacial seven-cycle

Frozen BASE: `ffea555fc2a896d8166ce198ca28ed9262912f25`, 2026-10-17.
The authority list and exact frozen byte hashes are in
[INPUTS.json](../INPUTS.json). This independently audits sections 1–2 of
the proposed continuation. The conclusions below are arbitrary-size paper
lemmas, not finite exclusions of hypothetical sources.

## 1. One source, exact centres, and a naming correction

Keep the same minimum completed no4ct C5 source G, its ordered original
boundary `(x,y,a,b,c)`, supports 932/933/941, rotation, actual attachments,
and private vertices. Keep the complete U319 relation on ordered pins
`(z,s,v,w,t,p,q)`, every empty fibre, and every legal original r lift in
one common colour frame. Keep the actual `J=U/(s=t)`, `m=[s=t]`, its sphere
dual `D=J*`, and the literal marks

`e=(vw)*`, `f=(pq)*`, `g=(mz)*`.

No original `d_G(v)=5` premise is added. Put `a0=d_G(a)` and `c0=d_G(c)`.
All matching statements refer to ordinary perfect matchings of this same
D, including matchings with an odd complement and no complete colouring
lift. In particular, a zero colouring fibre is never discarded.

Fix any `M in P101`, so `e,g in M` and `f not in M`. Suppose that a
nonfacial seven-cycle component C of `D-M` contains f, and put `X=V(C)`.
The adopted [seven-cycle classification A2–A3](../frozen/audits/2026-10-17-r6-joint-positive-113e41f/A/PROOF.md)
gives exactly two adjacent primal centres: one `u in {p,q}` of J-degree
four, and an ordinary centre h outside `{m,z,v,w,p,q}` of degree five.
Their two dual facial disks have boundary C. Their common primal edge
gives the unique internal matching chord, and the other five matching
edges incident with X form `delta_D(X)`. Thus:

* `d_G(u)=5` and `d_G(h)=5`;
* the dual vertex of a primal triangle belongs to X exactly when that
  triangle is incident with at least one of u,h;
* a dual edge incident with primal centre u is on C unless its primal
  edge is the shared edge uh.

The middle assertion includes the two ends of the shared chord: both
incident primal triangles are retained boundary vertices of the two-face
union. There is no internal dual vertex to add to X.

When `u=p`, write its original facial link as

`(a,b,q,ell,n_a)`.

The low-p proof calls `n_a` by the letter `m`; that is a different
original vertex from the current hub `m=[s=t]`. We consistently rename
that old local vertex `n_a`. Its J-link is `(z,q,ell,n_a)`. Therefore the
only possible ordinary second centres are `h=ell` or `h=n_a`.
The literal reflection of the original disk exchanges
`(x,y),(a,c),(p,q),(s,t),(v,w)`; write `ell_c,n_c` for its corresponding two
private neighbours at q. No independent graph or colouring is substituted.

The adopted [original source geometry §2](../frozen/audits/2026-10-15-j-source-geometry-6ddea32/PROOF.md)
gives the following exact original-sector data. Let alpha be the first
inner neighbour after t on the a-sector toward p, and beta the first
after s on the c-sector toward q. Then

`alpha=p iff a0=4`, `beta=q iff c0=4`,

and the two actual faces on mz are `(m,z,alpha)` and `(m,z,beta)`.
The actual marked face `(z,p,q)` is retained throughout. The
[low-p/q lemma §§1,5](../frozen/audits/2026-10-14-lowpq-source-676b102/pq/PROOF.md)
gives `d_G(p)=5 => a0>=6` and `d_G(q)=5 => c0>=6`.

## 2. A forced matching edge when an opposite sector has degree four

**Lemma A1.** For every `M in P101`, independently of any seven-cycle,

`c0=4 => (pz)* in M`, and `a0=4 => (zq)* in M`.

**Proof.** If `c0=4`, the literal identity `beta=q` makes `(m,z,q)` an
actual triangular face. At its dual vertex, the selected edge
`g=(mz)*` rules out `(zq)*` (and `(mq)*`). At the dual vertex of the
actual face `(z,p,q)`, both `(zq)*` and `f=(pq)*` are absent from M.
The perfect-matching identity at that same vertex forces `(pz)* in M`.

If `a0=4`, use the actual face `(m,z,p)` supplied by `alpha=p`.
Its selected g rules out `(zp)*`. At the same actual face `(z,p,q)`,
both `(zp)*` and f are absent, so `(zq)* is selected. These are two
direct matching arguments within the fixed J,D. QED.

**Theorem A2.** If `a0=4` or `c0=4`, the complement of any `M in P101`
contains no nonfacial seven-cycle through f.

**Proof.** Suppose first that `c0=4`. If the degree-four cap centre is p,
the other centre h is not z. Hence the edge `(pz)*` lies on the boundary
C, by the exact two-face description in §1. Every C edge belongs to
`D-M`, contradicting Lemma A1. If the degree-four centre is q, its
original degree is five, contradicting `d_G(q)=5 => c0>=6`.

If `a0=4`, a q-centred cap has `(zq)*` on C, contradicting Lemma A1.
A p-centred cap contradicts `d_G(p)=5 => a0>=6`. These cases exhaust
the adopted classification. QED.

This excludes the whole named degree-four subclass at arbitrary size.
It uses neither oddness minimality, a reference matching, a spoke-count
restriction, nor an additional cyclic six-cut construction. It concerns
nonfacial active-f seven-cycles; facial active-f seven-cycles and other
odd components are outside its conclusion.

## 3. The adjacent original-sector centre cannot have degree six

**Theorem A3.** If the two centres are `p,n_a`, then `a0>=7`.
Under literal reflection, centres `q,n_c` require `c0>=7`.

**Proof.** The p-centred classification gives `d_G(p)=5`, so the adopted
low-p lemma already gives `a0>=6`. Suppose that `a0=6`. The entire
original facial link of a is then

`(y,t,alpha,n_a,p,b)`.

Indeed the prescribed endpoints are y,t and p,b, and n_a is the
original neighbour immediately preceding p; the six-degree assumption
leaves exactly one additional inner vertex, alpha. The listed six
neighbours are distinct. In particular `alpha != n_a,p`, and alpha is
an actual original inner vertex, different from the quotient hub m and
the identified boundary vertex z.

The consecutive original faces `(a,t,alpha)` and `(a,alpha,n_a)` survive
as the actual J faces

`T=(m,z,alpha)`, `T'=(z,alpha,n_a)`.

The dual vertex `T*` lies outside X: T contains neither cap centre p
nor n_a. The dual vertex `T'*` lies inside X because T' contains n_a.
Their common edge `s0=(z alpha)*` therefore lies in `delta_D(X)`, so
the adopted matching-spoke conclusion gives `s0 in M`.

However `g=(mz)* in M` is also incident with the same outer vertex
`T*`. The edges g and s0 are distinct because alpha is different from
m,z. A perfect matching cannot contain two edges with a common endpoint.
This contradiction excludes `a0=6`; together with `a0>=6`, it proves
`a0>=7`.

Reflect all original incidences simultaneously. The corresponding
degree-six c-sector has faces `(m,z,beta)` and `(z,beta,n_c)`; its
shared dual spoke collides with g at the former face. Thus `c0>=7`
for centres `q,n_c`. QED.

The distinctness of alpha from n_a is essential and comes from the
complete original degree-six rotation. It would fail if the degree-five
rotation were silently substituted: in that rotation alpha is n_a,
and the proposed face `(z,alpha,n_a)` would be degenerate. The adopted
low-p degree bound excludes that branch before this argument is used.

## 4. Exact residual degree table and authority

Combining Theorems A2–A3 with the adopted low-p/q lemma gives the necessary
conditions below. These are residual conditions, not existence claims.

| Degree-four centre in J | Ordinary five-centre | Necessary original degrees |
| --- | --- | --- |
| p | ell | `a0>=6, c0>=5` |
| p | n_a | `a0>=7, c0>=5` |
| q | ell_c | `a0>=5, c0>=6` |
| q | n_c | `a0>=5, c0>=7` |

The original boundary-degree lower bound is four. Thus the opposite-sector
bound five follows exactly by excluding its degree-four case; no stronger
degree bound is inferred in that position.

[check.py](check.py) exhausts small binary matching-incidence systems for
the two pairs of actual triangular faces used above. It retains every
local assignment, including empty constrained slices, and positive
countermodels when a matching-mark or cut-spoke premise is removed.
Its certificates calibrate local matching algebra only. They do not
construct a complete J,D, a source colouring, a hypothetical minimum
source, or any U319 fibre. The complete source relation stays unchanged.
Normal and seed17 read-only replays pass; a missing-row certificate and
an attempted second exclusive creation both reject. The commands, exit
codes and log hashes are retained in [VERIFICATION.json](VERIFICATION.json).

No genuine target source is supplied: source realization is **not
triggered**. The arbitrary-size exclusions are the paper arguments
above. Remaining active-f nonfacial seven-caps, other odd components,
H-connected repair regions, even-complement positivity, `W110+W101>0`,
complete319 exclusion, and the general theorem remain **OPEN**. There
is no new Lean theorem, external theorem, reconstruction, commit or push.
