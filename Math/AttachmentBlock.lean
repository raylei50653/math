/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.GeometryDFA

/-! # Attachment block theorem

Geometry semantics of `RunOK` (winding ∈ {0,3}) without any enumeration. The cyclic step
sum on `Fin 3` is monotone under sublists (triangle inequality on the cyclic distance) and
invariant under rotation, so an accepting run can never contain the alternating pattern
`p, q, p, q'` (winding 6). Consequently the chords to a fixed interior vertex `k` form one
block in the cyclic order of boundary vertices: between any two boundary vertices attached
to `k`, one of the two open arcs of C5 is attached to nothing but `k`. -/

namespace FiveBoundary.GeometryDFA
open ColorDFA
open List (Sublist)

local infixl:50 " <+ " => List.Sublist

/-! ### Cyclic step sums on `Fin 3` -/

/-- Forward step from `a` to `b` on the triangle. -/
def stp (a b : Fin 3) : ℕ := (b - a).val

/-- Steps along a path starting at `a`. -/
def pathSteps : Fin 3 → List (Fin 3) → ℕ
  | _, [] => 0
  | a, b :: l => stp a b + pathSteps b l

/-- Cyclic step sum: the path closed back to its head. -/
def stepSum : List (Fin 3) → ℕ
  | [] => 0
  | h :: l => pathSteps h (l ++ [h])

theorem stp_triangle (a b c : Fin 3) : stp a c ≤ stp a b + stp b c := by
  revert a b c; decide

@[simp] theorem stp_self (a : Fin 3) : stp a a = 0 := by simp [stp]

theorem pathSteps_le_cons (a b : Fin 3) (l : List (Fin 3)) :
    pathSteps a l ≤ pathSteps a (b :: l) := by
  cases l with
  | nil => simp [pathSteps]
  | cons c l => simp only [pathSteps]; have := stp_triangle a b c; omega

theorem pathSteps_le_of_sublist {l₁ l₂ : List (Fin 3)} (h : l₁ <+ l₂) :
    ∀ a, pathSteps a l₁ ≤ pathSteps a l₂ := by
  induction h with
  | slnil => intro a; exact le_rfl
  | cons b _ ih => intro a; exact (ih a).trans (pathSteps_le_cons a b _)
  | cons_cons b _ ih => intro a; simp only [pathSteps]; exact Nat.add_le_add_left (ih b) _

theorem pathSteps_append_singleton (a : Fin 3) (l : List (Fin 3)) (e : Fin 3) :
    ∀ b, pathSteps a (b :: l ++ [e]) = stp a b + pathSteps b (l ++ [e]) := fun _ => rfl

/-- Rotating by one does not change the cyclic step sum. -/
theorem stepSum_rotate_one (l : List (Fin 3)) : stepSum (l.rotate 1) = stepSum l := by
  cases l with
  | nil => rfl
  | cons h l =>
    rw [List.rotate_cons_succ, List.rotate_zero]
    cases l with
    | nil => rfl
    | cons b l =>
      -- both sides are `stp h b + pathSteps b (l ++ [h])`, up to where the closing step sits
      have key : ∀ (a : Fin 3) (m : List (Fin 3)) (x y : Fin 3),
          pathSteps a (m ++ [x] ++ [y]) = pathSteps a (m ++ [x]) + stp x y := by
        intro a m x y
        induction m generalizing a with
        | nil => simp [pathSteps]
        | cons c m ih => simp only [List.cons_append, pathSteps, ih]; omega
      simp only [stepSum, List.cons_append]
      rw [key]
      simp only [pathSteps]
      omega

theorem stepSum_rotate (l : List (Fin 3)) (n : ℕ) : stepSum (l.rotate n) = stepSum l := by
  induction n with
  | zero => rw [List.rotate_zero]
  | succ n ih => rw [← List.rotate_rotate, stepSum_rotate_one, ih]

/-- The cyclic step sum is monotone under sublists. -/
theorem stepSum_le_of_sublist {l₁ l₂ : List (Fin 3)} (h : l₁ <+ l₂) : stepSum l₁ ≤ stepSum l₂ := by
  cases l₁ with
  | nil => exact Nat.zero_le _
  | cons a l =>
    obtain ⟨r₁, r₂, rfl, ha, hl⟩ := List.cons_sublist_iff.mp h
    obtain ⟨s, t, rfl⟩ := List.append_of_mem ha
    have hrot : (s ++ a :: t ++ r₂).rotate s.length = a :: (t ++ r₂ ++ s) := by
      rw [List.append_assoc, List.rotate_append_length_eq]; simp
    rw [← stepSum_rotate (s ++ a :: t ++ r₂) s.length, hrot]
    simp only [stepSum]
    apply pathSteps_le_of_sublist
    refine Sublist.append_right ?_ [a]
    exact (hl.trans (List.sublist_append_right t r₂)).trans (List.sublist_append_left _ s)

theorem stepSum_alternating (p q q' : Fin 3) (hq : q ≠ p) (hq' : q' ≠ p) :
    stepSum [p, q, p, q'] = 6 := by
  revert p q q'; decide

/-! ### Connecting to `winding` -/

theorem cyclicSteps_eq_stepSum (o : Bool) (l : List (Fin 5 × Fin 3)) :
    cyclicSteps o l = stepSum (l.map (fun e => pos o e.2)) := by
  cases l with
  | nil => rfl
  | cons e l =>
    have zipSteps : ∀ (f : Fin 5 × Fin 3 → Fin 3) (h : Fin 5 × Fin 3) (l : List (Fin 5 × Fin 3))
        (e : Fin 5 × Fin 3),
        ((List.zip (h :: l) (l ++ [e])).map (fun p => stp (f p.1) (f p.2))).sum =
          pathSteps (f h) (l.map f ++ [f e]) := by
      intro f h l e
      induction l generalizing h with
      | nil => simp [pathSteps]
      | cons b l ih => simp only [List.cons_append, List.zip_cons_cons, List.map_cons,
          List.sum_cons, pathSteps, ih]
    simp only [cyclicSteps, List.map_cons, stepSum]
    exact zipSteps (fun e => pos o e.2) e l e

theorem winding_eq_stepSum (w : Word) (ρ : Run) :
    winding w ρ = stepSum ((sequence w ρ).map (fun e => pos ρ.1 e.2)) :=
  cyclicSteps_eq_stepSum _ _

/-! ### Chords as sublists of the (rotated) sequence -/

theorem mem_fan (o : Bool) (letter : Finset (Fin 3)) (r : Fin 3) (k : Fin 3) :
    k ∈ fan o letter r ↔ k ∈ letter := by
  simp only [fan, List.mem_rotate, fanBase, List.mem_map, List.mem_filter, List.mem_finRange,
    true_and, decide_eq_true_eq]
  constructor
  · rintro ⟨p, hp, rfl⟩; exact hp
  · intro hk; exact ⟨pos o k, by rw [pos_involutive]; exact hk, pos_involutive o k⟩

theorem pos_injective (o : Bool) {k k' : Fin 3} (h : pos o k = pos o k') : k = k' := by
  rw [← pos_involutive o k, h, pos_involutive]

theorem forall₂_sublist_flatMap {ι α : Type*} (f : ι → List α) :
    ∀ {es : List α} {xs : List ι},
      List.Forall₂ (fun e x => e ∈ f x) es xs → es <+ xs.flatMap f := by
  intro es xs h
  induction h with
  | nil => exact List.Sublist.refl _
  | cons he _ ih =>
    rw [List.flatMap_cons, ← List.singleton_append]
    exact (List.singleton_sublist.mpr he).append ih

theorem flatMap_sublist_of_sublist {ι α : Type*} (f : ι → List α) {l₁ l₂ : List ι} (h : l₁ <+ l₂) :
    l₁.flatMap f <+ l₂.flatMap f := by
  induction h with
  | slnil => exact List.Sublist.refl _
  | cons a _ ih => rw [List.flatMap_cons]; exact ih.trans (List.sublist_append_right _ _)
  | cons_cons a _ ih => rw [List.flatMap_cons, List.flatMap_cons]; exact ih.append_left _

/-- `m` lies strictly inside the forward arc from `i` to `j` on C5. -/
def Between (i m j : Fin 5) : Prop := 0 < (m - i).val ∧ (m - i).val < (j - i).val

instance (i m j : Fin 5) : Decidable (Between i m j) := inferInstanceAs (Decidable (_ ∧ _))

theorem finRange_rotate (i : Fin 5) :
    (List.finRange 5).drop i.val ++ (List.finRange 5).take i.val = [i, i+1, i+2, i+3, i+4] := by
  fin_cases i <;> decide

theorem between_sublist (i j m₁ m₂ : Fin 5) (h₁ : Between i m₁ j) (h₂ : Between j m₂ i) :
    [i, m₁, j, m₂] <+ [i, i+1, i+2, i+3, i+4] := by
  revert i j m₁ m₂; decide

/-- The chord sequence, rotated to start at boundary vertex `i`. -/
theorem sequence_rotate (w : Word) (ρ : Run) (i : Fin 5) :
    ∃ n, (sequence w ρ).rotate n =
      [i, i+1, i+2, i+3, i+4].flatMap (fun j => (fan ρ.1 (w j) (ρ.2 j)).map (fun k => (j, k))) := by
  set F : Fin 5 → List (Fin 5 × Fin 3) := fun j => (fan ρ.1 (w j) (ρ.2 j)).map (fun k => (j, k))
  refine ⟨(((List.finRange 5).take i.val).flatMap F).length, ?_⟩
  have h1 : sequence w ρ =
      ((List.finRange 5).take i.val).flatMap F ++ ((List.finRange 5).drop i.val).flatMap F := by
    rw [← List.flatMap_append, List.take_append_drop]; rfl
  rw [h1, List.rotate_append_length_eq, ← List.flatMap_append, finRange_rotate]

/-! ### The attachment block theorem -/

/-- **Attachment block theorem.** In an accepting run, the chords to interior vertex `k` occupy
one block of the cyclic chord order: for boundary vertices `i, j` both attached to `k`, one of
the two open arcs between them carries no chord to any other interior vertex. -/
theorem attachment_block (w : Word) (ρ : Run) (h : RunOK w ρ) (k : Fin 3) (i j : Fin 5)
    (hi : k ∈ w i) (hj : k ∈ w j) :
    (∀ m, Between i m j → w m ⊆ {k}) ∨ (∀ m, Between j m i → w m ⊆ {k}) := by
  by_contra hcon
  push Not at hcon
  obtain ⟨⟨m₁, hm₁, hk₁⟩, ⟨m₂, hm₂, hk₂⟩⟩ := hcon
  have other : ∀ m, ¬ w m ⊆ {k} → ∃ k', k' ∈ w m ∧ k' ≠ k := by
    intro m hm
    by_contra h'
    push Not at h'
    exact hm (fun x hx => Finset.mem_singleton.mpr (h' x hx))
  obtain ⟨k₁, hk₁w, hk₁ne⟩ := other m₁ hk₁
  obtain ⟨k₂, hk₂w, hk₂ne⟩ := other m₂ hk₂
  obtain ⟨n, hn⟩ := sequence_rotate w ρ i
  have hchord : ∀ m k', k' ∈ w m →
      (m, k') ∈ (fan ρ.1 (w m) (ρ.2 m)).map (fun k => (m, k)) := by
    intro m k' hk'
    exact List.mem_map.mpr ⟨k', (mem_fan _ _ _ _).mpr hk', rfl⟩
  have hsub : [(i, k), (m₁, k₁), (j, k), (m₂, k₂)] <+ (sequence w ρ).rotate n := by
    rw [hn]
    refine (forall₂_sublist_flatMap _ ?_).trans
      (flatMap_sublist_of_sublist _ (between_sublist i j m₁ m₂ hm₁ hm₂))
    exact List.Forall₂.cons (hchord i k hi) (List.Forall₂.cons (hchord m₁ k₁ hk₁w)
      (List.Forall₂.cons (hchord j k hj) (List.Forall₂.cons (hchord m₂ k₂ hk₂w) List.Forall₂.nil)))
  have hle := stepSum_le_of_sublist (hsub.map (fun e => pos ρ.1 e.2))
  rw [List.map_rotate, stepSum_rotate, ← winding_eq_stepSum] at hle
  simp only [List.map_cons, List.map_nil] at hle
  rw [stepSum_alternating _ _ _ (fun h => hk₁ne (pos_injective ρ.1 h))
    (fun h => hk₂ne (pos_injective ρ.1 h))] at hle
  rcases h with h | h <;> omega

/-! ### Block normal form: `RunOK` is exactly "at most three blocks in triangle order" -/

/-- Last vertex of a path starting at `a`. -/
def lastOf : Fin 3 → List (Fin 3) → Fin 3
  | a, [] => a
  | _, b :: l => lastOf b l

/-- Three blocks starting at `h`, in the forward direction of the triangle. -/
def blocks (h : Fin 3) (a₀ a₁ a₂ : ℕ) : List (Fin 3) :=
  List.replicate a₀ h ++ List.replicate a₁ (h + 1) ++ List.replicate a₂ (h + 2)

@[simp] theorem pathSteps_nil (a : Fin 3) : pathSteps a [] = 0 := rfl
@[simp] theorem lastOf_nil (a : Fin 3) : lastOf a [] = a := rfl

theorem stp_le_two (a b : Fin 3) : stp a b ≤ 2 := by revert a b; decide

theorem stp_add_stp_of_ne {a b : Fin 3} (h : a ≠ b) : stp a b + stp b a = 3 := by
  revert a b; decide

@[simp] theorem stp_add_one (a : Fin 3) : stp a (a + 1) = 1 := by revert a; decide
@[simp] theorem stp_add_two (a : Fin 3) : stp a (a + 2) = 2 := by revert a; decide
@[simp] theorem fin3_add_one_add_one (a : Fin 3) : a + 1 + 1 = a + 2 := by revert a; decide
@[simp] theorem fin3_add_one_add_two (a : Fin 3) : a + 1 + 2 = a := by revert a; decide
@[simp] theorem fin3_add_two_add_one (a : Fin 3) : a + 2 + 1 = a := by revert a; decide
@[simp] theorem fin3_add_two_add_two (a : Fin 3) : a + 2 + 2 = a + 1 := by revert a; decide

theorem pathSteps_append (a : Fin 3) (l m : List (Fin 3)) :
    pathSteps a (l ++ m) = pathSteps a l + pathSteps (lastOf a l) m := by
  induction l generalizing a with
  | nil => simp [pathSteps, lastOf]
  | cons b l ih => simp only [List.cons_append, pathSteps, lastOf, ih]; omega

theorem lastOf_append (a : Fin 3) (l m : List (Fin 3)) :
    lastOf a (l ++ m) = lastOf (lastOf a l) m := by
  induction l generalizing a with
  | nil => rfl
  | cons b l ih => simp only [List.cons_append, lastOf, ih]

@[simp] theorem lastOf_replicate_succ (x y : Fin 3) (n : ℕ) :
    lastOf x (List.replicate (n + 1) y) = y := by
  induction n generalizing x with
  | zero => rfl
  | succ n ih => rw [List.replicate_succ]; exact ih y

@[simp] theorem lastOf_replicate_zero (x y : Fin 3) : lastOf x (List.replicate 0 y) = x := rfl

@[simp] theorem pathSteps_replicate_succ (x y : Fin 3) (n : ℕ) :
    pathSteps x (List.replicate (n + 1) y) = stp x y := by
  induction n generalizing x with
  | zero => simp [pathSteps]
  | succ n ih => rw [List.replicate_succ, pathSteps, ih y, stp_self, Nat.add_zero]

@[simp] theorem pathSteps_replicate_self (x : Fin 3) (n : ℕ) :
    pathSteps x (List.replicate n x) = 0 := by
  cases n <;> simp

@[simp] theorem lastOf_replicate_self (x : Fin 3) (n : ℕ) :
    lastOf x (List.replicate n x) = x := by
  cases n <;> simp

@[simp] theorem stp_add_one_add_two (a : Fin 3) : stp (a + 1) (a + 2) = 1 := by revert a; decide
@[simp] theorem stp_add_two_self (a : Fin 3) : stp (a + 2) a = 1 := by revert a; decide
@[simp] theorem stp_add_one_self (a : Fin 3) : stp (a + 1) a = 2 := by revert a; decide
@[simp] theorem stp_add_two_add_one (a : Fin 3) : stp (a + 2) (a + 1) = 2 := by revert a; decide

theorem stepSum_cons (h : Fin 3) (l : List (Fin 3)) :
    stepSum (h :: l) = pathSteps h l + stp (lastOf h l) h := by
  simp only [stepSum]; rw [pathSteps_append]; simp [pathSteps]

@[simp] theorem pathSteps_replicate_zero (x y : Fin 3) : pathSteps x (List.replicate 0 y) = 0 := rfl

theorem stp_le_pathSteps (a : Fin 3) (l : List (Fin 3)) : stp a (lastOf a l) ≤ pathSteps a l := by
  induction l generalizing a with
  | nil => simp [pathSteps, lastOf, stp_self]
  | cons b l ih =>
    simp only [pathSteps, lastOf]
    have := stp_triangle a b (lastOf b l)
    have := ih b
    omega

theorem lastOf_blocks (h : Fin 3) (a₀ a₁ a₂ : ℕ) :
    lastOf h (blocks h a₀ a₁ a₂) =
      if a₂ = 0 then (if a₁ = 0 then h else h + 1) else h + 2 := by
  rcases a₀ with _ | a₀ <;> rcases a₁ with _ | a₁ <;> rcases a₂ with _ | a₂ <;>
    simp [blocks, lastOf_append]

theorem fin3_trichotomy (a b : Fin 3) : b = a ∨ b = a + 1 ∨ b = a + 2 := by revert a b; decide

/-- A path whose total step count is exactly the cyclic distance to its endpoint never wraps:
it is three forward blocks starting at its head. -/
theorem blocks_of_pathSteps (l : List (Fin 3)) : ∀ a : Fin 3,
    pathSteps a l = stp a (lastOf a l) → ∃ a₀ a₁ a₂, a :: l = blocks a (a₀ + 1) a₁ a₂ := by
  induction l with
  | nil => intro a _; exact ⟨0, 0, 0, by simp [blocks]⟩
  | cons b l ih =>
    intro a h
    simp only [pathSteps, lastOf] at h
    have h1 := stp_le_pathSteps b l
    have h2 := stp_triangle a b (lastOf b l)
    obtain ⟨b₀, b₁, b₂, hl⟩ := ih b (by omega)
    have ht : lastOf b l = lastOf b (blocks b (b₀ + 1) b₁ b₂) := by rw [← hl]; rfl
    rw [lastOf_blocks] at ht
    rw [hl]
    rcases fin3_trichotomy a b with rfl | rfl | rfl
    · exact ⟨b₀ + 1, b₁, b₂, by simp [blocks, List.replicate_succ]⟩
    · rcases b₂ with _ | b₂
      · exact ⟨0, b₀ + 1, b₁, by simp [blocks, List.replicate_succ]⟩
      · exfalso; rw [ite_eq_right (Nat.succ_ne_zero _)] at ht; rw [ht] at h; simp at h
    · rcases b₂ with _ | b₂
      · rcases b₁ with _ | b₁
        · exact ⟨0, 0, b₀ + 1, by simp [blocks, List.replicate_succ]⟩
        · exfalso
          rw [ite_eq_left rfl, ite_eq_right (Nat.succ_ne_zero _)] at ht
          rw [ht] at h; simp at h
      · exfalso; rw [ite_eq_right (Nat.succ_ne_zero _)] at ht; rw [ht] at h; simp at h; omega

theorem lastOf_of_forall_eq (h : Fin 3) (l : List (Fin 3)) (hl : ∀ x ∈ l, x = h) :
    lastOf h l = h := by
  induction l with
  | nil => rfl
  | cons b l ih =>
    have hb := hl b (List.mem_cons_self ..)
    subst hb
    exact ih (fun x hx => hl x (List.mem_cons_of_mem _ hx))

/-- Either everything equals `h`, or split at the first element that differs. -/
theorem split_first_ne (h : Fin 3) (l : List (Fin 3)) :
    (∀ x ∈ l, x = h) ∨ ∃ l₁ b l₂, l = l₁ ++ b :: l₂ ∧ (∀ x ∈ l₁, x = h) ∧ b ≠ h := by
  induction l with
  | nil => exact Or.inl (by simp)
  | cons c l ih =>
    by_cases hc : c = h
    · subst hc
      rcases ih with ih | ⟨l₁, b, l₂, rfl, hl₁, hb⟩
      · exact Or.inl (by simpa using ih)
      · exact Or.inr ⟨c :: l₁, b, l₂, rfl, by simpa using hl₁, hb⟩
    · exact Or.inr ⟨[], c, l, rfl, by simp, hc⟩

theorem fin3_cases (b : Fin 3) : b = 0 ∨ b = 1 ∨ b = 2 := by revert b; decide

theorem blocks_rotate (b : Fin 3) (a₀ a₁ a₂ : ℕ) : ∃ m x y z, (blocks b a₀ a₁ a₂).rotate m =
    List.replicate x 0 ++ List.replicate y 1 ++ List.replicate z 2 := by
  have h11 : (1 : Fin 3) + 1 = 2 := by decide
  have h12 : (1 : Fin 3) + 2 = 0 := by decide
  have h21 : (2 : Fin 3) + 1 = 0 := by decide
  have h22 : (2 : Fin 3) + 2 = 1 := by decide
  rcases fin3_cases b with rfl | rfl | rfl
  · exact ⟨0, a₀, a₁, a₂, by simp [blocks]⟩
  · refine ⟨(List.replicate a₀ (1 : Fin 3) ++ List.replicate a₁ (2 : Fin 3)).length, a₂, a₀, a₁, ?_⟩
    simp only [blocks, h11, h12]
    rw [List.rotate_append_length_eq, List.append_assoc]
  · refine ⟨(List.replicate a₀ (2 : Fin 3)).length, a₁, a₂, a₀, ?_⟩
    simp only [blocks, h21, h22]
    rw [List.append_assoc, List.rotate_append_length_eq]

/-- **Block normal form (forward).** Cyclic step sum `0` or `3` forces some rotation to be
three forward blocks `0…0 1…1 2…2` (any of them possibly empty). -/
theorem blocks_of_stepSum (L : List (Fin 3)) (h : stepSum L = 0 ∨ stepSum L = 3) :
    ∃ n a b c, L.rotate n = List.replicate a 0 ++ List.replicate b 1 ++ List.replicate c 2 := by
  cases L with
  | nil => exact ⟨0, 0, 0, 0, rfl⟩
  | cons h0 l =>
    rcases split_first_ne h0 l with hall | ⟨l₁, b, l₂, rfl, hl₁, hb⟩
    · obtain ⟨m, rfl⟩ : ∃ m, l = List.replicate m h0 := ⟨_, List.eq_replicate_of_mem hall⟩
      obtain ⟨n, x, y, z, hn⟩ := blocks_rotate h0 (m + 1) 0 0
      exact ⟨n, x, y, z, by simpa [blocks, List.replicate_succ] using hn⟩
    · -- rotate to start at `b`; the closed walk then never wraps
      have hrot : (h0 :: (l₁ ++ b :: l₂)).rotate (h0 :: l₁).length = b :: (l₂ ++ h0 :: l₁) := by
        rw [← List.cons_append, List.rotate_append_length_eq]; rfl
      have hs : stepSum (b :: (l₂ ++ h0 :: l₁)) = stepSum (h0 :: (l₁ ++ b :: l₂)) := by
        rw [← hrot, stepSum_rotate]
      have hlast : lastOf b (l₂ ++ h0 :: l₁) = h0 := by
        rw [lastOf_append]; exact lastOf_of_forall_eq h0 l₁ hl₁
      have hlin : pathSteps b (l₂ ++ h0 :: l₁) = stp b (lastOf b (l₂ ++ h0 :: l₁)) := by
        have e1 : stepSum (b :: (l₂ ++ h0 :: l₁)) =
            pathSteps b (l₂ ++ h0 :: l₁) + stp h0 b := by
          simp only [stepSum]
          rw [pathSteps_append, hlast]; rfl
        have e2 := stp_le_pathSteps b (l₂ ++ h0 :: l₁)
        have e3 := stp_add_stp_of_ne hb
        rw [hlast] at e2 ⊢
        omega
      obtain ⟨a₀, a₁, a₂, hbl⟩ := blocks_of_pathSteps _ b hlin
      obtain ⟨m, x, y, z, hm⟩ := blocks_rotate b (a₀ + 1) a₁ a₂
      exact ⟨(h0 :: l₁).length + m, x, y, z, by rw [← List.rotate_rotate, hrot, hbl, hm]⟩

theorem stepSum_blocks' (h : Fin 3) (a₀ a₁ a₂ : ℕ) :
    stepSum (blocks h (a₀ + 1) a₁ a₂) = 0 ∨ stepSum (blocks h (a₀ + 1) a₁ a₂) = 3 := by
  simp only [blocks, List.replicate_succ, List.cons_append, stepSum_cons, pathSteps_append,
    lastOf_append, pathSteps_replicate_self, lastOf_replicate_self]
  rcases a₁ with _ | a₁ <;> rcases a₂ with _ | a₂ <;> simp

theorem stepSum_blocks (a b c : ℕ) :
    stepSum (List.replicate a 0 ++ List.replicate b 1 ++ List.replicate c 2) = 0 ∨
    stepSum (List.replicate a 0 ++ List.replicate b 1 ++ List.replicate c 2) = 3 := by
  have h11 : (1 : Fin 3) + 1 = 2 := by decide
  rcases a with _ | a
  · rcases b with _ | b
    · rcases c with _ | c
      · exact Or.inl rfl
      · simpa [blocks] using stepSum_blocks' 2 c 0 0
    · simpa [blocks, h11] using stepSum_blocks' 1 b c 0
  · simpa [blocks] using stepSum_blocks' 0 a b c

/-- **Block normal form.** `stepSum L ∈ {0,3}` iff some rotation of `L` is `0…0 1…1 2…2`. -/
theorem stepSum_mem_iff_blocks (L : List (Fin 3)) :
    (stepSum L = 0 ∨ stepSum L = 3) ↔
      ∃ n a b c, L.rotate n = List.replicate a 0 ++ List.replicate b 1 ++ List.replicate c 2 := by
  refine ⟨blocks_of_stepSum L, ?_⟩
  rintro ⟨n, a, b, c, hn⟩
  rw [← stepSum_rotate L n, hn]
  exact stepSum_blocks a b c

/-- **Attachment block theorem (sequence form).** A run is accepting iff, read cyclically along
C5, the triangle positions of its chords form at most three blocks in forward triangle order. -/
theorem runOK_iff_blocks (w : Word) (ρ : Run) :
    RunOK w ρ ↔ ∃ n a b c, ((sequence w ρ).map (fun e => pos ρ.1 e.2)).rotate n =
      List.replicate a 0 ++ List.replicate b 1 ++ List.replicate c 2 := by
  rw [RunOK, winding_eq_stepSum]
  exact stepSum_mem_iff_blocks _

end FiveBoundary.GeometryDFA
