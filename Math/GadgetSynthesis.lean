/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.TriangleConstraints
import Math.GadgetLibrary
import Math.GadgetTargets

/-! Connect the readable constraints to actual library data and exact target certificates. -/
set_option linter.style.nativeDecide false
set_option linter.style.setOption false
namespace FiveBoundary.Gadget
set_option maxRecDepth 100000
set_option maxHeartbeats 0

theorem left_graph_binding :
    (triangleEdges leftLinks).toFinset =
      (show List (Fin 8 × Fin 8) from GadgetLibrary.certificates[20].edges).toFinset := by
  native_decide
theorem right_graph_binding :
    (triangleEdges rightLinks).toFinset =
      (show List (Fin 8 × Fin 8) from GadgetLibrary.certificates[34].edges).toFinset := by
  native_decide

theorem targets_are_T4 : GadgetTargets.certificates.all (fun c =>
    decide (c.expected = properBoundary.filter (fun b => (usedColors b).card = 4))) = true := by
  native_decide

theorem all_targets_exact (c : SplitCertificate) (hc : c ∈ GadgetTargets.certificates)
    (b : BoundaryColoring) :
    b ∈ Sigma (graphOfEdges c.edges) (firstBoundary (by omega)) ↔
      Proper C5 b ∧ (usedColors b).card = 4 := by
  have hv := (List.all_eq_true.mp GadgetTargets.all_certificates_valid) c hc
  rw [splitChecker_exact c hv b]
  have he := of_decide_eq_true ((List.all_eq_true.mp targets_are_T4) c hc)
  rw [he]
  simp [properBoundary]

theorem relation_checker_accepts_good :
    checkRelationCertificate ⟨0, cycleEdges, properBoundary⟩ = true := by native_decide

theorem relation_checker_rejects_missing_colors :
    checkRelationCertificate ⟨0, cycleEdges, ∅⟩ = false := by native_decide

theorem relation_checker_rejects_missing_cycle_edge :
    checkRelationCertificate ⟨0, cycleEdges.tail, properBoundary⟩ = false := by native_decide

end FiveBoundary.Gadget
