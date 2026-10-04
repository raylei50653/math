# D₈：共同前提、共用 contact 與非相鄰新引理

基準 `2ac279b6144cdfcf4ececd7b72f5d287a6f4b4ac`，獨立 worktree
`/home/ray/developer/ai/math-task-d8`。只新增本稽核目錄，不改被稽核文件。
以下 `E3:n`、`E2:n`、`A:n`、`N:n` 分別指基準的
[E3 REPORT](../../artifacts/c5_excess_two_e3/REPORT.md)、
[E2 REPORT](../../artifacts/c5_excess_one_e2/REPORT.md)、
[adjacent_notes](../../artifacts/c5_excess_two_e3/adjacent_notes.md)、
[nonadjacent_notes](../../artifacts/c5_excess_two_e3/nonadjacent_notes.md)。

## 1. E3 §2：32 子集約化

**Verdict：成立。** [獨立程式](independent_foundation.py)不用 repository checker，
直接由 C₅ 的原五邊求誘導分量。完整具名 32 子集在
[independent_foundation.json](independent_foundation.json)。

| 子集類型 | 份數 | c(Q) | \|Q\|+c(Q) | 含 941 形三點？ | verdict |
| --- | ---: | ---: | ---: | --- | --- |
| 空集 | 1 | 0 | 0 | 否 | 成立 |
| 一點 | 5 | 1 | 2 | 否 | 成立 |
| 相鄰二點 | 5 | 1 | 3 | 否 | 成立 |
| 非相鄰二點 | 5 | 2 | 4 | 否 | 成立 |
| 三點弧 | 5 | 1 | 4 | 否 | 成立 |
| 二點弧加孤點 | 5 | 2 | 5 | 自己 | 成立 |
| 四點 | 5 | 1 | 5 | 各含兩份 | 成立 |
| Q=B | 1 | 1 | 6 | 五份全含 | 成立 |

五份 bad triples 為 `013、023、024、124、134`。D₅ 的整圖像恰為這五份，
十份 transport 有兩份映到每個 triple。`Q=B` 的 c 是 1，不能沿用真子集
的 `|Q|−誘導邊數` 而得到 0；本次 BFS 和原 foundation 都正確處理它。
故 E3:67–74 的 iff 成立。E3:59–65 的 cells masks 只供 Q 形狀，不能當
T4 全收來源圖；原文:56–57 已明列此限制。
固定 T4 indices 2/5/7/8/9，拒絕 indices 1/4/6，保留 indices 0/3 自由，
可得完整 masks 恰 `932、933、940、941`（E3:76–85）。
這個約化不把另外兩列預填為接受，也不提供來源存在性。

## 2. E3 §2.1：triple-critical 的逐步前提

**Verdict：成立；不缺 M 自己的 Σ-critical 或 H 連通。**

| 步驟 | verdict | 具體理由與引用 |
| --- | --- | --- |
| 有限 inclusion-minimal M 存在 | 成立 | E3:94–95；有限非框邊集合中保留 B，仍拒絕三列的子集合非空，取 inclusion-minimal，刪後忽略孤立點即可。 |
| M 接受 T4 | 成立 | E3:103；M⊆G，任一 G 的 T4 完整染色可限制到 M，再自由補孤立點。刪邊只能擴大 Σ。 |
| M 繼承 disk、induced B | 成立 | E3:94、103；只刪私有點／非框邊，五框邊全保留，沒有新框 chord。取原同一嵌入。 |
| M 自己 Σ-critical | 成立 | E3:95–96；刪任一 M 非框邊，至少一指定拒絕列接受，故 Σ(M−e)⊋Σ(M)。用的是 M minimal triple 身份，並非由 G criticality 遺傳。 |
| 有效內點 deg_M≥4 | 成立 | E3:96；用前一格給的 M−e 新接受列，保留其染色到 M−v；若 v 至多三鄰，四色可補回。就是 E2:49–52，無精確 mask 前提。 |
| M 的 H 非空、連通 | 成立 | E2:61–68 套在 M 自己；拒絕三列排除只有 B，Σ-critical 排除 Ω 分量。每份非空內分量若拒絕，T4 未接框改色迫四點支援；兩個四點支援各取交錯端點，原 disk 內互斥路徑不可能。 |
| ε(M)≤ε(G)=2 | 成立 | E3:98 的等式逐項非負：掉點用 deg_G≥4，保留點用 M⊆G。有效內點慣例使掉掉的 degree4 點貢獻 0，不誤算孤立點的 −4。 |
| ε(M)=2 ⇒ M=G | 成立 | E3:100–102；掉掉任一 surplus root 將有正第一項，因此所有 surplus roots 保留；第二項全為零，保留點全原邊保留。從 root 沿原 H 連通路徑傳播，所有 degree4 點入 M、全部附件入 M。不是從零 contribution 強迫被掉的 degree4 點存在。 |
| 真子 M 的 E2 適用性 | 成立 | E3:103–104；ε(M) 是非負整數且≤1，M 自己具備 T4、Σ-critical、induced disk、degree≥4、H 連通。ε=0 用 E2 §3，ε=1 用 §5；q₃ 與 q₀/q₁ 非相鄰。E2 結論不需另外三色列接受。 |
| G triple-critical | 成立 | E3:106–108；若某原邊刪後仍拒絕三列，真子图中可取上述 M，與前兩格矛盾。沒有主張 G 對每一列分別 minimal。 |

E2:204 的「每位置沒有拒絕框鄰点」按字面適用於 Q 恰二點；E2 §5 的
分支覆蓋另容許較大 Q（任一列有 proper core 或兩列都 full-minimal），
D₇ REPORT §10.2 亦明列此文字範圍。此處引用 E2 已宣告的非相鄰二列
排除，不要求 Σ(M) 恰缺兩列，因此無新缺口。

## 3. E3 §6／adjacent_notes §3：共用 contact

**Verdict：成立。** 以下只用 A:63–67 完整前提：原 H 連通／碰齊 B，
one-sided 原 degree4 mixed P，a/b 相鄰，兩側唯一原 contact 同為 x，
actual support ⊆原框邊 hk，以及同一份 P 外部合法拒絕染色。

| 步驟 | verdict | 具體理由 |
| --- | --- | --- |
| degree lists tight／Gallai | 成立 | A:69–70；每點完整 degree4，各有至少 deg_P 個可用色。若一處 slack，連通生成樹逆序貪婪可延拓，因此處處 tight，再套 connected degree assignment 的 Gallai 刻畫。 |
| 外集合 X 連通 | 成立 | A:71；H−P 連通且包含 a,b；P 只碰 h,k，故 B−{h,k} 每點由 H−P 碰到。B 與 H−P 的聯集連通。 |
| K₄ 的四條原 tether | 成立 | A:72–73；K₄ 每點已有三 clique 鄰，完整degree4只留一方向，或直接到 X，或沿一 bridge 到不同原外側。任何不碰 X 的外側有限 Gallai tree 必有 terminal private點，內 degree≤3卻沒有框／root外鄰，違反degree4。故每個方向可沿原路到 X。不同方向若重合／回另一 clique 點，K₄便非 block；四方向內部互斥，連通 X 加四 tether 去掉 clique 點構成第五袋。 |
| 多 block 的 terminal 選擇 | 成立 | A:85–86；有限 block-cut tree 有至少兩個不同末端 block。各末端 private點集合互斥，唯一 x 不可能同時 private 於兩個，所以至少一個末端不以 x 為 private。若 x 是 cutpoint，所有末端都沒有 private x。 |
| terminal bridge | 成立 | A:75–76；非 x private葉只有一個 P 鄰，沒有 root鄰，完整degree4需要三個不同框鄰，支援≤2不可能。 |
| terminal odd cycle 的 u,v | 成立 | A:77–78；避開唯一cutpoint可選相鄰private u,v。兩點均非 x、內degree2、root附件空，故各实际接 h,k；刪兩點後 P 仍非空連通且含 x。 |
| 五袋 O 的原連通性 | 成立 | A:79–83；O=(H−{u,v})∪(B−{h,k})。P 剩餘由 x-a/x-b 接 H−P，後者碰 B−{h,k}；後一框補弧是連通三點 path。所有袋互斥。 |
| 十條 K₅ 鄰接 | 成立 | uv、hk 加四條 u/v–h/k 是前四 singleton 的六邊；u/v 各由cycle端邊接 O，h/k各由原框補弧端邊接 O。共十份原鄰接，沒有新接線。 |
| 單 block／singleton | 成立 | A:86–89；單bridge另一端非 x，單odd cycle選相鄰非 x 原點，仍如上。K₄已排除，planarity排≥K₅ clique，只剩 P={x}。完整degree4和simple graph迫兩不同框鄰 h/k，固定pin拒絕等價於四鄰色互異。 |

這個引理**保留** 935 的 singleton mixed，沒有把相鄰 roots 的合法異色
誤當同色 hub，亦沒有宣告所有短 mixed／不同 contacts 都落入 K′。
E3:300–315 的作用僅為明列前提的短共用 contact 入口。

## 4. E3 §5：非相鄰兩個新限制

### 4.1 `(4,4)` core 的 mixed 數

**Verdict：成立。** E3:257–264／N:146–156 的實際前提是同一個 minimal-q
core M，包含非相鄰 z/w，自己全有效內點degree4、接受T4、disk。
沿 degree4 飽和，每個 retained 原 piece 整份、全部附件、全部 root incidence
保留（N:119–136）。M 的 H 連通所以至少一 mixed 保留。
每份 retained mixed 可取一條原簡單 z–w 路，內點只在該piece，長度≥2，
因原圖沒有 zw。兩份不同piece的路只共 z/w，聯合構成原simple cycle，長≥4。
[全 degree4 實際分類](../../docs/c5_degree4_guide.md#2-合成依賴從任意-block-tree-到三種末端類別)
只容许triangle simple cycles，所以恰保留一 mixed。loss(1,1)最多整份省略
一個 incidence(1,1) mixed，因此得到 m=1/2/≥3 的三格，沒有把 M 的
限制誤寫成原 G 只能一 mixed，也沒有聲稱由此排除全部N1–N3。

### 4.2 N-empty 的同色與異色 hubs

**Verdict：成立。** E3:270–275／N:95–115 只要求 P degree4 mixed，
H−P 連通與 N_B(P)=空；不要求 z/w 原相鄰、不讀拒絕列位置。
同一 H−P 取原simple z–w path L。
同色時只用一袋 L，它的 N(P) 交集只有兩 roots且同色；
異色時沿任一原path edge切兩個連續袋，各含且只含對應root，兩袋連通、
互斥、原鄰接。內部path點可取任意色，hub條件僅在與 N(P) 的交集。
每點complete degree4的拒絕lists tight，使收縮每袋不合併同一 P 點的兩條外邊，
满足 [hub原則](../../docs/c5_unary_shield_budget.md#4-定理-bhub-原則)的全部前提。
假如外染色拒絕P，即给原K₅ minor，與disk平面性矛盾。
任一contact edge e的critical新增列染色限制到G−P，再填回**完整**P，
就使G接受同一列，矛盾。因而P不能Σ-critical。
獨立80份hub分袋只驗连通／互斥／原鄰接，不替代Gallai或一般拓撲证明。
`m=1` separating mixed 没有這條 H−P 外路，原文正確停用此引理。

## 5. 外部依賴與證據界線

本次重新開啟 [Dvořák 講義](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
第5頁 Lemma7 和第6頁 Theorem10：連通、lists size≥degree 是必要前提；
不可染後才得tight和原Gallai blockwise-uniform palettes。以上每處都在同一
連通原P及同一份外部拒絕pin驗前提，沒有由Σ-critical直接聲稱每列q-critical。
歷史全degree4分類／E2合成是明列依賴，不重證全部歷史內容，也不把本次
固定Python算術當其任意大小證明。沒有新增Lean／四色定理oracle／一般出口結果。
