# N45-S-LONG-S-T1-RFIBRE：t_s=1 的同源原邊恢復

2026-10-11。BASE `f2692089ad4259808e27d9b7e882ac09505b180a`。
**全部成果待獨立驗收；尚未更新共享研究狀態。**

本輪交付一個任意大小紙面全排候選，覆蓋 assigned 14 schedules × 原 s-spoke
b0／b2，共 28 queries。β=q4 的七個 schedules 直接在原 X 的 retained edges
抽取 K5 minor；β=q3 的七個 schedules 在同一來源上證 q0、q1 各有完整
`r≠2` lift，恢復原 `e=rb4`。每個 q3 schedule 的 Δ 至少含這兩列之一。
T1-P22／941／013／βq3 的兩個 spoke 變體均由 q0 恢復。

這是新增紙面論證，仍需外部獨立驗收。有限核對只校準具名 palette 穩定子與
minor bags；沒有建立、枚舉或執行符合 K1–K12 的 finite target source。
source realizability、新 Lean、一般 N45/N2/E 及 ε≥3 不隨此交付成立。

## 1. 權威、原身份與量詞

開始的只讀 `check_dispatch.py --check` 通過。HEAD=固定 BASE。
指定目錄先核不存在，再 exclusive-create。唯一寫入邊界為本目錄。
[inputs.json](inputs.json) 分開記 12 BASE Git blobs、11 sealed audit SHA256
及 primary Gallai PDF；已驗收 review 未 tracked，其權威是 SHA256，git_blob=null。
派工包 `authority/base/` 與 `authority/sealed/` 是實讀副本。
原 B 的 pending 欄位與所有歷史 bytes 均保留；採納範圍依 sealed acceptance／
corrections，沿用分類 **12+4+10+4** 及 SF-RESIDUAL 的
**SF-T2-Q0-Q1-RESTORED** 依賴補列。

對**每一個任意大小有限原 G**，量詞保留 frozen long-contract §1 K1–K12 全部：

| 條款 | 本輪保留內容 |
| --- | --- |
| K1 | 具名 ordered induced-C5 disk；全部原 vertices、edges、rotation。 |
| K2 | 完整 Σ=933／941 或一次共同全圖 D5 像；所有原非框邊 Σ-critical。 |
| K3 | ε=2，非相鄰原 degree5 r/s；其餘有效內點完整 degree4，原 H 連通、full B-touch；自由孤立點保完整因子。 |
| K4 | 原 H−{r,s} 的完整分量恰 U/L/S；U 只接 s，L/S 均接 r/s；原 pieces one-sided。 |
| K5 | L actual support 非真框邊 pair，S actual support 本輪為原 pair。S 大小不預設。 |
| K6 | 原 e=rb4；X=G−e，保同一 vertex set 與其餘全部原 edges。 |
| K7 | X=M 自己是固定 β 的 inclusion-minimal core；不另取 core。 |
| K8 | 原 ordered／shared contacts、U owner=s、n_U=2；shared vertex 只有一個 assignment 座標。 |
| K9 | 跨列保原 attachments/supports、ownership、bridges、rotation、框順序；whole-source normalization 僅一次。 |
| K10 | 十列、全部 16 ordered pins、diagonal、空 fibres、tuples 的全部 preimages、完整 lifts。 |
| K11 | 原 G 各 retained／omitted 非框邊各自的 Σ-critical witnesses 另留，各邊列可不同。 |
| K12 | X 每條 retained 非框邊的**同一 β**完整刪邊 witness；恢復 e 另核原 r 色。 |

assigned profile `(t_s,m_s,n_U)=(1,2,2)`，原 r-split `(2,2)`，t_r=1；
X 無 retained r-spoke。actual U012／L234／S40、完整 C=`{r}∪L∪S`、
完整 U 恰為 H_X−s 的兩分量。所有 piece 大小、bridge 深度、旁支與 odd-cycle
長度無上界。原 s-spoke 為 b0 或 b2，兩者在 β 都是色0。

繼承已採納紙面必要式（非本輪有限 source 事實）：
`F_C(β)={1}, F_U(β)={2,3}, Q(X)={β}`；C 是 K4-free Gallai tree，
r 在 C 上完整 degree4、incident 兩個原 odd-cycle blocks。
固定 β、s=1，令

`D_T={a∈Col : Λ_T(β;a,1)=∅}`，T=L,S，Col={0,1,2,3}。

β 的 degree4 zero slack 給 `|D_L|=|D_S|=2` 且 `D_L ⊔ D_S=Col`。
原 pair S 的 N-diagonal 給 `1∉D_S`。這些只在當前 β 使用，沒有改名為其它列證書。
U 的結構另逐項建立：在當前 β，U 真拒 s=2（亦拒3），每個 U 點完整 degree4，
所以 tight degree-list／Gallai theorem 給 U 的 Gallai blocks。任一 incident 刪邊
由 degree-list slack 解除此固定色；外部 hub B∪{s} 經 X 的 retained s-spoke 連通。
因此 frozen connected-exterior K4 引理的四條原 tether 及 hub bags 同樣適用於
**完整 U**，排 K4 block；平面性排更大 clique，故 U 的 blocks 也只有 bridges／
odd cycles。這是把該引理前提明列映射到 U，沒有把只敘述 C 的採納欄位冒稱 U 定理。
依賴是 sealed review 所採納 SF-PRIVATE／SF-SPLIT-EXCLUSION、frozen contract §5、
以及 BASE `degree5-tree-components` §1／`degree5-interfaces` §2–3。

缺兩份 direct BASE observations blobs 的 finding 已重新保留：
`c5_no_spoke_exterior/observations.json` 與
`c5_single_spoke_residual_locality/observations.json` 的 git show 均 exit128。
相關 finite replay executed=false；實體／quarantine 不替代 BASE。
以下新論證不讀這兩份 observations，也不依賴其終局有限重播。

## 2. 完整 lifts 與接合介面

Λ_T(γ;a,b) 是**全部**原 T assignments，滿足 actual internal edges、B attachments
及原 r/s contacts 的避色；shared contact 同時核兩限制。Λ_U(γ;b) 是完整 U
assignments 避同一 s 色 b。每個 ordered tuple 保全部 preimages，空 fibre 照留。

在本身份，對所有十列與全部 `(a,b)∈Col²`：

`L_X(γ;a,b) ≅ 1[b≠γ(b_h)] × Λ_L(γ;a,b) × Λ_S(γ;a,b) × Λ_U(γ;b) × Col^I`，

h=0 或2，I 為原自由孤立點；restriction／union 在同一 vertices／edges 上互逆。
完整 C tuple 另保 r=a；未接 s 的 ambient C 是 Col²×Col，U 是 Col²，
其每個 slot 的 source-specific 全 preimage 集都未被替換成 marginals。

原邊恢復是 lift 集合的精確 filter：

`L_G(γ;a,b)=L_X(γ;a,b)` 若 `a≠γ(b4)`，否則為空。

新論證從 actual assignments 的存在性接合出 lift；沒有供給某個實現來源的
數值 relations／preimage 數。coverage 的 fibres 是必要義務與紙面存在性，並非實算來源。

## 3. 固定額外 s-contact 的原 bridge-path 穩定子

**T1-PATH-STABILIZER。** 取實際 T=L/S，刪去 root r 後的原件；外部色為
當前 γ 的 actual B attachments 加唯一實際 s-contact 的固定 b。或取完整 U，
root 為 s，外部僅為當前 B。若該兩-contact 原件拒絕兩個 root 色 F={a,d}，
其 contact 間有奇數長**原 bridge path** P=(x0,…,xℓ)。刪 P 的全部邊得
完整原塊 W_j（含 x_j 及其所有原旁支）。每塊的 residual pair 恰 F。

證明：兩份 root=a/d 拒絕都是 connected degree-list assignment；外部重色只能
增加 slack，因此拒絕迫全部 lists tight。Gallai theorem 給 blockwise-uniform
palettes。沿 contact path 外的 rooted branches，非 root lists 在兩份證書相同；
從 leaf 向 root 扣除後代 palettes，palette 唯一。若 contact block path 含 odd cycle，
該 cycle 第三點（含它的原旁支）強迫兩份 palette 相同，與 contact 所傳非零差矛盾；
所以只有 bridges，兩份 singleton palettes 交替，另一端 tightness 迫長度奇數。

令 D_j 為 x_j 的實際 B 色集合，若 x_j 就是固定 s-contact 亦加入 b；Q_j
為所有 path 外 incident palettes 的聯集。內點兩份 path residual 是 F，端點
扣除 root pin 後分別是 {d}／{a}，故端點也給

`D_j ∪ Q_j = Col−F`。

若 π 固定 W_j 的每個 actual B 色，且 W_j 含 s-contact 時固定 b，則 π 保持
所有非 root lists；rooted uniqueness 迫 πQ_j=Q_j，root actual D_j 也保持。
因此 **πF=F**。這裡看 W_j 的全部 actual 支援，不只 path root 的附件。

固定 s-contact 可在 path 上、旁支內或同時是原 r-contact；它始終只是同一 vertex
的原 list 限制。兩份 r 拒證書共用該 s pin，故上述唯一性與 tightness 逐步有效。
沒有假設 off-β source minimal，也沒有為 off-β lists 預填 palettes。
每次使用本引理，先由當前列的兩個真禁色建立兩份 palettes。

這是 frozen `two-two` §3／`two-two-minor` §2／`branch-palettes` §2 的明列推廣，
沿 finite block tree 歸納承擔任意大小。外部 Gallai PDF p5–6 Lemma7／Theorem10
是紙面信任依賴，已核 local pinned bytes；沒有新 Lean 證明。

## 4. 兩個保留原 edges 的 K5 抽取

**S-MINOR。** 若 S 的相鄰原 path blocks A=W_i、D=W_(i+1) 都 actual touch
b0、b4，令 x=x_i、y=x_(i+1)，J=P+rx0+rxℓ。由 actual L 的 b2 attachment
取原 r→b2 路，內部完全在 L。五個 bags 為

`A, D, X0={b0}, Y4={b4}, Z=(J−{x,y}) ∪ (r→b2 through L) ∪ {b1,b2,b3}`。

J−相鄰 x,y 是含 r 的連通路，ℓ=1 時就是 {r}。A/D 及 L 互不交；原 paths
只在所列端點碰框。五 bags 連通、不交。全部十鄰接：A–D 是 xy；A/D–Z 是
J 各自另一條 incident 邊；A/D–X0、Y4 是 actual attachments；X0–Y4=b0b4，
X0–Z=b0b1，Y4–Z=b4b3。全是 X retained 原 edges，e 未使用。

**U-MINOR。** 若完整 U 的相鄰原 path blocks A,D 都 actual touch b0、b2，
J=P+sx0+sxℓ。actual C 連通且 touch b4，故有原 s→b4 路，內部全在 C。
五 bags 為

`A, D, X0={b0}, Y12={b1,b2}, Z=(J−{x,y}) ∪ (s→b4 through C) ∪ {b3,b4}`。

A/D–X0、Y12 由 b0/b2 attachments；A/D–Z、A–D 由 J；框側三鄰接為
b0b1、b2b3、b4b0。Y12 由原 b1b2 連通，Z 經 b4 連通。全部 bags 不交且
仍只使用 X 的原 retained edges。兩抽取均在同一來源原 geometry 上證非平面；
沒有宣稱這些 minors 保 boundary 著色關係。

## 5. β=q4：七 schedules 的直接來源 minor

本列 S40 actual 邊界色依序是 (2,0)，s=1，`1∉D_S`；故 pair D_S 只可能
{0,2}、{0,3}、{2,3}。原 r-contact path 至少兩個 W_j，至多一塊含唯一
s-contact。取不含該 contact 的塊；它的全部 actual 外色在 {0,2}，置換 (1 3)
保持 lists。§3 迫其 residual D_S 不變，排 {0,3}、{2,3}，所以 D_S={0,2}。

對**每塊**，若缺 b0 或 b4 的 actual 支援，交換所缺的色0／2與色3，仍固定
該塊 actual boundary 色及 s=1，卻移動 D_S。故每塊都 touch b0,b4。
選任一相鄰兩塊，§4 S-MINOR 給原 X K5 minor，與 disk 平面性矛盾。

因此 βq4 七 schedules 的兩個 spoke 變體全排。本步直接核 q4 的 actual 色與
原 e/r 身份；完全沒有把 q4 schedules 稱為未經共同搬運的 q3 對稱像。

## 6. β=q3：從任意大小導出完整原 S

此列 S40 actual 色為 (1,0)，s=1；(2 3) 保持**全部**完整 S constraints。
滿額 `|D_S|=2` 與 `1∉D_S` 迫 D_S={2,3}，所以 D_L={0,1}。

§3 residual {2,3} 的每個 W 必看到外色0、1：若缺某外色，交換它與2，
保持 lists 卻移動 residual。故每個 W 都 touch b0；無 s-contact 的 W 也必
touch b4。若 path 長度ℓ≥3，至少四塊而至多一塊含 contact，必有相鄰兩個
無 contact 的塊；§4 S-MINOR 矛盾。ℓ 是正奇數，故 ℓ=1。
原 r–S block 因此是 triangle；兩塊中恰一塊含 s-contact。該 contact 塊若
touch b4，兩塊都 touch04 又給 S-MINOR，故 contact 塊 actual support 只有 b0。
無 contact 塊 actual support 恰04。

兩塊都不能有原旁支，理由保任意深度：

* 無 contact 塊若有旁支，有限 rooted block tree 有 leaf block。leaf bridge 的
  私有點完整 degree≤1+2=3，矛盾。leaf odd cycle 至少兩個相鄰私有點 x,y；
  各內部 degree2、無 r/s contact，完整 degree4 迫二者各 actual attach b0,b4。
  取 A={x},D={y}，Z 由 leaf cycle 去掉 x,y 的連通餘路、原 block-tree 路徑
  到該 path root、該 root→r 原邊、原 L 的 r→b2 路及 B123 組成。
  與 X0={b0},Y4={b4} 給同樣十條原鄰接的 K5。餘路含 leaf cut vertex，
  所選私有點不在接回 r 的路上，故連通與不交均成立。
* contact 塊只有 boundary b0、最多一個 s-contact。leaf bridge 私有點完整
  degree≤1+1+1=3；leaf odd cycle 至少兩私有點，其中至少一個無 s-contact，
  完整 degree≤2+1=3。皆矛盾。所有 blocks 為 bridges／odd cycles，沒有遺漏 K4。

故原 S 精確為兩點 u,v 的原邊 uv：

`N_G(u)={r,v,b0,b4}`，`N_G(v)={r,u,s,b0}`。

v 是原唯一 s-contact，u 是另一原 r-contact；原 ordered list 若讀成(v,u)，仍
保持該順序，這裡只依 actual incidence 命名，未改色框。這是從無大小上界契約
推得的結構，沒有預設 S 單點、替換 source piece 或刪除實際旁支。

## 7. q0／q1 的同步原 U preimage

q0=01212、q1=01202 在 actual U012 上逐附件完全相同012，故 U 的全部
assignments、ordered tuples、每個 preimage 集與空 fibres 恒等，特別是 F_U 相同。
固定任一列，其未加 s 的完整 U assignments 非空：lists 至少
deg_U(v)+1[v為s-contact]，有 contact 的 strict slack，connected greedy 可染。
取任一完整 contact tuple（兩座標），故 `|F_U|≤2`。

若 s=1、3 均無完整 U preimage，則 F_U(q1)={1,3}。**在當前 q1**兩份
s=1／3 真拒證書給 §3 的原 U bridge path 與 residual13；actual U012 色是012。
若任何 W 缺 b0 或 b2，交換所缺色0／2與未用色3，固定該塊所有 actual boundary
色，卻改變 residual13。因此每塊都 actual touch b0,b2。
任取相鄰兩塊，§4 U-MINOR 矛盾。

所以存在同一 `b∈{1,3}` 與原 U 的完整 assignment，全部 contacts 避 b；這一
assignment 本身同時適用 q0、q1。這不是把 β=010 的 U 拒證書改名為012。
若 q1 pair13 被反設，其 palettes 是由 q1 真拒絕即時取得；β 證書只供原
K4-free Gallai 結構。沒有依賴兩列 marginals 的合成。

## 8. q0／q1 的完整 r-fibre 恢復

兩列的 actual S40 boundary 都是 (2,0)。在§6原 S上，固定上述 b：

| s=b | 加 r pin 前 u list | 加 r pin 前 v list |
| --- | --- | --- |
| 1 | {1,3} | {2,3} |
| 3 | {1,3} | {1,2} |

刪任意 root 色 a 後，兩相鄰點仍可取異色：原两個二色 lists 不相同，若都縮為
singleton，這兩 singleton 必不同；其餘情形有二色的一側可避另一側。
所以**每個 a∈Col**都有同 pins 的完整 S assignment。

固定同一 γ=q0 或q1、同一 b，未 pin r 的 actual L lists 至少
deg_L(v)+1[v∈N_L(r)]，兩個原 r-contacts 提供 strict slack，故完整 L assignments
非空。從其中任一**完整** assignment取其兩個有序 r-contact 色；至少兩個 a
避該兩色。這些 a 都有完整 L preimage，其中至少一個 `a≠2`。
此处只是用完整 witness 證存在，不把 contact marginals 當完整 relation，也不
捏造其他 tuples／preimages。shared contact 的 s 避色已在該 assignment 裡核過。

取該 actual L assignment、同 a/b 的 actual S assignment、§7 同 b 的原 U
assignment，及原孤立點的全因子；restriction／union 得完整同源
`L_X(γ;a,b)≠∅`。兩個原 s-spoke 變體的 γ(b0)、γ(b2) 分別為0、2，
b=1／3 同時合法；X 無 retained r-spoke，r/s 非相鄰，故沒有遺漏 root factor。
兩列 `γ(b4)=2`，選得 a≠2，即恢復原 rb4，得到**原 G** 的完整 lift。

因此在同一原 q3 來源上，q0、q1 都恢復。T1-P22 的 Δ={q0,q1} 可直接使用
q0；q2/q4 本已接受，從未用其鄰列延拓作此 schedule 的反證。

## 9. 全部 assigned schedules、必要空 fibres 與結論

每列均乘原 spoke b0／b2。coverage 保存全部十列、每列16 ordered pins（含
diagonal）、完整 Δ、原 literal e 色、及未提供的 ambient C/U full preimage slots。
下表是紙面候選結論；沒有計為 source realization。

| Σ orbit | Q(G) | β | 完整 Δ | 此輪證據（兩 spoke 都適用） |
| --- | --- | --- | --- | --- |
| 933 | 0123 | q3 | q0,q1,q2 | q0 恢復 r≠2 |
| 933 | 0134 | q3 | q0,q1,q4 | q0 恢復 r≠2 |
| 933 | 0234 | q3 | q0,q2,q4 | q0 恢復 r≠2 |
| 933 | 1234 | q3 | q1,q2,q4 | q1 恢復 r≠2 |
| 941 | 013 | q3 | q0,q1 | q0 恢復 r≠2；T1-P22 |
| 941 | 023 | q3 | q0,q2 | q0 恢復 r≠2 |
| 941 | 134 | q3 | q1,q4 | q1 恢復 r≠2 |
| 933 | 0124 | q4 | q0,q1,q2 | 原 X 的 S-MINOR |
| 933 | 0134 | q4 | q0,q1,q3 | 原 X 的 S-MINOR |
| 933 | 0234 | q4 | q0,q2,q3 | 原 X 的 S-MINOR |
| 933 | 1234 | q4 | q1,q2,q3 | 原 X 的 S-MINOR |
| 941 | 024 | q4 | q0,q2 | 原 X 的 S-MINOR |
| 941 | 124 | q4 | q1,q2 | 原 X 的 S-MINOR |
| 941 | 134 | q4 | q1,q3 | 原 X 的 S-MINOR |

若假設真來源，β 所有 X fibres 空；Δ 全部非空 X lifts 必 r=γ(b4)，所以
全部 `a≠γ(b4)` fibres 是必要空。q3 分支的新證明對選定 Δ 的這些 cells 的
聯集證非空，產生來源矛盾；不指定哪個 source-specific a/b cell 或其 preimage 數。
q4 直接抽取原 source-minor，無需先構造恢复列。其餘 Δ r-fibres 不各自求解，
因每個 schedule 只需一個恢復列或原 minor，已達指定目標。

候選证明之下 assigned domain 無剩餘 OPEN schedule；獨立驗收本身仍 pending。
原 24 schedules 是本輪前的必要域，未改寫上輪證書；本輪僅覆蓋其中14個 t_s=1
schedule 的兩個 spoke 變體。t_s=2 的其餘10 schedules及同批其它任務不在此結論內。

## 10. 校準、custody 與證據界

[calibration-input.json](calibration-input.json) 先固定四色、全部24置換、具名局部
支援子集、bridge path 長度1/3/5、leaf odd cycles長度3/5，及四個 r pins×兩個 s pins
的原 S widget list 控制。[calibrate.py](calibrate.py) 只核必要代數／明列 minor
skeleton bags／widget assignment existence，不搜尋新來源圖，不 import 研究 checker。
這些 skeletons 不具完整 K1–K12 source 身份。

普通／seed17只讀重播一致；指定壞證書負控制保留並拒絕。原生 argv/cwd、stdout、
stderr、exit 全保於 logs，生成與負控制皆不覆寫原證書。未重跑上輪19 controls。
[checks.json](checks.json) 及 delivery 記詳細判定與 hashes；前後 authority inputs、
sealed舊證書和tracked diff均零漂移。

| 層 | 精確結果 |
| --- | --- |
| paper | 本報告任意大小 assigned-domain 全排候選，待獨立驗收；依賴 frozen accepted paper 與 pinned Gallai。 |
| finite calibration | 新固定域 symbolic／minor／list 控制：triggered and holds；壞證書拒絕是驗證器負控制。 |
| finite target source | not triggered；executed=false，trigger_count=null，未建立來源。 |
| source realizability | 未建立；沒有 relations／preimages 數值或新來源證書。 |
| Lean | 未執行 build，未新增 theorem；校準不形式化任意大小 paper。 |
| general N45/N2/E | 未建立；不改共享 docs、採納狀態或同批別的範圍。 |

僅新增本專屬目錄；未改原任務交付、舊證書、共享 docs 或其他 worker 目錄；
未 commit／push／PR、未發外部訊息。完成此窄域候選證明及逐項 coverage 後停止。
