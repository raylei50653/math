# N45-PG：五盾邊分割的原 root／附件幾何

2026-10-09。任務 **N45-PG**；交付狀態：完成窄幾何 lemma 與精確 residual，待獨立 paper 審閱。
BASE／本獨立 detached checkout HEAD：`dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`。

**新必要條件。** 共同搬運整圖，使原盾弧為 U=012、L=234、S=40，且 r 為 U 的原 owner。
則原 spokes 只能 `N_B(r)⊆{b0,b2}`、`N_B(s)⊆{b4}`。
三組具名原 K₃,₃ bags 排除 rb4、sb0、sb2，盾弧內點排其餘端點。
同 core β 的零 slack 再迫 S 的每個 s-contact 不接 b0；故 **S 不能是單頂點 piece**。
這項排除指支援仍是框邊兩端的單頂點 S，不是任務外的 singleton-support 分支。

**未關閉 N45-U-LP。** 收到八種必要 spoke 配置、56種正 incidence 整數 profile；
沒有任一完整目標來源、沒有一般任意大小正常形，也沒有全部 LP 排除。
抽象 contraction 的八張 disk embeddings 只表明這一層拓撲條件沒有矛盾。

交付：[checker.py](checker.py)、[certificate.json](certificate.json)、[residual.json](residual.json)、
[具名圖示](shield-geometry.svg)、[inputs.json](inputs.json)、[checks.json](checks.json)、
[MANIFEST.sha256](MANIFEST.sha256)。普通／seed17 replay 均只讀、逐 byte 相等。

## 1. 量詞、全部來源前提與依賴

主 claims 量化任意大小有限簡單 G、整份原 U、原拒絕 literal β；不設 |U|、|L|、|S| 或 k 上限。
G 為 ordered induced C5 B=(b0,…,b4) 的 disk 圖，完整 Σ=933／941 或共同搬運整圖的 D5 像，
每條非框邊 Σ-critical；有效 H 連通、full B-touch，ε(G)=2。
恰兩個原 degree5 roots r,s，rs 不存在；其餘有效內點在原 G 完整 degree4。
H−{r,s} 的完整分量恰為 U,L,S：U 唯一原 unary，唯一原 contact rx 且 owner r；
L、S 均原 mixed，各 root incidence 正；L 原 actual support long，S 原 actual support 恰真框邊兩端。
X=G−V(U)=M 是原拒絕 β 的 inclusion-minimal 45／54 core，r 是降度側。
保原 named／ordered contacts、shared 坐標、全部附件／support、ownership、原 bridges／rotation、
同一字面 β、完整 tuples／fibres（包括空 fibres）與 full lifts。

已採納前提：σ_G(U),σ_G(L),σ_G(S) 長度恰 2,2,1，分割五框邊；U/L support 各為連續三點。
core β 每側 retained spokes 色互異；兩 mixed 對每個 b∈E_s 的 raw forbidden columns 滿額、互斥，
union=E_r^X，五項 zero slack。short 的全部同色 pins 接受，long 必拒絕 (D,D)。
Δ=Σ(X)−Σ(G) 非空；每個 γ∈Δ，全部 X lifts 的 r 投影與原 U contact palette 同 singleton。
E2 的 Q(X) 必要表及 933 q2 完整保留。新幾何不改這些跨列充分前提。

| 依賴 | 精確使用 | 證據／信任界線 |
| --- | --- | --- |
| [權威 N45 §1–3](frozen/docs/c5_excess_two_nonadjacent_unit_core45.md) | 上列原 LP 身份、2+2+1、原零 slack 與 Δ forcing | 新頁 frozen bytes，不冒稱 BASE Git blob |
| [U WIT／U2／RES](frozen/audits/2026-10-09-n45-u/REPORT.md) | 原 witness／原費用、唯一 U、一 long／一 short；pair 子型恰五盾邊 | 任意大小已採納 paper；不重跑 U 控制 |
| [SU-A U-WIT／U-U2／U-RES](frozen/audits/2026-10-09-n45-su-a/REPORT.md) | 核以上 claims 的全部適用前提 | 只沿用已採納結果，不借其判定當新 PG 證明 |
| [BASE E3 nonadjacent §3、§5](base-source/artifacts/c5_excess_two_e3/nonadjacent_notes.md) | 兩 mixed 給 one-sided／原外路；原整份 unit 省略身份 | BASE objects；不重枚舉 |
| [BASE E4 §4、§6](base-source/artifacts/c5_excess_two_e4/REPORT.md) | 原 short diagonal、完整 tuple 接合介面 | BASE objects，不混讀主 worktree 後改 header |
| [原盾弧 §2](base-source/docs/c5_unary_shield_budget.md) | F_P 面定義、邊互斥、σ 內點禁止別的附件 | 純原拓撲；無 coloring replacement |
| [BASE Phase B B-S0／B-C2](base-source/docs/c5_phase_b_common_lemmas.md) | 逐原 piece witness／原外路與逐欄非負五項零 | 沿用任意大小 claims；本輪不用新外部分類 |

所有九個派工 pinned hashes 相符；38項直接輸入、6152條既有 manifests、78個 delivery items、
U 的70個 BASE objects 核對通過，見 [input-manifests log](logs/input-manifests.stdout.log)。
沒有讀 PG／PR／PC 之外的新 worker 判定，沒有等待 PR、委派或對外發布。

## 2. N45-PG-01：whole-frame named partition 與原 outside 面

**量詞／前提。** 任意上述原 LP 圖，使用已採納 2+2+1。
**結論／證據層。** 任意大小 paper 必要 identity；十份具名有限 partition 算術校準。

寫 e_i=b_i b_{i+1}（下標 mod5）。所有 named partitions 恰為

- 取 a∈Z/5、d∈{+1,−1}；
- U 支援 `(b_a,b_{a+d},b_{a+2d})`，盾邊前兩條；
- L 支援 `(b_{a+2d},b_{a+3d},b_{a+4d})`，盾邊接著兩條；
- S 支援 `(b_{a+4d},b_a)`，盾邊最後一條。

真 S 邊選定後，其餘四邊由 U、L 的兩個連續二邊弧切分，只剩兩個 named 次序；故共10份。
它們是一個 whole D5 orbit。root swap 必把 U owner、全部 contacts／附件、rotation、Σ 與 β 一起搬；
交換字面 r,s 後 U owner 隨之變，不保留另一份獨立歸一化的 U。

以下共同搬成 U012／L234／S40，並重命名 **U 的原 owner** 為 r。
Σ 與所有十列字面顏色同步搬運；**不能再独立把拒絕列搬回另一個 canonical mask／q 位置**。
若同時恰有 β(b0)=β(b2)，則兩條 r spokes 不能同時存在，因 β-minimal X 的 spoke 色必互異。
這是 literal equality 條件，不抹去 933 q2 或任一 whole-frame 對齊。

对 P∈{U,L,S}，仍使用原 `K_P=B∪P∪E(P,B)` 和含整份 H−P 的開面 F_P：

| 原 piece | σ_G(P) | actual support | F_P 邊界上的框邊 |
| --- | --- | --- | --- |
| U | 01、12 | 0、1、2 | 23、34、40 |
| L | 23、34 | 2、3、4 | 40、01、12 |
| S | 40 | 4、0 | 01、12、23、34 |

全部原 roots 均在每個相應 F_P；不同 open faces 的閉包可以共用框點和路段。
b1 的內部附件全部屬 U，b3 全部屬 L；原 roots／別的 pieces 都不能接 b1,b3。
不同原 pieces 在 H 中沒有互相接邊；跨盾弧的實際交流只能經具名 roots 或共用框端點。
共用框端點是 b0=U/S、b2=U/L、b4=L/S；不是把兩個原 contact 合併成同一頂點。

**原 witness／外路逐 contact 供給。** 對每一條原 contact e（不只每 piece 任選一條），
Σ-critical 給 γ_e∈Σ(G−e)−Σ(G) 及原 G−e full lift f_e。
`ψ_e=f_e|_(G−P)` 是合法 outside 而不能接回完整 P，否則 G 接受 γ_e。
γ_e、β 及不同 e 的 γ 可以不同；這裡只保同一原圖／原 rotation。
刪 L 時 S 提供避 L 的原 r–s 路；刪 S 時 L 提供避 S 路；刪 U 時 L/S 都完整。
U 若短，對任意其支援補弧點 h，原 full B-touch 供給 H−U 的原 h 附件，
再由 H−U 的連通原路從 r 抵達 h。完全不假設 X 自己 full B-touch。
本轮已有 2+2+1，不另從某個虛構 G−piece 染色收費。

**Coverage／未涵蓋／finding。** pair 的十份 named identities 全覆蓋，piece 任意大小；
不涵蓋 singleton support，沒有原 LP source control。此 identity 仍需完整原附件與 rotation。

## 3. N45-PG-02：三組原 K₃,₃ bags 迫 spokes 的位置

**量詞／最弱充分前提。** 任意有限簡單平面 G，含互斥 connected 原 sets U,L,S、
互異 r,s、五個具名框點；保上述 U012、L234、S40 的每個 actual attachment、
rx、r–L、s–L、r–S、s–S 原 contacts 及五框邊。
不需要 degree4、Σ、β、criticality、full B-touch 或 X 身份。
**結論。** rb4、sb0、sb2 各不可能。結合 §2 原盾內點限制，得

`N_B(r)⊆{b0,b2}`，`N_B(s)⊆{b4}`。

以下每格是 **原 vertex set**，U/L/S 代表完整原 piece，不是新原頂點。
取 u_i∈U、l_i∈L、v_i∈S 為其原 b_i 附件端點；
取 l_r,l_s,v_r,v_s 為相應原 root contacts。它們在同一 piece 中允許 shared；
root 與框點互異，三份 piece 的頂點集合互斥。每個 shared contact 只用原單一頂點。

| 假設存在的原 spoke | A1、A2、A3 | B1、B2、B3 | 非 singleton bag 的連通原邊 |
| --- | --- | --- | --- |
| rb4 | U；{b4}；L∪{s} | S∪{b0}；{b2,b3}；{r} | sl_s，b0v0，b2b3；U/L/S 自身連通 |
| sb0 | U∪{b0}；L；S | {r}；{s}；{b4} | b0u0；U/L/S 自身連通 |
| sb2 | U∪{b2}；L；S | {r}；{s}；{b3,b4} | b2u2，b3b4；U/L/S 自身連通 |

每行六袋互斥、各連通。九條 A_i–B_j 相鄰**全部由原邊供給**：

| 假設 | A1–B1／B2／B3 | A2–B1／B2／B3 | A3–B1／B2／B3 |
| --- | --- | --- | --- |
| rb4 | u0b0／u2b2／xr | b4v4／b4b3／b4r | sv_s／l3b3／l_rr |
| sb0 | xr／b0s／b0b4 | l_rr／l_ss／l4b4 | v_rr／v_ss／v4b4 |
| sb2 | xr／b2s／b2b3 | l_rr／l_ss／l4b4 | v_rr／v_ss／v4b4 |

故每行為原 K₃,₃ minor，與平面性矛盾。bag 內可選原 spanning tree；九條原邊均已具名，
沒有外加 outside apex、沒有補 rs、也沒有把收縮圖當染色替代。
root exchange 與所有10個 whole D5 搬運都逐項搬此六袋與九邊；checker 核60份模板。

**Coverage／未涵蓋／finding。** 本 lemma 對任意大小 connected bags 普遍成立，包含 shared contacts。
有限模板只核 symbolic bag 的連通／互斥／九邊，沒有新有限 source。singleton-support 不在 premises。

## 4. N45-PG-03：原 root 面／bridge 與 contraction 的限度

**量詞／前提。** 上述同一原 LP 圖及原一側分量連通性。
**證据層。** 原連通與 bridge 的任意大小必要 identity；八張 contraction disk 控制另列。

選原 L 中的 simple contact-to-contact 路（shared contact 可長0），連原 r、s；
同樣選原 S 路。兩條 r–s 路內部互斥且不碰 B，形成長至少4的原 Jordan cycle。
每條 mixed root-contact 都在這樣一個原 cycle 中，故 **不是 H 的 bridge**。
`rx` 是 H 的 bridge，刪它恰隔開完整 U；它未必是 G 的 bridge。
這些結論沒有把原 L/S 私有 bridge 樹或外部附件壓成可染色 star。

[圖示](shield-geometry.svg)與 certificate 的八張 embeddings 只畫拓撲 minor：
刪去多餘原邊，在 U/L/S 各取 spanning tree 並收縮，同原 disk embedding 保留需要的附件／contacts。
canonical minor 的有界 faces 為

`01U,12U,23L,34L,40S,U2Lr,UrS0,L4Ss,LsSr`，外面為 01234。

r 在 U 一側的中央位置，可接 b0,b2；s 在 b4 一側，可接 b4。
選用 optional spokes 會分割相應面；checker 核每個 dart 恰一次、vertex rotations 一圈、Euler=2、
指定 B 外面。這是原圖必要 minor 的面證書，不是「每個原 attachment 都在這張小圖上」。
原 pieces 的多個 contacts、port 次序、shared 頂點、內部 faces／bridges 均需另保原資料；
不從小圖還原一個不存在的 source。

**Coverage／未涵蓋／finding。** 原外路與 bridge identity 任意大小成立。
八種 spoke 小圖都抽象 planar，所以只有這個 contraction 層不足以排全部 LP。

## 5. N45-PG-04：同列零 slack 的實際 s-contact／框附件限制

**量詞／最弱充分前提。** 原 connected degree4 mixed P，全部外鄰在 B、r、s；
共同 proper literal β；非空 E_s；對每個 b∈E_s 的完整原 forbidden r-column G_P(b)
非空。LP 中由已採納 U-CAP 的 `|G_P(b)|=k_P^r≥1` 供給。

**結論。** 若原 v∈P 同時是 s-contact 且附著框點 h，則 `β(h)∉E_s`。
證明：若 b=β(h)∈E_s，固定任意 r=a、s=b。原 v 的 s、h 外鄰同色，
其 degree-list 有 strict slack；其他點 lists 大小至少原 internal degree。
以 v 為最後點的原 spanning-tree 貪婪染色，全部 P 可染，對每個 a 都產生整份 lift。
所以 G_P(b)=∅，與非空矛盾。這只查同一 β，沒有跨列加禁色，亦不用端點 marginals。

LP 的 X 沒有 unary，§3 給 s 只有 optional spoke sb4，故：

| s 原 spoke | 原 E_s | s-contacts 的原 B 附件必要條件 |
| --- | --- | --- |
| 無 | Col | L、S 每個 s-contact 都沒有 B 附件 |
| 恰 sb4 | Col∖{β(b4)} | 每條 s-contact 的 B 附件色都等於 β(b4) |

尤其 **S 的 s-contact 永不附著 b0**（proper β(b0)≠β(b4)）。
L 的 s-contact 永不附著 b3；對 b2，只有原 sb4 存在且 β(b2)=β(b4) 才未被此條件排掉。
這是實際原頂點／原邊限制；shared r/s contact 同樣適用，不能另造 shared ownership。
沒有 sb4 時 shared r/s contact 不碰 B，其 internal degree 恰2；
只接 s 且不接 r 的 s-contact internal degree 恰3。這些是原 degree4 identity。

**Coverage／未涵蓋／finding。** 任意大小局部貪婪 paper，原 LP zero-slack 跨所有 b 供給。
完整目標來源 0 控制；這不能從抽象 profile 推 s-contact 的存在或不存在。

## 6. N45-PG-05：排掉 edge-pair 支援的單頂點 S

**量詞／全部前提。** §1 原 LP，另 S 整份恰一個頂點 v。
原 mixed 與 actual support40 迫原邊 rv、sv、b0v、b4v；四邊已用盡原 degree4。
於是 s-contact v 也接 b0，違反 §5，故此子型不存在。

checker 對 support 兩個不同字面顏色的12種賦值，保 S 的完整16 pins 的全部單頂點 lifts。
當 s=β(b0) 時每個 r=a 都有 lift，forbidden column 真為空；
s 無 spoke或只在 b4 時 β(b0) 都在 E_s，故不能符合正值欄飽和。
這是原四邊局部 oracle；沒有一份完整目標 G，不叫數學來源反例。

**證據層／coverage／界線。** 任意大小 LP 的窄 paper 排除＋12份固定 local negative controls。
只關 `|V(S)|=1` 的 LP 子型。`|S|≥2`、singleton support、一般 U／N2／E 均不被此排除。

## 7. N45-PG-RES：最小精確 profile 與原 graph 義務

**量詞／前提。** 每份未被上述窄 lemma 排除的 LP；必要身份，不宣稱可實現。
保原全部物件後，canonical necessary profile 可以只用

- `T_r⊆{b0,b2}`、`T_s⊆{b4}`，共8種 spoke sets；
- `m_r=4−|T_r|∈{2,3,4}`、`m_s=5−|T_s|∈{4,5}`；
- `k_L^r+k_S^r=m_r`、`k_L^s+k_S^s=m_s`，四個 k 全正；
- U 的唯一原 contact rx；`|L|≥2`（單點接三框加兩roots違反degree4）、`|S|≥2`；
- 原 supports U012／L234／S40、全部具名 actual edges、§5 s-contact 附件限制；
- β 同側 spokes 色互異、完整 L/S 逐欄满额互斥分割；同色(D,D)由 L 禁止；
- 全 Δ 的原 U palette／全部 X r-projections 同 singleton；保七格 Q(X) 表與933 q2。

56種整數 profile 的計数為 `(3+2+2+1)×(4+3)`；
四項分別是 r 無／0／2／02 spokes 的正 split 數，s 的兩項是無／4 spokes 的正 split 數。
這只是原 degree arithmetic，尚未施加 literal β 碰撞或實際 attachment／degree／rotation／relation 存在。
**56不是 survivors，更不是56個 source**；也不由有限零survivor決定任意大小排除。
例如抽象 `T_r=02,T_s=4,k_L=(1,2),k_S=(1,2)` 符合 degree identities，
是否有原 pieces 與十列 relations 仍未知，未補造 vertices 或 lifts。

精確停止點 **N45-PG-OPEN-PORT**（機器欄位見 [residual.json](residual.json)）：
證明／反駁在這些 necessary data 下，能否有同一任意大小原 G 同時具有

1. 每個原 contact 的實際頂點、shared identity、ownership、原 bridges／cyclic rotation，
   完整 U/L/S degree4 attachments 及原 C5 disk 外面；
2. 完整10列 Σ=933／941（whole D5 同搬）、每條非框 critical contact／內邊／附件的原 full witness；
3. X 恰省完整 U、拒絕 β、每條 retained 非框刪邊接受 β 的 inclusion-minimality；
4. 每列全部 ordered relation tuples、空 fibres／full lifts，core β 的逐欄分割和全部 Δ forcing。

原 support geometry 及 root incidence 證明未提供任意大小 piece 正常形。
若想用固定 templates 排剩餘分支，仍須先證 **N45-PG-NF**：
每個合法原 LP 可映到有限 named templates，保原 interface／attachments／geometry／
全部十列 relations 與 critical／minimal witnesses；沒有此 lemma 就不能擴 k 枚舉充當完備。
本輪在 OPEN-PORT 停止，不枚舉新圖／新 pieces、不開下一 residual、不重開 U1–U4。

## 8. 重播、輸入／輸出封存與實際檢查

```sh
python3 -B audits/2026-10-09-n45-pg/checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-09-n45-pg/checker.py --check
python3 -B audits/2026-10-09-n45-pg/verify_inputs.py
```

certificate 保存10 named partitions、60 whole-D5/root-swap bag 模板、8 abstract disk embeddings、
56 necessary integer profiles、12份單點 S 全16 pins/full local lifts。完整目標來源0；未 import PR/PC 判定。
生成使用 `open('xb')`；重复生成実際 exit1 拒覆寫，既有 certificate hash 不變。
普通及 seed17 `--check` 都在記憶體重建、逐 byte 對比且不寫文件。
每條正式命令的 argv／cwd／actual exit／stdout／stderr 在 logs；checks.json 索引並區別預期拒絕與失敗。

| 檢查 | 實際結果／限制 |
| --- | --- |
| 九 pinned hashes、38 inputs、6152 manifests、78 delivery items、U 70 BASE objects | exit0；fresh source HEAD=BASE，clean |
| 新 finite 正常／seed17只讀重播 | 均 exit0，逐 byte 相等 |
| 重复生成 exclusive-create guard | **exit1**，FileExistsError；certificate 不被寫入 |
| fresh BASE `scripts/check_docs.py` | **exit1**；兩份歷史缺檔原樣保留 |
| fresh BASE formal DocGraph | exit0，62 documents／213 relations／5 families，0 errors／notes |
| shared whole-worktree DocGraph | **exit1**，62 duplicate-id errors；含本輪及其他保留 source 副本，不刪副本掩蓋 |
| shared tracked diff／本交付文字、JSON、連結、manifest／final input drift | 逐項實際結果見 checks.json 與 logs；不以 unrelated tracked changes 當本交付修改 |

fresh BASE 缺檔：`audits/2026-10-04-task-d5/c4/scope_ledger.json`、
`audits/2026-10-04-task-d2/integration_doc_changes.diff`，未補造。
歷史 E4 core_constraints／reductions replay 的 E3 provenance FAIL：
歷史 SHA `6d385639c565e2dd08eb61d7835f5fbfec29cd7c467ce8e5abba1dfc2e39e659`，
BASE E3 SHA `73ed652a55b159a44eb6da4608f11537efc0d43603128094101ef044a96b2cd3`。
沿 [已封存 provenance](frozen/audits/2026-10-09-n45-su-a/historical-provenance.json) 明列，
本輪不再重跑或改掉歷史 FAIL；這與兩缺檔／DocGraph duplicates 分開。

第一次 bootstrap 把 J certificate 路徑猜成 out/fixed.json 而 exit1；
保留已寫八份 frozen inputs 與失敗紀錄，再依 J declared digest 找到 results/certificate.json。
未覆寫已封存 bytes，恢復後全部九 pins／既有 exact manifests 通過。
沒有把這個工具路徑錯誤寫成數學 finding。

上游 E3/E4 大枚舉、原 S/U/SU-J finite controls、U1–U4、Lean build 均未重跑：
新 paper 不靠新 Lean 或新外部 Gallai 定理，本輪有限只核固定拓撲／局部邊模板。
無 Lean source/theorem/native_decide 變更；這份 paper lemma 未 Lean 化。

## 9. 統一返回與 scope

CLAIM：PG-01 named partition／outside，PG-02 原 K₃,₃ spokes，PG-03 原面／bridge identity，
PG-04 s-contact附件，PG-05 單點 S 窄排除，PG-RES exact profile／OPEN-PORT。
任意大小新證明與 finite symbolic controls 明列分層；沒有來源實現、完整 LP 排除或 source 反例。
僅可新增排除 |S|=1 的 edge-pair LP 子型；全部 LP、singleton-support、一般 N2／E、原55／其他 cores 保 OPEN。

全部交付只在本 fresh PG 目錄（含自己的 clean BASE checkout）；
未改共享 HANDOFF／STATUS／guide、其他 worker、原證書或 source 副本。
不 commit／push／PR／對外訊息、不委派；保留所有歷史 FAIL 和新命令 exit1。
父題只核已指定權威頁§1–3、BASE E4§4/6 與 B-S0；交監督驗收後才可傳播新必要條件，
本輪不寫共享路由／不自行改一般分支為 CLOSED。
