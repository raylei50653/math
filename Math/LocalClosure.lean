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

/-- At most three forbidden colours leave a usable colour in `Fin 4`. -/
theorem color_free_of_card_le_three (s : Finset Color) (hs : s.card ≤ 3) :
    ∃ c : Color, c ∉ s := by
  have hpos : 0 < sᶜ.card := by
    rw [Finset.card_compl]
    simp [Color]
    omega
  obtain ⟨c, hc⟩ := Finset.card_pos.mp hpos
  exact ⟨c, Finset.mem_compl.mp hc⟩

/-- A type of cardinality at most 3 uses at most three colours, so one colour remains. -/
theorem color_free_of_fintype_card_le_three {α : Type} [Fintype α] (f : α → Color)
    (hα : Fintype.card α ≤ 3) : ∃ c : Color, ∀ a, f a ≠ c := by
  classical
  let s : Finset Color := Finset.univ.image f
  have hs : s.card ≤ 3 :=
    (Finset.card_image_le).trans (by simpa [Finset.card_univ] using hα)
  obtain ⟨c, hc⟩ := color_free_of_card_le_three s hs
  refine ⟨c, fun a ha => hc ?_⟩
  exact Finset.mem_image.mpr ⟨a, Finset.mem_univ a, ha⟩

/-- A degree-two private vertex imposes no restriction on its endpoint colours. -/
theorem two_step_free (a b : Color) : ∃ c : Color, c ≠ a ∧ c ≠ b := by
  let f : Bool → Color := fun x => bif x then a else b
  obtain ⟨c, hc⟩ := color_free_of_fintype_card_le_three f (by simp)
  exact ⟨c, (hc true).symm, (hc false).symm⟩

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

/-! ### R1: a sealed private vertex of degree ≤ 3 does not change the summary -/

/-- Neighbours of a degree-`≤ 3` vertex omit at least one colour. -/
theorem exists_colour_of_degree_le_three {V : Type} (G : SimpleGraph V) (v : V)
    [Fintype (G.neighborSet v)] (c : V → Color) (hd : G.degree v ≤ 3) :
    ∃ col : Color, ∀ w, G.Adj v w → c w ≠ col := by
  obtain ⟨col, hcol⟩ :=
    color_free_of_fintype_card_le_three (fun w : G.neighborSet v => c w.val) (by
      have : Fintype.card (G.neighborSet v) = G.degree v := G.card_neighborSet_eq_degree v
      omega)
  exact ⟨col, fun w hw => hcol ⟨w, hw⟩⟩

/-- Induced region after deleting one sealed private vertex. -/
def deletePrivate {B I : Type} (g : SimpleGraph (B ⊕ I)) (v : I) :
    SimpleGraph (B ⊕ {i : I // i ≠ v}) :=
  g.comap (Sum.map id Subtype.val)

def extendPrivate {I : Type} [DecidableEq I] (v : I)
    (x : {i : I // i ≠ v} → Color) (col : Color) : I → Color :=
  fun i => if h : i = v then col else x ⟨i, h⟩

def keepGet {B I : Type} (v : I) :
    ∀ u : B ⊕ I, u ≠ Sum.inr v → B ⊕ {i : I // i ≠ v}
  | .inl b, _ => .inl b
  | .inr i, h => .inr ⟨i, fun hi => h (congrArg Sum.inr hi)⟩

theorem keepGet_map {B I : Type} (v : I) :
    ∀ (u : B ⊕ I) (hu : u ≠ Sum.inr v),
      Sum.map (id : B → B) (Subtype.val : {i : I // i ≠ v} → I) (keepGet v u hu) = u
  | .inl _, _ => rfl
  | .inr _, _ => rfl

theorem elim_keepGet {B I : Type} [DecidableEq I] (v : I) (b : B → Color)
    (x : {i : I // i ≠ v} → Color) (col : Color) :
    ∀ (u : B ⊕ I) (hu : u ≠ Sum.inr v),
      Sum.elim b x (keepGet v u hu) = Sum.elim b (extendPrivate v x col) u
  | .inl _, _ => rfl
  | .inr i, hu => by
    have hi : i ≠ v := fun h => hu (congrArg Sum.inr h)
    simp [keepGet, extendPrivate, hi]

theorem elim_keep_restrict {B I : Type} {v : I} (b : B → Color) (y : I → Color) :
    ∀ u : B ⊕ {i : I // i ≠ v},
      Sum.elim b (fun i => y i.val) u =
        Sum.elim b y (Sum.map (id : B → B) (Subtype.val : {i : I // i ≠ v} → I) u)
  | .inl _ => rfl
  | .inr _ => rfl

theorem extendPrivate_agree {B I : Type} [DecidableEq I] (v : I) (b : B → Color)
    (x : {i : I // i ≠ v} → Color) (col col' : Color)
    (u : B ⊕ I) (hu : u ≠ Sum.inr v) :
    Sum.elim b (extendPrivate v x col) u = Sum.elim b (extendPrivate v x col') u := by
  cases u with
  | inl _ => rfl
  | inr i =>
    have hi : i ≠ v := fun h => hu (congrArg Sum.inr h)
    simp [extendPrivate, hi]

theorem regionOK_restrict {B I : Type} (g : SimpleGraph (B ⊕ I)) (v : I)
    (b : B → Color) (y : I → Color) (hy : RegionOK g b y) :
    RegionOK (deletePrivate g v) b (fun i => y i.val) := by
  intro u w e
  simpa [elim_keep_restrict b y] using hy _ _ e

/-- Deleting a private vertex never removes a feasible boundary colouring. -/
theorem summary_restrict_private {B I : Type} (g : SimpleGraph (B ⊕ I)) (v : I)
    (b : B → Color) (h : Summary g b) : Summary (deletePrivate g v) b := by
  obtain ⟨y, hy⟩ := h
  exact ⟨fun i => y i.val, regionOK_restrict g v b y hy⟩

theorem regionOK_extend {B I : Type} [DecidableEq I] (g : SimpleGraph (B ⊕ I)) (v : I)
    (b : B → Color) (x : {i : I // i ≠ v} → Color) (col : Color)
    (hx : RegionOK (deletePrivate g v) b x)
    (hcol : ∀ w, g.Adj (.inr v) w → Sum.elim b (extendPrivate v x col) w ≠ col) :
    RegionOK g b (extendPrivate v x col) := by
  intro u w e
  by_cases hu : u = .inr v
  · subst hu
    have : Sum.elim b (extendPrivate v x col) (.inr v) = col := by
      simp [extendPrivate]
    rw [this]
    exact Ne.symm (hcol w e)
  · by_cases hw : w = .inr v
    · subst hw
      have : Sum.elim b (extendPrivate v x col) (.inr v) = col := by
        simp [extendPrivate]
      rw [this]
      exact hcol u e.symm
    · have e' : (deletePrivate g v).Adj (keepGet v u hu) (keepGet v w hw) := by
        simpa [deletePrivate, keepGet_map] using e
      simpa [elim_keepGet v b x col u hu, elim_keepGet v b x col w hw] using
        hx (keepGet v u hu) (keepGet v w hw) e'

/-- A remaining colour for a degree-`≤ 3` private vertex restores a feasible colouring. -/
theorem summary_extend_private {B I : Type} (g : SimpleGraph (B ⊕ I))
    (v : I) [Fintype (g.neighborSet (.inr v))] (b : B → Color)
    (hd : g.degree (.inr v) ≤ 3) (h : Summary (deletePrivate g v) b) :
    Summary g b := by
  classical
  obtain ⟨x, hx⟩ := h
  obtain ⟨col, hcol⟩ :=
    exists_colour_of_degree_le_three g (.inr v) (Sum.elim b (extendPrivate v x 0)) hd
  refine ⟨extendPrivate v x col, regionOK_extend g v b x col hx fun w hw => ?_⟩
  have hw' : w ≠ Sum.inr v := hw.ne.symm
  rw [← extendPrivate_agree (B := B) v b x 0 col w hw']
  exact hcol w hw

/-- R1 at the `LocalClosure` layer: a sealed private vertex of degree at most 3
does not change the complete boundary colouring relation. -/
theorem summary_eq_deletePrivate {B I : Type} (g : SimpleGraph (B ⊕ I))
    (v : I) [Fintype (g.neighborSet (.inr v))] (b : B → Color)
    (hd : g.degree (.inr v) ≤ 3) :
    Summary g b ↔ Summary (deletePrivate g v) b :=
  ⟨summary_restrict_private g v b, summary_extend_private g v b hd⟩

/-! ### C5-cell corollary: the same deletion preserves `Sigma` -/

def ProperOn {V : Type} (G : SimpleGraph V) (c : V → Color) : Prop :=
  ∀ u w, G.Adj u w → c u ≠ c w

def SigmaOn {V : Type} (G : SimpleGraph V) (B : Fin 5 ↪ V) : Set BoundaryColoring :=
  {b | ∃ c, ProperOn G c ∧ c ∘ B = b}

theorem sigma_eq_sigmaOn {n : ℕ} (G : SimpleGraph (Fin n)) (B : Fin 5 ↪ Fin n) :
    Sigma G B = SigmaOn G B :=
  rfl

def fill {V : Type} [DecidableEq V] (v : V) (c : {w : V // w ≠ v} → Color) (col : Color) :
    V → Color :=
  fun w => if h : w = v then col else c ⟨w, h⟩

theorem fill_self {V : Type} [DecidableEq V] (v : V) (c : {w : V // w ≠ v} → Color)
    (col : Color) : fill v c col v = col := by
  simp [fill]

theorem fill_of_ne {V : Type} [DecidableEq V] (v : V) (c : {w : V // w ≠ v} → Color)
    (col : Color) {w : V} (hw : w ≠ v) : fill v c col w = c ⟨w, hw⟩ := by
  simp [fill, hw]

theorem properOn_restrict {V : Type} (G : SimpleGraph V) (v : V) (c : V → Color)
    (hc : ProperOn G c) : ProperOn (G.induce {w | w ≠ v}) (fun w => c w.val) :=
  fun _ _ e => hc _ _ e

theorem properOn_extend {V : Type} [DecidableEq V] (G : SimpleGraph V) (v : V)
    [Fintype (G.neighborSet v)] (c : {w : V // w ≠ v} → Color)
    (hd : G.degree v ≤ 3) (hc : ProperOn (G.induce {w | w ≠ v}) c) :
    ∃ col : Color, ProperOn G (fill v c col) := by
  obtain ⟨col, hcol⟩ := exists_colour_of_degree_le_three G v (fill v c 0) hd
  refine ⟨col, fun u w e => ?_⟩
  by_cases hu : u = v
  · have hw : w ≠ v := hu ▸ e.ne.symm
    have hne : fill v c 0 w ≠ col := hcol w (hu ▸ e)
    rw [hu, fill_self, fill_of_ne (hw := hw)]
    rw [fill_of_ne (hw := hw)] at hne
    exact Ne.symm hne
  · by_cases hw : w = v
    · have hu' : u ≠ v := hw ▸ e.ne
      have hne : fill v c 0 u ≠ col := hcol u (hw ▸ e.symm)
      rw [hw, fill_self, fill_of_ne (hw := hu')]
      rw [fill_of_ne (hw := hu')] at hne
      exact hne
    · simpa [fill, hu, hw] using hc ⟨u, hu⟩ ⟨w, hw⟩ e

theorem sigmaOn_eq_delete {V : Type} (G : SimpleGraph V)
    (B : Fin 5 ↪ V) (v : V) [Fintype (G.neighborSet v)]
    (hv : v ∉ Set.range (B : Fin 5 → V)) (hd : G.degree v ≤ 3) :
    SigmaOn G B =
      SigmaOn (G.induce {w | w ≠ v})
        (Function.Embedding.codRestrict {w | w ≠ v} B fun i h => hv ⟨i, h⟩) := by
  classical
  ext b
  constructor
  · rintro ⟨c, hc, hb⟩
    refine ⟨fun w => c w.val, properOn_restrict G v c hc, ?_⟩
    funext i
    simp [Function.Embedding.codRestrict_apply, ← hb]
  · rintro ⟨c, hc, hb⟩
    obtain ⟨col, hcol⟩ := properOn_extend G v c hd hc
    refine ⟨fill v c col, hcol, ?_⟩
    funext i
    have hi : B i ≠ v := fun h => hv ⟨i, h⟩
    change fill v c col (B i) = b i
    rw [fill_of_ne (hw := hi)]
    exact congrFun hb i

/-- C5-cell form of R1: deleting an off-boundary vertex of degree at most 3
preserves the complete boundary colouring relation. -/
theorem sigma_eq_delete_private {n : ℕ} (G : SimpleGraph (Fin n))
    [DecidableRel G.Adj] (B : Fin 5 ↪ Fin n) (v : Fin n)
    (hv : v ∉ Set.range (B : Fin 5 → Fin n)) (hd : G.degree v ≤ 3) :
    Sigma G B =
      SigmaOn (G.induce {w | w ≠ v})
        (Function.Embedding.codRestrict {w | w ≠ v} B fun i h => hv ⟨i, h⟩) := by
  rw [sigma_eq_sigmaOn]
  exact sigmaOn_eq_delete G B v hv hd

end FiveBoundary.LocalClosure
