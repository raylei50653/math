/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.AutomataReplay
import Math.HallTriangle
import Math.AttachmentBlock
import Math.GeometryWitness
import Math.GeometryProfile
import Math.AttachmentNormalForm
import Math.NormalFormHall
import Math.GeoRejectBridge
import Math.AttachmentSaturated
import Math.AttachmentGaps
import Math.AttachmentOrder

/-! Actual trusted dependencies of the finite-state layer. -/
#print axioms FiveBoundary.ColorDFA.runFrom_spec
#print axioms FiveBoundary.ColorDFA.accept_iff_triangleCan
#print axioms FiveBoundary.ColorDFA.mem_sigma_triangle
#print axioms FiveBoundary.ColorDFA.splitSigma_triangle
#print axioms FiveBoundary.ColorDFA.acceptedReps_exact
#print axioms FiveBoundary.ColorDFA.acceptB_iff
#print axioms FiveBoundary.ColorDFA.wordOfMask_surjective
#print axioms FiveBoundary.GeometryDFA.geoAccept_iff
#print axioms FiveBoundary.GeometryDFA.accept_certificate
#print axioms FiveBoundary.GeometryDFA.accepted_count
#print axioms FiveBoundary.GeometryDFA.z5_profiles_checked
#print axioms FiveBoundary.Automata.library_sigma_reps
#print axioms FiveBoundary.Automata.synthesized_profiles
#print axioms FiveBoundary.Hall.k3_uncolorable_iff
#print axioms FiveBoundary.Hall.reject_iff_hall
#print axioms FiveBoundary.Hall.not_mem_sigma_iff_hall
#print axioms FiveBoundary.Hall.regression_guard
#print axioms FiveBoundary.GeometryDFA.stepSum_le_of_sublist
#print axioms FiveBoundary.GeometryDFA.attachment_block
#print axioms FiveBoundary.GeometryDFA.runOK_iff_blocks
#print axioms FiveBoundary.Hall.reject_iff_geometry
#print axioms FiveBoundary.Hall.threeProfile_eq_geo
#print axioms FiveBoundary.GeometryDFA.fan_excess_le_winding
#print axioms FiveBoundary.GeometryDFA.runOK_attachmentCount_le_eight
#print axioms FiveBoundary.GeometryDFA.runOK_eight_all_active
#print axioms FiveBoundary.GeometryDFA.runOK_common_card_le_two
#print axioms FiveBoundary.Hall.runOK_rejection_le_two_of_low_degree
#print axioms FiveBoundary.Hall.runOK_profile_ge_three_of_low_degree
#print axioms FiveBoundary.Hall.runOK_large_rejection_cases
#print axioms FiveBoundary.GeometryDFA.annulusAccept_iff_normalForm
#print axioms FiveBoundary.GeometryDFA.NecklaceCuts.degrees
#print axioms FiveBoundary.GeometryDFA.NecklaceCuts.packet_lengths
#print axioms FiveBoundary.GeometryDFA.NecklaceCuts.total_le_eight
#print axioms FiveBoundary.GeometryDFA.middle_count_eq_one
#print axioms FiveBoundary.GeometryDFA.NecklaceCuts.triple_packet_forces_degree_one
#print axioms FiveBoundary.GeometryDFA.NecklaceCuts.packet_shape
#print axioms FiveBoundary.GeometryDFA.NecklaceCuts.forward_pair_count_le_one
#print axioms FiveBoundary.GeometryDFA.annulusAccept_iff_nondegenerate_normalForm
#print axioms FiveBoundary.GeometryDFA.NecklaceCuts.degree_eq_singletons_add_junctions
#print axioms FiveBoundary.GeometryDFA.NecklaceCuts.common_next_eq_junction
#print axioms FiveBoundary.GeometryDFA.runOK_common_le_one_of_degrees
#print axioms FiveBoundary.GeometryDFA.runOK_fan_card_le_two_of_degrees
#print axioms FiveBoundary.Hall.geoReject_iff_pair_or_opposite
#print axioms FiveBoundary.GeometryDFA.NecklaceCuts.inventory
#print axioms FiveBoundary.GeometryDFA.NecklaceCuts.incidenceRegime
#print axioms FiveBoundary.GeometryDFA.NecklaceCuts.eight_iff_three_junctions_two_singletons
#print axioms FiveBoundary.GeometryDFA.NecklaceCuts.saturated_degree_cases
#print axioms FiveBoundary.GeometryDFA.junctions_cyclic_order
#print axioms FiveBoundary.GeometryDFA.anchored_gaps_constant
#print axioms FiveBoundary.GeometryDFA.three_junction_normalForm_iff
#print axioms FiveBoundary.GeometryDFA.NecklaceCuts.saturated_cyclic_normalForm
#print axioms FiveBoundary.GeometryDFA.runOK_saturated_normalForm
#print axioms FiveBoundary.GeometryDFA.three_junction_gaps_iff
#print axioms FiveBoundary.GeometryDFA.NecklaceCuts.three_junction_cyclic_gaps
#print axioms FiveBoundary.GeometryDFA.NecklaceCuts.three_junction_gap_inventory
#print axioms FiveBoundary.GeometryDFA.singletonPackets_ordered_blocks
#print axioms FiveBoundary.GeometryDFA.junction_tail_ordered
#print axioms FiveBoundary.GeometryDFA.one_junction_tail_iff
#print axioms FiveBoundary.GeometryDFA.two_junction_tail_iff
#print axioms FiveBoundary.GeometryDFA.NecklaceCuts.one_junction_cyclic_gaps
#print axioms FiveBoundary.GeometryDFA.NecklaceCuts.two_junction_cyclic_gaps
#print axioms FiveBoundary.GeometryDFA.NecklaceCuts.one_junction_normalForm
#print axioms FiveBoundary.GeometryDFA.NecklaceCuts.two_junction_gap_inventory
#print axioms FiveBoundary.Hall.runOK_exists_degree_two
#print axioms FiveBoundary.Hall.rejectionSet_subset_compl_of_degree_two
#print axioms FiveBoundary.Hall.runOK_rejection_le_three
#print axioms FiveBoundary.Hall.rejectionSet_eq_compl_of_three
#print axioms FiveBoundary.Hall.runOK_three_rejection_degrees
#print axioms FiveBoundary.Hall.nonadjacent_opposite_le_one
#print axioms FiveBoundary.Hall.rejectionSet_subset_opposite_union_common
#print axioms FiveBoundary.Hall.runOK_three_rejection_adjacent
#print axioms FiveBoundary.Hall.runOK_three_rejection_structure
#print axioms FiveBoundary.Hall.runOK_profile_ge_two
#print axioms FiveBoundary.Hall.runOK_two_profile_adjacent
#print axioms FiveBoundary.Hall.normalForm_rejection_bound
