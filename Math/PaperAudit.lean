/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.Boundary
import Math.Enumeration
import Math.Certificates
import Math.GeneratedCertificates
import Math.State
import Math.SplitCertificate
import Math.AutomataReplay
import Math.AlignmentCounterexample
import Math.ConstructedOriginal
import Math.ConstructedMinimal
import Math.ConstructedAnalysis
import Math.GadgetRelations
import Math.PrimitiveGadgets
import Math.TriangleConstraints
import Math.GadgetLibrary
import Math.GadgetTargets
import Math.GadgetSynthesis
import Math.ColorDFA
import Math.GeometryDFA
import Math.HallTriangle
import Math.AttachmentBlock
import Math.GeometryWitness
import Math.AttachmentBudget
import Math.GeometryProfile
import Math.AttachmentNormalForm
import Math.NormalFormHall
import Math.AttachmentSignature
import Math.AttachmentSaturated
import Math.AttachmentGaps
import Math.AttachmentOrder
import Math.GeoRejectBridge
import Math.AttachmentEndpoints
import Math.FanPentagon
import Math.BoundaryRelations
import Math.C5PairForcing
import Math.PPRelations
import Math.StepwiseState
import Math.StripGraph
import Math.StepwiseReplay
import Math.LocalClosure
import Math.LocalWiring
import Math.SymRelabel
import Math.SymNormalForm
import Math.PrefixPartition
import Math.ReducedViable
import Math.ReducedGraphBridge
import Math.ReducedDFS
import Math.EdgeMask
import Math.IntegerViable
import Math.C5Counts
import Math.C5ParityWord
import Math.NearTriangulation
import Math.KempeSurgery

/-!
# Paper-level trust audit

Centralised `#print axioms` for every Lean declaration that `paper/outline.md` cites as a
`[L]` (proved in Lean) headline claim, plus one or two headline theorems from each module the
outline references only by name. Section numbers follow `paper/outline.md`.

Run with `lake env lean Math/PaperAudit.lean > artifacts/paper_audit/lean-audit.txt`
(after `lake build`). The expected standard axioms are `propext`, `Classical.choice`,
`Quot.sound`; any `..._native.native_decide.ax_*` entry marks a `native_decide` dependency,
and `sorryAx` must never appear. This file does not change any statement or proof.
-/

/-! ## §3 Preliminaries: Σ, S4/D5 orbits, ten-bit encoding, gluing, alignment -/
#print axioms FiveBoundary.SigmaAt
#print axioms FiveBoundary.Sigma
#print axioms FiveBoundary.sigma_is_image
#print axioms FiveBoundary.sigma_color_invariant
#print axioms FiveBoundary.sigma_union_same_vertices
#print axioms FiveBoundary.c5_count
#print axioms FiveBoundary.three_color_count
#print axioms FiveBoundary.color_reps_count
#print axioms FiveBoundary.full_reps_count
#print axioms FiveBoundary.color_reps_minimal
#print axioms FiveBoundary.full_reps_minimal
#print axioms FiveBoundary.color_abstraction_exact
#print axioms FiveBoundary.abstract_intersection
#print axioms FiveBoundary.sigma_saturated
#print axioms FiveBoundary.color_state_count
#print axioms FiveBoundary.independent_gluing
#print axioms FiveBoundary.bad_sigma_exact
#print axioms FiveBoundary.bad_sigma_card
#print axioms FiveBoundary.no_bad_with_fewer_edges
#print axioms FiveBoundary.coarse_not_congruent
#print axioms FiveBoundary.glued_bad
#print axioms FiveBoundary.AlignmentCounterexample.reflection_in_D5
#print axioms FiveBoundary.AlignmentCounterexample.whole_state_reflection
#print axioms FiveBoundary.AlignmentCounterexample.reflected_good
#print axioms FiveBoundary.AlignmentCounterexample.reflected_gluing
#print axioms FiveBoundary.AlignmentCounterexample.same_D5_class_different_context_answer
#print axioms FiveBoundary.intersection_cannot_repair
#print axioms FiveBoundary.intersection_step_decreases
#print axioms FiveBoundary.intersection_scc_singleton
#print axioms FiveBoundary.edgeCheck_exact
#print axioms FiveBoundary.splitSigma_exact
#print axioms FiveBoundary.splitChecker_exact

/-! ## §4 Finite searches and the separating-C5 counterexample -/
#print axioms FiveBoundary.all_certificates_valid
#print axioms FiveBoundary.all_certificates_bad
#print axioms FiveBoundary.ConstructedOriginal.all_certificates_valid
#print axioms FiveBoundary.ConstructedOriginal.all_certificates_bad
#print axioms FiveBoundary.ConstructedMinimal.all_certificates_valid
#print axioms FiveBoundary.ConstructedMinimal.all_certificates_bad
#print axioms FiveBoundary.ConstructedAnalysis.minimal_sigma_exact

/-! ## §5 Gadget synthesis -/
#print axioms FiveBoundary.Gadget.seq_assoc
#print axioms FiveBoundary.Gadget.hide_shared
#print axioms FiveBoundary.Gadget.denote_equivariant
#print axioms FiveBoundary.Gadget.neq_exact
#print axioms FiveBoundary.Gadget.eq_exact
#print axioms FiveBoundary.Gadget.shared_frame
#print axioms FiveBoundary.Gadget.independent_frames
#print axioms FiveBoundary.Gadget.pigeonhole_rejection
#print axioms FiveBoundary.Gadget.compiled_meaning
#print axioms FiveBoundary.GadgetLibrary.all_certificates_valid
#print axioms FiveBoundary.GadgetLibrary.all_certificates_exact
#print axioms FiveBoundary.GadgetTargets.all_certificates_valid
#print axioms FiveBoundary.GadgetTargets.all_certificates_bad
#print axioms FiveBoundary.Gadget.all_targets_exact
#print axioms FiveBoundary.Automata.library_matches_automata
#print axioms FiveBoundary.Automata.library_sigma_reps
#print axioms FiveBoundary.Automata.synthesized_profiles
#print axioms FiveBoundary.Automata.synthesized_disk

/-! ## §6 Finite-state synthesis on the triangle grammar -/
#print axioms FiveBoundary.ColorDFA.mem_sigma_triangle
#print axioms FiveBoundary.ColorDFA.splitSigma_triangle
#print axioms FiveBoundary.ColorDFA.acceptedReps_exact
#print axioms FiveBoundary.ColorDFA.acceptB_iff
#print axioms FiveBoundary.ColorDFA.wordOfMask
#print axioms FiveBoundary.ColorDFA.wordOfMask_surjective
#print axioms FiveBoundary.GeometryDFA.wordOfMask_bijective
#print axioms FiveBoundary.GeometryDFA.rotationTable
#print axioms FiveBoundary.GeometryDFA.rotationOf
#print axioms FiveBoundary.GeometryDFA.checkRotation
#print axioms FiveBoundary.GeometryDFA.accepted_masks_have_rotation
#print axioms FiveBoundary.GeometryDFA.accept_certificate
#print axioms FiveBoundary.GeometryDFA.accepted_count
#print axioms FiveBoundary.GeometryDFA.z5_profiles_checked
#print axioms FiveBoundary.Hall.PairPinnedToFourth
#print axioms FiveBoundary.Hall.TripleRestrictedToTwo
#print axioms FiveBoundary.Hall.k3_uncolorable_iff
#print axioms FiveBoundary.Hall.reject_iff_hall
#print axioms FiveBoundary.Hall.not_mem_sigma_iff_hall
#print axioms FiveBoundary.Hall.regression_guard
#print axioms FiveBoundary.GeometryDFA.stepSum_le_of_sublist
#print axioms FiveBoundary.GeometryDFA.runOK_iff_blocks
#print axioms FiveBoundary.GeometryDFA.attachment_block
#print axioms FiveBoundary.Hall.GeoReject
#print axioms FiveBoundary.Hall.reject_iff_geometry
#print axioms FiveBoundary.Hall.threeProfile_eq_geo
#print axioms FiveBoundary.GeometryDFA.runOK_attachmentCount_le_eight
#print axioms FiveBoundary.GeometryDFA.runOK_common_card_le_two
#print axioms FiveBoundary.Hall.runOK_rejection_le_two_of_low_degree
#print axioms FiveBoundary.Hall.runOK_large_rejection_cases
#print axioms FiveBoundary.GeometryDFA.annulusAccept_iff_normalForm
#print axioms FiveBoundary.Hall.geoReject_iff_pair_or_opposite
#print axioms FiveBoundary.GeometryDFA.NecklaceCuts.incidenceRegime
#print axioms FiveBoundary.GeometryDFA.NecklaceCuts.eight_iff_three_junctions_two_singletons
#print axioms FiveBoundary.GeometryDFA.runOK_saturated_normalForm
#print axioms FiveBoundary.GeometryDFA.NecklaceCuts.three_junction_cyclic_gaps
#print axioms FiveBoundary.GeometryDFA.NecklaceCuts.one_junction_normalForm
#print axioms FiveBoundary.GeometryDFA.NecklaceCuts.two_junction_cyclic_gaps
#print axioms FiveBoundary.Hall.runOK_rejection_le_three
#print axioms FiveBoundary.Hall.runOK_three_rejection_structure
#print axioms FiveBoundary.Hall.runOK_profile_ge_two
#print axioms FiveBoundary.Hall.runOK_two_profile_adjacent
#print axioms FiveBoundary.Hall.normalForm_rejection_bound
#print axioms FiveBoundary.GeometryDFA.normalForm_of_endpoint_order
#print axioms FiveBoundary.GeometryDFA.annulusAccept_of_endpoint_order

/-! ## §7 Fan pentagon, boundary relations, pair forcing, pp-expressions -/
#print axioms FiveBoundary.FanPentagon.sigma_exact
#print axioms FiveBoundary.FanPentagon.rejected_pattern
#print axioms FiveBoundary.FanPentagon.two_colour_obstruction
#print axioms FiveBoundary.BoundaryRelations.forces_iff
#print axioms FiveBoundary.BoundaryRelations.conditional_forces_iff
#print axioms FiveBoundary.BoundaryRelations.condition_inter
#print axioms FiveBoundary.BoundaryRelations.pairProjection_inter_subset
#print axioms FiveBoundary.C5PairForcing.all_pair_projections_equal
#print axioms FiveBoundary.C5PairForcing.full_relations_differ
#print axioms FiveBoundary.C5PairForcing.pairwise_information_insufficient
#print axioms FiveBoundary.PP.eval_and_meet
#print axioms FiveBoundary.PP.eval_ex_hide

/-! ## §8 Stepwise colouring and strip automata -/
#print axioms StepwiseState.run_repeat_loop
#print axioms StepwiseState.pumped_distinction
#print axioms StripGraph.search_iff
#print axioms StripGraph.verdict_iff
#print axioms StripGraph.residual_injective
#print axioms StepwiseReplay.fan4_nerode_lower_bound
#print axioms StepwiseReplay.fan5_nerode_lower_bound
#print axioms StepwiseReplay.fan5_extendable_iff

/-! ## §9 Local closure and fixed-endpoint wiring -/
#print axioms FiveBoundary.LocalClosure.summary_glue
#print axioms FiveBoundary.LocalClosure.replacement
#print axioms FiveBoundary.LocalClosure.relation_count
#print axioms FiveBoundary.LocalClosure.summary_eq_deletePrivate
#print axioms FiveBoundary.LocalClosure.sigma_eq_delete_private
#print axioms FiveBoundary.LocalWiring.residual_exact
#print axioms FiveBoundary.LocalWiring.continue_iff_union
#print axioms FiveBoundary.LocalWiring.chord_residual_exact

/-! ## §10 Sealed C5 cells: SYM and the reduced-search completeness chain -/
#print axioms FiveBoundary.Sym.proper_relabel
#print axioms FiveBoundary.Sym.Sigma_relabel
#print axioms FiveBoundary.Sym.sigma_iff_relabel
#print axioms FiveBoundary.Sym.Sigma_relabel_eq
#print axioms FiveBoundary.Sym.patternOrder_length
#print axioms FiveBoundary.Sym.patternOrder_toFinset
#print axioms FiveBoundary.Sym.attMask_relabel
#print axioms FiveBoundary.Sym.exists_sorted_relabel
#print axioms FiveBoundary.PrefixPartition.unique_owner
#print axioms FiveBoundary.PrefixPartition.covered_iff
#print axioms FiveBoundary.PrefixPartition.owner_at_end
#print axioms FiveBoundary.ReducedViable.degree_upper
#print axioms FiveBoundary.ReducedViable.previous_block_fixed
#print axioms FiveBoundary.ReducedViable.viable_of_survivor
#print axioms FiveBoundary.ReducedViable.rejection_sound
#print axioms FiveBoundary.ReducedViable.retained_owner
#print axioms FiveBoundary.ReducedGraphBridge.degree_eq_graph
#print axioms FiveBoundary.ReducedGraphBridge.attValue_eq_attMask
#print axioms FiveBoundary.ReducedGraphBridge.survivor_iff
#print axioms FiveBoundary.ReducedGraphBridge.viable_of_graph
#print axioms FiveBoundary.ReducedGraphBridge.graph_rejection_sound
#print axioms FiveBoundary.ReducedGraphBridge.retained_graph_owner
#print axioms FiveBoundary.ReducedDFS.state_invariant
#print axioms FiveBoundary.ReducedDFS.prefix_reachable
#print axioms FiveBoundary.ReducedDFS.mem_candidates
#print axioms FiveBoundary.ReducedDFS.retained_graph_owner
#print axioms FiveBoundary.ReducedDFS.worker_reachable
#print axioms FiveBoundary.ReducedDFS.split_graph_complete
#print axioms FiveBoundary.EdgeMask.encode_injective
#print axioms FiveBoundary.EdgeMask.reach_iff
#print axioms FiveBoundary.EdgeMask.popcount_encode
#print axioms FiveBoundary.EdgeMask.viable_encode_iff
#print axioms FiveBoundary.EdgeMask.viable_decode_iff
#print axioms FiveBoundary.EdgeMask.integer_viable_of_graph
#print axioms FiveBoundary.EdgeMask.integer_rejection_sound
#print axioms FiveBoundary.EdgeMask.viable_reach_iff

/-! ## §11 Counting layer, XOR parity words, near-triangulations -/
#print axioms FiveBoundary.C5Counts.ofCoefficients_chordTotalConst
#print axioms FiveBoundary.C5Counts.conjecture9_iff
#print axioms FiveBoundary.C5Counts.independent_subset_chord
#print axioms FiveBoundary.C5Counts.all_chords_positive
#print axioms FiveBoundary.C5Counts.counterexample_violates_conjecture9
#print axioms FiveBoundary.ParityWord.eq_of_edgeWord
#print axioms FiveBoundary.ParityWord.fiber_eq_translates
#print axioms FiveBoundary.ParityWord.fiber_card
#print axioms FiveBoundary.ParityWord.extensionCount_colorAction
#print axioms FiveBoundary.ParityWord.extensionCount_of_edgeWord
#print axioms FiveBoundary.ParityWord.IsParityWord
#print axioms FiveBoundary.ParityWord.fiber_partition
#print axioms FiveBoundary.NearTriangulation.two_periodic_of_no_ear
#print axioms FiveBoundary.NearTriangulation.even_of_no_ear
#print axioms FiveBoundary.NearTriangulation.exists_hub_of_no_ear
#print axioms FiveBoundary.NearTriangulation.ear_or_hub
#print axioms FiveBoundary.NearTriangulation.counts
#print axioms FiveBoundary.NearTriangulation.corollary20_range

/-! ## §11 Kempe surgery: one-swap connectivity update and cut-interface contraction -/
#print axioms FiveBoundary.KempeSurgery.reachable_sup_iff_quotient
#print axioms FiveBoundary.KempeSurgery.componentEquiv
#print axioms FiveBoundary.KempeSurgery.swapOn_proper
#print axioms FiveBoundary.KempeSurgery.pairGraph_swap_same
#print axioms FiveBoundary.KempeSurgery.pairGraph_swap_complementary
#print axioms FiveBoundary.KempeSurgery.pairGraph_swap_mixed
#print axioms FiveBoundary.KempeSurgery.mixed_reachable_iff_quotient
#print axioms FiveBoundary.KempeSurgery.swapOn_univPair
