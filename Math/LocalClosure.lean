/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.BoundaryRelations

/-! Separator semantics for sealing a region. No disk-embedding assertion. -/
namespace FiveBoundary.LocalClosure

/-- A processed region has boundary B and private vertices I. -/
def RegionOK {B I : Type} (g : SimpleGraph (B ⊕ I))
    (b : B → Color) (x : I → Color) : Prop :=
  ∀ u v, g.Adj u v → Sum.elim b x u ≠ Sum.elim b x v

def Summary {B I : Type} (g : SimpleGraph (B ⊕ I)) (b : B → Color) : Prop :=
  ∃ x, RegionOK g b x

/-- Actual union on B + (I + J); private interiors are disjoint and have no cross edges. -/
def GlueAdj {B I J : Type} (g : SimpleGraph (B ⊕ I))
    (h : SimpleGraph (B ⊕ J)) : (B ⊕ (I ⊕ J)) → (B ⊕ (I ⊕ J)) → Prop
  | .inl u, .inl v => g.Adj (.inl u) (.inl v) ∨ h.Adj (.inl u) (.inl v)
  | .inl u, .inr (.inl v) => g.Adj (.inl u) (.inr v)
  | .inr (.inl u), .inl v => g.Adj (.inr u) (.inl v)
  | .inl u, .inr (.inr v) => h.Adj (.inl u) (.inr v)
  | .inr (.inr u), .inl v => h.Adj (.inr u) (.inl v)
  | .inr (.inl u), .inr (.inl v) => g.Adj (.inr u) (.inr v)
  | .inr (.inr u), .inr (.inr v) => h.Adj (.inr u) (.inr v)
  | _, _ => False

def glue {B I J : Type} (g : SimpleGraph (B ⊕ I))
    (h : SimpleGraph (B ⊕ J)) : SimpleGraph (B ⊕ (I ⊕ J)) where
  Adj := GlueAdj g h
  symm := ⟨by
    intro u v
    rcases u with u | (u | u) <;> rcases v with v | (v | v) <;>
      simp only [GlueAdj] <;> aesop (add safe apply SimpleGraph.Adj.symm)⟩
  loopless := ⟨by
    intro u
    rcases u with u | (u | u) <;> simp [GlueAdj]⟩

theorem regionOK_glue {B I J : Type} (g : SimpleGraph (B ⊕ I))
    (h : SimpleGraph (B ⊕ J)) (b : B → Color) (x : I → Color) (y : J → Color) :
    RegionOK (glue g h) b (Sum.elim x y) ↔ RegionOK g b x ∧ RegionOK h b y := by
  constructor
  · intro hp
    constructor
    · intro u v e
      rcases u with u | u <;> rcases v with v | v
      · exact hp (.inl u) (.inl v) (Or.inl e)
      · exact hp (.inl u) (.inr (.inl v)) e
      · exact hp (.inr (.inl u)) (.inl v) e
      · exact hp (.inr (.inl u)) (.inr (.inl v)) e
    · intro u v e
      rcases u with u | u <;> rcases v with v | v
      · exact hp (.inl u) (.inl v) (Or.inr e)
      · exact hp (.inl u) (.inr (.inr v)) e
      · exact hp (.inr (.inr u)) (.inl v) e
      · exact hp (.inr (.inr u)) (.inr (.inr v)) e
  · rintro ⟨hg, hh⟩ u v e
    rcases u with u | (u | u) <;> rcases v with v | (v | v)
    · exact e.elim (hg _ _) (hh _ _)
    · exact hg _ _ e
    · exact hh _ _ e
    · exact hg _ _ e
    · exact hg _ _ e
    · exact False.elim e
    · exact hh _ _ e
    · exact False.elim e
    · exact hh _ _ e

/-- Graph-level separator theorem, rather than a relation-algebra definition. -/
theorem summary_glue {B I J : Type} (g : SimpleGraph (B ⊕ I))
    (h : SimpleGraph (B ⊕ J)) (b : B → Color) :
    Summary (glue g h) b ↔ Summary g b ∧ Summary h b := by
  constructor
  · rintro ⟨z, hz⟩
    have he : Sum.elim (fun i => z (.inl i)) (fun j => z (.inr j)) = z := by
      funext a
      rcases a with a | a <;> rfl
    rw [← he, regionOK_glue] at hz
    exact ⟨⟨_, hz.1⟩, ⟨_, hz.2⟩⟩
  · rintro ⟨⟨x, hx⟩, ⟨y, hy⟩⟩
    exact ⟨Sum.elim x y, (regionOK_glue g h b x y).mpr ⟨hx, hy⟩⟩

/-- Equal summaries are interchangeable against every separated graph continuation. -/
theorem replacement {B I I' J : Type} (g : SimpleGraph (B ⊕ I))
    (g' : SimpleGraph (B ⊕ I')) (h : SimpleGraph (B ⊕ J))
    (he : Summary g = Summary g') (b : B → Color) :
    Summary (glue g h) b ↔ Summary (glue g' h) b := by
  simp only [summary_glue, he]

/-- Seal after imposing all constraints mentioning the forgotten assignment. -/
def closeRegion {B X : Type} (r c : B → X → Prop) : B → Prop :=
  fun b => ∃ x, r b x ∧ c b x

/-- Future constraints may access b but not the eliminated x. -/
theorem seal_future {B X Y : Type} (r c : B → X → Prop) (f : B → Y → Prop)
    (b : B) (y : Y) :
    (closeRegion r c b ∧ f b y) ↔ ∃ x, r b x ∧ c b x ∧ f b y := by
  simp only [closeRegion]
  aesop

theorem empty_prunes {B X Y : Type} (r c : B → X → Prop) (f : B → Y → Prop)
    (he : ∀ b, ¬ closeRegion r c b) : ¬ ∃ b x y, r b x ∧ c b x ∧ f b y := by
  rintro ⟨b, x, y, hr, hc, _⟩
  exact he b ⟨x, hr, hc⟩

/-- Exact number of possible labelled relation tables, not of realizable disk patches. -/
theorem relation_count (k : ℕ) :
    Fintype.card (BoundaryRelations.BoundaryRel k) = 2 ^ (4 ^ k) := by
  simp [BoundaryRelations.BoundaryRel, BoundaryAssignment, Color]

/-- A degree-two private vertex imposes no restriction on its endpoint colours. -/
theorem two_step_free (a b : Color) : ∃ c : Color, c ≠ a ∧ c ≠ b := by
  fin_cases a <;> fin_cases b <;> decide

/-- Arbitrarily many independent subdivided paths are all colour-neutral.
The index type permits repeated endpoint pairs with distinct private centers. -/
theorem path_network_free {P : Type} (a b : P → Color) :
    ∃ x : P → Color, ∀ p, x p ≠ a p ∧ x p ≠ b p := by
  classical
  exact Classical.axiomOfChoice (fun p => two_step_free (a p) (b p))

/-- A sealed hub retains a joint restriction: its neighbours omit some colour. -/
theorem hub_iff {B : Type} (b : B → Color) :
    (∃ c : Color, ∀ i, c ≠ b i) ↔ ¬ Function.Surjective b := by
  classical
  simp only [Function.Surjective]
  push Not
  simp only [ne_comm]

end FiveBoundary.LocalClosure
