# Independent C₈ interface and finite count controls

`checker.py` imports neither `interface.py` nor the frozen collar implementation.
It rebuilds all literal assignments, global S₄ orbits and their sizes, all 35
named collars and their complete literal transfers, and the full reverse lifts.
It checks the detailed-balance equation

`24 T[r,p] = orbit_size[p] · reverse_count[r,p]`.

In particular, the alternating two-color C₈ row has orbit size 12, so replacing
all orbit sizes with 24 is detected. Every comparison of a collar edge uses the
same literal color frame. There is no independent normalization at a join.

The Kempe reconstruction starts from all 1,430 noncrossing partitions of the
entire named C₈. For each complementary pair of colors it retains partitions
whose blocks lie on one color-pair side and which join every actual boundary
edge on that side. It enumerates all block swaps, then checks every recorded
simultaneous pruning round and all final accepted preimages. This differs from
the producer's pair of set-partition generators and reproduces all obligations.

The four finite inner disks are:

- the bare C₈;
- a fan triangulation with no interior vertices;
- a wheel with one interior vertex;
- a triangulated disk with two adjacent interior vertices, one adjacent to
  boundary vertices `0,1,2,3,4`, the other to `4,5,6,7,0`.

For each disk, generic graph-coloring backtracking computes its complete
274-coordinate extension-count vector. The checker then constructs the actual
whole graph for all 35 collars and directly counts colorings for each of the
ten fixed outer rows. All 1,400 results equal the full matrix transfer. Graph
edges and all counts are saved in `control_certificate.json`.

These graphs calibrate the implementation. They are not claimed to satisfy the
complete minimal catalogue-external source contract. The bare cycle is allowed
as an untriangulated disk control; the other three controls are triangulated.

The wheel has actual count `4 − number_of_used_boundary_colors`: its bicolor row
has two extensions, every tricolor row one, and every four-color row zero. A
linear identity is independently derived by exact rational elimination of the
91 active noncrossing equality columns and then verified individually on all
1,430 equality vectors. It holds on every actual control, but replacing the
wheel's counts with its Boolean support gives residual `−1`. Thus a Boolean
support vector cannot be used as actual counts, even when the support is an
actual planar graph's complete relation. Altering an identity coefficient also
produces a nonzero noncrossing-column residual.

Replay:

```bash
python3 audits/2026-10-13-c8-joint-count-3097ef5/controls/checker.py --check
PYTHONHASHSEED=17 python3 audits/2026-10-13-c8-joint-count-3097ef5/controls/checker.py --check
```

`--write` creates a new certificate exclusively. `--interface PATH` permits
negative tests against altered interface artifacts. The root proof checker
separately verifies universal exclusion certificates; these finite controls do
not replace that proof.
