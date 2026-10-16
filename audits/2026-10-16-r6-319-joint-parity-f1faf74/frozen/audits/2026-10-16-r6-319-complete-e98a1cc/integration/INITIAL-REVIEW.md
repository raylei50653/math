# Independent reconstruction correction

The first root replay reconstructed all 144 J colourings, all 18 PMs and
the single positive-oddness joint PM successfully, then rejected the draft
claim that all six root-normalized even111 labellings give two transitions.
The failure was `AssertionError` at `assert len(transitions) == 2`.

The even111 PM with complementary lengths 8+8 has four such labellings,
all with two transitions, one on each new odd cycle. The second even111 PM
has a 16-cycle complement and two labellings; both have four transitions,
distributed three on the new 9-cycle and one on the new 7-cycle.

The independent checker was corrected to test both exact distributions.
The B draft was corrected before adoption. This was a draft-summary error;
the complete B certificate and general transition-parity identity were
consistent with the reconstructed data. The rejected claim is not adopted.

The first receipt-aggregation command subsequently stopped with
`KeyError: 'records'` because C names its verification entries `runs`.
The root seed-17 and corrupted-receipt checks had already returned their
expected exit codes before that metadata aggregation failed. Their logs
were retained and the aggregator was corrected to read each actual schema;
the failed aggregation was not counted as a successful bundle check.
