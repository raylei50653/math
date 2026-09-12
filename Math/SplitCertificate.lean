/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.Certificates
import Mathlib.Data.Fin.Tuple.Basic

/-! Enumerate interiors separately, avoiding allocation of all 4^(5+k) colorings. -/
namespace FiveBoundary

def edgeCheck {n : ℕ} (edges : List (Fin n × Fin n)) (c : Fin n → Color) : Bool :=
  edges.all (fun e => decide (e.1 = e.2 ∨ c e.1 ≠ c e.2))

theorem edgeCheck_exact {n : ℕ} (edges : List (Fin n × Fin n)) (c : Fin n → Color) :
    edgeCheck edges c = true ↔ Proper (graphOfEdges edges) c := by
  simp only [edgeCheck, List.all_eq_true, decide_eq_true_eq]
  constructor
  · intro h u v ⟨hne, he⟩
    rcases he with he | he
    · exact (h (u, v) he).resolve_left hne
    · exact Ne.symm ((h (v, u) he).resolve_left hne.symm)
  · intro h e he
    by_cases hn : e.1 = e.2
    · exact Or.inl hn
    · exact Or.inr (h e.1 e.2 ⟨hn, Or.inl he⟩)

def splitSigma {k : ℕ} (edges : List (Fin (5 + k) × Fin (5 + k))) :
    Finset BoundaryColoring :=
  properBoundary.filter (fun b => ∃ inside : Fin k → Color,
    edgeCheck edges (Fin.append b inside) = true)

theorem splitSigma_exact {k : ℕ} (edges : List (Fin (5 + k) × Fin (5 + k)))
    (hc : boundaryIsCycle (graphOfEdges edges) (firstBoundary (by omega)))
    (b : BoundaryColoring) :
    b ∈ splitSigma edges ↔ b ∈ Sigma (graphOfEdges edges) (firstBoundary (by omega)) := by
  constructor
  · intro hb
    obtain ⟨_, inside, hi⟩ := Finset.mem_filter.mp hb
    refine ⟨Fin.append b inside, (edgeCheck_exact _ _).mp hi, ?_⟩
    funext i
    simp [boundaryColoring, firstBoundary]
  · rintro ⟨c, hp, rfl⟩
    apply Finset.mem_filter.mpr
    constructor
    · exact Finset.mem_filter.mpr ⟨Finset.mem_univ _, restrict_proper hc hp⟩
    · refine ⟨fun i => c (Fin.natAdd 5 i), ?_⟩
      have h : Fin.append (boundaryColoring (firstBoundary (by omega)) c)
          (fun i => c (Fin.natAdd 5 i)) = c := by
        exact Fin.append_castAdd_natAdd
      rw [h]
      exact (edgeCheck_exact _ _).mpr hp

structure SplitCertificate where
  k : ℕ
  edges : List (Fin (5 + k) × Fin (5 + k))
  expected : Finset BoundaryColoring

/-- Exact relation certificate: GOOD, BAD and empty states are all allowed. -/
def checkRelationCertificate (c : SplitCertificate) : Bool :=
  decide (c.edges.Nodup ∧ (∀ e ∈ c.edges, e.1 < e.2) ∧
    boundaryIsCycle (graphOfEdges c.edges) (firstBoundary (by omega)) ∧
    splitSigma c.edges = c.expected)

theorem relationChecker_exact (c : SplitCertificate) (h : checkRelationCertificate c = true)
    (b : BoundaryColoring) :
    b ∈ Sigma (graphOfEdges c.edges) (firstBoundary (by omega)) ↔ b ∈ c.expected := by
  simp only [checkRelationCertificate, decide_eq_true_eq] at h
  rw [← splitSigma_exact c.edges h.2.2.1 b, h.2.2.2]

def checkSplitCertificate (c : SplitCertificate) : Bool :=
  let actual := splitSigma c.edges
  decide (c.edges.Nodup ∧ (∀ e ∈ c.edges, e.1 < e.2) ∧
    boundaryIsCycle (graphOfEdges c.edges) (firstBoundary (by omega)) ∧
    actual = c.expected ∧ actual.Nonempty ∧
    ∀ b ∈ actual, (usedColors b).card > 3)

theorem splitChecker_sound (c : SplitCertificate) (h : checkSplitCertificate c = true) :
    BAD (graphOfEdges c.edges) (firstBoundary (by omega)) := by
  simp only [checkSplitCertificate, decide_eq_true_eq] at h
  obtain ⟨_, _, hc, _, ⟨b, hb⟩, hall⟩ := h
  refine ⟨⟨b, (splitSigma_exact c.edges hc b).mp hb⟩, ?_⟩
  rintro ⟨a, ha, hcard⟩
  exact Nat.not_lt_of_ge hcard (hall a ((splitSigma_exact c.edges hc a).mpr ha))

theorem splitChecker_exact (c : SplitCertificate) (h : checkSplitCertificate c = true)
    (b : BoundaryColoring) :
    b ∈ Sigma (graphOfEdges c.edges) (firstBoundary (by omega)) ↔ b ∈ c.expected := by
  simp only [checkSplitCertificate, decide_eq_true_eq] at h
  rw [← splitSigma_exact c.edges h.2.2.1 b, h.2.2.2.1]

end FiveBoundary
