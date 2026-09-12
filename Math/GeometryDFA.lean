/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.ColorDFA

/-! Geometry automaton for the triangle grammar: non-crossing chords in the annulus between
the outer C5 and the interior K3. Only the forward direction is claimed here: an accepting
run is turned into an explicit rotation system, and a combinatorial checker verifies the
face count against Euler's formula and that the C5 is a face. That a spherical rotation
system with a facial C5 is a disk embedding is standard combinatorial topology and is NOT
a Lean theorem of this project; the converse (rejection ⇒ no disk embedding) is left open.
Native computation is intentional for the 32,768-word enumeration; see docs/automata.md. -/
set_option linter.style.nativeDecide false
set_option linter.style.setOption false
namespace FiveBoundary.GeometryDFA
open ColorDFA Gadget
set_option maxRecDepth 100000
set_option maxHeartbeats 0

/-- Position of interior vertex `k` on the triangle: identity or mirrored orientation. -/
def pos (o : Bool) (k : Fin 3) : Fin 3 := if o then k else -k

theorem pos_involutive (o : Bool) (k : Fin 3) : pos o (pos o k) = k := by
  cases o <;> simp [pos]

/-- Interior vertices of a letter listed by increasing position. -/
def fanBase (o : Bool) (letter : Finset (Fin 3)) : List (Fin 3) :=
  ((List.finRange 3).filter (fun p => pos o p ∈ letter)).map (pos o)

theorem fanBase_length_le (o : Bool) (letter : Finset (Fin 3)) : (fanBase o letter).length ≤ 3 := by
  simp only [fanBase, List.length_map]
  exact (List.length_filter_le _ _).trans (by simp)

/-- The fan at a boundary vertex, rotated by `r`: a cyclic rotation of `fanBase`. -/
def fan (o : Bool) (letter : Finset (Fin 3)) (r : Fin 3) : List (Fin 3) :=
  (fanBase o letter).rotate r.val

/-- A run: an orientation and one fan rotation per boundary vertex. -/
abbrev Run := Bool × (Fin 5 → Fin 3)

def sequence (w : Word) (ρ : Run) : List (Fin 5 × Fin 3) :=
  (List.finRange 5).flatMap (fun i => (fan ρ.1 (w i) (ρ.2 i)).map (fun k => (i, k)))

def cyclicSteps (o : Bool) : List (Fin 5 × Fin 3) → ℕ
  | [] => 0
  | e :: l => ((List.zip (e :: l) (l ++ [e])).map
      (fun p => (pos o p.2.2 - pos o p.1.2).val)).sum

/-- Total winding of the chord sequence around the triangle. -/
def winding (w : Word) (ρ : Run) : ℕ := cyclicSteps ρ.1 (sequence w ρ)

def RunOK (w : Word) (ρ : Run) : Prop := winding w ρ = 0 ∨ winding w ρ = 3

instance (w : Word) (ρ : Run) : Decidable (RunOK w ρ) :=
  inferInstanceAs (Decidable (_ ∨ _))

/-- Annulus acceptance: some orientation and fan rotations wind at most once. -/
def AnnulusAccept (w : Word) : Prop := ∃ ρ : Run, RunOK w ρ

/-- Rotations that produce distinct fans: `r < max 1 (length of the fan)`. -/
def rots (w : Word) (o : Bool) (i : Fin 5) : List (Fin 3) :=
  (List.finRange 3).filter (fun r => r.val < max 1 (fanBase o (w i)).length)

/-- Deterministic search order: identity orientation first, then fan rotations
lexicographically from boundary vertex 0. -/
def runsFor (w : Word) : List Run :=
  [true, false].flatMap fun o =>
    (rots w o 0).flatMap fun r0 => (rots w o 1).flatMap fun r1 =>
    (rots w o 2).flatMap fun r2 => (rots w o 3).flatMap fun r3 =>
    (rots w o 4).map fun r4 => (o, ![r0, r1, r2, r3, r4])

theorem fan_reduce (o : Bool) (letter : Finset (Fin 3)) (r : Fin 3) :
    ∃ r' : Fin 3, r'.val < max 1 (fanBase o letter).length ∧ fan o letter r' = fan o letter r := by
  have hle := fanBase_length_le o letter
  refine ⟨⟨r.val % max 1 (fanBase o letter).length, ?_⟩, Nat.mod_lt _ (by omega), ?_⟩
  · exact (Nat.mod_lt _ (by omega)).trans_le (by omega)
  · simp only [fan]
    rcases Nat.eq_zero_or_pos (fanBase o letter).length with h0 | hpos
    · rw [List.length_eq_zero_iff.mp h0]; simp
    · rw [Nat.max_eq_right hpos, List.rotate_mod]

theorem mem_runsFor (w : Word) (o : Bool) (r : Fin 5 → Fin 3) (h : ∀ i, r i ∈ rots w o i) :
    (o, r) ∈ runsFor w := by
  have hr : r = ![r 0, r 1, r 2, r 3, r 4] := by
    funext i; fin_cases i <;> rfl
  rw [hr]
  simp only [runsFor, List.mem_flatMap, List.mem_map, List.mem_cons, Prod.mk.injEq]
  exact ⟨o, by cases o <;> simp, r 0, h 0, r 1, h 1, r 2, h 2, r 3, h 3, r 4, h 4, rfl, rfl⟩

theorem runsFor_complete (w : Word) (o : Bool) (r : Fin 5 → Fin 3) :
    ∃ r' : Fin 5 → Fin 3, (o, r') ∈ runsFor w ∧ sequence w (o, r') = sequence w (o, r) := by
  choose r' hr' hfan using fun i => fan_reduce o (w i) (r i)
  refine ⟨r', mem_runsFor w o r' (fun i => ?_), ?_⟩
  · simp only [rots, List.mem_filter, List.mem_finRange, true_and, decide_eq_true_eq]
    exact hr' i
  · simp only [sequence]
    congr 1
    funext i
    simp [hfan]

def geoRun (w : Word) : Option Run := (runsFor w).find? (fun ρ => decide (RunOK w ρ))

def geoAccept (w : Word) : Bool := (geoRun w).isSome

theorem geoRun_ok (w : Word) (ρ : Run) (h : geoRun w = some ρ) : RunOK w ρ := by
  have := List.find?_some h
  simpa using this

theorem geoAccept_iff (w : Word) : geoAccept w = true ↔ AnnulusAccept w := by
  simp only [geoAccept, geoRun, List.find?_isSome, decide_eq_true_eq, AnnulusAccept]
  constructor
  · rintro ⟨ρ, _, h⟩; exact ⟨ρ, h⟩
  · rintro ⟨⟨o, r⟩, h⟩
    obtain ⟨r', hmem, hseq⟩ := runsFor_complete w o r
    refine ⟨(o, r'), hmem, ?_⟩
    simpa only [RunOK, winding, hseq] using h

/-! ### Rotation system built from an accepting run -/

abbrev Rotation := Fin 8 → List (Fin 8)

/-- Rotate the chord sequence so that it starts at a block boundary of interior vertices. -/
def blockAligned (s : List (Fin 5 × Fin 3)) : List (Fin 5 × Fin 3) :=
  match s with
  | [] => []
  | e :: l =>
    let cyc := List.zip (e :: l) (l ++ [e])
    match (List.range cyc.length).find?
        (fun i => (cyc.getD i (e, e)).1.2 ≠ (cyc.getD i (e, e)).2.2) with
    | none => e :: l
    | some i => (e :: l).rotate (i + 1)

/-- Counterclockwise rotation system: boundary vertex `i` sees `i-1`, `i+1`, then its fan
from the `i+1` side; interior vertex `k` sees its outer fan in sequence order, then the
next and previous triangle vertices. The table is materialised once per run. -/
def rotationTable (w : Word) (ρ : Run) : List (List (Fin 8)) :=
  let s := blockAligned (sequence w ρ)
  ((List.finRange 5).map fun i =>
    [outer (i - 1), outer (i + 1)] ++ ((fan ρ.1 (w i) (ρ.2 i)).reverse.map inner)) ++
  ((List.finRange 3).map fun k =>
    let p := pos ρ.1 k
    ((s.filter (fun e => e.2 = k)).map (fun e => outer e.1)) ++
      [inner (pos ρ.1 (p + 1)), inner (pos ρ.1 (p - 1))])

def rotationOf (w : Word) (ρ : Run) : Rotation :=
  let t := rotationTable w ρ
  fun u => t.getD u.val []

/-! ### Combinatorial embedding checker -/

abbrev Dart := Fin 8 × Fin 8

def darts (rot : Rotation) : List Dart :=
  (List.finRange 8).flatMap (fun u => (rot u).map (fun v => (u, v)))

/-- Dart `(u,v)` is followed by `(v, w)` where `w` follows `u` in the rotation at `v`. -/
def nextDart (rot : Rotation) (d : Dart) : Dart :=
  let l := rot d.2
  (d.2, l.getD ((l.idxOf d.1 + 1) % l.length) d.1)

def traceFace (rot : Rotation) (start : Dart) : ℕ → Dart → List Dart → List Dart
  | 0, _, acc => acc.reverse
  | n + 1, d, acc =>
    let d' := nextDart rot d
    if d' = start then (d :: acc).reverse else traceFace rot start n d' (d :: acc)

def faces (rot : Rotation) : List (List Dart) :=
  let ds := darts rot
  ds.foldl (fun acc d =>
    if acc.any (fun f => d ∈ f) then acc else acc ++ [traceFace rot d ds.length d []]) []

def reachable (rot : Rotation) : ℕ → List (Fin 8) → List (Fin 8)
  | 0, seen => seen
  | n + 1, seen =>
    let next := ((seen.flatMap rot).filter (fun v => v ∉ seen)).eraseDups
    if next = [] then seen else reachable rot n (seen ++ next)

def componentCount (rot : Rotation) : ℕ :=
  ((List.finRange 8).foldl (fun (acc : List (Fin 8) × ℕ) u =>
    if u ∈ acc.1 then acc else (acc.1 ++ reachable rot 8 [u], acc.2 + 1)) ([], 0)).2

def cycleDarts : List Dart := [(0,1),(1,2),(2,3),(3,4),(4,0)]

/-- Every check is finite: rotations list exactly the neighbours, every component of the
rotation system is spherical (`V - E + F = 2` per component), and C5 bounds a face. -/
def checkRotation (edges : List (Fin 8 × Fin 8)) (rot : Rotation) : Bool :=
  decide (∀ u : Fin 8, (rot u).Nodup ∧ u ∉ rot u ∧
      ∀ v : Fin 8, v ∈ rot u ↔ (u, v) ∈ edges ∨ (v, u) ∈ edges) &&
  decide (edges.Nodup ∧ ∀ e ∈ edges, e.1 < e.2) &&
  (let fs := faces rot
   decide (8 + fs.length = edges.length + 2 * componentCount rot) &&
   fs.any (fun f => f.toFinset = cycleDarts.toFinset ∨
     f.toFinset = (cycleDarts.map (fun d => (d.2, d.1))).toFinset))

def certified (w : Word) : Bool :=
  ((geoRun w).map (fun ρ => checkRotation (triangleEdges (linksOf w)) (rotationOf w ρ))).getD true

/-- Forward soundness certificate, replayed for all 32,768 masks: whenever the automaton
accepts, its own rotation system passes the combinatorial checker on the compiled graph. -/
theorem accepted_masks_have_rotation : ∀ m : Fin 32768, certified (wordOfMask m.val) = true := by
  native_decide

theorem accepted_words_have_rotation (w : Word) (ρ : Run) (h : geoRun w = some ρ) :
    checkRotation (triangleEdges (linksOf w)) (rotationOf w ρ) = true := by
  obtain ⟨m, rfl⟩ := wordOfMask_surjective w
  have := accepted_masks_have_rotation m
  rw [certified, h] at this
  simpa using this

theorem accept_certificate (w : Word) (h : AnnulusAccept w) :
    ∃ ρ : Run, RunOK w ρ ∧ checkRotation (triangleEdges (linksOf w)) (rotationOf w ρ) = true := by
  have hs := (geoAccept_iff w).mpr h
  obtain ⟨ρ, hρ⟩ := Option.isSome_iff_exists.mp hs
  exact ⟨ρ, geoRun_ok w ρ hρ, accepted_words_have_rotation w ρ hρ⟩

/-- Enumeration count matching the external apex-planarity test (7,194 of 32,768).
`wordOfMask` is a bijection from masks to words, so this counts words. -/
theorem accepted_mask_count :
    (Finset.univ.filter (fun m : Fin 32768 => geoAccept (wordOfMask m.val) = true)).card =
      7194 := by
  native_decide

theorem wordOfMask_bijective : Function.Bijective (fun m : Fin 32768 => wordOfMask m.val) := by
  rw [Fintype.bijective_iff_surjective_and_card]
  exact ⟨fun w => wordOfMask_surjective w, by simp⟩

theorem accepted_count :
    (Finset.univ.filter (fun w : Word => geoAccept w = true)).card = 7194 := by
  rw [← accepted_mask_count]
  exact (Finset.card_bij (fun m _ => wordOfMask m.val)
    (fun m hm => by simpa using hm)
    (fun m _ m' _ h => wordOfMask_bijective.1 h)
    (fun w hw => by
      obtain ⟨m, rfl⟩ := wordOfMask_surjective w
      exact ⟨m, by simpa using hw, rfl⟩)).symm

/-! ### Three-colour profiles of disk-accepted words (finite observation, not a lemma) -/

def threeReps : List BoundaryColoring :=
  [![0,1,0,1,2], ![0,1,0,2,1], ![0,1,2,0,1], ![0,1,2,0,2], ![0,1,2,1,2]]

/-- The boundary vertex whose colour is used once; these are `4,3,2,1,0` for `threeReps`. -/
def uniquePosition (b : BoundaryColoring) : Option (Fin 5) :=
  (List.finRange 5).find? (fun i => decide (∀ j, j ≠ i → b j ≠ b i))

theorem threeReps_positions :
    threeReps.map uniquePosition = [some 4, some 3, some 2, some 1, some 0] := by decide

def threeProfile (w : Word) : Finset (Fin 5) :=
  ((threeReps.filter (fun b => acceptB (run w b))).filterMap uniquePosition).toFinset

/-- Inside this grammar every disk-accepted word accepts at least two three-colour patterns,
and exactly two only when their unique positions are adjacent on C5. -/
theorem z5_masks_checked : ∀ m : Fin 32768, geoAccept (wordOfMask m.val) = true →
    2 ≤ (threeProfile (wordOfMask m.val)).card ∧
    ((threeProfile (wordOfMask m.val)).card = 2 →
      ∃ i, threeProfile (wordOfMask m.val) = {i, i + 1}) := by native_decide

theorem z5_profiles_checked (w : Word) (h : geoAccept w = true) :
    2 ≤ (threeProfile w).card ∧
    ((threeProfile w).card = 2 → ∃ i, threeProfile w = {i, i + 1}) := by
  obtain ⟨m, rfl⟩ := wordOfMask_surjective w
  exact z5_masks_checked m h

end FiveBoundary.GeometryDFA
