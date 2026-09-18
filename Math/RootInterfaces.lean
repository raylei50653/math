/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.ForcingLists

/-! Exact list-colouring interfaces used by the degree-5 block reports.

All contacts of one component share a single colouring witness. Components may be glued
only after fixing the same hub colour; parts sharing a cut vertex must agree at that root.
The results are independent of degree bounds, planarity and any cycle-shortening claim. -/
namespace FiveBoundary.RootInterfaces

open ForcingLists

variable {V ι P : Type*}

/-- The complete ordered contact relation; repeated contacts are allowed. -/
def contactRelation (G : SimpleGraph V) (L : V → Finset Color) (p : P → V) :
    Set (P → Color) := {t | ∃ c, ListProper G L c ∧ c ∘ p = t}

/-- Hub colours for which no single contact tuple avoids that colour everywhere. -/
def forbidden (R : Set (P → Color)) : Set Color :=
  {a | ¬ ∃ t ∈ R, ∀ k, t k ≠ a}

/-- A component extends a fixed hub colour precisely when that colour is not forbidden. -/
theorem not_mem_forbidden_iff (G : SimpleGraph V) (L : V → Finset Color)
    (p : P → V) (a : Color) :
    a ∉ forbidden (contactRelation G L p) ↔
      ∃ c, ListProper G L c ∧ ∀ k, c (p k) ≠ a := by
  classical
  simp only [forbidden, Set.mem_ofPred_eq, not_not]
  constructor
  · rintro ⟨t, ⟨c, hc, rfl⟩, ht⟩
    exact ⟨c, hc, ht⟩
  · rintro ⟨c, hc, hp⟩
    exact ⟨c ∘ p, ⟨c, hc, rfl⟩, hp⟩

/-- Weakening a joint relation can only remove forbidden colours. -/
theorem forbidden_antitone {R S : Set (P → Color)} (h : R ⊆ S) :
    forbidden S ⊆ forbidden R := by
  rintro a ha ⟨t, ht, ht'⟩
  exact ha ⟨t, h ht, ht'⟩

/-- For a single contact, rejection means every attainable root colour equals the hub colour.
The empty root set rejects every colour, so nonemptiness must not be silently dropped. -/
theorem mem_forbidden_single_iff (G : SimpleGraph V) (L : V → Finset Color)
    (r : V) (a : Color) :
    a ∈ forbidden (contactRelation G L (fun _ : Unit => r)) ↔ avail G L r ⊆ {a} := by
  constructor
  · intro h b hb
    obtain ⟨c, hc, hcr⟩ := hb
    by_contra hba
    apply h
    refine ⟨c ∘ (fun _ : Unit => r), ⟨c, hc, rfl⟩, fun _ => ?_⟩
    simpa only [Function.comp_apply, hcr, Set.mem_singleton_iff] using hba
  · intro h
    rintro ⟨t, ⟨c, hc, rfl⟩, ht⟩
    exact ht () (h ⟨c, hc, rfl⟩)

/-- For a colourable single-contact component, rejection is exactly singleton forcing. -/
theorem mem_forbidden_single_iff_eq (G : SimpleGraph V) (L : V → Finset Color)
    (r : V) (a : Color) (hne : (avail G L r).Nonempty) :
    a ∈ forbidden (contactRelation G L (fun _ : Unit => r)) ↔ avail G L r = {a} := by
  rw [mem_forbidden_single_iff]
  constructor
  · intro h
    apply Set.Subset.antisymm h
    obtain ⟨b, hb⟩ := hne
    have hba : b = a := h hb
    simpa [hba] using Set.singleton_subset_iff.mpr hb
  · intro h; exact h.subset

/-! ### One centre and independent components -/

variable {Q : ι → Type*}

/-- `none` is the hub. `some (i,v)` is vertex `v` of component `i`.
There are no edges between different components. -/
def hubGraph (G : ι → SimpleGraph V) (p : (i : ι) → Q i → V) :
    SimpleGraph (Option (ι × V)) where
  Adj
    | none, none => False
    | none, some (i, v) => ∃ k, p i k = v
    | some (i, v), none => ∃ k, p i k = v
    | some (i, u), some (j, v) => i = j ∧ (G i).Adj u v
  symm := ⟨by
    intro x y h
    cases x with
    | none => cases y <;> exact h
    | some x =>
      rcases x with ⟨i, u⟩
      cases y with
      | none => exact h
      | some y =>
        rcases y with ⟨j, v⟩
        obtain ⟨rfl, h⟩ := h
        exact ⟨rfl, h.symm⟩⟩
  loopless := ⟨by
    intro x h
    cases x with
    | none => exact h
    | some x => exact (G x.1).irrefl h.2⟩

/-- Hub list and component lists in a common colour frame. -/
def hubLists (A : Finset Color) (L : ι → V → Finset Color) :
    Option (ι × V) → Finset Color
  | none => A
  | some (i, v) => L i v

/-- Exact hub gluing, retaining one simultaneous colouring of all contacts per component. -/
theorem mem_avail_hub_iff (G : ι → SimpleGraph V) (L : ι → V → Finset Color)
    (p : (i : ι) → Q i → V) (A : Finset Color) (a : Color) :
    a ∈ avail (hubGraph G p) (hubLists A L) none ↔
      a ∈ A ∧ ∀ i, a ∉ forbidden (contactRelation (G i) (L i) (p i)) := by
  classical
  constructor
  · rintro ⟨c, hc, ha⟩
    refine ⟨ha ▸ hc.2 none, fun i => (not_mem_forbidden_iff _ _ _ _).2 ?_⟩
    refine ⟨fun v => c (some (i, v)), ⟨?_, fun v => hc.2 _⟩, ?_⟩
    · intro u v huv
      exact hc.1 _ _ ⟨rfl, huv⟩
    · intro k
      rw [← ha]
      exact hc.1 _ _ ⟨k, rfl⟩
  · rintro ⟨ha, hi⟩
    have witnesses := fun i => (not_mem_forbidden_iff _ _ _ _).1 (hi i)
    choose c hc hp using witnesses
    let f : Option (ι × V) → Color
      | none => a
      | some (i, v) => c i v
    refine ⟨f, ⟨?_, ?_⟩, rfl⟩
    · intro x y hxy
      cases x with
      | none =>
        cases y with
        | none => exact hxy.elim
        | some y =>
          obtain ⟨k, hk⟩ := hxy
          exact (hk ▸ hp y.1 k).symm
      | some x =>
        cases y with
        | none =>
          obtain ⟨k, hk⟩ := hxy
          change c x.1 x.2 ≠ a
          simpa only [hk] using hp x.1 k
        | some y =>
          rcases x with ⟨i, u⟩
          rcases y with ⟨j, v⟩
          obtain ⟨rfl, h⟩ := hxy
          exact (hc i).1 u v h
    · intro x
      cases x with
      | none => exact ha
      | some x => exact (hc x.1).2 x.2

/-- The reusable `Z = A \ ⋃ F` formula; it is a set of hub colours, not a full relation. -/
theorem avail_hub (G : ι → SimpleGraph V) (L : ι → V → Finset Color)
    (p : (i : ι) → Q i → V) (A : Finset Color) :
    avail (hubGraph G p) (hubLists A L) none =
      (↑A : Set Color) \ ⋃ i, forbidden (contactRelation (G i) (L i) (p i)) := by
  ext a
  simp [mem_avail_hub_iff]

/-! ### Shared cut vertex -/

/-- If two vertex regions cover the graph, intersect exactly at `r`, and every edge lies
in one region, the full root set is exactly the intersection of the two regional root sets.
No colourability assumption is imposed on either side. -/
theorem avail_eq_inter (G : SimpleGraph V) (L : V → Finset Color)
    (A B : Set V) (r : V) (hcover : ∀ v, v ∈ A ∨ v ∈ B)
    (hinter : A ∩ B = {r})
    (hedge : ∀ u v, G.Adj u v → (u ∈ A ∧ v ∈ A) ∨ (u ∈ B ∧ v ∈ B)) :
    avail G L r = availOn G L A r ∩ availOn G L B r := by
  classical
  have hr : r ∈ A ∧ r ∈ B := by
    have : r ∈ A ∩ B := by rw [hinter]; exact Set.mem_singleton r
    exact this
  ext a
  constructor
  · rintro ⟨c, hc, ha⟩
    exact ⟨⟨c, fun u v h => hc.1 u v h.1, fun v _ => hc.2 v, ha⟩,
      ⟨c, fun u v h => hc.1 u v h.1, fun v _ => hc.2 v, ha⟩⟩
  · rintro ⟨⟨c, hc, hLc, hcr⟩, ⟨d, hd, hLd, hdr⟩⟩
    let f := fun v => if v ∈ A then c v else d v
    have hfA : ∀ v ∈ A, f v = c v := fun v hv => ite_eq_left hv
    have hfB : ∀ v ∈ B, f v = d v := by
      intro v hv
      by_cases hvA : v ∈ A
      · have heq : v = r := by
          have : v ∈ A ∩ B := ⟨hvA, hv⟩
          rwa [hinter, Set.mem_singleton_iff] at this
        subst v
        exact (hfA r hr.1).trans (hcr.trans hdr.symm)
      · exact ite_eq_right hvA
    refine ⟨f, ⟨?_, ?_⟩, (hfA r hr.1).trans hcr⟩
    · intro u v huv
      rcases hedge u v huv with ⟨hu, hv⟩ | ⟨hu, hv⟩
      · rw [hfA u hu, hfA v hv]; exact hc u v ⟨huv, hu, hv⟩
      · rw [hfB u hu, hfB v hv]; exact hd u v ⟨huv, hu, hv⟩
    · intro v
      rcases hcover v with hv | hv
      · rw [hfA v hv]; exact hLc v hv
      · rw [hfB v hv]; exact hLd v hv

/-- Root-set nonemptiness is exactly list colourability. -/
theorem listColorable_iff_avail_nonempty (G : SimpleGraph V) (L : V → Finset Color)
    (r : V) : ListColorable G L ↔ (avail G L r).Nonempty := by
  constructor
  · rintro ⟨c, hc⟩; exact ⟨c r, c, hc, rfl⟩
  · rintro ⟨a, c, hc, _⟩; exact ⟨c, hc⟩

/-- Boolean gluing is weaker than equality of the individual or intersected root sets. -/
theorem listColorable_iff_inter_nonempty (G : SimpleGraph V) (L : V → Finset Color)
    (A B : Set V) (r : V) (hcover : ∀ v, v ∈ A ∨ v ∈ B)
    (hinter : A ∩ B = {r})
    (hedge : ∀ u v, G.Adj u v → (u ∈ A ∧ v ∈ A) ∨ (u ∈ B ∧ v ∈ B)) :
    ListColorable G L ↔ (availOn G L A r ∩ availOn G L B r).Nonempty := by
  rw [listColorable_iff_avail_nonempty G L r, avail_eq_inter G L A B r hcover hinter hedge]

/-- Existence of a global colouring is exactly nonemptiness of the hub's unblocked list. -/
theorem listColorable_hub_iff (G : ι → SimpleGraph V) (L : ι → V → Finset Color)
    (p : (i : ι) → Q i → V) (A : Finset Color) :
    ListColorable (hubGraph G p) (hubLists A L) ↔
      ((↑A : Set Color) \ ⋃ i, forbidden (contactRelation (G i) (L i) (p i))).Nonempty := by
  rw [listColorable_iff_avail_nonempty _ _ none, avail_hub]

/-! ### A single path step -/

/-- Extend an endpoint message through one inequality edge into list `L`. -/
def transfer (S L : Set Color) : Set Color := {b | b ∈ L ∧ ∃ a ∈ S, a ≠ b}

@[simp] theorem transfer_empty (L : Set Color) : transfer ∅ L = ∅ := by
  ext b; simp [transfer]

@[simp] theorem transfer_singleton (a : Color) (L : Set Color) :
    transfer {a} L = L \ {a} := by
  ext b; simp [transfer, ne_comm]

/-- Once a message contains two distinct colours, the next message is the entire next list. -/
theorem transfer_of_two {S : Set Color} (L : Set Color) {a b : Color}
    (ha : a ∈ S) (hb : b ∈ S) (hab : a ≠ b) : transfer S L = L := by
  ext x
  constructor
  · exact fun h => h.1
  · intro hx
    by_cases hax : a = x
    · exact ⟨hx, b, hb, fun hbx => hab (hax.trans hbx.symm)⟩
    · exact ⟨hx, a, ha, hax⟩

/-! ### Irredundant forbidden-colour covers -/

/-- If `F` covers `A` and removing any one member frees a colour of `A`, each member has
its own private colour in `A`. The colours are distinct, even when members are not singletons. -/
theorem private_colours (A : Finset Color) (F : ι → Set Color)
    (hcover : ∀ a ∈ A, ∃ i, a ∈ F i)
    (hdelete : ∀ i, ∃ a ∈ A, ∀ j, j ≠ i → a ∉ F j) :
    ∃ p : ι → Color, Function.Injective p ∧
      ∀ i, p i ∈ A ∧ p i ∈ F i ∧ ∀ j, j ≠ i → p i ∉ F j := by
  classical
  choose p hp hother using hdelete
  have hmem : ∀ i, p i ∈ F i := by
    intro i
    obtain ⟨j, hj⟩ := hcover (p i) (hp i)
    by_cases hji : j = i
    · simpa [hji] using hj
    · exact (hother i j hji hj).elim
  refine ⟨p, ?_, fun i => ⟨hp i, hmem i, hother i⟩⟩
  intro i j hij
  by_contra hne
  exact hother i j (Ne.symm hne) (hij.symm ▸ hmem j)

/-- The number of indispensable components is bounded by the number of available hub colours.
The graph-theoretic edge-deletion discharge lemma is a separate obligation. -/
theorem card_le_of_irredundant_cover [Fintype ι] (A : Finset Color) (F : ι → Set Color)
    (hcover : ∀ a ∈ A, ∃ i, a ∈ F i)
    (hdelete : ∀ i, ∃ a ∈ A, ∀ j, j ≠ i → a ∉ F j) :
    Fintype.card ι ≤ A.card := by
  obtain ⟨p, hinj, hp⟩ := private_colours A F hcover hdelete
  let f : ι → {a // a ∈ A} := fun i => ⟨p i, (hp i).1⟩
  have hf : Function.Injective f := fun i j h => hinj (congrArg Subtype.val h)
  simpa using Fintype.card_le_of_injective f hf

end FiveBoundary.RootInterfaces
