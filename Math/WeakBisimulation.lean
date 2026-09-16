/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.Boundary

/-! Observation-labelled, divergence-insensitive weak bisimulation.
No finiteness, termination, geometry, or computational certificate assumption. -/
namespace ObservationSystem

universe u v
variable {S : Type u} {O : Type v} (step : S → S → Prop) (obs : S → O)

def Silent (x y : S) : Prop := step x y ∧ obs x = obs y

def Visible (x y : S) : Prop := step x y ∧ obs x ≠ obs y

abbrev SilentStar := Relation.ReflTransGen (Silent step obs)

/-- A weak exit has a silent prefix and exactly one visible step. -/
def Exit (x y : S) : Prop := ∃ z, SilentStar step obs x z ∧ Visible step obs z y

def WeakExits (x : S) : Set O := {o | ∃ y, Exit step obs x y ∧ obs y = o}

/-- Standard weak visible move, including an optional silent suffix. -/
def WeakVisible (x y : S) : Prop := ∃ z, Exit step obs x z ∧ SilentStar step obs z y

def Kernel (x y : S) : Prop := obs x = obs y

/-- Symmetry makes the two matching obligations bidirectional. Visible actions
are target observations; the matching intermediate target has the same observation
as the endpoint because the suffix is silent. -/
structure IsWeakBisimulation (R : S → S → Prop) : Prop where
  symm : ∀ {x y}, R x y → R y x
  observation : ∀ {x y}, R x y → obs x = obs y
  silent : ∀ {x y x'}, R x y → Silent step obs x x' →
    ∃ y', SilentStar step obs y y' ∧ R x' y'
  visible : ∀ {x y x'}, R x y → Visible step obs x x' →
    ∃ y', WeakVisible step obs y y' ∧ obs x' = obs y' ∧ R x' y'

theorem silentStar_observation {x y : S} (h : SilentStar step obs x y) :
    obs x = obs y := by
  induction h with
  | refl => rfl
  | tail _ h ih => exact ih.trans h.2

/-- Fiberwise constancy of weak exits suffices for the observation kernel. -/
theorem kernel_isWeakBisimulation
    (hW : ∀ x y, obs x = obs y → WeakExits step obs x = WeakExits step obs y) :
    IsWeakBisimulation step obs (Kernel obs) where
  symm := Eq.symm
  observation := id
  silent := by
    intro x y x' hxy hxx'
    exact ⟨y, .refl, hxx'.2.symm.trans hxy⟩
  visible := by
    intro x y x' hxy hxx'
    have hx : obs x' ∈ WeakExits step obs x := ⟨x', ⟨x, .refl, hxx'⟩, rfl⟩
    rw [hW x y hxy] at hx
    obtain ⟨y', hy', he⟩ := hx
    exact ⟨y', ⟨y', hy', .refl⟩, he.symm, he.symm⟩

/-- Finite executions, recording only visible target observations. Any finite
prefix may stop; silent steps contribute no entries. -/
inductive Trace : S → List O → Prop
  | nil (x) : Trace x []
  | silent {x y t} : Silent step obs x y → Trace y t → Trace x t
  | visible {x y t} : Visible step obs x y → Trace y t → Trace x (obs y :: t)

theorem trace_of_silentStar {x y : S} {t : List O}
    (h : SilentStar step obs x y) (ht : Trace step obs y t) : Trace step obs x t := by
  induction h with
  | refl => exact ht
  | tail _ h ih => exact ih (Trace.silent h ht)

theorem trace_of_weakVisible {x y : S} {t : List O}
    (h : WeakVisible step obs x y) (ht : Trace step obs y t) :
    Trace step obs x (obs y :: t) := by
  obtain ⟨z, ⟨w, hxw, hwz⟩, hzy⟩ := h
  rw [← silentStar_observation step obs hzy]
  exact trace_of_silentStar step obs hxw
    (Trace.visible hwz (trace_of_silentStar step obs hzy ht))

theorem IsWeakBisimulation.trace_transfer {R : S → S → Prop}
    (hR : IsWeakBisimulation step obs R) {x y : S} {t : List O}
    (hxy : R x y) (ht : Trace step obs x t) : Trace step obs y t := by
  induction ht generalizing y with
  | nil => exact Trace.nil y
  | silent hs _ ih =>
    obtain ⟨y', hy', hr⟩ := hR.silent hxy hs
    exact trace_of_silentStar step obs hy' (ih hr)
  | visible hs _ ih =>
    obtain ⟨y', hy', he, hr⟩ := hR.visible hxy hs
    rw [he]
    exact trace_of_weakVisible step obs hy' (ih hr)

/-- Includes the initial observation, as in the C5 audit's compressed traces. -/
def ObservableTraces (x : S) : Set (List O) :=
  {t | ∃ rest, Trace step obs x rest ∧ t = obs x :: rest}

theorem IsWeakBisimulation.observableTraces_eq {R : S → S → Prop}
    (hR : IsWeakBisimulation step obs R) {x y : S} (hxy : R x y) :
    ObservableTraces step obs x = ObservableTraces step obs y := by
  have forward : ∀ {a b}, R a b →
      ObservableTraces step obs a ⊆ ObservableTraces step obs b := by
    intro a b hab t ht
    obtain ⟨rest, hr, he⟩ := ht
    exact ⟨rest, hR.trace_transfer step obs hab hr, he.trans (by rw [hR.observation hab])⟩
  exact Set.Subset.antisymm (forward hxy) (forward (hR.symm hxy))

theorem kernel_observableTraces_eq
    (hW : ∀ x y, obs x = obs y → WeakExits step obs x = WeakExits step obs y)
    {x y : S} (hxy : obs x = obs y) :
    ObservableTraces step obs x = ObservableTraces step obs y :=
  (kernel_isWeakBisimulation step obs hW).observableTraces_eq step obs hxy

end ObservationSystem

namespace FiveBoundary

/-- Specialization to the existing complete labelled boundary relation. The state
type may be a closed deletion domain, including a dependent union over k.
This theorem does not assert that any audit satisfies the hypothesis. -/
theorem sigma_kernel_isWeakBisimulation {S : Type} (step : S → S → Prop)
    (n : S → ℕ) (graph : (s : S) → SimpleGraph (Fin (n s)))
    (boundary : (s : S) → Fin 5 ↪ Fin (n s))
    (hW : ∀ x y, Sigma (graph x) (boundary x) = Sigma (graph y) (boundary y) →
      ObservationSystem.WeakExits step (fun s => Sigma (graph s) (boundary s)) x =
      ObservationSystem.WeakExits step (fun s => Sigma (graph s) (boundary s)) y) :
    ObservationSystem.IsWeakBisimulation step (fun s => Sigma (graph s) (boundary s))
      (ObservationSystem.Kernel (fun s => Sigma (graph s) (boundary s))) :=
  ObservationSystem.kernel_isWeakBisimulation step _ hW

end FiveBoundary
