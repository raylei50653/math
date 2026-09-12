/-
Copyright (c) 2026 raylei50653. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: raylei50653
-/
import Math.SplitCertificate

/-! Generated data. Run scripts/export_certificates.py to regenerate.
Native computation is intentional; see docs/phase1.md for the trust boundary. -/
set_option linter.style.nativeDecide false
set_option linter.style.setOption false
namespace FiveBoundary.ConstructedMinimal
set_option maxRecDepth 100000
set_option maxHeartbeats 0

def expected0 : List BoundaryColoring := [
  ![0,1,0,2,3],![0,1,0,3,2],![0,1,2,0,3],![0,1,2,1,3],
  ![0,1,2,3,1],![0,1,2,3,2],![0,1,3,0,2],![0,1,3,1,2],
  ![0,1,3,2,1],![0,1,3,2,3],![0,2,0,1,3],![0,2,0,3,1],
  ![0,2,1,0,3],![0,2,1,2,3],![0,2,1,3,1],![0,2,1,3,2],
  ![0,2,3,0,1],![0,2,3,1,2],![0,2,3,1,3],![0,2,3,2,1],
  ![0,3,0,1,2],![0,3,0,2,1],![0,3,1,0,2],![0,3,1,2,1],
  ![0,3,1,2,3],![0,3,1,3,2],![0,3,2,0,1],![0,3,2,1,2],
  ![0,3,2,1,3],![0,3,2,3,1],![1,0,1,2,3],![1,0,1,3,2],
  ![1,0,2,0,3],![1,0,2,1,3],![1,0,2,3,0],![1,0,2,3,2],
  ![1,0,3,0,2],![1,0,3,1,2],![1,0,3,2,0],![1,0,3,2,3],
  ![1,2,0,1,3],![1,2,0,2,3],![1,2,0,3,0],![1,2,0,3,2],
  ![1,2,1,0,3],![1,2,1,3,0],![1,2,3,0,2],![1,2,3,0,3],
  ![1,2,3,1,0],![1,2,3,2,0],![1,3,0,1,2],![1,3,0,2,0],
  ![1,3,0,2,3],![1,3,0,3,2],![1,3,1,0,2],![1,3,1,2,0],
  ![1,3,2,0,2],![1,3,2,0,3],![1,3,2,1,0],![1,3,2,3,0],
  ![2,0,1,0,3],![2,0,1,2,3],![2,0,1,3,0],![2,0,1,3,1],
  ![2,0,2,1,3],![2,0,2,3,1],![2,0,3,0,1],![2,0,3,1,0],
  ![2,0,3,1,3],![2,0,3,2,1],![2,1,0,1,3],![2,1,0,2,3],
  ![2,1,0,3,0],![2,1,0,3,1],![2,1,2,0,3],![2,1,2,3,0],
  ![2,1,3,0,1],![2,1,3,0,3],![2,1,3,1,0],![2,1,3,2,0],
  ![2,3,0,1,0],![2,3,0,1,3],![2,3,0,2,1],![2,3,0,3,1],
  ![2,3,1,0,1],![2,3,1,0,3],![2,3,1,2,0],![2,3,1,3,0],
  ![2,3,2,0,1],![2,3,2,1,0],![3,0,1,0,2],![3,0,1,2,0],
  ![3,0,1,2,1],![3,0,1,3,2],![3,0,2,0,1],![3,0,2,1,0],
  ![3,0,2,1,2],![3,0,2,3,1],![3,0,3,1,2],![3,0,3,2,1],
  ![3,1,0,1,2],![3,1,0,2,0],![3,1,0,2,1],![3,1,0,3,2],
  ![3,1,2,0,1],![3,1,2,0,2],![3,1,2,1,0],![3,1,2,3,0],
  ![3,1,3,0,2],![3,1,3,2,0],![3,2,0,1,0],![3,2,0,1,2],
  ![3,2,0,2,1],![3,2,0,3,1],![3,2,1,0,1],![3,2,1,0,2],
  ![3,2,1,2,0],![3,2,1,3,0],![3,2,3,0,1],![3,2,3,1,0]
]

def certificates : List SplitCertificate := [
  -- JSON SHA-256: 6dc6ddbcf0b3901e3740342e965c97f02a991cbad9e70feead03ebdb37b59601
  ⟨6, [(0,1),(0,4),(0,7),(0,10),(1,2),(1,6),(1,7),(1,8),
    (2,3),(2,5),(2,6),(2,8),(3,4),(3,5),(3,8),(3,9),
    (4,5),(4,7),(4,9),(4,10),(5,6),(5,7),(6,7),(8,9),
    (8,10),(9,10)],
    expected0.toFinset⟩
]

theorem certificate_count : certificates.length = 1 := by decide
theorem all_certificates_valid : certificates.all checkSplitCertificate = true := by native_decide
theorem all_certificates_bad (c : SplitCertificate) (hc : c ∈ certificates) :
    BAD (graphOfEdges c.edges) (firstBoundary (by omega)) := by
  exact splitChecker_sound c ((List.all_eq_true.mp all_certificates_valid) c hc)

end FiveBoundary.ConstructedMinimal
