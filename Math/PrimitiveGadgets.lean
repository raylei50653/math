/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.GadgetRelations

/-! Finite exact primitive specifications; topology is NOT a Lean premise. -/
set_option linter.style.nativeDecide false
set_option linter.style.setOption false
namespace FiveBoundary.Gadget
set_option maxRecDepth 100000
set_option maxHeartbeats 0

def neqEdges : List (Fin 2 × Fin 2) := [(0,1)]
def eqEdges : List (Fin 5 × Fin 5) :=
  [(0,2),(0,3),(0,4),(1,2),(1,3),(1,4),(2,3),(2,4),(3,4)]

theorem neq_exact : ∀ x y : Color,
    (∃ c : Fin 2 → Color, Proper (graphOfEdges neqEdges) c ∧ c 0 = x ∧ c 1 = y) ↔
      x ≠ y := by native_decide

/-- K5 minus the terminal edge realizes equality. It is not a disk wire. -/
theorem eq_exact : ∀ x y : Color,
    (∃ c : Fin 5 → Color, Proper (graphOfEdges eqEdges) c ∧ c 0 = x ∧ c 1 = y) ↔
      x = y := by native_decide

def frameEdges : List (Fin 5 × Fin 5) := [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
def frame (c : Fin 5 → Color) : Prop :=
  Function.Injective (fun i : Fin 4 => c (Fin.castLE (by omega) i))
instance (c : Fin 5 → Color) : Decidable (frame c) :=
  inferInstanceAs (Decidable (Function.Injective _))

/-- Coordinates A,B,C,D = 0,1,2,3 are reference vertices, not absolute colors. -/
theorem frame_exclusion_exact : ∀ c : Fin 5 → Color,
    Proper (graphOfEdges (frameEdges ++ [(0,4),(2,4)])) c ↔
      frame c ∧ (c 4 = c 1 ∨ c 4 = c 3) := by native_decide

theorem frame_force_exact : ∀ c : Fin 5 → Color,
    Proper (graphOfEdges (frameEdges ++ [(0,4),(1,4),(2,4)])) c ↔
      frame c ∧ c 4 = c 3 := by native_decide

abbrev Frame := Equiv.Perm Color

theorem shared_frame : ∀ x y : Color,
    (∃ f : Frame, x = f 3 ∧ y = f 3) ↔ x = y := by native_decide

/-- Hiding two independent frames forgets their relative alignment entirely. -/
theorem independent_frames : ∀ x y : Color,
    ∃ f g : Frame, x = f 3 ∧ y = g 3 := by native_decide

end FiveBoundary.Gadget
