/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.TwoSpokeReflection

/-! Finite query algebra and transport only. Source reductions are paper theorems. -/
namespace FiveBoundary.TwoSpokeNonadjacent

open ForcingLists TwoSpokeReflection

abbrev Row := Fin 5 → Color

def pA : Row := ![0, 1, 0, 2, 1]
def pB : Row := ![0, 1, 2, 1, 2]

/-- The duplicate-spoke reduction and the two-color pentagon query. -/
theorem query_rows :
    pA 1 = pA 4 ∧ pB 1 = pB 3 ∧ pB 2 = pB 4 ∧
    (Finset.univ \ {pB 1, pB 4} : Finset Color) = {0, 3} := by decide

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- Kernel reduction checks all 16 color subsets and all four singleton colors.
/-- Exact finite screen, conditional on the same component's stabilizer and port bound. -/
theorem two_color_screen (F : Finset Color) (a : Color)
    (ha : a = 0 ∨ a = 3) (hcard : F.card ≤ 2)
    (hsym : ∀ c, c ∈ F ↔ Equiv.swap (0 : Color) 3 c ∈ F)
    (hcover : ({0, 3} : Finset Color) ⊆ F ∪ {a}) :
    F = {0, 3} := by
  revert F a
  decide

/-- Component identities and their ordered contacts do not exchange under reflection. -/
theorem nonadjacent_orbit :
    ({1, 4} : Finset (Fin 5)).image rho = {2, 4} ∧
    ({1, 2, 3, 4} : Finset (Fin 5)).image rho = {0, 1, 2, 4} ∧
    ({4, 0, 1} : Finset (Fin 5)).image rho = {2, 3, 4} ∧
    pi 0 = 1 ∧ pi 3 = 3 := by decide

theorem reflection_queries :
    (Equiv.swap (1 : Color) 2 ∘ reflectRow pB) = pA ∧
    (Equiv.swap (0 : Color) 2 ∘ reflectRow pA) = pB := by decide

/-- Transport both designated queries, using ordinary color invariance of extension. -/
theorem reflection_separation (accept acceptReflected : Row → Prop)
    (transport : ∀ b, acceptReflected (reflectRow b) ↔ accept b)
    (colors : ∀ (e : Equiv.Perm Color) b, acceptReflected (e ∘ b) ↔ acceptReflected b)
    (hA : accept pA) (hB : accept pB) :
    acceptReflected pA ∧ acceptReflected pB := by
  constructor
  · rw [← reflection_queries.1]
    exact (colors _ _).mpr ((transport pB).mpr hB)
  · rw [← reflection_queries.2]
    exact (colors _ _).mpr ((transport pA).mpr hA)

end FiveBoundary.TwoSpokeNonadjacent
