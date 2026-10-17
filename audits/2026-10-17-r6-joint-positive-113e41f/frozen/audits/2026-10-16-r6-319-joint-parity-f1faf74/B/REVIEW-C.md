# B review of C's source proof

Reviewed `../C/PROOF.md` on the same audit BASE.

The marked cyclic four-cut exclusion is sound conditional on its cited
frozen source statements. An induced C4 containing vw cannot use m because
one of mv,mw is a chord, and cannot use z because one of zv,zw would be an
edge. For pq the same reasoning excludes z, leaving m. The cycle order
forces mp or mq, and the exact source common-neighbour formula excludes
the remaining fourth vertex. The a/c degree sum removes the optional
middle-fan vertex before that formula is used. No PM or colouring witness
is silently inserted.

The v-degree-five C5 completion also retains its stated scope. Removing v
exposes the original six-cycle; adding si cuts off the actual triangular
ear sji. The complete v fibre must retain the private colour of j, as C
does. In the ABABC row, i,j are indeed C,D in either order, so one common
permutation gives ABCBC or ABCBD on the new five-boundary. This is a legal
smaller helper graph, not a completed smaller bad source: reconstruction
still costs k+5.

The remaining all-lift/K132 exclusion is not proved by C/PROOF.md and is
correctly OPEN there. B's complete fixed-graph countercontrol satisfies
the new four-cut restriction as well as the old five-cut restriction while
its entire joint family has positive oddness. It fails C's literal source
layout, so it does not challenge C4 or full319; it confirms the need to
use the source geometry beyond abstract cut restrictions.
