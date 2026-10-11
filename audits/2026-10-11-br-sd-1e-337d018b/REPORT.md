# BR-SD-1e：J3／q 外臂單一原 W 的 scoped exclusion

2026-10-11。**結果：指定完整原來源合同不可能成立；任意大小紙面證明完成，
狀態為 candidate scoped exclusion，待 owner 另行批准 canonical 採納。**
同一原 J1／J2 的兩個 private witnesses 對本輪全部允許 W 保持，包含 triangles。
没有修改共享 canonical、STATUS、導覽或 BR-SD-1a／1b／1c／1d 封存，未 commit、push 或發布。

工作目錄 `/home/ray/developer/ai/math`。研究 BASE、初始 actual HEAD、origin/main 與
`git ls-remote origin refs/heads/main` 均為 `337d018bfaddfe6b39f7cdc3f3c8ec8bc7c4075f`，
初始工作樹乾淨，HEAD 相對 BASE 差異為空。唯一新增輸出為本專屬目錄。
原輸入 exact BASE blobs／hash 與即時 Git 紀錄見 [INPUTS](authority/INPUTS.json)。
最終實際回讀及封存核對見 [final validation](validation/final.json)。

## 精確来源域與任意大小結果

[PROOF§1](PROOF.md#1-完整原來源合同與量詞) 展開全部合同；
[MAPPING](MAPPING.md) 對回 BASE [N45§1／§2.11／§3](../../docs/c5_excess_two_nonadjacent_unit_core45.md)、
已採1a／1c及1d採納紀錄。保持同一原 G／原 β／原 M：

- 有限簡單 ordered induced-C5 disk，完整 Σ933／941 或整圖共同 D5 像，ε2，
  逐非框原邊 Σ-critical 與各自 full witnesses；原非相鄰 roots r/s 完整5，其餘有效內點4。
- 原 U=0，L long，S 的 raw actual support 恰同一真框邊兩端。
  exact-S 只省略 r 唯一原 B-spoke e；`X=M=G−e` 自身拒絕同一 proper literal 三色 β，
  自身對 β inclusion-minimal，保全部 retained-edge witnesses。
- M 僅 s 完整5，其餘有效內點完整4；s 恰不同原有序內鄰 p∈L／q∈S及三原B-spokes。
  `C=H_M−s={r}∪L∪S` 是實際 sole connected component，r split22。
- 三個任意奇長≥3的原 cycle blocks，J1/J2只共用r、不交J3；原唯一環間 bridge uv，
  u為J2私有點、v為J3私有點；p/q原simple外臂到私有a1/a3，長度任意非負，允許a3=v。
- 唯一放寬為一份候選原來源自己的有限非空 off-skeleton W，W連通、只在具名
  `x∈J3∪q-arm` 接骨架，無其他cross edge、s-contact或J1/J2接線。
  W屬原S，繼承全部actual附件／pair support、ownership及rotation；不是對舊完整degree4圖加邊。
- 全部原點／原邊、named/ordered/shared contacts、attachments、bridges、rotation、
  同一literal四色集、完整relations／fibres（含空fibres）／full lifts均保留。

**結論涵蓋全部允許接點、任意三環奇長、任意p/q外臂長及任意有限非空W大小。**
沒有實際target disk source提交；這是完整原來源假設的全稱反證。

## Degree、保持性與 D-palette 矛盾

原邊給每點 `4=d_M(y)=d_C(y)+|N_B^M(y)|+1[sy∈E(M)]`。
[PROOF§2](PROOF.md#2-先核全部接點的原-degree-與-support)／MAPPING保存所有重合接點的完整表。
`x=a3=v` 零長時q=a3=v，原C-degree3加s-contact1；正長時原C-degree4。
兩者在接W前已飽和，任何非空W直接結構排除。
其餘v／a3（含零長q=a3）最多容一條W incident edge；ordinary J3點、正長q與臂內點最多兩條。
表中的k均須等於候選來源已有附件數，不能刪附件來容W；供給附件已滿度的其他x亦排除。
W原點沒有s-contact，pair support給k≤2，故C-degree至少2；degree1旁支葉不合法。
容量合法不代表原disk／Σ／minimality可實現。

[Private-witness preservation lemma](PROOF.md#3-可重用-private-witness-preservation-lemma) 保留原
`w1∈J1−{r,a1}`、`w2∈J2−{r,u}`。每個簡單奇環至少三點，排除至多兩點，各集合非空。
W唯一骨架接點在別處，不能合併原blocks或改變原bridges；刪w_i後原環餘路與全部接入口
仍連通，W亦仍在x接合。兩點因此非割點、非s-contact、只屬本環block、C-degree2。
全部兩個原B附件均不使用同一β未用的D。禁止其他跨接線的前提在引理中明列。

完整原邊定義 `L^D=Col−β(N_B^M)−({D} if s-contact else ∅)`，原完整degree4給
`|L^D(y)|≥d_C(y)`。完整C list-coloring iff 原β在同一M上有s=D的完整延拓；
逐類核B–B、B–C、s–B、s–C、C–C（含全部W邊／附件）。被effective-H忽略的原內圖孤立點
沿各自β剩餘list填色，真正無鄰居自由點才任填Col，全部full-lift坐標保留。
M拒絕β，所以C不可著色。

[Dvořák Theorem10／blockwise-uniform定義，p.6](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
給原blocks的palettes及相交blocks的互斥性。
两非割點各只屬本環，故 `L^D(w1)=P_J1`、`L^D(w2)=P_J2`，同一D屬兩palette。
原J1/J2在r相交卻要求兩palette互斥，矛盾。作者PDF與原頁本輪已核，見[SOURCE](external/SOURCE.md)。
W接q／臂內點確可增加其C-degree，舊terminal lemma的末端／無額外C邊條件不能普遍沿用；
本證明的兩private witnesses仍保持，沒有使用terminal lemma、SD-A、H二連通或R27 minor。

## 獨立審查、精度更正與證據分工

獨立[mapping](agents/mapping/MAPPING.review.md) 窮盡原接點degree及q=a3/v重合。
獨立paper先從來源重推[INDEPENDENT](agents/paper/INDEPENDENT.md)，再審查root最終三文件。
精確最終PROOF／MAPPING／REPORT的hash與接受裁決見
[REVIEW.final](agents/paper/REVIEW.final.md)／[ACCEPTANCE](agents/paper/ACCEPTANCE.json)。
它核原G/M身份、任意長度witness存在性、W對block-cut結構的影響、外部刻畫全部前提、
全部原邊延拓等價及scoped量詞；接受紙面候選不構成canonical採納。

保留一項後續範圍精度finding：早期草稿把「兩W分別佔J1/J2唯一triangle witnesses」列為
下一OPEN，但該形狀仍保原J3/q末端，已採1c的可重用terminal lemma可直接排除。
root與paper各自辨認此問題，最終改為一份W佔J1 witness、另一份接J3/q臂的窄候選，
使兩條既有保持保證均失去；未宣稱此候選有actual source或形成完整殘餘分類。
[重建的早期稿](PROOF.reviewed-v1.reconstructed.md) 保留錯誤停止點與早期孤立點措辭；
它是事後依patch重建，早期review當下未hash，不宣稱有該代次exact-byte custody。
最終稿亦精確區分B-only孤立點與完全自由孤點的full-lift因子。
Controls原REPORT末句對J1/J2推廣過寬，[REPORT.v2](agents/controls/REPORT.v2.md) 僅澄清
已採1c合同不重開。另有原controls把數值ε=2誤列缺失前提的精度finding；
[REPORT.v3](agents/controls/REPORT.v3.md) 與v2 scripts／certificates改為由全部G原邊明算ε=2，
actual來源仍not triggered。所有原稿、scripts、certificates／負控制、replays與hash清單均保留，
沒有扩大固定fixture域或改動tuples／lift數。

## 必要最小 controls 與負控制

只用三份允許位置的固定synthetic M、一份禁止接點負控制及兩份小結構／list負控制。
沒有扩大環長、臂長、旁支大小、來源或list域枚舉。
[certificate](agents/controls/certificate.v2.normal.json) 保存全部具名頂點／邊、固定B assignment／附件、
lists、blocks／cutpoints、完整D-query tuples、有序p/q全部16fibres（含空）、完整M/G lifts。

| 固定控制 | 完整M-β lifts | 完整G-β lifts | 狀態／界線 |
| --- | ---: | ---: | --- |
| W接ordinary J3 triangle點w3 | 112 | 56 | private-witness保持 `triggered and holds` |
| W接正長q端點 | 256 | 128 | 保持 `triggered and holds`，q不再末端 |
| W接q-arm內點t | 112 | 56 | 保持 `triggered and holds`，t有額外C邊 |
| 禁止W接J1唯一triangle witness w1 | 16 | 16 | unrestricted保持的 `counterexample`；違本輪接點合同 |
| q=a3=v滿度接點 | 不配置 | 不配置 | 原degree結構排除 `triggered and holds` |
| 4點triangle＋bridge，D只落bridge palette | 完整list fibre空 | 不配置 | cutpoint→所有palettes含D的 `counterexample` |
| actual target disk／Σ／β-minimal拒絕來源 | 未提交 | 未提交 | `not triggered` |

四份synthetic G各由完整原邊核得數值ε=2；四份M都接受β。沒有rotation/disk、完整Σ、逐邊critical／minimal witnesses或
完整來源provenance。不得以它們或零target承擔任意大小來源排除。
只保存D-query；三條s-spokes恰三已用β色，故這些固定β的完整M/G lifts只能s=D，
證書所存即全部fixed-β lifts；沒有冒稱全Σ或另外三色component queries。
獨立[original-edge reader](agents/controls/independent_edges.v2.py) 不import producer，從M原邊重建
附件／lists，另用alphabetical DFS重算全部tuples／fibres／lifts並核block-cut tree。

## 重播、hashes 與驗證範圍

normal／seed17證書byte-equal，479749 bytes，SHA256
`df640b4b5a60929ccd5d1fda4a8018876fff34ff83221d0a92ba3838e41c6705`。
root實際重播紀錄見[root-replay](validation/root-replay.v2.json)：兩checker normal／seed17皆exit0，
非法完整tuple（a1:0→9）與malformed JSON各在兩checker預期exit1，實際均拒絕。
舊1a／1c frozen verifier各exit0，未用發布後不適用的舊`--live`或重生舊controls。
正式文件檢查exit0（601 Markdown、7384 links），正式DocGraph exit0（62 docs、213 relations），
tracked whitespace exit0；它們不裁決數學，既有check_docs不掃新audit。
新audit本地連結／whitespace、全部15個BASE snapshot、206份舊封存／採納歷史的
paths／sizes／modes／SHA256由本輪[verify.py](verify.py)另核，見final validation。

從repo root只讀重播：

```sh
python3 -B audits/2026-10-11-br-sd-1e-337d018b/verify.py --check
python3 -B audits/2026-10-11-br-sd-1e-337d018b/verify.py --check --live
python3 -B audits/2026-10-11-br-sd-1e-337d018b/agents/controls/checker.v2.py --check --certificate audits/2026-10-11-br-sd-1e-337d018b/agents/controls/certificate.v2.normal.json
PYTHONHASHSEED=17 python3 -B audits/2026-10-11-br-sd-1e-337d018b/agents/controls/checker.v2.py --check --certificate audits/2026-10-11-br-sd-1e-337d018b/agents/controls/certificate.v2.seed17.json
python3 -B audits/2026-10-11-br-sd-1e-337d018b/agents/controls/independent_edges.v2.py --certificate audits/2026-10-11-br-sd-1e-337d018b/agents/controls/certificate.v2.normal.json
```

frozen模式仍對回BASE blobs及舊custody，live模式另核HEAD／tracking／remote main與
tracked/index零diff、工作樹只新增本audit；後續HEAD前進時不假造舊live provenance。
[seal-v1](seal-v1.json) 綁immutable payloads及最終review hashes；seal損壞負控制見final validation。
seal／hash驗證只核bytes；任意大小結論由PROOF／獨立審查負責。
全工作樹DocGraph、Lean build、舊大型枚舉及source搜尋均未執行；沒有新Lean theorem。

## 文件責任、下一個最小 OPEN 與停止點

僅本audit L0有新輸出。已唯讀核degree-5 guide§4、interfaces§2／§7、STATUS相關條目、
N45§1／§2.11／§3與1d歷史；它們仍保已採1a／1c及當時1e OPEN語境。
使用者明確禁止canonical修改，候選採納與後續L1/L2傳播留owner另行裁決。
document-first已足夠，未用Graphify；既有LOW／HIGH／LONG／U排除未重開。

本精確單W合同內沒有未解private-witness義務。下一步行政義務是owner對candidate採納決定。
下一個最小數學候選可取兩份原旁支：一份接J1 triangle唯一private點，另一份接J3／q臂，
先核degree／原S pair／原完整來源身份，再問合法palette routing；本輪未研究或分類此形狀。

完整N45-S-NOU-LS-PAIR、其他splits／三環形狀、一般多旁支Gallai trees、其他45／54／55、
ε≥3、R31、一般N45／N2／E、一般出口、主命題及`K∞=K≤5`保持OPEN。
**完整父身份新增無條件closure數0；沒有actual source realization、canonical採納或發布。**
