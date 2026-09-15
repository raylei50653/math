/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.Enumeration

/-! XOR edge words of proper C5 boundary assignments (docs/c5_count_cone_bridge.md §1).
Colours are read as `Z₂²`; the edge word `q_j = b_j xor b_{j+1}` is the dual
three-edge-colouring seen by Dvořák–Lidický. Each parity word has exactly four proper
preimages, the four XOR translates of any one of them, and colour translation preserves the
extension count of every graph. Nothing here uses planarity or the dual graph. -/
namespace FiveBoundary.ParityWord
set_option maxRecDepth 100000

/-- Bitwise XOR on `Fin 4`, i.e. addition in `Z₂²`. -/
def xor4 (a b : Color) : Color :=
  ⟨a.val ^^^ b.val, Nat.xor_lt_two_pow (n := 2) a.isLt b.isLt⟩

theorem xor4_comm : ∀ a b : Color, xor4 a b = xor4 b a := by decide
theorem xor4_assoc : ∀ a b c : Color, xor4 (xor4 a b) c = xor4 a (xor4 b c) := by decide
@[simp] theorem xor4_self : ∀ a : Color, xor4 a a = 0 := by decide
@[simp] theorem xor4_zero : ∀ a : Color, xor4 a 0 = a := by decide
@[simp] theorem zero_xor4 : ∀ a : Color, xor4 0 a = a := by decide
@[simp] theorem xor4_cancel : ∀ a b : Color, xor4 a (xor4 a b) = b := by decide
theorem xor4_left_cancel : ∀ a b c : Color, xor4 a b = xor4 a c → b = c := by decide
theorem xor4_translate : ∀ c a b : Color, xor4 (xor4 c a) (xor4 c b) = xor4 a b := by decide

/-- Translation by `c` is a colour permutation (an involution). -/
def xorPerm (c : Color) : Equiv.Perm Color where
  toFun := xor4 c
  invFun := xor4 c
  left_inv := xor4_cancel c
  right_inv := xor4_cancel c

/-- The dual edge word of a boundary assignment. -/
def edgeWord (b : BoundaryColoring) : Fin 5 → Color := fun j => xor4 (b j) (b (j + 1))

/-- The colour translate `b ↦ c xor b`, as the existing colour action. -/
def translate (c : Color) (b : BoundaryColoring) : BoundaryColoring := colorAction (xorPerm c) b

@[simp] theorem translate_apply (c : Color) (b : BoundaryColoring) (i : Fin 5) :
    translate c b i = xor4 c (b i) := rfl

theorem edgeWord_translate (c : Color) (b : BoundaryColoring) :
    edgeWord (translate c b) = edgeWord b := by
  funext j
  simp [edgeWord, xor4_translate]

theorem translate_proper (c : Color) {b : BoundaryColoring} (h : Proper C5 b) :
    Proper C5 (translate c b) := colorAction_proper _ h

/-- Cyclic rotation of the boundary rotates the edge word. -/
theorem edgeWord_rotate (r : Fin 5) (b : BoundaryColoring) :
    edgeWord (fun i => b (i + r)) = fun j => edgeWord b (j + r) := by
  funext j
  simp [edgeWord, add_right_comm]

theorem edgeWord_step (b : BoundaryColoring) (j : Fin 5) :
    b (j + 1) = xor4 (b j) (edgeWord b j) := by
  simp [edgeWord]

/-- A boundary assignment is determined by its base colour and its edge word. -/
theorem eq_of_edgeWord {b b' : BoundaryColoring} (h0 : b 0 = b' 0)
    (hw : edgeWord b = edgeWord b') : b = b' := by
  have h1 : b 1 = b' 1 := by
    have e : b 1 = xor4 (b 0) (edgeWord b 0) := edgeWord_step b 0
    have e' : b' 1 = xor4 (b' 0) (edgeWord b' 0) := edgeWord_step b' 0
    rw [e, e', h0, hw]
  have h2 : b 2 = b' 2 := by
    have e : b 2 = xor4 (b 1) (edgeWord b 1) := edgeWord_step b 1
    have e' : b' 2 = xor4 (b' 1) (edgeWord b' 1) := edgeWord_step b' 1
    rw [e, e', h1, hw]
  have h3 : b 3 = b' 3 := by
    have e : b 3 = xor4 (b 2) (edgeWord b 2) := edgeWord_step b 2
    have e' : b' 3 = xor4 (b' 2) (edgeWord b' 2) := edgeWord_step b' 2
    rw [e, e', h2, hw]
  have h4 : b 4 = b' 4 := by
    have e : b 4 = xor4 (b 3) (edgeWord b 3) := edgeWord_step b 3
    have e' : b' 4 = xor4 (b' 3) (edgeWord b' 3) := edgeWord_step b' 3
    rw [e, e', h3, hw]
  funext i
  fin_cases i <;> assumption

/-- The proper assignments with a given edge word are exactly the four translates. -/
theorem fiber_eq_translates {b : BoundaryColoring} (hb : Proper C5 b) :
    properBoundary.filter (fun b' => edgeWord b' = edgeWord b) =
      Finset.univ.image (fun c => translate c b) := by
  ext b'
  simp only [Finset.mem_filter, properBoundary, Finset.mem_univ, true_and, Finset.mem_image]
  constructor
  · rintro ⟨hb', hw⟩
    refine ⟨xor4 (b' 0) (b 0), eq_of_edgeWord ?_ ?_⟩
    · simp [xor4_assoc]
    · rw [edgeWord_translate, hw]
  · rintro ⟨c, rfl⟩
    exact ⟨translate_proper c hb, edgeWord_translate c b⟩

theorem translate_injective (b : BoundaryColoring) :
    Function.Injective (fun c => translate c b) := by
  intro c c' h
  have := congrFun h 0
  simp only [translate_apply] at this
  rw [xor4_comm c, xor4_comm c'] at this
  exact xor4_left_cancel _ _ _ this

/-- Each parity word has exactly four proper preimages; the fibre is a colour orbit, so it
carries no extension-count information beyond one representative. -/
theorem fiber_card {b : BoundaryColoring} (hb : Proper C5 b) :
    (properBoundary.filter (fun b' => edgeWord b' = edgeWord b)).card = 4 := by
  rw [fiber_eq_translates hb, Finset.card_image_of_injective _ (translate_injective b)]
  rfl

/-! ### Extension counts are constant on fibres -/

/-- Number of proper colourings of `G` restricting to `b` on the boundary. -/
def extensionCount {n : ℕ} (G : SimpleGraph (Fin n)) [DecidableRel G.Adj] (B : Fin 5 ↪ Fin n)
    (b : BoundaryColoring) : ℕ :=
  (Finset.univ.filter (fun c => Proper G c ∧ boundaryColoring B c = b)).card

theorem extensionCount_colorAction {n : ℕ} (G : SimpleGraph (Fin n)) [DecidableRel G.Adj]
    (B : Fin 5 ↪ Fin n) (p : Equiv.Perm Color) (b : BoundaryColoring) :
    extensionCount G B (colorAction p b) = extensionCount G B b := by
  unfold extensionCount
  refine Finset.card_bij (fun c _ => p.symm ∘ c) ?_ ?_ ?_
  · intro c hc
    simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hc ⊢
    refine ⟨fun i j e eq => hc.1 i j e (p.symm.injective eq), ?_⟩
    funext i
    have := congrFun hc.2 i
    simp only [boundaryColoring, Function.comp, colorAction] at this ⊢
    rw [this]; simp
  · intro c _ c' _ h
    exact p.symm.injective.comp_left h
  · intro c hc
    simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hc
    refine ⟨p ∘ c, ?_, ?_⟩
    · simp only [Finset.mem_filter, Finset.mem_univ, true_and]
      refine ⟨fun i j e eq => hc.1 i j e (p.injective eq), ?_⟩
      rw [← hc.2]; rfl
    · funext i; simp

theorem extensionCount_translate {n : ℕ} (G : SimpleGraph (Fin n)) [DecidableRel G.Adj]
    (B : Fin 5 ↪ Fin n) (c : Color) (b : BoundaryColoring) :
    extensionCount G B (translate c b) = extensionCount G B b :=
  extensionCount_colorAction G B (xorPerm c) b

/-- Two proper assignments with the same edge word have the same extension count in every
graph: the literature's fixed dual-edge-colouring count equals our fixed-assignment count. -/
theorem extensionCount_of_edgeWord {n : ℕ} (G : SimpleGraph (Fin n)) [DecidableRel G.Adj]
    (B : Fin 5 ↪ Fin n) {b b' : BoundaryColoring} (hb : Proper C5 b) (hb' : Proper C5 b')
    (hw : edgeWord b' = edgeWord b) : extensionCount G B b' = extensionCount G B b := by
  have hmem : b' ∈ properBoundary.filter (fun b' => edgeWord b' = edgeWord b) := by
    simp [properBoundary, hb', hw]
  rw [fiber_eq_translates hb] at hmem
  obtain ⟨c, _, rfl⟩ := Finset.mem_image.mp hmem
  exact extensionCount_translate G B c b

/-! ### Parity words -/

/-- A parity word: no zero letter, and each nonzero letter used an odd number of times. -/
def IsParityWord (w : Fin 5 → Color) : Prop :=
  (∀ j, w j ≠ 0) ∧ ∀ c : Color, c ≠ 0 → Odd (Finset.univ.filter (fun j => w j = c)).card

instance (w : Fin 5 → Color) : Decidable (IsParityWord w) :=
  inferInstanceAs (Decidable (_ ∧ ∀ c : Color, c ≠ 0 → Odd _))

/-- Integrate a word from base colour `0`. -/
def integrate (w : Fin 5 → Color) : BoundaryColoring :=
  ![0, w 0, xor4 (w 0) (w 1), xor4 (xor4 (w 0) (w 1)) (w 2),
    xor4 (xor4 (xor4 (w 0) (w 1)) (w 2)) (w 3)]

theorem xorSum_zero_of_parity : ∀ w : Fin 5 → Color, IsParityWord w →
    xor4 (xor4 (xor4 (xor4 (w 0) (w 1)) (w 2)) (w 3)) (w 4) = 0 := by decide

theorem edgeWord_integrate : ∀ w : Fin 5 → Color, IsParityWord w →
    edgeWord (integrate w) = w := by decide

theorem integrate_proper : ∀ w : Fin 5 → Color, IsParityWord w → Proper C5 (integrate w) := by
  decide

theorem edgeWord_isParity : ∀ b : BoundaryColoring, Proper C5 b → IsParityWord (edgeWord b) := by
  decide

theorem parityWord_count : (Finset.univ.filter IsParityWord).card = 60 := by decide

/-- `240 = 4 · 60`: the fibres over the sixty parity words partition the proper assignments. -/
theorem fiber_partition :
    properBoundary = (Finset.univ.filter IsParityWord).biUnion
      (fun w => properBoundary.filter (fun b => edgeWord b = w)) := by
  ext b
  simp only [Finset.mem_biUnion, Finset.mem_filter, Finset.mem_univ, true_and, properBoundary]
  constructor
  · intro hb; exact ⟨edgeWord b, edgeWord_isParity b hb, hb, rfl⟩
  · rintro ⟨w, _, hb, _⟩; exact hb

/-! ### Literature anchors (Dvořák–Lidický, Conjecture 9) -/

/-- The `a` word `(1,1,2,3,1)` integrates to the singleton-3 three-colour state. -/
theorem word_a : integrate ![1, 1, 2, 3, 1] = ![0, 1, 0, 2, 1] := by decide

/-- The `b` word `(1,2,1,1,3)` integrates to the four-colour state with repeated pair `{2,4}`. -/
theorem word_b : integrate ![1, 2, 1, 1, 3] = ![0, 1, 3, 2, 3] := by decide

theorem word_a_singleton : (usedColors (integrate ![1, 1, 2, 3, 1])).card = 3 ∧
    integrate ![1, 1, 2, 3, 1] 0 = integrate ![1, 1, 2, 3, 1] 2 ∧
    integrate ![1, 1, 2, 3, 1] 1 = integrate ![1, 1, 2, 3, 1] 4 := by decide

theorem word_b_pair : (usedColors (integrate ![1, 2, 1, 1, 3])).card = 4 ∧
    integrate ![1, 2, 1, 1, 3] 2 = integrate ![1, 2, 1, 1, 3] 4 := by decide

end FiveBoundary.ParityWord
