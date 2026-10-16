# Independent matching-branch review of the general seven-cut exclusion

BASE `120aae90cab8bc4881916adc598cf344f2f20f4b`. The reviewer authored
the exterior matching lemmas and the intermediate equality extension,
but did NOT originate the general excess/ear argument below. The root
agent supplied that argument for independent review after the narrower
I=5 proof was reviewed. This review distinguishes that provenance.

**Verdict: PASS.** The general argument excludes the entire seven-cut
101 barrier, with no bound on I, even interior vertices, complete degree
excess, or source order. Together with the adopted complete earlier 101
barrier exclusions and Tutte's theorem, it proves ordinary P101 nonempty
on the same original source. It does not establish an even-complement
member or W101>0.

## 1. Exact data and signs

For each complete J vertex u let s_u be its actual complete degree minus
its adopted parity-sensitive minimum. Every s_u is a nonnegative even
integer; their complete sum is Delta. Put Delta_i=sum of these s_u over
strictly interior disk vertices, beta_u=t_u mod two, and h_u=1 exactly
when an ordinary boundary vertex has no exterior neighbour, zero
otherwise. Set h=sum h_u. The disk and global identities are

`sum_Q t_u=8+I-Delta_i`,

`Delta=I+B-2 epsilon-10`.

The first is valid at arbitrary complete degrees: an interior degree
is 6-o_u+s_u, so its contribution to interior curvature is o_u-s_u.
Neither identity assumes the equality Delta=2(1-epsilon).

## 2. Every boundary inequality was independently checked

For an ordinary boundary vertex, its complete degree is
`6-beta_u+s_u`. Its number of exterior neighbours is
`d_J(u)-d_R(u)=4-beta_u+s_u-t_u`, a nonnegative EVEN integer.
If it vanishes, u has exactly one actual exterior face, its triangular
ear, and h_u=1. Otherwise it is at least two. Thus exactly the needed
uniform bound holds:

`t_u <= 2-beta_u+s_u+2h_u`.

For v,w,p,q the complete degree is `5-beta_u+s_u`. The corresponding
exterior-neighbour count is nonnegative and ODD, hence at least one.
It gives `t_u<=2-beta_u+s_u` without an ear term.

For z, its complete degree is `7-beta_u+s_u`. If z is on Q, three
DISTINCT faces are exterior: mz alpha, mz beta and zpq. The first two
belong to X; the third cannot belong to C because all z,p,q avoid the
strict interior and an R-side chord is impossible. Since the R interval
contains t_z+1 faces,

`d_J(z)-(t_z+1)>=3`.

This first gives t_z<=d_J(z)-4; parity strengthens it to
`t_z<=d_J(z)-5=2-beta_z+s_z`. No bound on h, I or s_z is used.

For m on Q, its C interval is in one original sector, whose exact word
gives original degree at least t_m+5. The other sector has odd original
degree at least seven. Hence `d_J(m)>=t_m+7`. Its adopted complete
minimum is `7+beta_m`, yielding

`t_m<=beta_m+s_m`
`    =2-beta_m+s_m-2(1-beta_m)`.

If m is absent from Q, both original sectors have odd degree at least
seven; d_J(m)>=9 and its parity-sensitive minimum is seven, so s_m>=2.
This excess is outside both the boundary and the strict disk interior.
This verifies the same two-unit correction when epsilon=0 and m is absent.

## 3. The excess cancellation and forced ears

Sum the checked boundary bounds. Nonnegative excess away from Q and
its strict interior may be discarded in the appropriate direction.
The m correction, on Q or outside it, is exactly sufficient for

`sum_Q t_u <= 14-B+Delta-Delta_i-2(1-epsilon)+2h`
`           = I+2-Delta_i+2h`.

Comparison with disk curvature gives `6<=2h`, hence h>=3. The interior
excess cancels exactly; it is not bounded, set to zero, or counted twice.
Every h vertex is an ordinary actual ear centre. Two cannot be adjacent
on Q because a common Q edge has only one exterior face; the purported
two ears would identify distinct vertices of the simple seven-cycle.
A seven-cycle has at most three pairwise nonadjacent vertices, so h=3.

The previously reviewed three-ear/Q4 proof applies to these ears without
any degree bound on the centres. It requires only that they are ordinary,
actual unique exterior faces, and zero faces. Their old Q edges meet
ordinary centres, hence are not pq; the exact face-bit identity makes
each ear zero. All six T0 vertices remain on or outside the compressed
Q4, and zpq remains outside. A chord would make the exterior a two-face
disk with no interior vertex, impossible for six distinct T0 vertices
and four boundary positions. The four forced-ear cases then contradict
the EXACT source-sector theorem C2, including its crossed both-hub case.
Thus the arbitrary-size seven-barrier is impossible.

## 4. Matching conclusion and stopping point

The conclusion is about the same original D and literal marks: there
exists an ordinary perfect matching containing e,g and excluding f.
The argument assumes nonexistence only to select a maximum Tutte barrier,
and the earlier exhaustive 101 barrier results reduce it to the case
just excluded. It does not construct a smaller source or combine
independently feasible fibres. The nonempty P111 family, actual source
rotation, ordered ports, all complete lifts and empty cells are retained
through the contradiction.

An ordinary P101 member may have an odd complementary cycle. Its full
Tait fibre is then empty. Consequently no W101>0, W110+W101>0, omega=0,
complete319 exclusion or general K_infinity=K_<=5 result follows. The
new geometry proof is a paper theorem; finite controls and Lean build
success have separate scope. In particular the 140 even111 eligibility
bound remains a conditional interface statement, while 420 ordinary
signatures and all empty fibres remain fully preserved.

## 5. Final canonical proof review

The updated canonical PROOF, titled ordinary101 matching existence,
was read in full after the general theorem was incorporated. Its
sections 2--4 reproduce the reviewed bounds, exact excess cancellation
and source-sector contradiction. It properly invokes the earlier
exhaustive 101 barrier classification before concluding H has a PM,
and supplements that PM with the original e,g on the same D.

Sections 5--6 explicitly mark the seven-barrier exterior as conditional,
retain all 128 E_T^101 empty cells, and state the even exterior path
criterion including repeated endpoints. The 140 count is correctly an
eligibility bound for even111 joins before actual exterior support and
componentwise parity equations. It does not replace the 420 ordinary
signature bound or discard complete lifts. Section 7 correctly moves
ordinary101 from OPEN to proved while leaving even-complement positivity,
the joint omega=0 obligation, complete319 exclusion and general source
closure OPEN. No material correction is required.
