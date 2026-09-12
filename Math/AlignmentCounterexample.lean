/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.Certificates

/-! A whole-state D5 alignment counterexample, not a BAD disk patch.
Finite computations use native_decide, with the trust boundary of docs/phase1.md. -/
set_option linter.style.nativeDecide false
set_option linter.style.setOption false

namespace FiveBoundary.AlignmentCounterexample
set_option maxRecDepth 100000
set_option maxHeartbeats 0

/-- The reflection of C5 + {02} is C5 + {03}. -/
def reflectedEdges : List (Fin 5 × Fin 5) :=
  [(0,1),(0,3),(0,4),(1,2),(2,3),(3,4)]

def reflectedState := sigmaFinite (graphOfEdges reflectedEdges) identityBoundary

/-- The position map used below really is an element of the defined D5. -/
theorem reflection_in_D5 : ∃ p : D5, ∀ i : Fin 5, p.val i = -i := by
  native_decide

/-- Equality up to reflection of the ENTIRE accepted-coloring sets. -/
theorem whole_state_reflection : ∀ c : BoundaryColoring,
    c ∈ reflectedState ↔ (fun i => c (-i)) ∈ leftState := by
  native_decide

/-- Both alternative components are GOOD. -/
theorem reflected_good : GOOD (graphOfEdges reflectedEdges) identityBoundary := by
  native_decide

/-- The fixed context already contains edge 03, so this gluing changes no state. -/
theorem reflected_gluing : reflectedState ∩ rightState = rightState := by
  native_decide

/-- Replacing a component by a D5-equivalent whole state changes the GOOD answer. -/
theorem same_D5_class_different_context_answer :
    (∃ c ∈ reflectedState ∩ rightState, (usedColors c).card ≤ 3) ∧
    (leftState ∩ rightState).Nonempty ∧
    ¬ (∃ c ∈ leftState ∩ rightState, (usedColors c).card ≤ 3) := by
  native_decide

end FiveBoundary.AlignmentCounterexample
