import Math.ExcessTwoColoring
open FiveBoundary FiveBoundary.ExcessTwo
set_option linter.style.nativeDecide false
set_option maxRecDepth 100000
set_option maxHeartbeats 0
-- Source artifacts/c5_excess_two_finite_search/AD_k9_validate/crit_orbits/orbit_0001.json
def probeEdges : List (Fin 14 × Fin 14) := [(0,1),(0,4),(0,5),(0,6),(0,7),(0,8),(0,9),(0,10),(1,2),(1,7),(1,11),(2,3),(2,5),(2,11),(2,12),(3,4),(3,6),(3,12),(3,13),(4,8),(4,13),(5,6),(5,9),(5,12),(6,10),(6,12),(7,9),(7,11),(8,10),(8,13),(9,11),(10,13)]
theorem no_probe : ¬ Extends (k := 9) probeEdges 0 := by native_decide
#print axioms no_probe
