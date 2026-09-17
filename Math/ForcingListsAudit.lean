/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.ForcingLists

/-! Trust dependencies of the forcing-list layer. Every proof is an ordinary proof; nothing may
depend on `sorryAx` or `Lean.ofReduceBool`. -/
#print axioms FiveBoundary.ForcingLists.listColorable_iff_bridge
#print axioms FiveBoundary.ForcingLists.bridge_forced
#print axioms FiveBoundary.ForcingLists.listProper_swap
#print axioms FiveBoundary.ForcingLists.avail_swap_iff
#print axioms FiveBoundary.ForcingLists.forced_eq_of_symmetric
#print axioms FiveBoundary.ForcingLists.exists_asymmetric_of_forced
#print axioms FiveBoundary.ForcingLists.forced_palettes
#print axioms FiveBoundary.ForcingLists.card_eq_of_forced_palettes
#print axioms FiveBoundary.ForcingLists.listColorable_of_last_free
#print axioms FiveBoundary.ForcingLists.cycle_colorable_of_three
#print axioms FiveBoundary.ForcingLists.cycle_colorable_of_lists_ne
#print axioms FiveBoundary.ForcingLists.odd_cycle_common_uncolorable
#print axioms FiveBoundary.ForcingLists.even_cycle_common_colorable
#print axioms FiveBoundary.ForcingLists.cycle_two_lists_uncolorable_iff
#print axioms FiveBoundary.ForcingLists.cycle_uncolorable_iff
#print axioms FiveBoundary.ForcingLists.c5_two_lists_uncolorable_iff
#print axioms FiveBoundary.ForcingLists.triangle_two_lists_uncolorable_iff
#print axioms FiveBoundary.ForcingLists.shared_chain_interface
#print axioms FiveBoundary.ForcingLists.apex_extension_iff
#print axioms FiveBoundary.ForcingLists.apex_forbidden_eq
