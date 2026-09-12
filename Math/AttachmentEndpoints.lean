/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.AttachmentNormalForm

/-! # Compiling cyclic endpoint order

The packets here can be read from an embedding; they are not assumed to be automaton
fans. This file proves only the combinatorial compilation step. Extracting the cyclic
order premise from a topological disk embedding is NOT proved here. In particular,
this premise must not be used as the definition of a disk embedding.
-/

namespace FiveBoundary.GeometryDFA
open ColorDFA

/-- Arbitrary duplicate-free endpoint packets in boundary order generate the existing
normal form when their normalized inner labels have the cyclic three-block order.
The topology obligation is precisely `horder`, together with extraction of the packets. -/
theorem normalForm_of_endpoint_order (w : Word) (F : Fin 5 → List (Fin 3))
    (hn : ∀ i, (F i).Nodup) (hw : ∀ i, (F i).toFinset = w i)
    (o : Bool) (n a b c : ℕ)
    (horder : (((List.ofFn F).flatten).map (pos o)).rotate n = necklace a b c) :
    AttachmentNormalForm w := by
  let P := fun i => (F i).map (pos o)
  let ls := List.ofFn P
  have he : ls.flatten = ((List.ofFn F).flatten).map (pos o) := by
    simp only [ls, P, List.ofFn_eq_map, ← List.flatMap_def, List.map_flatMap]
  rw [← he] at horder
  have hinv := List.rotate_eq_iff.mp horder
  let s : NecklaceCuts := {
    orientation := o, a := a, b := b, c := c
    offset := (necklace a b c).length - n % (necklace a b c).length
    widths := ls.map List.length
    five := by simp [ls]
    total := by
      have hh := congrArg List.length horder
      simpa [List.length_flatten, necklace, Nat.add_assoc] using hh }
  have hp : s.packets = ls := by
    change cutPackets (ls.map List.length) _ = ls
    rw [← hinv]
    exact cutPackets_of_lengths ls
  have hpi : ∀ i, s.packet i = P i := by
    intro i
    simp only [NecklaceCuts.packet, hp, ls, List.getElem_ofFn]
  refine ⟨s, ?_, ?_⟩
  · intro i
    rw [hpi]
    exact List.Nodup.map (fun _ _ hh => pos_injective o hh) (hn i)
  · funext i
    simp only [NecklaceCuts.word, hpi, P]
    change (((F i).map (pos o)).map (pos o)).toFinset = w i
    simpa [List.map_map, Function.comp_def, pos_involutive] using hw i

/-- The Lean endpoint of the proposed disk-completeness proof. This is conditional on
cyclic endpoint order, not a theorem deriving that order from noncrossing arcs. -/
theorem annulusAccept_of_endpoint_order (w : Word) (F : Fin 5 → List (Fin 3))
    (hn : ∀ i, (F i).Nodup) (hw : ∀ i, (F i).toFinset = w i)
    (o : Bool) (n a b c : ℕ)
    (horder : (((List.ofFn F).flatten).map (pos o)).rotate n = necklace a b c) :
    AnnulusAccept w :=
  (annulusAccept_iff_normalForm w).mpr
    (normalForm_of_endpoint_order w F hn hw o n a b c horder)

end FiveBoundary.GeometryDFA
