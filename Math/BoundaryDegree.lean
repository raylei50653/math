/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.TwoRejectionTools

/-! Actual boundary attachments, extension semantics and degree-list tightness.

The vertices of the source graph are partitioned as `B ⊕ V`: named boundary
vertices and interior vertices. All attachments and degrees are read from that
same graph. No cycle, embedding, minimality or Gallai decomposition is assumed.
-/
namespace FiveBoundary.BoundaryDegree

open Finset ForcingLists TwoRejectionTools

variable {B V : Type*}

/-- The actual graph induced by the interior vertices. -/
def interiorGraph (G : SimpleGraph (B ⊕ V)) : SimpleGraph V := G.comap Sum.inr

/-- A fixed boundary row respects every actual boundary edge, including chords. -/
def BoundaryProper (G : SimpleGraph (B ⊕ V)) (q : B → Color) : Prop :=
  ∀ b b', G.Adj (Sum.inl b) (Sum.inl b') → q b ≠ q b'

/-- A proper colouring of the whole source graph extending the named boundary row. -/
def Extends (G : SimpleGraph (B ⊕ V)) (q : B → Color) : Prop :=
  ∃ c : B ⊕ V → Color,
    (∀ x y, G.Adj x y → c x ≠ c y) ∧ ∀ b, c (Sum.inl b) = q b

variable [Fintype B] (G : SimpleGraph (B ⊕ V)) [DecidableRel G.Adj]

instance : DecidableRel (interiorGraph G).Adj :=
  inferInstanceAs (DecidableRel (G.comap Sum.inr).Adj)

/-- Actual boundary neighbours, without identifying equally coloured vertices. -/
def attachments (v : V) : Finset B := univ.filter (fun b => G.Adj (Sum.inr v) (Sum.inl b))

/-- Colours left after imposing the fixed colours of all actual boundary neighbours. -/
def lists (q : B → Color) (v : V) : Finset Color := univ \ (attachments G v).image q

@[simp] theorem mem_attachments (v : V) (b : B) :
    b ∈ attachments G v ↔ G.Adj (Sum.inr v) (Sum.inl b) := by
  simp [attachments]

theorem mem_lists_iff (q : B → Color) (v : V) (a : Color) :
    a ∈ lists G q v ↔ ∀ b, G.Adj (Sum.inr v) (Sum.inl b) → a ≠ q b := by
  simp [lists, ne_comm]

/-- One interior colouring supplies all contacts at once. -/
theorem proper_sum_iff (q : B → Color) (c : V → Color) :
    (∀ x y, G.Adj x y → Sum.elim q c x ≠ Sum.elim q c y) ↔
      BoundaryProper G q ∧ ListProper (interiorGraph G) (lists G q) c := by
  constructor
  · intro h
    refine ⟨fun b b' hb => h _ _ hb, fun v w hvw => h _ _ hvw, ?_⟩
    intro v
    exact (mem_lists_iff G q v (c v)).mpr (fun b hb => h _ _ hb)
  · rintro ⟨hq, hc, hL⟩ x y hxy
    cases x with
    | inl b =>
      cases y with
      | inl b' => exact hq b b' hxy
      | inr v => exact ((mem_lists_iff G q v (c v)).mp (hL v) b hxy.symm).symm
    | inr v =>
      cases y with
      | inl b => exact (mem_lists_iff G q v (c v)).mp (hL v) b hxy
      | inr w => exact hc v w hxy

/-- Exact graph/list correspondence; boundary properness is a separate necessary condition. -/
theorem extends_iff (q : B → Color) :
    Extends G q ↔ BoundaryProper G q ∧ ListColorable (interiorGraph G) (lists G q) := by
  constructor
  · rintro ⟨c, hc, hq⟩
    have heq : Sum.elim q (fun v => c (Sum.inr v)) = c := by
      funext x
      cases x with
      | inl b => exact (hq b).symm
      | inr v => rfl
    have h := (proper_sum_iff G q (fun v => c (Sum.inr v))).mp (by rwa [heq])
    exact ⟨h.1, _, h.2⟩
  · rintro ⟨hq, c, hc⟩
    exact ⟨Sum.elim q c, (proper_sum_iff G q c).mpr ⟨hq, hc⟩, fun _ => rfl⟩

/-- The list and the distinct boundary colours partition the four-colour universe. -/
theorem card_lists_add_image (q : B → Color) (v : V) :
    (lists G q v).card + ((attachments G v).image q).card = 4 := by
  simpa [lists, Color] using
    card_sdiff_add_card_eq_card (subset_univ ((attachments G v).image q))

variable [Fintype V]

/-- The complete degree splits into actual interior and boundary neighbours. -/
theorem degree_split (v : V) :
    G.degree (Sum.inr v) = (interiorGraph G).degree v + (attachments G v).card := by
  classical
  have h : G.neighborFinset (Sum.inr v) =
      (attachments G v).disjSum ((interiorGraph G).neighborFinset v) := by
    ext x
    cases x with
    | inl b => simp
    | inr w =>
      simp only [SimpleGraph.mem_neighborFinset, inr_mem_disjSum]
      rfl
  rw [← SimpleGraph.card_neighborFinset_eq_degree, h, card_disjSum]
  simp [Nat.add_comm]

/-- Complete degree at most four supplies the degree-list premise automatically. -/
theorem degree_le_card_lists (q : B → Color)
    (hdegree : ∀ v, G.degree (Sum.inr v) ≤ 4) (v : V) :
    (interiorGraph G).degree v ≤ (lists G q v).card := by
  have hdeg := hdegree v
  rw [degree_split G v] at hdeg
  have himage : ((attachments G v).image q).card ≤ (attachments G v).card := card_image_le
  have hlist := card_lists_add_image G q v
  omega

/-- Rejection forces full degree four, tight interior lists, and injectivity on
each vertex's actual boundary neighbours. The boundary row need not be proper. -/
theorem tight_of_rejection (q : B → Color)
    (hconn : (interiorGraph G).Connected)
    (hdegree : ∀ v, G.degree (Sum.inr v) ≤ 4)
    (hreject : ¬ ListColorable (interiorGraph G) (lists G q)) :
    ∀ v, G.degree (Sum.inr v) = 4 ∧
      (lists G q v).card = (interiorGraph G).degree v ∧
      Set.InjOn q (attachments G v) := by
  classical
  have htight := lists_tight_of_rejection (interiorGraph G) (lists G q) hconn
    (fun v => by simpa [SimpleGraph.degree, SimpleGraph.neighborFinset_eq_filter] using
      degree_le_card_lists G q hdegree v) hreject
  intro v
  have ht : (lists G q v).card = (interiorGraph G).degree v := by
    simpa [SimpleGraph.degree, SimpleGraph.neighborFinset_eq_filter] using htight v
  have hn := tight_of_no_slack ((interiorGraph G).degree v) (attachments G v).card
    ((attachments G v).image q).card (lists G q v).card
    (by simpa [degree_split G v] using hdegree v) card_image_le
    (card_lists_add_image G q v) ht.le
  exact ⟨(degree_split G v).trans hn.1, ht, card_image_iff.mp hn.2.2⟩

/-- Failure to extend a proper boundary row supplies the actual list rejection. -/
theorem tight_of_not_extends (q : B → Color) (hq : BoundaryProper G q)
    (hconn : (interiorGraph G).Connected)
    (hdegree : ∀ v, G.degree (Sum.inr v) ≤ 4) (hreject : ¬ Extends G q) :
    ∀ v, G.degree (Sum.inr v) = 4 ∧
      (lists G q v).card = (interiorGraph G).degree v ∧
      Set.InjOn q (attachments G v) := by
  apply tight_of_rejection G q hconn hdegree
  exact fun hc => hreject ((extends_iff G q).mpr ⟨hq, hc⟩)

/-- A single interior vertex below full degree four rules out list rejection. -/
theorem listColorable_of_degree_lt_four (q : B → Color)
    (hconn : (interiorGraph G).Connected)
    (hdegree : ∀ v, G.degree (Sum.inr v) ≤ 4)
    (r : V) (hslack : G.degree (Sum.inr r) < 4) :
    ListColorable (interiorGraph G) (lists G q) := by
  by_contra h
  have := (tight_of_rejection G q hconn hdegree h r).1
  omega

/-- Two distinct actual neighbours of one interior vertex with the same boundary
colour create enough slack to colour the entire connected interior. -/
theorem listColorable_of_repeated_boundary_colour (q : B → Color)
    (hconn : (interiorGraph G).Connected)
    (hdegree : ∀ v, G.degree (Sum.inr v) ≤ 4)
    (r : V) {b b' : B} (hb : G.Adj (Sum.inr r) (Sum.inl b))
    (hb' : G.Adj (Sum.inr r) (Sum.inl b')) (hne : b ≠ b') (heq : q b = q b') :
    ListColorable (interiorGraph G) (lists G q) := by
  by_contra h
  exact hne ((tight_of_rejection G q hconn hdegree h r).2.2
    ((mem_attachments G r b).mpr hb) ((mem_attachments G r b').mpr hb') heq)

/-- The low-degree criterion extends every proper boundary row. -/
theorem extends_of_degree_lt_four (q : B → Color) (hq : BoundaryProper G q)
    (hconn : (interiorGraph G).Connected)
    (hdegree : ∀ v, G.degree (Sum.inr v) ≤ 4)
    (r : V) (hslack : G.degree (Sum.inr r) < 4) : Extends G q := by
  exact (extends_iff G q).mpr
    ⟨hq, listColorable_of_degree_lt_four G q hconn hdegree r hslack⟩

/-- The repeated-colour criterion extends the same proper boundary row on the same graph. -/
theorem extends_of_repeated_boundary_colour (q : B → Color) (hq : BoundaryProper G q)
    (hconn : (interiorGraph G).Connected)
    (hdegree : ∀ v, G.degree (Sum.inr v) ≤ 4)
    (r : V) {b b' : B} (hb : G.Adj (Sum.inr r) (Sum.inl b))
    (hb' : G.Adj (Sum.inr r) (Sum.inl b')) (hne : b ≠ b') (heq : q b = q b') :
    Extends G q := by
  exact (extends_iff G q).mpr
    ⟨hq, listColorable_of_repeated_boundary_colour G q hconn hdegree r hb hb' hne heq⟩

end FiveBoundary.BoundaryDegree
