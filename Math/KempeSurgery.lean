/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.Boundary

/-! Graph-level Kempe lemmas that were paper proofs in
`docs/c5_kempe_connectivity.md` §1 and `docs/c5_cut_interfaces.md` §2.

* `reachable_sup_iff_reflTransGen` / `componentEquiv`: connectivity of `H ⊔ A` is computed on
  the quotient whose nodes are the components of `H`, wired by the edges of `A`. This is the
  "delete the cut, keep the retained blocks, add the switched cut edges" interface.
* `swapOn`: swapping two colours on a set closed under two-colour adjacency keeps a colouring
  proper, fixes the `{a,b}` and complementary induced graphs, and rewrites every mixed pair
  `{a,d}` as the retained graph on `(a \ S) ∪ d` plus `d`-neighbour stars at `b ∩ S`.

Nothing here uses planarity, disks or a four-colour axiom; the vertex type is arbitrary. -/
namespace FiveBoundary.KempeSurgery

open SimpleGraph

variable {V : Type*}

/-! ### Contracting components then adding edges -/

/-- Quotient graph: components of `H` are the nodes, `A`-edges between different components
are the arcs. -/
def quotientGraph (H A : SimpleGraph V) : SimpleGraph H.ConnectedComponent where
  Adj C D := C ≠ D ∧ ∃ x y, H.connectedComponentMk x = C ∧ H.connectedComponentMk y = D ∧ A.Adj x y
  symm := ⟨by
    rintro C D ⟨hne, x, y, hx, hy, hxy⟩
    exact ⟨hne.symm, y, x, hy, hx, hxy.symm⟩⟩
  loopless := ⟨by
    rintro C ⟨hne, -⟩
    exact hne rfl⟩

/-- Reachability in `H ⊔ A` is the reflexive-transitive closure of "reachable in `H`, or one
`A`-edge". -/
theorem reachable_sup_iff_reflTransGen (H A : SimpleGraph V) (u v : V) :
    (H ⊔ A).Reachable u v ↔
      Relation.ReflTransGen (fun x y => H.Reachable x y ∨ A.Adj x y) u v := by
  constructor
  · intro h
    rw [reachable_iff_reflTransGen] at h
    refine Relation.ReflTransGen.mono ?_ _ _ h
    rintro x y (hxy | hxy)
    · exact Or.inl hxy.reachable
    · exact Or.inr hxy
  · intro h
    induction h with
    | refl => exact Reachable.refl _
    | tail _ hxy ih =>
      refine ih.trans ?_
      rcases hxy with hxy | hxy
      · exact hxy.mono le_sup_left
      · exact (Adj.reachable hxy).mono le_sup_right

theorem quotient_reachable_of_reachable (H A : SimpleGraph V) {u v : V}
    (h : (H ⊔ A).Reachable u v) :
    (quotientGraph H A).Reachable (H.connectedComponentMk u) (H.connectedComponentMk v) := by
  rw [reachable_sup_iff_reflTransGen] at h
  induction h with
  | refl => exact Reachable.refl _
  | @tail x y _ hxy ih =>
    refine ih.trans ?_
    rcases hxy with hxy | hxy
    · rw [ConnectedComponent.sound hxy]
    · by_cases hcomp : H.connectedComponentMk x = H.connectedComponentMk y
      · rw [hcomp]
      · exact Adj.reachable ⟨hcomp, x, y, rfl, rfl, hxy⟩

theorem reachable_of_quotient_reachable (H A : SimpleGraph V) {C D : H.ConnectedComponent}
    (h : (quotientGraph H A).Reachable C D) :
    ∀ u v, H.connectedComponentMk u = C → H.connectedComponentMk v = D →
      (H ⊔ A).Reachable u v := by
  rw [reachable_iff_reflTransGen] at h
  induction h with
  | refl =>
    intro u v hu hv
    exact (ConnectedComponent.exact (hu.trans hv.symm)).mono le_sup_left
  | tail _ hxy ih =>
    intro u v hu hv
    obtain ⟨-, x, y, hx, hy, hxy⟩ := hxy
    refine (ih u x hu hx).trans (((Adj.reachable hxy).mono le_sup_right).trans ?_)
    exact (ConnectedComponent.exact (hy.trans hv.symm)).mono le_sup_left

/-- Connectivity of `H ⊔ A` equals connectivity of the quotient graph on `H`-components. -/
theorem reachable_sup_iff_quotient (H A : SimpleGraph V) (u v : V) :
    (H ⊔ A).Reachable u v ↔
      (quotientGraph H A).Reachable (H.connectedComponentMk u) (H.connectedComponentMk v) :=
  ⟨quotient_reachable_of_reachable H A,
    fun h => reachable_of_quotient_reachable H A h u v rfl rfl⟩

/-- The map from `H ⊔ A`-components to quotient components. -/
def componentMap (H A : SimpleGraph V) :
    (H ⊔ A).ConnectedComponent → (quotientGraph H A).ConnectedComponent :=
  ConnectedComponent.lift (fun v => (quotientGraph H A).connectedComponentMk
      (H.connectedComponentMk v))
    (fun _ _ p _ => ConnectedComponent.sound (quotient_reachable_of_reachable H A ⟨p⟩))

theorem componentMap_mk (H A : SimpleGraph V) (v : V) :
    componentMap H A ((H ⊔ A).connectedComponentMk v) =
      (quotientGraph H A).connectedComponentMk (H.connectedComponentMk v) := rfl

theorem componentMap_bijective (H A : SimpleGraph V) : Function.Bijective (componentMap H A) := by
  constructor
  · intro C D
    induction C using ConnectedComponent.ind with
    | h u =>
      induction D using ConnectedComponent.ind with
      | h v =>
        intro h
        rw [componentMap_mk, componentMap_mk] at h
        exact ConnectedComponent.sound
          (reachable_of_quotient_reachable H A (ConnectedComponent.exact h) u v rfl rfl)
  · intro Q
    induction Q using ConnectedComponent.ind with
    | h C =>
      induction C using ConnectedComponent.ind with
      | h v => exact ⟨(H ⊔ A).connectedComponentMk v, rfl⟩

/-- Components of `H ⊔ A` are in bijection with components of the quotient graph: the
one-step cut interface of `docs/c5_cut_interfaces.md` §2 loses nothing. -/
noncomputable def componentEquiv (H A : SimpleGraph V) :
    (H ⊔ A).ConnectedComponent ≃ (quotientGraph H A).ConnectedComponent :=
  Equiv.ofBijective _ (componentMap_bijective H A)

/-! ### Two-colour induced subgraphs on a common vertex type -/

/-- Edges of `G` with both ends in `s`, kept on the ambient vertex type. -/
def within (G : SimpleGraph V) (s : Set V) : SimpleGraph V where
  Adj u v := G.Adj u v ∧ u ∈ s ∧ v ∈ s
  symm := ⟨fun _ _ ⟨h, hu, hv⟩ => ⟨h.symm, hv, hu⟩⟩
  loopless := ⟨fun _ ⟨h, _, _⟩ => G.loopless.irrefl _ h⟩

theorem within_adj (G : SimpleGraph V) (s : Set V) (u v : V) :
    (within G s).Adj u v ↔ G.Adj u v ∧ u ∈ s ∧ v ∈ s := Iff.rfl

/-- The `{a,b}`-induced graph of a colouring. -/
def pairGraph (G : SimpleGraph V) (c : V → Color) (a b : Color) : SimpleGraph V :=
  within G {v | c v = a ∨ c v = b}

/-- `S` is a union of `{a,b}`-components: contained in the `{a,b}` vertices and closed under
`{a,b}`-adjacency. A single connected component is the intended case. -/
structure KempeSet (G : SimpleGraph V) (c : V → Color) (a b : Color) (S : Set V) : Prop where
  subset : ∀ v ∈ S, c v = a ∨ c v = b
  closed : ∀ u ∈ S, ∀ v, G.Adj u v → (c v = a ∨ c v = b) → v ∈ S

/-- Swap colours `a`, `b` on `S`. -/
noncomputable def swapOn (c : V → Color) (a b : Color) (S : Set V) : V → Color :=
  open Classical in fun v => if v ∈ S then Equiv.swap a b (c v) else c v

theorem swapOn_of_mem {c : V → Color} {a b : Color} {S : Set V} {v : V} (h : v ∈ S) :
    swapOn c a b S v = Equiv.swap a b (c v) := by simp [swapOn, h]

theorem swapOn_of_not_mem {c : V → Color} {a b : Color} {S : Set V} {v : V} (h : v ∉ S) :
    swapOn c a b S v = c v := by simp [swapOn, h]

/-- A global colour transposition is the swap on all `{a,b}` vertices (which is a Kempe set),
so Kempe classes are closed under `S₄` (`docs/c5_kempe_class_counts.md` §1). -/
theorem swapOn_univPair (c : V → Color) (a b : Color) :
    swapOn c a b {v | c v = a ∨ c v = b} = Equiv.swap a b ∘ c := by
  funext v
  by_cases h : c v = a ∨ c v = b
  · exact swapOn_of_mem (show v ∈ {v | c v = a ∨ c v = b} from h)
  · rw [swapOn_of_not_mem (show v ∉ {v | c v = a ∨ c v = b} from h), Function.comp_apply,
      Equiv.swap_apply_of_ne_of_ne]
    · exact fun e => h (Or.inl e)
    · exact fun e => h (Or.inr e)

theorem kempeSet_univPair (G : SimpleGraph V) (c : V → Color) (a b : Color) :
    KempeSet G c a b {v | c v = a ∨ c v = b} :=
  ⟨fun _ h => h, fun _ _ _ _ h => h⟩

/-- Swapping on a Kempe set keeps the colouring proper. -/
theorem swapOn_proper {G : SimpleGraph V} {c : V → Color} {a b : Color} {S : Set V}
    (hS : KempeSet G c a b S) (hc : ∀ u v, G.Adj u v → c u ≠ c v) :
    ∀ u v, G.Adj u v → swapOn c a b S u ≠ swapOn c a b S v := by
  intro u v huv
  by_cases hu : u ∈ S <;> by_cases hv : v ∈ S
  · rw [swapOn_of_mem hu, swapOn_of_mem hv]
    exact fun e => hc u v huv ((Equiv.swap a b).injective e)
  · rw [swapOn_of_mem hu, swapOn_of_not_mem hv]
    intro e
    have hvab : c v = a ∨ c v = b := by
      rcases hS.subset u hu with h | h <;> rw [h] at e
      · rw [Equiv.swap_apply_left] at e; exact Or.inr e.symm
      · rw [Equiv.swap_apply_right] at e; exact Or.inl e.symm
    exact hv (hS.closed u hu v huv hvab)
  · rw [swapOn_of_not_mem hu, swapOn_of_mem hv]
    intro e
    have huab : c u = a ∨ c u = b := by
      rcases hS.subset v hv with h | h <;> rw [h] at e
      · rw [Equiv.swap_apply_left] at e; exact Or.inr e
      · rw [Equiv.swap_apply_right] at e; exact Or.inl e
    exact hu (hS.closed v hv u huv.symm huab)
  · rw [swapOn_of_not_mem hu, swapOn_of_not_mem hv]
    exact hc u v huv

/-- Membership in `{a,b}` is unchanged pointwise by the swap. -/
theorem swapOn_pair_iff (c : V → Color) (a b : Color) (S : Set V) (v : V) :
    (swapOn c a b S v = a ∨ swapOn c a b S v = b) ↔ (c v = a ∨ c v = b) := by
  by_cases h : v ∈ S
  · rw [swapOn_of_mem h]
    constructor
    · rintro (e | e)
      · have := (Equiv.swap a b).injective (e.trans (Equiv.swap_apply_right a b).symm)
        exact Or.inr this
      · have := (Equiv.swap a b).injective (e.trans (Equiv.swap_apply_left a b).symm)
        exact Or.inl this
    · rintro (e | e) <;> rw [e]
      · rw [Equiv.swap_apply_left]; exact Or.inr rfl
      · rw [Equiv.swap_apply_right]; exact Or.inl rfl
  · rw [swapOn_of_not_mem h]

/-- The `{a,b}`-induced graph, hence its component partition, is untouched. -/
theorem pairGraph_swap_same (G : SimpleGraph V) (c : V → Color) (a b : Color) (S : Set V) :
    pairGraph G (swapOn c a b S) a b = pairGraph G c a b := by
  ext u v
  simp only [pairGraph, within_adj, Set.mem_ofPred_eq, swapOn_pair_iff]

/-- Outside `{a,b}` the swap changes nothing, so any pair disjoint from `{a,b}` (the
complementary pair `BD`) keeps its induced graph. -/
theorem swapOn_of_ne {c : V → Color} {a b : Color} {S : Set V} {v : V}
    (hS : ∀ v ∈ S, c v = a ∨ c v = b) (ha : c v ≠ a) (hb : c v ≠ b) :
    swapOn c a b S v = c v := by
  by_cases h : v ∈ S
  · exact absurd (hS v h) (by rintro (e | e); exacts [ha e, hb e])
  · exact swapOn_of_not_mem h

theorem swapOn_eq_iff_of_ne {c : V → Color} {a b : Color} {S : Set V}
    (hS : ∀ v ∈ S, c v = a ∨ c v = b) {x : Color} (hxa : x ≠ a) (hxb : x ≠ b) (v : V) :
    swapOn c a b S v = x ↔ c v = x := by
  by_cases h : v ∈ S
  · rw [swapOn_of_mem h]
    rcases hS v h with e | e <;> rw [e]
    · rw [Equiv.swap_apply_left]; exact ⟨fun e => absurd e.symm hxb, fun e => absurd e.symm hxa⟩
    · rw [Equiv.swap_apply_right]; exact ⟨fun e => absurd e.symm hxa, fun e => absurd e.symm hxb⟩
  · rw [swapOn_of_not_mem h]

theorem pairGraph_swap_complementary (G : SimpleGraph V) (c : V → Color) {a b x y : Color}
    {S : Set V} (hS : ∀ v ∈ S, c v = a ∨ c v = b)
    (hxa : x ≠ a) (hxb : x ≠ b) (hya : y ≠ a) (hyb : y ≠ b) :
    pairGraph G (swapOn c a b S) x y = pairGraph G c x y := by
  ext u v
  simp only [pairGraph, within_adj, Set.mem_ofPred_eq,
    swapOn_eq_iff_of_ne hS hxa hxb, swapOn_eq_iff_of_ne hS hya hyb]

/-! ### Mixed pairs: delete `a ∩ S`, contract, add stars from `b ∩ S` -/

/-- Vertex set of the mixed pair `{a,d}` after the swap, expressed in the old colouring. -/
theorem swapOn_mixed_iff {c : V → Color} {a b d : Color} {S : Set V}
    (hS : ∀ v ∈ S, c v = a ∨ c v = b) (hda : d ≠ a) (hdb : d ≠ b) (hab : a ≠ b) (v : V) :
    (swapOn c a b S v = a ∨ swapOn c a b S v = d) ↔
      ((c v = a ∧ v ∉ S) ∨ c v = d ∨ (c v = b ∧ v ∈ S)) := by
  rw [swapOn_eq_iff_of_ne hS hda hdb]
  by_cases h : v ∈ S
  · rw [swapOn_of_mem h]
    rcases hS v h with e | e <;> rw [e]
    · rw [Equiv.swap_apply_left]
      constructor
      · rintro (e' | e')
        · exact absurd e' hab.symm
        · exact Or.inr (Or.inl e')
      · rintro (⟨-, hn⟩ | e' | ⟨e', -⟩)
        · exact absurd h hn
        · exact Or.inr e'
        · exact absurd e' hab
    · rw [Equiv.swap_apply_right]
      constructor
      · rintro _; exact Or.inr (Or.inr ⟨rfl, h⟩)
      · rintro _; exact Or.inl rfl
  · rw [swapOn_of_not_mem h]
    constructor
    · rintro (e | e)
      · exact Or.inl ⟨e, h⟩
      · exact Or.inr (Or.inl e)
    · rintro (⟨e, -⟩ | e | ⟨-, hm⟩)
      · exact Or.inl e
      · exact Or.inr e
      · exact absurd hm h

/-- Retained graph of the mixed pair: old `{a,d}` vertices with `a ∩ S` deleted. -/
def retained (G : SimpleGraph V) (c : V → Color) (a d : Color) (S : Set V) : SimpleGraph V :=
  within G {v | (c v = a ∧ v ∉ S) ∨ c v = d}

/-- Star edges: each `z ∈ b ∩ S` joined to its old `d`-neighbours. -/
def stars (G : SimpleGraph V) (c : V → Color) (b d : Color) (S : Set V) : SimpleGraph V where
  Adj u v := G.Adj u v ∧ ((c u = b ∧ u ∈ S ∧ c v = d) ∨ (c v = b ∧ v ∈ S ∧ c u = d))
  symm := ⟨fun _ _ ⟨h, hs⟩ => ⟨h.symm, hs.symm⟩⟩
  loopless := ⟨fun _ ⟨h, _⟩ => G.loopless.irrefl _ h⟩

/-- **Surgery lemma** (`docs/c5_kempe_connectivity.md` §1): after swapping `a`, `b` on a
Kempe set `S` of a proper colouring, the `{a,d}`-induced graph is exactly the retained graph
`G[(a \ S) ∪ d]` plus the `d`-neighbour stars at `b ∩ S`. No planarity is used. -/
theorem pairGraph_swap_mixed {G : SimpleGraph V} {c : V → Color} {a b d : Color} {S : Set V}
    (hS : KempeSet G c a b S) (hc : ∀ u v, G.Adj u v → c u ≠ c v)
    (hda : d ≠ a) (hdb : d ≠ b) (hab : a ≠ b) :
    pairGraph G (swapOn c a b S) a d = retained G c a d S ⊔ stars G c b d S := by
  ext u v
  simp only [pairGraph, retained, stars, within_adj, sup_adj, Set.mem_ofPred_eq,
    swapOn_mixed_iff hS.subset hda hdb hab]
  constructor
  · rintro ⟨huv, hu, hv⟩
    rcases hu with hu | hu | hu <;> rcases hv with hv | hv | hv
    · exact Or.inl ⟨huv, Or.inl hu, Or.inl hv⟩
    · exact Or.inl ⟨huv, Or.inl hu, Or.inr hv⟩
    · -- `a \ S` adjacent to `b ∩ S` contradicts closure of `S`.
      exact absurd (hS.closed v hv.2 u huv.symm (Or.inl hu.1)) hu.2
    · exact Or.inl ⟨huv, Or.inr hu, Or.inl hv⟩
    · exact Or.inl ⟨huv, Or.inr hu, Or.inr hv⟩
    · exact Or.inr ⟨huv, Or.inr ⟨hv.1, hv.2, hu⟩⟩
    · exact absurd (hS.closed u hu.2 v huv (Or.inl hv.1)) hv.2
    · exact Or.inr ⟨huv, Or.inl ⟨hu.1, hu.2, hv⟩⟩
    · -- two `b` vertices are never adjacent in a proper colouring.
      exact absurd (hu.1.trans hv.1.symm) (hc u v huv)
  · rintro (⟨huv, hu, hv⟩ | ⟨huv, ⟨hu, hus, hv⟩ | ⟨hv, hvs, hu⟩⟩)
    · refine ⟨huv, ?_, ?_⟩
      · rcases hu with hu | hu
        · exact Or.inl hu
        · exact Or.inr (Or.inl hu)
      · rcases hv with hv | hv
        · exact Or.inl hv
        · exact Or.inr (Or.inl hv)
    · exact ⟨huv, Or.inr (Or.inr ⟨hu, hus⟩), Or.inr (Or.inl hv)⟩
    · exact ⟨huv, Or.inr (Or.inl hu), Or.inr (Or.inr ⟨hv, hvs⟩)⟩

/-- Connectivity of the swapped mixed pair, computed by contracting retained components and
wiring the stars. -/
theorem mixed_reachable_iff_quotient {G : SimpleGraph V} {c : V → Color} {a b d : Color}
    {S : Set V} (hS : KempeSet G c a b S) (hc : ∀ u v, G.Adj u v → c u ≠ c v)
    (hda : d ≠ a) (hdb : d ≠ b) (hab : a ≠ b) (u v : V) :
    (pairGraph G (swapOn c a b S) a d).Reachable u v ↔
      (quotientGraph (retained G c a d S) (stars G c b d S)).Reachable
        ((retained G c a d S).connectedComponentMk u)
        ((retained G c a d S).connectedComponentMk v) := by
  rw [pairGraph_swap_mixed hS hc hda hdb hab, reachable_sup_iff_quotient]

/-! ### Disjoint swaps commute -/

theorem swapOn_union_of_disjoint (c : V → Color) (a b : Color) {S T : Set V}
    (h : Disjoint S T) :
    swapOn (swapOn c a b S) a b T = swapOn c a b (S ∪ T) := by
  funext v
  by_cases hT : v ∈ T
  · have hS : v ∉ S := fun hS => Set.disjoint_left.mp h hS hT
    rw [swapOn_of_mem hT, swapOn_of_not_mem hS, swapOn_of_mem (Set.mem_union_right S hT)]
  · rw [swapOn_of_not_mem hT]
    by_cases hS : v ∈ S
    · rw [swapOn_of_mem hS, swapOn_of_mem (Set.mem_union_left T hS)]
    · rw [swapOn_of_not_mem hS, swapOn_of_not_mem (by simp [hS, hT])]

/-- Swapping two disjoint Kempe sets in either order gives the same colouring. -/
theorem swapOn_comm_of_disjoint (c : V → Color) (a b : Color) {S T : Set V}
    (h : Disjoint S T) :
    swapOn (swapOn c a b S) a b T = swapOn (swapOn c a b T) a b S := by
  rw [swapOn_union_of_disjoint c a b h, swapOn_union_of_disjoint c a b h.symm, Set.union_comm]

/-- A Kempe set stays a Kempe set after any `{a,b}`-swap: the `{a,b}` vertex set and
adjacency are unchanged. -/
theorem kempeSet_swapOn {G : SimpleGraph V} {c : V → Color} {a b : Color} {S T : Set V}
    (hT : KempeSet G c a b T) : KempeSet G (swapOn c a b S) a b T where
  subset := fun v hv => (swapOn_pair_iff c a b S v).mpr (hT.subset v hv)
  closed := fun u hu v huv hv => hT.closed u hu v huv ((swapOn_pair_iff c a b S v).mp hv)

/-- Swapping the same Kempe set twice is the identity. -/
theorem swapOn_swapOn (c : V → Color) (a b : Color) (S : Set V) :
    swapOn (swapOn c a b S) a b S = c := by
  funext v
  by_cases h : v ∈ S
  · rw [swapOn_of_mem h, swapOn_of_mem h, Equiv.swap_apply_self]
  · rw [swapOn_of_not_mem h, swapOn_of_not_mem h]

end FiveBoundary.KempeSurgery
