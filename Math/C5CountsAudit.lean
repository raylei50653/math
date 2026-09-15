/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.C5Counts
import Math.C5ParityWord
import Math.NearTriangulation

/-! Trust dependencies of the C5 counting, parity-word and near-triangulation layers.
Every finite check here is kernel `decide`; nothing may depend on `sorryAx` or
`Lean.ofReduceBool`. -/
#print axioms FiveBoundary.C5Counts.chord_of_nonadj
#print axioms FiveBoundary.C5Counts.ofCoefficients_chordTotalConst
#print axioms FiveBoundary.C5Counts.x_eq_m_add
#print axioms FiveBoundary.C5Counts.sum_x
#print axioms FiveBoundary.C5Counts.slack_eq
#print axioms FiveBoundary.C5Counts.conjecture9_iff
#print axioms FiveBoundary.C5Counts.independent_subset_chord
#print axioms FiveBoundary.C5Counts.all_chords_positive
#print axioms FiveBoundary.C5Counts.counterexample_violates_conjecture9
#print axioms FiveBoundary.C5Counts.NP_chordTotalConst
#print axioms FiveBoundary.C5Counts.NP_m
#print axioms FiveBoundary.C5Counts.NP_slack
#print axioms FiveBoundary.C5Counts.NP_support

#print axioms FiveBoundary.ParityWord.eq_of_edgeWord
#print axioms FiveBoundary.ParityWord.fiber_eq_translates
#print axioms FiveBoundary.ParityWord.fiber_card
#print axioms FiveBoundary.ParityWord.extensionCount_colorAction
#print axioms FiveBoundary.ParityWord.extensionCount_of_edgeWord
#print axioms FiveBoundary.ParityWord.edgeWord_integrate
#print axioms FiveBoundary.ParityWord.integrate_proper
#print axioms FiveBoundary.ParityWord.edgeWord_isParity
#print axioms FiveBoundary.ParityWord.parityWord_count
#print axioms FiveBoundary.ParityWord.fiber_partition
#print axioms FiveBoundary.ParityWord.word_a_singleton
#print axioms FiveBoundary.ParityWord.word_b_pair

#print axioms FiveBoundary.NearTriangulation.two_periodic_of_no_ear
#print axioms FiveBoundary.NearTriangulation.even_of_no_ear
#print axioms FiveBoundary.NearTriangulation.exists_hub_of_no_ear
#print axioms FiveBoundary.NearTriangulation.ear_or_hub
#print axioms FiveBoundary.NearTriangulation.counts
#print axioms FiveBoundary.NearTriangulation.corollary20_range

open FiveBoundary.C5Counts FiveBoundary.ParityWord

-- Small kernel-reduced spot checks.
example : m t = 1 := by decide
example : slack (NP {0, 2}) = -5 := by decide
example : edgeWord ![0, 1, 0, 2, 1] = ![1, 1, 2, 3, 1] := by decide
example : edgeWord ![0, 1, 3, 2, 3] = ![1, 2, 1, 1, 3] := by decide
