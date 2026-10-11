# H-TREE-LEAVES 及 H-SAME-EDGE 的獨立紙面核對

2026-10-11。審查對象為 `../high-contact/REPORT.md`；前提權威仍是本 audit 的
`../BASE.json`／`../frozen/`。本 reviewer 只寫 `synchrony/`。

**裁決：採納 H-TREE-LEAVES 的任意大小局部結論及所列完整來源推論。**
前提是原 C 為tree、没有sharedcontact、**每個**root-contact都是 C leaf。
沒有接點數上界；不是一般tree或一般 k=4 escape。

不可染的 tight degree lists 確實令 D bridges 成為覆蓋所有普通vertices、避開全部
contact leaves 的matching。因原普通vertex誘導的圖也是tree，perfect matching若存在
就是唯一：兩個不同matching的symmetric difference應有cycle，而tree没有cycle。
因此三列D matching相同，沒有錯把逐列不同matching當同一matching。

普通 vertices 至少 C degree2，原 C 的所有 leaves 都是contacts；反方向由命題的
額外前提給出。Matching contraction只在輔助計數tree內進行，不改原lists、附件或relation。
普通units的誘導圖連通，因兩ordinaryunits之間的原path不能經過contact leaf；故可取
terminal unit。其兩個原endpoints至少一個沒有通到另一unit的非D邊。該endpoint y 的
全部非D neighbors都為原contact leaves，數目 `ell=d_C(y)-1` 恰為1、2或3。
這覆蓋任意長鏈及任意branch degree，不需要有限圖大小上界。

三個ell cases均有效：ell1逼原兩個H degree2 vertices同附件邊；ell2逼兩T signatures
逐列異色，只有01／23及01／34兩對，第三色signatures都不是實際原框點；ell3逼三條
不同原框邊的T signatures在三列逐列rainbow，而q0、q1先迫01／40／12，q3三者全2。
單bridge另外由三列T signatures互異及附件單射排除。所有量詞都是同一原C、同一原框。

選出的escape row有原C完整list coloring；保留original root edges的owner不變。
在完整 `(1,0)` 子族，另一原short的N-diagonal lift同列接回；D避開spokes、原rs缺邊，
因此完整來源排除成立。`(1,1)` 不可單憑此escape排除，因为原U可能在該列拒絕；
`(2,0)` 也仍需要另一long同列接受，报告已明確保留這兩個義務。

四contact path控制確實違反「contacts全部為leaves」前提：兩個原內部path vertices也是
contacts。報告把其 `M=I` 當一般局部k=4／tree escape的counterexample是正確範圍，
沒有宣稱它是完整Σ933／941來源。報告的完整fibres有限控制不承担紙面無界完備性。

**另採納 H-SAME-EDGE。** 五原袋 R、S、A、B、F 與根 reviewer 的T-SAME-EDGE一致：
兩原mixed提供內部互斥r–s paths，含原vh的path內點接上B−{a,b}，五袋連通／互斥且
十對鄰接均由原邊給出。中央biconnected block的two-fan提供所需過v的r–s path；
首次碰root前不可能離開原C。long actualsupport至少三點保證 h outside{a,b}；
u=0則full B-touch及roots的完整兩spokes同樣給出此h。
證明不用minor的Σ、degree identity、replacement source或獨立色框正規化。

本審查沒有新增Lean theorem，也沒有實現完整target source。一般原55／N2／E-ARC2
及contact-at-cutpoint／odd-cycle／same-row residual皆維持OPEN。
