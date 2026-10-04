import Math.ExcessTwoColoring
import Math.ExcessTwoShape
import Math.ExcessTwoRotation

/-! # Soundness of the ES finite excess-two certificate checker

Closed graph checks live in GeneratedExcessTwoCertificates: positive checks use
`decide +kernel`, and only rejected rows use `native_decide`.
The reusable implication from the Boolean checker to the finite mathematical
predicates and the existing complete Sigma semantics is an ordinary Lean proof.
No statement here asserts enumeration completeness or a topological drawing. -/
namespace FiveBoundary.ExcessTwo
set_option linter.style.nativeDecide false
set_option linter.style.setOption false
set_option maxRecDepth 100000
set_option maxHeartbeats 0

structure Certificate where
  k : Nat
  edges : List (Fin (5 + k) × Fin (5 + k))
  kind : DegreeType
  sigmaMask : Nat
  q : List Nat
  qComponents : Nat
  rotation : RotationData
  accepted : Fin 10 → Option (Fin (5 + k) → Color)
  deletions : List (DeletionWitness k)

def natEdges (c : Certificate) : List Edge :=
  c.edges.map fun e => (e.1.val, e.2.val)

def DeletionsCover (c : Certificate) : Prop :=
  ∀ e ∈ c.edges, 5 ≤ e.2.val → ∃ d ∈ c.deletions, d.edge = e

instance (c : Certificate) : Decidable (DeletionsCover c) := by
  unfold DeletionsCover
  infer_instance

def StructureConditions (c : Certificate) : Prop :=
  ShapeConditions (5 + c.k) (natEdges c) c.kind ∧
  QConditions c.sigmaMask c.q c.qComponents ∧
  RotationValid (5 + c.k) (natEdges c) c.rotation ∧
  boundaryIsCycle (graphOfEdges c.edges) (boundaryEmbedding c.k) ∧
  DeletionsCover c

instance (c : Certificate) : Decidable (StructureConditions c) := by
  unfold StructureConditions
  infer_instance

/-- All data used by the checker refer to one literal labelled graph. -/
def check (c : Certificate) : Bool :=
  decide (StructureConditions c) &&
  (List.finRange 10).all (checkRow c.edges c.sigmaMask c.accepted) &&
  c.deletions.all (checkDeletion c.edges c.sigmaMask)

/-- Inexpensive positive witnesses and all structural/rotation claims. -/
def checkPositive (c : Certificate) : Bool :=
  decide (StructureConditions c) &&
  (List.finRange 10).all (fun i =>
    if maskBit c.sigmaMask i then checkAccepted c.edges i (c.accepted i) else true) &&
  c.deletions.all (checkDeletion c.edges c.sigmaMask)

/-- Only absence claims invoke the exhaustive interior function space. -/
def checkRejected (c : Certificate) : Bool :=
  (List.finRange 10).all (fun i =>
    if maskBit c.sigmaMask i then true else decide (¬ Extends c.edges i))

theorem check_from_parts (c : Certificate)
    (hp : checkPositive c = true) (hn : checkRejected c = true) : check c = true := by
  simp only [checkPositive, Bool.and_eq_true] at hp
  simp only [check, Bool.and_eq_true]
  refine ⟨⟨hp.1.1, ?_⟩, hp.2⟩
  apply List.all_eq_true.mpr
  intro i hi
  have ha := List.all_eq_true.mp hp.1.2 i hi
  have hr := List.all_eq_true.mp hn i hi
  unfold checkRow
  split
  next hm => simpa [hm] using ha
  next hm => simpa [hm] using hr

/-- These are finite labelled graph and combinatorial embedding statements.
    `RotationValid` has no conclusion about a topological planar disk. -/
def CertificateFacts (c : Certificate) : Prop :=
  StructureConditions c ∧
  Sigma (graphOfEdges c.edges) (boundaryEmbedding c.k) = expectedSigma c.sigmaMask ∧
  ∀ e ∈ c.edges, 5 ≤ e.2.val →
    ∃ b, b ∈ Sigma (graphOfEdges (c.edges.filter (· ≠ e))) (boundaryEmbedding c.k) ∧
      b ∉ Sigma (graphOfEdges c.edges) (boundaryEmbedding c.k)

/-- Soundness for the ten exact representatives, without using the imported
    native-decide theorem about their complete S4 orbit cover. -/
def FiniteCertificateFacts (c : Certificate) : Prop :=
  StructureConditions c ∧
  (∀ i : Fin 10,
    boundaryRow i ∈ Sigma (graphOfEdges c.edges) (boundaryEmbedding c.k) ↔
      maskBit c.sigmaMask i = true) ∧
  ∀ e ∈ c.edges, 5 ≤ e.2.val →
    ∃ b, b ∈ Sigma (graphOfEdges (c.edges.filter (· ≠ e))) (boundaryEmbedding c.k) ∧
      b ∉ Sigma (graphOfEdges c.edges) (boundaryEmbedding c.k)

/-- Ordinary soundness bridge. All absence claims are supplied by the actual
    exhaustive finite decision procedure in `checkRow`, never by JSON flags. -/
theorem check_finite_sound (c : Certificate) (h : check c = true) : FiniteCertificateFacts c := by
  simp only [check, Bool.and_eq_true] at h
  have hs : StructureConditions c := of_decide_eq_true h.1.1
  have hrows : ∀ i : Fin 10,
      boundaryRow i ∈ Sigma (graphOfEdges c.edges) (boundaryEmbedding c.k) ↔
        maskBit c.sigmaMask i = true := by
    intro i
    exact row_sound c.edges hs.2.2.2.1 c.sigmaMask c.accepted i
      (List.all_eq_true.mp h.1.2 i (List.mem_finRange i))
  refine ⟨hs, hrows, ?_⟩
  intro e he hnonframe
  obtain ⟨d, hd, hde⟩ := hs.2.2.2.2 e he hnonframe
  have hx := deletion_sound c.edges c.sigmaMask hrows d
    (List.all_eq_true.mp h.2 d hd)
  simpa only [hde] using hx

/-- Complete raw Sigma follows by one global colour permutation. This ordinary
    proof inherits the explicitly native-decide S4 cover from Enumeration. -/
theorem check_sound (c : Certificate) (h : check c = true) : CertificateFacts c := by
  obtain ⟨hs, hrows, hdelete⟩ := check_finite_sound c h
  exact ⟨hs, rows_exact_sigma c.edges hs.2.2.2.1 c.sigmaMask hrows, hdelete⟩

end FiveBoundary.ExcessTwo
