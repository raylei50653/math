/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.RootInterfaces

/-! Reusable proof tools for the two-rejection paper. These do not assert the
Gallai decomposition, the bridge-chain extraction, or any disk embedding theorem. -/
namespace FiveBoundary.TwoRejectionTools

open Finset ForcingLists RootInterfaces

variable {V : Type*}

/-- Greedy list colouring from a removable vertex in every nonempty induced subset.
The hypothesis can be supplied by a rooted spanning-tree order. -/
theorem listColorable_of_removable [Finite V] (G : SimpleGraph V)
    [DecidableRel G.Adj] (L : V → Finset Color)
    (hremove : ∀ S : Finset V, S.Nonempty →
      ∃ v ∈ S, (S.filter (G.Adj v)).card < (L v).card) :
    ListColorable G L := by
  classical
  let := Fintype.ofFinite V
  have build : ∀ S : Finset V, ∃ c : V → Color,
      (∀ v ∈ S, c v ∈ L v) ∧
      (∀ u ∈ S, ∀ v ∈ S, G.Adj u v → c u ≠ c v) := by
    intro S
    induction S using Finset.strongInductionOn with
    | _ S ih =>
      by_cases hS : S.Nonempty
      · obtain ⟨v, hv, hcard⟩ := hremove S hS
        obtain ⟨c, hcL, hcG⟩ := ih (S.erase v) (erase_ssubset hv)
        let forbidden := ((S.erase v).filter (G.Adj v)).image c
        have hsmall : forbidden.card < (L v).card := by
          calc
            forbidden.card ≤ ((S.erase v).filter (G.Adj v)).card := card_image_le
            _ ≤ (S.filter (G.Adj v)).card :=
              card_le_card (filter_subset_filter _ (erase_subset _ _))
            _ < (L v).card := hcard
        obtain ⟨a, ha, haf⟩ : ∃ a ∈ L v, a ∉ forbidden := by
          by_contra h
          have hsub : L v ⊆ forbidden := by
            intro x hx
            by_contra hxf
            exact h ⟨x, hx, hxf⟩
          have := card_le_card hsub
          omega
        have hne : ∀ w ∈ S.erase v, G.Adj v w → a ≠ c w := by
          intro w hw hvw heq
          apply haf
          exact mem_image.mpr ⟨w, mem_filter.mpr ⟨hw, hvw⟩, heq.symm⟩
        refine ⟨Function.update c v a, ?_, ?_⟩
        · intro w hw
          by_cases hwv : w = v
          · subst w; simpa using ha
          · simpa [Function.update, hwv] using hcL w (mem_erase.mpr ⟨hwv, hw⟩)
        · intro u hu w hw huw
          by_cases huv : u = v <;> by_cases hwv : w = v
          · subst u; subst w; exact (G.irrefl huw).elim
          · subst u
            simpa [Function.update, hwv] using hne w (mem_erase.mpr ⟨hwv, hw⟩) huw
          · subst w
            simpa [Function.update, huv] using (hne u (mem_erase.mpr ⟨huv, hu⟩) huw.symm).symm
          · simpa [Function.update, huv, hwv] using
              hcG u (mem_erase.mpr ⟨huv, hu⟩) w (mem_erase.mpr ⟨hwv, hw⟩) huw
      · refine ⟨fun _ => 0, ?_, ?_⟩ <;> simp_all
  obtain ⟨c, hcL, hcG⟩ := build univ
  exact ⟨c, fun u v h => hcG u (mem_univ _) v (mem_univ _) h,
    fun v => hcL v (mem_univ _)⟩

/-- In a connected graph, degree-sized lists and one strict surplus suffice.
This proves the spanning-tree greedy step without an external degree-list theorem. -/
theorem listColorable_of_connected_slack [Fintype V] (G : SimpleGraph V)
    [DecidableRel G.Adj] (L : V → Finset Color) (hconn : G.Connected)
    (hdegree : ∀ v, (univ.filter (G.Adj v)).card ≤ (L v).card)
    (r : V) (hslack : (univ.filter (G.Adj r)).card < (L r).card) :
    ListColorable G L := by
  classical
  apply listColorable_of_removable
  intro S hS
  by_cases hr : r ∈ S
  · exact ⟨r, hr, lt_of_le_of_lt (card_le_card (filter_subset_filter _ (subset_univ _))) hslack⟩
  · have hcross : ∃ v ∈ S, ∃ w, w ∉ S ∧ G.Adj v w := by
      by_contra h
      have closed : ∀ v ∈ S, ∀ w, G.Adj v w → w ∈ S := by
        intro v hv w hvw
        by_contra hw
        exact h ⟨v, hv, w, hw, hvw⟩
      obtain ⟨v, hv⟩ := hS
      obtain ⟨p⟩ := hconn.preconnected v r
      have propagate : ∀ {x y}, G.Walk x y → x ∈ S → y ∈ S := by
        intro x y walk
        induction walk with
        | nil => exact id
        | cons hxy _ ih => exact fun hx => ih (closed _ hx _ hxy)
      exact hr (propagate p hv)
    obtain ⟨v, hv, w, hw, hvw⟩ := hcross
    refine ⟨v, hv, lt_of_lt_of_le ?_ (hdegree v)⟩
    apply card_lt_card
    refine Finset.ssubset_iff_subset_ne.mpr ⟨filter_subset_filter _ (subset_univ _), ?_⟩
    intro heq
    have : w ∈ S.filter (G.Adj v) := heq.symm ▸ mem_filter.mpr ⟨mem_univ _, hvw⟩
    exact hw (mem_filter.mp this).1

/-- Rejection in a connected degree-list instance forces every list to be tight. -/
theorem lists_tight_of_rejection [Fintype V] (G : SimpleGraph V)
    [DecidableRel G.Adj] (L : V → Finset Color) (hconn : G.Connected)
    (hdegree : ∀ v, (univ.filter (G.Adj v)).card ≤ (L v).card)
    (hreject : ¬ ListColorable G L) :
    ∀ v, (L v).card = (univ.filter (G.Adj v)).card := by
  intro v
  apply Nat.le_antisymm _ (hdegree v)
  by_contra h
  exact hreject (listColorable_of_connected_slack G L hconn hdegree v (by omega))

/-- The numerical tightness step once rejection has excluded strict list slack.
`imageSize` is the number of distinct boundary colours; `attachments` counts actual neighbours. -/
theorem tight_of_no_slack (degree attachments imageSize listSize : ℕ)
    (hdegree : degree + attachments ≤ 4) (himage : imageSize ≤ attachments)
    (hlist : listSize + imageSize = 4) (hno : listSize ≤ degree) :
    degree + attachments = 4 ∧ listSize = degree ∧ imageSize = attachments := by
  omega

/-- Arithmetic core of the two-port forest argument. Each nonempty tree component
contributes two ports plus the sum of block-size excesses. Forest construction and
that identity must be proved separately for the actual block-cut tree. -/
theorem two_port_count {ι : Type*} (S : Finset ι) (excess : ι → ℕ)
    (hne : S.Nonempty) (hports : 2 * S.card + ∑ i ∈ S, excess i = 2) :
    S.card = 1 ∧ ∀ i ∈ S, excess i = 0 := by
  have hpos := card_pos.mpr hne
  have hcard : S.card = 1 := by omega
  refine ⟨hcard, ?_⟩
  have hz : ∑ i ∈ S, excess i = 0 := by omega
  exact (sum_eq_zero_iff).mp hz

/-- Ordered attachment intervals telescope, independently of the disk argument
that supplies their order. -/
theorem interval_width_sum (lo hi : ℕ → ℕ) (n : ℕ)
    (hvalid : ∀ i < n + 1, lo i ≤ hi i)
    (horder : ∀ i < n, hi i ≤ lo (i + 1)) :
    (∑ i ∈ range (n + 1), (hi i - lo i)) + lo 0 ≤ hi n := by
  induction n with
  | zero => simp; have := hvalid 0 (by omega); omega
  | succ n ih =>
    have hprev := ih (fun i hi => hvalid i (by omega))
      (fun i hi => horder i (by omega))
    rw [sum_range_succ]
    have := hvalid (n + 1) (by omega)
    have := horder n (by omega)
    omega

/-- The paper's two final path-length deductions, with their width/parity inputs explicit. -/
theorem path_size_bounds (n : ℕ) (hmin : 2 ≤ n) :
    (n - 1 + 2 ≤ 3 → n = 2) ∧ (n ≤ 3 → Even n → n = 2) := by
  constructor
  · omega
  · rintro h ⟨k, hk⟩; omega

/-- A colourable fixed core cannot reject two different singleton leaf colours.
Both tests use precisely the same graph, lists and root, and core nonemptiness is essential. -/
theorem not_two_singleton_rejections (G : SimpleGraph V) (L : V → Finset Color)
    (r : V) (a b : Color) (hab : a ≠ b) (hcol : ListColorable G L) :
    ¬ (a ∈ forbidden (contactRelation G L (fun _ : Unit => r)) ∧
       b ∈ forbidden (contactRelation G L (fun _ : Unit => r))) := by
  rintro ⟨ha, hb⟩
  obtain ⟨c, hc⟩ := hcol
  have hroot : c r ∈ avail G L r := ⟨c, hc, rfl⟩
  have hca : c r = a := (mem_forbidden_single_iff G L r a).mp ha hroot
  have hcb : c r = b := (mem_forbidden_single_iff G L r b).mp hb hroot
  exact hab (hca.symm.trans hcb)

/-- Boundary rows that agree on every actual attachment yield identical lists.
No identification of named boundary vertices is made. -/
theorem boundary_lists_eq {B : Type*} (A : V → Finset B) (q q' : B → Color)
    (h : ∀ v, ∀ b ∈ A v, q b = q' b) :
    (fun v => (univ : Finset Color) \ (A v).image q) =
      (fun v => (univ : Finset Color) \ (A v).image q') := by
  classical
  funext v
  rw [Finset.image_congr (h v)]

end FiveBoundary.TwoRejectionTools
