# BR-SD-1e：精確最終三文件的獨立紙面審查

2026-10-11。Reviewer：獨立 paper worker。研究 BASE：
`337d018bfaddfe6b39f7cdc3f3c8ec8bc7c4075f`。
先完成 [INDEPENDENT](INDEPENDENT.md) 的來源／任意大小推導，再讀取主端三文件與 controls。
本次接受的 exact bytes：

| 檔案 | SHA256 |
| --- | --- |
| PROOF.md | `f184188fc6a18fe84a593b30514ff930783a2d268be9b209775f5c7e223dfd40` |
| REPORT.md | `e6386fabd931c4482186331ab22d839987ec1e2fd59f733ace4adf3ecee054c7` |
| MAPPING.md | `e1b6abc4dd2a27474fc93c40207551e92acd0d8f9b275403788b3b269e0392fc` |

機器可讀裁決見 [ACCEPTANCE](ACCEPTANCE.json)。

**裁決：accepted candidate scoped exclusion。三文件的完整原來源合同、
所有允許接點及任意大小量詞均成立，沒有未解主證明 finding。此裁決不構成 canonical 採納。**

## 1. 原身份與 degree

逐項對回 BASE N45§1／§2.11／§3、guide§4、interfaces§2／§7、common language、
unary actual-support 定義與指定1a／1c／1d frozen inputs。
原 G／M 的完整 Σ 身份、ε2、逐邊 witnesses、exact-S 原 e、M 自身同 β minimal、
完整 degree、原 contacts／附件／rotation／ownership／完整 relations／fibres／full lifts 全保。
短反證只使用其中部分強前提；未將其他前提從來源域刪除。

所有 x 位置的 degree 表窮盡且正確：原J3普通點2、v3、正長a3再加臂邊，
正長q1加s-contact、臂內點2。特別 `a3=v` 的零長／正長情形分別為3+1／4+0，
已有完整度4，任何非空W超度。其餘必要m／k全部由原
`d_C0(x)+m+k+t=4` 算出。k仍是來源指定的實際附件数，沒有刪附件容W。
每個W點無s-contact、S raw pair給k≤2，因此C-degree≥2；不能用三框附件支持W葉點。
局部degree合法不證實際disk、Σ或拒絕來源存在。

W是原來源的一份branch，off-skeleton點連通且只共用具名x，允许多條x–W incident邊；
不是向一張舊已degree4圖增邊。W的S ownership、完整pair支援、原L/S mixed及U=0保留。

## 2. 任意長度 witness 與 blocks 保持

`w1∈J1−{r,a1}`、`w2∈J2−{r,u}` 各至多排除兩點；簡單奇環≥3，
所以任意長度均存在，包括兩個triangle各剩唯一原第三點。
p外臂零長时p=a1已排除，正長時p在環外；q在不交的J3／q-arm，
新增W無s-contact。因此兩wi都不是s-contact。

骨架與 `C[W∪{x}]` 只共用x；跨兩側的二連通block刪x將分離，故不存在。
這個論證不假定W只有一條接入邊，亦不假定W只有一個bridge或是tree。
原cycle blocks、uv及原外臂bridge身份保持。刪wi後原環剩連通path，
r及a1／u原接入口仍在；W保持在x接合，所以C−wi連通。
兩wi仍只屬Ji一個block，全部C鄰居仍恰兩個原cycle鄰點，原完整M-degree4迫兩B附件。
附件由同一β賦色，均不含β未用D；沒有從割點含D猜incident palettes。

## 3. 完整原邊 list 等價與外部定理

每個原y的list按全部M的B鄰居與s-contact定義，含W全部原點／邊／附件。
原完整degree4給 `|L^D(y)|≥d_C(y)`，boundary同色只可能產生slack，
所以不先假定tight。完整C list-coloring與同一M的β延拓且s=D等價，
沿B–B、B–C、s–B、s–C、C–C逐類核，未漏W邊或附件。
若有效H忽略原內圖孤立點，B-only點按 `Col−β(N_B)` 填色（含D）；
只有完全無原鄰居的點才可任填Col；所有原full-lift坐標及因素保持。
這個修訂準確。原M拒絕β迫C不可L^D-color。

獨立讀取 [Dvořák作者PDF](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，
並抽取全文、[渲染目視p.6](gallai-p6.png)；外部PDF hash
`50e998fcb016418698ef31b932c6c2e728007f5e3b3348b93744781196ac1aea` 相符。
Theorem10的實際前提是連通圖的degree assignment；不要求二連通、planarity、minimality
或先驗tight。原C有限簡單連通、lists大小≥degree、不可著色，全部前提已核。
刻畫给list等於incident palettes聯集與相交blocks palette互斥；
兩wi只屬Ji，因此 `L^D(wi)=P_Ji`、兩palette均含同一D。
原J1/J2仍共用r，卻須互斥，矛盾。
沒有使用1c terminal lemma、SD-A、H二連通、R27 minor、四queries變換或W大小分類。

## 4. 保留的精度 finding 與更正

1. **早期下一OPEN過度陳述，已更正。** 兩W只佔J1／J2 triangle witnesses時，
   J3／q臂仍保持原terminal配置，已採1c可重用末端引理可直接排除。
   root與reviewer獨立辨認此問題；三份最終文件改為一份W佔J1 witness、另一份接J3／q臂
   的更窄後續候選，使原雙witness與未改動末端兩個保證均不再可直接套用。
   這只是尚未研究的候選，不是actual來源、已證存活格或完整残餘分類。
   [早期重建稿](../../PROOF.reviewed-v1.reconstructed.md) 保留；reviewer當時未保存／hash該版本，
   故明示事後重建，不冒稱早期exact-byte custody。
2. **孤立點的完整factor精度，已更正。** 早期自由點措辭只適用無任何鄰居的點；
   現PROOF、MAPPING、REPORT明列B-only內圖孤立點按原剩餘list填色。
3. **Controls範圍措辭，已更正。** [REPORT.v2](../controls/REPORT.v2.md) 保留已採1c不重開的界線，
   不把其J1/J2完整來源域再次列為待證。原REPORT仍保存。
4. **Controls數值ε metadata，已更正。** 舊certificates誤將ε2列入缺失前提；
   [REPORT.v3](../controls/REPORT.v3.md)、v2 scripts及certificate改為從完整原G邊算ε2。
   reviewer另直接讀四份全部G邊，重新計degree及ε，均恰2；比較新舊證書移去該metadata後
   固定圖、附件、lists、blocks、tuples、fibres、lifts全部相同。
   見 [CONTROL-METADATA-CHECK](CONTROL-METADATA-CHECK.json)。原versions全部保留。

這些更正沒有改變主private-witness證明或本輪scoped來源量詞。

## 5. 有限、來源、封存與停止點

讀取controls v3、v2 normal／seed17證書及root-replay.v2全部13條結果；
八份新controls回放exit0／預期exit1一致，其餘五項舊frozen／文件檢查亦符合紀錄。
兩證書byte-equal，479749 bytes，SHA256
`df640b4b5a60929ccd5d1fda4a8018876fff34ff83221d0a92ba3838e41c6705`。
四M lifts為112／256／112／16，四G lifts為56／128／56／16；均接受β。
禁止J1 witness接入只反駁撤前提後泛化保持；4點triangle＋bridge只反駁cutpoint D推每環D。
它們不反駁本輪來源排除。完整target disk／Σ-critical／β-minimal拒絕來源仍`not triggered`。
固定controls與零source沒有承擔任意大小量詞。

本worker未重跑solver、source搜尋、舊枚舉或Lean；原邊控制的獨立solver驗證由controls worker負責。
本次另做的metadata比較只核陳述／bytes／固定tuples身份，不能取代紙面審查。
root後續seal與final custody驗證由其實際執行紀錄負責；本裁決只綁上列三文件與其數學／scope。

接受全稱範圍為：同一完整N45-S-NOU-LS-PAIR、split22、三環單bridge原骨架，
恰一份有限非空原W唯一接J3／q-arm、无其他跨接線／s-contact／J1/J2接線，
全部允许x、任意奇環長≥3、兩原外臂長≥0、有限W大小及命名重合。
飽和x結構排除，其餘x由保持引理與D-palette矛盾排除。

canonical採納待owner；完整N45-S-NOU-LS-PAIR、其他splits／三環位置、一般多旁支、
其他45／54／55、ε≥3、R31、一般N45／N2／E、一般出口、主命題及K∞=K≤5仍OPEN。
沒有actual source realization、新Lean theorem、commit／push或發布宣稱。
