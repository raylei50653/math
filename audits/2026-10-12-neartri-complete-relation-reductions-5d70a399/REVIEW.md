# Independent read-only review

Reviewed the current `REPORT.md`, `certificate.json`, and
`collar_certificate.json` in the neartri-complete-relation-reductions audit.
No blocking issue was found. The only requested wording correction was to
include cyclic reindexing, as well as global colour permutation, when placing
a three-colour degree-five link in the representative `01012`.

The independent checker imports no production checker. It generates proper
patterns and noncrossing partitions using restricted-growth strings, verifies
924 full-S4 crosscut joins and their 9,240 named fibres, reverses the direction
of collar transfer to fix outer representatives and enumerate literal inner
words, transports both sides together to recover the saved full outer lifts,
and recomputes all 42 fixed points by asynchronous set deletion. It also
checks every recorded synchronous deletion round and compares input hashes
before and after the run. All comparisons passed.

The paper topology has the necessary support: absence of a two-edge crosscut
limits each interior vertex to at most two consecutive original boundary
contacts. A vertex with two contacts is the unique facial apex of their
boundary edge, since a different apex would give a separating triangle.
Consequently, the boundary neighbour paths intersect only at their named
consecutive apices and form a simple inner cycle of length `5+h`. Their
triangular faces fill the collar, leaving the same actual remaining graph
inside that cycle.

For sound pruning, let `S` be the complete relation of that actual inner disk.
Exact gluing gives `R = union(C_t(q) for q in S)`, so `S` lies in the initial
allowed set. Every actual inner colouring and each complementary colour split
give one enumerated noncrossing partition whose full component-swap orbit is
contained in `S`. Thus `S` remains inside every pruning round. Failure of the
final column union to cover `R` excludes the source. Different abstract
partition witnesses are never combined into one colouring.

The conclusions are conditional on the stated globally minimal outsider
normal form. All `h <= 2` collars exclude 933. For 941, the sole surviving
necessary envelope is `t=(0,0,1,0,1)`, with 55 of 91 C7 rows and outer union
941. The actual inner relation need only be contained in this envelope; the
envelope is not a realized source. Distinct trigger edges retain independent
existential rejection witnesses.

Replay:

```bash
python3 audits/2026-10-12-neartri-complete-relation-reductions-5d70a399/independent_review.py
```

The saved report is `independent_review.json`. The packaged checker defaults to read-only; an explicit `--report` uses exclusive creation. The requested rotation wording has been corrected in REPORT.md.
