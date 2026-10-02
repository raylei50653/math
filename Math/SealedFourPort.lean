/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.Boundary

/-! Exact labelled four-port relations. Interior vertices are existentially
sealed; no disk embedding or legality of geometric replacement is asserted. -/
namespace FiveBoundary.SealedFourPort

set_option maxRecDepth 4096

abbrev Row := Fin 4 → Color

def EdgeProper {n : ℕ} (edges : List (Fin n × Fin n)) (c : Fin n → Color) : Prop :=
  ∀ e ∈ edges, c e.1 ≠ c e.2

instance {n : ℕ} (edges : List (Fin n × Fin n)) (c : Fin n → Color) :
    Decidable (EdgeProper edges c) :=
  inferInstanceAs (Decidable (∀ e ∈ edges, c e.1 ≠ c e.2))

theorem proper_graphOfEdges_iff {n : ℕ} (edges : List (Fin n × Fin n))
    (hloop : ∀ e ∈ edges, e.1 ≠ e.2) (c : Fin n → Color) :
    Proper (graphOfEdges edges) c ↔ EdgeProper edges c := by
  constructor
  · intro h e he
    exact h e.1 e.2 ⟨hloop e he, Or.inl he⟩
  · intro h i j hij
    rcases hij.2 with hij | hji
    · exact h (i, j) hij
    · exact (h (j, i) hji).symm

def Extends {n : ℕ} (edges : List (Fin n × Fin n)) (ports : Fin 4 → Fin n)
    (b : Row) : Prop :=
  ∃ c, Proper (graphOfEdges edges) c ∧ ∀ i, c (ports i) = b i

def RingProper (b : Row) : Prop :=
  b 0 ≠ b 1 ∧ b 1 ≠ b 2 ∧ b 2 ≠ b 3 ∧ b 3 ≠ b 0

def WheelCondition (b : Row) : Prop :=
  RingProper b ∧ ∃ missing : Color, ∀ i, b i ≠ missing

def capEdges : List (Fin 13 × Fin 13) :=
  [(0,1), (0,3), (0,4), (0,9), (0,11), (1,2), (1,11),
   (2,3), (2,5), (2,11), (2,12), (3,5), (3,8), (3,9),
   (4,6), (4,9), (4,11), (5,6), (5,7), (5,8), (5,12),
   (6,7), (6,9), (6,10), (6,11), (6,12), (7,8), (7,10),
   (8,9), (8,10), (9,10), (11,12)]

def wheelEdges : List (Fin 5 × Fin 5) :=
  [(0,1), (0,3), (1,2), (2,3), (0,4), (1,4), (2,4), (3,4)]

def capPorts : Fin 4 → Fin 13 := Fin.castLE (by decide)
def wheelPorts : Fin 4 → Fin 5 := Fin.castLE (by decide)

theorem cap_proper_iff (c : Fin 13 → Color) :
    Proper (graphOfEdges capEdges) c ↔ EdgeProper capEdges c :=
  proper_graphOfEdges_iff capEdges (by decide) c

theorem wheel_proper_iff (c : Fin 5 → Color) :
    Proper (graphOfEdges wheelEdges) c ↔ EdgeProper wheelEdges c :=
  proper_graphOfEdges_iff wheelEdges (by decide) c

/-- A small colour lemma checked by kernel reduction, not native evaluation. -/
theorem four_colors_exhaust : ∀ a b c d : Color,
    a ≠ b → a ≠ c → a ≠ d → b ≠ c → b ≠ d → c ≠ d →
    ∀ x : Color, x = a ∨ x = b ∨ x = c ∨ x = d := by decide

theorem exists_color_outside_three : ∀ a b c : Color,
    ∃ d : Color, d ≠ a ∧ d ≠ b ∧ d ≠ c := by decide

theorem ring_injective_of_diagonals {b : Row} (h : RingProper b)
    (h02 : b 0 ≠ b 2) (h13 : b 1 ≠ b 3) : Function.Injective b := by
  intro i j hij
  fin_cases i <;> fin_cases j <;> simp_all [RingProper, Ne.symm]

theorem missing_of_diagonal {b : Row} (h : b 0 = b 2 ∨ b 1 = b 3) :
    ∃ missing : Color, ∀ i, b i ≠ missing := by
  have hn : ¬ Function.Injective b := by
    intro hi
    rcases h with h | h
    · have := hi h; contradiction
    · have := hi h; contradiction
  have hns : ¬ Function.Surjective b := fun hs =>
    hn (Finite.injective_iff_surjective.mpr hs)
  simpa only [Function.Surjective, not_forall, not_exists] using hns

/-- The contradiction follows the actual edges through 11, 5/12, 6, 9, 4. -/
theorem cap_no_rainbow {c : Fin 13 → Color} (h : EdgeProper capEdges c)
    (h02 : c 0 ≠ c 2) (h13 : c 1 ≠ c 3) : False := by
  have he (u v : Fin 13) (hm : (u,v) ∈ capEdges) : c u ≠ c v := h (u,v) hm
  have h01 := he 0 1 (by decide)
  have h03 := he 0 3 (by decide)
  have h12 := he 1 2 (by decide)
  have h23 := he 2 3 (by decide)
  have allColors := four_colors_exhaust (c 0) (c 1) (c 2) (c 3)
    h01 h02 h03 h12 h13 h23
  have h11 : c 11 = c 3 := by
    have := allColors (c 11)
    have := he 0 11 (by decide)
    have := he 1 11 (by decide)
    have := he 2 11 (by decide)
    tauto
  have h5 : c 5 = c 0 ∨ c 5 = c 1 := by
    have := allColors (c 5)
    have := he 2 5 (by decide)
    have := he 3 5 (by decide)
    tauto
  have h12' : c 12 = c 0 ∨ c 12 = c 1 := by
    have := allColors (c 12)
    have := he 2 12 (by decide)
    have := he 11 12 (by decide)
    rw [h11] at this
    tauto
  have h6 : c 6 = c 2 := by
    have := allColors (c 6)
    have := he 5 12 (by decide)
    have := he 5 6 (by decide)
    have := he 6 12 (by decide)
    have := he 6 11 (by decide)
    rw [h11] at this
    rcases h5 with h5 | h5 <;> rcases h12' with h12' | h12' <;> simp_all
    all_goals tauto
  have h9 : c 9 = c 1 := by
    have := allColors (c 9)
    have := he 0 9 (by decide)
    have := he 3 9 (by decide)
    have := he 6 9 (by decide)
    rw [h6] at this
    tauto
  have := he 0 4 (by decide)
  have := he 4 6 (by decide)
  have := he 4 9 (by decide)
  have := he 4 11 (by decide)
  rcases allColors (c 4) with h4 | h4 | h4 | h4 <;> simp_all

theorem cap_extends_implies_condition {b : Row} (h : Extends capEdges capPorts b) :
    WheelCondition b := by
  obtain ⟨c, hc, hb⟩ := h
  have h := (cap_proper_iff c).mp hc
  have he (u v : Fin 13) (hm : (u,v) ∈ capEdges) : c u ≠ c v := h (u,v) hm
  have h0 := hb 0
  have h1 := hb 1
  have h2 := hb 2
  have h3 := hb 3
  change c 0 = b 0 at h0
  change c 1 = b 1 at h1
  change c 2 = b 2 at h2
  change c 3 = b 3 at h3
  have hring : RingProper b := by
    simpa only [RingProper, ← h0, ← h1, ← h2, ← h3] using
      And.intro (he 0 1 (by decide)) (And.intro (he 1 2 (by decide))
        (And.intro (he 2 3 (by decide)) (he 0 3 (by decide)).symm))
  refine ⟨hring, missing_of_diagonal ?_⟩
  by_contra hn
  push Not at hn
  exact cap_no_rainbow h (by simpa only [h0, h2] using hn.1)
    (by simpa only [h1, h3] using hn.2)

/-- Three explicit lifts, using one common palette throughout the graph. -/
theorem cap_lift_0101 {a b c d : Color}
    (hab : a ≠ b) (hac : a ≠ c) (had : a ≠ d)
    (hbc : b ≠ c) (hbd : b ≠ d) (hcd : c ≠ d) :
    Extends capEdges capPorts ![a,b,a,b] := by
  refine ⟨![a,b,a,b,b,c,a,b,a,c,d,c,b], (cap_proper_iff _).mpr ?_, ?_⟩
  · simp_all [EdgeProper, capEdges, Ne.symm]
  · intro i; fin_cases i <;> rfl

theorem cap_lift_0102 {a b c d : Color}
    (hab : a ≠ b) (hac : a ≠ c) (had : a ≠ d)
    (hbc : b ≠ c) (hbd : b ≠ d) (hcd : c ≠ d) :
    Extends capEdges capPorts ![a,b,a,c] := by
  refine ⟨![a,b,a,c,d,b,a,c,a,b,d,c,d], (cap_proper_iff _).mpr ?_, ?_⟩
  · simp_all [EdgeProper, capEdges, Ne.symm]
  · intro i; fin_cases i <;> rfl

theorem cap_lift_0121 {a b c d : Color}
    (hab : a ≠ b) (hac : a ≠ c) (had : a ≠ d)
    (hbc : b ≠ c) (hbd : b ≠ d) (hcd : c ≠ d) :
    Extends capEdges capPorts ![a,b,c,b] := by
  refine ⟨![a,b,c,b,b,a,c,b,c,d,a,d,b], (cap_proper_iff _).mpr ?_, ?_⟩
  · simp_all [EdgeProper, capEdges, Ne.symm]
  · intro i; fin_cases i <;> rfl

theorem cap_extends_of_condition {b : Row} (h : WheelCondition b) :
    Extends capEdges capPorts b := by
  obtain ⟨hring, missing, hm⟩ := h
  obtain ⟨h01, h12, h23, h30⟩ := hring
  by_cases h02 : b 0 = b 2
  · by_cases h13 : b 1 = b 3
    · obtain ⟨d, hd0, hd1, hdm⟩ := exists_color_outside_three (b 0) (b 1) missing
      have hb : b = ![b 0, b 1, b 0, b 1] := by
        funext i; fin_cases i <;> simp [← h02, ← h13]
      rw [hb]
      exact cap_lift_0101 h01 (hm 0) hd0.symm (hm 1) hd1.symm hdm.symm
    · have hb : b = ![b 0, b 1, b 0, b 3] := by
        funext i; fin_cases i <;> simp [← h02]
      rw [hb]
      exact cap_lift_0102 h01 h30.symm (hm 0) h13 (hm 1) (hm 3)
  · have h13 : b 1 = b 3 := by
      by_contra hn
      have hinj := ring_injective_of_diagonals ⟨h01,h12,h23,h30⟩ h02 hn
      obtain ⟨i, hi⟩ := Finite.injective_iff_surjective.mp hinj missing
      exact hm i hi
    have hb : b = ![b 0, b 1, b 2, b 1] := by
      funext i; fin_cases i <;> simp [← h13]
    rw [hb]
    exact cap_lift_0121 h01 h02 (hm 0) h12 (hm 1) (hm 2)

theorem cap_extends_iff (b : Row) :
    Extends capEdges capPorts b ↔ WheelCondition b :=
  ⟨cap_extends_implies_condition, cap_extends_of_condition⟩

theorem wheel_extends_iff (b : Row) :
    Extends wheelEdges wheelPorts b ↔ WheelCondition b := by
  constructor
  · rintro ⟨c, hc, hb⟩
    have he := (wheel_proper_iff c).mp hc
    have h0 := hb 0
    have h1 := hb 1
    have h2 := hb 2
    have h3 := hb 3
    change c 0 = b 0 at h0
    change c 1 = b 1 at h1
    change c 2 = b 2 at h2
    change c 3 = b 3 at h3
    simp only [EdgeProper, wheelEdges, List.mem_cons, forall_eq_or_imp] at he
    refine ⟨⟨?_, ?_, ?_, ?_⟩, c 4, ?_⟩
    · simpa only [← h0, ← h1] using he.1
    · simpa only [← h1, ← h2] using he.2.2.1
    · simpa only [← h2, ← h3] using he.2.2.2.1
    · simpa only [← h3, ← h0] using he.2.1.symm
    · intro i; fin_cases i <;> simp_all
  · rintro ⟨⟨h01,h12,h23,h30⟩, m, hm⟩
    refine ⟨![b 0,b 1,b 2,b 3,m], (wheel_proper_iff _).mpr ?_, ?_⟩
    · simp_all [EdgeProper, wheelEdges, Ne.symm]
    · intro i; fin_cases i <;> rfl

theorem cap_wheel_equivalent (b : Row) :
    Extends capEdges capPorts b ↔ Extends wheelEdges wheelPorts b :=
  (cap_extends_iff b).trans (wheel_extends_iff b).symm

/-- Explicitly sealed semantics: only the first four named vertices belong to
the exterior; every remaining colour is separately existentially quantified. -/
def Sealed {X : Type*} {k : ℕ} (edges : List (Fin (4 + k) × Fin (4 + k)))
    (attach : Fin 4 → X) (outside : Set (X → Color)) : Set (X → Color) :=
  {x | x ∈ outside ∧ ∃ inside : Fin k → Color,
    Proper (graphOfEdges edges) (Fin.addCases (x ∘ attach) inside)}

theorem extends_iff_sealed_tail {k : ℕ}
    (edges : List (Fin (4 + k) × Fin (4 + k))) (b : Row) :
    Extends edges (Fin.castAdd k) b ↔
      ∃ inside : Fin k → Color, Proper (graphOfEdges edges) (Fin.addCases b inside) := by
  constructor
  · rintro ⟨c, hc, hb⟩
    refine ⟨fun i => c (Fin.natAdd 4 i), ?_⟩
    have heq : Fin.addCases b (fun i => c (Fin.natAdd 4 i)) = c := by
      have hleft : b = fun i => c (Fin.castAdd k i) := (funext hb).symm
      rw [hleft]
      funext i
      exact Fin.addCases_castAdd_natAdd c i
    rwa [heq]
  · rintro ⟨inside, hc⟩
    exact ⟨Fin.addCases b inside, hc, fun i => by simp⟩

/-- Exact relation equality preserves each entire exterior colouring, under
arbitrary joint exterior constraints and the same literal attachment map. -/
theorem sealed_congr {X : Type*} {k l : ℕ}
    (left : List (Fin (4 + k) × Fin (4 + k)))
    (right : List (Fin (4 + l) × Fin (4 + l)))
    (h : ∀ b, Extends left (Fin.castAdd k) b ↔ Extends right (Fin.castAdd l) b)
    (attach : Fin 4 → X) (outside : Set (X → Color)) :
    Sealed left attach outside = Sealed right attach outside := by
  ext x
  change (x ∈ outside ∧ _) ↔ (x ∈ outside ∧ _)
  rw [← extends_iff_sealed_tail, ← extends_iff_sealed_tail, h]

theorem cap_sealed_replacement {X : Type*} (attach : Fin 4 → X)
    (outside : Set (X → Color)) :
    Sealed (k := 9) capEdges attach outside = Sealed (k := 1) wheelEdges attach outside := by
  apply sealed_congr
  exact cap_wheel_equivalent

/-- The complete exterior relation is preserved before taking any further
observation; the observation may retain every exterior vertex. -/
theorem cap_exterior_observation {X Y : Type*} (attach : Fin 4 → X)
    (outside : Set (X → Color)) (observe : (X → Color) → Y) :
    observe '' Sealed (k := 9) capEdges attach outside =
      observe '' Sealed (k := 1) wheelEdges attach outside := by
  rw [cap_sealed_replacement]

/-- Keeping the old centre as a fifth port invalidates the equivalence. -/
theorem cap_center_not_preserved :
    ∃ c : Fin 13 → Color, Proper (graphOfEdges capEdges) c ∧
      ∀ w : Fin 5 → Color, Proper (graphOfEdges wheelEdges) w →
        ¬ (∀ i : Fin 5, w i = c (Fin.castLE (by decide) i)) := by
  let c : Fin 13 → Color := ![0,1,0,1,1,2,0,1,0,2,3,2,1]
  refine ⟨c, (cap_proper_iff _).mpr (by decide), ?_⟩
  intro w hw heq
  have hedge := (wheel_proper_iff w).mp hw (1,4) (by decide)
  have h1 := heq 1
  have h4 := heq 4
  change w 1 = 1 at h1
  change w 4 = 1 at h4
  exact hedge (h1.trans h4.symm)

/-- The original edge 4--6 is essential: deleting it admits a rainbow rim. -/
theorem cap_missing_edge_rainbow :
    Extends (capEdges.filter (fun e => e ≠ (4,6))) capPorts ![0,1,2,3] := by
  refine ⟨![0,1,2,3,2,0,2,1,2,1,0,3,1], ?_, ?_⟩
  · exact (proper_graphOfEdges_iff _ (by decide) _).mpr (by decide)
  · intro i; fin_cases i <;> rfl

end FiveBoundary.SealedFourPort
