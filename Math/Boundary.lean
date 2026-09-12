/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Mathlib

/-! Finite, labelled five-boundary semantics. No planarity or four-colour theorem axiom. -/
namespace FiveBoundary

abbrev Color := Fin 4
abbrev BoundaryAssignment (k : ℕ) := Fin k → Color
abbrev BoundaryColoring := BoundaryAssignment 5

def C5 : SimpleGraph (Fin 5) where
  Adj i j := j = i + 1 ∨ i = j + 1
  symm := ⟨by intro i j h; exact h.elim Or.inr Or.inl⟩
  loopless := ⟨by intro i h; fin_cases i <;> simp_all⟩

instance : DecidableRel C5.Adj := fun _ _ => inferInstanceAs
  (Decidable (_ = _ + (1 : Fin 5) ∨ _ = _ + (1 : Fin 5)))

def Proper {n : ℕ} (G : SimpleGraph (Fin n)) (c : Fin n → Color) : Prop :=
  ∀ i j, G.Adj i j → c i ≠ c j

instance {n : ℕ} (G : SimpleGraph (Fin n)) [DecidableRel G.Adj]
    (c : Fin n → Color) : Decidable (Proper G c) :=
  inferInstanceAs (Decidable (∀ i j, G.Adj i j → c i ≠ c j))

def usedColors {n : ℕ} (c : Fin n → Color) : Finset Color := Finset.univ.image c

abbrev Col4 {n : ℕ} (G : SimpleGraph (Fin n)) := {c : Fin n → Color // Proper G c}

def restrictionMap {n k : ℕ} (G : SimpleGraph (Fin n)) (B : Fin k ↪ Fin n) :
    Col4 G → BoundaryAssignment k := fun c => c.val ∘ B

def SigmaAt {n k : ℕ} (G : SimpleGraph (Fin n)) (B : Fin k ↪ Fin n) :
    Set (BoundaryAssignment k) := Set.range (restrictionMap G B)

def colorAction (p : Equiv.Perm Color) (c : BoundaryColoring) : BoundaryColoring := p ∘ c

theorem colorAction_one (c : BoundaryColoring) : colorAction 1 c = c := rfl
theorem colorAction_mul (p q : Equiv.Perm Color) (c : BoundaryColoring) :
    colorAction (p * q) c = colorAction p (colorAction q c) := rfl

def dihedralSubgroup : Subgroup (Equiv.Perm (Fin 5)) where
  carrier := {p | ∀ i j, C5.Adj (p i) (p j) ↔ C5.Adj i j}
  one_mem' := by intro i j; rfl
  mul_mem' := by intro p q hp hq i j; exact (hp (q i) (q j)).trans (hq i j)
  inv_mem' := by
    intro p hp i j
    have h := hp (p.symm i) (p.symm j)
    simpa using h.symm

abbrev D5 := dihedralSubgroup

instance (p : Equiv.Perm (Fin 5)) : Decidable (p ∈ dihedralSubgroup) :=
  inferInstanceAs (Decidable (∀ i j, C5.Adj (p i) (p j) ↔ C5.Adj i j))
instance : Fintype D5 := Subtype.fintype _

def dihedralAction (p : D5) (c : BoundaryColoring) : BoundaryColoring := c ∘ p.val.symm

theorem dihedralAction_one (c : BoundaryColoring) : dihedralAction 1 c = c := rfl
theorem dihedralAction_mul (p q : D5) (c : BoundaryColoring) :
    dihedralAction (p * q) c = dihedralAction p (dihedralAction q c) := rfl

theorem actions_commute (p : Equiv.Perm Color) (d : D5) (c : BoundaryColoring) :
    colorAction p (dihedralAction d c) = dihedralAction d (colorAction p c) := rfl

theorem colorAction_proper (p : Equiv.Perm Color) {c : BoundaryColoring}
    (h : Proper C5 c) : Proper C5 (colorAction p c) := by
  intro i j e eq
  exact h i j e (p.injective eq)

theorem dihedralAction_proper (p : D5) {c : BoundaryColoring}
    (h : Proper C5 c) : Proper C5 (dihedralAction p c) := by
  intro i j e
  apply h
  exact (dihedralSubgroup.inv_mem p.property i j).mpr e

def boundaryColoring {n : ℕ} (B : Fin 5 ↪ Fin n) (c : Fin n → Color) :
    BoundaryColoring := c ∘ B

def Sigma {n : ℕ} (G : SimpleGraph (Fin n)) (B : Fin 5 ↪ Fin n) :
    Set BoundaryColoring := {b | ∃ c, Proper G c ∧ boundaryColoring B c = b}

instance {n : ℕ} (G : SimpleGraph (Fin n)) [DecidableRel G.Adj]
    (B : Fin 5 ↪ Fin n) (b : BoundaryColoring) : Decidable (b ∈ Sigma G B) :=
  inferInstanceAs (Decidable (∃ c, Proper G c ∧ boundaryColoring B c = b))

theorem sigma_is_image {n : ℕ} (G : SimpleGraph (Fin n)) (B : Fin 5 ↪ Fin n) :
    Sigma G B = SigmaAt G B := by
  ext b
  constructor
  · rintro ⟨c,hc,hb⟩; exact ⟨⟨c,hc⟩,hb⟩
  · rintro ⟨⟨c,hc⟩,hb⟩; exact ⟨c,hc,hb⟩

def GOOD {n : ℕ} (G : SimpleGraph (Fin n)) (B : Fin 5 ↪ Fin n) : Prop :=
  ∃ b ∈ Sigma G B, (usedColors b).card ≤ 3

def BAD {n : ℕ} (G : SimpleGraph (Fin n)) (B : Fin 5 ↪ Fin n) : Prop :=
  (Sigma G B).Nonempty ∧ ¬ GOOD G B

instance {n : ℕ} (G : SimpleGraph (Fin n)) [DecidableRel G.Adj]
    (B : Fin 5 ↪ Fin n) : Decidable (GOOD G B) :=
  inferInstanceAs (Decidable (∃ b ∈ Sigma G B, (usedColors b).card ≤ 3))

instance {n : ℕ} (G : SimpleGraph (Fin n)) [DecidableRel G.Adj]
    (B : Fin 5 ↪ Fin n) : Decidable (BAD G B) :=
  inferInstanceAs (Decidable ((∃ b, b ∈ Sigma G B) ∧ ¬ GOOD G B))

def sigmaFinite {n : ℕ} (G : SimpleGraph (Fin n)) [DecidableRel G.Adj]
    (B : Fin 5 ↪ Fin n) : Finset BoundaryColoring :=
  (Finset.univ.filter (Proper G)).image (boundaryColoring B)

theorem mem_sigmaFinite {n : ℕ} (G : SimpleGraph (Fin n)) [DecidableRel G.Adj]
    (B : Fin 5 ↪ Fin n) (b : BoundaryColoring) : b ∈ sigmaFinite G B ↔ b ∈ Sigma G B := by
  simp [sigmaFinite, Sigma]

theorem sigma_color_invariant {n : ℕ} (G : SimpleGraph (Fin n))
    (B : Fin 5 ↪ Fin n) (p : Equiv.Perm Color) {b : BoundaryColoring}
    (hb : b ∈ Sigma G B) : colorAction p b ∈ Sigma G B := by
  obtain ⟨c, hc, rfl⟩ := hb
  refine ⟨p ∘ c, ?_, rfl⟩
  intro i j e eq
  exact hc i j e (p.injective eq)

/-- Input edges are checked separately for ordering, loops and duplicates. -/
def graphOfEdges {n : ℕ} (edges : List (Fin n × Fin n)) : SimpleGraph (Fin n) where
  Adj u v := u ≠ v ∧ ((u,v) ∈ edges ∨ (v,u) ∈ edges)
  symm := ⟨by intro u v h; exact ⟨Ne.symm h.1, h.2.symm⟩⟩
  loopless := ⟨by intro u h; exact h.1 rfl⟩

instance {n : ℕ} (edges : List (Fin n × Fin n)) : DecidableRel (graphOfEdges edges).Adj :=
  fun _ _ => inferInstanceAs (Decidable (_ ≠ _ ∧ (_ ∈ edges ∨ _ ∈ edges)))

def firstBoundary {n : ℕ} (h : 5 ≤ n) : Fin 5 ↪ Fin n :=
  ⟨Fin.castLE h, Fin.castLE_injective h⟩

def boundaryIsCycle {n : ℕ} (G : SimpleGraph (Fin n)) (B : Fin 5 ↪ Fin n) : Prop :=
  ∀ i j, C5.Adj i j → G.Adj (B i) (B j)

instance {n : ℕ} (G : SimpleGraph (Fin n)) [DecidableRel G.Adj]
    (B : Fin 5 ↪ Fin n) : Decidable (boundaryIsCycle G B) :=
  inferInstanceAs (Decidable (∀ i j, C5.Adj i j → G.Adj (B i) (B j)))

theorem restrict_proper {n : ℕ} {G : SimpleGraph (Fin n)} {B : Fin 5 ↪ Fin n}
    (hB : boundaryIsCycle G B) {c : Fin n → Color} (hc : Proper G c) :
    Proper C5 (boundaryColoring B c) := by
  intro i j h
  exact hc (B i) (B j) (hB i j h)

/-- Composition of exact, aligned boundary relations. -/
def compose (s t : Set BoundaryColoring) : Set BoundaryColoring := s ∩ t

theorem sigma_union_same_vertices {n : ℕ} (G H : SimpleGraph (Fin n))
    (c : Fin n → Color) : Proper (G ⊔ H) c ↔ Proper G c ∧ Proper H c := by
  constructor
  · intro h; exact ⟨fun i j e => h i j (Or.inl e), fun i j e => h i j (Or.inr e)⟩
  · rintro ⟨hg, hh⟩ i j (e | e)
    · exact hg i j e
    · exact hh i j e

end FiveBoundary
