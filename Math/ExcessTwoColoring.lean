import Math.SplitCertificate
import Math.State

/-! ES colouring semantics. The closed absence checks use native_decide in the
    generated file; the soundness bridges below are ordinary Lean proofs. -/
namespace FiveBoundary.ExcessTwo
set_option linter.style.nativeDecide false
set_option linter.style.setOption false
set_option maxRecDepth 100000
set_option maxHeartbeats 0

def boundaryRow (i : Fin 10) : BoundaryColoring :=
  ![![0,1,0,1,2], ![0,1,0,2,1], ![0,1,0,2,3], ![0,1,2,0,1], ![0,1,2,0,2],
    ![0,1,2,0,3], ![0,1,2,1,2], ![0,1,2,1,3], ![0,1,2,3,1], ![0,1,2,3,2]] i

def maskBit (mask : Nat) (i : Fin 10) : Bool := mask.testBit i.val

def boundaryEmbedding (k : Nat) : Fin 5 ↪ Fin (5 + k) :=
  firstBoundary (Nat.le_add_right 5 k)

def Extends {k : Nat} (edges : List (Fin (5 + k) × Fin (5 + k)))
    (i : Fin 10) : Prop :=
  ∃ inside : Fin k → Color, edgeCheck edges (Fin.append (boundaryRow i) inside) = true

instance {k : Nat} (edges : List (Fin (5 + k) × Fin (5 + k))) (i : Fin 10) :
    Decidable (Extends edges i) := inferInstanceAs (Decidable (∃ inside : Fin k → Color,
      edgeCheck edges (Fin.append (boundaryRow i) inside) = true))

def checkAccepted {k : Nat} (edges : List (Fin (5 + k) × Fin (5 + k)))
    (i : Fin 10) (witness : Option (Fin (5 + k) → Color)) : Bool :=
  match witness with
  | none => false
  | some c => edgeCheck edges c && decide (boundaryColoring (boundaryEmbedding k) c = boundaryRow i)

def checkRow {k : Nat} (edges : List (Fin (5 + k) × Fin (5 + k)))
    (mask : Nat) (witness : Fin 10 → Option (Fin (5 + k) → Color)) (i : Fin 10) : Bool :=
  if maskBit mask i then checkAccepted edges i (witness i) else decide (¬ Extends edges i)

theorem extends_iff_sigma {k : Nat} (edges : List (Fin (5 + k) × Fin (5 + k)))
    (hB : boundaryIsCycle (graphOfEdges edges) (boundaryEmbedding k)) (i : Fin 10) :
    Extends edges i ↔ boundaryRow i ∈ Sigma (graphOfEdges edges) (boundaryEmbedding k) := by
  have hp : Proper C5 (boundaryRow i) := by fin_cases i <;> decide +kernel
  unfold boundaryEmbedding at *
  rw [← splitSigma_exact edges hB]
  simp only [splitSigma, Finset.mem_filter, properBoundary, Finset.mem_univ,
    true_and, hp]
  rfl

theorem accepted_sound {k : Nat} (edges : List (Fin (5 + k) × Fin (5 + k)))
    (i : Fin 10) (witness : Option (Fin (5 + k) → Color))
    (h : checkAccepted edges i witness = true) :
    boundaryRow i ∈ Sigma (graphOfEdges edges) (boundaryEmbedding k) := by
  cases witness with
  | none => simp [checkAccepted] at h
  | some c =>
    simp only [checkAccepted, Bool.and_eq_true, decide_eq_true_eq] at h
    exact ⟨c, (edgeCheck_exact _ _).mp h.1, h.2⟩

theorem row_sound {k : Nat} (edges : List (Fin (5 + k) × Fin (5 + k)))
    (hB : boundaryIsCycle (graphOfEdges edges) (boundaryEmbedding k))
    (mask : Nat) (witness : Fin 10 → Option (Fin (5 + k) → Color)) (i : Fin 10)
    (h : checkRow edges mask witness i = true) :
    boundaryRow i ∈ Sigma (graphOfEdges edges) (boundaryEmbedding k) ↔ maskBit mask i = true := by
  unfold checkRow at h
  split at h
  next hm => exact ⟨fun _ => hm, fun _ => accepted_sound edges i (witness i) h⟩
  next hm =>
    have hn : ¬ Extends edges i := of_decide_eq_true h
    rw [extends_iff_sigma edges hB i] at hn
    simp only [hn, false_iff]
    exact hm

def expectedSigma (mask : Nat) : Set BoundaryColoring :=
  {b | ∃ i : Fin 10, maskBit mask i = true ∧ b ∈ colorOrbit (boundaryRow i)}

theorem boundaryRow_cover (r : BoundaryColoring) (h : r ∈ colorReps) :
    ∃ i : Fin 10, boundaryRow i = r := by
  have hc : ∀ r ∈ colorReps, ∃ i : Fin 10, boundaryRow i = r := by decide +kernel
  exact hc r h

theorem rows_exact_sigma {k : Nat} (edges : List (Fin (5 + k) × Fin (5 + k)))
    (hB : boundaryIsCycle (graphOfEdges edges) (boundaryEmbedding k))
    (mask : Nat) (h : ∀ i : Fin 10,
      boundaryRow i ∈ Sigma (graphOfEdges edges) (boundaryEmbedding k) ↔ maskBit mask i = true) :
    Sigma (graphOfEdges edges) (boundaryEmbedding k) = expectedSigma mask := by
  ext b
  constructor
  · intro hb
    have hproper : b ∈ properBoundary := by
      obtain ⟨c, hc, rfl⟩ := hb
      exact Finset.mem_filter.mpr ⟨Finset.mem_univ _, restrict_proper hB hc⟩
    rw [← color_orbits_cover] at hproper
    obtain ⟨r, hr, hp⟩ := Finset.mem_biUnion.mp hproper
    obtain ⟨i, rfl⟩ := boundaryRow_cover r hr
    obtain ⟨p, _, heq⟩ := Finset.mem_image.mp hp
    have hi := sigma_color_invariant (graphOfEdges edges) (boundaryEmbedding k) p.symm hb
    rw [← heq] at hi
    have hir : boundaryRow i ∈ Sigma (graphOfEdges edges) (boundaryEmbedding k) := by
      simpa [colorAction, Function.comp_def] using hi
    exact ⟨i, (h i).mp hir, Finset.mem_image.mpr ⟨p, Finset.mem_univ _, heq⟩⟩
  · rintro ⟨i, hm, hb⟩
    obtain ⟨p, _, rfl⟩ := Finset.mem_image.mp hb
    exact sigma_color_invariant (graphOfEdges edges) (boundaryEmbedding k) p ((h i).mpr hm)

structure RowWitness (k : Nat) where
  row : Fin 10
  coloring : Fin (5 + k) → Color

structure DeletionWitness (k : Nat) where
  edge : Fin (5 + k) × Fin (5 + k)
  witnesses : List (RowWitness k)

def checkDeletion {k : Nat} (edges : List (Fin (5 + k) × Fin (5 + k)))
    (mask : Nat) (d : DeletionWitness k) : Bool :=
  decide (d.edge ∈ edges ∧ 5 ≤ d.edge.2.val) && !d.witnesses.isEmpty &&
    d.witnesses.all (fun w => !maskBit mask w.row &&
      checkAccepted (edges.filter (· ≠ d.edge)) w.row (some w.coloring))

theorem deletion_sound {k : Nat} (edges : List (Fin (5 + k) × Fin (5 + k)))
    (mask : Nat) (hrows : ∀ i : Fin 10,
      boundaryRow i ∈ Sigma (graphOfEdges edges) (boundaryEmbedding k) ↔ maskBit mask i = true)
    (d : DeletionWitness k) (h : checkDeletion edges mask d = true) :
    ∃ b, b ∈ Sigma (graphOfEdges (edges.filter (· ≠ d.edge))) (boundaryEmbedding k) ∧
      b ∉ Sigma (graphOfEdges edges) (boundaryEmbedding k) := by
  simp only [checkDeletion, Bool.and_eq_true] at h
  have hn : d.witnesses ≠ [] := by simpa using h.1.2
  obtain ⟨w, hw⟩ := List.exists_mem_of_ne_nil d.witnesses hn
  have hh := List.all_eq_true.mp h.2 w hw
  simp only [Bool.and_eq_true, Bool.not_eq_true'] at hh
  refine ⟨boundaryRow w.row, accepted_sound _ _ _ hh.2, ?_⟩
  intro hb
  have hm := (hrows w.row).mp hb
  rw [hh.1] at hm
  contradiction

end FiveBoundary.ExcessTwo
