# B cross-review of A's complete rectangles and singleton cubes

Reviewed `../A/PROOF.md` on the shared frozen BASE. The source-conditional
paper statements pass this review; they do not supply a full319 exclusion.

## Complete four-fibre rectangle

The E/F rows have the stated marked sectors, and every split s=t=C row
has exactly the retained r lift D. Under X, the whole AB component of vw
is disjoint from the actual component of zd; swapping it exchanges the
v/w orientation and fixes all other named colours. Under Y, the whole CD
component of u avoids m; swapping it changes precisely the displayed u
colour among the pins. AB and CD have disjoint vertex palettes, so each
operation leaves the other entire induced graph unchanged. Consequently
both separation predicates are preserved and both maps commute on every
private vertex. The four fibre bijections, including simultaneous empty
fibres, follow. No independent full colourings are spliced.

## CD components may flip independently

This independence does not invalidate the singleton assertion. Since z=A,
removing z changes neither CD components nor any independent component
orientation. Every base colouring still extends with z=A. The actual
neighbours m,u exclude both C,D when their colours differ. When m=u=C,
the putative z=D extension has `e=g!=f`; when m=u=D, the putative z=C
extension has the same forbidden pattern. B is always excluded by the
actual neighbour d. Thus **every** full CD-cube member has exactly `{A}`
as its full z fibre, whether m/u are in one component or two and whether
their selected orientations agree or differ.

## BD cube

The preliminary connection of w and d is necessary and correctly proved.
If their full BD components were different, swapping d's component would
give `e=f!=g` while fixing all other named colours, a complete FJ
violation. Hence all BD orientations keep w=d. In each such orientation,
m=u=C and z=v=A remain fixed; z's one candidate fourth colour again
gives `e=g!=f`. Every member therefore has the same singleton z fibre.

## Mixed-link equivalence and induced odd connector

For each actual component, its intersection with the complete z link is
empty, monochromatic in either orientation, or mixed in both orientations.
If no intersection is mixed, orient all nonempty ones to one common colour;
the choices are independent. Conversely one mixed intersection retains
both colours under every orientation. This proves the stated iff without
dropping components or assuming only the displayed pins are neighbours.
Together with the singleton cubes it forces both claimed mixed components
in the same initial full colouring.

When no link edge gives the mixed connection, the globally shortest
opposite-colour neighbour pair has an odd palette path of length at least
three. An interior z-neighbour would yield a shorter opposite-colour pair,
and a chord would shorten the chosen path. Adding z gives the claimed
induced odd cycle of length at least five. CD/BD paths may meet at D and
their induced cycles pass through z, so the new small-cut exclusions do
not eliminate them. A correctly keeps this residual open.

An independent 24-colour-frame calculation in
`REVIEW-A-ALGEBRA.json` confirms all four displayed rectangle rows, the
independent CD m/u cases, the separated-BD violation, and the whole BD
cube extension calculation. All 256 four-component link-intersection
patterns verify the iff over all sixteen independent orientations. These
are algebraic calibrations only; arbitrary-size source authority is the
whole-component argument above and in A's proof.
