# N45-S-LONG-S-JOINT：U owner=s 的完整 lift 鏈有限校準

2026-10-11。任務 `N45-S-LONG-S-JOINT`；派工 BASE
`f2692089ad4259808e27d9b7e882ac09505b180a`。
**固定 19 圖、全部 21 個 eligible 原 spoke 省略的完整 lift 鏈核對相等。**
這是固定有限介面校準；target source 與 private-cover 均 **not triggered**。
不提出新的來源排除、來源實現或 Lean 定理，成果 **待獨立驗收**。

## 1. 契約、輸入與寫入界線

本任務逐項保留 [long-contract §1](frozen/audits/2026-10-10-n45-s-long-contract/REPORT.md)
的 K1–K12，另固定原 U owner=s。這些是待排來源的假設，不能預填成控制圖已滿足。

| ID | 完整来源前提／資料義務 |
| --- | --- |
| K1 | 任意大小有限簡單 disk G；具名 ordered 外框 B=(b0,…,b4) 為 induced C5；完整原 vertices、edges、rotation。 |
| K2 | 完整有序 Σ(G)=933／941，或共同搬運整圖的 D5 像；每條非框邊 Σ-critical。 |
| K3 | 有效 H 連通，ε=2；恰兩個原完整 degree5 roots r,s，rs 不存在；其他有效原內點完整 degree4；原 full B-touch。自由孤立點另留全部染色因子。 |
| K4 | H−{r,s} 的完整原分量恰 U,L,S；U 只接 s，L/S 都接兩 roots；原 actual supports 非空，原件 one-sided。 |
| K5 | L 的 actual support 不包含於任何真框邊兩端；S 的 actual support 包含於真框邊兩端；真 pair／singleton 分開，不假設 S 單頂點。 |
| K6 | 只刪具名原 spoke e=rb_i；V(X)=V(G)，E(X)=E(G)−{e}；完整原 U/L/S、接點邊、附件與 bridges 全保留。 |
| K7 | 固定原拒絕 literal β，X=G−e=M 自己是 inclusion-minimal β-core，root degrees=(4,5)，不能另取小 core 冒稱 X。 |
| K8 | 原 U owner=s，n_U≥1，不假設 unit；shared r/s contact 是同一 actual vertex／tuple 座標。 |
| K9 | 原 named/ordered/shared contacts、ownership、edges、actual attachments/support、bridges、rotation、框順序跨列不變；D5/S4/root swap 共同搬整圖全部資料。 |
| K10 | 十 literal 代表保全部 16 ordered pins、diagonal、空 fibres；全部 relation tuples、全部 preimages、全部 full lifts。 |
| K11 | 原 G 每條非框邊 f 有其 Σ-critical witness γ_f∉Σ(G) 及 G−f 完整 lift；不同邊／piece 的 γ_f 可不同。 |
| K12 | X 每條 retained 非框邊 f 有同一 β 的 X−f 完整 witness；與 G−f 的圖、列、assignments 分開；恢復 e 另核 r 色。 |

實際 H_X−s 的兩分量為 C={r}∪L∪S 和完整 U。
令 P_C、P_U 為繼承原 piece contact_order 的 s 接點序列；shared contact 不重複造座標。
m_s=|P_C|、n_U=|P_U|，t_s 是原 s-spoke 數，m_s+n_U+t_s=5。
不預設 β 是 U 盾中點，933 的 q2 保留：q0,…,q4 的十列 indices=(6,4,3,1,0)，
941 原拒絕 q0/q1/q3，933 另拒絕 q2。

入口 [HANDOFF](frozen/docs/HANDOFF.md)、[STATUS](frozen/docs/STATUS.md)、
[N45 §§1/2.9/3](frozen/docs/c5_excess_two_nonadjacent_unit_core45.md)、
long-contract §§1–7 與 [long-r-map](frozen/audits/2026-10-10-n45-s-long-r-map/REPORT.md)
已讀；後者只提供既有介面／停止點，不重開 U-owner=r 分支。
有限工作只讀 contract inputs 指定的 19 份 N2 控制及其 19 份原 orbit 圖。
原 canonical_edges 是本次重建依據，control pieces 只提供原 ID 和 ordering，其他字段逐項對回原邊。

[inputs.json](inputs.json) 凍結 51 份實讀權威輸入：每份列原路徑、SHA256、bytes、
BASE Git blob 或精確 BASE archive 來源。首次凍結在舊 certificate-v2 的直接 Git blob
查詢 exit128，setup exit1；[失敗記錄](setup-attempt1.json)與實際 stdout/stderr 保留，
39 份已凍結檔保留。該 logical 路徑在 BASE 由 `audits/ARCHIVE.json` 及 gzip blob 管理，
沒有獨立 uncompressed Git blob，故明列 `git_blob=null`，並列 archive Git blob。
本次核 BASE manifest、壓縮 SHA256、解壓 bytes 與磁碟舊證書完全相等：
`41c3b82ab4afdade42f70b722a2624a9d1a726a4af22f783a09ab32a099b4ed6`。
這是同一 BASE 的儲存形式辨識，未更新基準或採用不同來源。contract delivery 的歷史 routing
hashes 不當成當前 BASE；共享 docs 用本次 BASE 自己的 blobs。

只新增本目錄。共享 docs、舊 audits／證書及其他任務輸出只讀；不使用同批其他任務新結果。
同一任務內有一份只讀子核對，記於 [reviews.json](reviews.json)，不代替交付後的獨立驗收。
未 commit/push/PR、未發外部訊息、未擴 graph/k。

## 2. 原兩 mixed → actual C：未 pin s 的全部 assignments

Col={0,1,2,3}。十個 literal γ 依序為
`01012,01021,01023,01201,01202,01203,01212,01213,01231,01232`。
對原 mixed T，Λ_T(γ) 枚舉全部 internal edges 與 actual B attachments 的完整 assignments；
Λ_T°(γ;a) 只再加所有原 r-contact 避 a，**此時不 pin s、不加 s-contact 避色**。
Λ_U(γ) 同樣未 pin s。

用 X retained r-spokes 定義 A_r^X(γ)=Col−γ(N_B^X(r))。原兩 mixed 記 P,Q；
在來源契約它們是 L,S，兩 short 控制仍用原 P0/P1/P2 IDs，不造 long 身份。

\[
\Lambda_C(\gamma)=\coprod_{a\in A_r^X(\gamma)}
\{r\mapsto a\}\times\Lambda_P^\circ(\gamma;a)\times\Lambda_Q^\circ(\gamma;a).
\]

限制／union 在原 vertices/edges 上互逆：兩 mixed 互斥，跨件只經原 r，
它們所有 r 接點不等式及 retained r-spokes 全在右式，C 沒有被替換或收縮。
checker 在左邊直接按 C 原邊枚舉，在右邊按同一 a 接合，逐份 assignment 比較；
每個 C assignment 保存唯一 `[r色,第一mixed assignment index,第二mixed assignment index]`。
完整兩 mixed relation 及所有 tuple preimages 另逐項對回 frozen v2。

R_C(γ) 把全部 C assignments 投影至 P_C；R_U(γ) 投影至 P_U；每個 tuple 保全部
assignment indices。C 原 ordered vertices 中含 r，所以 preimages 不丟 r 色。
對整個 ambient Col×Col^{P_C} 明列 Φ_C(γ;a,τ) 的所有 indices，包括 r-spokes 禁色、
無法實現的 τ、diagonal 所導出的所有空 cells。另明列 U 的全部 ambient tuples 與空 cells。
原 mixed 的全部 16 ordered pin assignment indices 亦保留；shared contact 的 r/s
不等式作用同一頂點。checker 不獨立 normalize pieces，不做 D5/S4 搬運。

## 3. C/U → direct X/G：完整接合與恢復式

對全部 (a,b)∈Col²，X 的 full lifts 與下列 product 的 restriction／union 互逆：

\[
1[b\notin\gamma(N_B(s))]\cdot
\{f_C\in\Lambda_C:f_C(r)=a,\ f_C(P_C)\text{ 全避 }b\}
\times\{f_U\in\Lambda_U:f_U(P_U)\text{ 全避 }b\}
\times\mathrm{Col}^{I},
\]

I 是原自由孤立內點集；其全部 assignments 保存為独立自由因子。
certificate 每個 pin 存全部 `[C index,U index,isolated index]`，與該列的 literal B、s=b
及原 graph.vertices order 合併，可無損重建每份全圖 lift。不是只有 counts，也不是選一份 witness。
原 direct whole-X/G 枚舉用固定 vertex order，local pieces 用 MRV；完整集合逐項相比。

對 e=rb_i，c_γ=γ(b_i)，全十列／全 pins 檢查

\[
\mathcal L_G(\gamma;a,b)=
\begin{cases}\mathcal L_X(\gamma;a,b),&a\ne c_\gamma,\\
\varnothing,&a=c_\gamma.
\end{cases}
\]

因唯一恢復邊就是 e，這是原邊上的集合等式。若 X 新接受 γ 而 G 拒絕，
則 X 所有 lifts 的 r 色都恰 c_γ。21 個新接受 **row×omission** 全核此 forcing；
不把它叫整 U 刪除的 singleton forcing。

對 frozen v2 比較時，prior roots 為原數字遞增順序。本次一律按 (r,s)，其中 s 是原 U owner。
14 案例 prior pair 是 (a,b)，7 案例 prior pair 是 (b,a)；每份 G/X 的整對 root 座標共同搬運。
`whole_root_transport_to_prior` 和每個 cell 的 `prior_pins` 明列此排列；literal 色名及原頂點不變。
owner-r 的舊 C 證書未當成本次 owner-s 的 C 資料。

## 4. 真實禁色／覆蓋及 private-cover 的觸發前提

在兩個 unpinned relations 非空時，直接從完整 tuples 算

\[
F_C(\gamma)=\bigcap_{\tau\in R_C(\gamma)}\operatorname{set}(\tau),\qquad
F_U(\gamma)=\bigcap_{\upsilon\in R_U(\gamma)}\operatorname{set}(\upsilon).
\]

兩禁色集允許空。由完整接合而不是由 marginals 有

\[
X\text{ 拒絕 }\gamma\iff
F_C(\gamma)\cup F_U(\gamma)\cup\gamma(N_B(s))=\mathrm{Col}.
\]

理由是給定 s=b，可各自選完整 C/U 避 b 的 assignments；兩分量沒有互相約束。
C 中已含全部 retained r 限制與所有 r 色。局部非空不是從已 pin s 的 joint 推回來的。
本固定域逐列直接確認 Λ_C、Λ_U 非空，210 份覆蓋等價逐項核對。
對任意來源援用此式，須另交局部非空或明確的空 relation 語義；本次不把控制圖校準當作無界來源證明。

紙面條件導式：若同一 X 實際拒絕 β，且全部 retained 非框邊都有同 β 刪邊完整 witnesses，
刪 s-contact sv 的 witness 必 s=f(v)，其他 s contacts 與 spokes 都避該色。
v∈C 時給 F_C−(F_U∪β(N_B(s))) 中的 private 色，v∈U 時反向；
刪 retained s-spoke 的 witness 給該 literal 色不在 F_C∪F_U，且 minimality 迫 spokes 色互異。
所有 witnesses 必是 X−f 原邊圖上完整 assignments，不能用 G−f 的不同列代替。
這只是條件式的 witness 解讀，沒有因此證成 K7/K12 或任意大小來源排除。

checker 的 private 正分支只在 actual rejection 才執行，先核全部 retained 非框邊 witnesses。
**本次所有 X 接受十列，故該正分支未實跑，private-cover=not triggered，trigger=0。**
不產生合成拒絕圖或捏造 minimal witnesses；未建立／執行 satisfying target finite source。

## 5. 逐圖、逐案與來源前提覆蓋

下表每條 edge 都是一個 eligible case，均覆蓋上述十列及所有 16 pins。
每案 m_s=2；t_s=1 時 n_U=2，t_s=2 時 n_U=1。全部 X 的直接 mask=1023。
`short` 欄只表示原兩 mixed 真框邊 pair；本域無 singleton S。

| 原圖 | (r,s) | 全部 e | (t_s,n_U) | 原 mixed IDs／支援型 | direct Σ(G) | 原缺 touch |
| --- | --- | --- | --- | --- | --- | --- |
| NA7-0002 | (6,5) | (1,6) | (2,1) | P0/P2：兩 short | 959 | 無 |
| NA8-0014 | (6,5) | (1,6) | (2,1) | P0/P2：兩 short | 1021 | 無 |
| NA8-0015 | (5,6) | (0,5) | (2,1) | P0/P1：兩 short | 1015 | 無 |
| NA8-0016 | (6,5) | (1,6) | (1,2) | P0/P2：兩 short | 1015 | 無 |
| NA8-0017 | (5,6) | (0,5) | (2,1) | P0/P1：兩 short | 1021 | 無 |
| NA8-0018 | (5,6) | (0,5) | (2,1) | P0/P1：兩 short | 1015 | 無 |
| NA8-0020 | (5,6) | (0,5)、(1,5) | (1,2) | P0/P1：兩 short | 1007 | 無 |
| NA8-0021 | (5,6) | (0,5)、(1,5) | (1,2) | P0/P1：兩 short | 1007 | 無 |
| NA8-0022 | (5,6) | (0,5) | (1,2) | P0/P1：兩 short | 1022 | 無 |
| NA9-0010 | (6,5) | (1,6) | (2,1) | P0/P2：兩 short | 959 | 無 |
| NA9-0011 | (6,5) | (1,6) | (2,1) | P0/P2：兩 short | 959 | 無 |
| NA9-0020 | (5,6) | (0,5) | (1,2) | P0 short／P1 long | 1022 | b4 |
| NA9-0021 | (6,5) | (1,6) | (1,2) | P0/P2：兩 short | 1022 | b4 |
| NA9-0022 | (5,6) | (0,5) | (1,2) | P0/P1：兩 short | 1021 | b3 |
| NA9-0023 | (5,6) | (0,5) | (1,2) | P0 short／P1 long | 1022 | b4 |
| NA9-0024 | (5,6) | (0,5) | (1,2) | P0/P1：兩 short | 1021 | b3 |
| NA9-0025 | (5,6) | (0,5) | (1,2) | P0/P1：兩 short | 1015 | b2 |
| NA9-0026 | (5,6) | (0,5) | (1,2) | P0 short／P1 long | 1022 | b4 |
| NA9-0027 | (6,5) | (3,6) | (1,2) | P1 long／P2 short | 1022 | b4 |

每圖 source_coverage 逐項保存完整 degree、ε、有效 H 連通、actual touch、直接 Σ
與缺失／未驗前提；每案保存精確 X_edges、retained spokes、X touch。從原邊驗到的
simple/induced-C5、degrees、components、contacts、附件／支援等不提升成 disk 來源資格。

| 来源義務 | 本次 fixed controls 的核對／缺口 |
| --- | --- |
| K1 | finite simple induced-C5 已按邊核；rotation bytes 與原 orbit 完全相等且保存，disk rotation 拓撲未獨立驗。 |
| K2/K11 | 每圖完整 Σ 直接重算且對回原 mask；全有九個接受列，D5 保接受數，故無 target 933(六列)/941(七列)。原 criticality／各邊 witnesses 未獨立驗。 |
| K3 | 完整 degrees、ε=2、nonadjacent roots、有效 H 連通按原邊核；touch 缺口逐圖列上表。沒有非零自由孤立點正控制。 |
| K4/K8 | 恰一 unary 與兩 mixed、U 原 owner=s、全部 actual contacts 按原邊重建；one-sided embedding 未獨立驗。 |
| K5 | 4 圖有一 long+一 pair-short，但全缺 b4；15 圖兩 short，不冒稱 long source。singleton S 未觸發。 |
| K6 | 全 21 原 r-spokes 建 exact G−e，全原 vertices/其他 edges 保留，actual C/U 與 degree 身份已核。 |
| K7/K12 | 各 X 十列全接受；無拒絕 β，minimality／同 β 刪邊 witnesses 未建立或執行，不能從 G criticality 遺傳。 |
| K9/K10 | 同原邊、原 IDs/order/shared 座標、attachments/support、bridges、rotation bytes、十列全部 relations/preimages/pins/空 fibres/lifts 保留；未驗的幾何不能由保存 bytes 宣稱已驗。 |

## 6. 有限狀態、重播、負控制與封存

獨立 [checker.py](checker.py) 僅用 Python standard library，不 import 研究 checker；
固定讀 [inputs.json](inputs.json) 的圖，`--check` 只讀，生成用 `open('xb')`。
其 labels／inventory 驗證針對這份固定控制，不是任意 named-source validator。
[certificate.json](certificate.json) 是完整 assignments/preimages/fibres 與無損 lift indices；
[claims.json](claims.json) 明列量詞、前提、結論类型、證據與未解義務。

| 有限控制 | 實際覆蓋 | 判定 |
| --- | --- | --- |
| 原兩 mixed → direct C 全 assignments | 21 cases×10 rows=210 | triggered and holds |
| C/U → direct X 全 16 pins，對回 prior full lifts | 3,360 pin cells；X/G 合計 6,720 prior 比較 | triggered and holds |
| 全 pins 恢復 G；新接受列全部 r 色 forcing | 3,360 恢復 cells；21 新接受 row×omission | triggered and holds |
| 真實 F_C/F_U/spokes 覆蓋等價 | 210 rows，Λ_C/Λ_U 全非空 | triggered and holds |
| C 全 assignments／ambient r-tuple fibres | 5,505 assignments；13,440 cells，其中10,240空 | triggered and holds |
| U 全 assignments／ambient tuples | 512 assignments；2,520 cells，其中2,028空 | triggered and holds |
| X 空 ordered pin cells／diagonal | 全16包括diagonal；空cells=1,964 | triggered and holds |
| t_s=0／1／2 inventory | 0／14／7 cases；t_s=0 無控制 | t_s=0 not triggered；其餘介面 triggered and holds |
| 非零孤立點自由因子／singleton S | 沒有此類控制；零孤立時 factor=[[]] | not triggered |
| actual rejection + own minimal witnesses 的 private-cover | X拒絕 rows=0，minimal 正分支未執行 | not triggered |
| 全 K1–K12 且 U owner=s 的 target source | satisfying finite source 未建立／執行；本 inventory trigger=0 | not triggered |

[run_checks.py](run_checks.py) 執行的全部命令、環境、stdout/stderr 和 exits 在
[checks.json](checks.json) 及 `logs/`。普通與 `PYTHONHASHSEED=17` 的只讀重播 exit0，
stdout byte 相同，兩次各核整個本 audit 檔樹的 before/after hash 完全相同。

```sh
python3 -B audits/2026-10-11-n45-s-long-s-joint/checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-11-n45-s-long-s-joint/checker.py --check
```

兩份 exclusive-create 負證書保存不刪：

- [bad-C-r-colour.json](bad-C-r-colour.json)：改壞第一份 C assignment 的 r 色；exit1，精確指出 C_assignments[0][0] value differs。
- [missing-empty-ambient.json](missing-empty-ambient.json)：刪一個真空 ambient cell；exit1，精確指出 fibres length differs。

兩者判定皆 **triggered and holds**，即預期拒絕成立。再次對既有 canonical 生成 exit1
FileExistsError，canonical bytes 零變；該失敗的命令與 logs 保留。沒有覆寫失敗證書。
[custody-before.json](custody-before.json)／[custody-after.json](custody-after.json) 核 frozen inputs、
實際舊 input 路徑及舊 v2 全零漂移。[delivery.json](delivery.json) 列本目錄交付 payload
清單及 SHA256；receipt 自身和其生成／驗證 metadata 的排除名單明列，不把它們算作已hash payload。

最後界線核對首次誤要求整個 workspace 的 untracked paths 都屬本任務，因其他任務並行新增
獨立目錄而失敗；[boundary-attempt1.json](boundary-attempt1.json) 保留此核對失敗與 Git stdout/stderr。
後續只核本次寫入界線、tracked shared diff、BASE 和 frozen/live inputs；其他目錄只在 Git
路徑清單出現，沒有讀其內容或使用其新結果，未刪除／修改任何檔案。

## 7. 證據分層、依賴与精確停止點

- 紙面：§§2–4 是原邊 restriction／union、恢復式與條件 private-witness 導式；待独立驗收，未證含 long 来源全排。
- 外部定理：本次 lift 鏈不新增或调用 Gallai／degree-list 排除；舊 contract/r-map 的外部定理信任不由本次工具驗證或升級。
- 有限控制：只上表固定 19 圖，普通/seed17/負控制核對，不假設它們滿足 K1–K12。
- 來源實現：satisfying target finite source 未建立或執行；零觸發不是來源排除。
- Lean：無新定理，未執行 Lean build；此工具及紙面接口未形式化。
- 一般命題：U-owner=s 含long來源排除、一般 N45/N2/E、其他45/54、55、ε≥3仍未建立。

停止於 **固定有限介面校準**。下一來源義務仍是同一原圖的 K1–K12、實際拒絕 β、
全部 X 同 β minimal witnesses 與原 G critical witnesses、完整 C/U 禁色／private cover，
再按真正 t_s 及 pair/singleton 支援核來源命題種類；本次沒有推进此無界排除。
不擴搜尋，不重開整 U、兩 short 或 U-owner=r 已採分支，不更新共享研究狀態。
