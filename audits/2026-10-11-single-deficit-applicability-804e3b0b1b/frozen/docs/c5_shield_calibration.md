# 猜想 S：可實現圖的盾弧校準

2026-10-04；分支 `shield-budget-hub-principle`，基準
`ca3870f9b79684c2100480d0dc04523899666928`。本任務校準已完成；未 commit、未 push。
依據：[四個猜想原文 §8](c5_research_synthesis.md#8-2026-10-04-新猜想基準-0b5e00a未證)、
[盾弧引理與 hub 原則](c5_unary_shield_budget.md)、[文件規則](DOCUMENTATION.md)。
目前研究入口仍由 [Kempe 導覽 §3](c5_kempe_guide.md#3-停止點與保留缺口) 維護。
本次只新增本報告、兩份 scripts 及本任務 artifacts；導覽與 STATUS 的整合交由發派者。

**結論：校準版否定，原文 S 未決。** 可實現的 T4 全收、Σ-edge-minimal induced-C₅
disk 圖中，確實有支援包含於一條框邊的 one-sided mixed 分量。
具名反例 **S935 / P0={5}** 的實際支援為 `{3,4}`，盾弧為單邊 `34`。
完整 Σ 是 mask **935**，不是 933／941。因此它否定「對所有可實現 T4 全收圖皆成立」
的推廣，**不反駁**限定完整 Σ=933／941 的原猜想 S。
原文 S 的證明不能只用這個較廣圖類共有的局部 hub linkage；必須使用
933／941 特有的拒絕列，或從它們推出的額外結構。

## 1. 圖類、輸入與證據層

B=(0,1,2,3,4) 是指定有序 induced C₅，圍住外面；其餘頂點私有。
Σ 保存全部可延拓的有序框列，只有共同 S4 色名置換用於十個代表列的編碼；
框點沒有獨立重編、D₅ quotient 或分量各自換色。T4 索引為 `{2,5,7,8,9}`，mask=932。
Q 是拒絕三色列的 singleton 位置，按輸入的 `singleton_of_three_colour` 計算。

重用 [cells.json](../artifacts/c5_cells/cells.json) 的 **21 份 T4 全收 witnesses**：
20 份 Q 非空，及一份 Σ=1023 的裸 C₅ 控制。開始讀取時未發現可重用的 E1 artifact，
故按任務允許的替代路徑自行極小化。沒有執行原目錄的大枚舉，也沒有額外隨機搜尋。
輸入 SHA-256：

```text
04650cea947a5086360e895c1a7350690f53da745314379a3328b97ee02d81b8
```

這是每個完整 Σ 類的一份封存 witness 的子圖搜尋，**不是**所有至多五個私有頂點的
Σ-edge-minimal 圖目錄，更不是任意大小的枚舉。即使原 cells 目錄涵蓋該大小的
relation classes，也不能把一份 witness 當成同類所有圖。此次無缺失輸入，未執行
[audit 還原程序](../audits/README.md#新-checkout-的還原)。

| 證據層 | 本次內容與界線 |
| --- | --- |
| 紙面有限構造 | §3 明列單張反例的邊、內面、分量及拒絕見證；不新增任意大小定理 |
| 外部定理 | 未新增外部 degree-list／Gallai 依賴；只沿用原 hub 原則解釋證明缺口，未重驗其外部證明 |
| Python 有限域證書 | 21 張圖、每條非框邊、全部 240 個合法字面框列、具名嵌入與面盾弧；networkx 3.5 的平面嵌入是計算依賴 |
| Lean 普通證明／native_decide | 都沒有新增；未執行 `lake build`，不宣稱本構造已 Lean 化 |

沒有把四色定理當搜尋 oracle。可延拓性全部由四個顏色的精確有限搜尋決定。

## 2. Checker 與完整統計

[主 checker](../scripts/c5_shield_calibration.py) 對每份 witness 做 40 個決定性刪邊次序：
第一個採排序，其餘使用 `20261004 + mask*40 + trial` 作種子洗牌。
僅在刪除後**完整 Σ 相同**時刪邊。所有 840 次都沒有刪掉任何邊；
原 witnesses 已經 Σ-edge-minimal。裸 C₅ 的 criticality 是空邊集上的條件。
沒有刪去私有頂點，原 vertex labels 全保留。

每張 final 圖與其每份單邊刪除圖都用兩條有限路徑核對：
確定性的 backtracking，以及對十個代表列直接遍歷 `4^k` 私有指派。
另外逐一搜尋全部 **240 個合法字面框列**，核對共同 S4 normalization。
21 張 final 圖加上 220 份單邊刪除圖，合計 57,840 個字面框列測試。
保存可接受代表的完整染色與刪邊新接受列的完整染色。

[面 helper](../scripts/c5_shield_calibration_faces.py) 使用 apex-wheel 平面嵌入，
保存完整 clockwise rotation、全部 facial walks 與指定外面 `01234`。
對 one-sided P，按原嵌入刪去 K_P 之外的邊，合併原面；
H−P 所在的合併內面就是 F_P，框邊不在其邊界上者才是 σ_P。
不以「任選支援 gap」代替面定義。helper 要求 G 連通；本測試集全部符合。

| 統計 | 數量 |
| --- | ---: |
| T4 全收 witness / Q 非空 witness | 21 / 20 |
| 刪邊次序 / distinct labelled final 圖 | 840 / 21 |
| 刪掉至少一條邊的次序 | 0 |
| 私有頂點範圍 | 0–5 |
| 具名非框 critical 邊 | 220 |
| pieces 總數 | 25 |
| unary / one-sided unary | 15 / 15 |
| 至少兩個 root 的 mixed / one-sided mixed | 5 / 5 |
| 零 root 的整份 H piece | 5 |
| 短支援 one-sided mixed | **5** |
| unary 盾弧長 2 / mixed 盾弧長 1 | 15 / 5 |
| 具有 0 / 1 / 2 份 unary 的圖 | 11 / 5 / 5 |

依題目「一個 root 為 unary，否則 mixed」的字面規則，零 root 的五份 piece
也記 `kind=mixed`，另外以 `rootless=true` 標記；H−P 為空，所以**不是** one-sided。
它們屬 masks 959、1007、1015、1021、1022。Σ=1023 的控制沒有 piece。

| 順帶檢查的性質 | 適用份數 | 違反 |
| --- | ---: | ---: |
| unary 的盾弧長 ≥2 | 15 pieces | 0 |
| one-sided 支援連續 | 20 pieces | 0 |
| 引理 2 的支援恰等於盾弧頂點集 | 20 pieces | 0 |
| 引理 1(a) 的盾弧連續 | 20 pieces | 0 |
| 引理 1(c) 的其餘內部附件避開盾弧內點 | 20 pieces | 0 |
| 引理 1(d) 的盾弧邊互斥 | 5 unordered piece pairs | 0 |
| 全圖至多兩份 unary | 21 graphs | 0 |

20 張非空內部圖的 H 都連通、碰齊五框點；引理 2 的 20 份檢查都滿足這兩個
拓撲前提且支援至少兩點。這些數字只支持本測試集，沒有提升為較廣圖類的定理。

以下列出**全部** pieces。記法 `頂點 : U/M/0 ; 實際支援 ; 盾邊`；
U=unary、M=至少兩個 root 的 mixed、0=零 root mixed。
U/M 在此全部 one-sided；0 的盾弧記不適用。`04` 是框邊 `{0,4}`。

| 圖 ID | ε | roots | 全部分量與實際支援、盾弧 |
| --- | ---: | --- | --- |
| S935 | 2 | 6,7 | 5 : M ; 34 ; 34 |
| S942 | 2 | 5,7 | 6 : M ; 23 ; 23 |
| S943 | 1 | 7 | 56 : U ; 234 ; 23,34 |
| S951 | 2 | 5 | 69 : U ; 014 ; 01,04；78 : U ; 123 ; 12,23 |
| S956 | 2 | 5,6 | 7 : M ; 12 ; 12 |
| S957 | 2 | 5 | 69 : U ; 014 ; 01,04；78 : U ; 234 ; 23,34 |
| S958 | 1 | 5 | 67 : U ; 123 ; 12,23 |
| S959 | 0 | 無 | 56 : 0 ; 01234 ; 不適用 |
| S997 | 2 | 5,7 | 6 : M ; 04 ; 04 |
| S999 | 1 | 7 | 56 : U ; 034 ; 04,34 |
| S1005 | 2 | 5 | 69 : U ; 012 ; 01,12；78 : U ; 234 ; 23,34 |
| S1006 | 2 | 5 | 69 : U ; 012 ; 01,12；78 : U ; 034 ; 04,34 |
| S1007 | 0 | 無 | 56 : 0 ; 01234 ; 不適用 |
| S1012 | 2 | 5,6 | 7 : M ; 01 ; 01 |
| S1013 | 1 | 6 | 57 : U ; 014 ; 01,04 |
| S1014 | 2 | 5 | 69 : U ; 123 ; 12,23；78 : U ; 034 ; 04,34 |
| S1015 | 0 | 無 | 56 : 0 ; 01234 ; 不適用 |
| S1020 | 1 | 5 | 67 : U ; 012 ; 01,12 |
| S1021 | 0 | 無 | 56 : 0 ; 01234 ; 不適用 |
| S1022 | 0 | 無 | 56 : 0 ; 01234 ; 不適用 |
| S1023 | 0 | 無 | 無 |

完整資料：[observations.json](../artifacts/c5_shield_calibration/observations.json)。
其中每張圖保存完整 Σ 的 accepted/rejected ordered rows、所有原附件、degree、roots、
pieces、one-sided 判斷、嵌入環序、F_P 面邊界、盾弧與每條非框邊的新增列。
840 份 trial 保存刪邊次序、各步 Σ 及 final graph ID。

## 3. 具名反例 S935 / P0

獨立入口：[counterexample_S935.json](../artifacts/c5_shield_calibration/counterexample_S935.json)，
包含整圖、完整 Σ、逐邊 critical 證書、原面嵌入，以及全部拒絕代表列上
G−P 的合法染色（若有）。

頂點為 0,…,7，框是 `01234`。非框邊為：

```text
06 16 17 27 35 37 45 46 56 57 67
```

可實現 disk 的九個內面為以下三角面；循環方向見 artifact 的 rotation：

```text
046 061 167 172 273 354 375 456 576
```

加上外面 `01234`，V=8、E=16、F=10，Euler 值為 2。
各邊恰在兩個 facial darts 出現，框面為指定有序 C₅；這給出具名平面 disk 嵌入。
內點 degree 為 `(deg 5,deg 6,deg 7)=(4,5,5)`，故 ε=2、R={6,7}。
H 為三角形 `567`。P0={5} 同時接 6、7，是 mixed；H−P 是非空連通邊 `67`。

K_P 是框加邊 `35,45`。H−P 在 K_P 的內面 F_P 中，其邊界 walk 為
`0,4,5,3,2,1`。框邊 `34` 不在該面邊界上，其餘四條框邊都在，因而

```text
S_P={3,4},  σ_P={{3,4}},  |σ_P|=1.
```

完整 Σ 的十個代表列判定如下；S4 展開後接受 168 個、拒絕 72 個有序合法框列。
沒有只保存三色 profile 或某一列的結果。

| pattern index | ordered pattern | 是否延拓 |
| --- | --- | --- |
| 0 | 01012 | 是 |
| 1 | 01021 | 是 |
| 2 | 01023 | 是（T4） |
| 3 | 01201 | 否 |
| 4 | 01202 | 否 |
| 5 | 01203 | 是（T4） |
| 6 | 01212 | 否 |
| 7 | 01213 | 是（T4） |
| 8 | 01231 | 是（T4） |
| 9 | 01232 | 是（T4） |

所以 Σ=935，Q={0,1,2}、c(Q)=1、e(Q)=2。此例與猜想 E 的 ε≥2 下界相容，
本任務不判斷 E、K 或 W。

| 刪除邊 | 新完整 Σ mask | 新增 pattern indices |
| --- | ---: | --- |
| 06 | 959 | 3,4 |
| 16 | 999 | 6 |
| 17 | 943 | 3 |
| 27 | 1015 | 4,6 |
| 35 | 1007 | 3,6 |
| 37 | 959 | 3,4 |
| 45 | 1007 | 3,6 |
| 46 | 1015 | 4,6 |
| 56 | 1007 | 3,6 |
| 57 | 1007 | 3,6 |
| 67 | 1023 | 3,4,6 |

每條非框邊刪除都擴大完整 Σ，證明這張具名圖的 Σ-edge-minimality。
其餘四個短支援例子是 S942/P0、S956/P0、S997/P0、S1012/P0，
其具名邊、完整 Σ 與 face 證書均保存在 observations；不把旋轉後的圖重新共同正規化來合併記錄。

## 4. 對 hub linkage 證明的含義

在拒絕列 q=`01201`，G−{5} 有染色

```text
vertex: 0 1 2 3 4 6 7
colour: 0 1 2 0 1 2 3
```

P 的四個鄰點 `(3,4,6,7)` 用齊四色，所以無法給頂點 5 著色。
兩個相鄰 roots 分別是色 2、3，正好落在原推論 B2 沒有排除的情況。
四個直接外鄰 singleton hubs 只有環 `3−4−6−7−3`，欠 `36`、`47`；
不能直接套用四個 pairwise-adjacent hubs 的假設。
這不是只檢查 singleton hubs 就宣稱所有 branch sets 不存在：若真能找到符合定理 B 的
任意 connected hubs，定理 B 會與此實際平面拒絕見證矛盾。

artifact 逐一列出拒絕代表列上所有 G−P 染色：indices 3、6 各一份，roots 都異色；
index 4 沒有 G−P 染色，本來就不是 P 的拒絕見證。沒有把不存在的 witness 用來推論 roots 顏色。
因此一般的可實現圖中，短 mixed 確實能存活；原文 S 需要完整來源的額外拒絕約束。
如何由 933／941 的拒絕列排除它們，仍是原導覽的 hub／Kempe 缺口。

## 5. 實際重播與交接

本輪執行命令（生成只寫新目錄；再次生成會拒絕覆寫，`--check` 不寫檔）：

```bash
.venv/bin/python scripts/c5_shield_calibration.py
.venv/bin/python scripts/c5_shield_calibration.py --check
PYTHONHASHSEED=17 .venv/bin/python scripts/c5_shield_calibration.py --check
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

| 實際執行 | exit / 輸出摘要 |
| --- | --- |
| 生成、一般 `--check`、`PYTHONHASHSEED=17 --check` | 三次都是 exit 0；輸出相同 summary，21 圖、840 次序、220 critical 邊、25 pieces、5 短 mixed、`property_failures=[]`；兩次 check 均逐 byte 核對兩份 artifact |
| `python3 scripts/check_docs.py` | **exit 1**：`not directly indexed by STATUS: docs/c5_shield_calibration.md`；`FAIL: 1 errors (541 Markdown files, 5680 local links)` |
| `python3 tools/docgraph check` | exit 0：`OK: 62 documents, 213 relations, 5 families; 0 errors, 0 notes` |
| `git diff --check` | exit 0，無輸出 |

文件檢查的唯一錯誤是本報告尚未被 STATUS 直接索引；按本任務約定，留給發派者整合，
沒有把檢查記成通過。其他任務仍在共用工作樹進行，以上是本次實際檢查的截點數字。
另外對三份新增文字檔各執行 `git diff --no-index --check /dev/null <path>`，
皆無 whitespace 診斷；此模式因檔案新增而回傳 exit 1，不冒稱 exit 0。
沒有重跑舊的大枚舉或原盾弧 checker 的 6,091,827 份 hub wirings；
沒有新增 Lean 工作，也沒有覆寫原 artifacts。

剩餘缺口：原文固定完整 Σ=933／941 的 S 未決；較大可實現代表的統計未搜尋；
本 corpus 未出現 separating mixed、空或單點支援 one-sided mixed。
這些缺口不影響已具體否定的校準版。發派者仍須把此報告加入 STATUS，並整合導覽；
本任務不修改那些檔案。
