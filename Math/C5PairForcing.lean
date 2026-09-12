/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.BoundaryRelations
import Math.FanPentagon

/-! This round instantiates and checks pair forcing on ONE ordered C5 only.
The full fan relation and the C5 universe have identical pair marginals but
different conditional forcing. Native finite checks are explicitly audited.
-/
set_option linter.style.nativeDecide false
set_option linter.style.setOption false
namespace FiveBoundary.C5PairForcing
open BoundaryRelations

set_option maxRecDepth 100000
set_option maxHeartbeats 0

def guard (b : BoundaryColoring) : Prop := b 1 = b 4 ∧ b 0 ≠ b 2
instance (b : BoundaryColoring) : Decidable (guard b) := inferInstanceAs (Decidable (_ ∧ _))

theorem fan_guard_forces : ForcesEq (condition FanPentagon.expected guard) 0 3 := by
  unfold ForcesEq Forces
  native_decide

theorem universe_guard_not_forces : ¬ ForcesEq (condition properBoundary guard) 0 3 := by
  unfold ForcesEq Forces
  native_decide

theorem all_pair_projections_equal : ∀ i j : Fin 5,
    pairProjection FanPentagon.expected i j = pairProjection properBoundary i j := by
  native_decide

theorem full_relations_differ : FanPentagon.expected ≠ properBoundary := by native_decide

/-- Thus no collection of unconditional pair projections recovers these
complete states or their conditional forcing behaviour. -/
theorem pairwise_information_insufficient :
    (∀ i j : Fin 5,
      pairProjection FanPentagon.expected i j = pairProjection properBoundary i j) ∧
    FanPentagon.expected ≠ properBoundary ∧
    ForcesEq (condition FanPentagon.expected guard) 0 3 ∧
    ¬ ForcesEq (condition properBoundary guard) 0 3 :=
  ⟨all_pair_projections_equal, full_relations_differ, fan_guard_forces, universe_guard_not_forces⟩

end FiveBoundary.C5PairForcing
