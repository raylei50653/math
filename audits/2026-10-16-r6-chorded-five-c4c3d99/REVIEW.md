# Proof review and scope audit

This is a second-pass review by the same agent, not independent-agent or
formal verification. The paper conclusion is adopted under the frozen
source contract; numerical minimum-source coverage remains not triggered.

| Obligation | Resolution |
| --- | --- |
| C is a whole side of Q, not a selected subset | Five-cut complement is connected by the three-edge lower bound; bond duality gives a Jordan five-cycle. |
| Factor-critical is measured in H, while geometry uses D | Common111 saturation puts f between different components, so H[C]=D[C]. |
| An interior chord could leave a nonfacial triangle | Every J triangle is facial, and the other Q vertices determine its exterior side; the ear is a real face. |
| Exterior ear might belong to another odd component | It has two distinct edges to C; there is at most the single f between different components. |
| Expanded four-cycle might still have a chord | Both sides have more than two faces: C plus the ear has at least four, and at least three X faces remain outside. |
| Adding an S face could hide the f endpoint | Saturation puts both f endpoints outside S, so zpq lies in C and the other f endpoint stays outside the expanded disk. |
| X face could have an unmarked third edge | Its forced partner is also in X; its two C incidences leave exactly that forced edge as the chord. |
| mz chord uses both hubs; old induced-five argument does not apply | PROOF 4.2 works on the new induced C4, then checks pq against all five ORIGINAL boundary edges. |
| alpha=p or beta=q could create a missed pq edge | The only edge of the original Q avoiding m,z is uv; induced C4 makes v a non-neighbour of z, so it cannot be p or q. |
| Single-component conclusion accidentally used for paired components | The chord proof never uses the number of other non-singletons or the one-five-cut budget. It applies separately to every five-cut component. |
| Ordinary matching confused with even complement | Neither remaining 101 barrier type is excluded; ordinary existence and positive even-complement weight remain OPEN. |

The finite controls deliberately include nonsource chorded factor-critical
five-cut sides. They confirm that source sector and forced-face hypotheses
cannot be erased. Complete original colour relations are inherited without
modification; local perfect-matching witnesses are not original colour lifts.
No strict completed-source descent or improved point bound is inferred.
