/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.Boundary

/-! Colour-side lemmas behind the near-triangulation completion
(docs/c5_count_cone_bridge.md §3.2–§4). A properly coloured polygon either has an ear whose
two neighbours differ, or alternates two colours around an even cycle and admits a hub colour.
The Euler count for a near-triangulation with a C5 outer face is plain arithmetic.
Face structure, planarity and the disk embedding stay paper premises. -/
namespace FiveBoundary.NearTriangulation

/-- A cyclic colouring of length `n` is modelled as an `n`-periodic sequence. -/
def Periodic (n : ℕ) (c : ℕ → Color) : Prop := ∀ i, c (i + n) = c i

/-- Properness along the cycle. -/
def CycleProper (c : ℕ → Color) : Prop := ∀ i, c i ≠ c (i + 1)

/-- Vertex `i+1` is an ear when its two neighbours carry different colours. -/
def Ear (c : ℕ → Color) (i : ℕ) : Prop := c i ≠ c (i + 2)

/-- Clipping an ear produces a properly three-coloured triangle. -/
theorem ear_triangle_proper {c : ℕ → Color} (hp : CycleProper c) {i : ℕ} (h : Ear c i) :
    c i ≠ c (i + 1) ∧ c (i + 1) ≠ c (i + 2) ∧ c i ≠ c (i + 2) :=
  ⟨hp i, hp (i + 1), h⟩

/-- Without ears the colouring is two-periodic. -/
theorem two_periodic_of_no_ear {c : ℕ → Color} (h : ∀ i, ¬ Ear c i) (i : ℕ) : c i = c (i % 2) := by
  induction i using Nat.strong_induction_on with
  | _ i ih =>
    rcases Nat.lt_or_ge i 2 with hi | hi
    · rw [Nat.mod_eq_of_lt hi]
    · obtain ⟨k, rfl⟩ : ∃ k, i = k + 2 := ⟨i - 2, by omega⟩
      have := not_not.mp (h k)
      rw [← this, ih k (by omega)]
      congr 1
      omega

/-- An earless proper cycle has even length. -/
theorem even_of_no_ear {n : ℕ} {c : ℕ → Color} (hper : Periodic n c) (hp : CycleProper c)
    (h : ∀ i, ¬ Ear c i) : Even n := by
  by_contra hodd
  have h1 : n % 2 = 1 := Nat.odd_iff.mp (Nat.not_even_iff_odd.mp hodd)
  have := two_periodic_of_no_ear h n
  have h0 : c n = c 0 := by simpa using hper 0
  rw [h1, h0] at this
  exact hp 0 this

/-- An earless proper cycle uses exactly the two colours `c 0`, `c 1`. -/
theorem uses_two_colors_of_no_ear {c : ℕ → Color} (h : ∀ i, ¬ Ear c i) (i : ℕ) :
    c i = c 0 ∨ c i = c 1 := by
  rw [two_periodic_of_no_ear h i]
  rcases Nat.mod_two_eq_zero_or_one i with h0 | h1
  · rw [h0]; exact Or.inl rfl
  · rw [h1]; exact Or.inr rfl

theorem exists_third_color : ∀ a b : Color, ∃ h : Color, h ≠ a ∧ h ≠ b := by decide

/-- A hub colour unused on the cycle exists, and every cone triangle is proper. -/
theorem exists_hub_of_no_ear {c : ℕ → Color} (hp : CycleProper c) (h : ∀ i, ¬ Ear c i) :
    ∃ hub : Color, ∀ i, c i ≠ hub ∧ c (i + 1) ≠ hub ∧ c i ≠ c (i + 1) := by
  obtain ⟨hub, ha, hb⟩ := exists_third_color (c 0) (c 1)
  refine ⟨hub, fun i => ⟨?_, ?_, hp i⟩⟩
  · rcases uses_two_colors_of_no_ear h i with e | e <;> rw [e] <;> exact Ne.symm ‹_›
  · rcases uses_two_colors_of_no_ear h (i + 1) with e | e <;> rw [e] <;> exact Ne.symm ‹_›

/-- The dichotomy driving the completion loop (`fill_polygon` in
`scripts/c5_count_cone_bridge.py`): clip an ear, or cone an even alternating polygon. -/
theorem ear_or_hub {n : ℕ} {c : ℕ → Color} (hper : Periodic n c) (hp : CycleProper c) :
    (∃ i, Ear c i) ∨ (Even n ∧ ∃ hub : Color, ∀ i, c i ≠ hub ∧ c (i + 1) ≠ hub) := by
  by_cases h : ∃ i, Ear c i
  · exact Or.inl h
  · have h' : ∀ i, ¬ Ear c i := fun i hi => h ⟨i, hi⟩
    obtain ⟨hub, hhub⟩ := exists_hub_of_no_ear hp h'
    exact Or.inr ⟨even_of_no_ear hper hp h', hub, fun i => ⟨(hhub i).1, (hhub i).2.1⟩⟩

/-! ### Euler count for a near-triangulation with outer face C5 -/

/-- With `k` interior vertices, `t` triangular inner faces and `E` edges: every triangle has
three sides, each boundary edge lies on one triangle and each other edge on two, and Euler's
formula holds. Then `t = 2k+3`, `E = 3(k+5) - 8`, and the dual has `2k+4` vertices. -/
theorem counts (k t E : ℕ) (hsides : 3 * t = 2 * E - 5) (h5 : 5 ≤ E)
    (heuler : (k + 5 : ℤ) - E + (t + 1) = 2) :
    t = 2 * k + 3 ∧ E = 3 * (k + 5) - 8 ∧ t + 1 = 2 * k + 4 := by
  omega

/-- The cited Corollary 20 covers dual graphs with fewer than 30 vertices, i.e. `k ≤ 12`. -/
theorem corollary20_range (k : ℕ) : 2 * k + 4 < 30 ↔ k ≤ 12 := by omega

end FiveBoundary.NearTriangulation
