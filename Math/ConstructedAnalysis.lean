/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.ConstructedOriginal
import Math.ConstructedMinimal

/-! Exact meaning of the constructed 11-vertex BAD, with no planarity axiom. -/
set_option linter.style.nativeDecide false
set_option linter.style.setOption false

namespace FiveBoundary.ConstructedAnalysis
set_option maxRecDepth 100000
set_option maxHeartbeats 0

def minimal : SplitCertificate := ConstructedMinimal.certificates[0]

theorem minimal_valid : checkSplitCertificate minimal = true :=
  (List.all_eq_true.mp ConstructedMinimal.all_certificates_valid) minimal
    (by simp [minimal, ConstructedMinimal.certificates])

theorem minimal_bad : BAD (graphOfEdges minimal.edges) (firstBoundary (by omega)) :=
  splitChecker_sound minimal minimal_valid

theorem minimal_induced : ∀ i j : Fin 5,
    (graphOfEdges minimal.edges).Adj (firstBoundary (by omega) i)
      (firstBoundary (by omega) j) ↔ C5.Adj i j := by
  native_decide

theorem expected_shape : ∀ b : BoundaryColoring,
    b ∈ minimal.expected ↔ Proper C5 b ∧ (usedColors b).card = 4 := by
  native_decide

theorem minimal_sigma_exact (b : BoundaryColoring) :
    b ∈ Sigma (graphOfEdges minimal.edges) (firstBoundary (by omega)) ↔
      Proper C5 b ∧ (usedColors b).card = 4 := by
  rw [splitChecker_exact minimal minimal_valid b]
  exact expected_shape b

theorem minimal_sigma_card : minimal.expected.card = 120 := by native_decide
theorem minimal_edge_count : minimal.edges.length = 26 := by decide

def leftEdges : List (Fin 8 × Fin 8) :=
  [(0,1),(0,4),(0,7),(1,2),(1,6),(1,7),(2,3),(2,5),
   (2,6),(3,4),(3,5),(4,5),(4,7),(5,6),(5,7),(6,7)]
def rightEdges : List (Fin 8 × Fin 8) :=
  [(0,1),(0,4),(0,7),(1,2),(1,5),(2,3),(2,5),(3,4),
   (3,5),(3,6),(4,6),(4,7),(5,6),(5,7),(6,7)]

def leftPatterns : Finset BoundaryColoring :=
  {![0,1,0,2,3], ![0,1,2,0,1], ![0,1,2,0,2], ![0,1,2,0,3],
   ![0,1,2,1,3], ![0,1,2,3,1], ![0,1,2,3,2]}
def rightPatterns : Finset BoundaryColoring :=
  {![0,1,0,1,2], ![0,1,0,2,1], ![0,1,0,2,3], ![0,1,2,0,3],
   ![0,1,2,1,2], ![0,1,2,1,3], ![0,1,2,3,1], ![0,1,2,3,2]}

theorem left_sigma : splitSigma (k := 3) leftEdges = leftPatterns.biUnion colorOrbit := by
  native_decide
theorem right_sigma : splitSigma (k := 3) rightEdges = rightPatterns.biUnion colorOrbit := by
  native_decide
theorem aligned_intersection :
    splitSigma (k := 3) leftEdges ∩ splitSigma (k := 3) rightEdges = minimal.expected := by
  rw [left_sigma, right_sigma]
  native_decide

theorem rejects_incomplete_certificate :
    checkSplitCertificate ⟨0, badEdges, ∅⟩ = false := by native_decide

end FiveBoundary.ConstructedAnalysis
