# N45-H3A：HIGH3 到 BASE no-spoke 的獨立前提映射

日期：2026-10-10。BASE `dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`。
判定：**holds under stated hypotheses**。在 [完整共同契約 K1–K13](frozen/authority/common-contract.md)
內，HIGH3 任意大小來源不存在；這是待監督採納的 paper candidate。
沒有新增充分前提、沒有發現映射 gap，沒有自行採納 HIGH3 或完整 HIGH。

入口：[獨立裁決](independent-judgment.json)、[初始 pins](initial-pin-check.json)、
[抽象搬運見證](transport-witness.json)、[只讀 verifier](verifier.py)、
[manifest](manifest.json)、[delivery](delivery.json)。
HIGH2 的在製作中內容及 H3R/H3G 結論均未讀取、引用或修改。

## 1. 凍結範圍與獨立判定

專屬目錄使用 `mkdir(exist_ok=False)` 建立；全部寫入只在此目錄。
8 個 current live pins、6 個 `git show BASE:path` blobs 與各自 manager frozen 副本
逐項 SHA256 相同。全部 frozen 副本再次存在本目錄，不以同步新增的 sibling/HIGH2
檔案作漂移輸入。HEAD 初核為 BASE。Git tracked 狀態已存在四份改動：
`artifacts/c5_excess_two_e4/REPORT.md`、`docs/STATUS.md`、
`docs/c5_kempe_guide.md`、`docs/c5_phase_b_common_lemmas.md`；本稽核沒有修改它們。
完整權威索引見 [inputs](frozen/authority/inputs.json)。

本稽核獨立讀取 BASE [no-spoke exterior](frozen/base/docs/c5_no_spoke_exterior.md)
§§1–5，及其 [完整介面](frozen/base/docs/c5_degree5_interfaces.md) §§1–4、
[list-critical 基礎](frozen/base/docs/c5_weak_list_cores.md) §1、
[三接點 active triangle](frozen/base/docs/c5_single_spoke_three_one.md) §§1–3、
[degree-4 K4 tethers](frozen/base/docs/c5_degree5_tree_components.md) §1。
不把其他稽核的结论作為前提核對的替代。

## 2. CORE：所有 degrees、minimality 都屬於 X 自己

對每一滿足 K1–K13 的有限圖 G，令 e=rb_i、X=G−e=M。
K9/K11 只刪一條 r–B 邊，內部頂點與所有內邊不變，所以有效 H_X=H_G
仍非空連通。r 從原 degree5 降為 X 完整 degree4；s 沒有失邊、完整 degree5；
其他有效內點的完整 degree4 全保留。唯一 X degree5 內點因此是 z=s。
X 是 G 的 disk 子圖，有序 induced B 仍然是原 C5 外框。

K10 **另行假設 X 自己**是拒絕原 literal β 的 inclusion-minimal obstruction。
對每條 f∈E(X)\E(B)，X−f 是真子邊集，故存在完整 β-lift；X 本身沒有。
這就是 BASE edge-minimal β-obstruction 所需的逐非框邊 β-criticality。
沒有從 G 的 Σ-criticality 遺傳 X minimality，也沒有只在 45/54 圖類內 minimalize。
若兩條 X-spokes 的 β 色相同，刪其中一條不改對其內端點的禁色，矛盾
X−f 的完整 witness；故 BASE 所用 spoke 異色性也是 X 自己 minimality 的推論。

原忽略孤立內點集 I 不變，因唯一失邊的 r 仍有 degree4。
每列 γ 的完整 lifts 含同一因子 `Col^I`，每個孤立點獨立四色。
存在延拓與有效圖存在延拓等價，但 witnesses/lifts 不刪這些坐標。
刪 contact 的 X−f 另用其自己的全部 vertices/edges，若新增孤立點也保留自由因子。

## 3. COMPONENT：實際分量恰為 C 與 U，接點 (2,3)

K5/K7/K11 給 H_X−s 的一個完整原分量 U：它連通、只接 s、不接 r，
且其三條原 contacts 恰 sx1、sx2、sx3，三個點相異，全數保留。
另一份 `C={r}∪P∪Q` 連通，因 P/Q 各連通且對 r 的原 incidence 正。
H−{r,s} 除 U/P/Q 無其他分量、沒有跨 piece 內邊；r 不接 U、rs 不存在。
因此 C/U 恰是 H_X−s 的全部實際分量，沒有另造、合併或縮減 piece。

K8 給 s 對 P/Q 各一條原 contact；兩端點位於不同原分量、不能共享同一點。
故 `|N_X(s)∩C|=2`、`|N_X(s)∩U|=3`。C 內三條 r–P/Q contacts 留在 C，
不能把它們再算為 s contacts。K9 給 `N_B^X(s)=∅`。
BASE 使用無序分拆記為 **(3,2)**；具名分量順序本稽核始終記 **(C,U)=(2,3)**。
U 即使任意大、有旁支或 cycles 也完整保留。

K5 的 actual support 非空已給 C/U 實際 B-touch；BASE §2 亦可僅由
minimality/private-cover 加共同 S4 不變性推導此性質。
另原分量中的 s-contact、內簡單路徑和真 B 附件給 s–B 外路，避開指定整分量。
這条路沒有使用被省略的 e，也沒有新增 s-spoke。

## 4. TRANSPORT：任意原拒絕 β 共同搬到 q=01012

[當前權威入口](frozen/current/docs/c5_excess_two_nonadjacent_unit_core45.md) §1
明列 canonical q cells 為 `{6,4,3,1,0}`、T4 cells 為 `{2,5,7,8,9}`；
941 只拒 q0/q1/q3，933 另拒 q2。K2 的共同整圖 D5 像也保色類數。
因此原拒絕 literal β 使用恰三色，而非額外加入「β 是 U 盾中點」前提。

proper C5 三色列的每個色類至多兩點，故大小為 (2,2,1)。將唯一 singleton
旋轉到 b4 後，b0…b3 在剩餘兩色間交替。對整圖所有 assignments 施加同一
S4 置換，把兩交替色搬到 0、1，singleton 色搬到 2、未用色搬到 3，就得 q。
這只需 D5 的旋轉子群；共同反射亦有效但非必要。

具體寫為新列 `γ'_i=π(γ_{ρ(i)})`，其中 ρ 是同一 D5 boundary index map。
boundary 附件索引、supports/ownership、完整 contact 名稱及其順序、全 embedding、
bridges、所有十列 relations、全部 pins 與 ambient 空/非空 fibres 同時搬運。
對每個完整 lift 的每個頂點色都用同一 π；inverse 給 lifts 的雙射，
連同原孤立自由坐標。每條邊 deletion 也共同搬運，故 rejection、X 自身
edge-minimality、degree、實際分量分拆與無 s-spoke 都不變。
原 933 的 q2 rejection 同時搬成其對應拒絕列，沒有被丟掉。
不同 piece 或不同 root 絕不各自挑置換；root swap 僅沿共同 r 降度命名。

[transport witness](transport-witness.json) 獨立列全部 120 proper 三色 literals
的共同 ρ/π 見證，以及 933/941 codes、(2,3) 覆蓋容量的抽象控制。
這些控制為 **triggered and holds** 的 boundary/集合算術，沒有建立 finite HIGH3 source。

## 5. BASE-MAP：逐項父定理前提與 (3,2) 排除

| BASE no-spoke §1 的前提 | 本題映射 | 主要契約 |
| --- | --- | --- |
| 任意有限簡單 induced-C5 disk 圖 | X 只刪 e；原 B 與 embedding 全留 | K1,K9,K11 |
| 有效 H 非空連通 | H_X=H_G；r/s/P/Q/U 全留 | K3,K4,K11 |
| q=01012 edge-minimal obstruction | X 自己 β-minimal；共同 ρ/π 搬 β 到 q | K2,K10,K12,K13 |
| 唯一完整 degree5 內點 z，其餘 degree4 | z=s；r 降為4，其餘點不變 | K4,K9,K11 |
| N_B(z)=∅ | s 原無 spoke，X 未加邊 | K9,K11 |
| H−z 的實際 connected 分量與非空具名 ordered contacts | C/U；(2,3)；共享點保持單坐標 | K5,K6,K7,K8,K11,K12 |
| 所有 boundary 附件、旁支、rotation 及原 identity | X 全保、ρ/π 共同搬 | K11,K12,K13 |

在同一 q 下，令 `R_C,R_U` 為全部原 contact tuples 的完整關係，
`F_D=intersection(set(t) for t in R_D)`。未 pin s 時，每個分量的
boundary lists 大小至少內 degree，contact 端點具有 slack；故 R_C/R_U 非空。
精確接合是 `q∈Σ(X) iff Col\(F_C∪F_U)≠∅`，連同完整 assignments/fibres。
X 拒絕 q 給 union=Col；逐刪分量 incident edge 的 X full witnesses 給兩份
private colors 非空。容量 `|F_C|≤2` 因而迫三接點 U 有 `|F_U|≥2`。
沒有從 marginals 或不同列湊兩個拒絕 s 色。

BASE [no-spoke exterior](frozen/base/docs/c5_no_spoke_exterior.md) §2 原外路、§3
K4-free、§5 三接點至少兩拒色的 active triangle/tethers，在同一實際 U 上適用。
§5 最後十鄰接的 K5，其中 s–外 hub 鄰接使用另一完整原分量 C 中外路的
第一條原 s-contact。與 X 的 disk 平面性矛盾，直接排除 (3,2)。
原 C 不併入 U 的 coloring relation，minor 只反證平面性。
這是 **source exclusion**，不是保留 (2,2,1)/(2,1,1,1) 的 necessary records，
也不是 BASE 其他節的指定 p 延拓；無需 T4 acceptance 或第二拒絕列。
沒有將任何指定 X 延拓當成原 G 延拓。

外部信任另列：[Dvořák 原 PDF](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
的 Lemma 7（p5）及 Theorem 10（p6）：適用於 connected 圖的 degree lists；
不可著色給 tight lists 與 Gallai/blockwise uniform palettes。
已線上核原文並 [凍結 PDF](frozen/external/gallai.pdf)，hash 見 [external index](external-index.json)。
本稽核沿用這項外部定理及指定 BASE paper 論證，沒有宣稱 Python/Lean 證出它們。

## 6. 必要父前提、scope 限制與精確停止點

父定理必要的是：X 的有限簡單 disk/induced B、有效 H 連通、X 自己
拒絕且逐非框邊 minimal、唯一完整 degree5 s／其他 degree4、無 s-spoke、
實際 (3,2) 分量及完整同源附件/relations。β 恰三色讓固定 q 寫法可共同搬運。

K2 的 ε(G)=2、G 的逐邊 Σ-critical，以及精確 933/941 除了保證 β 三色，
不是 no-spoke 排除的必要父前提。K3 的 full B-touch、K5 的 one-sided、
K6 的 actual support 恰真框邊兩端等比父定理更強，限制本題 HIGH3 scope；
不能因父定理較弱就跳過本題 K1–K13 或自行採納較廣圖類。
K4 的原非相鄰双 roots、K7/K8 的完整原分量資料、K9 的原 r 兩 spokes，
用來重建上述 X 前提；不是將父圖 G degrees 直接當成 X degrees。

五項 claim（CORE、COMPONENT、TRANSPORT、BASE-MAP、EXCLUSION）均判
`holds under stated hypotheses`；新增充分前提為空、finding/gap/counterexample 為空。
只裁完整 K1–K13 的 HIGH3 任意大小 candidate。
完整 HIGH composition 還需要使用者 HIGH2 結果、其獨立採納及限定父身份的
窮盡核對；本稽核不裁這些依賴。全部 HIGH、S、N2/E、long、原55、其他 cores、
一般45/54核心存在性及 ε≥3 不由本判定關閉。

## 7. 實際驗證與未執行項目

只讀重播命令（各 exit0、stdout byte 相同、stderr 空，收據內嵌實際 streams）：

```sh
python3 -B audits/2026-10-10-n45-h3a/verifier.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-10-n45-h3a/verifier.py --check
```

收據：[normal](receipt-normal.json)、[seed17](receipt-seed17.json)。
封存負控制使用 nested `receipt.json` payload 的漏列 manifest，必拒絕，實際 exit2；
命令及 streams 見 [負控制收據](receipt-negative.json)。它只校準工具 custody，非 source。
manifest 精確列所有 immutable payload；僅排除 exact top-level manifest/delivery/
receipt metadata，metadata 綁 verifier/manifest/streams hashes，delivery 再綁所有 receipts。
nested 同名檔全部列 payload，沒有 whole-worktree inventory 或 sibling hash。
本新寫 REPORT 的本地 Markdown targets 與 whitespace 均核回；frozen 原文的歷史
links 保持原 bytes，不以 snapshots 內缺少其他依賴當新漂移或修補。

沒有建立或執行 HIGH3 finite source；沒有 source trigger 數。抽象算術控制
和 custody 負控制不承擔任意大小 paper 證明。source realizability 未建立。
没有新增 Lean，`lake build`、原 broad graph 枚舉及 whole-worktree DocGraph 未跑。
既存歷史缺檔、E4 provenance FAIL、whole-worktree DocGraph 62 duplicates 均保留，
本輪未重播或修改它們。精確停止於候選交付，等待監督與使用者 HIGH2。
