/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.Enumeration

/-! Exact raw and colour-saturated states, with aligned relational composition. -/

namespace FiveBoundary

/-- A raw state has one Boolean for every labelled proper boundary colouring. -/
abbrev RawIndex := {b : BoundaryColoring // b ∈ properBoundary}
abbrev RawState := RawIndex → Bool

theorem raw_index_count : Fintype.card RawIndex = 240 := by
  simpa using c5_count

def rawEncode (s : Finset BoundaryColoring) : RawState := fun b => decide (b.val ∈ s)

theorem raw_intersection (s t : Finset BoundaryColoring) (b : RawIndex) :
    rawEncode (s ∩ t) b = (rawEncode s b && rawEncode t b) := by
  simp [rawEncode]

def T3 : Set BoundaryColoring := {b | Proper C5 b ∧ (usedColors b).card ≤ 3}

theorem good_iff_intersects_T3 {n : ℕ} (G : SimpleGraph (Fin n)) (B : Fin 5 ↪ Fin n)
    (hB : boundaryIsCycle G B) : GOOD G B ↔ (Sigma G B ∩ T3).Nonempty := by
  constructor
  · rintro ⟨b,hb,hc⟩
    refine ⟨b,hb,?_,hc⟩
    obtain ⟨c,hcol,rfl⟩ := hb
    exact restrict_proper hB hcol
  · rintro ⟨b,hb,_,hc⟩; exact ⟨b,hb,hc⟩

theorem bad_iff_avoids_T3 {n : ℕ} (G : SimpleGraph (Fin n)) (B : Fin 5 ↪ Fin n)
    (hB : boundaryIsCycle G B) :
    BAD G B ↔ (Sigma G B).Nonempty ∧ ¬ (Sigma G B ∩ T3).Nonempty := by
  rw [BAD, good_iff_intersects_T3 G B hB]

def Saturated (s : Finset BoundaryColoring) : Prop :=
  ∀ p : Equiv.Perm Color, ∀ b ∈ s, colorAction p b ∈ s

def abstractColors (s : Finset BoundaryColoring) : Finset BoundaryColoring :=
  colorReps.filter (· ∈ s)

def decodeColors (s : Finset BoundaryColoring) : Finset BoundaryColoring :=
  s.biUnion colorOrbit

theorem color_abstraction_exact (s : Finset BoundaryColoring)
    (valid : s ⊆ properBoundary) (sat : Saturated s) :
    decodeColors (abstractColors s) = s := by
  ext b
  simp only [decodeColors, Finset.mem_biUnion, abstractColors, Finset.mem_filter]
  constructor
  · rintro ⟨r, ⟨_, hr⟩, hb⟩
    obtain ⟨p, _, rfl⟩ := Finset.mem_image.mp hb
    exact sat p r hr
  · intro hb
    have hcov : b ∈ colorReps.biUnion colorOrbit := by
      rw [color_orbits_cover]
      exact valid hb
    obtain ⟨r, hr, hp⟩ := Finset.mem_biUnion.mp hcov
    obtain ⟨p, _, heq⟩ := Finset.mem_image.mp hp
    refine ⟨r, ⟨hr, ?_⟩, ?_⟩
    · have h := sat p.symm b hb
      rw [← heq] at h
      simpa [colorAction, Function.comp_def] using h
    · exact Finset.mem_image.mpr ⟨p, Finset.mem_univ _, heq⟩

theorem abstract_intersection (s t : Finset BoundaryColoring) :
    abstractColors (s ∩ t) = abstractColors s ∩ abstractColors t := by
  ext b
  simp [abstractColors, and_assoc, and_left_comm, and_comm]

theorem sigma_saturated {n : ℕ} (G : SimpleGraph (Fin n)) [DecidableRel G.Adj]
    (B : Fin 5 ↪ Fin n) : Saturated (sigmaFinite G B) := by
  intro p b hb
  exact (mem_sigmaFinite _ _ _).mpr
    (sigma_color_invariant G B p ((mem_sigmaFinite _ _ _).mp hb))

theorem sigma_valid {n : ℕ} (G : SimpleGraph (Fin n)) [DecidableRel G.Adj]
    (B : Fin 5 ↪ Fin n) (hB : boundaryIsCycle G B) : sigmaFinite G B ⊆ properBoundary := by
  intro b hb
  obtain ⟨c, hc, rfl⟩ := (mem_sigmaFinite _ _ _).mp hb
  exact Finset.mem_filter.mpr ⟨Finset.mem_univ _, restrict_proper hB hc⟩

abbrev ColorState := Finset {b : BoundaryColoring // b ∈ colorReps}

theorem color_state_count : Fintype.card ColorState = 1024 := by
  simp [ColorState, Fintype.card_finset, color_reps_count]

/-- Independent interiors share exactly the labelled boundary: relational gluing law. -/
theorem independent_gluing {X Y : Type} (P : BoundaryColoring → X → Prop)
    (Q : BoundaryColoring → Y → Prop) :
    {b | ∃ xy : X × Y, P b xy.1 ∧ Q b xy.2} =
    {b | ∃ x, P b x} ∩ {b | ∃ y, Q b y} := by
  ext b
  constructor
  · rintro ⟨⟨x,y⟩, hp, hq⟩; exact ⟨⟨x,hp⟩,⟨y,hq⟩⟩
  · rintro ⟨⟨x,hp⟩,⟨y,hq⟩⟩; exact ⟨⟨x,y⟩,hp,hq⟩

/-- Adding a component by intersection cannot introduce a new three-colour option. -/
theorem intersection_cannot_repair (s t : Finset BoundaryColoring)
    (h : ∀ b ∈ s, (usedColors b).card > 3) :
    ∀ b ∈ s ∩ t, (usedColors b).card > 3 := by
  intro b hb
  exact h b (Finset.mem_inter.mp hb).1

def IntersectionStep (allowed : Set (Finset BoundaryColoring))
    (s t : Finset BoundaryColoring) : Prop := ∃ p ∈ allowed, t = s ∩ p

theorem intersection_step_decreases {allowed : Set (Finset BoundaryColoring)}
    {s t : Finset BoundaryColoring} (h : IntersectionStep allowed s t) : t ⊆ s := by
  obtain ⟨p,_,rfl⟩ := h
  exact Finset.inter_subset_left

theorem intersection_reachable_decreases {allowed : Set (Finset BoundaryColoring)}
    {s t : Finset BoundaryColoring}
    (h : Relation.ReflTransGen (IntersectionStep allowed) s t) : t ⊆ s := by
  induction h with
  | refl => exact Finset.Subset.refl _
  | tail _ hstep ih => exact (intersection_step_decreases hstep).trans ih

/-- For intersection-only transitions, an SCC cannot contain distinct exact states. -/
theorem intersection_scc_singleton {allowed : Set (Finset BoundaryColoring)}
    {s t : Finset BoundaryColoring}
    (hst : Relation.ReflTransGen (IntersectionStep allowed) s t)
    (hts : Relation.ReflTransGen (IntersectionStep allowed) t s) : s = t := by
  exact Finset.Subset.antisymm (intersection_reachable_decreases hts)
    (intersection_reachable_decreases hst)

end FiveBoundary
