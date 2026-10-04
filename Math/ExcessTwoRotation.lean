/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Mathlib.Data.List.Basic

/-! # Finite rotation-system certificates for the excess-two representatives

The checker consumes explicit clockwise neighbour lists and explicit face walks.
It checks the two directed darts of every undirected edge exactly once, and the
actual face-successor rule at every step.  It also checks Euler's equation and a
specified outer face equal to the boundary five-cycle.  Thus its conclusion is a
finite combinatorial embedding certificate; this file does not state or prove
a theorem about topological planar drawings or disks.

`checkRotation_sound` is an ordinary proof by unfolding `decide`.  Concrete
checks may be proved by `decide +kernel` or separately labelled `native_decide`.
-/

namespace FiveBoundary.ExcessTwo

/-- Clockwise neighbour lists indexed by vertex, the complete face walks, and
    the face designated as the outside of the disk certificate. -/
structure RotationData where
  rotation : List (List Nat)
  faces : List (List Nat)
  outerFace : List Nat
  deriving Repr, DecidableEq

/-- Consecutive cyclic pairs, including the final-to-first pair.  Empty lists
    give no pairs; singleton lists give their single self-pair. -/
def cyclePairs {α : Type} (xs : List α) : List (α × α) :=
  xs.zip (xs.drop 1 ++ xs.take 1)

/-- The complete directed-dart list supplied by undirected edges. -/
def edgeDarts (edges : List (Nat × Nat)) : List (Nat × Nat) :=
  edges.flatMap fun e => [e, (e.2, e.1)]

/-- The neighbour ring at a vertex.  An out-of-range lookup gives the empty
    list, while the checker separately enforces the exact number of rings. -/
def rotationAt (r : RotationData) (v : Nat) : List Nat :=
  (r.rotation[v]?).getD []

/-- A face advances from `(u,v)` to `(v,w)` where `w` immediately precedes
    `u` in the clockwise ring at `v`.  This is the counterclockwise incoming
    successor convention used by the exported ES `disk_rotation`. -/
def faceStep (r : RotationData) (d e : Nat × Nat) : Prop :=
  e.1 = d.2 ∧ (e.2, d.1) ∈ cyclePairs (rotationAt r d.2)

/-- No loops, no duplicate undirected edges, canonical endpoint order, and
    endpoints in the stated finite vertex range. -/
def rotationEdgesValid (n : Nat) (edges : List (Nat × Nat)) : Prop :=
  edges.Nodup ∧ ∀ e ∈ edges, e.1 < e.2 ∧ e.2 < n

/-- At every vertex the clockwise list contains precisely the graph
    neighbours, each once. -/
def rotationRingsValid (n : Nat) (edges : List (Nat × Nat))
    (r : RotationData) : Prop :=
  r.rotation.length = n ∧ ∀ v ∈ List.range n,
    (rotationAt r v).Nodup ∧
    (∀ u ∈ rotationAt r v, (v, u) ∈ edgeDarts edges) ∧
    (∀ d ∈ edgeDarts edges, d.1 = v → d.2 ∈ rotationAt r v)

/-- Flattened face darts partition the graph darts, with no repetition.
    Face walks need not have distinct vertices: bridges can appear twice in
    a face, but the directed darts must still be distinct. -/
def rotationFacesPartition (edges : List (Nat × Nat))
    (r : RotationData) : Prop :=
  let ds := r.faces.flatMap cyclePairs
  (∀ face ∈ r.faces, face ≠ []) ∧ ds.Nodup ∧
    (∀ d ∈ ds, d ∈ edgeDarts edges) ∧
    (∀ d ∈ edgeDarts edges, d ∈ ds)

/-- Every consecutive pair of face darts follows the supplied rotation.
    The cyclic pairing also checks closure of each face walk. -/
def rotationFaceWalks (r : RotationData) : Prop :=
  ∀ face ∈ r.faces, ∀ step ∈ cyclePairs (cyclePairs face),
    faceStep r step.1 step.2

/-- The designated outside is either orientation of the frame C5, and is
    an actual listed face, up to cyclic choice of starting vertex. -/
def rotationOuterFrame (r : RotationData) : Prop :=
  (r.outerFace = [0, 1, 2, 3, 4] ∨ r.outerFace = [0, 4, 3, 2, 1]) ∧
    ∃ face ∈ r.faces,
      r.outerFace ∈ (List.range face.length).map (fun i => face.rotate i)

/-- The complete finite combinatorial embedding predicate.  Connectedness
    is checked by the graph certificate which consumes this rotation data;
    this predicate itself makes no topological planarity assertion. -/
def RotationValid (n : Nat) (edges : List (Nat × Nat))
    (r : RotationData) : Prop :=
  rotationEdgesValid n edges ∧ rotationRingsValid n edges r ∧
    rotationFacesPartition edges r ∧ rotationFaceWalks r ∧
    n + r.faces.length = edges.length + 2 ∧ rotationOuterFrame r

instance (r : RotationData) (d e : Nat × Nat) : Decidable (faceStep r d e) :=
  inferInstanceAs (Decidable (e.1 = d.2 ∧
    (e.2, d.1) ∈ cyclePairs (rotationAt r d.2)))

instance (n : Nat) (edges : List (Nat × Nat)) :
    Decidable (rotationEdgesValid n edges) := by
  unfold rotationEdgesValid
  infer_instance

instance (n : Nat) (edges : List (Nat × Nat)) (r : RotationData) :
    Decidable (rotationRingsValid n edges r) := by
  unfold rotationRingsValid
  infer_instance

instance (edges : List (Nat × Nat)) (r : RotationData) :
    Decidable (rotationFacesPartition edges r) := by
  unfold rotationFacesPartition
  infer_instance

instance (r : RotationData) : Decidable (rotationFaceWalks r) := by
  unfold rotationFaceWalks
  infer_instance

instance (r : RotationData) : Decidable (rotationOuterFrame r) := by
  unfold rotationOuterFrame
  infer_instance

instance (n : Nat) (edges : List (Nat × Nat)) (r : RotationData) :
    Decidable (RotationValid n edges r) := by
  unfold RotationValid
  infer_instance

/-- Evaluate the finite rotation, face-partition, Euler, and outer-frame
    conditions directly on the supplied graph and certificate data. -/
def checkRotation (n : Nat) (edges : List (Nat × Nat))
    (r : RotationData) : Bool :=
  decide (RotationValid n edges r)

/-- An ordinary kernel proof connects the Boolean checker to its explicit
    finite predicate.  It adds no native-computation axiom. -/
theorem checkRotation_sound (n : Nat) (edges : List (Nat × Nat))
    (r : RotationData) (h : checkRotation n edges r = true) :
    RotationValid n edges r := by
  simpa only [checkRotation, decide_eq_true_eq] using h

theorem checkRotation_iff (n : Nat) (edges : List (Nat × Nat))
    (r : RotationData) :
    checkRotation n edges r = true ↔ RotationValid n edges r := by
  simp only [checkRotation, decide_eq_true_eq]

end FiveBoundary.ExcessTwo
