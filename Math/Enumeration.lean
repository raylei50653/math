/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.Boundary

/-! Exhaustive C5 orbits. Native computation is intentional; see docs/phase1.md. -/
set_option linter.style.nativeDecide false
set_option linter.style.setOption false

namespace FiveBoundary
set_option maxRecDepth 100000
set_option maxHeartbeats 800000
set_option Elab.async false

def properBoundary : Finset BoundaryColoring := Finset.univ.filter (Proper C5)

def colorOrbit (b : BoundaryColoring) : Finset BoundaryColoring :=
  Finset.univ.image (fun p : Equiv.Perm Color => colorAction p b)

def fullOrbit (b : BoundaryColoring) : Finset BoundaryColoring :=
  Finset.univ.biUnion (fun d : D5 => colorOrbit (dihedralAction d b))

/-- Lexicographically least tuples, computed by the external enumerator and replayed below. -/
def colorReps : Finset BoundaryColoring :=
  {![0,1,0,1,2], ![0,1,0,2,1], ![0,1,0,2,3], ![0,1,2,0,1], ![0,1,2,0,2],
   ![0,1,2,0,3], ![0,1,2,1,2], ![0,1,2,1,3], ![0,1,2,3,1], ![0,1,2,3,2]}

def fullReps : Finset BoundaryColoring := {![0,1,0,1,2], ![0,1,0,2,3]}

theorem c5_count : properBoundary.card = 240 := by native_decide
theorem d5_count : Fintype.card D5 = 10 := by native_decide
theorem d5_rotations_or_reflections : ∀ p : D5, ∃ a : Fin 5,
    (∀ i, p.val i = a + i) ∨ (∀ i, p.val i = a - i) := by native_decide
theorem three_color_count :
    (properBoundary.filter (fun b => (usedColors b).card ≤ 3)).card = 120 := by native_decide
theorem color_reps_count : colorReps.card = 10 := by native_decide
theorem full_reps_count : fullReps.card = 2 := by native_decide

theorem color_orbits_cover : colorReps.biUnion colorOrbit = properBoundary := by native_decide
theorem color_orbits_disjoint :
    ∀ a ∈ colorReps, ∀ b ∈ colorReps, a ≠ b → Disjoint (colorOrbit a) (colorOrbit b) := by
  native_decide

theorem full_orbits_cover : fullReps.biUnion fullOrbit = properBoundary := by native_decide
theorem full_orbits_disjoint :
    ∀ a ∈ fullReps, ∀ b ∈ fullReps, a ≠ b → Disjoint (fullOrbit a) (fullOrbit b) := by
  native_decide

/-- Base-4 ordering agrees with lexicographic tuple ordering. -/
def code (b : BoundaryColoring) : ℕ :=
  256 * (b 0).val + 64 * (b 1).val + 16 * (b 2).val + 4 * (b 3).val + (b 4).val

theorem color_reps_minimal : ∀ r ∈ colorReps, ∀ b ∈ colorOrbit r, code r ≤ code b := by
  have checked : ∀ r ∈ colorReps, ∀ p : Equiv.Perm Color, code r ≤ code (colorAction p r) := by
    native_decide
  intro r hr b hb
  obtain ⟨p, _, rfl⟩ := Finset.mem_image.mp hb
  exact checked r hr p
theorem full_reps_minimal : ∀ r ∈ fullReps, ∀ b ∈ fullOrbit r, code r ≤ code b := by
  have checked : ∀ r ∈ fullReps, ∀ d : D5, ∀ p : Equiv.Perm Color,
      code r ≤ code (colorAction p (dihedralAction d r)) := by native_decide
  intro r hr b hb
  obtain ⟨d, _, hb⟩ := Finset.mem_biUnion.mp hb
  obtain ⟨p, _, rfl⟩ := Finset.mem_image.mp hb
  exact checked r hr d p

end FiveBoundary
