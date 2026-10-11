# Frozen finite interface schema — 待獨立驗收

`cases.json` is the sole named finite graph input. A case supplies `id`, ordered
`vertices`, `original_edges` of C, `pieces.L/S`, actual `boundary_attachments`,
ordered `s_contacts=[u_L,u_S]`, ordered `r_contacts.L/S`, `ownership`, original
`blocks` (bridge or cyclic odd-cycle vertex order), and `rotation` on the fragment
including s-contact edges and original rb4. Rotation is supplied but disk topology
is **not verified**. U and complete G are not supplied.

Ten literals in this order: 01012,01021,01023,01201,01202,01203,01212,01213,01231,01232.
Colours are 0,1,2,3. No retained r-spoke. Original e=[r,b4], t_r=1.

For each valid case a certificate record contains `case_id`, `vertices`, and
`rows`. Each row contains `literal`, `assignments` (sorted full colour vectors in
the original vertex order), `ambient_fibres` (all 64 ordered cells, tau0 then tau1
then r colour, each with `tuple`, `r`, `preimages`), `pins` (all 16 ordered a,b
cells with `r`, `s`, `preimages`, `restored_preimages`), and `spoke_variants`.
Each spoke variant supplies `s_spokes` and all 16 `pins`; preimages there are C
assignments filtered by the literal spoke factor only. They are **not X lifts**.
Empty preimage lists must be present. Preimages are full named-vertex vectors.
`restored_preimages` applies the original rb4 filter a != literal[4].

The top-level certificate has `schema=1`, `cases_sha256`, `cases` (valid cases),
`failed_cases` (invalid declared cases with named degree findings),
`target_source={executed:false,trigger_count:null,status:"not triggered"}`.

The direct enumerator reads only cases.json and enumerates original edges. It
imports no transfer/checker modules. The checker compares every full field and
reports the first named case/row/cell/vertex difference. Generation is exclusive
create; --check is strictly read only.
