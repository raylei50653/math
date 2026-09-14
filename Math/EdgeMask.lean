/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.ReducedDFS
import Mathlib.Data.Nat.Bitwise
import Mathlib.Data.Finset.Fold
import Mathlib.Data.Finset.Max

/-! Natural-number masks for the finite-set DFS. These are Lean `Nat` operations,
not a formal semantics of Python integers, graph mutation, or the scheduler. -/
namespace FiveBoundary.EdgeMask

open PrefixPartition ReducedDFS

local instance : Std.Commutative Nat.lor := ⟨Nat.lor_comm⟩
local instance : Std.Associative Nat.lor := ⟨Nat.lor_assoc⟩

def encode (M : Finset ℕ) : ℕ := M.fold Nat.lor 0 (fun e => 2 ^ e)

@[simp] theorem testBit_encode (M : Finset ℕ) (e : ℕ) :
    (encode M).testBit e = decide (e ∈ M) := by
  induction M using Finset.induction_on with
  | empty => simp [encode]
  | @insert a M ha ih =>
    change (M.fold Nat.lor 0 (fun e => 2 ^ e)).testBit e = _ at ih
    simp [encode, Finset.fold_insert ha, Nat.testBit_two_pow, ih, eq_comm]

theorem encode_injective : Function.Injective encode := by
  intro M N h
  ext e
  have := congrArg (fun n => n.testBit e) h
  simpa using this

@[simp] theorem encode_empty : encode ∅ = 0 := rfl

theorem encode_insert (M : Finset ℕ) (e : ℕ) :
    encode (insert e M) = encode M ||| (1 <<< e) := by
  apply Nat.eq_of_testBit_eq
  intro i
  simp [Nat.shiftLeft_eq, Nat.testBit_two_pow, eq_comm, Bool.or_comm]

theorem encode_lt {M : Finset ℕ} {E : ℕ} (h : ∀ e ∈ M, e < E) :
    encode M < 2 ^ E := by
  induction M using Finset.induction_on with
  | empty => simp
  | @insert e M he ih =>
    rw [encode_insert, Nat.shiftLeft_eq, one_mul]
    exact Nat.bitwise_lt_two_pow (ih (fun i hi => h i (Finset.mem_insert_of_mem hi)))
      (Nat.pow_lt_pow_right (by decide) (h e (Finset.mem_insert_self _ _)))

/-- The OR fold also equals production's sum of distinct bit weights. -/
theorem encode_eq_sum (M : Finset ℕ) : encode M = ∑ e ∈ M, 2 ^ e := by
  induction M using Finset.induction_on_max with
  | empty => simp
  | insert e M h ih =>
    have he : e ∉ M := fun he => (Nat.lt_irrefl e) (h e he)
    rw [encode_insert, Nat.shiftLeft_eq, one_mul,
      Nat.or_two_pow_eq_add_of_lt (encode_lt h), ih, Finset.sum_insert he, Nat.add_comm]

theorem encode_inter (M N : Finset ℕ) :
    encode (M ∩ N) = encode M &&& encode N := by
  apply Nat.eq_of_testBit_eq
  intro i
  simp

theorem encode_prefix (M : Finset ℕ) (p : ℕ) :
    encode (prefixPart p M) = encode M &&& ((1 <<< p) - 1) := by
  apply Nat.eq_of_testBit_eq
  intro i
  simp [prefixPart, Nat.shiftLeft_eq, Bool.and_comm]

/-- Bounded decoding deliberately discards bits at or above E. -/
def decode (E n : ℕ) : Finset ℕ := (Finset.range E).filter (fun e => n.testBit e)

theorem decode_encode (M : Finset ℕ) (E : ℕ) :
    decode E (encode M) = prefixPart E M := by
  ext e
  simp [decode, prefixPart, and_comm]

theorem encode_decode (E n : ℕ) :
    encode (decode E n) = n &&& ((1 <<< E) - 1) := by
  apply Nat.eq_of_testBit_eq
  intro i
  simp [decode, Nat.shiftLeft_eq]

/-- The width bound is essential for a lossless integer round trip. -/
theorem encode_decode_of_lt {E n : ℕ} (h : n < 2 ^ E) :
    encode (decode E n) = n := by
  apply Nat.eq_of_testBit_eq
  intro i
  by_cases hi : i < E
  · simp [decode, hi]
  · have hn : n.testBit i = false := Nat.testBit_lt_two_pow
      (lt_of_lt_of_le h (Nat.pow_le_pow_right (by decide) (by omega)))
    simp [decode, hi, hn]

/-- Shift removes the decided prefix and renumbers the remaining bits. -/
def shifted (p : ℕ) (M : Finset ℕ) : Finset ℕ :=
  (suffix p M).image (fun e => e - p)

theorem mem_shifted (p : ℕ) (M : Finset ℕ) (i : ℕ) :
    i ∈ shifted p M ↔ p + i ∈ M := by
  simp only [shifted, suffix, Finset.mem_image, Finset.mem_filter]
  constructor
  · rintro ⟨e, ⟨he, hp⟩, hi⟩
    have : e = p + i := by omega
    simpa [this] using he
  · intro h
    exact ⟨p + i, ⟨h, by omega⟩, by omega⟩

theorem encode_shifted (M : Finset ℕ) (p : ℕ) :
    encode (shifted p M) = encode M >>> p := by
  apply Nat.eq_of_testBit_eq
  intro i
  simp [mem_shifted]

/-- The five-bit extraction is exactly the numeric attachment value, not merely
an unordered attachment set or its cardinality. -/
theorem attachment_value (M : Finset ℕ) (m : ℕ) :
    (encode M >>> ReducedViable.blockStart m) &&& 31 = ReducedViable.attValue M m := by
  let W := (Finset.range 5).filter (fun i => ReducedViable.blockStart m + i ∈ M)
  have hw : encode W = (encode M >>> ReducedViable.blockStart m) &&& 31 := by
    apply Nat.eq_of_testBit_eq
    intro i
    change (encode W).testBit i =
      ((encode M >>> ReducedViable.blockStart m) &&& (2 ^ 5 - 1)).testBit i
    rw [Nat.testBit_land, Nat.testBit_shiftRight, Nat.testBit_two_pow_sub_one]
    simp [W, Bool.and_comm]
  rw [← hw, encode_eq_sum]
  simp [W, Finset.sum_filter, ReducedViable.attValue]

theorem shifted_card (M : Finset ℕ) (p : ℕ) :
    (shifted p M).card = (suffix p M).card := by
  apply Finset.card_image_iff.mpr
  intro a ha b hb hab
  have ha' : p ≤ a := (Finset.mem_filter.mp ha).2
  have hb' : p ≤ b := (Finset.mem_filter.mp hb).2
  dsimp at hab
  omega

/-- Integer control relation using the production OR/shift expression. -/
inductive Reach (guard : ℕ → ℕ → Prop) (oracle : ℕ → Prop)
    (stop base lo : ℕ) : Phase → ℕ → ℕ → Prop
  | root : Reach guard oracle stop base lo .node base lo
  | begin {n s} : Reach guard oracle stop base lo .node n s →
      Reach guard oracle stop base lo .scan n s
  | next {n e} : Reach guard oracle stop base lo .scan n e → e < stop →
      guard n e → Reach guard oracle stop base lo .scan n (e + 1)
  | take {n e} : Reach guard oracle stop base lo .scan n e → e < stop →
      guard n e → oracle (n ||| (1 <<< e)) →
      Reach guard oracle stop base lo .node (n ||| (1 <<< e)) (e + 1)

theorem reach_encode {guard : ℕ → ℕ → Prop} {oracle : ℕ → Prop}
    {stop lo s : ℕ} {base M : Finset ℕ} {phase : Phase}
    (h : ReducedDFS.Reach (fun P => guard (encode P)) (fun P => oracle (encode P))
      stop base lo phase M s) :
    Reach guard oracle stop (encode base) lo phase (encode M) s := by
  induction h with
  | root => exact .root
  | begin _ ih => exact .begin ih
  | next _ he hg ih => exact .next ih he hg
  | take _ he hg ho ih =>
    simpa [encode_insert] using Reach.take ih he hg (by simpa [encode_insert] using ho)

theorem reach_lift {guard : ℕ → ℕ → Prop} {oracle : ℕ → Prop}
    {stop lo s n : ℕ} {base : Finset ℕ} {phase : Phase}
    (h : Reach guard oracle stop (encode base) lo phase n s) :
    ∃ M, encode M = n ∧
      ReducedDFS.Reach (fun P => guard (encode P)) (fun P => oracle (encode P))
        stop base lo phase M s := by
  induction h with
  | root => exact ⟨base, rfl, .root⟩
  | begin _ ih =>
    obtain ⟨M, hm, hr⟩ := ih
    exact ⟨M, hm, .begin hr⟩
  | next _ he hg ih =>
    obtain ⟨M, rfl, hr⟩ := ih
    exact ⟨M, rfl, .next hr he hg⟩
  | @take n e _ he hg ho ih =>
    obtain ⟨M, rfl, hr⟩ := ih
    exact ⟨insert e M, encode_insert M e,
      .take hr he hg (by simpa [encode_insert] using ho)⟩

/-- Exact correspondence of both control models, with guards/oracles transported
through encode. It does not identify those predicates with Python implementations. -/
theorem reach_iff {guard : ℕ → ℕ → Prop} {oracle : ℕ → Prop}
    {stop lo s : ℕ} {base M : Finset ℕ} {phase : Phase} :
    Reach guard oracle stop (encode base) lo phase (encode M) s ↔
      ReducedDFS.Reach (fun P => guard (encode P)) (fun P => oracle (encode P))
        stop base lo phase M s := by
  constructor
  · intro h
    obtain ⟨N, hn, hr⟩ := reach_lift h
    exact encode_injective hn ▸ hr
  · exact reach_encode

theorem integer_owner (M : Finset ℕ) (p : ℕ) :
    ∃! n, ∃ A, Owns p A M ∧ encode A = n := by
  refine ⟨encode M &&& ((1 <<< p) - 1), ?_, ?_⟩
  · exact ⟨prefixPart p M, (owns_iff p _ _).mpr rfl, encode_prefix M p⟩
  · rintro n ⟨A, ha, rfl⟩
    rw [(owns_iff p A M).mp ha, encode_prefix]

end FiveBoundary.EdgeMask
