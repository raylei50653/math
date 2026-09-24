/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.RootInterfaces

/-! Exact reflection transport of actual boundary attachments and ordered contact relations.
Disk reflection and the source K5 exclusion remain paper arguments. -/
namespace FiveBoundary.TwoSpokeReflection

open ForcingLists RootInterfaces

/-- Reflection fixing boundary position 4. -/
def rho : Equiv.Perm (Fin 5) where
  toFun := ![3, 2, 1, 0, 4]
  invFun := ![3, 2, 1, 0, 4]
  left_inv := by decide
  right_inv := by decide

/-- The simultaneous colour change needed to preserve q. -/
def pi : Equiv.Perm Color := Equiv.swap 0 1

def q : Fin 5 → Color := ![0, 1, 0, 1, 2]

def reflectRow (b : Fin 5 → Color) : Fin 5 → Color := fun i => pi (b (rho i))

theorem rho_involutive : Function.Involutive rho := by
  intro i
  fin_cases i <;> rfl

theorem pi_involutive : Function.Involutive pi := Equiv.swap_apply_self 0 1

theorem reflectRow_involutive (b : Fin 5 → Color) :
    reflectRow (reflectRow b) = b := by
  funext i
  change pi (pi (b (rho (rho i)))) = b i
  rw [rho_involutive, pi_involutive]

theorem reflectRow_q : reflectRow q = q := by decide

/-- Boundary cycle adjacency is reversed, hence preserved. -/
theorem rho_cycle (i j : Fin 5) :
    (rho j = rho i + 1 ∨ rho i = rho j + 1) ↔ (j = i + 1 ∨ i = j + 1) := by
  revert i j
  decide

variable {V P : Type*}

def boundaryLists (A : V → Finset (Fin 5)) (b : Fin 5 → Color) : V → Finset Color :=
  fun v => Finset.univ \ (A v).image b

/-- Attachments move as named vertices; every colour uses the same permutation. -/
theorem boundaryLists_transport (A : V → Finset (Fin 5)) (b : Fin 5 → Color)
    (v : V) (a : Color) :
    pi a ∈ boundaryLists (fun w => (A w).image rho) (reflectRow b) v ↔
      a ∈ boundaryLists A b v := by
  simp only [boundaryLists, Finset.mem_sdiff, Finset.mem_univ, true_and,
    Finset.mem_image, reflectRow]
  constructor
  · intro h ha
    obtain ⟨i, hi, he⟩ := ha
    apply h
    exact ⟨rho i, ⟨i, hi, rfl⟩, by rw [rho_involutive, he]⟩
  · intro h ha
    obtain ⟨j, ⟨i, hi, rfl⟩, he⟩ := ha
    rw [rho_involutive] at he
    exact h ⟨i, hi, pi.injective he⟩

/-- General colour-frame transport on one unchanged component. -/
theorem listProper_transport (G : SimpleGraph V) (L L' : V → Finset Color)
    (e : Equiv.Perm Color) (hL : ∀ v a, e a ∈ L' v ↔ a ∈ L v)
    (c : V → Color) : ListProper G L' (e ∘ c) ↔ ListProper G L c := by
  constructor
  · intro h
    exact ⟨fun u v huv he => h.1 u v huv (congrArg e he),
      fun v => (hL v (c v)).mp (h.2 v)⟩
  · intro h
    exact ⟨fun u v huv he => h.1 u v huv (e.injective he),
      fun v => (hL v (c v)).mpr (h.2 v)⟩

/-- All contacts are transported together using a single complete colouring. -/
theorem contactRelation_transport (G : SimpleGraph V) (L L' : V → Finset Color)
    (p : P → V) (e : Equiv.Perm Color)
    (hL : ∀ v a, e a ∈ L' v ↔ a ∈ L v) (t : P → Color) :
    (e ∘ t) ∈ contactRelation G L' p ↔ t ∈ contactRelation G L p := by
  constructor
  · rintro ⟨c, hc, ht⟩
    refine ⟨e.symm ∘ c, ?_, ?_⟩
    · apply (listProper_transport G L L' e hL (e.symm ∘ c)).mp
      simpa [Function.comp_def] using hc
    · funext k
      have h := congrFun ht k
      simpa [Function.comp_def] using congrArg e.symm h
  · rintro ⟨c, hc, rfl⟩
    exact ⟨e ∘ c, (listProper_transport G L L' e hL c).mpr hc, rfl⟩

/-- Forbidden hub colours transform in the same frame as the full contact tuple. -/
theorem forbidden_transport (G : SimpleGraph V) (L L' : V → Finset Color)
    (p : P → V) (e : Equiv.Perm Color)
    (hL : ∀ v a, e a ∈ L' v ↔ a ∈ L v) (a : Color) :
    e a ∈ forbidden (contactRelation G L' p) ↔
      a ∈ forbidden (contactRelation G L p) := by
  constructor
  · intro h ⟨t, ht, hav⟩
    apply h
    exact ⟨e ∘ t, (contactRelation_transport G L L' p e hL t).mpr ht,
      fun k he => hav k (e.injective he)⟩
  · intro h ⟨t, ht, hav⟩
    apply h
    refine ⟨e.symm ∘ t, ?_, ?_⟩
    · apply (contactRelation_transport G L L' p e hL (e.symm ∘ t)).mp
      simpa [Function.comp_def] using ht
    · intro k he
      apply hav k
      simpa [Function.comp_def] using congrArg e he

/-- Reflection transport at the fixed q, for any number of named contacts. -/
theorem q_contactRelation (G : SimpleGraph V) (A : V → Finset (Fin 5))
    (p : P → V) (t : P → Color) :
    (pi ∘ t) ∈ contactRelation G (boundaryLists (fun v => (A v).image rho) q) p ↔
      t ∈ contactRelation G (boundaryLists A q) p := by
  apply contactRelation_transport
  intro v a
  simpa only [reflectRow_q] using boundaryLists_transport A q v a

theorem q_forbidden (G : SimpleGraph V) (A : V → Finset (Fin 5))
    (p : P → V) (a : Color) :
    pi a ∈ forbidden (contactRelation G (boundaryLists (fun v => (A v).image rho) q) p) ↔
      a ∈ forbidden (contactRelation G (boundaryLists A q) p) := by
  apply forbidden_transport
  intro v c
  simpa only [reflectRow_q] using boundaryLists_transport A q v c

/-- The adjacent spoke orbits; the first transports the established exclusion. -/
theorem adjacent_orbits :
    ({0, 1} : Finset (Fin 5)).image rho = {2, 3} ∧
    ({1, 2} : Finset (Fin 5)).image rho = {1, 2} ∧
    ({3, 4} : Finset (Fin 5)).image rho = {4, 0} ∧
    pi 2 = 2 ∧ pi 3 = 3 ∧ pi 0 = 1 := by decide

end FiveBoundary.TwoSpokeReflection
