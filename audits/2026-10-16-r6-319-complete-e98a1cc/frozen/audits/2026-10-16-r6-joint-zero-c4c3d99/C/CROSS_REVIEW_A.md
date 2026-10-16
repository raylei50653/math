# Independent C review of A

Reviewed `../A/PROOF.md` against the frozen source geometry and matching
proof. Result: PASS for the stated arbitrary-size singleton-barrier
exclusion, with its remaining-branch boundary retained.

* The source J degree table permits degree four only at v,w,p,q; m has
  degree at least seven. Euler therefore gives precisely
  `2t4+t5+n5-E=12`, and `n5>=5` outside the six original marked vertices.
* For a singleton Tutte failure, the four removed forced endpoints have
  eight external stubs because their induced edges are exactly the two
  forced edges. Thus `3q<=3s+10`, and the positive even deficiency is
  exactly two. This argument does not assume a maximum barrier.
* The exact degree equation gives `|E_D(S)|+|E_D(S,X)|=1+tau`; an h edge
  within S is included once in that count, and h between S and I is
  bichromatic. All locations of h are covered.
* With bits zero on S union X and one on I, all monochromatic primal
  edges outside the three prescribed edges belong to B, which has at
  most two edges. The face-walk parity identity requires every original
  odd-degree vertex outside the six pins to meet B*. Its at most four
  endpoints cannot cover the five supplied by Euler.
* The five-cut localization in A4 matches frozen matching proof section
  5: connectivity makes the cut a bond; forced faces put both stars
  outside its component; the proper-C5 cap theorem includes chorded
  cycles; an empty pentagon dual tree is not factor-critical. No
  stronger restriction on the seven-cut case is inferred.

This review checks the proof and its exact hypotheses. It does not turn
the finite controls into original sources and does not prove an
ordinary matching or an even-complement matching exists.
