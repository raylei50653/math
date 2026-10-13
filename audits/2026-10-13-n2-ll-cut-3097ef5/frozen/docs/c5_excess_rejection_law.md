# E1：超額–拒絕定律的有限證據與反例搜尋

2026-10-04，分支 `shield-budget-hub-principle`，基準
`ca3870f9b79684c2100480d0dc04523899666928`。來源是
[綜合報告 §8.1](c5_research_synthesis.md#81-猜想-e超額拒絕定律) 的猜想 E；
已讀取[盾弧預算與 hub 原則](c5_unary_shield_budget.md)及
[文件與證據規則](DOCUMENTATION.md)。研究線目前入口仍見
[Kempe 導覽 §3](c5_kempe_guide.md#3-停止點與保留缺口)。
本任務已完成；依發派約定只新增本報告、checker 與 artifact，索引整合由發派者負責。

**結論：猜想 E 在任意大小仍未決。** 在使用者確認的「排除孤立內點」約定下，
完整窮舉有效內點數 **k≤5** 的指定有序 induced-C₅ disk、T4 全收、
每條非框邊 Σ-critical、1≤|Q|≤4 的圖，得到 **310 個私有頂點重標號類**，
全部滿足 ε≥2|Q|−e(Q)−2，沒有反例。這是 Python 有限域證據。
此外已正式重現 20 個目錄 witness、每份 40 次隨機刪邊的 scratch 檢查；
其最小 ε 全部等於猜想下界，但這些 witness 原本就已 Σ-edge-minimal。

## 1. 前提、記號與證據層

G 是有限簡單圖，B=(0,1,2,3,4) 為指定有序 induced C₅，圍住 disk 外面；
其餘頂點私有。框邊隱含於來源 witness，本 checker 會補回全部五條。
Σ 是完整可延拓的有序 boundary 列，僅按共同 S4 色名置換取軌道；
不按 D₅ 合併框點位置，不獨立重命名各分量的色框。

- T4 的 pattern 索引為 `{2,5,7,8,9}`，mask 為 932。
- 三色索引至 singleton 位置為 `{0:4,1:3,3:2,4:1,6:0}`。
- Q 是被拒絕的三色 singleton 位置；對 1≤|Q|≤4，c(Q)=|Q|−e(Q)，
  所以猜想式為 ε≥|Q|+c(Q)−2=2|Q|−e(Q)−2。
- 本次使用者明確確認沿用[容量報告 §1](c5_independent_support_capacity.md#1-兩種-minimality-與來源的基本結構)
  的有效內點約定：**排除孤立內點**，k 與 ε 都只計剩餘內點。
  若計入孤立內點，加一個孤立點就使 ε 減 4，而 Σ 與 criticality 不變；
  此版本不是本輪所搜尋的命題。

| 證據層 | 本輪內容與界線 |
| --- | --- |
| 紙面證明 | §3 的必要度數、spoke 數及邊數界；私有重標號覆蓋與 disk 檢查的理由。沒有任意大小的 E 證明 |
| 外部定理 | 未以四色定理、degree-list 或 Gallai 作 oracle；平面邊數界是下述 Euler 計數。盾弧／hub 報告的任意大小定理沒有直接用來判定 E |
| Python 有限域證書 | 20×40 scratch；全部 k≤5 搜尋；逐邊 criticality、完整 Σ 與代表圖的獨立回溯／NetworkX 嵌入證書；§5 重播 |
| Lean 普通證明 | 沒有新增 theorem；未執行 `lake build` |
| Lean `native_decide` | 沒有新增證書 |

實際環境為 `.venv/bin/python`、NetworkX 3.5、rustworkx 0.17.1。
窮舉的快速 planarity 決策使用 rustworkx；保存的代表圖全部另經 NetworkX
及回溯著色檢查。沒有 rustworkx 時 checker 會改用 NetworkX；結果結構不含耗時或後端選擇。

## 2. 封存 witness 的 scratch 重現

讀取 [cells.json](../artifacts/c5_cells/cells.json) 的全部 132 個 key，選出
T4 全收且 Q 非空的 20 份。輸入 SHA-256 為
`04650cea947a5086360e895c1a7350690f53da745314379a3328b97ee02d81b8`。
未重跑原 `c5_cell_enumerator.py` 的目錄枚舉；沒有覆寫來源 artifact。

每份 witness 用 MRV 回溯計算十個完整 boundary patterns 的可延拓性。
第 t 次刪邊次序使用 `Random(17+t)`，t=0,…,39；先將具名非框邊排序，
再 shuffle，每次只刪除使完整 Σ 不變的邊。最後按有效內點計算 ε 與度數。
一次順序已足以得到 Σ-edge-minimal 子圖：測試時 critical 的邊，在其後的
Σ-preserving 刪邊中仍有原新列的延拓，而圖本身的 Σ 維持不變。
最後仍逐邊獨立驗證 minimality。

| Q 形狀 | 全部具名 mask | 下界 | scratch 最小 ε | 內點度數 |
| --- | --- | ---: | ---: | --- |
| 一點 | 959、1007、1015、1021、1022 | 0 | 0 | (4,4) |
| 相鄰兩點 | 943、958、999、1013、1020 | 1 | 1 | (4,4,5) |
| 不相鄰兩點 | 951、957、1005、1006、1014 | 2 | 2 | (4,4,4,4,6) |
| 三點弧 | 935、942、956、997、1012 | 2 | 2 | (4,5,5) |

所有 800 次結果均保留原 witness 的邊集，每份只有一種 outcome。
因此隨機次序只提供可重播控制，沒有增加候選多樣性。這部分本身只證明
固定 witness 子圖中達到這些 ε，不能作任意大小最小值的下界。
下一節的完整小 k 搜尋才提供相應有限圖類的下界。

## 3. 搜尋規模與完整覆蓋

### 3.1 搜尋前的規模估計

induced C₅ 已固定，所以可選邊只有 5k 條 spokes 與 k(k−1)/2 條內邊。
原始子集合數為 2^(5k+k(k−1)/2)。直接遍歷 k=5 的 343 億份子集合不適合本任務。
下列必要條件將它減至約 2,334 萬份接法；初步 k≤4 執行只需約 1.2 秒，
因此本輪完成 k=5，不需退回 near-triangulation 刪邊子圖的受限域。

| k | 原始 induced 邊集數 | 內部模板數 | degree／spoke／邊數界後接法 | T4 通過葉數 | 合格私有重標號類 |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 32 | 0 | 0 | 0 | 0 |
| 2 | 2,048 | 1 | 100 | 60 | 5 |
| 3 | 262,144 | 2 | 9,000 | 5,430 | 35 |
| 4 | 67,108,864 | 7 | 515,625 | 308,035 | 35 |
| 5 | 34,359,738,368 | 23 | 23,342,626 | 16,466,995 | 235 |

「接法」已選一個私有重標號下的 H 模板，仍保留其所有具名框點接線；
不是完全 labelled 圖數。合格類只合併私有頂點置換，**五個框點始終逐點固定**。
不按平面嵌入數重複計數。k=0 只有 C₅，Σ 全收、Q 空，所以不在命題範圍。

### 3.2 三個必要條件

**有效內點 degree≥4。** 若有效內點 v 的 degree≤3，任取 incident 邊 e。
一份 G−e 的 boundary 延拓捨去 v 後，仍可選一個避開其至多三個原鄰色的顏色補回 v。
因此 Σ(G−e)=Σ(G)，與 e critical 矛盾。這個論證不使用四色定理。

**每個內點至多三條 spokes。** 若內點接到四個框點，令 t 是第五個框點。
將 t 與一個不相鄰框點取同色、其餘三點各取不同色，得到一個 T4 pattern，
而那四個鄰框點恰用滿四色，所以無法延拓到該內點。T4 全收排除此情形。
因此 deg_H(v)≥1，spoke 數 s_v 滿足 max(0,4−deg_H(v))≤s_v≤3。

**非框邊至多 3k+2。** disk 外添加一個連到全部五個框點的新 apex，得到
k+6 點的簡單平面圖。Euler 面計數給 |E_aug|≤3(k+6)−6。
其中原框邊五條、新 apex 邊五條，所以非框邊數≤3k+2。

以上全部是任何合格圖的必要條件，沒有額外假設 H 連通、near-triangulation、
root 數、root 相鄰性、degree 序列或特定 Σ。

### 3.3 枚舉、著色、criticality 與 disk

1. 枚舉 H 的全部 2^(k(k−1)/2) 個 labelled 邊集；比較全部 k! 個私有置換，
   只保留最小編碼模板。模板完整性由這段直接有限枚舉給出，不依賴 graph atlas。
2. 對每個模板，枚舉上述區間內的全部框支援子集，檢查總邊數界。
   用 suffix 計數精確記錄每個 T4 剪枝節點覆蓋的有界接法；
   `T4_attachment_leaves + T4_pruned_bounded_completions` 必須等於接法總數。
3. 對每個 pattern 保存全部 4^k 個共同內點賦色的 bitset，按所有原邊的
   不等色約束作交集。這是 simultaneous assignments，不是分量 marginals。
   一個 T4 bitset 空了，其所有附件超圖都無法恢復，故可安全剪枝。
4. Σ 全收者 Q 空；|Q|=5 者不在 E 的前提。其餘列逐一檢查。
   在 H 的完整 automorphism group 下合併重複接法，仍固定具名框點。
5. 對每條非框邊，用原邊約束的 prefix／suffix 交集檢查刪除此邊是否讓
   某個原拒絕三色列獲得延拓。T4 原本已全收，所以這覆蓋所有新接受列。
   全部邊 critical 才進入 disk 檢查。
6. 用新增 boundary apex 的圖測平面性。對此時的有效 critical 圖，它等價於
   存在指定 C₅ 外面的 disk 嵌入：限制任一增廣平面嵌入到 wheel C₅+apex，
   每個 H 分量落在某一 wheel 面中。apex 側的面都是三角形，只能碰一對相鄰框點。
   這類分量的一份 T4 著色，可按同一 S4 置換搬到任何合法框列，因為相鄰框點
   的色型永遠異色；其所有邊遂都非 critical。故合格圖的所有有效分量只能落在
   C₅ 另一側。刪 apex 後，C₅ 正是面邊界。保存的 NetworkX rotation 與外面 walk
   另外逐份驗證此事；不是只測原圖普通 planarity。
7. 對每個合格圖計算 ε 與具名 Q 下界。若 ε 低於下界，立即停止並保存完整
   邊集、Σ、度數、嵌入與所有 critical 見證。本輪未觸發此停止條件。

這是全域 **k≤5 有效圖類** 的完整枚舉，並非「沒找到反例的隨機抽樣」。
此有限覆蓋不提供 k≥6 的結論。

## 4. 觀察到的最小 ε 與證書入口

| Q 形狀 | 下界 | k≤5 最小 ε | 最早 k | 合格類總數 | 具名代表 |
| --- | ---: | ---: | ---: | ---: | --- |
| 一點 | 0 | 0 | 2 | 215 | Σ=959，(4,4) |
| 相鄰兩點 | 1 | 1 | 3 | 60 | Σ=943，(4,4,5) |
| 不相鄰兩點 | 2 | 2 | 5 | 10 | Σ=951，(4,4,4,4,6) |
| 三點弧 | 2 | 2 | 3 | 25 | Σ=935，(4,5,5) |
| 兩點弧＋孤點 | 3 | 無合格圖 | — | 0 | 包含 Σ=941；沒有 witness |
| 四點弧 | 3 | 無合格圖 | — | 0 | 包含 Σ=933；沒有 witness |

「無合格圖」沒有定義該形狀任意大小的最小 ε，尤其沒有證明 933／941
需 ε≥3。這兩個 mask 的 k≤5 空域不能代替 ε=2、任意大小的來源排除。

[Checker](../scripts/c5_excess_rejection_law.py) 與
[observations.json](../artifacts/c5_excess_rejection_law/observations.json) 是本輪具名證書入口。
JSON 中保存所有 pattern 的固定順序、singleton 映射、來源 SHA、完整配置，
以及各 k 的模板、覆蓋計數、逐 mask 圖數、ε histogram、合格圖 stream SHA-256。
stream hash 是完整搜尋輸出的摘要，**不是保存了全部 310 張圖的邊集**。
邊集與逐邊見證保存於各 k、各 Σ 的最小 ε 代表及全部 scratch 代表。
合計保存 70 份圖證書（50 份分層最小代表及 20 份 scratch 代表，允許相同圖重複）。
artifact 大小 1,125,356 bytes，SHA-256 為
`23a92b56f325bd4bd496d7e8dfb14714d8481618253f88243df4cb7916ca999e`。

代表圖的精確 JSON pointers：

- 一點：`/exhaustive/1/minima_by_sigma/959`。
- 相鄰兩點：`/exhaustive/2/minima_by_sigma/943`。
- 不相鄰兩點：`/exhaustive/4/minima_by_sigma/951`。
- 三點弧：`/exhaustive/2/minima_by_sigma/935`。

每份圖記錄完整 vertices、原具名 nonframe edges、補回的 frame edges、
完整 Σ 的有序 S4 代表列、各接受列的一份完整染色、所有 degree、ε、Q、
c/e、disk rotation 和 C₅ 外面。每條原非框邊保存刪邊後完整 Σ、
全部新接受 pattern 索引，以及一份該新列的完整染色；被刪邊的兩端同色，
其餘全部原邊異色。各 witness 始終使用一個字面色框。

## 5. 重播與實際驗證

建立 artifact 的實際命令：

```bash
.venv/bin/python scripts/c5_excess_rejection_law.py --max-k 4 --output /tmp/c5-e1-k4-20261004.json
.venv/bin/python scripts/c5_excess_rejection_law.py --max-k 5 --output /tmp/c5-e1-k5-20261004.json
.venv/bin/python scripts/c5_excess_rejection_law.py --max-k 5
```

前三個搜尋均未找到反例。初次 k≤4 耗時約 1.2 秒，初次 k≤5 約 47.4 秒；
使用 shell `time` 觀測，耗時不寫入 artifact。前導嘗試 `/usr/bin/time` 因該執行檔
不存在而 exit 127，沒有執行 checker；改用 shell `time` 後才得到上述結果。
最終 generator 以 exclusive create 寫入本輪新 artifact；如果輸出已存在就拒絕覆寫。
若要重新生成，使用新的 `--output` 路徑。

封存後正式執行：

```bash
.venv/bin/python scripts/c5_excess_rejection_law.py --check
PYTHONHASHSEED=17 .venv/bin/python scripts/c5_excess_rejection_law.py --check
.venv/bin/python scripts/c5_excess_rejection_law.py --audit-k3
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

| 命令／檢查 | 實際輸出摘要 |
| --- | --- |
| `--check` | exit 0；`CHECK OK: exact artifact replay; NetworkX/backtracking witnesses verified`；20 類 scratch、310 個合格類全重算，約 51.9 秒 |
| `PYTHONHASHSEED=17 ... --check` | exit 0；相同 `CHECK OK`，整份 JSON 精確相等，約 51.6 秒；實際 shell 呼叫使用 `env PYTHONHASHSEED=17` |
| `--audit-k3` | exit 0；`RAW K3 AUDIT OK`；262,144 原始邊集 → 19,000 degree／邊數界候選 → 435 labelled critical 圖 → 210 labelled disk 圖 → 35 私有重標號類；約 3.4 秒 |
| `python3 scripts/check_docs.py` | 最新 exit 1；3 個 `not directly indexed by STATUS`，544 Markdown files、5,718 local links；首次為 4 項，詳見下段 |
| `python3 tools/docgraph check` | exit 0；`OK: 62 documents, 213 relations, 5 families; 0 errors, 0 notes` |
| `git diff --check` | exit 0；無輸出 |

`--audit-k3` 不使用 H 模板、spoke 上限剪枝、T4 前綴剪枝或 producer 的
prefix／suffix criticality 演算法：直接遍歷全部原始邊集，對全部 19,000 份
必要度數／邊數界內候選，以 MRV 回溯核對完整 Σ，再直接刪每條邊重算。
disk 決策用 NetworkX，最後用全部私有置換合併圖；逐 Σ 圖數與 ε histogram
精確等於 producer。這是不同搜尋方式的 k=3 交叉控制，不是 k≥6 證據。

最新文件檢查的三項是 `docs/c5_excess_rejection_law.md`、
`docs/c5_kempe_transport.md`、`docs/c5_qcore_shield_budget.md`。
首次另有 `docs/c5_shield_calibration.md`；其索引在並行任務整合後已補上。
另外兩份未索引報告也屬並行任務。
本輪沒有修改 STATUS 或檢查器來消除索引缺口；依發派約定留待整合。
其餘檢查沒有報出缺失連結或錨點。

另已執行種子 1741 的 600 張 k=1..3 隨機圖交叉控制：assignment bitset 的 Σ
與獨立 MRV 回溯全相同，適用圖的 prefix／suffix criticality 與直接刪邊相同。
另將快速後端停用，以 NetworkX-only 執行 `search_level(3)`，所得完整結果精確
等於 rustworkx 版本。這些控制不擴大 E 的 k≤5 結論。

## 6. 停止點與剩餘缺口

本輪 E1 的完成條件已達到：scratch 已具名封存，全部 k≤5 有效圖類已檢查，
每種 Q 形狀的有限最小值／空域均明列，checker 可從封存配置重播。
任意大小 E、k≥6 的反例搜尋及其理論下界仍未解；沒有推進或代證猜想 S／K／W。
使用者指定的禁改導覽、STATUS、README、HANDOFF 約定保持，未 commit、未 push。
跨任務的整合與現行研究排程仍由發派者及 Kempe 導覽負責。
