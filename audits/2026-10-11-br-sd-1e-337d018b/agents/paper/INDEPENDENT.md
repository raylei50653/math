# BR-SD-1e：獨立紙面推導

2026-10-11。Reviewer：獨立 paper worker。研究 BASE：
`337d018bfaddfe6b39f7cdc3f3c8ec8bc7c4075f`。
本稿在讀取主端 PROOF／REPORT／MAPPING 前完成；之後仍需精確版本整合審查。
僅寫入本 worker 的 `agents/paper/`，未改 canonical、原 audits、主端輸出，未 commit／push。

**獨立判定：private-witness 路線對本轮所有允許接點成立，足以給任意大小
candidate scoped exclusion。没有 terminal-lemma 必要前提的障礙需要 routing 補救。**

## 1. 受核合同與依賴

讀取本 audit `authority/INPUTS.json` 及其 BASE frozen inputs：
HANDOFF、DOCUMENTATION、STATUS 的相關 N45／degree-5 條目、
N45§1／§2.11／§3、degree-5 guide§4、interfaces§2／§7、common language、
unary shield 的原 piece／actual support 定義；並讀取1a PROOF／REPORT、
1c PROOF／MAPPING／REPORT／最終 paper review 及1d採納紀錄。
INPUTS 記 actual HEAD／origin-main／remote-main 全等於 BASE、初始工作樹乾淨；
本 worker 沒有另以歷史 HEAD 取代當前 provenance。

全部來源身份仍是同一原有限簡單 ordered induced-C5 disk G，完整Σ933／941或整圖D5像、
ε2、逐非框邊Σ-critical及原 witnesses；原非相鄰degree5 r/s、其餘有效原內點degree4；
原U=0、L long、S actual support恰原真框邊兩端；exact-S只省略r唯一原spoke e，
`M=X=G−e` 自身拒絕同一proper三色β、自身對β inclusion-minimal且保retained-edge full witnesses。
M只s完整degree5，其餘有效內點完整degree4，s內鄰恰不同ordered p∈L、q∈S，
三原boundary spokes全留；sole connected `C=H_M−s={r}∪L∪S`、r split22。
原attachments／ownership／rotation／完整relations／空fibres／full lifts全保留。

原骨架 K 包含任意奇長≥3的三cycle blocks，`J1∩J2={r}`、J3與兩者不交，
J2私有u≠r至J3私有v的原bridge uv；simple p/q外臂接J1/J3私有a1/a3、各長≥0。
臂的off-cycle點互斥且沒有其他骨架接線，允許a3=v及q=a3。
本輪W只指來源自己的非空連通off-skeleton內點集，`N_C(W)={x}`，
`x∈J3∪q-arm`；沒有其他C跨邊、s-contact或J1/J2接線，W屬原S且繼承完整actual pair附件限制。
W與x間可以有多條不同incident邊；不能偷換成「只一條W邊」假設。

## 2. Degree／來源可行性核對

對原x，令 `m=|N_C(x)∩W|≥1`、`k=|N_B^M(x)|`、`t=1[sx∈E(M)]`，
則同一原來源必有 `d_K(x)+m+k+t=4`。以下表格只給必要條件，不能證disk實現。
全保原附件；若來源指定的k已耗盡餘額，就直接結構排除，不能刪附件換空間。

| 原x位置 | d_K(x) | t | 非空W後完整degree4的必要条件 |
| --- | ---: | ---: | --- |
| J3普通點，x∉{v,a3} | 2 | 0 | m+k=2；m=1或2 |
| v≠a3 | 3 | 0 | m=1、k=0 |
| a3≠v，q臂正長 | 3 | 0 | m=1、k=0 |
| a3=q≠v，q臂零長 | 2 | 1 | m=1、k=0 |
| a3=v，q臂正長 | 4 | 0 | m≥1超度，結構排除 |
| a3=v=q，q臂零長 | 3 | 1 | m≥1超度，結構排除 |
| q臂off-cycle內點（非q） | 2 | 0 | m+k=2；m=1或2 |
| q臂正長的末端q | 1 | 1 | m+k=2；m=1或2 |

所有原W點y非s-contact，所以 `d_C(y)+|N_B^M(y)|=4`；S actual pair限制另給
`|N_B^M(y)|≤2`、`d_C(y)≥2`。例如只有一條C邊的W葉點不能以三個S附件補度；
不能拿synthetic leaf fixture當本輪actual來源。
骨架其餘各点degree公式不變，r仍有四條環邊、M中無spoke，G中恰恢復e成degree5。
W在刪r/s後仍透過原S中的x與S連通，不另成unary U或改L/S ownership。
S actual支援的聯集必仍是同一真框邊兩端；新增W附件只能屬此pair。

## 3. Private-witness preservation lemma

取任意原點

`w1∈J1−{r,a1}`、`w2∈J2−{r,u}`。

每個簡單奇環至少三點，排除至多兩個點，故任意環長（包含triangle）都各有一點。
這個選擇不依J3長度、兩臂長度、W大小或x的允許位置。

**Lemma。** 在上述原骨架與單一x接入合同下，兩原w各保持非C割點、非s-contact、
只屬原Ji cycle block，且 `N_C(wi)={prev_Ji(wi),next_Ji(wi)}`。
必要前提是保原骨架全部邊／點、W與骨架互斥、`N_C(W)={x}`且x在J3／q-arm、
沒有其他C跨接或s-contact；不能只以W的owner名S代替接線限制。

**證明。** K與 `C[W∪{x}]` 只共用x。若某個2-connected子圖包含兩側各一個
非x點，刪x就會把這兩側分開，矛盾；所以W不能把原骨架blocks合併。
原骨架bridges仍是C bridges；新增W blocks只掛在x，不要求W本身是path或單bridge。
原w1不在r／a1，原w2不在r／u；它們既不在J3／q-arm，也不等於x。
故W沒有任何邊碰wi，原骨架中它們的全部C鄰居仍恰兩個原cycle鄰點。

刪w1後，J1−w1是一條包含r及a1的連通原path，其餘骨架仍由r／uv連通，
p外臂仍在a1接入；刪w2後同理J2−w2保持r及u連通。
因此K−wi連通，且W仍附著未刪的x，故C−wi連通，wi不是C割點。
block separation又給wi只屬原Ji一個block。

若p臂零長，p=a1已排除；若正長，p在J1外。q位於J3／q-arm，與兩wi互斥。
新W沒有s-contact，因此兩wi都不是s-contact。證畢。

完整原M-degree4迫每份wi恰有兩個實際boundary鄰點：

`N_M(wi)={prev_Ji(wi),next_Ji(wi)} ⊔ N_B^M(wi)`、`|N_B^M(wi)|=2`。

兩個附件原點是否在β下同色，不需先猜測；它們的β色均不可能是未用D。
上述全部鄰點與附件來自同一原M，沒有為接W重做attachment選擇。

## 4. 原lists、原全圖接合及正式外部依賴

令Col為同一literal四色集，D為β唯一未用色。每個原y∈C的list精確為

`L^D(y)=Col−(β(N_B^M(y)) ∪ ({D} if sy原邊 else ∅))`。

全部有效原點完整degree4，且C是刪s後sole實際分量，因此
`d_M(y)=d_C(y)+k(y)+t(y)=4`；不同附件可以同β色，故用
`|L^D(y)|≥4−k(y)−t(y)=d_C(y)`，不先假定lists tight。

若f完整L^D-color C，同一assignment `β∪{s↦D}∪f` 沿全部原B–B、B–C、
s–B、s–C、C–C邊proper，含W內邊、x–W邊與全部原W附件。
s–B合法因β沒用D；其餘各類直接由原lists及f proper核。
被effective-H慣例忽略的原自由孤點保其原full-lift自由因子並各任填Col色。
反方向任意M的β延拓且s=D，其C限制也滿足上述原lists；故是完整assignment等價，
不是contacts marginals或只有可染布林值的替代。
原M拒絕β迫C不可L^D-color。

外部來源：[Dvořák作者講義，Theorem10及blockwise-uniform定義，印刷p.6](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)。
本worker另以web讀作者PDF，抽取本audit frozen PDF全文，並獨立渲染／目視核p.6
（[原頁](gallai-p6.png)）；作者、日期March24,2018及定理前提均一致。
PDF的SHA256為 `50e998fcb016418698ef31b932c6c2e728007f5e3b3348b93744781196ac1aea`。
這是外部紙面依賴，沒有宣稱期刊新證或Lean形式化。

精確套用：C有限簡單連通、L^D是degree assignment、且不可著色。
定理導出C為Gallai tree，並有各實際C-block的palettes P_K，
每個list恰是該點incident palettes的聯集；相交blocks的palettes互斥。
奇環palette大小2，triangle以clique看也大小2，bridge以K2看大小1。
W若含其他非Gallai block，已直接違此必要結論；不需预設W的blocks種類。

## 5. 矛盾與scope裁決

兩wi非s-contact而原boundary附件均不使用D，故 `D∈L^D(wi)`。
Lemma給wi只屬Ji，正式blockwise-uniform equality给 `L^D(wi)=P_Ji`。
所以 `D∈P_J1∩P_J2`；但J1/J2仍在同一原r相交，正式互斥條件给
`P_J1∩P_J2=∅`。矛盾。

所有degree合法x一次覆蓋；飽和x另由degree排除。有限非空W可以任意大小，
任意奇環長≥3、兩原外臂任意非負長、a3=v／q=a3重合均包含。
q接W或臂內點接W確實可失去1c的terminal-q／無額外臂邊前提；本證明沒有套用它。
沒有從cutpoint含D推所有incident palettes含D，沒有使用SD-A、H二連通、
R27 minor、縮臂、四-query變換或其他row補容量。

紙面结論只為BR-SD-1e指定完整來源合同的candidate scoped exclusion；
Σ／criticality／β-minimal／disk／rotation等完整身份仍保留，其中多項強前提未被短反證使用。
不提交actual source；actual target disk、完整來源控制均`not triggered`。
本worker未建立有限controls或枚舉；其量詞不承擔任意大小排除。

完整N45-S-NOU-LS-PAIR、其他split22形狀、多旁支Gallai trees、一般非二連通來源、
其他45／54／55、ε≥3、R31任意長minor、一般N45／N2／E、一般出口及主命題
均保持OPEN。canonical採納另由owner裁決；不重開LOW／HIGH／LONG／U。

## 6. 精度事項與重播

没有阻止本限定纸面结論的finding。主端最终文件仍須明寫：
W是原來源的一份branch，不是向已degree4舊M增邊；保原附件，
單x接入允許多條x–W incident邊；完整自由因子與全原邊接合；
a3=v兩種臂長的degree飽和；candidate／canonical／有限／actual-source／Lean分層。

可重讀外部原頁：

```sh
pdftotext -f 6 -l 6 -layout audits/2026-10-11-br-sd-1e-337d018b/external/gallai.pdf -
sha256sum audits/2026-10-11-br-sd-1e-337d018b/external/gallai.pdf
```

這些命令核依賴bytes及原敘述，不能以hash替代本稿的數學逐步核對。
