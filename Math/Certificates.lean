/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.Enumeration

/-! Closed counterexamples and a complete finite certificate checker.
Native computation is intentional; see docs/phase1.md for the trust boundary. -/
set_option linter.style.nativeDecide false
set_option linter.style.setOption false

namespace FiveBoundary
set_option maxRecDepth 100000
set_option maxHeartbeats 0

def badEdges : List (Fin 5 × Fin 5) :=
  [(0,1),(0,2),(0,3),(0,4),(1,2),(1,3),(2,3),(3,4)]
def badGraph := graphOfEdges badEdges
instance : DecidableRel badGraph.Adj :=
  inferInstanceAs (DecidableRel (graphOfEdges badEdges).Adj)
def identityBoundary : Fin 5 ↪ Fin 5 := Function.Embedding.refl _
def badSigma : Finset BoundaryColoring :=
  colorOrbit ![0,1,2,3,1] ∪ colorOrbit ![0,1,2,3,2]

theorem bad_graph_boundary : boundaryIsCycle badGraph identityBoundary := by decide +kernel
theorem bad_sigma_exact : sigmaFinite badGraph identityBoundary = badSigma := by native_decide
theorem bad_sigma_card : badSigma.card = 48 := by native_decide
theorem bad_verified : BAD badGraph identityBoundary := by native_decide
theorem bad_edges_valid : badEdges.Nodup ∧ ∀ e ∈ badEdges, e.1 < e.2 := by decide +kernel

/-- Exhausts every possible chord subset on exactly the five boundary vertices. -/
def cycleEdges : List (Fin 5 × Fin 5) := [(0,1),(0,4),(1,2),(2,3),(3,4)]
def chords : List (Fin 5 × Fin 5) := [(0,2),(0,3),(1,3),(1,4),(2,4)]

theorem no_bad_with_fewer_edges :
    ∀ extra ∈ chords.sublists, extra.length < 3 →
      GOOD (graphOfEdges (cycleEdges ++ extra)) identityBoundary := by native_decide

/-- Boundary injectivity supplies the vertex lower bound independently of search. -/
theorem at_least_five_vertices {n : ℕ} (B : Fin 5 ↪ Fin n) : 5 ≤ n := by
  simpa using Fintype.card_le_of_injective B B.injective

def leftEdges : List (Fin 5 × Fin 5) := [(0,1),(0,2),(0,4),(1,2),(2,3),(3,4)]
def rightEdges : List (Fin 5 × Fin 5) := [(0,1),(0,3),(0,4),(1,2),(1,3),(2,3),(3,4)]
def leftState := sigmaFinite (graphOfEdges leftEdges) identityBoundary
def rightState := sigmaFinite (graphOfEdges rightEdges) identityBoundary

/-- The lossy abstraction records which individual S4 x D5 orbits occur. -/
def coarse (s : Finset BoundaryColoring) : Finset BoundaryColoring :=
  fullReps.filter (fun r => (s ∩ fullOrbit r).Nonempty)

theorem coarse_equal : coarse leftState = coarse rightState := by native_decide
theorem left_good : GOOD (graphOfEdges leftEdges) identityBoundary := by native_decide
theorem right_good : GOOD (graphOfEdges rightEdges) identityBoundary := by native_decide
theorem glued_bad : leftState ∩ rightState = badSigma := by native_decide
theorem coarse_not_congruent :
    coarse (leftState ∩ leftState) ≠ coarse (leftState ∩ rightState) := by native_decide

structure Certificate where
  n : ℕ
  large : 5 ≤ n
  edges : List (Fin n × Fin n)
  expected : Finset BoundaryColoring

/-- Recomputes ALL proper colourings, including absence claims, from graph data. -/
def checkCertificate (c : Certificate) : Bool :=
  let G := graphOfEdges c.edges
  let B := firstBoundary c.large
  let actual := sigmaFinite G B
  decide (c.edges.Nodup ∧ (∀ e ∈ c.edges, e.1 < e.2) ∧
    boundaryIsCycle G B ∧ actual = c.expected ∧
    actual.Nonempty ∧ ∀ b ∈ actual, (usedColors b).card > 3)

theorem checker_sound (c : Certificate) (h : checkCertificate c = true) :
    BAD (graphOfEdges c.edges) (firstBoundary c.large) := by
  simp only [checkCertificate, decide_eq_true_eq] at h
  obtain ⟨_, _, _, _, ⟨b, hb⟩, hall⟩ := h
  refine ⟨⟨b, (mem_sigmaFinite _ _ _).mp hb⟩, ?_⟩
  rintro ⟨a, ha, hcard⟩
  exact Nat.not_lt_of_ge hcard (hall a ((mem_sigmaFinite _ _ _).mpr ha))

theorem rejects_missing_sigma :
    checkCertificate ⟨5, by decide, badEdges, ∅⟩ = false := by native_decide

theorem rejects_extra_coloring :
    checkCertificate ⟨5, by decide, badEdges, insert ![0,0,0,0,0] badSigma⟩ = false := by
  native_decide

def missingBoundaryEdges := badEdges.filter (· ≠ (0,4))

theorem rejects_missing_boundary_edge :
    checkCertificate ⟨5, by decide, missingBoundaryEdges,
      sigmaFinite (graphOfEdges missingBoundaryEdges) identityBoundary⟩ = false := by
  native_decide

theorem rejects_loop :
    checkCertificate ⟨5, by decide, (0,0) :: badEdges, badSigma⟩ = false := by native_decide

end FiveBoundary
