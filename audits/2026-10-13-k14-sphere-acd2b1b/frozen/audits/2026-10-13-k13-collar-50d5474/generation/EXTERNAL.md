# External inputs and replayed scope

Fixed BASE: `50d5474f2446403f3b3001d5943571184c8c9936`.

Generator: plantri **5.8 - March 4, 2026**, Gunnar Brinkmann, Brendan McKay, Heidi Van den Camp. The source is bundled at BASE; no installed or downloaded executable is used.

Compiler: `cc (GCC) 16.2.1 20260810`. Python: `3.14.7 (main, Aug 10 2026, 07:46:56) [GCC 16.1.1 20260728]`. Standard library postprocessors only.

| Input | SHA256 |
|---|---|
| `artifacts/c5_excess_two_independent_search/vendor/plantri-guide.txt` | `79bbe51083318aa22797d5ca1a28cc347bc38a6871c7cf35e057863de3f785fc` |
| `artifacts/c5_excess_two_independent_search/vendor/plantri.c` | `3f70de5a3cacc78b2ed25b6a257588da94a518d8ae1dae74bcd0bf259cea07e8` |
| `min5paper_sc.pdf` | `d9a1c671d189965a3de57b2ec004cee6c7bea8bf24f0cccb17a1e7172b33d97f` |
| `plantri-full.pdf` | `a4a3cdc8783b09515597bd8762a429cb03758786767e6630f9aea76d0917866f` |

Primary sources:

- [Official plantri distribution](https://users.cecs.anu.edu.au/~bdm/plantri/): version and supported generation classes.
- [Minimum-five construction](https://users.cecs.anu.edu.au/~bdm/plantri/min5paper_sc.pdf): Brinkmann and McKay, Discrete Mathematics 301 (2005), 147-163. Theorems 1 and 3 plus the corrected proof of Theorem 2 supply the mathematical generation authority.
- [General implementation paper](https://users.cecs.anu.edu.au/~bdm/papers/plantri-full.pdf): Brinkmann and McKay, MATCH 58 (2007), 323-357, expanded edition. Section 2 Figure 6 gives the minimum-four construction; Section 1.2 describes canonical construction paths.

Both PDFs were retrieved from the authors' university server during this run and are retained verbatim with these hashes. Published proofs and the generic canonical augmentation theorem are imported mathematical dependencies; the local audit does not re-prove those papers or formally verify plantri, GCC, or Python.

Actual full generation was replayed locally for `-m5 19`, `-m4 19` with an output-only degree-five filter, and `-m4 14`. `normal/` and `seed17/` contain complete command and output logs. All twelve mathematical products match across normal, seed17, and the initial data; see `normal_seed17_comparison.json`.

The 2005 table count and the 5.8 guide table agree with the generated counts, but count agreement is only a diagnostic. Completeness is carried by the published generation constructions plus the cone and explicit annulus proofs in `COMPLETENESS.md`.

These sphere generators do not use the Dvorak-Lidicky fewer-than-thirty result. The parent proof imports the already established K≤12 theorem, whose external dependency is separately disclosed. No inclusive-thirty extension is used.
