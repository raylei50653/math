# Rejected preliminary model: no theorem or certificate of impossibility

`naive_pinched_boundary.py`, `.json`, and `.log` are retained historical
exploration. The model applies ordinary-disk noncrossing to the weak boundary
walk `z,s,r,t,z,p,q` and treats both z occurrences as one component block.
That overconstrains the cut at z and falsely eliminates all rows. Its result
is rejected. The raw script still points to its original `/tmp` output path;
it is not a replay entry point for this audit.

Use `../controls/check_interface.py --check` for the adopted outer-C4
necessary control. No graph realizability or impossibility claim follows
from any file in this directory.
