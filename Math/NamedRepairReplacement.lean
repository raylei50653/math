/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.NamedRepair

/-! One sealed D₁₃ replacement on either or both named private centres.
All relations use the original U and palette. The actual graft graph retains
all thirteen exterior vertices, including the five private exterior vertices.
No disk embedding, frame completeness, or arbitrary iteration is asserted. -/
namespace FiveBoundary.NamedRepairReplacement

open SealedFourPort CommonRepair

set_option maxRecDepth 16384

abbrev Exterior := Fin 13 → Color

/-- Delete only h5=8 and v=13 from the original labelled fifteen vertices. -/
def exteriorMap : Fin 13 → Fin 15 := ![0,1,2,3,4,5,6,7,9,10,11,12,14]
def attachA : Fin 4 → Fin 13 := ![9,2,11,0]
def attachB : Fin 4 → Fin 13 := ![7,6,12,5]

/-- The original 35 edges with exactly the eight centre spokes removed. -/
def exteriorEdges (rev : Bool) : List (Fin 13 × Fin 13) :=
  let s : Fin 13 := if rev then 2 else 0
  let t : Fin 13 := if rev then 0 else 2
  [(0,1), (1,2), (2,3), (3,4), (0,4),
   (0,8), (0,9), (0,10), (0,11),
   (2,9), (2,11), (3,8), (3,9), (3,10),
   (1,11), (4,10), (8,9), (8,10),
   (5,s), (s,6), (6,t), (t,7), (5,7), (6,7),
   (5,12), (6,12), (s,12)]

/-- Reconstruct the original core assignment with the two sealed centres. -/
def coreColor (x : Exterior) (a b : Color) : Fin 15 → Color :=
  ![x 0,x 1,x 2,x 3,x 4,x 5,x 6,x 7,a,x 8,x 9,x 10,x 11,b,x 12]

theorem coreColor_exterior (x : Exterior) (a b : Color) :
    ∀ i, coreColor x a b (exteriorMap i) = x i := by
  intro i; fin_cases i <;> rfl

theorem coreColor_reconstruct (c : Fin 15 → Color) :
    coreColor (c ∘ exteriorMap) (c 8) (c 13) = c := by
  funext i; fin_cases i <;> rfl

/-- The local arrays have exactly the original ordered rims and centres. -/
theorem core_proper_decomposition (rev : Bool) (x : Exterior) (a b : Color) :
    EdgeProper (NamedRepair.coreEdges rev) (coreColor x a b) ↔
      EdgeProper (exteriorEdges rev) x ∧
      EdgeProper wheelEdges (fun i => Fin.addCases (x ∘ attachA) (fun _ : Fin 1 => a) i) ∧
      EdgeProper wheelEdges (fun i => Fin.addCases (x ∘ attachB) (fun _ : Fin 1 => b) i) := by
  have ha : (fun i : Fin 5 => Fin.addCases (x ∘ attachA) (fun _ : Fin 1 => a) i) =
      ![x 9,x 2,x 11,x 0,a] := by
    funext i; fin_cases i <;> rfl
  have hb : (fun i : Fin 5 => Fin.addCases (x ∘ attachB) (fun _ : Fin 1 => b) i) =
      ![x 7,x 6,x 12,x 5,b] := by
    funext i; fin_cases i <;> rfl
  rw [ha, hb]
  cases rev <;>
    simp [EdgeProper, NamedRepair.coreEdges, exteriorEdges, wheelEdges,
      coreColor, ne_comm] <;> tauto

/-- All thirteen exterior colours, rather than only U, are observed. -/
def coreExterior (rev : Bool) : Set Exterior :=
  {x | ∃ c : Fin 15 → Color,
    Proper (graphOfEdges (NamedRepair.coreEdges rev)) c ∧ c ∘ exteriorMap = x}

def mapEdges {n m : ℕ} (f : Fin n → Fin m) (es : List (Fin n × Fin n)) :
    List (Fin m × Fin m) := es.map (fun e => (f e.1, f e.2))

/-- The exterior is first, then the A tail, then the B tail. -/
def aMap {k l : ℕ} : Fin (4 + k) → Fin (13 + (k + l)) :=
  Fin.addCases (fun i => Fin.castAdd (k + l) (attachA i))
    (fun i => Fin.natAdd 13 (Fin.castAdd l i))
def bMap {k l : ℕ} : Fin (4 + l) → Fin (13 + (k + l)) :=
  Fin.addCases (fun i => Fin.castAdd (k + l) (attachB i))
    (fun i => Fin.natAdd 13 (Fin.natAdd k i))

/-- Actual original exterior edges plus both attached local edge lists.
Repeated rim edges denote the same edges in graphOfEdges. -/
def graftEdges {k l : ℕ} (rev : Bool)
    (left : List (Fin (4 + k) × Fin (4 + k)))
    (right : List (Fin (4 + l) × Fin (4 + l))) :
    List (Fin (13 + (k + l)) × Fin (13 + (k + l))) :=
  mapEdges (Fin.castAdd (k + l)) (exteriorEdges rev) ++
    mapEdges (aMap (k := k) (l := l)) left ++
    mapEdges (bMap (k := k) (l := l)) right

def graftColor {k l : ℕ} (x : Exterior) (a : Fin k → Color) (b : Fin l → Color) :
    Fin (13 + (k + l)) → Color := Fin.addCases x (Fin.addCases a b)

theorem edgeProper_map {n m : ℕ} (f : Fin n → Fin m)
    (es : List (Fin n × Fin n)) (c : Fin m → Color) :
    EdgeProper (mapEdges f es) c ↔ EdgeProper es (c ∘ f) := by
  constructor
  · intro h e he
    exact h (f e.1, f e.2) (List.mem_map.mpr ⟨e, he, rfl⟩)
  · intro h e he
    obtain ⟨d, hd, rfl⟩ := List.mem_map.mp he
    exact h d hd

theorem edgeProper_append {n : ℕ} (xs ys : List (Fin n × Fin n))
    (c : Fin n → Color) :
    EdgeProper (xs ++ ys) c ↔ EdgeProper xs c ∧ EdgeProper ys c := by
  simp only [EdgeProper, List.mem_append, or_imp, forall_and]

theorem graftColor_aMap {k l : ℕ} (x : Exterior)
    (a : Fin k → Color) (b : Fin l → Color) :
    graftColor x a b ∘ aMap = Fin.addCases (x ∘ attachA) a := by
  funext i
  refine Fin.addCases ?_ ?_ i
  · intro j; simp [graftColor, aMap]
  · intro j; simp [graftColor, aMap]

theorem graftColor_bMap {k l : ℕ} (x : Exterior)
    (a : Fin k → Color) (b : Fin l → Color) :
    graftColor x a b ∘ bMap = Fin.addCases (x ∘ attachB) b := by
  funext i
  refine Fin.addCases ?_ ?_ i
  · intro j; simp [graftColor, bMap]
  · intro j; simp [graftColor, bMap]

theorem graft_edgeProper_iff {k l : ℕ} (rev : Bool)
    (left : List (Fin (4 + k) × Fin (4 + k)))
    (right : List (Fin (4 + l) × Fin (4 + l)))
    (x : Exterior) (a : Fin k → Color) (b : Fin l → Color) :
    EdgeProper (graftEdges rev left right) (graftColor x a b) ↔
      EdgeProper (exteriorEdges rev) x ∧
      EdgeProper left (Fin.addCases (x ∘ attachA) a) ∧
      EdgeProper right (Fin.addCases (x ∘ attachB) b) := by
  rw [graftEdges, edgeProper_append, edgeProper_append,
    edgeProper_map, edgeProper_map, edgeProper_map,
    graftColor_aMap, graftColor_bMap]
  have he : graftColor x a b ∘ Fin.castAdd (k + l) = x := by
    funext i; simp [graftColor]
  rw [he]
  tauto

/-- false retains the four-wheel; true uses the original 32-edge D₁₃. -/
def tailSize (patch : Bool) : ℕ := if patch then 9 else 1

def patchEdges (patch : Bool) : List (Fin (4 + tailSize patch) × Fin (4 + tailSize patch)) :=
  match patch with
  | false => wheelEdges
  | true => capEdges

/-- Single A, single B, and simultaneous replacements have 23, 23, and 31 vertices. -/
theorem vertex_counts :
    13 + (tailSize true + tailSize false) = 23 ∧
    13 + (tailSize false + tailSize true) = 23 ∧
    13 + (tailSize true + tailSize true) = 31 := by decide

theorem graft_no_loops : ∀ rev pa pb,
    ∀ e ∈ graftEdges rev (patchEdges pa) (patchEdges pb), e.1 ≠ e.2 := by
  intro rev pa pb
  have h : (graftEdges rev (patchEdges pa) (patchEdges pb)).all
      (fun e => decide (e.1 ≠ e.2)) = true := by
    cases rev <;> cases pa <;> cases pb <;> decide
  simpa only [List.all_eq_true, decide_eq_true_eq] using h

def exteriorRelation (rev pa pb : Bool) : Set Exterior :=
  {x | ∃ c : Fin (13 + (tailSize pa + tailSize pb)) → Color,
    Proper (graphOfEdges (graftEdges rev (patchEdges pa) (patchEdges pb))) c ∧
    ∀ i, c (Fin.castAdd (tailSize pa + tailSize pb) i) = x i}

/-- This decomposition is proved from the actual graph edge list. -/
theorem exteriorRelation_iff (rev pa pb : Bool) (x : Exterior) :
    x ∈ exteriorRelation rev pa pb ↔
      EdgeProper (exteriorEdges rev) x ∧
      Extends (patchEdges pa) (Fin.castAdd (tailSize pa)) (x ∘ attachA) ∧
      Extends (patchEdges pb) (Fin.castAdd (tailSize pb)) (x ∘ attachB) := by
  rw [extends_iff_sealed_tail, extends_iff_sealed_tail]
  constructor
  · rintro ⟨c, hc, hx⟩
    let a : Fin (tailSize pa) → Color :=
      fun i => c (Fin.natAdd 13 (Fin.castAdd (tailSize pb) i))
    let b : Fin (tailSize pb) → Color :=
      fun i => c (Fin.natAdd 13 (Fin.natAdd (tailSize pa) i))
    have heq : graftColor x a b = c := by
      funext i
      refine Fin.addCases ?_ ?_ i
      · intro j; simpa [graftColor] using (hx j).symm
      · intro j
        refine Fin.addCases ?_ ?_ j
        · intro q; simp [graftColor, a]
        · intro q; simp [graftColor, b]
    have hp := (proper_graphOfEdges_iff _ (graft_no_loops rev pa pb) c).mp hc
    rw [← heq, graft_edgeProper_iff] at hp
    exact ⟨hp.1, ⟨a, (proper_graphOfEdges_iff _ (by cases pa <;> decide) _).mpr hp.2.1⟩,
      ⟨b, (proper_graphOfEdges_iff _ (by cases pb <;> decide) _).mpr hp.2.2⟩⟩
  · rintro ⟨hx, ⟨a, ha⟩, ⟨b, hb⟩⟩
    refine ⟨graftColor x a b,
      (proper_graphOfEdges_iff _ (graft_no_loops rev pa pb) _).mpr ?_, ?_⟩
    · rw [graft_edgeProper_iff]
      exact ⟨hx,
        (proper_graphOfEdges_iff _ (by cases pa <;> decide) _).mp ha,
        (proper_graphOfEdges_iff _ (by cases pb <;> decide) _).mp hb⟩
    · intro i; simp [graftColor]

theorem patch_extends_iff (pa : Bool) (x : SealedFourPort.Row) :
    Extends (patchEdges pa) (Fin.castAdd (tailSize pa)) x ↔
      Extends wheelEdges wheelPorts x := by
  cases pa
  · exact Iff.rfl
  · exact cap_wheel_equivalent x

/-- Both modes retain every whole exterior assignment under the same attachments. -/
theorem exteriorRelation_eq_unpatched (rev pa pb : Bool) :
    exteriorRelation rev pa pb = exteriorRelation rev false false := by
  ext x
  rw [exteriorRelation_iff, exteriorRelation_iff,
    patch_extends_iff, patch_extends_iff]
  rfl

/-- The unpatched graft is exactly the original 35-edge core, after restoring
its two centres; this is the bridge to the existing named theorems. -/
theorem coreExterior_eq_unpatched (rev : Bool) :
    coreExterior rev = exteriorRelation rev false false := by
  ext x
  rw [exteriorRelation_iff]
  change x ∈ coreExterior rev ↔ EdgeProper (exteriorEdges rev) x ∧
    Extends wheelEdges (Fin.castAdd 1) (x ∘ attachA) ∧
    Extends wheelEdges (Fin.castAdd 1) (x ∘ attachB)
  rw [extends_iff_sealed_tail (k := 1), extends_iff_sealed_tail (k := 1)]
  constructor
  · rintro ⟨c, hc, hx⟩
    have he := (NamedRepair.core_proper_iff rev c).mp hc
    have hcEq : coreColor x (c 8) (c 13) = c := by
      rw [← hx]; exact coreColor_reconstruct c
    rw [← hcEq, core_proper_decomposition] at he
    exact ⟨he.1, ⟨(fun _ => c 8), (wheel_proper_iff _).mpr he.2.1⟩,
      ⟨(fun _ => c 13), (wheel_proper_iff _).mpr he.2.2⟩⟩
  · rintro ⟨hx, ⟨a, ha⟩, ⟨b, hb⟩⟩
    have haEq : a = fun _ => a 0 := by funext i; fin_cases i; rfl
    have hbEq : b = fun _ => b 0 := by funext i; fin_cases i; rfl
    rw [haEq] at ha
    rw [hbEq] at hb
    exact ⟨coreColor x (a 0) (b 0),
      (NamedRepair.core_proper_iff rev _).mpr
        ((core_proper_decomposition rev x (a 0) (b 0)).mpr
          ⟨hx, (wheel_proper_iff _).mp ha, (wheel_proper_iff _).mp hb⟩),
      funext (coreColor_exterior x (a 0) (b 0))⟩

/-- A once, B once, or both once: equality of complete thirteen-point relations. -/
theorem exteriorRelation_eq_core (rev pa pb : Bool) :
    exteriorRelation rev pa pb = coreExterior rev := by
  rw [exteriorRelation_eq_unpatched, coreExterior_eq_unpatched]


/-- U remains (a0,a1,a2,a3,a4,b0,b2,b4), in its original literal order. -/
def observeU (x : Exterior) : NamedRepair.Row :=
  fun i => x (Fin.castLE (by decide) i)

/-- The attachments are literally the original rims, before removing centres. -/
theorem attachments_literal :
    exteriorMap ∘ attachA = ![(10 : Fin 15),2,12,0] ∧
    exteriorMap ∘ attachB = ![(7 : Fin 15),6,14,5] := by
  constructor <;> funext i <;> fin_cases i <;> rfl

/-- The full eight-point joint relation is the observation of the actual graph. -/
def joint (rev pa pb : Bool) : Set NamedRepair.Row :=
  observeU '' exteriorRelation rev pa pb

/-- Direct graph semantics for the eight named ports: each row extends to
one full colouring of the actual grafted graph. -/
theorem joint_iff_graph (rev pa pb : Bool) (u : NamedRepair.Row) :
    u ∈ joint rev pa pb ↔
      ∃ c : Fin (13 + (tailSize pa + tailSize pb)) → Color,
        Proper (graphOfEdges (graftEdges rev (patchEdges pa) (patchEdges pb))) c ∧
        ∀ i : Fin 8, c (Fin.castAdd (tailSize pa + tailSize pb)
          (Fin.castLE (by decide) i)) = u i := by
  constructor
  · rintro ⟨x, ⟨c, hc, hx⟩, hxu⟩
    refine ⟨c, hc, fun i => ?_⟩
    exact (hx _).trans (congrFun hxu i)
  · rintro ⟨c, hc, hu⟩
    let x : Exterior := fun i => c (Fin.castAdd (tailSize pa + tailSize pb) i)
    exact ⟨x, ⟨c, hc, fun _ => rfl⟩, funext hu⟩

theorem observe_core (c : Fin 15 → Color) :
    observeU (c ∘ exteriorMap) = fun i => c (NamedRepair.ports i) := by
  funext i; fin_cases i <;> rfl

theorem joint_eq (rev pa pb : Bool) : joint rev pa pb = NamedRepair.J rev := by
  rw [joint, exteriorRelation_eq_core]
  ext u
  constructor
  · rintro ⟨x, ⟨c, hc, hcx⟩, hxu⟩
    refine ⟨c, hc, ?_⟩
    have he : (fun i => c (NamedRepair.ports i)) = u := by
      rw [← observe_core, hcx, hxu]
    exact congrFun he
  · rintro ⟨c, hc, hu⟩
    exact ⟨c ∘ exteriorMap, ⟨c, hc, rfl⟩, by
      rw [observe_core]; exact funext hu⟩

/-- Complete literal projections of the replaced graph relation. -/
def accept (rev pa pb : Bool) (scope : Finset (Fin 8))
    (b : NamedRepair.Row) : Prop :=
  ∃ c ∈ joint rev pa pb, ∀ u ∈ scope, c u = b u

/-- Only the two specified mixed frames are used, with the same labelled entries. -/
def candidate (rev pa pb : Bool) : Set NamedRepair.Row :=
  {b | accept rev pa pb NamedRepair.frame₁ b ∧
    accept rev pa pb (NamedRepair.frame₂ rev) b}

theorem accept_iff (rev pa pb : Bool) (scope : Finset (Fin 8))
    (b : NamedRepair.Row) :
    accept rev pa pb scope b ↔ NamedRepair.Accept rev scope b := by
  rw [accept, joint_eq]
  rfl

theorem candidate_eq (rev pa pb : Bool) : candidate rev pa pb = NamedRepair.P rev := by
  ext b
  exact and_congr (accept_iff rev pa pb _ b) (accept_iff rev pa pb _ b)

theorem joint_subset_candidate (rev pa pb : Bool) :
    joint rev pa pb ⊆ candidate rev pa pb := by
  rw [joint_eq, candidate_eq]
  exact NamedRepair.j_subset_p rev

def system (rev pa pb : Bool) : System NamedRepair.Row NamedRepair.Scope :=
  projectionSystem (joint rev pa pb) (candidate rev pa pb)
    (joint_subset_candidate rev pa pb) (fun s => (s.val : Set (Fin 8)))

/-- Equality of the entire faithful projection system, including every scope. -/
theorem system_eq (rev pa pb : Bool) : system rev pa pb = NamedRepair.system rev := by
  simp only [system, joint_eq, candidate_eq, NamedRepair.system]

/-- The three full-U obstruction witnesses and all their rejector sets transport. -/
theorem witness_coverage (rev pa pb : Bool) :
    (NamedRepair.roles rev).WitnessCoverage (system rev pa pb) := by
  rw [system_eq]
  exact NamedRepair.witness_coverage rev

theorem repairs_iff (rev pa pb : Bool) (H : Set NamedRepair.Scope) :
    (system rev pa pb).Repairs H ↔
      (NamedRepair.scopeA ∈ H ∧ NamedRepair.scopeB rev ∈ H) ∨
      ∃ e ∈ NamedRepair.scopesE rev,
        NamedRepair.scopeA ∈ H ∧ NamedRepair.scopeT ∈ H ∧ e ∈ H := by
  rw [system_eq]
  exact NamedRepair.repairs_iff rev H

theorem minimal_repairs_iff (rev pa pb : Bool) (H : Set NamedRepair.Scope) :
    (system rev pa pb).MinimalRepair H ↔
      H = {NamedRepair.scopeA, NamedRepair.scopeB rev} ∨
      ∃ e ∈ NamedRepair.scopesE rev,
        H = {NamedRepair.scopeA, NamedRepair.scopeT, e} := by
  rw [system_eq]
  exact NamedRepair.minimal_repairs_iff rev H

theorem unique_minimum_pair (rev pa pb : Bool) (H : Finset NamedRepair.Scope) :
    (system rev pa pb).Repairs (H : Set NamedRepair.Scope) ∧ H.card ≤ 2 ↔
      H = {NamedRepair.scopeA, NamedRepair.scopeB rev} := by
  rw [system_eq]
  exact NamedRepair.unique_minimum_pair rev H

theorem forced_scope_iff (rev pa pb : Bool) (s : NamedRepair.Scope) :
    (∀ H, (system rev pa pb).Repairs H → s ∈ H) ↔ s = NamedRepair.scopeA := by
  rw [system_eq]
  exact NamedRepair.forced_scope_iff rev s

theorem minimal_repairs_mem (rev pa pb : Bool) (H : Finset NamedRepair.Scope) :
    (system rev pa pb).MinimalRepair (H : Set NamedRepair.Scope) ↔
      H ∈ NamedRepair.minimalRepairs rev := by
  rw [system_eq]
  exact NamedRepair.minimal_repairs_mem rev H

/-- Exactly the original fifteen finite inclusion-minimal four-scope repairs. -/
theorem fifteen_minimal_repairs (rev pa pb : Bool) :
    (∀ H : Finset NamedRepair.Scope,
      (system rev pa pb).MinimalRepair (H : Set NamedRepair.Scope) ↔
        H ∈ NamedRepair.minimalRepairs rev) ∧
      (NamedRepair.minimalRepairs rev).card = 15 :=
  ⟨minimal_repairs_mem rev pa pb, NamedRepair.fifteen_minimal_repairs rev⟩

/-- No family of literal projections of arity at most three repairs the same P. -/
theorem no_small_projection_repair (rev pa pb : Bool) {Λ : Type*}
    (scope : Λ → Finset (Fin 8)) (hs : ∀ i, (scope i).card ≤ 3) (H : Set Λ) :
    ¬ (projectionSystem (joint rev pa pb) (candidate rev pa pb)
      (joint_subset_candidate rev pa pb) (fun i => (scope i : Set (Fin 8)))).Repairs H := by
  simpa only [joint_eq, candidate_eq] using
    NamedRepair.no_small_projection_repair rev scope hs H

/-- Two four-point projections repair P, completing the exact r*=4 transport. -/
theorem four_point_repair (rev pa pb : Bool) :
    (system rev pa pb).Repairs {NamedRepair.scopeA, NamedRepair.scopeB rev} := by
  rw [system_eq]
  exact NamedRepair.four_point_repair rev

end FiveBoundary.NamedRepairReplacement
