/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.SplitCertificate

/-! Logical relations only: no assertion that composition preserves a disk embedding. -/
namespace FiveBoundary.Gadget

abbrev Rel (X Y : Type) := X → Y → Prop
def meet {X Y : Type} (r s : Rel X Y) : Rel X Y := fun x y => r x y ∧ s x y
def seq {X Y Z : Type} (r : Rel X Y) (s : Rel Y Z) : Rel X Z :=
  fun x z => ∃ y, r x y ∧ s y z
def identity (X : Type) : Rel X X := Eq
def hide {X H : Type} (r : X → H → Prop) : X → Prop := fun x => ∃ h, r x h

theorem seq_assoc {W X Y Z : Type} (r : Rel W X) (s : Rel X Y) (t : Rel Y Z) :
    seq (seq r s) t = seq r (seq s t) := by
  funext w z
  apply propext
  constructor
  · rintro ⟨y, ⟨x, hr, hs⟩, ht⟩
    exact ⟨x, hr, y, hs, ht⟩
  · rintro ⟨x, hr, y, hs, ht⟩
    exact ⟨y, ⟨x, hr, hs⟩, ht⟩

theorem seq_identity {X Y : Type} (r : Rel X Y) : seq r (identity Y) = r := by
  funext x y
  simp [seq, identity]

/-- Hiding must retain the SAME witness across constraints. -/
theorem hide_shared {X H : Type} (r s : X → H → Prop) :
    hide (fun x h => r x h ∧ s x h) = fun x => ∃ h, r x h ∧ s x h := rfl

def act {k : ℕ} (p : Equiv.Perm Color) (c : BoundaryAssignment k) : BoundaryAssignment k :=
  p ∘ c

def Equivariant {m n : ℕ} (r : Rel (BoundaryAssignment m) (BoundaryAssignment n)) : Prop :=
  ∀ p x y, r x y → r (act p x) (act p y)

def denote {v m n : ℕ} (g : SimpleGraph (Fin v))
    (input : Fin m → Fin v) (output : Fin n → Fin v) :
    Rel (BoundaryAssignment m) (BoundaryAssignment n) := fun x y =>
  ∃ c, Proper g c ∧ (∀ i, c (input i) = x i) ∧ (∀ j, c (output j) = y j)

theorem denote_equivariant {v m n : ℕ} (g : SimpleGraph (Fin v))
    (input : Fin m → Fin v) (output : Fin n → Fin v) :
    Equivariant (denote g input output) := by
  rintro p x y ⟨c, hp, hi, ho⟩
  refine ⟨p ∘ c, ?_, ?_, ?_⟩
  · intro i j he hh
    exact hp i j he (p.injective hh)
  · intro i
    exact congrArg p (hi i)
  · intro j
    exact congrArg p (ho j)

theorem seq_equivariant {m n k : ℕ}
    {r : Rel (BoundaryAssignment m) (BoundaryAssignment n)}
    {s : Rel (BoundaryAssignment n) (BoundaryAssignment k)}
    (hr : Equivariant r) (hs : Equivariant s) : Equivariant (seq r s) := by
  rintro p x z ⟨y, hxy, hyz⟩
  exact ⟨act p y, hr p x y hxy, hs p y z hyz⟩

theorem meet_equivariant {m n : ℕ}
    {r s : Rel (BoundaryAssignment m) (BoundaryAssignment n)}
    (hr : Equivariant r) (hs : Equivariant s) : Equivariant (meet r s) := by
  rintro p x y ⟨hx, hy⟩
  exact ⟨hr p x y hx, hs p x y hy⟩

end FiveBoundary.Gadget
