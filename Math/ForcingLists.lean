/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.KempeSurgery

/-! Forcing-list lemmas shared by the triangle-block and cycle-block reports.

The C5 block reports (`docs/c5_tree_cores.md` §2–3, `docs/c5_pentagon_branches.md` §1 and §4,
`docs/c5_two_triangle_blocks.md` §2–3, `docs/c5_three_triangle_blocks.md` §1,
`docs/c5_shared_triangle_blocks.md` §2) keep reusing the same handful of list-colouring
facts as paper lemmas. Their semantics are now fixed, so they are proved here once, on an
arbitrary vertex type, without planarity, disks or a four-colour axiom.

* `listColorable_iff_bridge` / `bridge_forced`: gluing across a bridge, and the forced common
  singleton at both ends of a bridge of an uncolourable instance whose two sides are colourable.
* `listProper_swap` / `forced_eq_of_symmetric`: if two colours are interchangeable on every
  list, the set of root colours is swap-invariant, so a root forced to one of them cannot avoid
  the other ("a `c`-forcer must touch a `c`-coloured boundary vertex").
* `forced_palettes`: at a vertex whose incident branches each force one colour, blocking plus
  edge-minimality make the forced colours distinct and exactly the list of the vertex.
* `cycleGraph`, `cycle_two_lists_uncolorable_iff`, `cycle_uncolorable_iff`: a cycle with
  two-colour lists is uncolourable iff it is odd and every list is the same pair; lists of size
  at least two with one list of size at least three are always colourable. `cycleGraph 3 = C5`.
* `triangle_two_lists_uncolorable_iff`, `shared_chain_interface`, `apex_extension_iff`: the
  triangle instances, including the `P = Q = univ \ R` interface of the shared-cut-vertex chain
  and the 36-case forbidden-colour rule of a triangle apex. -/
namespace FiveBoundary.ForcingLists

open Finset SimpleGraph

variable {V : Type*}

/-- A proper colouring of `G` obeying the lists `L`. -/
def ListProper (G : SimpleGraph V) (L : V → Finset Color) (c : V → Color) : Prop :=
  (∀ u v, G.Adj u v → c u ≠ c v) ∧ ∀ v, c v ∈ L v

/-- The list instance `(G, L)` has a proper list colouring. -/
def ListColorable (G : SimpleGraph V) (L : V → Finset Color) : Prop :=
  ∃ c, ListProper G L c

/-! ### Bridge gluing -/

/-- Colours a vertex can take in colourings of the part of `G` inside `A`: only edges with both
ends in `A` and only the lists of `A` are enforced. -/
def availOn (G : SimpleGraph V) (L : V → Finset Color) (A : Set V) (u : V) : Set Color :=
  {a | ∃ c : V → Color, (∀ x y, (KempeSurgery.within G A).Adj x y → c x ≠ c y) ∧
    (∀ x ∈ A, c x ∈ L x) ∧ c u = a}

/-- Colours a root can take in list colourings of the whole instance. -/
def avail (G : SimpleGraph V) (L : V → Finset Color) (r : V) : Set Color :=
  {a | ∃ c, ListProper G L c ∧ c r = a}

/-- If `uv` is the only edge of `G` leaving `A` (`u ∈ A`, `v ∉ A`), the instance is colourable
iff the two sides admit colourings whose colours at `u` and `v` differ. -/
theorem listColorable_iff_bridge (G : SimpleGraph V) (L : V → Finset Color) (A : Set V)
    {u v : V} (hu : u ∈ A) (hv : v ∉ A) (huv : G.Adj u v)
    (hcross : ∀ x y, G.Adj x y → x ∈ A → y ∉ A → x = u ∧ y = v) :
    ListColorable G L ↔ ∃ a ∈ availOn G L A u, ∃ b ∈ availOn G L Aᶜ v, a ≠ b := by
  constructor
  · rintro ⟨c, hc, hL⟩
    exact ⟨c u, ⟨c, fun x y h => hc x y h.1, fun x _ => hL x, rfl⟩,
      c v, ⟨c, fun x y h => hc x y h.1, fun x _ => hL x, rfl⟩, hc u v huv⟩
  · rintro ⟨a, ⟨c₁, hc₁, hL₁, rfl⟩, b, ⟨c₂, hc₂, hL₂, rfl⟩, hab⟩
    classical
    refine ⟨fun x => if x ∈ A then c₁ x else c₂ x, ?_, ?_⟩
    · intro x y hxy
      by_cases hx : x ∈ A <;> by_cases hy : y ∈ A <;> simp only [hx, hy, ite_true, ite_false]
      · exact hc₁ x y ⟨hxy, hx, hy⟩
      · obtain ⟨rfl, rfl⟩ := hcross x y hxy hx hy
        exact hab
      · obtain ⟨rfl, rfl⟩ := hcross y x hxy.symm hy hx
        exact hab.symm
      · exact hc₂ x y ⟨hxy, hx, hy⟩
    · intro x
      by_cases hx : x ∈ A
      · simp only [hx, ite_true]; exact hL₁ x hx
      · simp only [hx, ite_false]; exact hL₂ x hx

/-- Bridge forcing: an uncolourable instance whose two sides are colourable forces the same
single colour at both ends of the bridge. -/
theorem bridge_forced (G : SimpleGraph V) (L : V → Finset Color) (A : Set V)
    {u v : V} (hu : u ∈ A) (hv : v ∉ A) (huv : G.Adj u v)
    (hcross : ∀ x y, G.Adj x y → x ∈ A → y ∉ A → x = u ∧ y = v)
    (hG : ¬ ListColorable G L) (hS : (availOn G L A u).Nonempty)
    (hT : (availOn G L Aᶜ v).Nonempty) :
    ∃ k, availOn G L A u = {k} ∧ availOn G L Aᶜ v = {k} := by
  rw [listColorable_iff_bridge G L A hu hv huv hcross] at hG
  replace hG : ∀ a ∈ availOn G L A u, ∀ b ∈ availOn G L Aᶜ v, a = b :=
    fun a ha b hb => by_contra fun h => hG ⟨a, ha, b, hb, h⟩
  obtain ⟨a, ha⟩ := hS
  obtain ⟨b, hb⟩ := hT
  have hab := hG a ha b hb
  refine ⟨a, Set.eq_singleton_iff_unique_mem.mpr ⟨ha, fun x hx => hG x hx b hb ▸ hab.symm⟩,
    Set.eq_singleton_iff_unique_mem.mpr ⟨hab ▸ hb, fun y hy => (hG a ha y hy).symm⟩⟩

/-! ### Colour symmetry of a forced root -/

/-- If `a` and `b` are interchangeable on every list, swapping them keeps a list colouring. -/
theorem listProper_swap {G : SimpleGraph V} {L : V → Finset Color} {c : V → Color}
    (h : ListProper G L c) {a b : Color} (hsym : ∀ v, a ∈ L v ↔ b ∈ L v) :
    ListProper G L (Equiv.swap a b ∘ c) := by
  refine ⟨fun u v huv e => h.1 u v huv ((Equiv.swap a b).injective e), fun v => ?_⟩
  have hv := h.2 v
  simp only [Function.comp]
  by_cases ha : c v = a
  · rw [ha, Equiv.swap_apply_left]; exact (hsym v).1 (ha ▸ hv)
  by_cases hb : c v = b
  · rw [hb, Equiv.swap_apply_right]; exact (hsym v).2 (hb ▸ hv)
  rw [Equiv.swap_apply_of_ne_of_ne ha hb]; exact hv

theorem swap_mem_avail {G : SimpleGraph V} {L : V → Finset Color} {r : V} {a b : Color}
    (hsym : ∀ v, a ∈ L v ↔ b ∈ L v) {x : Color} (hx : x ∈ avail G L r) :
    Equiv.swap a b x ∈ avail G L r := by
  obtain ⟨c, hc, rfl⟩ := hx
  exact ⟨Equiv.swap a b ∘ c, listProper_swap hc hsym, rfl⟩

/-- The set of root colours is invariant under a list-symmetric swap. -/
theorem avail_swap_iff {G : SimpleGraph V} {L : V → Finset Color} {r : V} {a b : Color}
    (hsym : ∀ v, a ∈ L v ↔ b ∈ L v) (x : Color) :
    Equiv.swap a b x ∈ avail G L r ↔ x ∈ avail G L r :=
  ⟨fun h => by simpa using swap_mem_avail hsym h, swap_mem_avail hsym⟩

/-- A root forced to the single colour `a` cannot have `a` and `b` interchangeable on all lists
unless `a = b`. In the reports: a `c`-forcer with `c ≠ D` must contain a vertex whose list
lacks `c`, i.e. it touches a `c`-coloured boundary vertex. -/
theorem forced_eq_of_symmetric {G : SimpleGraph V} {L : V → Finset Color} {r : V} {a b : Color}
    (h : avail G L r = {a}) (hsym : ∀ v, a ∈ L v ↔ b ∈ L v) : a = b := by
  have ha : a ∈ avail G L r := h ▸ Set.mem_singleton a
  have hb := swap_mem_avail hsym ha
  rw [Equiv.swap_apply_left, h] at hb
  exact (Set.mem_singleton_iff.mp hb).symm

/-- Contrapositive form: a forced colour `a ≠ b` is witnessed by a vertex whose list separates
`a` from `b`. -/
theorem exists_asymmetric_of_forced {G : SimpleGraph V} {L : V → Finset Color} {r : V}
    {a b : Color} (h : avail G L r = {a}) (hab : a ≠ b) : ∃ v, ¬ (a ∈ L v ↔ b ∈ L v) := by
  by_contra hcon
  exact hab (forced_eq_of_symmetric h fun v => by_contra fun hv => hcon ⟨v, hv⟩)

/-! ### Forced palettes at a vertex -/

/-- Combinatorial core of `docs/c5_tree_cores.md` §2. `L` is the list of a vertex, `p i` the
colour forced by its `i`-th incident branch. Blocking (`hblock`: every list colour is forced by
some branch) and edge-minimality (`hmin`: deleting any one branch frees a list colour) make the
forced colours injective and exactly the list. -/
theorem forced_palettes {ι : Type*} (L : Finset Color) (p : ι → Color)
    (hblock : ∀ a ∈ L, ∃ i, p i = a)
    (hmin : ∀ i, ∃ a ∈ L, ∀ j, j ≠ i → p j ≠ a) :
    Function.Injective p ∧ (∀ i, p i ∈ L) ∧ Set.range p = ↑L := by
  have hmem : ∀ i, p i ∈ L := by
    intro i
    obtain ⟨a, ha, hother⟩ := hmin i
    obtain ⟨j, hj⟩ := hblock a ha
    by_cases hij : j = i
    · subst hij; exact hj ▸ ha
    · exact absurd hj (hother j hij)
  refine ⟨fun i j hij => ?_, hmem, ?_⟩
  · by_contra hne
    obtain ⟨a, ha, hother⟩ := hmin i
    obtain ⟨k, hk⟩ := hblock a ha
    by_cases hki : k = i
    · subst hki
      exact hother j (Ne.symm hne) (hij ▸ hk)
    · exact hother k hki hk
  · ext a
    constructor
    · rintro ⟨i, rfl⟩; exact hmem i
    · intro ha
      obtain ⟨i, hi⟩ := hblock a ha
      exact ⟨i, hi⟩

/-- With finitely many branches the number of branches is the size of the list. -/
theorem card_eq_of_forced_palettes {ι : Type*} [Fintype ι] (L : Finset Color) (p : ι → Color)
    (hblock : ∀ a ∈ L, ∃ i, p i = a)
    (hmin : ∀ i, ∃ a ∈ L, ∀ j, j ≠ i → p j ≠ a) :
    Fintype.card ι = #L := by
  obtain ⟨hinj, _, hrange⟩ := forced_palettes L p hblock hmin
  classical
  have : L = univ.image p := by
    ext a
    rw [mem_image]
    constructor
    · intro ha
      have ha' : a ∈ Set.range p := by rw [hrange]; exact mem_coe.mpr ha
      obtain ⟨i, hi⟩ := ha'
      exact ⟨i, mem_univ i, hi⟩
    · rintro ⟨i, _, rfl⟩
      have : p i ∈ Set.range p := Set.mem_range_self i
      rw [hrange] at this
      exact mem_coe.mp this
  rw [this, card_image_of_injective _ hinj, card_univ]

/-! ### Cycles with two-colour lists -/

/-- The cycle on `Fin (n+2)`, adjacency `j = i + 1 ∨ i = j + 1`; `cycleGraph 3 = C5`. -/
def cycleGraph (n : ℕ) : SimpleGraph (Fin (n + 2)) where
  Adj i j := j = i + 1 ∨ i = j + 1
  symm := ⟨fun _ _ h => h.elim Or.inr Or.inl⟩
  loopless := ⟨fun i h => by
    have h1 : (1 : Fin (n + 2)) = 0 := by
      rcases h with h | h <;> exact add_eq_left.mp h.symm
    rw [Fin.one_eq_zero_iff] at h1
    omega⟩

theorem cycleGraph_adj (n : ℕ) (i j : Fin (n + 2)) :
    (cycleGraph n).Adj i j ↔ j = i + 1 ∨ i = j + 1 := Iff.rfl

example : cycleGraph 3 = C5 := rfl

theorem val_add_one_of_ne_last {n : ℕ} {i : Fin (n + 2)} (h : i ≠ Fin.last (n + 1)) :
    (i + 1).val = i.val + 1 :=
  Fin.val_add_one_of_lt (Fin.lt_last_iff_ne_last.mpr h)

theorem mk_add_one {n k : ℕ} (hk : k + 1 < n + 2) :
    (⟨k + 1, hk⟩ : Fin (n + 2)) = ⟨k, by omega⟩ + 1 :=
  Fin.ext (by rw [Fin.val_add, Fin.val_one]; exact (Nat.mod_eq_of_lt hk).symm)

theorem zero_ne_last (n : ℕ) : (0 : Fin (n + 2)) ≠ Fin.last (n + 1) := by
  simp [Fin.ext_iff]

theorem last_add_add_one {n : ℕ} (i : Fin (n + 2)) : Fin.last (n + 1) + (i + 1) = i := by
  calc Fin.last (n + 1) + (i + 1) = i + (Fin.last (n + 1) + 1) := by abel
    _ = i := by rw [Fin.last_add_one, add_zero]

/-- Shifting all lists along the cycle does not change colourability. -/
theorem listColorable_of_shift {n : ℕ} {L : Fin (n + 2) → Finset Color} (s : Fin (n + 2))
    (h : ListColorable (cycleGraph n) fun i => L (i + s)) : ListColorable (cycleGraph n) L := by
  obtain ⟨c, hc, hL⟩ := h
  refine ⟨fun i => c (i - s), fun i j hij => hc _ _ ?_, fun i => by simpa using hL (i - s)⟩
  rcases hij with rfl | rfl
  · left; abel
  · right; abel

/-- Reflecting the cycle (`i ↦ -i - 1`) does not change colourability. -/
theorem listColorable_of_reflect {n : ℕ} {L : Fin (n + 2) → Finset Color}
    (h : ListColorable (cycleGraph n) fun i => L (-i - 1)) : ListColorable (cycleGraph n) L := by
  obtain ⟨c, hc, hL⟩ := h
  refine ⟨fun i => c (-i - 1), fun i j hij => hc _ _ ?_, fun i => ?_⟩
  · rcases hij with rfl | rfl
    · right; abel
    · left; abel
  · have := hL (-i - 1)
    simpa [show -(-i - 1) - 1 = i by abel] using this

/-- Greedy colouring along `ℕ`: start with `x`, then always pick a list colour different from
the previous one. -/
noncomputable def greedy (M : ℕ → Finset Color) (hM : ∀ k, 2 ≤ #(M k)) (x : Color) :
    ℕ → Color
  | 0 => x
  | k + 1 => Classical.choose (exists_mem_ne (hM (k + 1)) (greedy M hM x k))

theorem greedy_zero (M : ℕ → Finset Color) (hM : ∀ k, 2 ≤ #(M k)) (x : Color) :
    greedy M hM x 0 = x := rfl

theorem greedy_succ_mem (M : ℕ → Finset Color) (hM : ∀ k, 2 ≤ #(M k)) (x : Color) (k : ℕ) :
    greedy M hM x (k + 1) ∈ M (k + 1) :=
  (Classical.choose_spec (exists_mem_ne (hM (k + 1)) (greedy M hM x k))).1

theorem greedy_succ_ne (M : ℕ → Finset Color) (hM : ∀ k, 2 ≤ #(M k)) (x : Color) (k : ℕ) :
    greedy M hM x (k + 1) ≠ greedy M hM x k :=
  (Classical.choose_spec (exists_mem_ne (hM (k + 1)) (greedy M hM x k))).2

/-- Core greedy lemma: colour `0` with `x`, walk up to `n`, and close at the last vertex, which
must be able to avoid `x` and one more colour. -/
theorem listColorable_of_last_free {n : ℕ} (L : Fin (n + 2) → Finset Color)
    (h2 : ∀ i, 2 ≤ #(L i)) {x : Color} (hx : x ∈ L 0)
    (hlast : ∀ z, ∃ y ∈ L (Fin.last (n + 1)), y ≠ z ∧ y ≠ x) :
    ListColorable (cycleGraph n) L := by
  classical
  let M : ℕ → Finset Color := fun k => L ⟨k % (n + 2), Nat.mod_lt _ (by omega)⟩
  have hM : ∀ k, 2 ≤ #(M k) := fun k => h2 _
  have hMval : ∀ i : Fin (n + 2), M i.val = L i := fun i => by
    simp only [M]
    congr 1
    exact Fin.ext (Nat.mod_eq_of_lt i.isLt)
  obtain ⟨y, hyL, hy1, hy2⟩ := hlast (greedy M hM x n)
  refine ⟨fun i => if i = Fin.last (n + 1) then y else greedy M hM x i.val, ?_, ?_⟩
  · suffices key : ∀ i j : Fin (n + 2), j = i + 1 →
        (if i = Fin.last (n + 1) then y else greedy M hM x i.val) ≠
          (if j = Fin.last (n + 1) then y else greedy M hM x j.val) by
      intro i j hij
      rcases hij with h | h
      · exact key i j h
      · exact (key j i h).symm
    intro i j hj
    by_cases hi : i = Fin.last (n + 1)
    · subst hi
      rw [Fin.last_add_one] at hj
      subst hj
      simp only [ite_true, zero_ne_last, ite_false, Fin.val_zero, greedy_zero]
      exact hy2
    · simp only [hi, ite_false]
      by_cases hj' : j = Fin.last (n + 1)
      · simp only [hj', ite_true]
        have hval : i.val = n := by
          have := val_add_one_of_ne_last hi
          rw [← hj, hj', Fin.val_last] at this
          omega
        rw [hval]
        exact hy1.symm
      · simp only [hj', ite_false]
        have hval : j.val = i.val + 1 := by rw [hj]; exact val_add_one_of_ne_last hi
        rw [hval]
        exact (greedy_succ_ne M hM x i.val).symm
  · intro i
    by_cases hi : i = Fin.last (n + 1)
    · simp only [hi, ite_true]; exact hyL
    · simp only [hi, ite_false]
      rw [← hMval i]
      rcases hk : i.val with _ | k
      · rw [greedy_zero]
        have : i = 0 := Fin.ext hk
        subst this
        exact hx
      · exact greedy_succ_mem M hM x k

/-- If some list has at least three colours (all at least two), the cycle is colourable. -/
theorem cycle_colorable_of_three {n : ℕ} (L : Fin (n + 2) → Finset Color)
    (h2 : ∀ i, 2 ≤ #(L i)) (h3 : ∃ i, 3 ≤ #(L i)) : ListColorable (cycleGraph n) L := by
  classical
  obtain ⟨i, hi⟩ := h3
  apply listColorable_of_shift (i + 1)
  obtain ⟨x, hx⟩ : (L (0 + (i + 1))).Nonempty :=
    card_pos.mp (by have := h2 (0 + (i + 1)); omega : 0 < #(L (0 + (i + 1))))
  refine listColorable_of_last_free _ (fun j => h2 _) hx fun z => ?_
  simp only [last_add_add_one]
  have hcard : 1 ≤ #(L i \ {z, x}) := by
    have h1 := le_card_sdiff {z, x} (L i)
    have h2' : #({z, x} : Finset Color) ≤ 2 := (card_insert_le z {x}).trans (by simp)
    omega
  obtain ⟨y, hy⟩ := card_pos.mp hcard
  rw [mem_sdiff, mem_insert, mem_singleton] at hy
  exact ⟨y, hy.1, fun h => hy.2 (Or.inl h), fun h => hy.2 (Or.inr h)⟩

/-- Two-colour lists that differ across some edge: colourable. -/
theorem cycle_colorable_of_notMem_pred {n : ℕ} (L : Fin (n + 2) → Finset Color)
    (h2 : ∀ i, 2 ≤ #(L i)) (h : ∃ i, ∃ x ∈ L (i + 1), x ∉ L i) :
    ListColorable (cycleGraph n) L := by
  obtain ⟨i, x, hx1, hx2⟩ := h
  apply listColorable_of_shift (i + 1)
  refine listColorable_of_last_free _ (fun j => h2 _) (by simpa using hx1) fun z => ?_
  simp only [last_add_add_one]
  obtain ⟨y, hy, hyz⟩ := exists_mem_ne (s := L i) (by have := h2 i; omega) z
  exact ⟨y, hy, hyz, fun e => hx2 (e ▸ hy)⟩

theorem cycle_colorable_of_notMem_succ {n : ℕ} (L : Fin (n + 2) → Finset Color)
    (h2 : ∀ i, 2 ≤ #(L i)) (h : ∃ i, ∃ x ∈ L i, x ∉ L (i + 1)) :
    ListColorable (cycleGraph n) L := by
  obtain ⟨i, x, hx1, hx2⟩ := h
  apply listColorable_of_reflect
  refine cycle_colorable_of_notMem_pred _ (fun j => h2 _) ⟨-i - 1 - 1, x, ?_, ?_⟩
  · simpa [show -(-i - 1 - 1 + 1) - 1 = i by abel] using hx1
  · rw [show -(-i - 1 - 1) - 1 = i + 1 by abel]; exact hx2

/-- Two-colour lists that are not all equal along the cycle: colourable
(`docs/c5_pentagon_branches.md` §1). -/
theorem cycle_colorable_of_lists_ne {n : ℕ} (L : Fin (n + 2) → Finset Color)
    (h2 : ∀ i, #(L i) = 2) (h : ∃ i, L i ≠ L (i + 1)) : ListColorable (cycleGraph n) L := by
  obtain ⟨i, hi⟩ := h
  by_cases hsub : L i ⊆ L (i + 1)
  · exact absurd (eq_of_subset_of_card_le hsub (by rw [h2, h2])) hi
  · obtain ⟨x, hx1, hx2⟩ := not_subset.mp hsub
    exact cycle_colorable_of_notMem_succ L (fun j => (h2 j).ge) ⟨i, x, hx1, hx2⟩

/-- Two-element pigeonhole along an edge of a `{a,b}`-coloured walk. -/
theorem pair_step {a b x y z : Color} (hab : a ≠ b) (hx : x = a ∨ x = b) (hy : y = a ∨ y = b)
    (hz : z = a ∨ z = b) (hxy : x ≠ y) : x = z ↔ ¬ y = z := by
  rcases hx with rfl | rfl <;> rcases hy with rfl | rfl <;> rcases hz with rfl | rfl <;>
    simp_all [eq_comm]

/-- An odd cycle whose lists are all the same pair is not colourable. -/
theorem odd_cycle_common_uncolorable {n : ℕ} (hodd : Odd (n + 2)) {L : Fin (n + 2) → Finset Color}
    {a b : Color} (hab : a ≠ b) (hL : ∀ i, L i = {a, b}) :
    ¬ ListColorable (cycleGraph n) L := by
  rintro ⟨c, hc, hLc⟩
  have hmem : ∀ i, c i = a ∨ c i = b := fun i => by
    have := hLc i
    rw [hL i, mem_insert, mem_singleton] at this
    exact this
  have key : ∀ k (hk : k < n + 2), c ⟨k, hk⟩ = c 0 ↔ Even k := by
    intro k
    induction k with
    | zero => intro hk; simp
    | succ k ih =>
      intro hk
      have hadj : (cycleGraph n).Adj ⟨k, by omega⟩ ⟨k + 1, hk⟩ := Or.inl (mk_add_one hk)
      rw [Nat.even_add_one, ← ih (by omega)]
      exact pair_step hab (hmem _) (hmem _) (hmem 0) (hc _ _ hadj).symm
  have heven : Even (n + 1) := by
    rcases hodd with ⟨m, hm⟩
    exact ⟨m, by omega⟩
  have hlast := (key (n + 1) (by omega)).mpr heven
  have hadj : (cycleGraph n).Adj 0 (Fin.last (n + 1)) := Or.inr (Fin.last_add_one (n + 1)).symm
  exact hc _ _ hadj hlast.symm

/-- An even cycle whose lists are all the same pair is colourable by alternating. -/
theorem even_cycle_common_colorable {n : ℕ} (heven : Even (n + 2))
    {L : Fin (n + 2) → Finset Color} {a b : Color} (hab : a ≠ b) (hL : ∀ i, L i = {a, b}) :
    ListColorable (cycleGraph n) L := by
  classical
  refine ⟨fun i => if Even i.val then a else b, ?_, fun i => by
    rw [hL i]; by_cases h : Even i.val <;> simp [h]⟩
  suffices key : ∀ i j : Fin (n + 2), j = i + 1 →
      (if Even i.val then a else b) ≠ (if Even j.val then a else b) by
    intro i j hij
    rcases hij with h | h
    · exact key i j h
    · exact (key j i h).symm
  intro i j hj
  by_cases hi : i = Fin.last (n + 1)
  · subst hi
    rw [Fin.last_add_one] at hj
    subst hj
    have hodd : ¬ Even (n + 1) := by
      rcases heven with ⟨m, hm⟩
      rintro ⟨r, hr⟩
      omega
    have h0 : Even (0 : ℕ) := ⟨0, rfl⟩
    simp only [Fin.val_last, Fin.val_zero, hodd, ite_false, h0, ite_true]
    exact hab.symm
  · have hval : j.val = i.val + 1 := by rw [hj]; exact val_add_one_of_ne_last hi
    rw [hval]
    by_cases he : Even i.val
    · have hne : ¬ Even (i.val + 1) := Nat.even_add_one.not.mpr (not_not.mpr he)
      simp only [he, hne, ite_true, ite_false]; exact hab
    · have hne : Even (i.val + 1) := Nat.even_add_one.mpr he
      simp only [he, hne, ite_true, ite_false]; exact hab.symm

theorem lists_eq_zero_of_consecutive {n : ℕ} {L : Fin (n + 2) → Finset Color}
    (h : ∀ i, L i = L (i + 1)) : ∀ i, L i = L 0 := by
  have key : ∀ k (hk : k < n + 2), L ⟨k, hk⟩ = L 0 := by
    intro k
    induction k with
    | zero => intro hk; rfl
    | succ k ih => intro hk; rw [mk_add_one hk, ← h, ih]
  intro i
  exact key i.val i.isLt

/-- **Cycle with two-colour lists**: uncolourable iff the cycle is odd and every list is the
same pair (`docs/c5_pentagon_branches.md` §1, §4). -/
theorem cycle_two_lists_uncolorable_iff {n : ℕ} (L : Fin (n + 2) → Finset Color)
    (h2 : ∀ i, #(L i) = 2) :
    ¬ ListColorable (cycleGraph n) L ↔ Odd (n + 2) ∧ ∀ i, L i = L 0 := by
  constructor
  · intro hnot
    have hall : ∀ i, L i = L 0 := by
      by_contra hne
      have : ∃ i, L i ≠ L (i + 1) := by
        by_contra h
        exact hne (lists_eq_zero_of_consecutive fun i => by_contra fun h' => h ⟨i, h'⟩)
      exact hnot (cycle_colorable_of_lists_ne L h2 this)
    refine ⟨?_, hall⟩
    rcases Nat.even_or_odd (n + 2) with heven | hodd
    · exfalso
      obtain ⟨a, b, hab, hab'⟩ := card_eq_two.mp (h2 0)
      exact hnot (even_cycle_common_colorable heven hab fun i => (hall i).trans hab')
    · exact hodd
  · rintro ⟨hodd, hall⟩
    obtain ⟨a, b, hab, hab'⟩ := card_eq_two.mp (h2 0)
    exact odd_cycle_common_uncolorable hodd hab fun i => (hall i).trans hab'

/-- Same statement for lists of size at least two: uncolourable iff odd and all lists are one
common pair. -/
theorem cycle_uncolorable_iff {n : ℕ} (L : Fin (n + 2) → Finset Color)
    (h2 : ∀ i, 2 ≤ #(L i)) :
    ¬ ListColorable (cycleGraph n) L ↔ Odd (n + 2) ∧ ∃ P, #P = 2 ∧ ∀ i, L i = P := by
  constructor
  · intro hnot
    have hcard : ∀ i, #(L i) = 2 := by
      intro i
      by_contra h
      exact hnot (cycle_colorable_of_three L h2 ⟨i, by have := h2 i; omega⟩)
    obtain ⟨hodd, hall⟩ := (cycle_two_lists_uncolorable_iff L hcard).mp hnot
    exact ⟨hodd, L 0, hcard 0, hall⟩
  · rintro ⟨hodd, P, hP, hall⟩
    have hcard : ∀ i, #(L i) = 2 := fun i => (hall i).symm ▸ hP
    exact (cycle_two_lists_uncolorable_iff L hcard).mpr
      ⟨hodd, fun i => (hall i).trans (hall 0).symm⟩

/-- The boundary pentagon itself: two-colour lists on `C5` are uncolourable iff all five lists
coincide (the six rejected configurations of the `6^5` check in
`docs/c5_pentagon_branches.md` §1). -/
theorem c5_two_lists_uncolorable_iff (L : Fin 5 → Finset Color) (h2 : ∀ i, #(L i) = 2) :
    ¬ ListColorable C5 L ↔ ∀ i, L i = L 0 := by
  rw [show C5 = cycleGraph 3 from rfl, cycle_two_lists_uncolorable_iff L h2]
  exact ⟨fun h => h.2, fun h => ⟨⟨2, rfl⟩, h⟩⟩

/-! ### Triangle instances -/

/-- A triangle with three two-colour lists is uncolourable iff all three lists coincide
(`docs/c5_shared_triangle_blocks.md` §2). -/
theorem triangle_two_lists_uncolorable_iff (L : Fin 3 → Finset Color) (h2 : ∀ i, #(L i) = 2) :
    ¬ ListColorable (cycleGraph 1) L ↔ L 1 = L 0 ∧ L 2 = L 0 := by
  rw [cycle_two_lists_uncolorable_iff L h2]
  constructor
  · rintro ⟨_, h⟩; exact ⟨h 1, h 2⟩
  · rintro ⟨h1, h2⟩
    refine ⟨⟨1, rfl⟩, fun i => ?_⟩
    fin_cases i <;> simp [h1, h2]

/-- Interface of the shared-cut-vertex chain: the middle triangle with lists `univ \ P`,
`univ \ Q`, `R` (all pairs) is uncolourable iff `P = Q = univ \ R`. -/
theorem shared_chain_interface (P Q R : Finset Color) (hP : #P = 2) (hQ : #Q = 2)
    (hR : #R = 2) :
    ¬ ListColorable (cycleGraph 1) ![univ \ P, univ \ Q, R] ↔ P = Q ∧ P = univ \ R := by
  have hc : ∀ S : Finset Color, #S = 2 → #(univ \ S) = 2 := by
    intro S hS
    rw [← compl_eq_univ_sdiff, card_compl, hS]
    simp
  rw [triangle_two_lists_uncolorable_iff _ (by
    intro i; fin_cases i <;> simp [hc P hP, hc Q hQ, hR])]
  simp only [Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.cons_val_two,
    ← compl_eq_univ_sdiff, compl_inj_iff]
  constructor
  · rintro ⟨h1, h2⟩; exact ⟨h1.symm, eq_compl_comm.mp h2⟩
  · rintro ⟨h1, h2⟩; exact ⟨h1.symm, eq_compl_comm.mp h2⟩

/-- 36-case forbidden-colour rule of a triangle apex (`docs/c5_two_triangle_blocks.md` §3):
with two-colour lists `La`, `Lb` on the other two vertices, the apex colour `x` extends iff it
is not the case that `La = Lb` and `x ∈ La`. -/
theorem apex_extension_iff (La Lb : Finset Color) (ha : #La = 2) (hb : #Lb = 2) (x : Color) :
    (∃ a ∈ La, ∃ b ∈ Lb, a ≠ x ∧ b ≠ x ∧ a ≠ b) ↔ ¬ (La = Lb ∧ x ∈ La) := by
  constructor
  · rintro ⟨a, ha', b, hb', hax, hbx, hab⟩ ⟨rfl, hx⟩
    obtain ⟨p, q, hpq, rfl⟩ := card_eq_two.mp ha
    simp only [mem_insert, mem_singleton] at ha' hb' hx
    rcases ha' with rfl | rfl <;> rcases hb' with rfl | rfl <;> rcases hx with rfl | rfl <;>
      simp_all
  · intro h
    by_cases heq : La = Lb
    · subst heq
      have hx : x ∉ La := fun hx => h ⟨rfl, hx⟩
      obtain ⟨p, q, hpq, rfl⟩ := card_eq_two.mp ha
      simp only [mem_insert, mem_singleton, not_or] at hx
      exact ⟨p, by simp, q, by simp, Ne.symm hx.1, Ne.symm hx.2, hpq⟩
    · by_contra hcon'
      have hcon : ∀ a ∈ La, ∀ b ∈ Lb, a ≠ x → b ≠ x → b = a :=
        fun a ha b hb hax hbx => by_contra fun hne => hcon' ⟨a, ha, b, hb, hax, hbx, Ne.symm hne⟩
      obtain ⟨a0, ha0, ha0x⟩ := exists_mem_ne (by omega : 1 < #La) x
      obtain ⟨b0, hb0, hb0x⟩ := exists_mem_ne (by omega : 1 < #Lb) x
      have hb0a : b0 = a0 := hcon a0 ha0 b0 hb0 ha0x hb0x
      have hLa : La = {x, a0} := by
        refine eq_of_subset_of_card_le (fun c hc => ?_)
          (by rw [ha]; exact (card_insert_le _ _).trans (by simp))
        rw [mem_insert, mem_singleton]
        by_cases hcx : c = x
        · exact Or.inl hcx
        · exact Or.inr ((hcon c hc b0 hb0 hcx hb0x).symm.trans hb0a)
      have hLb : Lb = {x, a0} := by
        refine eq_of_subset_of_card_le (fun d hd => ?_)
          (by rw [hb]; exact (card_insert_le _ _).trans (by simp))
        rw [mem_insert, mem_singleton]
        by_cases hdx : d = x
        · exact Or.inl hdx
        · exact Or.inr (hcon a0 ha0 d hd ha0x hdx)
      exact heq (hLa.trans hLb.symm)

/-- The forbidden apex colours are the common list when the two lists agree, nothing otherwise. -/
theorem apex_forbidden_eq (La Lb : Finset Color) (ha : #La = 2) (hb : #Lb = 2) :
    {x | ¬ ∃ a ∈ La, ∃ b ∈ Lb, a ≠ x ∧ b ≠ x ∧ a ≠ b} =
      if La = Lb then (↑La : Set Color) else ∅ := by
  ext x
  change (¬ ∃ a ∈ La, ∃ b ∈ Lb, a ≠ x ∧ b ≠ x ∧ a ≠ b) ↔ _
  rw [apex_extension_iff La Lb ha hb x, not_not]
  split_ifs with h <;> simp [h]

end FiveBoundary.ForcingLists
