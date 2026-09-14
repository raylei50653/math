/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.PrefixPartition
import Mathlib.Data.Finset.Card
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Order.Monotone.Basic

/-!+# Soundness of the R1 + SYM prefix rejection rule

Finite edge sets model masks. `blockStart` follows production's five chords and
blocks of five attachments plus `m` back edges. `touch` is a supplied incidence
table: connecting it to actual graph degrees or Python bit operations is a
separate obligation. No planarity or search execution is formalised here.
-/

namespace FiveBoundary.ReducedViable

open PrefixPartition

def blockStart : ℕ → ℕ
  | 0 => 5
  | m + 1 => blockStart m + 5 + m

theorem blockStart_strictMono : StrictMono blockStart := by
  apply strictMono_nat_of_lt_succ
  intro m
  simp only [blockStart]
  omega

def attValue (M : Finset ℕ) (m : ℕ) : ℕ :=
  ∑ i ∈ Finset.range 5, if blockStart m + i ∈ M then 2 ^ i else 0

def degree (touch : ℕ → Finset ℕ) (M : Finset ℕ) (m : ℕ) : ℕ :=
  (M ∩ touch m).card

def Survivor (k : ℕ) (touch : ℕ → Finset ℕ) (M : Finset ℕ) : Prop :=
  (∀ m < k, 4 ≤ degree touch M m) ∧
  (∀ m, m + 1 < k → attValue M (m + 1) ≤ attValue M m)

/-- Only blocks already started are tested, exactly as in production's loop. -/
def Viable (k : ℕ) (touch : ℕ → Finset ℕ) (P : Finset ℕ) (cut : ℕ) : Prop :=
  (∀ m < k, blockStart m < cut →
    4 ≤ degree touch P m + (suffix cut (touch m)).card) ∧
  (∀ m, m + 1 < k → blockStart (m + 1) < cut →
    attValue P (m + 1) ≤ attValue P m)

theorem degree_upper (touch : ℕ → Finset ℕ) (M : Finset ℕ) (cut m : ℕ) :
    degree touch M m ≤ degree touch (prefixPart cut M) m +
      (suffix cut (touch m)).card := by
  apply le_trans (Finset.card_le_card (show M ∩ touch m ⊆
      (prefixPart cut M ∩ touch m) ∪ suffix cut (touch m) from ?_))
    (Finset.card_union_le _ _)
  intro e he
  obtain ⟨hM, hT⟩ := Finset.mem_inter.mp he
  by_cases h : e < cut
  · exact Finset.mem_union_left _ (Finset.mem_inter.mpr
      ⟨Finset.mem_filter.mpr ⟨hM, h⟩, hT⟩)
  · exact Finset.mem_union_right _ (Finset.mem_filter.mpr ⟨hT, Nat.le_of_not_gt h⟩)

theorem attValue_mono {P M : Finset ℕ} (h : P ⊆ M) (m : ℕ) :
    attValue P m ≤ attValue M m := by
  apply Finset.sum_le_sum
  intro i hi
  by_cases hp : blockStart m + i ∈ P
  · simp [hp, h hp]
  · simp [hp]

theorem attValue_prefix_le (M : Finset ℕ) (cut m : ℕ) :
    attValue (prefixPart cut M) m ≤ attValue M m :=
  attValue_mono (Finset.filter_subset _ _) m

theorem attValue_prefix_eq (M : Finset ℕ) (cut m : ℕ)
    (h : ∀ i < 5, blockStart m + i < cut) :
    attValue (prefixPart cut M) m = attValue M m := by
  apply Finset.sum_congr rfl
  intro i hi
  simp only [prefixPart, Finset.mem_filter, h i (Finset.mem_range.mp hi), and_true]

/-- Once block `m+1` is started, all five attachment bits of block `m` are final. -/
theorem previous_block_fixed (M : Finset ℕ) (cut m : ℕ)
    (h : blockStart (m + 1) < cut) :
    attValue (prefixPart cut M) m = attValue M m := by
  apply attValue_prefix_eq
  intro i hi
  simp only [blockStart] at h
  omega

/-- Every prefix of a valid R1+SYM target passes both rejection tests. -/
theorem viable_of_survivor (k : ℕ) (touch : ℕ → Finset ℕ) (M : Finset ℕ)
    (hM : Survivor k touch M) (cut : ℕ) :
    Viable k touch (prefixPart cut M) cut := by
  constructor
  · intro m hm _
    exact le_trans (hM.1 m hm) (degree_upper touch M cut m)
  · intro m hm hstart
    rw [previous_block_fixed M cut m hstart]
    exact le_trans (attValue_prefix_le M cut (m + 1)) (hM.2 m hm)

/-- Rejection rules out all survivor completions with these exact decided bits. -/
theorem rejection_sound (k : ℕ) (touch : ℕ → Finset ℕ) (P : Finset ℕ) (cut : ℕ)
    (hP : ¬ Viable k touch P cut) :
    ¬ ∃ M, prefixPart cut M = P ∧ Survivor k touch M := by
  rintro ⟨M, hprefix, hM⟩
  exact hP (hprefix ▸ viable_of_survivor k touch M hM cut)

/-- Connect the pruning lemma to the earlier prefix ownership theorem. Reachability
of the unfiltered candidate label in `candidates` remains an explicit premise. -/
noncomputable def retainedTasks (k : ℕ) (touch : ℕ → Finset ℕ) (cut : ℕ)
    (candidates : Finset (Finset ℕ)) : Finset (Finset ℕ) := by
  classical
  exact candidates.filter (fun P => Viable k touch P cut)

theorem retained_owner (k : ℕ) (touch : ℕ → Finset ℕ) (M : Finset ℕ)
    (hM : Survivor k touch M) (cut : ℕ) (candidates : Finset (Finset ℕ))
    (hc : prefixPart cut M ∈ candidates) :
    ∃ A ∈ retainedTasks k touch cut candidates, Owns cut A M := by
  classical
  apply (covered_iff cut _ M).mpr
  exact Finset.mem_filter.mpr ⟨hc, viable_of_survivor k touch M hM cut⟩

end FiveBoundary.ReducedViable
