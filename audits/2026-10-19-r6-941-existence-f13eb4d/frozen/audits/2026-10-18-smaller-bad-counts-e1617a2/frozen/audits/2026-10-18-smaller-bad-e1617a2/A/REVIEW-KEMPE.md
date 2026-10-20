# A independent review of the necessary C8 Kempe closure

Reviewed the root `kempe_consistency.py` and `kempe-consistency.json`.
Independently replayed the certificate with [verify_kempe.py](verify_kempe.py),
which does not import or execute the root script. It constructs partitions
as sets of blocks, separately enumerates the old b,p,h lifts, checks every
compatible noncrossing partition for each removed tuple, and checks all
subset flips for each surviving witness. The root-script SHA is also
checked against the certificate.

## Necessity for an actual exterior

The geometric premise is a genuine plane disk with the displayed simple
ordered boundary `(a,n,R,L,q,c,x,y)` and its actual eight rim edges.
Application to the original source requires the exact distinctness and
rotation justification supplied separately; this computation cannot
establish that premise.

Under that premise, take one full exterior colouring and one split of the
four colours into two complementary pairs. Its actual two-colour
components form vertex-disjoint connected sets. Their contacts with the
simple disk boundary give a noncrossing set partition: alternating
contacts in distinct blocks would force two vertex-disjoint paths to
cross in the disk. Each block uses one pair only, and every boundary
edge whose endpoints use the same pair forces its two contacts into the
same block. These are precisely the partition filters in the root script.

Every subset of these actual components can be switched simultaneously.
Within one pair, components are disjoint and have no edge to another
component of that pair; between complementary pairs, all edges remain
proper. Components missing the boundary have no effect on its tuple.
Thus every boundary tuple in the recorded subset-flip orbit has a full
exterior extension on that same graph. The full exterior relation is
invariant under a common S4 renaming, so canonical tuple storage is valid.

The initial filter is also necessary. For any one actual exterior
assignment, every legal b,p,h lift produces a full original colouring;
the whole local old mask must therefore lie in the original support.
The independent lift checker verified all those edges, including bp and
ph. No independently feasible local choices are combined with an
incompatible exterior assignment.

Inductively an actual exterior relation survives every deletion round:
its actual component partition supplies an option whose entire orbit is
still present. Conversely, the survivor witnesses show that the reported
set is closed under the stated existential partition rule. The root
deduplication of equal flip orbits is safe for this rule, since equal
orbits have exactly the same missing-tuple test; the independent checker
rechecked all compatible partitions before each deletion.

## Independent results

| Original support | Initial tuples | Surviving tuples | Surviving accepted tuples | Old projection |
| --- | ---: | ---: | ---: | ---: |
| 932 | 197 | 154 | 8 | 932 |
| 933 | 215 | 191 | 9 | 933 |
| 941 | 233 | 225 | 10 | 941 |

Command executed successfully:

```
python3 -B audits/2026-10-18-smaller-bad-e1617a2/A/verify_kempe.py
```

This independently verifies the necessary-closure counts and their full
old-mask projections. Candidate-support projections are a separate
computation and are not asserted independently checked by this file.

## Essential relaxation boundary

The surviving partition is selected separately for each boundary tuple
and each complementary-palette split. The checker supplies no common
exterior graph, no common complete colouring realizing the three chosen
partitions, and no compatibility of its witness choices after subsequent
switches. A real full colouring would supply all those structures at
once, but satisfying these weaker existential conditions does not produce
one. The survivor count is consequently **not** a count of realizable
sources or colourings.

The computation proves that this particular necessary planar boundary
closure does not eliminate the accepted tuples or alter the original
projected masks. It does not prove that an actual counterexample exterior
exists, that every stronger Kempe condition would also fail, or that no
smaller bad construction is possible. Its inputs are the fixed interface
and source masks; it is not an enlarged search of local plane patches.

No substantive error was found in the root script's necessity direction,
and the independent replay passed.
