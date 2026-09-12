/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.HallTriangle

/-! # Geometry → Hall witness layer

A three-colour boundary pattern has a fixed shape: one vertex `u` carries a colour used once,
`u+1, u+3` share a colour and `u+2, u+4` share the third. The Hall witnesses of
`reject_iff_hall` only ask which boundary colours each interior vertex has seen, so they are
statements about the attachment sets `linksOf w k` hitting `{u}`, `{u+1,u+3}`, `{u+2,u+4}`.
`GeoReject w u` is that colour-free predicate; `reject_iff_geometry` proves it is exactly
rejection, and `threeProfile_eq_geo` rewrites the Z5 profile in these terms. Plain proofs. -/

namespace FiveBoundary.Hall
open ColorDFA GeometryDFA Finset

/-- Interior vertex `k` is attached to the unique-colour vertex `u`. -/
def HitsUnique (w : Word) (u : Fin 5) (k : Fin 3) : Prop := u ∈ linksOf w k

/-- `k` is attached to `u+1` or `u+3` (one colour class of the pattern). -/
def HitsOdd (w : Word) (u : Fin 5) (k : Fin 3) : Prop :=
  u + 1 ∈ linksOf w k ∨ u + 3 ∈ linksOf w k

/-- `k` is attached to `u+2` or `u+4` (the other colour class). -/
def HitsEven (w : Word) (u : Fin 5) (k : Fin 3) : Prop :=
  u + 2 ∈ linksOf w k ∨ u + 4 ∈ linksOf w k

/-- `k` sees all three boundary colours of the pattern with unique vertex `u`. -/
def SeesAll (w : Word) (u : Fin 5) (k : Fin 3) : Prop :=
  HitsUnique w u k ∧ HitsOdd w u k ∧ HitsEven w u k

/-- Colour-free rejection: two interior vertices see everything (witness A), or every interior
vertex sees the same two of the three colour classes (witness B, three choices of the
missing class). -/
def GeoReject (w : Word) (u : Fin 5) : Prop :=
  (∃ k k', k ≠ k' ∧ SeesAll w u k ∧ SeesAll w u k') ∨
  (∀ k, HitsOdd w u k ∧ HitsEven w u k) ∨
  (∀ k, HitsUnique w u k ∧ HitsEven w u k) ∨
  (∀ k, HitsUnique w u k ∧ HitsOdd w u k)

instance (w : Word) (u : Fin 5) (k : Fin 3) : Decidable (HitsUnique w u k) :=
  inferInstanceAs (Decidable (_ ∈ _))
instance (w : Word) (u : Fin 5) (k : Fin 3) : Decidable (HitsOdd w u k) :=
  inferInstanceAs (Decidable (_ ∨ _))
instance (w : Word) (u : Fin 5) (k : Fin 3) : Decidable (HitsEven w u k) :=
  inferInstanceAs (Decidable (_ ∨ _))
instance (w : Word) (u : Fin 5) (k : Fin 3) : Decidable (SeesAll w u k) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _))
instance (w : Word) (u : Fin 5) : Decidable (GeoReject w u) :=
  inferInstanceAs (Decidable (_ ∨ _ ∨ _ ∨ _))

/-! ### Finite facts about `Fin 5` positions and `Fin 4` colours -/

theorem fin5_cover (j u : Fin 5) : j = u ∨ j = u + 1 ∨ j = u + 2 ∨ j = u + 3 ∨ j = u + 4 := by
  revert j u; decide

theorem exists_fourth (c₀ x y : Color) (hxy : x ≠ y) (hx : x ≠ c₀) (hy : y ≠ c₀) :
    ∃ d, d ≠ c₀ ∧ d ≠ x ∧ d ≠ y := by
  revert c₀ x y; decide

theorem colour_cover (c d c₀ x y : Color) (hxy : x ≠ y) (hx : x ≠ c₀) (hy : y ≠ c₀)
    (hd0 : d ≠ c₀) (hdx : d ≠ x) (hdy : d ≠ y) (hc : c ≠ d) : c = c₀ ∨ c = x ∨ c = y := by
  revert c d c₀ x y; decide

/-! ### The pattern shape -/

/-- The shape of a three-colour proper pattern with unique vertex `u`. -/
structure Shape (b : BoundaryColoring) (u : Fin 5) (c₀ x y : Color) : Prop where
  h0 : b u = c₀
  h1 : b (u + 1) = x
  h2 : b (u + 2) = y
  h3 : b (u + 3) = x
  h4 : b (u + 4) = y
  hxy : x ≠ y
  hx : x ≠ c₀
  hy : y ≠ c₀

variable {w : Word} {b : BoundaryColoring} {u : Fin 5} {c₀ x y : Color}

theorem Shape.value (s : Shape b u c₀ x y) (j : Fin 5) : b j = c₀ ∨ b j = x ∨ b j = y := by
  rcases fin5_cover j u with rfl | rfl | rfl | rfl | rfl
  · exact Or.inl s.h0
  · exact Or.inr (Or.inl s.h1)
  · exact Or.inr (Or.inr s.h2)
  · exact Or.inr (Or.inl s.h3)
  · exact Or.inr (Or.inr s.h4)

theorem mem_run_iff (w : Word) (b : BoundaryColoring) (k : Fin 3) (c : Color) :
    c ∈ run w b k ↔ ∃ j ∈ linksOf w k, b j = c := by
  rw [run_spec, mem_image]

theorem Shape.sees_unique (s : Shape b u c₀ x y) (k : Fin 3) :
    c₀ ∈ run w b k ↔ HitsUnique w u k := by
  rw [mem_run_iff, HitsUnique]
  constructor
  · rintro ⟨j, hj, hbj⟩
    rcases fin5_cover j u with rfl | rfl | rfl | rfl | rfl
    · exact hj
    · exact absurd (s.h1 ▸ hbj) s.hx
    · exact absurd (s.h2 ▸ hbj) s.hy
    · exact absurd (s.h3 ▸ hbj) s.hx
    · exact absurd (s.h4 ▸ hbj) s.hy
  · intro h; exact ⟨u, h, s.h0⟩

theorem Shape.sees_x (s : Shape b u c₀ x y) (k : Fin 3) :
    x ∈ run w b k ↔ HitsOdd w u k := by
  rw [mem_run_iff, HitsOdd]
  constructor
  · rintro ⟨j, hj, hbj⟩
    rcases fin5_cover j u with rfl | rfl | rfl | rfl | rfl
    · exact absurd (s.h0 ▸ hbj) s.hx.symm
    · exact Or.inl hj
    · exact absurd (s.h2 ▸ hbj) s.hxy.symm
    · exact Or.inr hj
    · exact absurd (s.h4 ▸ hbj) s.hxy.symm
  · rintro (h | h)
    · exact ⟨u + 1, h, s.h1⟩
    · exact ⟨u + 3, h, s.h3⟩

theorem Shape.sees_y (s : Shape b u c₀ x y) (k : Fin 3) :
    y ∈ run w b k ↔ HitsEven w u k := by
  rw [mem_run_iff, HitsEven]
  constructor
  · rintro ⟨j, hj, hbj⟩
    rcases fin5_cover j u with rfl | rfl | rfl | rfl | rfl
    · exact absurd (s.h0 ▸ hbj) s.hy.symm
    · exact absurd (s.h1 ▸ hbj) s.hxy
    · exact Or.inl hj
    · exact absurd (s.h3 ▸ hbj) s.hxy
    · exact Or.inr hj
  · rintro (h | h)
    · exact ⟨u + 2, h, s.h2⟩
    · exact ⟨u + 4, h, s.h4⟩

theorem Shape.not_used (s : Shape b u c₀ x y) {d : Color} (hd0 : d ≠ c₀) (hdx : d ≠ x)
    (hdy : d ≠ y) : d ∉ usedColors b := by
  simp only [usedColors, mem_image, mem_univ, true_and, not_exists]
  intro j hj
  rcases s.value j with h | h | h
  · exact hd0 (by rw [← hj, h])
  · exact hdx (by rw [← hj, h])
  · exact hdy (by rw [← hj, h])

/-! ### The bridge -/

/-- **Geometry → Hall witness.** For any boundary pattern of the three-colour shape with unique
vertex `u`, rejection by the compiled triangle gadget is the colour-free predicate `GeoReject`. -/
theorem reject_iff_geometry (s : Shape b u c₀ x y) : ¬ Accept (run w b) ↔ GeoReject w u := by
  obtain ⟨d, hd0, hdx, hdy⟩ := exists_fourth c₀ x y s.hxy s.hx s.hy
  have hd : d ∉ usedColors b := s.not_used hd0 hdx hdy
  have hdrun : ∀ k, d ∉ run w b k := fun k h => by
    obtain ⟨j, _, hj⟩ := (mem_run_iff w b k d).mp h
    exact hd (mem_image.mpr ⟨j, mem_univ _, hj⟩)
  have cover := fun c hc => colour_cover c d c₀ x y s.hxy s.hx s.hy hd0 hdx hdy hc
  -- witness A: pinned ⇔ sees all
  have hA : ∀ k, availOf w b k = {d} ↔ SeesAll w u k := by
    intro k
    rw [pinned_iff_sees_all w b k (hdrun k), SeesAll, ← s.sees_unique, ← s.sees_x, ← s.sees_y]
    constructor
    · intro h; exact ⟨h c₀ hd0.symm, h x hdx.symm, h y hdy.symm⟩
    · rintro ⟨h0, hx', hy'⟩ c hc
      rcases cover c hc with rfl | rfl | rfl <;> assumption
  -- witness B: restricted to `{d, x'}` ⇔ everyone sees the two other colours
  have hB : ∀ x', x' ≠ d → ((∀ k, availOf w b k ⊆ {d, x'}) ↔
      ((x' = c₀ ∧ ∀ k, HitsOdd w u k ∧ HitsEven w u k) ∨
       (x' = x ∧ ∀ k, HitsUnique w u k ∧ HitsEven w u k) ∨
       (x' = y ∧ ∀ k, HitsUnique w u k ∧ HitsOdd w u k))) := by
    intro x' hx'
    rw [restricted_iff_sees_two]
    rcases cover x' hx' with rfl | rfl | rfl
    · constructor
      · intro h
        exact Or.inl ⟨rfl, fun k =>
          ⟨(s.sees_x k).mp (h k x hdx.symm s.hx), (s.sees_y k).mp (h k y hdy.symm s.hy)⟩⟩
      · rintro (⟨_, h⟩ | ⟨hxx, _⟩ | ⟨hyy, _⟩)
        · intro k c hc hc'
          rcases cover c hc with rfl | rfl | rfl
          · exact absurd rfl hc'
          · exact (s.sees_x k).mpr (h k).1
          · exact (s.sees_y k).mpr (h k).2
        · exact absurd hxx s.hx.symm
        · exact absurd hyy s.hy.symm
    · constructor
      · intro h
        exact Or.inr (Or.inl ⟨rfl, fun k =>
          ⟨(s.sees_unique k).mp (h k c₀ hd0.symm s.hx.symm),
            (s.sees_y k).mp (h k y hdy.symm s.hxy.symm)⟩⟩)
      · rintro (⟨hxx, _⟩ | ⟨_, h⟩ | ⟨hyy, _⟩)
        · exact absurd hxx s.hx
        · intro k c hc hc'
          rcases cover c hc with rfl | rfl | rfl
          · exact (s.sees_unique k).mpr (h k).1
          · exact absurd rfl hc'
          · exact (s.sees_y k).mpr (h k).2
        · exact absurd hyy s.hxy
    · constructor
      · intro h
        exact Or.inr (Or.inr ⟨rfl, fun k =>
          ⟨(s.sees_unique k).mp (h k c₀ hd0.symm s.hy.symm),
            (s.sees_x k).mp (h k x hdx.symm s.hxy)⟩⟩)
      · rintro (⟨hxx, _⟩ | ⟨hyy, _⟩ | ⟨_, h⟩)
        · exact absurd hxx s.hy
        · exact absurd hyy s.hxy.symm
        · intro k c hc hc'
          rcases cover c hc with rfl | rfl | rfl
          · exact (s.sees_unique k).mpr (h k).1
          · exact (s.sees_x k).mpr (h k).2
          · exact absurd rfl hc'
  rw [reject_iff_hall w b hd, GeoReject, PairPinnedToFourth, TripleRestrictedToTwo]
  simp only [hA]
  constructor
  · rintro (⟨k, k', hne, h1, h2⟩ | ⟨x', hx', h⟩)
    · exact Or.inl ⟨k, k', hne, h1, h2⟩
    · rcases (hB x' hx').mp h with ⟨_, h⟩ | ⟨_, h⟩ | ⟨_, h⟩
      · exact Or.inr (Or.inl h)
      · exact Or.inr (Or.inr (Or.inl h))
      · exact Or.inr (Or.inr (Or.inr h))
  · rintro (⟨k, k', hne, h1, h2⟩ | h | h | h)
    · exact Or.inl ⟨k, k', hne, h1, h2⟩
    · exact Or.inr ⟨c₀, hd0.symm, (hB c₀ hd0.symm).mpr (Or.inl ⟨rfl, h⟩)⟩
    · exact Or.inr ⟨x, hdx.symm, (hB x hdx.symm).mpr (Or.inr (Or.inl ⟨rfl, h⟩))⟩
    · exact Or.inr ⟨y, hdy.symm, (hB y hdy.symm).mpr (Or.inr (Or.inr ⟨rfl, h⟩))⟩

/-! ### The Z5 profile is colour-free -/

/-- The three-colour representative with unique vertex `u` (`threeReps` re-indexed by
`uniquePosition`). -/
def repAt : Fin 5 → BoundaryColoring :=
  ![![0,1,2,1,2], ![0,1,2,0,2], ![0,1,2,0,1], ![0,1,0,2,1], ![0,1,0,1,2]]

theorem repAt_mem (u : Fin 5) : repAt u ∈ threeReps ∧ uniquePosition (repAt u) = some u := by
  revert u; decide

set_option maxRecDepth 100000 in
theorem eq_repAt_of_position : ∀ b ∈ threeReps, ∀ u, uniquePosition b = some u → b = repAt u := by
  decide

theorem repAt_shape (u : Fin 5) : ∃ c₀ x y, Shape (repAt u) u c₀ x y := by
  fin_cases u
  · exact ⟨0, 1, 2, by constructor <;> decide⟩
  · exact ⟨1, 2, 0, by constructor <;> decide⟩
  · exact ⟨2, 0, 1, by constructor <;> decide⟩
  · exact ⟨2, 1, 0, by constructor <;> decide⟩
  · exact ⟨2, 0, 1, by constructor <;> decide⟩

theorem mem_threeProfile_iff (w : Word) (u : Fin 5) :
    u ∈ threeProfile w ↔ Accept (run w (repAt u)) := by
  simp only [threeProfile, List.mem_toFinset, List.mem_filterMap, List.mem_filter]
  constructor
  · rintro ⟨b, ⟨hb, hacc⟩, hpos⟩
    rw [eq_repAt_of_position b hb u hpos] at hacc
    exact (acceptB_iff _).mp hacc
  · intro h
    exact ⟨repAt u, ⟨(repAt_mem u).1, (acceptB_iff _).mpr h⟩, (repAt_mem u).2⟩

/-- **The Z5 profile without colours.** `u` is accepted iff `GeoReject w u` fails. -/
theorem threeProfile_eq_geo (w : Word) :
    threeProfile w = univ.filter (fun u => ¬ GeoReject w u) := by
  ext u
  rw [mem_filter, mem_threeProfile_iff]
  obtain ⟨c₀, x, y, s⟩ := repAt_shape u
  rw [← reject_iff_geometry s, not_not]
  simp

end FiveBoundary.Hall
