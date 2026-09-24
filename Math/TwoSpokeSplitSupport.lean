/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.TwoSpokeReflection

/-! Finite all-row algebra. The source graph/support classification is a paper theorem. -/
namespace FiveBoundary.TwoSpokeSplitSupport

open ForcingLists TwoSpokeReflection

abbrev Row := Fin 5 → Color

def proper (b : Row) : Prop := ∀ i : Fin 5, b i ≠ b (i + 1)

instance (b : Row) : Decidable (proper b) := inferInstanceAs (Decidable (∀ i, b i ≠ b (i + 1)))

def banA (b : Row) : Finset Color := if b 1 = b 3 then {b 2} else ∅

def banD (b : Row) : Finset Color :=
  if b 1 = b 4 then ∅ else Finset.univ \ {b 0, b 1, b 4}

def allowed (b : Row) : Finset Color :=
  (Finset.univ \ {b 3, b 4}) \ (banA b ∪ banD b)

/-- On proper C5 rows these equalities specify exactly the colour orbit of q. -/
def missing (b : Row) : Prop := b 0 = b 2 ∧ b 1 = b 3

instance (b : Row) : Decidable (missing b) := inferInstanceAs (Decidable (_ ∧ _))

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- Kernel reduction checks all 1,024 labeled rows, including improper rows.
/-- Applies only after the paper proof supplies the two exact forbidden-set laws. -/
theorem all_rows (b : Row) : proper b → ((allowed b).Nonempty ↔ ¬ missing b) := by
  revert b
  decide

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- Kernel reduction checks all 1,024 labeled rows, including improper rows.
theorem reflection_missing (b : Row) : missing (reflectRow b) ↔ missing b := by
  revert b
  decide

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- Kernel reduction checks all 1,024 labeled rows, including improper rows.
theorem reflection_proper (b : Row) : proper (reflectRow b) ↔ proper b := by
  revert b
  decide

/-- The reflected acceptance conclusion is transported, not independently classified. -/
theorem reflection_transport (accept acceptReflected : Row → Prop)
    (transport : ∀ b, acceptReflected (reflectRow b) ↔ accept b)
    (classification : ∀ b, proper b → (accept b ↔ ¬ missing b))
    (b : Row) (hb : proper b) :
    acceptReflected b ↔ ¬ missing b := by
  have h := transport (reflectRow b)
  rw [reflectRow_involutive, classification _ ((reflection_proper b).mpr hb),
    reflection_missing] at h
  exact h

end FiveBoundary.TwoSpokeSplitSupport
