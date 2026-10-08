/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.Enumeration

/-!
Finite structural controls for the ES excess-two certificates. Vertices are
literal natural-number labels: the boundary is 0,1,2,3,4, followed by the
interior vertices. These definitions neither enumerate graph isomorphism
classes nor assert that a finite source search is complete.
-/
namespace FiveBoundary.ExcessTwo

abbrev Edge := Nat × Nat

/-- NA and AD have degree-five roots at 5,6; D6 has a degree-six root at 5. -/
inductive DegreeType where
  | na | ad | d6
  deriving DecidableEq, Repr

/-- The original ES row order, in one common labelled colour frame. -/
def rows : List (List Nat) :=
  [[0,1,0,1,2], [0,1,0,2,1], [0,1,0,2,3], [0,1,2,0,1],
   [0,1,2,0,2], [0,1,2,0,3], [0,1,2,1,2], [0,1,2,1,3],
   [0,1,2,3,1], [0,1,2,3,2]]

/-- The same rows in the existing `BoundaryColoring` type. -/
def boundaryRows : List BoundaryColoring :=
  [![0,1,0,1,2], ![0,1,0,2,1], ![0,1,0,2,3], ![0,1,2,0,1],
   ![0,1,2,0,2], ![0,1,2,0,3], ![0,1,2,1,2], ![0,1,2,1,3],
   ![0,1,2,3,1], ![0,1,2,3,2]]

def frameEdges : List Edge := [(0,1), (0,4), (1,2), (2,3), (3,4)]

def isFrameEdge (e : Edge) : Bool := frameEdges.contains e

def edgeLt (a b : Edge) : Prop := a.1 < b.1 ∨ (a.1 = b.1 ∧ a.2 < b.2)

instance : DecidableRel edgeLt := fun a b =>
  inferInstanceAs (Decidable (a.1 < b.1 ∨ (a.1 = b.1 ∧ a.2 < b.2)))

/-- Undirected adjacency; validity is checked separately, including no loops. -/
def adjacent (edges : List Edge) (u v : Nat) : Bool :=
  edges.contains (min u v, max u v)

def interior (n : Nat) : List Nat := (List.range n).drop 5

def degree (edges : List Edge) (v : Nat) : Nat :=
  (edges.filter fun e => e.1 == v || e.2 == v).length

def spokes (edges : List Edge) (v : Nat) : Nat :=
  (edges.filter fun e =>
    (e.1 == v && e.2 < 5) || (e.2 == v && e.1 < 5)).length

/-- Exact prescribed degree, with roots kept in their original labelled roles. -/
def prescribedDegree (kind : DegreeType) (v : Nat) : Nat :=
  match kind with
  | .d6 => if v == 5 then 6 else 4
  | .na | .ad => if v == 5 || v == 6 then 5 else 4

/-- Expand the visited set by one interior edge; boundary vertices never join it. -/
def expandInterior (n : Nat) (edges : List Edge) (seen : List Nat) : List Nat :=
  (interior n).filter fun v =>
    seen.contains v || seen.any fun u => adjacent edges u v

/-- At most `fuel` expansion steps starting at the literal first interior vertex. -/
def reachInterior (n : Nat) (edges : List Edge) : Nat → List Nat
  | 0 => [5]
  | fuel + 1 => expandInterior n edges (reachInterior n edges fuel)

/-- Reaching every interior label in `n - 5` steps certifies interior connectivity. -/
def connectedInterior (n : Nat) (edges : List Edge) : Bool :=
  (interior n).all fun v => (reachInterior n edges (n - 5)).contains v

/-- An actual interior path from the first interior vertex; every extension is
an edge and its new endpoint is an interior label below `n`. -/
inductive InteriorPath (n : Nat) (edges : List Edge) : Nat → Prop where
  | root (h : 5 < n) : InteriorPath n edges 5
  | step {u v : Nat} (prior : InteriorPath n edges u)
      (inside : v ∈ interior n) (edge : adjacent edges u v = true) :
      InteriorPath n edges v

theorem reachInterior_sound (n : Nat) (edges : List Edge) (hn : 5 < n)
    (fuel v : Nat) (h : v ∈ reachInterior n edges fuel) : InteriorPath n edges v := by
  induction fuel generalizing v with
  | zero =>
      have hv : v = 5 := List.mem_singleton.mp h
      subst v
      exact InteriorPath.root hn
  | succ fuel ih =>
      have hm := List.mem_filter.mp h
      rcases Bool.or_eq_true _ _ |>.mp hm.2 with hold | hnew
      · exact ih v (List.contains_iff_mem.mp hold)
      · obtain ⟨u, hu, hedge⟩ := List.any_eq_true.mp hnew
        exact InteriorPath.step (ih u hu) hm.1 hedge

/-- Boolean connectivity supplies a path for each interior vertex, by an
ordinary Lean induction rather than an external graph-library assertion. -/
theorem connectedInterior_sound (n : Nat) (edges : List Edge) (hn : 5 < n)
    (h : connectedInterior n edges = true) :
    ∀ v ∈ interior n, InteriorPath n edges v := by
  intro v hv
  have hr := List.all_eq_true.mp h v hv
  exact reachInterior_sound n edges hn (n - 5) v (List.contains_iff_mem.mp hr)

/-- Excess above degree four. Exact degrees ensure these subtractions lose nothing. -/
def excess (n : Nat) (edges : List Edge) : Nat :=
  ((interior n).map fun v => degree edges v - 4).foldl (· + ·) 0

/-- All finite structural requirements, before any colouring or embedding checks. -/
def ShapeConditions (n : Nat) (edges : List Edge) (kind : DegreeType) : Prop :=
  5 < n ∧
  edges.Pairwise edgeLt ∧
  (∀ e ∈ edges, e.1 < e.2 ∧ e.2 < n) ∧
  edges.filter (fun e => e.2 < 5) = frameEdges ∧
  (∀ v ∈ interior n, degree edges v = prescribedDegree kind v ∧ spokes edges v ≤ 3) ∧
  excess n edges = 2 ∧
  connectedInterior n edges = true ∧
  (match kind with
   | .na => 7 ≤ n ∧ adjacent edges 5 6 = false
   | .ad => 7 ≤ n ∧ adjacent edges 5 6 = true
   | .d6 => True) ∧
  (∃ e ∈ edges, e.1 < 5 ∧ 5 ≤ e.2)

instance (n : Nat) (edges : List Edge) (kind : DegreeType) :
    Decidable (ShapeConditions n edges kind) := by
  unfold ShapeConditions
  cases kind <;> infer_instance

def checkShape (n : Nat) (edges : List Edge) (kind : DegreeType) : Bool :=
  decide (ShapeConditions n edges kind)

/-- An ordinary proof extracting the exact finite statement from the checker. -/
theorem checkShape_sound (n : Nat) (edges : List Edge) (kind : DegreeType)
    (h : checkShape n edges kind = true) : ShapeConditions n edges kind := by
  exact of_decide_eq_true h

theorem checkShape_interior_paths (n : Nat) (edges : List Edge) (kind : DegreeType)
    (h : checkShape n edges kind = true) :
    ∀ v ∈ interior n, InteriorPath n edges v := by
  obtain ⟨hn, _, _, _, _, _, hc, _⟩ := checkShape_sound n edges kind h
  exact connectedInterior_sound n edges hn hc

/-- Bit `i` has precisely the original ES row index, without a per-graph renaming. -/
def maskAccepts (mask i : Nat) : Bool := mask.testBit i

/-- ES `REJ_IDX`: the three-colour row whose singleton is boundary position `p`. -/
def singletonRowIndices : List Nat := [6,4,3,1,0]

/-- The five four-colour rows; their ES bit mask is 932. -/
def t4RowIndices : List Nat := [2,5,7,8,9]

def missingPositions (mask : Nat) : List Nat :=
  (List.range 5).filter fun p => !maskAccepts mask (singletonRowIndices[p]!)

/-- Cyclic components: for a proper subset, `|Q|` minus its retained frame edges. -/
def cyclicComponents (q : List Nat) : Nat :=
  if q.length == 5 then 1
  else q.length - ((List.range 5).filter fun p =>
    q.contains p && q.contains ((p + 1) % 5)).length

/-- Q is the exact named rejection set, with all T4 rows accepted. -/
def QConditions (mask : Nat) (q : List Nat) (qComponents : Nat) : Prop :=
  mask < 1024 ∧
  (∀ i ∈ t4RowIndices, maskAccepts mask i = true) ∧
  q = missingPositions mask ∧
  q ≠ [] ∧
  qComponents = cyclicComponents q ∧
  q.length + qComponents ≤ 4

instance (mask : Nat) (q : List Nat) (qComponents : Nat) :
    Decidable (QConditions mask q qComponents) := by
  unfold QConditions
  infer_instance

def checkQ (mask : Nat) (q : List Nat) (qComponents : Nat) : Bool :=
  decide (QConditions mask q qComponents)

theorem checkQ_sound (mask : Nat) (q : List Nat) (qComponents : Nat)
    (h : checkQ mask q qComponents = true) : QConditions mask q qComponents := by
  exact of_decide_eq_true h

/-- Fixed row data agrees with the established boundary-colouring type. -/
theorem rows_match_boundaryRows :
    rows = boundaryRows.map (fun b => (List.range 5).map fun i => (b ⟨i % 5, Nat.mod_lt _ (by decide)⟩).val) := by
  decide +kernel

/-- The ten fixed representatives are all proper C5 rows using colours below four. -/
theorem rows_wellFormed :
    rows.length = 10 ∧ rows.Pairwise (· ≠ ·) ∧
    ∀ row ∈ rows, row.length = 5 ∧ (∀ c ∈ row, c < 4) ∧
      ∀ e ∈ frameEdges, row[e.1]! ≠ row[e.2]! := by
  decide +kernel

/-- The fixed indices partition all ten rows. -/
theorem row_index_partition :
    singletonRowIndices.length = 5 ∧ t4RowIndices.length = 5 ∧
    ∀ i ∈ List.range 10,
      (i ∈ singletonRowIndices ∧ i ∉ t4RowIndices) ∨
      (i ∈ t4RowIndices ∧ i ∉ singletonRowIndices) := by
  decide +kernel

/-- The accepted T4 indices are exactly the four-colour rows and encode 932. -/
theorem t4_indices_exact :
    ((t4RowIndices.map fun i => 2 ^ i).foldl (· + ·) 0 = 932) ∧
    ∀ i ∈ List.range 10, ((rows[i]!).eraseDups.length = 4 ↔ i ∈ t4RowIndices) := by
  decide +kernel

end FiveBoundary.ExcessTwo
