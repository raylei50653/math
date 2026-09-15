/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.KempeSurgery

/-! Trust dependencies of the Kempe surgery / cut-interface layer. Every proof is an ordinary
proof; nothing may depend on `sorryAx` or `Lean.ofReduceBool`. -/
#print axioms FiveBoundary.KempeSurgery.reachable_sup_iff_reflTransGen
#print axioms FiveBoundary.KempeSurgery.reachable_sup_iff_quotient
#print axioms FiveBoundary.KempeSurgery.componentMap_bijective
#print axioms FiveBoundary.KempeSurgery.componentEquiv
#print axioms FiveBoundary.KempeSurgery.swapOn_univPair
#print axioms FiveBoundary.KempeSurgery.kempeSet_univPair
#print axioms FiveBoundary.KempeSurgery.swapOn_proper
#print axioms FiveBoundary.KempeSurgery.swapOn_pair_iff
#print axioms FiveBoundary.KempeSurgery.pairGraph_swap_same
#print axioms FiveBoundary.KempeSurgery.pairGraph_swap_complementary
#print axioms FiveBoundary.KempeSurgery.swapOn_mixed_iff
#print axioms FiveBoundary.KempeSurgery.pairGraph_swap_mixed
#print axioms FiveBoundary.KempeSurgery.mixed_reachable_iff_quotient
#print axioms FiveBoundary.KempeSurgery.swapOn_union_of_disjoint
#print axioms FiveBoundary.KempeSurgery.swapOn_comm_of_disjoint
#print axioms FiveBoundary.KempeSurgery.kempeSet_swapOn
#print axioms FiveBoundary.KempeSurgery.swapOn_swapOn
