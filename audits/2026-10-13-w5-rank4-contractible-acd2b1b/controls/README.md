# W5-RANK4-C primary finite certificate

`check.py` implements the complete necessary domain specified by
`../structure/CORE.md` and `../structure/ATTACHMENTS.md`. Those paper arguments
prove coverage; the generator itself supplies no general-source completeness
claim. All 6,389 parameter records retain their original named vertices, ten
pins, literal edges, oriented faces, rotations, bridges and shared cutvertices.
There is no graph-isomorphism deduplication or replacement by a smaller graph.

Each record in `certificate.jsonl.gz` stores ten rows in the explicit header
order. Every row contains all 1,024 U tuples, including empty fibres, all full
A-colourings in each fibre, and all restored G-colourings including the centre.
Restoration is also checked by directly colouring G. `Sigma` is the resulting
ten-bit accepted-row mask. `Sigma_in_K132` is direct frozen-catalogue membership;
it is not an R3 equivalence claim. Original-source minimality is `not triggered`
for these necessary templates. The certificate includes a superset: the
separately recorded full U/B degree flags are not used to delete records.

`summary.json` contains totals. `templates.json.gz` is the parameter and graph
digest index. Both gzip outputs use deterministic headers. The mathematical
digest in the summary hashes the complete uncompressed canonical JSONL stream,
including the header and all complete records.

Run from the repository root:

```sh
python audits/2026-10-13-w5-rank4-contractible-acd2b1b/controls/check.py --check
python audits/2026-10-13-w5-rank4-contractible-acd2b1b/controls/check.py --check --seed 17
python audits/2026-10-13-w5-rank4-contractible-acd2b1b/controls/catalogue.py --check
```

`--seed 17` changes variable tie priorities and colour search order before
comparing complete sorted lifts and every certificate record. `--write` uses
exclusive creation and is intended only for an empty controls output location.
`--list` reconstructs every graph and reports the domain counts without colour
search. Parameters encode ordered serial components, an O/B/U/D word on their
backbone vertices, original B/U bit words on polygon sides, and ordered terminal
triangles between components. All backbone vertices of a component receive
labels first; other polygon vertices then receive labels in ascending polygon
order, atom by atom. The independent checker uses a different enumeration and
builds adjacency directly rather than importing this implementation.

Provenance: facial-dart validation, the primary MRV colouring routine and full
cell grouping were adapted from the frozen BASE copy of
`audits/2026-10-13-w5-rank3-contractible-50d5474/controls/check.py`.
The serial rank-four domain and constructions are new in this audit.
`catalogue.py` retains the frozen rank-three catalogue/D5 algorithm with local
input paths. Neither implementation imports or mutates an old audit.

This is a finite computational certificate, conditional on the source contract,
paper coverage and frozen K132 input. It is not a new Lean theorem. The parent
report states the resulting mathematical exclusion and its essential-branch
boundary separately.
