# Parity/shared-cut continuation proposal

Recorded before the new experiments, 2026-10-29.
BASE: e1a90fea41702d7c98747716a5960198aecbecb3. Initial root Git status was clean.

1. P1: prove the four-terminal parity-free switching lemma without 4CT;
   independently enumerate every PM family of the marked pentagram/pentagon.
   Check the exact six-term double-dimer identity on deterministic plane disk controls.
2. P2: remove the added matching edges from the old complement, retain each
   actual segment with its length parity, and add the removed matching edges.
   Check the reconstructed odd-cycle count against the full new complement.
3. P3: reprove complete-region exchange for a five-leaf near-cubic network,
   restricting safe batches to one fixed terminal incidence word. Check the
   oddness/syndrome identities and terminal-support bound at actual minimizers.
   Keep nonzero-syndrome intermediates separate: they may expose 0 or 4 leaves.
4. Reuse the existing same-cut side checker on actual even-reference Tait
   colorings. Common-side soundness remains a necessary plane condition;
   no claim that it prohibits every possible five-reference blocker.

Finite controls use one source graph and literal terminal order per record.
No 4CT oracle, source switching, boundary marginal splice, or catalogue
coverage claim. P1 catalogue applicability and full P2 frozen-F4 coverage,
P3 general multi-reference exclusion remain OPEN unless proved here.
