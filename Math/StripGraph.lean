/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Mathlib

/-! Strip graph semantics for the stepwise colouring problem, and a verified
backtracking checker for the finite-prefix extendability language.

The strip is described by a list of fans, one per interior row: vertex `(r, i)` of
row `r ≥ 1` is adjacent to `(r-1, i), …, (r-1, i + fans[r-1] - 1)` in the row below and
to `(r, i-1)`, `(r, i+1)`.  For a boundary word of length `n`, exactly the vertices whose
entire lower fan is present are included (row lengths `n, n+1-f₁, …`), matching
`direct_colouring` in `scripts/stepwise_aligned_reference.py`.  `Extendable fans w` says
the finite strip induced by the boundary word `w` has a proper 4-colouring extending `w`.

`verdict` decides `Extendable` on concrete inputs: `verdict_true` and `verdict_false`
are ordinary proofs; the per-instance side conditions (functional boundary, edge
coverage) are checked by the same computation.  Nothing here certifies the Python DFA
transition tables; see `Math/StepwiseReplay.lean` for what is replayed. -/
namespace StripGraph

abbrev V := ℕ × ℕ
abbrev Assign := List (V × Fin 4)

/-! ### Association-list colourings -/

def lookup : Assign → V → Option (Fin 4)
  | [], _ => none
  | (u, c) :: a, v => if u = v then some c else lookup a v

def keys (a : Assign) : List V := a.map Prod.fst

theorem lookup_mem {a : Assign} {v : V} {c : Fin 4} (h : lookup a v = some c) : (v, c) ∈ a := by
  induction a with
  | nil => simp [lookup] at h
  | cons p a ih =>
    obtain ⟨u, d⟩ := p
    by_cases huv : u = v
    · subst huv
      simp only [lookup, ite_true, Option.some_inj] at h
      subst h
      exact List.mem_cons_self
    · simp only [lookup, huv, ite_false] at h
      exact List.mem_cons_of_mem _ (ih h)

theorem lookup_eq_none {a : Assign} {v : V} : lookup a v = none ↔ v ∉ keys a := by
  induction a with
  | nil => simp [lookup, keys]
  | cons p a ih =>
    obtain ⟨u, d⟩ := p
    by_cases huv : u = v
    · subst huv; simp [lookup, keys]
    · simp [lookup, keys, huv, ih, Ne.symm huv]

theorem lookup_cons_ne {a : Assign} {u v : V} {c : Fin 4} (h : u ≠ v) :
    lookup ((u, c) :: a) v = lookup a v := by
  simp [lookup, h]

/-- The proper-colouring test on the assigned endpoints of an edge. -/
def okEdge (a : Assign) (e : V × V) : Bool :=
  match lookup a e.1, lookup a e.2 with
  | some x, some y => x != y
  | _, _ => true

def consistent (a : Assign) (es : List (V × V)) : Bool := es.all (okEdge a)

/-- Backtracking over the vertex list; vertices already assigned are skipped. -/
def search (es : List (V × V)) : List V → Assign → Bool
  | [], a => consistent a es
  | v :: vs, a =>
    match lookup a v with
    | some _ => search es vs a
    | none => (List.finRange 4).any fun c =>
        consistent ((v, c) :: a) es && search es vs ((v, c) :: a)

/-! ### Specification -/

def Agrees (f : V → Fin 4) (a : Assign) : Prop := ∀ p ∈ a, f p.1 = p.2
def Proper (f : V → Fin 4) (es : List (V × V)) : Prop := ∀ e ∈ es, f e.1 ≠ f e.2
/-- Every stored pair is what `lookup` returns: no conflicting duplicates. -/
def Func (a : Assign) : Prop := ∀ p ∈ a, lookup a p.1 = some p.2
/-- Every edge endpoint is assigned or still to be visited. -/
def Covers (es : List (V × V)) (a : Assign) (vs : List V) : Prop :=
  ∀ e ∈ es, (e.1 ∈ keys a ∨ e.1 ∈ vs) ∧ (e.2 ∈ keys a ∨ e.2 ∈ vs)

theorem func_cons {a : Assign} {v : V} (c : Fin 4) (ha : Func a) (hv : lookup a v = none) :
    Func ((v, c) :: a) := by
  intro p hp
  rcases List.mem_cons.mp hp with h | hp'
  · subst h; simp [lookup]
  · have hne : v ≠ p.1 := by
      intro hvp
      rw [hvp, ha p hp'] at hv
      exact Option.some_ne_none _ hv
    rw [lookup_cons_ne hne]
    exact ha p hp'

theorem consistent_of {f : V → Fin 4} {a : Assign} {es : List (V × V)}
    (hf : Agrees f a) (hp : Proper f es) : consistent a es = true := by
  rw [consistent, List.all_eq_true]
  intro e he
  unfold okEdge
  split
  · rename_i x y hx hy
    have h1 := hf _ (lookup_mem hx)
    have h2 := hf _ (lookup_mem hy)
    simp only at h1 h2
    subst h1 h2
    exact bne_iff_ne.mpr (hp e he)
  · rfl

theorem covers_of_lookup_some {es : List (V × V)} {a : Assign} {v : V} {vs : List V} {c : Fin 4}
    (hc : Covers es a (v :: vs)) (hv : lookup a v = some c) : Covers es a vs := by
  have hk : v ∈ keys a := by
    by_contra h
    rw [← lookup_eq_none] at h
    rw [h] at hv
    cases hv
  intro e he
  obtain ⟨h1, h2⟩ := hc e he
  refine ⟨?_, ?_⟩
  · rcases h1 with h | h
    · exact Or.inl h
    · rcases List.mem_cons.mp h with rfl | h
      · exact Or.inl hk
      · exact Or.inr h
  · rcases h2 with h | h
    · exact Or.inl h
    · rcases List.mem_cons.mp h with rfl | h
      · exact Or.inl hk
      · exact Or.inr h

theorem covers_cons {es : List (V × V)} {a : Assign} {v : V} {vs : List V}
    (hc : Covers es a (v :: vs)) (c : Fin 4) : Covers es ((v, c) :: a) vs := by
  intro e he
  obtain ⟨h1, h2⟩ := hc e he
  refine ⟨?_, ?_⟩
  · rcases h1 with h | h
    · exact Or.inl (List.mem_cons_of_mem _ h)
    · rcases List.mem_cons.mp h with rfl | h
      · exact Or.inl List.mem_cons_self
      · exact Or.inr h
  · rcases h2 with h | h
    · exact Or.inl (List.mem_cons_of_mem _ h)
    · rcases List.mem_cons.mp h with rfl | h
      · exact Or.inl List.mem_cons_self
      · exact Or.inr h

/-- The checker is exactly the existence of a proper colouring extending `a`, provided
`a` is functional and every edge endpoint is assigned or listed. -/
theorem search_iff (es : List (V × V)) :
    ∀ (vs : List V) (a : Assign), Func a → Covers es a vs →
      (search es vs a = true ↔ ∃ f : V → Fin 4, Agrees f a ∧ Proper f es) := by
  intro vs
  induction vs with
  | nil =>
    intro a ha hc
    simp only [search]
    constructor
    · intro h
      refine ⟨fun v => (lookup a v).getD 0, ?_, ?_⟩
      · intro p hp
        simp [ha p hp]
      · intro e he
        obtain ⟨h1, h2⟩ := hc e he
        simp only [List.not_mem_nil, or_false] at h1 h2
        obtain ⟨x, hx⟩ : ∃ x, lookup a e.1 = some x :=
          Option.ne_none_iff_exists'.mp fun hn => lookup_eq_none.mp hn h1
        obtain ⟨y, hy⟩ : ∃ y, lookup a e.2 = some y :=
          Option.ne_none_iff_exists'.mp fun hn => lookup_eq_none.mp hn h2
        have := (List.all_eq_true.mp h) e he
        unfold okEdge at this
        rw [hx, hy] at this
        simp only [hx, hy, Option.getD_some]
        exact bne_iff_ne.mp this
    · rintro ⟨f, hf, hp⟩
      exact consistent_of hf hp
  | cons v vs ih =>
    intro a ha hc
    simp only [search]
    cases hv : lookup a v with
    | some c =>
      exact ih a ha (covers_of_lookup_some hc hv)
    | none =>
      simp only [List.any_eq_true, List.mem_finRange, true_and, Bool.and_eq_true]
      constructor
      · rintro ⟨c, _, hs⟩
        obtain ⟨f, hf, hp⟩ :=
          (ih ((v, c) :: a) (func_cons c ha hv) (covers_cons hc c)).mp hs
        exact ⟨f, fun p hp => hf p (List.mem_cons_of_mem _ hp), hp⟩
      · rintro ⟨f, hf, hp⟩
        have hf' : Agrees f ((v, f v) :: a) := by
          intro p hp
          rcases List.mem_cons.mp hp with rfl | hp
          · rfl
          · exact hf p hp
        refine ⟨f v, consistent_of hf' hp, ?_⟩
        exact (ih ((v, f v) :: a) (func_cons _ ha hv) (covers_cons hc _)).mpr ⟨f, hf', hp⟩

/-! ### The strip -/

def rowVertices (r len : ℕ) : List V := (List.range len).map fun i => (r, i)

def rowEdges (r len : ℕ) : List (V × V) :=
  (List.range (len - 1)).map fun i => ((r, i), (r, i + 1))

/-- Edges from row `r` (length `len`) down to its fan of `f` vertices in row `r - 1`. -/
def fanEdges (r len f : ℕ) : List (V × V) :=
  (List.range len).flatMap fun i => (List.range f).map fun j => ((r, i), (r - 1, i + j))

/-- All edges of the strip above row `r` of length `n` with the given remaining fans. -/
def edgesFrom : List ℕ → ℕ → ℕ → List (V × V)
  | [], r, n => rowEdges r n
  | f :: fs, r, n =>
    rowEdges r n ++ fanEdges (r + 1) (n + 1 - f) f ++ edgesFrom fs (r + 1) (n + 1 - f)

/-- Interior vertices above row `r` of length `n`, in row order. -/
def interiorFrom : List ℕ → ℕ → ℕ → List V
  | [], _, _ => []
  | f :: fs, r, n => rowVertices (r + 1) (n + 1 - f) ++ interiorFrom fs (r + 1) (n + 1 - f)

def stripEdges (fans : List ℕ) (n : ℕ) : List (V × V) := edgesFrom fans 0 n
def interiorVertices (fans : List ℕ) (n : ℕ) : List V := interiorFrom fans 0 n

/-- The boundary word as an assignment of row 0. -/
def boundary (w : List (Fin 4)) : Assign :=
  (List.finRange w.length).map fun i => ((0, i.val), w[i])

theorem agrees_boundary_iff (f : V → Fin 4) (w : List (Fin 4)) :
    Agrees f (boundary w) ↔ ∀ i (h : i < w.length), f (0, i) = w[i] := by
  constructor
  · intro hf i h
    exact hf ((0, i), w[i]) (List.mem_map.mpr ⟨⟨i, h⟩, List.mem_finRange _, rfl⟩)
  · intro hf p hp
    obtain ⟨i, _, rfl⟩ := List.mem_map.mp hp
    exact hf i.val i.isLt

/-- The finite strip induced by `w` has a proper 4-colouring extending `w`. -/
def Extendable (fans : List ℕ) (w : List (Fin 4)) : Prop :=
  ∃ f : V → Fin 4, Agrees f (boundary w) ∧ Proper f (stripEdges fans w.length)

def funcCheck (a : Assign) : Bool := a.all fun p => lookup a p.1 == some p.2

def coversCheck (es : List (V × V)) (a : Assign) (vs : List V) : Bool :=
  es.all fun e => (decide (e.1 ∈ keys a) || decide (e.1 ∈ vs)) &&
    (decide (e.2 ∈ keys a) || decide (e.2 ∈ vs))

theorem func_of_check {a : Assign} (h : funcCheck a = true) : Func a := by
  intro p hp
  have := (List.all_eq_true.mp h) p hp
  exact beq_iff_eq.mp this

theorem covers_of_check {es : List (V × V)} {a : Assign} {vs : List V}
    (h : coversCheck es a vs = true) : Covers es a vs := by
  intro e he
  have := (List.all_eq_true.mp h) e he
  simpa only [Bool.and_eq_true, Bool.or_eq_true, decide_eq_true_eq] using this

/-- `some b` iff the side conditions hold and the search answers `b`; `none` otherwise. -/
def verdict (fans : List ℕ) (w : List (Fin 4)) : Option Bool :=
  if funcCheck (boundary w) &&
      coversCheck (stripEdges fans w.length) (boundary w) (interiorVertices fans w.length) then
    some (search (stripEdges fans w.length) (interiorVertices fans w.length) (boundary w))
  else none

theorem verdict_iff {fans : List ℕ} {w : List (Fin 4)} {b : Bool}
    (h : verdict fans w = some b) : (Extendable fans w ↔ b = true) := by
  unfold verdict at h
  split at h
  · rename_i hc
    rw [Bool.and_eq_true] at hc
    rw [Option.some_inj] at h
    subst h
    exact (search_iff _ _ _ (func_of_check hc.1) (covers_of_check hc.2)).symm
  · cases h

theorem verdict_true {fans : List ℕ} {w : List (Fin 4)} (h : verdict fans w = some true) :
    Extendable fans w :=
  (verdict_iff h).mpr rfl

theorem verdict_false {fans : List ℕ} {w : List (Fin 4)} (h : verdict fans w = some false) :
    ¬ Extendable fans w := fun he => Bool.false_ne_true ((verdict_iff h).mp he)

/-! ### Residual languages -/

/-- The right residual of the extendability language at the history `w`. -/
def residual (fans : List ℕ) (w : List (Fin 4)) : Set (List (Fin 4)) :=
  {s | Extendable fans (w ++ s)}

theorem residual_ne_of_verdict {fans : List ℕ} {u v s : List (Fin 4)}
    (hu : verdict fans (u ++ s) = some true) (hv : verdict fans (v ++ s) = some false) :
    residual fans u ≠ residual fans v := by
  intro h
  have hs : s ∈ residual fans u := verdict_true hu
  rw [h] at hs
  exact verdict_false hv hs

/-- One stored separator per unordered pair of representatives, with opposite verdicts. -/
def separatesAll (fans : List ℕ) (reps : List (List (Fin 4)))
    (seps : List (ℕ × ℕ × List (Fin 4))) : Bool :=
  decide (∀ q r : Fin reps.length, q < r → ∃ t ∈ seps, t.1 = q.val ∧ t.2.1 = r.val ∧
    ((verdict fans (reps[q] ++ t.2.2) = some true ∧ verdict fans (reps[r] ++ t.2.2) = some false) ∨
     (verdict fans (reps[q] ++ t.2.2) = some false ∧ verdict fans (reps[r] ++ t.2.2) = some true)))

/-- Representatives with pairwise separators have pairwise distinct residuals, hence the
Nerode right congruence of the true extendability language has at least `reps.length`
classes. -/
theorem residual_injective {fans : List ℕ} {reps : List (List (Fin 4))}
    {seps : List (ℕ × ℕ × List (Fin 4))} (h : separatesAll fans reps seps = true) :
    Function.Injective fun q : Fin reps.length => residual fans reps[q] := by
  have h' := of_decide_eq_true h
  have key : ∀ q r : Fin reps.length, q < r → residual fans reps[q] ≠ residual fans reps[r] := by
    intro q r hqr
    obtain ⟨t, _, _, _, hsep⟩ := h' q r hqr
    rcases hsep with ⟨h1, h2⟩ | ⟨h1, h2⟩
    · exact residual_ne_of_verdict h1 h2
    · exact (residual_ne_of_verdict h2 h1).symm
  intro q r hqr
  by_contra hne
  rcases lt_or_gt_of_ne hne with hlt | hgt
  · exact key q r hlt hqr
  · exact key r q hgt hqr.symm

theorem residual_range_ncard {fans : List ℕ} {reps : List (List (Fin 4))}
    {seps : List (ℕ × ℕ × List (Fin 4))} (h : separatesAll fans reps seps = true) :
    (Set.range fun q : Fin reps.length => residual fans reps[q]).ncard = reps.length := by
  rw [Set.ncard_range_of_injective (residual_injective h), Nat.card_eq_fintype_card,
    Fintype.card_fin]

end StripGraph
