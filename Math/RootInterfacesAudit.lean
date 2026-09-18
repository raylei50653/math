/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.RootInterfaces

/-! Trust dependencies of the exact contact, hub, shared-root, path-transfer and cover layer.
Every theorem uses ordinary proofs, with no `sorryAx` or `Lean.ofReduceBool`. -/
#print axioms FiveBoundary.RootInterfaces.not_mem_forbidden_iff
#print axioms FiveBoundary.RootInterfaces.forbidden_antitone
#print axioms FiveBoundary.RootInterfaces.mem_forbidden_single_iff
#print axioms FiveBoundary.RootInterfaces.mem_forbidden_single_iff_eq
#print axioms FiveBoundary.RootInterfaces.mem_avail_hub_iff
#print axioms FiveBoundary.RootInterfaces.avail_hub
#print axioms FiveBoundary.RootInterfaces.avail_eq_inter
#print axioms FiveBoundary.RootInterfaces.listColorable_iff_avail_nonempty
#print axioms FiveBoundary.RootInterfaces.listColorable_iff_inter_nonempty
#print axioms FiveBoundary.RootInterfaces.listColorable_hub_iff
#print axioms FiveBoundary.RootInterfaces.transfer_empty
#print axioms FiveBoundary.RootInterfaces.transfer_singleton
#print axioms FiveBoundary.RootInterfaces.transfer_of_two
#print axioms FiveBoundary.RootInterfaces.private_colours
#print axioms FiveBoundary.RootInterfaces.card_le_of_irredundant_cover
