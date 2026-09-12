/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.GeometryDFA
import Math.GadgetSynthesis

/-! Replay of the stored gadget data through the two automata. The colour automaton's
prediction is compared with every exact library certificate; the geometry automaton
accepts every stored disk witness. Native computation is intentional; see docs/automata.md. -/
set_option linter.style.nativeDecide false
set_option linter.style.setOption false
namespace FiveBoundary.Automata
open ColorDFA GeometryDFA Gadget
set_option maxRecDepth 100000
set_option maxHeartbeats 0

def natEdges {n : ℕ} (edges : List (Fin n × Fin n)) : Finset (ℕ × ℕ) :=
  (edges.map (fun e => (e.1.val, e.2.val))).toFinset

/-- Every library witness lies in the triangle grammar (its edge set is exactly the compiled
word), its stored exact Σ abstracts to the automaton's ten-bit prediction, and its word is
disk-accepted by the geometry automaton. -/
theorem library_matches_automata : GadgetLibrary.certificates.all (fun c =>
    let w := wordOfEdges c.edges
    decide (c.k = 3 ∧ natEdges c.edges = natEdges (triangleEdges (linksOf w)) ∧
      abstractColors c.expected = acceptedReps w) && geoAccept w) = true := by
  native_decide

/-- The two synthesized components are the words `leftLinks`/`rightLinks`; the automaton's
three-colour profiles are `{01021, 01201}` and `{01012, 01202, 01212}`, i.e. Z5 positions
`{2,3}` and `{0,1,4}`. -/
theorem synthesized_profiles :
    threeProfile (wordOf leftLinks) = {2, 3} ∧ threeProfile (wordOf rightLinks) = {0, 1, 4} := by
  decide +kernel

theorem synthesized_disk :
    geoAccept (wordOf leftLinks) = true ∧ geoAccept (wordOf rightLinks) = true := by
  native_decide

/-- Semantic form: for each library certificate, the exact boundary relation restricted to the
canonical colour orbit representatives is the automaton's accepted set. -/
theorem library_sigma_reps (c : SplitCertificate) (hc : c ∈ GadgetLibrary.certificates) :
    abstractColors c.expected = acceptedReps (wordOfEdges c.edges) := by
  have h := (List.all_eq_true.mp library_matches_automata) c hc
  simp only [Bool.and_eq_true, decide_eq_true_eq] at h
  exact h.1.2.2

end FiveBoundary.Automata
