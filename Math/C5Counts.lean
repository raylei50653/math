/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.Enumeration

/-! Abstract extension-count layer for one ordered C5 (docs/c5_adjacent_singleton_counts.md,
docs/c5_count_cone_bridge.md). `x j` is the extension count of the four-colour state whose
repeated pair is chord `j`; `y i` is the count of the three-colour state whose singleton sits
at `v_i`. Everything here is integer algebra on these ten numbers. The inclusion–exclusion
step that produces the coefficients `a₀, a e` from a disk graph, and the noncrossing
topology behind it, remain paper premises and are NOT formalized. -/
namespace FiveBoundary.C5Counts

/-- Chord `j` of the ordered C5 is the non-adjacent pair `{j, j+2}`. -/
def chord (j : Fin 5) : Finset (Fin 5) := {j, j + 2}

theorem chord_not_adj : ∀ j : Fin 5, ¬ C5.Adj j (j + 2) := by decide

/-- Every non-adjacent pair of C5 is one of the five chords. -/
theorem chord_of_nonadj : ∀ u v : Fin 5, u ≠ v → ¬ C5.Adj u v → ∃ j, chord j = {u, v} := by
  decide

theorem chord_injective : ∀ j j' : Fin 5, chord j = chord j' → j = j' := by decide

/-- The two repeated pairs of the singleton-`i` state are chords `i+1` and `i+2`, so for
chord `j = {j, j+2}` the set `{j, e_j, f_j, e_{j+2}, f_{j+2}}` is all five chords. -/
theorem five_shifts_cover : ∀ j : Fin 5,
    ({j, j + 1, j + 2, j + 3, j + 4} : Finset (Fin 5)) = Finset.univ := by decide

/-- Complement of a chord inside the boundary. -/
theorem chord_compl : ∀ j : Fin 5, (chord j)ᶜ = {j + 1, j + 3, j + 4} := by decide

/-- Extension counts per fixed labelled boundary assignment: `x` by chord, `y` by singleton. -/
@[ext] structure Counts where
  x : Fin 5 → ℤ
  y : Fin 5 → ℤ

/-- The chord total `x_uv + y_u + y_v` does not depend on the chord. -/
def ChordTotalConst (N : Counts) : Prop :=
  ∀ j j', N.x j + N.y j + N.y (j + 2) = N.x j' + N.y j' + N.y (j' + 2)

instance (N : Counts) : Decidable (ChordTotalConst N) :=
  inferInstanceAs (Decidable (∀ j j' : Fin 5,
    N.x j + N.y j + N.y (j + 2) = N.x j' + N.y j' + N.y (j' + 2)))

/-- The common chord total `L`. -/
def total (N : Counts) : ℤ := N.x 0 + N.y 0 + N.y 2

/-- The algebraic parameter `m = L - Σ y`. -/
def m (N : Counts) : ℤ := total N - ∑ i, N.y i

/-- Slack of the translated Dvořák–Lidický Conjecture 9: `3 Σ y - Σ x`. -/
def slack (N : Counts) : ℤ := 3 * ∑ i, N.y i - ∑ j, N.x j

/-- Counts assembled from inclusion–exclusion coefficients: `a₀` for the discrete
boundary partition and `a j` for the single-chord partition `{j, j+2}`. The paper argument
shows any disk cell has this shape; the shape itself is the premise here. -/
def ofCoefficients (a₀ : ℤ) (a : Fin 5 → ℤ) : Counts where
  x j := a₀ + a j
  y i := a₀ + a (i + 1) + a (i + 2)

theorem ofCoefficients_total (a₀ : ℤ) (a : Fin 5 → ℤ) (j : Fin 5) :
    (ofCoefficients a₀ a).x j + (ofCoefficients a₀ a).y j + (ofCoefficients a₀ a).y (j + 2) =
      3 * a₀ + ∑ e, a e := by
  simp only [ofCoefficients, Fin.sum_univ_five]
  fin_cases j <;> simp <;> ring

/-- Paper theorem §2 of docs/c5_adjacent_singleton_counts.md, algebraic half. -/
theorem ofCoefficients_chordTotalConst (a₀ : ℤ) (a : Fin 5 → ℤ) :
    ChordTotalConst (ofCoefficients a₀ a) := by
  intro j j'
  rw [ofCoefficients_total, ofCoefficients_total]

theorem total_eq {N : Counts} (h : ChordTotalConst N) (j : Fin 5) :
    N.x j + N.y j + N.y (j + 2) = total N := h j 0

/-- `x_uv = m + Σ_{i ∉ {u,v}} y_i`. -/
theorem x_eq_m_add {N : Counts} (h : ChordTotalConst N) (j : Fin 5) :
    N.x j = m N + N.y (j + 1) + N.y (j + 3) + N.y (j + 4) := by
  have ht := total_eq h j
  unfold m
  rw [← ht, Fin.sum_univ_five]
  fin_cases j <;> simp <;> ring

theorem sum_x {N : Counts} (h : ChordTotalConst N) :
    ∑ j, N.x j = 5 * m N + 3 * ∑ i, N.y i := by
  simp only [Fin.sum_univ_five]
  rw [x_eq_m_add h 0, x_eq_m_add h 1, x_eq_m_add h 2, x_eq_m_add h 3, x_eq_m_add h 4]
  simp
  ring

theorem slack_eq {N : Counts} (h : ChordTotalConst N) : slack N = -5 * m N := by
  unfold slack
  rw [sum_x h]
  ring

/-- Conjecture 9 of Dvořák–Lidický, translated through the XOR edge-word correspondence,
reads `3 Σ y ≥ Σ x`. Under the chord-total identity it is exactly `m ≤ 0`. -/
theorem conjecture9_iff {N : Counts} (h : ChordTotalConst N) :
    (∑ j, N.x j ≤ 3 * ∑ i, N.y i) ↔ m N ≤ 0 := by
  rw [sum_x h]
  constructor <;> intro hm <;> linarith

/-- Every independent set of C5 lies inside some chord. -/
theorem independent_subset_chord :
    ∀ P : Finset (Fin 5), (∀ i ∈ P, i + 1 ∉ P) → ∃ j, P ⊆ chord j := by decide

/-- Counterexample-preservation lemma (docs/c5_count_cone_bridge.md §2), abstract half.
If the singleton support lies in chord `e` and the four-colour state of `e` extends, then
`m = x_e > 0` and every four-colour state extends. -/
theorem all_chords_positive {N : Counts} (h : ChordTotalConst N) (hy : ∀ i, 0 ≤ N.y i)
    (e : Fin 5) (hP : ∀ i, 0 < N.y i → i ∈ chord e) (he : 0 < N.x e) :
    m N = N.x e ∧ 0 < m N ∧ ∀ f, 0 < N.x f := by
  have hzero : ∀ i, i ∉ chord e → N.y i = 0 := by
    intro i hi
    by_contra hne
    exact hi (hP i (lt_of_le_of_ne (hy i) (Ne.symm hne)))
  have hnot : ∀ e : Fin 5, e + 1 ∉ chord e ∧ e + 3 ∉ chord e ∧ e + 4 ∉ chord e := by decide
  obtain ⟨h1, h3, h4⟩ := hnot e
  have hm : m N = N.x e := by
    rw [x_eq_m_add h e, hzero _ h1, hzero _ h3, hzero _ h4]
    ring
  refine ⟨hm, hm ▸ he, fun f => ?_⟩
  rw [x_eq_m_add h f]
  have := hy (f + 1); have := hy (f + 3); have := hy (f + 4)
  linarith

/-- Hence any such counterexample violates the translated Conjecture 9. -/
theorem counterexample_violates_conjecture9 {N : Counts} (h : ChordTotalConst N)
    (hy : ∀ i, 0 ≤ N.y i) (e : Fin 5) (hP : ∀ i, 0 < N.y i → i ∈ chord e) (he : 0 < N.x e) :
    ¬ (∑ j, N.x j ≤ 3 * ∑ i, N.y i) := by
  rw [conjecture9_iff h]
  have := (all_chords_positive h hy e hP he).2.1
  omega

/-! ### Abstract countermodels `N_P = t + Σ_{i ∈ P} f_i` -/

instance : Add Counts := ⟨fun N M => ⟨fun j => N.x j + M.x j, fun i => N.y i + M.y i⟩⟩
instance : Zero Counts := ⟨⟨fun _ => 0, fun _ => 0⟩⟩

@[simp] theorem add_x (N M : Counts) (j : Fin 5) : (N + M).x j = N.x j + M.x j := rfl
@[simp] theorem add_y (N M : Counts) (i : Fin 5) : (N + M).y i = N.y i + M.y i := rfl
@[simp] theorem zero_x (j : Fin 5) : (0 : Counts).x j = 0 := rfl
@[simp] theorem zero_y (i : Fin 5) : (0 : Counts).y i = 0 := rfl

instance : AddCommMonoid Counts where
  add_assoc a b c := by ext <;> simp [add_assoc]
  zero_add a := by ext <;> simp
  add_zero a := by ext <;> simp
  add_comm a b := by ext <;> simp [add_comm]
  nsmul := nsmulRec

/-- Sums of count vectors keep the chord-total identity. -/
theorem chordTotalConst_add {N M : Counts} (hN : ChordTotalConst N) (hM : ChordTotalConst M) :
    ChordTotalConst (N + M) := by
  intro j j'
  simp only [add_x, add_y]
  have := hN j j'; have := hM j j'
  linarith

/-- `t`: one for each four-colour state, zero for each three-colour state. This is an
abstract vector, not a realized cell count. -/
def t : Counts := ⟨fun _ => 1, fun _ => 0⟩

/-- `f_i`: extension counts of the pentagon fan with both chords at `v_i`. -/
def fan (i : Fin 5) : Counts :=
  ⟨fun j => if i ∈ chord j then 0 else 1, fun k => if k = i then 1 else 0⟩

def NP (P : Finset (Fin 5)) : Counts := t + ∑ i ∈ P, fan i

theorem t_chordTotalConst : ChordTotalConst t := by decide
theorem fan_chordTotalConst : ∀ i, ChordTotalConst (fan i) := by decide

theorem NP_chordTotalConst (P : Finset (Fin 5)) : ChordTotalConst (NP P) := by
  unfold NP
  refine chordTotalConst_add t_chordTotalConst ?_
  induction P using Finset.induction_on with
  | empty => intro j j'; simp
  | insert a s ha ih =>
    rw [Finset.sum_insert ha]
    exact chordTotalConst_add (fan_chordTotalConst a) ih

theorem t_m : m t = 1 := by decide
theorem fan_m : ∀ i, m (fan i) = 0 := by decide

theorem m_add (N M : Counts) : m (N + M) = m N + m M := by
  simp only [m, total, add_x, add_y, Finset.sum_add_distrib]
  ring

/-- Every `N_P` has `m = 1`, hence slack `-5` against the translated Conjecture 9,
independently of whether `P` is independent. -/
theorem NP_m (P : Finset (Fin 5)) : m (NP P) = 1 := by
  unfold NP
  rw [m_add, t_m]
  have : m (∑ i ∈ P, fan i) = 0 := by
    induction P using Finset.induction_on with
    | empty => decide
    | insert a s ha ih => rw [Finset.sum_insert ha, m_add, fan_m, ih]; rfl
  rw [this]; rfl

theorem NP_slack (P : Finset (Fin 5)) : slack (NP P) = -5 := by
  rw [slack_eq (NP_chordTotalConst P), NP_m]; rfl

theorem sumFan_x (P : Finset (Fin 5)) (j : Fin 5) :
    (∑ i ∈ P, fan i).x j = ∑ i ∈ P, (fan i).x j := by
  induction P using Finset.induction_on with
  | empty => rfl
  | insert a s ha ih => rw [Finset.sum_insert ha, Finset.sum_insert ha, add_x, ih]

theorem sumFan_y (P : Finset (Fin 5)) (k : Fin 5) :
    (∑ i ∈ P, fan i).y k = ∑ i ∈ P, (fan i).y k := by
  induction P using Finset.induction_on with
  | empty => rfl
  | insert a s ha ih => rw [Finset.sum_insert ha, Finset.sum_insert ha, add_y, ih]

theorem NP_y (P : Finset (Fin 5)) (k : Fin 5) : (NP P).y k = if k ∈ P then 1 else 0 := by
  rw [NP, add_y, sumFan_y]
  simp [fan, t]

theorem NP_x (P : Finset (Fin 5)) (j : Fin 5) :
    (NP P).x j = 1 + (P.filter (fun i => i ∉ chord j)).card := by
  rw [NP, add_x, sumFan_x]
  simp [fan, t, Finset.sum_ite]

/-- The singleton support of `N_P` is exactly `P`, and all five `x` are positive. -/
theorem NP_support (P : Finset (Fin 5)) :
    (∀ i, 0 < (NP P).y i ↔ i ∈ P) ∧ ∀ j, 0 < (NP P).x j := by
  refine ⟨fun i => ?_, fun j => ?_⟩
  · rw [NP_y]; split_ifs <;> simp_all
  · rw [NP_x]; positivity

end FiveBoundary.C5Counts
