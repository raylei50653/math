/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.CommonRepair
import Math.SealedFourPort

/-! The two labelled private-interior cores, in one literal colour frame.
The selected mixed frames are specified explicitly; disk availability is not asserted. -/
namespace FiveBoundary.NamedRepair

open SealedFourPort CommonRepair

set_option maxRecDepth 16384

/-- U=(a0,a1,a2,a3,a4,b0,b2,b4); private vertices 8..12 are A_inner5..9,
and 13,14 are B_inner5,6. -/
abbrev Row := Fin 8 → Color
abbrev Scope := {s : Finset (Fin 8) // s.card = 4}

/-- The four named entries use at most three colours. -/
def N (a b c d : Color) : Prop :=
  a = b ∨ a = c ∨ a = d ∨ b = c ∨ b = d ∨ c = d
instance (a b c d : Color) : Decidable (N a b c d) :=
  inferInstanceAs (Decidable (_ ∨ _ ∨ _ ∨ _ ∨ _ ∨ _))

def ARule (x l y m n : Color) : Prop :=
  x ≠ l ∧ l ≠ y ∧ y ≠ m ∧ m ≠ n ∧ x ≠ n ∧ N x l y m ∧ N x n m y
instance (x l y m n : Color) : Decidable (ARule x l y m n) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _ ∧ _ ∧ _ ∧ _ ∧ _))

def AInner (x l y m n : Color) : Prop :=
  ∃ h7 : Color, x ≠ h7 ∧ y ≠ h7 ∧ m ≠ h7 ∧
    (∃ h5 h9 : Color, x ≠ h5 ∧ y ≠ h5 ∧ h5 ≠ h7 ∧
      x ≠ h9 ∧ y ≠ h9 ∧ l ≠ h9 ∧ h5 ≠ h9) ∧
    (∃ h6 h8 : Color, x ≠ h6 ∧ m ≠ h6 ∧ h6 ≠ h7 ∧
      x ≠ h8 ∧ m ≠ h8 ∧ n ≠ h8 ∧ h6 ≠ h8)
instance (x l y m n : Color) : Decidable (AInner x l y m n) :=
  inferInstanceAs (Decidable (∃ _ : Color, _))

set_option maxHeartbeats 2000000 in
-- Reduce the finite five-colour-argument path certificate in the kernel.
/-- Factor the private path at h7, so the finite kernel check has two short tails. -/
theorem a_rule : ∀ x l y m n : Color,
    (x ≠ l ∧ l ≠ y ∧ y ≠ m ∧ m ≠ n ∧ x ≠ n ∧ AInner x l y m n) ↔
      ARule x l y m n := by decide

def BRule (p s q t r : Color) : Prop :=
  p ≠ s ∧ s ≠ q ∧ q ≠ t ∧ t ≠ r ∧ p ≠ r ∧ q ≠ r ∧ (s ≠ r ∨ p = q)
instance (p s q t r : Color) : Decidable (BRule p s q t r) :=
  inferInstanceAs (Decidable (_ ∧ _ ∧ _ ∧ _ ∧ _ ∧ _ ∧ _))

def BInner (p s q r : Color) : Prop :=
  ∃ v w : Color, p ≠ v ∧ q ≠ v ∧ r ≠ v ∧ p ≠ w ∧ q ≠ w ∧ s ≠ w ∧ v ≠ w
instance (p s q r : Color) : Decidable (BInner p s q r) :=
  inferInstanceAs (Decidable (∃ _ _ : Color, _))

set_option maxHeartbeats 2000000 in
-- Check the two private lists over all five fixed boundary colours.
theorem b_rule : ∀ p s q t r : Color,
    (p ≠ s ∧ s ≠ q ∧ q ≠ t ∧ t ≠ r ∧ p ≠ r ∧ q ≠ r ∧ BInner p s q r) ↔
      BRule p s q t r := by decide

/-- false is forward, true is reverse; the shared named vertices are 0 and 2. -/
def source (rev : Bool) : Fin 8 := if rev then 2 else 0
def other (rev : Bool) : Fin 8 := if rev then 0 else 2

def JRule (rev : Bool) (b : Row) : Prop :=
  ARule (b 0) (b 1) (b 2) (b 3) (b 4) ∧
  BRule (b 5) (b (source rev)) (b 6) (b (other rev)) (b 7)
instance (rev : Bool) (b : Row) : Decidable (JRule rev b) :=
  inferInstanceAs (Decidable (_ ∧ _))

def coreEdges (rev : Bool) : List (Fin 15 × Fin 15) :=
  let s : Fin 15 := if rev then 2 else 0
  let t : Fin 15 := if rev then 0 else 2
  [(0,1), (1,2), (2,3), (3,4), (0,4),
   (0,8), (0,9), (0,10), (0,11), (0,12),
   (2,8), (2,10), (2,12), (3,9), (3,10), (3,11),
   (1,12), (4,11), (8,12), (8,10), (9,10), (9,11),
   (5,s), (s,6), (6,t), (t,7), (5,7), (6,7),
   (5,13), (6,13), (7,13), (5,14), (6,14), (s,14), (13,14)]

def ports : Fin 8 → Fin 15 := Fin.castLE (by decide)

def J (rev : Bool) : Set Row :=
  {b | ∃ c : Fin 15 → Color, Proper (graphOfEdges (coreEdges rev)) c ∧
    ∀ i, c (ports i) = b i}

/-- Every edge is the original named edge, including both C5 frames. -/
theorem core_proper_iff (rev : Bool) (c : Fin 15 → Color) :
    Proper (graphOfEdges (coreEdges rev)) c ↔ EdgeProper (coreEdges rev) c :=
  proper_graphOfEdges_iff _ (by cases rev <;> decide) c


/-- Exact extension to the original fifteen vertices, with all eight colours fixed. -/
theorem j_iff_rule (rev : Bool) (b : Row) : b ∈ J rev ↔ JRule rev b := by
  constructor
  · rintro ⟨c, hc, hb⟩
    have he := (core_proper_iff rev c).mp hc
    simp only [EdgeProper, coreEdges, List.mem_cons, List.not_mem_nil, or_false,
      forall_eq_or_imp, forall_eq] at he
    rcases he with ⟨h0, h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12,
      h13, h14, h15, h16, h17, h18, h19, h20, h21, h22, h23, h24, h25, h26,
      h27, h28, h29, h30, h31, h32, h33, h34⟩
    have ha := (a_rule (c 0) (c 1) (c 2) (c 3) (c 4)).mp
      ⟨h0, h1, h2, h3, h4, c 10, h7, h11, h14,
        ⟨c 8, c 12, h5, h10, h19, h9, h12, h16, h18⟩,
        ⟨c 9, c 11, h6, h13, h20, h8, h15, h17, h21⟩⟩
    have hb' := (b_rule (c 5) (c (if rev then 2 else 0)) (c 6)
      (c (if rev then 0 else 2)) (c 7)).mp
      ⟨h22, h23, h24, h25, h26, h27, c 13, c 14,
        h28, h29, h30, h31, h32, h33, h34⟩
    have h : JRule rev (fun i => c (ports i)) := by
      cases rev <;> simpa [JRule, source, other, ports] using And.intro ha hb'
    have eq : (fun i => c (ports i)) = b := funext hb
    exact eq ▸ h
  · intro h
    obtain ⟨ha, hb⟩ := h
    obtain ⟨ha0, ha1, ha2, ha3, ha4, h7, hx7, hy7, hm7,
      ⟨h5, h9, hx5, hy5, h57, hx9, hy9, hl9, h59⟩,
      ⟨h6, h8, hx6, hm6, h67, hx8, hm8, hn8, h68⟩⟩ := (a_rule _ _ _ _ _).mpr ha
    obtain ⟨hb0, hb1, hb2, hb3, hb4, hb5, v, w,
      hpv, hqv, hrv, hpw, hqw, hsw, hvw⟩ := (b_rule _ _ _ _ _).mpr hb
    let c : Fin 15 → Color :=
      ![b 0, b 1, b 2, b 3, b 4, b 5, b 6, b 7, h5, h6, h7, h8, h9, v, w]
    refine ⟨c, (core_proper_iff rev c).mpr ?_, ?_⟩
    · cases rev <;> simp_all [EdgeProper, coreEdges, c, source, other]
    · intro i
      fin_cases i <;> rfl

end FiveBoundary.NamedRepair
