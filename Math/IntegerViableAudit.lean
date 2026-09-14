import Math.IntegerViable

#print axioms FiveBoundary.EdgeMask.popcount_even
#print axioms FiveBoundary.EdgeMask.popcount_odd
#print axioms FiveBoundary.EdgeMask.bitIndices_encode
#print axioms FiveBoundary.EdgeMask.popcount_encode
#print axioms FiveBoundary.EdgeMask.popcount_inter
#print axioms FiveBoundary.EdgeMask.popcount_shift
#print axioms FiveBoundary.EdgeMask.viable_encode_iff
#print axioms FiveBoundary.EdgeMask.viable_decode_iff
#print axioms FiveBoundary.EdgeMask.integer_viable_of_survivor
#print axioms FiveBoundary.EdgeMask.integer_viable_of_graph
#print axioms FiveBoundary.EdgeMask.integer_rejection_sound
#print axioms FiveBoundary.EdgeMask.viable_reach_iff

set_option maxRecDepth 4096
set_option exponentiation.threshold 512

open FiveBoundary.EdgeMask

-- Ordinary kernel reduction, including beyond-machine-word masks and open blocks.
example : popcount (2 ^ 256 + 2 ^ 128 + 1) = 3 := by decide
example : popcount (2 ^ 257 - 1) = 257 := by decide
example : viable 0 (fun _ => 0) 0 0 = true := by decide
example : viable 1 (fun _ => 992) 0 5 = true := by decide
example : viable 1 (fun _ => 992) 0 7 = false := by decide
example : viable 1 (fun _ => 992) 480 10 = true := by decide
-- Both degrees pass; numeric attachment order must reject 15 < 16,
-- even though the first attachment has more set bits.
example : viable 2 (fun _ => 65535) (15 * 2 ^ 5 + 16 * 2 ^ 10) 16 = false := by decide
example : viable 2 (fun _ => 65535) (16 * 2 ^ 5 + 15 * 2 ^ 10) 16 = true := by decide
