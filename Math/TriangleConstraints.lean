/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.PrimitiveGadgets

/-! Readable rejection certificates: adjacent vertices cannot share too few colors. -/
set_option linter.style.nativeDecide false
set_option linter.style.setOption false
namespace FiveBoundary.Gadget
set_option maxRecDepth 100000
set_option maxHeartbeats 0

abbrev Links := Fin 3 → Finset (Fin 5)
def Allowed (links : Links) (b : BoundaryColoring) (i : Fin 3) (c : Color) : Prop :=
  ∀ j ∈ links i, c ≠ b j
def TriangleCan (links : Links) (b : BoundaryColoring) : Prop :=
  ∃ t : Fin 3 → Color, Function.Injective t ∧ ∀ i, Allowed links b i (t i)

theorem pigeonhole_rejection (links : Links) (b : BoundaryColoring)
    (vertices : Finset (Fin 3)) (colors : Finset Color)
    (small : colors.card < vertices.card)
    (covers : ∀ i ∈ vertices, ∀ c, Allowed links b i c → c ∈ colors) :
    ¬ TriangleCan links b := by
  rintro ⟨t, ht, ha⟩
  have hle : vertices.card ≤ colors.card := by
    calc
      vertices.card = (vertices.image t).card := (Finset.card_image_of_injective _ ht).symm
      _ ≤ colors.card := Finset.card_le_card (by
        intro c hc
        obtain ⟨i, hi, rfl⟩ := Finset.mem_image.mp hc
        exact covers i hi (t i) (ha i))
  exact (Nat.not_lt_of_ge hle) small

def leftLinks : Links := ![{0,1,2}, {0,3,4}, {2,3}]
def rightLinks : Links := ![{0,1}, {0,4}, {1,2,3}]

structure Obstruction where
  links : Links
  boundary : BoundaryColoring
  vertices : Finset (Fin 3)
  colors : Finset Color

def checkObstruction (o : Obstruction) : Bool :=
  decide (o.colors.card < o.vertices.card ∧
    ∀ i ∈ o.vertices, ∀ c, (∀ j ∈ o.links i, c ≠ o.boundary j) → c ∈ o.colors)

theorem obstruction_sound (o : Obstruction) (h : checkObstruction o = true) :
    ¬ TriangleCan o.links o.boundary := by
  simp only [checkObstruction, decide_eq_true_eq] at h
  exact pigeonhole_rejection o.links o.boundary o.vertices o.colors h.1 h.2

def obstructions : List Obstruction := [
  ⟨leftLinks, ![0,1,0,1,2], {0,1,2}, {2,3}⟩,
  ⟨leftLinks, ![0,1,2,0,2], {0,1,2}, {1,3}⟩,
  ⟨leftLinks, ![0,1,2,1,2], {0,1}, {3}⟩,
  ⟨rightLinks, ![0,1,0,2,1], {0,1,2}, {2,3}⟩,
  ⟨rightLinks, ![0,1,2,0,1], {0,1,2}, {2,3}⟩]

theorem obstructions_checked : obstructions.all checkObstruction = true := by decide +kernel
theorem all_obstructions_sound (o : Obstruction) (h : o ∈ obstructions) :
    ¬ TriangleCan o.links o.boundary :=
  obstruction_sound o ((List.all_eq_true.mp obstructions_checked) o h)

/-- Concrete compiler from exclusion links to graph edges. -/
def triangleEdges (links : Links) : List (Fin 8 × Fin 8) :=
  [(0,1),(0,4),(1,2),(2,3),(3,4),(5,6),(5,7),(6,7)] ++
    (List.finRange 3).flatMap (fun i =>
      (List.finRange 5).filterMap (fun j =>
        if j ∈ links i then some (Fin.castLE (by omega) j, Fin.natAdd 5 i) else none))

/-- Exact graph/compiler agreement for BOTH synthesized components and every boundary. -/
theorem compiled_components_checked : [leftLinks, rightLinks].all (fun links =>
    let actual := splitSigma (k := 3) (triangleEdges links)
    decide (∀ b : BoundaryColoring,
      b ∈ actual ↔
        Proper C5 b ∧ (∃ t : Fin 3 → Color,
          Function.Injective t ∧ ∀ i, ∀ j ∈ links i, t i ≠ b j))) = true := by native_decide

theorem compiled_meaning (links : Links) (h : links ∈ [leftLinks, rightLinks])
    (b : BoundaryColoring) :
    b ∈ splitSigma (k := 3) (triangleEdges links) ↔ Proper C5 b ∧ TriangleCan links b := by
  have checked := (List.all_eq_true.mp compiled_components_checked) links h
  exact (of_decide_eq_true checked) b

end FiveBoundary.Gadget
