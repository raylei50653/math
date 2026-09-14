/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.ReducedGraphBridge

/-! Abstract control flow of the reduced increasing-edge DFS.
`node` is a recursive entry (where production appends/records); `scan` is a loop
position. Advancing the loop requires its guard, including skipped indices.
Oracle acceptance is explicit: this does not verify Python or planarity.
-/
namespace FiveBoundary.ReducedDFS

open PrefixPartition ReducedViable ReducedGraphBridge

inductive Phase | node | scan

/-- Reachable control locations in a finite DFS tree. `next` abstracts returning
from a child (or rejecting it); no child result influences subsequent siblings. -/
inductive Reach (guard : Finset ℕ → ℕ → Prop) (oracle : Finset ℕ → Prop)
    (stop : ℕ) (base : Finset ℕ) (lo : ℕ) : Phase → Finset ℕ → ℕ → Prop
  | root : Reach guard oracle stop base lo .node base lo
  | begin {P s} : Reach guard oracle stop base lo .node P s →
      Reach guard oracle stop base lo .scan P s
  | next {P e} : Reach guard oracle stop base lo .scan P e → e < stop →
      guard P e → Reach guard oracle stop base lo .scan P (e + 1)
  | take {P e} : Reach guard oracle stop base lo .scan P e → e < stop →
      guard P e → oracle (insert e P) →
      Reach guard oracle stop base lo .node (insert e P) (e + 1)

/-- All reachable locations preserve the fixed base and increasing-index bounds. -/
theorem state_invariant {guard : Finset ℕ → ℕ → Prop} {oracle : Finset ℕ → Prop}
    {stop lo s : ℕ} {base P : Finset ℕ} {phase : Phase}
    (h : Reach guard oracle stop base lo phase P s)
    (hlo : lo ≤ stop) (hb : ∀ e ∈ base, e < lo) :
    lo ≤ s ∧ s ≤ stop ∧ base ⊆ P ∧ (∀ e ∈ P, e < s) ∧
      prefixPart lo P = base := by
  induction h with
  | root => exact ⟨le_refl _, hlo, Finset.Subset.refl _, hb, owner_at_end lo base hb⟩
  | begin _ ih => exact ih
  | next _ he _ ih =>
    obtain ⟨hl, hs, hbase, hbits, hprefix⟩ := ih
    exact ⟨by omega, by omega, hbase, fun e hm => by have := hbits e hm; omega, hprefix⟩
  | @take P e _ he _ _ ih =>
    obtain ⟨hl, hs, hbase, hbits, hprefix⟩ := ih
    refine ⟨by omega, by omega, fun x hx => Finset.mem_insert_of_mem (hbase hx), ?_, ?_⟩
    · intro x hx
      rcases Finset.mem_insert.mp hx with rfl | hx
      · omega
      · have := hbits x hx
        omega
    · rw [← hprefix]
      ext x
      simp only [prefixPart, Finset.mem_filter, Finset.mem_insert]
      constructor
      · rintro ⟨rfl | hx, hlt⟩
        · omega
        · exact ⟨hx, hlt⟩
      · rintro ⟨hx, hlt⟩
        exact ⟨Or.inr hx, hlt⟩

/-- Both a recursive child and the next loop position strictly reduce this fuel.
This is a bound for the abstract traversal, not Python runtime verification. -/
theorem remaining_decreases {e stop : ℕ} (h : e < stop) :
    stop - (e + 1) < stop - e := by omega

theorem prefix_zero (M : Finset ℕ) : prefixPart 0 M = ∅ := by
  simp [prefixPart]

theorem prefix_succ (M : Finset ℕ) (e : ℕ) :
    prefixPart (e + 1) M = if e ∈ M then insert e (prefixPart e M) else prefixPart e M := by
  ext x
  by_cases he : e ∈ M <;> simp only [he, ite_true, ite_false, prefixPart,
    Finset.mem_filter, Finset.mem_insert] <;> constructor
  · rintro ⟨hx, hlt⟩
    by_cases hxe : x = e
    · exact Or.inl hxe
    · exact Or.inr ⟨hx, by omega⟩
  · rintro (rfl | ⟨hx, hlt⟩)
    · exact ⟨he, by omega⟩
    · exact ⟨hx, by omega⟩
  · rintro ⟨hx, hlt⟩
    exact ⟨hx, by have : x ≠ e := fun h => he (h ▸ hx); omega⟩
  · rintro ⟨hx, hlt⟩
    exact ⟨hx, by omega⟩

/-- Every target prefix is an actual recursive entry, although its entry `start`
can be smaller than the requested cut. The scan also reaches that cut. -/
theorem prefix_reachable (guard : Finset ℕ → ℕ → Prop) (oracle : Finset ℕ → Prop)
    (M : Finset ℕ) (lo stop : ℕ)
    (hg : ∀ e, lo ≤ e → e < stop → guard (prefixPart e M) e)
    (ho : ∀ e, lo ≤ e → e < stop → e ∈ M → oracle (prefixPart (e + 1) M))
    (p : ℕ) (hl : lo ≤ p) (hp : p ≤ stop) :
    (∃ s, s ≤ p ∧ Reach guard oracle stop (prefixPart lo M) lo .node (prefixPart p M) s) ∧
      Reach guard oracle stop (prefixPart lo M) lo .scan (prefixPart p M) p := by
  induction p, hl using Nat.le_induction with
  | base => exact ⟨⟨lo, le_refl _, .root⟩, .begin .root⟩
  | succ p hl ih =>
    obtain ⟨hn, hs⟩ := ih (by omega)
    have hlt : p < stop := by omega
    have hg' := hg p hl hlt
    by_cases he : p ∈ M
    · have ht := Reach.take hs hlt hg' (by simpa [prefix_succ, he] using ho p hl hlt he)
      simp only [prefix_succ, he, ite_true]
      exact ⟨⟨p + 1, le_refl _, ht⟩, .begin ht⟩
    · simp only [prefix_succ, he, ite_false]
      obtain ⟨s, hsp, hn⟩ := hn
      exact ⟨⟨s, by omega, hn⟩, .next hs hlt hg'⟩

/-- Candidate labels are exactly reachable recursive entries, not loop positions. -/
noncomputable def candidates (guard : Finset ℕ → ℕ → Prop)
    (oracle : Finset ℕ → Prop) (p : ℕ) : Finset (Finset ℕ) := by
  classical
  exact (Finset.range p).powerset.filter (fun P => ∃ s, Reach guard oracle p ∅ 0 .node P s)

/-- Discharges the old candidate-membership obligation from control-flow reachability. -/
theorem mem_candidates (guard : Finset ℕ → ℕ → Prop) (oracle : Finset ℕ → Prop)
    (M : Finset ℕ) (p : ℕ)
    (hg : ∀ e < p, guard (prefixPart e M) e)
    (ho : ∀ e < p, e ∈ M → oracle (prefixPart (e + 1) M)) :
    prefixPart p M ∈ candidates guard oracle p := by
  classical
  obtain ⟨⟨s, _, hs⟩, _⟩ := prefix_reachable guard oracle M 0 p
    (fun e _ he => hg e he) (fun e _ he => ho e he) p (Nat.zero_le _) (le_refl _)
  apply Finset.mem_filter.mpr
  refine ⟨Finset.mem_powerset.mpr ?_, s, ?_⟩
  · intro e he
    exact Finset.mem_range.mpr (Finset.mem_filter.mp he).2
  · simpa [prefix_zero] using hs

/-- R1+SYM graphs have a retained owner, conditional only on the oracle accepting
selected-edge prefixes. No candidate-membership premise remains. -/
theorem retained_graph_owner {k : ℕ} (G : SimpleGraph (Fin (5 + k)))
    (M : Finset ℕ) (hM : Represents G M) (hG : GraphSurvivor G)
    (oracle : Finset ℕ → Prop) (p : ℕ)
    (ho : ∀ e < p, e ∈ M → oracle (prefixPart (e + 1) M)) :
    ∃ A ∈ retainedTasks k (touch k) p
      (candidates (Viable k (touch k)) oracle p), Owns p A M := by
  apply ReducedGraphBridge.retained_graph_owner G M hM hG
  exact mem_candidates _ oracle M p (fun e _ => viable_of_graph G M hM hG e) ho

/-- Worker traversal from a fixed prefix reaches the complete target at an entry,
so recording need not wait for `start = E`. Covers empty suffixes as well. -/
theorem worker_reachable {k : ℕ} (G : SimpleGraph (Fin (5 + k)))
    (M : Finset ℕ) (hM : Represents G M) (hG : GraphSurvivor G)
    (oracle : Finset ℕ → Prop) (p E : ℕ) (hp : p ≤ E)
    (hbound : ∀ e ∈ M, e < E)
    (ho : ∀ e, p ≤ e → e < E → e ∈ M → oracle (prefixPart (e + 1) M)) :
    ∃ s, s ≤ E ∧ Reach (Viable k (touch k)) oracle E (prefixPart p M) p .node M s := by
  obtain ⟨hn, _⟩ := prefix_reachable (Viable k (touch k)) oracle M p E
    (fun e _ _ => viable_of_graph G M hM hG e) ho E hp (le_refl _)
  simpa [owner_at_end E M hbound] using hn

/-- End-to-end abstract split coverage: a unique retained label owns a worker
entry for the target, and the terminal recording guard passes. At `p = E`,
this same entry is handled directly by the parent, without launching a worker.
Uniqueness concerns labels, not scheduler execution or multiplicity. -/
theorem split_graph_complete {k : ℕ} (G : SimpleGraph (Fin (5 + k)))
    (M : Finset ℕ) (hM : Represents G M) (hG : GraphSurvivor G)
    (oracle : Finset ℕ → Prop) (p E : ℕ) (hp : p ≤ E)
    (hbound : ∀ e ∈ M, e < E)
    (ho : ∀ e < E, e ∈ M → oracle (prefixPart (e + 1) M)) :
    ∃! A, A ∈ retainedTasks k (touch k) p
      (candidates (Viable k (touch k)) oracle p) ∧ Owns p A M ∧
      (∃ s, s ≤ E ∧ Reach (Viable k (touch k)) oracle E A p .node M s) ∧
      Viable k (touch k) M E := by
  obtain ⟨A, ha, hown⟩ := retained_graph_owner G M hM hG oracle p
    (fun e he => ho e (by omega))
  have heq := (owns_iff p A M).mp hown
  refine ⟨A, ⟨ha, hown, ?_, ?_⟩, ?_⟩
  · rw [heq]
    exact worker_reachable G M hM hG oracle p E hp hbound (fun e _ he => ho e he)
  · simpa [owner_at_end E M hbound] using viable_of_graph G M hM hG E
  · intro B hb
    exact owners_equal hb.2.1 hown

end FiveBoundary.ReducedDFS
