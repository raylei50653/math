/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.ReducedViable
import Math.SymNormalForm
import Mathlib.Combinatorics.SimpleGraph.Finite

/-! Graph-to-search bridge for the interior blocks of the production edge order.
Boundary-only edges do not contribute to interior degrees or attachment masks.
All results are uniform in the number of private vertices; no finite enumeration.
-/
namespace FiveBoundary.ReducedGraphBridge

open ReducedViable PrefixPartition

/-- An ordered pair with at least one private endpoint. -/
abbrev Edge (k : ℕ) := {p : Fin (5 + k) × Fin (5 + k) // p.1 < p.2 ∧ 5 ≤ p.2.val}

def edgeIndex {k : ℕ} (e : Edge k) : ℕ :=
  blockStart (e.val.2.val - 5) + e.val.1.val

theorem blockIndex_injective {m n i j : ℕ} (hi : i < 5 + m) (hj : j < 5 + n)
    (h : blockStart m + i = blockStart n + j) : m = n ∧ i = j := by
  have hm : ¬ m < n := by
    intro hmn
    have := blockStart_strictMono.monotone (show m + 1 ≤ n by omega)
    simp only [blockStart] at this
    omega
  have hn : ¬ n < m := by
    intro hnm
    have := blockStart_strictMono.monotone (show n + 1 ≤ m by omega)
    simp only [blockStart] at this
    omega
  have he : m = n := by omega
  subst n
  exact ⟨rfl, by omega⟩

theorem edgeIndex_injective {k : ℕ} : Function.Injective (@edgeIndex k) := by
  intro a b h
  have ha := a.property
  have hb := b.property
  have hh := blockIndex_injective (m := a.val.2.val - 5) (n := b.val.2.val - 5)
    (i := a.val.1.val) (j := b.val.1.val) (by omega) (by omega) h
  apply Subtype.ext
  apply Prod.ext <;> apply Fin.ext <;> omega

theorem edgeIndex_lt {k : ℕ} (e : Edge k) : edgeIndex e < blockStart k := by
  have hp := e.property
  have hv := e.val.2.isLt
  have h := blockStart_strictMono.monotone (show e.val.2.val - 5 + 1 ≤ k by omega)
  simp only [blockStart] at h
  unfold edgeIndex
  omega

/-- The unique ordered edge from private vertex m to a distinct vertex v. -/
def incident {k : ℕ} (m : Fin k) (v : Fin (5 + k))
    (h : v ≠ Fin.natAdd 5 m) : Edge k :=
  if hv : v < Fin.natAdd 5 m then
    ⟨(v, Fin.natAdd 5 m), hv, by simp⟩
  else
    ⟨(Fin.natAdd 5 m, v), lt_of_le_of_ne (le_of_not_gt hv) (Ne.symm h), by
      have := (le_of_not_gt hv : Fin.natAdd 5 m ≤ v)
      change 5 + m.val ≤ v.val at this
      change 5 ≤ v.val
      omega⟩

theorem incident_injective {k : ℕ} (m : Fin k) (v w : Fin (5 + k))
    (hv : v ≠ Fin.natAdd 5 m) (hw : w ≠ Fin.natAdd 5 m)
    (h : edgeIndex (incident m v hv) = edgeIndex (incident m w hw)) : v = w := by
  have he := congrArg Subtype.val (edgeIndex_injective h)
  unfold incident at he
  split_ifs at he <;> simp only at he <;> cases Prod.mk.inj he <;> simp_all

noncomputable def encode {k : ℕ} (G : SimpleGraph (Fin (5 + k))) : Finset ℕ := by
  classical
  exact (Finset.univ.filter (fun e : Edge k => G.Adj e.val.1 e.val.2)).image edgeIndex

@[simp] theorem mem_encode {k : ℕ} (G : SimpleGraph (Fin (5 + k))) (e : Edge k) :
    edgeIndex e ∈ encode G ↔ G.Adj e.val.1 e.val.2 := by
  classical
  simp [encode, edgeIndex_injective.eq_iff]

theorem mem_encode_incident {k : ℕ} (G : SimpleGraph (Fin (5 + k)))
    (m : Fin k) (v : Fin (5 + k)) (h : v ≠ Fin.natAdd 5 m) :
    edgeIndex (incident m v h) ∈ encode G ↔ G.Adj (Fin.natAdd 5 m) v := by
  rw [mem_encode]
  unfold incident
  split_ifs <;> simp only
  exact G.adj_comm _ _

/-- Exact interior-edge representation. Bits 0..4 are boundary chords and unrestricted. -/
def Represents {k : ℕ} (G : SimpleGraph (Fin (5 + k))) (M : Finset ℕ) : Prop :=
  ∀ e : Edge k, edgeIndex e ∈ M ↔ G.Adj e.val.1 e.val.2

theorem represents_encode {k : ℕ} (G : SimpleGraph (Fin (5 + k))) :
    Represents G (encode G) := mem_encode G

theorem represents_incident {k : ℕ} {G : SimpleGraph (Fin (5 + k))} {M : Finset ℕ}
    (hM : Represents G M) (m : Fin k) (v : Fin (5 + k))
    (h : v ≠ Fin.natAdd 5 m) :
    edgeIndex (incident m v h) ∈ M ↔ G.Adj (Fin.natAdd 5 m) v := by
  rw [hM]
  unfold incident
  split_ifs <;> simp only
  exact G.adj_comm _ _

/-- Any choice of the five chord bits preserves the interior representation. -/
theorem represents_with_chords {k : ℕ} (G : SimpleGraph (Fin (5 + k)))
    (C : Finset ℕ) (hC : C ⊆ Finset.range 5) : Represents G (C ∪ encode G) := by
  intro e
  have hlo : 5 ≤ edgeIndex e := by
    have := blockStart_strictMono.monotone (Nat.zero_le (e.val.2.val - 5))
    simp only [blockStart] at this
    unfold edgeIndex
    omega
  have hn : edgeIndex e ∉ C := fun h => by
    have := Finset.mem_range.mp (hC h)
    omega
  simp [hn, mem_encode]

/-- Finite incidence table, including both earlier and later private neighbours. -/
noncomputable def touch (k m : ℕ) : Finset ℕ := by
  classical
  exact (Finset.univ.filter (fun e : Edge k =>
    e.val.1.val = 5 + m ∨ e.val.2.val = 5 + m)).image edgeIndex

theorem mem_touch {k : ℕ} (m : Fin k) (e : Edge k) :
    edgeIndex e ∈ touch k m.val ↔
      e.val.1 = Fin.natAdd 5 m ∨ e.val.2 = Fin.natAdd 5 m := by
  classical
  simp [touch, edgeIndex_injective.eq_iff, Fin.ext_iff]

theorem incident_mem_touch {k : ℕ} (m : Fin k) (v : Fin (5 + k))
    (h : v ≠ Fin.natAdd 5 m) : edgeIndex (incident m v h) ∈ touch k m.val := by
  rw [mem_touch]
  unfold incident
  split_ifs <;> simp

open Classical in
theorem degree_eq_graph {k : ℕ} (G : SimpleGraph (Fin (5 + k)))
    (M : Finset ℕ) (hM : Represents G M) (m : Fin k) :
    degree (touch k) M m.val = G.degree (Fin.natAdd 5 m) := by
  classical
  symm
  unfold SimpleGraph.degree degree
  apply Finset.card_bij (fun v hv => edgeIndex (incident m v
    (Ne.symm (G.ne_of_adj ((G.mem_neighborFinset _ _).mp hv)))))
  · intro v hv
    exact Finset.mem_inter.mpr ⟨(represents_incident hM m v _).mpr
      ((G.mem_neighborFinset _ _).mp hv), incident_mem_touch m v _⟩
  · intro v hv w hw he
    exact incident_injective m v w _ _ he
  · intro b hb
    obtain ⟨he, ht⟩ := Finset.mem_inter.mp hb
    obtain ⟨e, _, rfl⟩ := Finset.mem_image.mp ht
    have hadj := (hM e).mp he
    rcases (mem_touch m e).mp ht with h | h
    · refine ⟨e.val.2, (G.mem_neighborFinset _ _).mpr (h ▸ hadj), ?_⟩
      congr 1
      apply Subtype.ext
      simp [incident, ← h, not_lt_of_ge (le_of_lt e.property.1)]
    · refine ⟨e.val.1, (G.mem_neighborFinset _ _).mpr (h ▸ hadj.symm), ?_⟩
      congr 1
      apply Subtype.ext
      simp [incident, ← h, e.property.1]

/-- Attachment bit i has exactly the production offset blockStart(m)+i. -/
def attachment {k : ℕ} (m : Fin k) (i : Fin 5) : Edge k :=
  ⟨(Fin.castAdd k i, Fin.natAdd 5 m), by
    change i.val < 5 + m.val
    omega, by simp⟩

@[simp] theorem attachment_index {k : ℕ} (m : Fin k) (i : Fin 5) :
    edgeIndex (attachment m i) = blockStart m.val + i.val := by
  simp [edgeIndex, attachment]

theorem attValue_eq_attMask {k : ℕ} (G : SimpleGraph (Fin (5 + k)))
    (M : Finset ℕ) (hM : Represents G M) (m : Fin k) :
    attValue M m.val =
      Sym.attMask G (firstBoundary (Nat.le_add_right 5 k)) (Fin.natAdd 5 m) := by
  classical
  unfold attValue Sym.attMask
  rw [← Fin.sum_univ_eq_sum_range]
  apply Finset.sum_congr rfl
  intro i _
  simp only [← attachment_index m i, hM (attachment m i)]
  rfl

open Classical in
/-- Graph-layer R1 and numeric-mask SYM, with no planarity premise. -/
def GraphSurvivor {k : ℕ} (G : SimpleGraph (Fin (5 + k))) : Prop :=
  (∀ m : Fin k, 4 ≤ G.degree (Fin.natAdd 5 m)) ∧ Sym.SortedAttachments G

theorem survivor_iff {k : ℕ} (G : SimpleGraph (Fin (5 + k)))
    (M : Finset ℕ) (hM : Represents G M) :
    Survivor k (touch k) M ↔ GraphSurvivor G := by
  constructor
  · rintro ⟨hd, hs⟩
    constructor
    · intro m
      rw [← degree_eq_graph G M hM]
      exact hd m.val m.isLt
    · cases k with
      | zero => intro i; exact Fin.elim0 i
      | succ n =>
        apply Fin.antitone_iff_succ_le.mpr
        intro i
        have h := hs i.val (by omega)
        have h1 := attValue_eq_attMask G M hM i.succ
        have h0 := attValue_eq_attMask G M hM i.castSucc
        simp only [Fin.val_succ, Fin.val_castSucc] at h1 h0
        rw [h1, h0] at h
        exact h
  · rintro ⟨hd, hs⟩
    constructor
    · intro m hm
      rw [degree_eq_graph G M hM ⟨m, hm⟩]
      exact hd ⟨m, hm⟩
    · intro m hm
      rw [attValue_eq_attMask G M hM ⟨m + 1, hm⟩,
        attValue_eq_attMask G M hM ⟨m, by omega⟩]
      exact hs (show (⟨m, by omega⟩ : Fin k) ≤ ⟨m + 1, hm⟩ by simp)

theorem viable_of_graph {k : ℕ} (G : SimpleGraph (Fin (5 + k)))
    (M : Finset ℕ) (hM : Represents G M) (hG : GraphSurvivor G) (cut : ℕ) :
    Viable k (touch k) (prefixPart cut M) cut :=
  viable_of_survivor k (touch k) M ((survivor_iff G M hM).mpr hG) cut

theorem graph_rejection_sound (k : ℕ) (P : Finset ℕ) (cut : ℕ)
    (hP : ¬ Viable k (touch k) P cut) :
    ¬ ∃ (G : SimpleGraph (Fin (5 + k))) (M : Finset ℕ),
      Represents G M ∧ prefixPart cut M = P ∧ GraphSurvivor G := by
  rintro ⟨G, M, hM, hprefix, hG⟩
  exact hP (hprefix ▸ viable_of_graph G M hM hG cut)

theorem retained_graph_owner {k : ℕ} (G : SimpleGraph (Fin (5 + k)))
    (M : Finset ℕ) (hM : Represents G M) (hG : GraphSurvivor G) (cut : ℕ)
    (candidates : Finset (Finset ℕ))
    (hc : prefixPart cut M ∈ candidates) :
    ∃ A ∈ retainedTasks k (touch k) cut candidates, Owns cut A M :=
  retained_owner k (touch k) M ((survivor_iff G M hM).mpr hG) cut candidates hc

end FiveBoundary.ReducedGraphBridge
