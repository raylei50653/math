/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.SplitCertificate

/-! One exact witness from the internal pentagon with diagonals 1-3 and 1-4.
The external exhaustive search and disk topology are NOT proved by this file.
The full labelled Sigma certificate intentionally uses native computation.
-/
set_option linter.style.nativeDecide false
set_option linter.style.setOption false

namespace FiveBoundary.FanPentagon

set_option maxRecDepth 100000
set_option maxHeartbeats 0

/-- Boundary 0..4; internal user labels 1..5 are vertices 5..9.
Attachment mask 1116616; exactly seven attachments. -/
def edges : List (Fin 10 × Fin 10) :=
  [(0,1), (0,4), (0,8), (1,2), (1,6), (1,7), (1,8), (2,3), (2,6),
   (3,4), (3,6), (4,5), (5,6), (5,7), (5,8), (5,9), (6,7), (7,8), (8,9)]

/-- All proper boundary colourings except the colour orbit of 01231.
Boundary positions stay labelled; there is no D5 quotient. -/
def expected : Finset BoundaryColoring :=
  properBoundary.filter (fun b => b 1 ≠ b 4 ∨ b 0 = b 2 ∨ b 0 = b 3 ∨ b 2 = b 3)

def certificate : SplitCertificate := ⟨5, edges, expected⟩

theorem checked : checkRelationCertificate certificate = true := by native_decide

theorem sigma_exact (b : BoundaryColoring) :
    b ∈ Sigma (graphOfEdges edges) (firstBoundary (by decide)) ↔ b ∈ expected :=
  relationChecker_exact certificate checked b

theorem sigma_card : expected.card = 216 := by native_decide

theorem all_three_extend :
    ∀ b ∈ properBoundary, (usedColors b).card = 3 → b ∈ expected := by native_decide

theorem rejected_pattern : ![0,1,2,3,1] ∉ expected := by decide +kernel

theorem no_extension :
    ![0,1,2,3,1] ∉ Sigma (graphOfEdges edges) (firstBoundary (by decide)) := by
  intro h
  exact rejected_pattern ((sigma_exact _).mp h)

/-- The lists induced by boundary 01231, in internal user order 1..5. -/
def available : Fin 5 → Finset Color :=
  ![{0,2,3}, {0}, {0,2,3}, {2,3}, {0,1,2,3}]

/-- These are exactly the lists imposed by the real attachment edges. -/
theorem available_exact : ∀ (k : Fin 5) (c : Color),
    c ∈ available k ↔ ∀ u : Fin 5,
      (u.castAdd 5, k.natAdd 5) ∈ edges → (![0,1,2,3,1] : BoundaryColoring) u ≠ c := by
  decide +kernel

def localTriangle (i j k : Fin 5) : Prop :=
  ∃ a ∈ available i, ∃ b ∈ available j, ∃ c ∈ available k,
    a ≠ b ∧ a ≠ c ∧ b ≠ c

/-- Every constituent triangle has a list-colouring when checked separately. -/
theorem each_triangle_feasible :
    localTriangle 0 1 2 ∧ localTriangle 0 2 3 ∧ localTriangle 0 3 4 := by
  unfold localTriangle
  decide +kernel

/-- Transparent finite pigeonhole obstruction: the first triangle forces the
hub and vertex 3 to use 2 and 3, leaving no colour for vertex 4. -/
theorem two_colour_obstruction (a b c : Color)
    (ha : a = 2 ∨ a = 3) (hb : b = 2 ∨ b = 3) (hc : c = 2 ∨ c = 3)
    (hab : a ≠ b) (hac : a ≠ c) (hbc : b ≠ c) : False := by
  rcases ha with rfl | rfl <;> rcases hb with rfl | rfl <;>
    rcases hc with rfl | rfl <;> simp_all

/-- No common assignment even for the first two triangles. This uses only
the explicit lists and the elementary obstruction, with no native decision. -/
theorem lists_incompatible : ¬ ∃ c : Fin 5 → Color,
    (∀ i, c i ∈ available i) ∧ c 0 ≠ c 1 ∧ c 0 ≠ c 2 ∧ c 0 ≠ c 3 ∧
      c 1 ≠ c 2 ∧ c 2 ≠ c 3 := by
  rintro ⟨c, hm, h01, h02, h03, h12, h23⟩
  have hz : c 1 = 0 := by simpa [available] using hm 1
  rw [hz] at h01 h12
  have ha : c 0 = 2 ∨ c 0 = 3 := by simpa [available, h01] using hm 0
  have hb : c 2 = 2 ∨ c 2 = 3 := by simpa [available, Ne.symm h12] using hm 2
  have hc : c 3 = 2 ∨ c 3 = 3 := by simpa [available] using hm 3
  exact two_colour_obstruction _ _ _ ha hb hc h02 h03 h23

end FiveBoundary.FanPentagon
