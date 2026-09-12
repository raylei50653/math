/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.TriangleConstraints
import Math.State

/-! Colour automaton for the triangle grammar: ordered C5 + interior K3 + boundary-to-K3
attachments. The automaton scans the five boundary vertices in order; its state is the
triple of forbidden colour sets of the three interior vertices. Its semantics are proved
exactly against `Sigma`, for every attachment word, without native computation. -/
namespace FiveBoundary.ColorDFA
open Gadget

/-- Letter `i`: the interior vertices attached to boundary vertex `i`. -/
abbrev Word := Fin 5 → Finset (Fin 3)

def linksOf (w : Word) : Links := fun k => Finset.univ.filter (fun i => k ∈ w i)
def wordOf (l : Links) : Word := fun i => Finset.univ.filter (fun k => i ∈ l k)

theorem linksOf_wordOf (l : Links) : linksOf (wordOf l) = l := by
  funext k; ext i; simp [linksOf, wordOf]
theorem wordOf_linksOf (w : Word) : wordOf (linksOf w) = w := by
  funext i; ext k; simp [linksOf, wordOf]

/-- Forbidden colours of each interior vertex. -/
abbrev State := Fin 3 → Finset Color

def start : State := fun _ => ∅

def step (s : State) (letter : Finset (Fin 3)) (c : Color) : State :=
  fun k => if k ∈ letter then insert c (s k) else s k

def runFrom (w : Word) (b : BoundaryColoring) (s : State) : List (Fin 5) → State
  | [] => s
  | i :: l => runFrom w b (step s (w i) (b i)) l

def run (w : Word) (b : BoundaryColoring) : State := runFrom w b start (List.finRange 5)

/-- State invariant: after reading the positions in `l`, vertex `k` has seen exactly the
colours of its neighbours among `l`. -/
theorem runFrom_spec (w : Word) (b : BoundaryColoring) (s : State) (l : List (Fin 5)) (k : Fin 3) :
    runFrom w b s l k = s k ∪ (l.filter (fun i => k ∈ w i)).toFinset.image b := by
  induction l generalizing s with
  | nil => simp [runFrom]
  | cons i l ih =>
    rw [runFrom, ih]
    by_cases h : k ∈ w i
    · ext c
      simp [step, h]
    · simp [step, h]

theorem step_spec (s : State) (letter : Finset (Fin 3)) (c : Color) (k : Fin 3) :
    step s letter c k = if k ∈ letter then insert c (s k) else s k := rfl

theorem run_spec (w : Word) (b : BoundaryColoring) (k : Fin 3) :
    run w b k = (linksOf w k).image b := by
  rw [run, runFrom_spec]
  have : ((List.finRange 5).filter (fun i => k ∈ w i)).toFinset = linksOf w k := by
    ext i; simp [linksOf]
  rw [this]
  simp [start]

/-- Terminal acceptance: the K3 takes three distinct colours outside the forbidden sets. -/
def Accept (s : State) : Prop := ∃ t : Fin 3 → Color, Function.Injective t ∧ ∀ k, t k ∉ s k

instance (s : State) : Decidable (Accept s) :=
  inferInstanceAs (Decidable (∃ t : Fin 3 → Color, Function.Injective t ∧ ∀ k, t k ∉ s k))

theorem accept_iff_triangleCan (w : Word) (b : BoundaryColoring) :
    Accept (run w b) ↔ TriangleCan (linksOf w) b := by
  unfold Accept TriangleCan Allowed
  simp only [run_spec, Finset.mem_image, not_exists, not_and]
  constructor
  · rintro ⟨t, ht, h⟩
    exact ⟨t, ht, fun k j hj e => h k j hj e.symm⟩
  · rintro ⟨t, ht, h⟩
    exact ⟨t, ht, fun k j hj e => h k j hj e.symm⟩

/-! ### Exact semantics of the compiled graph, for every attachment set. -/

def baseEdges : List (Fin 8 × Fin 8) := [(0,1),(0,4),(1,2),(2,3),(3,4),(5,6),(5,7),(6,7)]

abbrev outer (i : Fin 5) : Fin 8 := Fin.castLE (by omega) i
abbrev inner (k : Fin 3) : Fin 8 := Fin.natAdd 5 k

theorem mem_triangleEdges (l : Links) (e : Fin 8 × Fin 8) :
    e ∈ triangleEdges l ↔ e ∈ baseEdges ∨ ∃ k j, j ∈ l k ∧ e = (outer j, inner k) := by
  simp only [triangleEdges, baseEdges, List.mem_append, List.mem_flatMap, List.mem_filterMap,
    List.mem_finRange, true_and, Option.ite_none_right_eq_some, Option.some.injEq]
  constructor
  · rintro (h | ⟨k, j, hj, rfl⟩)
    · exact Or.inl h
    · exact Or.inr ⟨k, j, hj, rfl⟩
  · rintro (h | ⟨k, j, hj, rfl⟩)
    · exact Or.inl h
    · exact Or.inr ⟨k, j, hj, rfl⟩

theorem base_cycle : ∀ i j : Fin 5, C5.Adj i j →
    (outer i, outer j) ∈ baseEdges ∨ (outer j, outer i) ∈ baseEdges := by decide
theorem base_triangle : ∀ k k' : Fin 3, k ≠ k' →
    (inner k, inner k') ∈ baseEdges ∨ (inner k', inner k) ∈ baseEdges := by decide
theorem base_cases : ∀ e ∈ baseEdges,
    (∃ i j, C5.Adj i j ∧ e = (outer i, outer j)) ∨
    (∃ k k', k ≠ k' ∧ e = (inner k, inner k')) := by decide
theorem outer_ne_inner (j : Fin 5) (k : Fin 3) : outer j ≠ inner k := by
  intro h
  have := congrArg Fin.val h
  simp at this
  omega

theorem adj_of_mem (l : Links) {u v : Fin 8} (hne : u ≠ v)
    (h : (u, v) ∈ triangleEdges l ∨ (v, u) ∈ triangleEdges l) :
    (graphOfEdges (triangleEdges l)).Adj u v := ⟨hne, h⟩

/-- A colouring of the compiled graph is proper iff the boundary is a proper C5 colouring,
the triangle is injective, and every attachment separates its endpoints. -/
theorem proper_triangle (l : Links) (c : Fin 8 → Color) :
    Proper (graphOfEdges (triangleEdges l)) c ↔
      Proper C5 (fun i => c (outer i)) ∧ Function.Injective (fun k => c (inner k)) ∧
      ∀ k, ∀ j ∈ l k, c (inner k) ≠ c (outer j) := by
  constructor
  · intro hc
    refine ⟨?_, ?_, ?_⟩
    · intro i j hij
      have hne : outer i ≠ outer j := fun h => C5.ne_of_adj hij (Fin.castLE_injective _ h)
      exact hc _ _ (adj_of_mem l hne ((base_cycle i j hij).imp
        (fun h => (mem_triangleEdges l _).mpr (Or.inl h))
        (fun h => (mem_triangleEdges l _).mpr (Or.inl h))))
    · intro k k' e
      by_contra hkk
      have hne : inner k ≠ inner k' := fun h =>
        hkk (by simpa [Fin.ext_iff] using congrArg Fin.val h)
      exact hc _ _ (adj_of_mem l hne ((base_triangle k k' hkk).imp
        (fun h => (mem_triangleEdges l _).mpr (Or.inl h))
        (fun h => (mem_triangleEdges l _).mpr (Or.inl h)))) e
    · intro k j hj
      exact hc _ _ (adj_of_mem l (outer_ne_inner j k).symm
        (Or.inr ((mem_triangleEdges l _).mpr (Or.inr ⟨k, j, hj, rfl⟩))))
  · rintro ⟨hb, ht, hl⟩
    have key : ∀ e ∈ triangleEdges l, c e.1 ≠ c e.2 := by
      intro e he
      rcases (mem_triangleEdges l e).mp he with h | ⟨k, j, hj, rfl⟩
      · rcases base_cases e h with ⟨i, j, hij, rfl⟩ | ⟨k, k', hkk, rfl⟩
        · exact hb i j hij
        · exact fun h => hkk (ht h)
      · exact (hl k j hj).symm
    rintro u v ⟨_, h | h⟩
    · exact key _ h
    · exact (key _ h).symm

theorem boundaryIsCycle_triangle (l : Links) :
    boundaryIsCycle (graphOfEdges (triangleEdges l)) (firstBoundary (by omega)) := by
  intro i j hij
  have hne : outer i ≠ outer j := fun h => C5.ne_of_adj hij (Fin.castLE_injective _ h)
  exact adj_of_mem l hne ((base_cycle i j hij).imp
    (fun h => (mem_triangleEdges l _).mpr (Or.inl h))
    (fun h => (mem_triangleEdges l _).mpr (Or.inl h)))

/-- Exact boundary relation of every compiled triangle gadget. -/
theorem mem_sigma_triangle (l : Links) (b : BoundaryColoring) :
    b ∈ Sigma (graphOfEdges (triangleEdges l)) (firstBoundary (by omega)) ↔
      Proper C5 b ∧ TriangleCan l b := by
  constructor
  · rintro ⟨c, hc, rfl⟩
    obtain ⟨hb, ht, hl⟩ := (proper_triangle l c).mp hc
    exact ⟨hb, fun k => c (inner k), ht, fun k j hj => hl k j hj⟩
  · rintro ⟨hb, t, ht, ha⟩
    refine ⟨Fin.append b t, (proper_triangle l _).mpr ⟨?_, ?_, ?_⟩, ?_⟩
    · intro i j hij
      change Fin.append b t (Fin.castAdd 3 i) ≠ Fin.append b t (Fin.castAdd 3 j)
      simpa [Fin.append_left] using hb i j hij
    · intro k k' e
      apply ht
      simpa [Fin.append_right] using e
    · intro k j hj
      change Fin.append b t (Fin.natAdd 5 k) ≠ Fin.append b t (Fin.castAdd 3 j)
      simpa [Fin.append_left, Fin.append_right] using ha k j hj
    · funext i
      change Fin.append b t (Fin.castAdd 3 i) = b i
      simp [Fin.append_left]

/-- The automaton computes exactly the boundary relation of the compiled graph. -/
theorem sigma_iff_accept (w : Word) (b : BoundaryColoring) :
    b ∈ Sigma (graphOfEdges (triangleEdges (linksOf w))) (firstBoundary (by omega)) ↔
      Proper C5 b ∧ Accept (run w b) := by
  rw [mem_sigma_triangle, accept_iff_triangleCan]

/-- Connection to the exact split checker used by every certificate. -/
theorem splitSigma_triangle (w : Word) :
    splitSigma (k := 3) (triangleEdges (linksOf w)) =
      properBoundary.filter (fun b => Accept (run w b)) := by
  ext b
  rw [splitSigma_exact _ (boundaryIsCycle_triangle _), sigma_iff_accept]
  simp [properBoundary]

/-- The ten-bit colour-orbit state of `State.lean`, read off the automaton. -/
def acceptedReps (w : Word) : Finset BoundaryColoring :=
  colorReps.filter (fun b => Accept (run w b))

theorem colorReps_proper : ∀ b ∈ colorReps, Proper C5 b := by decide +kernel

theorem acceptedReps_exact (w : Word) :
    acceptedReps w = abstractColors (splitSigma (k := 3) (triangleEdges (linksOf w))) := by
  ext b
  rw [splitSigma_triangle]
  simp only [acceptedReps, abstractColors, Finset.mem_filter, properBoundary, Finset.mem_univ,
    true_and]
  constructor
  · rintro ⟨hb, ha⟩; exact ⟨hb, colorReps_proper b hb, ha⟩
  · rintro ⟨hb, _, ha⟩; exact ⟨hb, ha⟩

/-- Read the attachment word back from a stored edge list of any size. -/
def wordOfEdges {n : ℕ} (edges : List (Fin n × Fin n)) : Word := fun i =>
  Finset.univ.filter (fun k : Fin 3 => ∃ e ∈ edges, e.1.val = i.val ∧ e.2.val = 5 + k.val)

end FiveBoundary.ColorDFA

/-! ### Mask enumeration of the 32,768 words, without enumerating the function type. -/
namespace FiveBoundary.ColorDFA

def letterOf : Fin 8 → Finset (Fin 3) := ![∅, {0}, {1}, {0, 1}, {2}, {0, 2}, {1, 2}, {0, 1, 2}]

theorem letterOf_surjective : ∀ s : Finset (Fin 3), ∃ l : Fin 8, letterOf l = s := by decide

/-- Bits `3*i + k` of the mask: boundary vertex `i` attached to interior vertex `k`. -/
def wordOfMask (m : ℕ) : Word := fun i => letterOf ⟨m / 8 ^ i.val % 8, Nat.mod_lt _ (by norm_num)⟩

theorem wordOfMask_surjective (w : Word) : ∃ m : Fin 32768, wordOfMask m.val = w := by
  choose l hl using fun i => letterOf_surjective (w i)
  refine ⟨⟨(l 0).val + 8 * (l 1).val + 64 * (l 2).val + 512 * (l 3).val + 4096 * (l 4).val,
    by omega⟩, ?_⟩
  funext i
  rw [← hl i]
  fin_cases i <;> simp only [wordOfMask] <;> congr 1 <;> ext <;> simp <;> omega

theorem card_word : Fintype.card Word = 32768 := by
  simp [Fintype.card_pi, Fintype.card_finset]

end FiveBoundary.ColorDFA

/-! ### Executable acceptance test without enumerating the function type `Fin 3 → Color`. -/
namespace FiveBoundary.ColorDFA

def acceptB (s : State) : Bool :=
  (List.finRange 4).any fun a => (List.finRange 4).any fun b => (List.finRange 4).any fun c =>
    decide (a ≠ b ∧ a ≠ c ∧ b ≠ c ∧ a ∉ s 0 ∧ b ∉ s 1 ∧ c ∉ s 2)

theorem acceptB_iff (s : State) : acceptB s = true ↔ Accept s := by
  simp only [acceptB, List.any_eq_true, List.mem_finRange, true_and, decide_eq_true_eq]
  constructor
  · rintro ⟨a, b, c, hab, hac, hbc, ha, hb, hc⟩
    refine ⟨![a, b, c], ?_, ?_⟩
    · intro i j h
      fin_cases i <;> fin_cases j <;> simp_all
    · intro k; fin_cases k <;> assumption
  · rintro ⟨t, ht, h⟩
    exact ⟨t 0, t 1, t 2, fun e => by simpa using ht e, fun e => by simpa using ht e,
      fun e => by simpa using ht e, h 0, h 1, h 2⟩

end FiveBoundary.ColorDFA
