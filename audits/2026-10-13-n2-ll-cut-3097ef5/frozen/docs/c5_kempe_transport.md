# Kempe 轉運有限表與 hub-linkage 停止見證

2026-10-04；分支 `shield-budget-hub-principle`，基準
`ca3870f9b79684c2100480d0dc04523899666928`。本報告是任務 K 的獨立交付；
目前研究入口仍見 [Kempe 導覽 §3](c5_kempe_guide.md#3-停止點與保留缺口)。
本輪不修改導覽、STATUS、README、HANDOFF，不 commit、不 push。

**結論：固定 933／941 的猜想 K 未決，且已觸發局部分類的停止條件。**

- 完成兩個固定標號的單一 Kempe block 轉運表：933／941 各 20 筆；
  分別來自 28／21 份完整 noncrossing partitions。
- 有共同 partition 的 a、b 框端點交換共 8／16 筆，全部非交錯。
  因此單靠這張必要表，不能推出「兩側所需的實際 root 鏈必交錯」。
- 小型控制在 singleton P 層已找到具名 `P1-witness-001`：實際 disk、
  roots 各 degree 5、完整 Σ=1012、T4 全收、每條非框邊 Σ-critical；
  拒絕見證無 theorem-B hubs，接點環序也不是指定的 a–c₁–b–c₂ 型。
  停止擴大 P；**沒有完成 ≤6 點的普查**。
- 這否定可實現圖上的一般「hubs 或上述指定交錯環序」二分。
  Σ=1012 不在 933／941 的 D₅ 軌道，故不是固定來源 K 的反例。
  該配置反而有四條碰框且能延拓 P 的交換，沒有否定轉運存在部分。

[Checker](../scripts/c5_kempe_transport_table.py)、
[完整有限表與控制](../artifacts/c5_kempe_transport/observations.json)、
[具名停止見證](../artifacts/c5_kempe_transport/P1-witness-001.json)。
沿用的猜想原文見 [綜合報告 §8](c5_research_synthesis.md#8-2026-10-04-新猜想基準-0b5e00a未證)，
hub 定義見 [盾弧報告 §4](c5_unary_shield_budget.md#4-定理-bhub-原則)。

## 1. 索引的精確語意與證據層

框固定為 B=(0,1,2,3,4)，是外邊界的 induced C₅，其餘頂點私有。
pattern 順序及三色 singleton 位置直接讀取
[cells.json](../artifacts/c5_cells/cells.json)；mask 第 i 位對應 `pattern_order[i]`。
933 拒絕索引 {1,3,4,6}，941 拒絕 {1,4,6}，只按共同 S₄ 色名置換取軌道。
本輪不對框做 D₅ quotient，也不另外 normalize roots。

有限表保留 q、色對、完整 frame block、交換後字面 q′、共同 S₄ 正規化後的
索引，以及容納該 block 的**每份完整 partition**。只 import
[既有 screen](../scripts/c5_kempe_screen.py) 的 `partitions`、`noncrossing` 等純函數；
不呼叫其 `report()`、外側 screen 或目錄枚舉，不使用四色定理 oracle。
每個色對出現在三份 complementary splits 中的一份。
強制同一色對內的框邊端點屬同一 block，再保留 noncrossing partitions。
對每個 block 交換其色對，恰在 q∉Σ 且 q′∈Σ 時收錄。

**側別必須附條件。** artifact 的 `frame_side_contexts` 對所有五條有向框邊
a=i、b=i+1 mod 5，逐筆列出 block 碰 a、碰 b、碰兩者或都不碰，
並記錄端點顏色是否在交換色對內。這是框接點標記。
`actual_root_origin` 明列 UNASSIGNED：設定沒有指定各 root 屬於哪個 Kempe component，
因此不能由 (q, 色對, block) 唯一標成「a 側 root 出發」或「b 側 root 出發」。
具名控制才逐點保存 `roots_in_chain`、`neighbor_incidences`、`psi_prime`，
以及該實際鏈的框側別；不把框側別冒充 root 起點。

**紙面觀察。** 對同一 G−P 染色 ψ 的實際 Kempe component 交換後，ψ′ 仍合法。
若 ψ′ 能延拓 P，則其框列 q′∈Σ(G)；若 ψ′ 仍拒絕 P 且滿足定理 B 的 hub 條件，
則與平面性矛盾。
若交換不碰框，q′=q，而 q∉Σ，所以能延拓或能組 hubs 的內部交換會直接矛盾。
這只是**有用交換的必要條件**，尚未證明一定存在有用交換。
反方向也不成立：q′∈Σ 是對所有外部染色的存在性敘述，
不保證這一份特定 ψ′ 能延拓 P；§4 保存具體例子。

| 證據層 | 本輪內容與界線 |
| --- | --- |
| 紙面 | 上述條件式觀察；索引缺少 root incidence 的界線；singleton 接點環序核對 |
| 外部定理 | 不新增外部定理；定理 B 及 degree-list／Gallai 依賴沿用原報告，本輪不重證。networkx planarity 是有限計算工具，不是任意大小分類 |
| Python 有限證書 | 完整框 partition 表、singleton 附件控制、完整 Σ／刪邊關係、rotation、精確 hub 搜尋、所有實際 Kempe chains |
| Lean | 無新增 theorem；未執行 `lake build`，不宣稱拓撲或 K 已形式化 |

## 2. 完整單一 block 轉運表

下表固定 a=0、b=1，`a／b／—` 只表示該 block 碰到的框端點。
`q′ index` 按共同 S₄ 色名置換計算；完整字面 q′ 與所有五條框邊的側別見 artifact。
一列含兩個 blocks 時是**兩筆單鏈交換紀錄**，不是一次同時交換兩條鏈。

| q index／q | 色對 | frame blocks（逐個交換） | q′ index | a=0,b=1 的框側別 | 適用 Σ |
| --- | --- | --- | ---: | --- | --- |
| 1／01021 | 02 | {0}；{2,3} | 3 | a；— | 941 |
| 1／01021 | 03 | {0}；{2} | 8 | a；— | 933、941 |
| 1／01021 | 12 | {1}；{3,4} | 0 | b；— | 933、941 |
| 1／01021 | 13 | {1}；{4} | 2 | b；— | 933、941 |
| 3／01201 | 03 | {0}；{3} | 8 | a；— | 933 |
| 3／01201 | 13 | {1}；{4} | 5 | b；— | 933 |
| 4／01202 | 03 | {0}；{3} | 9 | a；— | 933、941 |
| 4／01202 | 12 | {1,2}；{4} | 3 | b；— | 941 |
| 4／01202 | 23 | {2}；{4} | 5 | —；— | 933、941 |
| 6／01212 | 02 | {0,4}；{2} | 0 | a；— | 933、941 |
| 6／01212 | 13 | {1}；{3} | 9 | b；— | 933、941 |
| 6／01212 | 23 | {2}；{4} | 7 | —；— | 933、941 |

每個 Σ 各有 20 筆，無其他單 block 能從其拒絕列送到其接受列。
獨立 restricted-growth partitions 枚舉與原生成器逐集合相等；
大小 0,…,5 的 Bell 數為 1,1,2,5,15,52。
此外對每份 q／split 的 admissible partition 集合再次逐集合比對。

## 3. 交錯性：共同 partition 已有非交錯候選

定義 frame blocks A、D 的交錯證據為四個**不同**且循環交替的框點，
第一、第三點在 A，第二、第四點在 D。
只有同一染色中的互斥實際 chains 才能用此條件推出 disk 不可並存。
不同且共享顏色的色對所產生的 chains 可能相交；端點的交錯標記本身不夠。

最小具名表見證在兩個 mask 都是
`KT933-q1-s2-p0`／`KT941-q1-s2-p0`：

\[
q=(0,1,0,2,1),\quad (03\mid12),\quad
\pi=(\{0\},\{1\},\{2\},\{3,4\}).
\]

- a-block={0}，交換 03，字面 q′=(3,1,0,2,1)，正規化索引 8；
- b-block={1}，交換 12，字面 q′=(0,2,0,2,1)，正規化索引 0。

兩者都在 Σ 內，且是**同一**合法 noncrossing partition 的 blocks；
其色對互斥、各 block 是 singleton，沒有交錯的四框點。
這否定「有限表的 a、b 框端點候選必交錯」的裸命題；
不能否定加入實際 root incidence 與來源條件後，某個更窄的所需鏈集合會交錯。

checker 逐份共同 partition 列出 a∈A、b∈D、A≠D 且兩個交換目標都在 Σ 的紀錄。
933：8 筆，覆蓋 20 個 q／框邊項目的 8 個；
941：16 筆，覆蓋 15 個項目的 13 個。全部 noninterlacing。
其餘項目沒有這種共同端點候選，不能因此推得有 hubs 或來源被排除。
這層是必要的框索引，不實現 root wiring，更不實現 Σ=933／941 來源。

## 4. 小型 disk 控制與具名停止配置

預設 P 上限為 6；按照停止規則，完成首個大小層後即停止擴大。
本輪實際只窮舉 |P|=1 的完整命名域：

- 框 B=0,…,4，a=0、b=1；roots z=5、w=6，保留實際邊 zw；
- P={7} 連通、每點完整 degree 恰 4；枚舉其到 {a,b,z,w} 的所有簡單附件；
- z、w 各自在五框點的所有 32 種 spoke 子集，共 1,024 個命名接法；
- 要求 roots 完整 degree≥5、五框點均有內鄰、H−P={z,w} 連通；
- 加一個暫時 apex 鄰接五框點作 planarity 篩選，移除 apex 後驗證 rotation、
  所有 faces 及實際外面 C₅；每張圖保存一份合法 embedding。

184 份接法通過 degree／全框條件，只有 2 份 disk 圖，兩者完整 Σ 都是 1012。
對每張圖的每個拒絕代表 q，再窮舉 G−P 的所有 roots 染色。
分類域是這些 **q∉Σ 的拒絕見證**；可延拓的外部染色不當成阻擋配置。
兩張圖共 4 份見證，全部以具名 `classification_rows` 保存：

| 分類 | 判準 | 本輪數量 |
| --- | --- | ---: |
| hubs 可以組成 | 精確滿足定理 B：互斥連通 bags、兩兩相鄰、覆蓋 N(P)、在 N(P) 上各 bag 顏色常數且不同 | 0 |
| 交錯阻擋 | 實際 P 面上的接點含循環 a–z–b–w 或 a–w–b–z；本輪四個接點顏色互異 | 0 |
| 其他 | 以上兩個判準均不成立 | 4 |

三分類按 hubs 優先、交錯次之、其餘為其他，逐份覆蓋且不重複。
它核對的是**明列的四接點交錯型**，不是尚未定義的所有 Kempe 阻擋型。
P={7} 時 ab、zw 都是實際邊，形成 PabP 與 PzwP 兩個三角形；
這也解釋了此域的接點為何不可能呈 a–z–b–w。

### 4.1 `P1-witness-001`

框邊為 01、12、23、34、40；全部非框邊恰為

\[
06,07,15,17,25,35,36,46,56,57,67.
\]

P={7}，N(P)={0,1,5,6}，S_P={0,1}。
內點 degrees=(5,5,4)，ε=2；H−P={5,6} 連通，R={5,6}。
取 q=01012，ψ(5)=2、ψ(6)=3；外部每條邊都合法，
P 的四個外鄰顏色恰為 {0,1,2,3}，因此 L(7)=∅，是完整拒絕見證。

保存的外面是 (0,1,2,3,4)，P 的 clockwise rotation 為 (5,1,0,6)，
即 **z–b–a–w**，不屬於指定交錯型（循環起點及反向均已核對）。
這是在 P 邊界的接點順序，與 §3 在 C₅ 的 Kempe block 交錯是兩種不同檢查。

hub 搜尋保留每個鄰點顏色的所有可連通 candidate bags，
允許 bag 內其他非 N(P) 頂點取任意顏色。
四個顏色各有 4、4、6、6 個 candidate bags，全部 576 個 tuple 都不符合
互斥且兩兩相鄰的條件；不是只檢查四個 terminal singleton hubs。
獨立枚舉全部外部子集再次得到相同 candidate 集合。

完整 Σ 的代表索引為 {2,4,5,6,7,8,9}，共有 168 份完整有序字面框列。
artifact 保留全部有序列與各代表的延拓 witness，依同一 S₄ 置換搬運整份染色。
Q={2,3,4}，故它不在 933 的四拒絕位置軌道、也不在 941 的非連續三位置軌道。

所有非框邊均 Σ-critical；每份刪邊的完整 Σ、有序列及新增列 witness 都已保存：

| 刪除邊 | Σ(G−e) |
| --- | ---: |
| 06、25 | 1015 |
| 07、17、57、67 | 1021 |
| 15、46 | 1022 |
| 35 | 1020 |
| 36 | 1013 |
| 56 | 1023 |

所以這份停止配置滿足 T4 全收、Σ-edge-minimal、全內 degree≥4、
one-sided、短支援及相鄰雙 roots 等條件；缺少的是 **933／941 的完整 Σ 條件**。
它正是可實現圖類上的機制校準，不把有限檢查的空結果當任意大小的定理。

### 4.2 同一 ψ 的全部實際 Kempe chains

每份交換都保留原圖、實際 component 頂點、root 身份、P 接點邊、字面 ψ′、
q′、完整延拓結果及 hub 可行性。下表共 9 條，已包含所有六個色對的 components。

| 色對 | component 頂點 | frame block | 所含 roots | q′ index | q′∈Σ(1012) | 此 ψ′ 延拓 P |
| --- | --- | --- | --- | ---: | --- | --- |
| 01 | {0,1,2,3} | {0,1,2,3} | — | 0 | 否 | 否 |
| 02 | {0,4} | {0,4} | — | 6 | 是 | 是，P 色 0 |
| 02 | {2,5} | {2} | z | 6 | 是 | 是，P 色 2 |
| 03 | {0,6} | {0} | w | 7 | 是 | 否 |
| 03 | {2} | {2} | — | 7 | 是 | 否 |
| 12 | {1,3,4,5} | {1,3,4} | z | 0 | 否 | 否 |
| 13 | {1} | {1} | — | 2 | 是 | 是，P 色 1 |
| 13 | {3,6} | {3} | w | 2 | 是 | 是，P 色 3 |
| 23 | {4,5,6} | {4} | z,w | 0 | 否 | 否 |

四條可延拓交換全部碰框；沒有任何交換後能組定理 B hubs。
特別是 03／{0,6} 與 03／{2} 的目標列雖在完整 Σ 內，這份 ψ′ 仍拒絕 P：
這直接顯示有限表不能替代同一外部染色的 extension fibre。

## 5. 重播與實際驗證

checker 要求 networkx==3.5，讀取既有 cells.json 與 screen 的 SHA-256，
並記錄自身 hash；本輪沒有缺少輸入，未執行封存還原。
若新 checkout 缺檔，先依 [audits/README](../audits/README.md) 還原。
生成只以 exclusive-create 新增兩個檔案，已存在時停止，絕不覆寫。
`--check` 重新計算並逐 byte 比對完整 observations 與具名 witness。

```bash
.venv/bin/python scripts/c5_kempe_transport_table.py
.venv/bin/python scripts/c5_kempe_transport_table.py --check
PYTHONHASHSEED=17 .venv/bin/python scripts/c5_kempe_transport_table.py --check
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

上述六條命令均已實際執行，首輪輸出摘要如下；原始檢查輸出另存
[validation.json](../artifacts/c5_kempe_transport/validation.json)。

| 命令 | exit code | 實際輸出摘要 |
| --- | ---: | --- |
| 首次生成 | 0 | 新建 observations 與 `P1-witness-001.json`；933／941 各 20 筆、控制 2 圖／4 份見證 |
| 預設 `--check` | 0 | `CHECK OK`，逐 byte 比對兩個 artifact |
| `PYTHONHASHSEED=17` 的 `--check` | 0 | 同一摘要、`CHECK OK`，逐 byte 結果一致 |
| `python3 scripts/check_docs.py` | 1 | `FAIL: 4 errors`；四份新報告未被 STATUS 直接索引，沒有 missing path／anchor 診斷 |
| `python3 tools/docgraph check` | 0 | `OK: 62 documents, 213 relations, 5 families; 0 errors, 0 notes` |
| `git diff --check` | 0 | 無輸出；此 Git 命令涵蓋已追蹤檔案的 diff |

文件檢查指出的未索引檔案為本報告，以及並行任務新增的
`docs/c5_shield_calibration.md`、`docs/c5_excess_rejection_law.md`、
`docs/c5_qcore_shield_budget.md`。依本任務約定不修改 STATUS，交由發派者整合；
**文件檢查未通過**，不把此例外寫成通過。

完成正文後再次執行三項指定檢查，DocGraph 與 `git diff --check` 仍為 exit 0。
最後記錄的 `check_docs.py` 為 exit 1：`FAIL: 3 errors (544 Markdown files, 5718 local links)`；
它只列本報告、`c5_excess_rejection_law.md`、`c5_qcore_shield_budget.md` 未索引，
已不再列 `c5_shield_calibration.md`。這是並行工作區兩次檢查的實際快照，
本任務沒有修改 STATUS。

另實際執行以下兩條命令檢查本任務的未追蹤新增 source/report：

```bash
git diff --no-index --check /dev/null scripts/c5_kempe_transport_table.py
git diff --no-index --check /dev/null docs/c5_kempe_transport.md
```

兩者 exit code 都是 1（`--no-index` 比對到新增檔案差異），均無 whitespace 診斷。
最後核對 HEAD 仍為基準 `ca3870f`；其他任務的變更保留。

計算內另以直接私有點染色窮舉核對 12 份完整關係（G 與全部 11 份 G−e），
共 7,680 個完整私有點賦色；逐集合核對完整共同 S₄ 軌道，並獨立核對全部
576 組 hub candidate tuple。這些都是固定命名圖的有限證書。

## 6. 剩餘缺口與停止界線

固定 933／941 的 K 沒有成立或否定證明。本輪保存的「其他」配置已要求停止推廣；
不擴大 P，不重跑大枚舉，不續拆其他來源案例。
後續若要保留 K，至少需處理以下獨立缺口：

1. 用來源 Σ 的特定條件排除 `P1-witness-001` 所示的非交錯局部機制；
   只靠 plane disk、T4、edge-minimality、degrees、one-sided 或 roots 相鄰都不足。
2. 補上實際 roots 到 Kempe components 的 joint incidence，以及同一 ψ 的
   extension fibres，才能將框表標為真正的「a 側／b 側所需鏈」。
3. 證明一定存在有用交換；有限表只提供可用目標，不提供鏈存在性。
4. 若改用更廣的「交錯阻擋」定義，先明列其同圖 witness 與判準；
   本輪否定的只是指定 a–c₁–b–c₂ 接點二分，未宣稱完整分類所有阻擋。

本報告的有限表、交錯判定與停止控制均已具體保存；一般 disk 定理、
固定 933／941 來源排除、猜想 S、ε≥3 及 `K∞=K≤5` 都沒有由此得到。
