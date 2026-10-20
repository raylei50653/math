# Discovery only

These files preserve the bounded 20-candidate exploration and floating LP discovery.
They are not replay authority. The root `check.py` independently reconstructs every
complete lift and uses standard-library integer arithmetic to verify the integer
`counted-control.json`, including its planar coefficients and complete counted orbits.
It never imports numpy/scipy or reads `counted-discovery.npz`.

`explore_counted.py` requires numpy/scipy. Its successful LP result is not proof.
`extract_control.py` reconstructs small rational coefficients, scales by two, and
exclusive-creates the root control file; it does not overwrite an existing control.
`probe_source.py` checks the explicit original-c transfer, U319 and the two original
mandatory positive restricted fibres. All of those checks are included in the formal
standard-library replay. No discovery file asserts source graph realizability.
