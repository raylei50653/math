# D7 子稽核：§3.3 來源前提與 §2–4 快速複核

2026-10-04。以本任務開始的工作區快照為準；只新增本檔，不修改來源報告、程式或 artifacts。不執行歷史大枚舉，不 import 被稽核 checker。本文的行號以本次工作區原檔為準。

**總判定：本子稽核範圍確認。** §3.3 各來源排除的正文確實支援一般 minimal-q 用法，沒有偷偷套用固定 Σ=933／941 或「恰缺兩列」。其唯一 degree-5、其餘 degree-4 的前提實質用到 ε=1。§2 的連通性、§3 的飽和，以及 §4 明列 K₃,₃ 的九條鄰接均成立。這不是對 §5.2–5.4 或整個 E2 結論的背書。

## 證據層與依賴界線

- 紙面：下文重新推導 degree≥4、H 連通、ε=0 的 core 飽和、不可刪減 root 覆蓋、三／四／五接點的原圖排除與 K₃,₃ branch sets。
- 外部定理：[Dvořák, List coloring and Gallai trees](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，本次開啟原 PDF；Lemma 7 在 PDF p.5 證 degree lists 拒絕必 tight，Theorem 10 在 p.6 給 connected degree-list 拒絕與 Gallai tree、blockwise-uniform assignment 的等價。這兩條適用於同一原分量及每份拒絕 list，不要求完整 Σ 的特定 mask。
- 沿用的紙面＋有限合成：ε=0 的最後單缺失分類，以及 §4 的全 degree-4 原圖結構與尾枝 transfer；已打開原文核對適用前提。本次未把歷史全 degree-4 分類的全部有限拓撲枚舉重新執行一遍。
- Python：本子稽核沒有據既有 checker 通過來判定紙面步驟；另以標準函式庫讀取未按 941 篩選的全 18 endpoint bases 與 8 tail contexts，枚舉全部合法邊界列、枝內完整色指派，獨立確認 20 個 slot 的附件性質及 1,920 個首點色集合等式。五個 E2 checker 的重播與 §5.4 獨立有限核對由總稽核記錄。
- Lean：本子稽核沒有 Lean 驗證；不得把下列紙面證明記為已形式化。

## 1. §3.3 逐格來源前提

E2 `REPORT.md:131–146` 的表只處理原 G 對所選列都是 minimal-q 的分支。先固定一列 q，令 root-spoke 所見色集為 S，A=U∖S。root 各條 spoke 的 q 色互異：若重色，刪去其中一條仍保留同一 root 約束，違反 q-criticality。對每份原 C，未固定 r 時接點有 degree-list slack，故完整 R_C(q) 非空，|F_C|≤|P_C|。刪除任一碰 C 的原邊，在拒絕的 root 色下造成 slack，故把 C 的全部禁色解除。minimal-q 於是迫使各 F_C 覆蓋 A、各有 private color，而且 F_C 不含 S：刪一條 spoke 所釋放的色必能被所有 C 避開。這是同圖整份 relations 的精確 root 查詢，不是 marginal 拼接。

| t／容量分拆 | 原文位置與實際前提 | 自己重推的排除 | 判定 |
| --- | --- | --- | --- |
| 0／(5) | `docs/c5_no_spoke_exterior.md:44–49,128–176`：minimal q、連通 H、唯一 degree-5、其他 degree-4、disk；明示不需 T4 | 唯一 C 有 F_C=U。四份 root 色拒絕 lists 的差為 1_P(e_b−e_a)。原 vertex–block incidence matrix 欄獨立；共同差係數 τ 只許正 K₄ palette U∖{d}、負 bridge palette {d}。active forest 每個 contact 是葉，非 contact 度二，block 度四或二，所以 |P|=2h+2k 為偶數，不能等於 5。沒有先假設 C 外連通或 K₄-free。 | 確認 |
| 0／(4,1) | 同檔 `79–126,180–218,225`，以及 `docs/c5_single_spoke_four.md:73–189` 的被抽出論證 | private-color 覆蓋使 F₁={c}、F₄=U∖{c}。另一原分量提供避開 C₄ 的 r–B 路徑，先恢復連通外 hub 排 K₄。三份禁色在同一 block tree 的共同 τ 使四葉 active forest 恰為兩個正 triangle 加一條負 bridge。左 triangle 三條實際 boundary tethers，加右 triangle 與 r 作一袋，並以另一原分量的外路徑提供最後鄰接，得到 K₅。 | 確認 |
| 0／(3,2) | `docs/c5_no_spoke_exterior.md:180–205,226`：只需三接點、至少兩禁色與上節的外部原路徑；未要求禁色恰兩個 | 二接點至多禁兩色，故三接點至少禁兩色。兩份 palettes 的差在同一 incidence forest 恰有三個 contact 葉，故 forest 連通，葉數公式迫唯一 triangle 加三條 bridge arms。triangle 各點尚有一條原邊，直達 B 或進入不含 contact 的旁支；若旁支不碰 B，以 slack coloring 加四色整體置換拼回，矛盾。因此三條 tethers 存在；三臂、r、B 加另一原分量外路徑成五袋 K₅。 | 確認 |
| 0／(3,1,1) | 同檔 `180–205,227` | 兩個 singleton 至多禁兩色，所以三接點至少禁兩色，同上得到 K₅。此外，在本次 |Q|≥2 來源也直接違反至多兩原分量。 | 確認 |
| 0／(2,2,1)、(2,1,1,1)、(1⁵) | E2 `114–122,136,145–146`；盾弧原文 `docs/c5_unary_shield_budget.md:38–171` | |Q|≥2 已給連通 H、全框被碰。每份原 C 是 unary 且 H−C 連通。Σ-critical contact-edge witness 迫非空 F_C；短支援的兩／三 hub 論證只需 C 的 degree-4、外部避開 C 的 r–B 原路徑，故每份盾弧至少兩邊。同嵌入盾弧邊互斥，三份需六邊而框只有五。固定 mask 的用途已被 E2 §2 自行補出的結構前提取代。 | 確認 |
| 1／(4) | `docs/c5_single_spoke_four.md:35–39,48–71,73–189`：minimal q、連通 H、唯一 degree-5、四具名原 contacts、其餘 degree-4、disk；`22–26` 明示不需 T4 或第二列 | A 大小三，F₄=A。共同 τ 的正 block 必為 odd cycle、不能為 bridge；四葉 forest 只可連通並有恰兩個 triangle。負 triangle 需要三個互異正 triangle，不可能；故兩個正 triangle 恰由單負 bridge 連起，沒有 active 外臂。三條真實 tethers 加原 spoke 給 `168–189` 的五袋 K₅。 | 確認 |
| 1／(3,1) | `docs/c5_single_spoke_three_one.md:35–44,47–150`：同上，但原 contacts 分為三＋一；`22–29` 明示不需 T4／第二列 | private-color 覆蓋迫 F₃=A∖{c}、F₁={c}。三接點兩拒絕的 signed active forest 有恰三葉，唯一 triangle 加三臂。所有 contacts 在 active 結構上，剩餘一條邊不能進另一原分量或回接結構；沒有 B 附件的旁支可用 slack＋置換拼回，所以三條原 tethers 必存在。三臂、{r}、B 加 tethers，最後一條原 spoke 接上，給 K₅。 | 確認 |
| 1／(2,1,1)、(1⁴) | E2 `137,145–146`，與上述盾弧用途相同 | 分量數至少三，直接違反共同五邊盾弧預算。沒有用原 single-spoke「兩列相鄰」出口定理。 | 確認 |
| 1／(2,2) 留待 §5.2 | E2 `137` | 容量總和 4 的所有整數分拆都已列入；其餘四型排除後，(2,2) 是唯一兩分量剩餘。這格只確認分支涵蓋，不判定 §5.2 排除。 | 確認 |
| 2／(3) | `docs/c5_two_spoke_three_contacts.md:28–37,44–159,180–183`：開頭先寫相鄰 spokes，但 §5 明確逐步延伸到任意兩條異色 spokes；不需 T4 或第二拒絕列 | root 有兩種可用色；唯一 C 同時禁這兩色。lists 差及三葉 active forest 給 triangle 加三臂；各 triangle 點完整 degree-4 剩一條 boundary tether，旁支缺附件會 slack 拼回。三臂、root、整 B 及 tethers 成 K₅，spoke 只提供 root–B 鄰接。任意位置兩異色 spokes 作一次全圖色名置換，證明不讀相鄰性，故適用範圍擴張無循環。 | 確認 |
| 2／(1,1,1) | E2 `138`；不可刪減覆蓋推導見本表前的獨立論證 | |A|=2，而三份 F_C 各需一個 private color；private colors 必兩兩不同，三份不可能。也違反盾弧至多兩分量。 | 確認 |
| 2／(2,1) 留待 §5.3 | E2 `138` | 容量總和 3 的所有分拆為 (3)、(2,1)、(1,1,1)，其餘兩型已排。這格只確認分支涵蓋。 | 確認 |
| 3／(1,1) | E2 `139` | root 的三條 q-spokes 異色，故 |A|=1；兩份分量各需 private color 不可能。 | 確認 |
| 3／(2) 留待 §5.1 | E2 `139` | 容量總和 2，排除 (1,1) 後唯一剩餘為 (2)。區域定位原文 `docs/c5_degree5_sectors.md:31–70` 只用 T4、minimal q，不要求完整 Σ 只缺某些列。 | 確認 |
| t≥4 | E2 `141–143` | 任取四個異框點作 spoke 端點，將唯一未選框點與其某個非鄰框點同色，其餘三點各異色，得到 proper T4 且這四個端點四色各異，root 无色。 | 確認 |

對原資料中「Σ=933／941」的關鍵拆解：no-spoke、single (4)/(3,1)、two-spoke (3) 的直接引用來源本來就没有該條前提；E2 不需要擴張那些定理。盾弧工具的原 theorem 的確書寫固定 Σ，但其幾何證明只用連通 P、連通 H−P、框在外面；支援區間補一步用全圖碰齊 B。原 unary 最短支援只用 degree-4、nonempty forbidden witness、避開分量的外路徑。E2 `47–75,114–122` 已另證这些结构，因此這個證明重用成立，應與「原定理可直接套」區分。

## 2. §2 H 連通、§3 ε=0 飽和

**判定：確認。** E2 `47–50` 對有效 v 取 incident nonframe e，使用 G−e 新接受列的完整 coloring，移除 v 後若 deg_G(v)≤3 有可用色，拼回 G，直接反證。這個論證不要求 v 的原 q 所見 spokes 互異。

E2 `52–67` 的未接框點改色與連通性有效。對每個有效 H 分量 C，G_C 的完整 Σ 全收會使其中任何非框刪邊不改全圖交集，違反 Σ-criticality，所以 G_C 至少拒絕一個 singleton 列並有至少四個 actual support 點。若有 C、D 两份，取 C 支援中四點形成循環四點組 A；D 的支援與 A 至少交三點，任何三個循環四點包含一組對角點。以該對給 D，另一組對角點給 C，兩份各自原路徑的框端點交錯、内部互斥，违反 disk Jordan 分離。路徑從 actual 附件構造，沒有把支持超集當附件。

E2 `69–75,82–88` 的單列 core 飽和有效：每份 inclusion-minimal q-core 自己度數≥4且内部連通；ε=0 使原圖有效點全 degree-4，所以 core 内点保留原图全部 incident 邊，沿原連通 H 傳到全圖。最終引 `docs/c5_degree4_guide.md:10–24`、`docs/c5_k4_blocks.md:104–123`：它要求 T4-accepting C5 disk、minimal q、core 自身完整 degree-4；E2 全部滿足。這一步并不要求固定 Σ 或恰缺兩列，得到 Σ=Ω∖{q}，故 |Q|≤1。

## 3. §4 快速複核與前提

**判定：確認（本節快速複核範圍）。** 原 `docs/c5_excess_one_subcovers.md:84–117` 明確抽出 T4／minimal degree-5 相鄰列分離；其 t=3 區域化約只用 T4、minimal q。兩個 sector 來源的精確前提已開啟核對：`docs/c5_sector_3703_exclusion.md:16–27` 要 disk、內部連通、完整 degree≤4、指定 boundary 點恰兩個内鄰，以及指定三拒絕，不要求其餘列接受；`docs/c5_two_rejection_proof_zh.md:26–47` 要相同 sector 圖類與指定雙拒絕，不要求完整 mask。故相鄰分離沒有從「恰缺兩列」出口結論反推。

三點弧每個拒絕位置都有一个拒絕鄰位，full degree-5 minimal core 的相鄰分離迫三列都用真子核心。E2 `99–108` 的省略原身份互斥可直接重推：root 在 core 的 degree=4 時恰少一 incidence；保留的 degree-4 原點保留所有 incident 邊，故只有 spoke 或整份單接點原分量可省略。每份省略圖全 degree-4 且连通、T4 全收，上一節飽和及分類迫恰缺其拒絕列，所以一个具名省略圖不能供兩個不同列。

原 `docs/c5_excess_one_subcovers.md:152–169` 的 unary D membership 歸納没有用固定 mask：每個非 contact 原點的 lists 含 D；在兩份 blockwise-uniform 分解中，逐 leaf-block private 點固定 D membership，再向根扣除共同值，所有未根點對 incident membership 的總和相同，所以根 contact 的 membership 也相同。singleton C 由空 list 直接成立。故全單容量三拒絕的奇數／省略身份矛盾可在 E2 重用。

E2 `162–181` 的 degree-4 核心結構與 transfer 是沿用依賴；本次查 `docs/c5_941_two_spoke.md:60–134`、`docs/c5_941_three_spoke.md:66–98`，证明只读取全 degree-4 原 core 的 paths、actual attachments、proper boundary rows、parent 色。前一文件开头虽有完整 Σ=941，但 §3 的单／双 run 色集合等式與 joint 拼回没有读取941；使用的18 endpoint bases来自全 degree-4 core分类。任意長枝的第一点全可取色保留足以與原 parent 接合，接回 spoke 只是同一 joint 的 r≠b(e) 過濾。没有按不同分量独立重新正規化。

進一步打開 `docs/c5_triangle_path_reduction.md:16–25,31–55,69–102,104–126`：18 bases 是一般 T4-accepting／minimal-q／all-degree-4 單 triangle path-tree 核心的全部 endpoint minors，20 slots 是這 18 bases 的全部原 tails，8 contexts 是其两-run disk minors；沒有按原來源 Σ=941 篩選。獨立小核對直接讀 `artifacts/c5_triangle_branches/observations.json` 的整個 `disk_templates` 和 `artifacts/c5_triangle_path_reduction/observations.json` 的整個 `normal_forms`，只 import 標準函式庫 `json,itertools`：對每個 slot 重驗 X 兩點相鄰或 X⊆L；對每個 two-run form 和全部 240 proper literal boundary rows，以枝內所有合法完整色指派算第一点 domain，與兩點 endpoint 枝比较，全部 8×240=1,920 相等。這是獨立有限補核對；任意長單 run 的首點 domain 仍由色集合遞迴和附件性質紙面推導，任意長 two-run 的偶數 Y run 由固定端色 transfer 推導，沒有從有限長樣本外推。

E2 `189–194` 的 K₃,₃ 直接在原 triangle rxy 中成立。设相鄰 {a,b}為 x、y 的共同实际附件，cde=B∖{a,b} 是原三框點 path。左 {a},{b},{r}，右 {x},{y},{c,d,e} 非空互斥连通。九條跨組來源邊：ax、ay、a–{c,d,e}（a 的非 b 框邻邊）；bx、by、b–{c,d,e}（b 的非 a 框邻邊）；rx、ry、r–{c,d,e}（原 spoke）。三組對右兩個 singleton 共六條加三個至 path 袋的鄰接，恰九条，全不用新接線。

本子稽核不重新宣稱 E2 的 592／1194 有限表已覆蓋任意大小；無界涵蓋責任在原 degree-4 紙面分類與以上 transfer，有限表只處理其末端。

## 4. 建議整合者寫回的限定

1. §3.3 的來源前提可以保留現有結論，但最好將「表内所有来源排除」与「盾弧原证明重用」分开标记：前者的原陈述本来就一般 minimal-q，后者以已另证的 H 连通、全框被碰代替原固定 Σ 前提。
2. §5 开头 `202–204` 说不相邻二点 Q 的每个拒绝位没有拒绝邻位，只在 Q 恰为所选二点时成立；要和 §3.3 对更大 Q 的涵盖协调，宜改写为「所选两列彼此不相邻；若原 Q 还含相邻拒绝，则相应列已落入真子核心分支」。这不构成这里分支树的缺口，因为 §5.4 接收任一所选列有真子核心。
3. 保留本轮与旧分类的证据界线：ε=0 最终单缺失和 §4 任意大小基础沿用历史纸面／外部／有限合成，本次不应称为仅靠新 E2 Python 的独立一般证明。
