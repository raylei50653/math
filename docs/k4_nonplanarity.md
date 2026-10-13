# K₄ 非平面障礙偵測：實作、效果與漏判分類

2026-10-13。已完成本輪固定資料實驗；判準為既有
[K4 block 報告 §3](c5_k4_blocks.md#3-不需正常形枚舉的-k5-minor) 的一般圖版本，
不是新平面性演算法。研究入口見 [State 導覽](c5_state_guide.md)，
具體比較保存於 [固定域實驗](../audits/2026-10-13-k4-nonplanarity-45bc1c3/results.json)。
本輪不改變任何 C₅ 原來源排除、完整 Σ 或研究主命題的停止點。

**結論：K₄ 加一個同時接到四點的外部連通部分，是有效、容易核對的非平面證書。
在七點以下全部小圖中抓到 161／237 張非平面圖，沒有誤報；它不能單獨取代完整判定。**

## 1. 完整判準與紙面證明

適用有限簡單無向圖 G，無需連通、染色、degree、minimality 或 disk 假設。
Q 是四個不同原頂點，六條 Q 內邊全部存在，亦即字面 K₄。
若 G−Q 有一個連通分量 H，Q 的四點各有一條原邊接到 H，則 G 非平面。

證明：取五個 branch sets：四個 Q 頂點各自的 singleton，以及 V(H)。
五組非空、互斥且連通；前四組之間有六條原邊，第五組與前四組各有一條原邊。
收縮 H 的生成樹並刪掉其他不需要的頂點、邊，得到 K₅。使用標準事實：
平面圖取 minor 仍平面，而 K₅ 非平面。故 G 非平面。∎

外部可以任意大，四條接線不需連到同一外部頂點，也不需先猜各條長路徑。
找「連通子集」與找「連通分量」在此等價：任一符合條件的子集所屬分量也符合。
但把不同分量的接點合併計數會錯誤；K₄ 加四個獨立葉子就是平面負控制。

此判準只作拓撲證書，收縮不保持指定 boundary、染色延伸或完整 Σ。
Q 可包括框點，例如本輪 603 的命中確實使用兩個框點。

## 2. 偵測器與可核對證書

[scripts/k4_nonplanarity.py](../scripts/k4_nonplanarity.py) 只依賴 Python 標準函式庫：

1. 驗證實際頂點、邊，建立 adjacency；頂點 ID 必須為不同整數，拒絕 loops
   與未宣告端點，重複或反向重複邊合併為一條無向邊。
2. 以共同鄰居枚舉每個字面 K₄，四個頂點依 ID 遞增，各組只掃一次。
3. 在刪除這四點後，遍歷每個外部分量，檢查其接到多少個 K₄ 頂點。
4. 一旦四點都接到同一分量，保存五組原頂點、外部分量生成樹及十條原接線。
5. 獨立 checker 核對原邊、組間互斥、組內連通和十組不同的 K₅ 接線。

命中輸出 `triggered and holds`，未命中輸出 `not triggered`，後者不表示平面。
每次掃描遇第一個證書即停，不宣稱輸出所有障礙或最小證書。
checker 不呼叫平面性 oracle，且嚴格驗證證書中的整數 ID，不以布林或浮點數代替。

若 G 有 t 個字面 K₄，理想線性分量遍歷的成本為 O(t(n+m))。
目前程式為保留固定 ID 次序，反覆取 `min(remaining)` 並排序鄰居；
保守的實際分量掃描上界為 O(t(n²+m log(n+1)))，另計 K₄ 枚舉與輸入排序成本。
t 最多為 C(n,4)，因此沒有一般線性時間保證；大量孤點或 K₄ 亦會增加掃描成本。

## 3. 固定資料與效果

BASE 為 `45bc1c3dc9dacaee1b10df9d64f1c6a27bb0e954`，本輪輸入依
[BASE.json](../audits/2026-10-13-k4-nonplanarity-45bc1c3/BASE.json) 的 SHA-256
逐份保存到獨立 frozen 目錄，包含當時尚未提交的 cell-flip 實圖。
沒有重建既有 cell catalogue 或舊研究證書。

比較 oracle 為 `networkx==3.5` 的 `check_planarity`，使用 Left–Right Planarity Test；
這是有限 Python 比較，不是 Lean 定理。
[NetworkX 官方說明](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.planarity.check_planarity.html)。
Graph Atlas 是七點以下全部 1,253 個無標號簡單圖，含不連通圖與空圖。
[Atlas 官方說明](https://networkx.org/documentation/stable/reference/generated/networkx.generators.atlas.graph_atlas_g.html)。

下表只統計**原圖**，相同標號接線按既有保存記錄計數，不推稱不同同構型：

| 資料 | 圖數 | 非平面數 | 偵測數 | 漏判數 | 平面誤報 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Graph Atlas，n≤7 | 1,253 | 237 | 161（67.93%） | 76 | 0／1,016 |
| 既有 K₄ 正常形 | 289 | 289 | 289 | 0 | 無平面輸入 |
| 既有 K₄ 任意外枝控制 | 10 | 10 | 10 | 0 | 無平面輸入 |
| 既有 3903 非平面 sector 控制 | 22 | 22 | 12（54.55%） | 10 | 無平面輸入 |
| C₅ 保存代表 | 132 | 0 | 0 | 0 | 0／132 |
| 891 翻邊四態 | 4 | 1 | 1 | 0 | 0／3 |
| 具名正負控制 | 10 | 6 | 2 | 4 | 0／4 |
| K₄ 外接路徑長度／接點 sweep | 80 | 5 | 5 | 0 | 0／75 |

外接 sweep 固定一個 K₄，外部是一條長度按頂點數 1、2、4、8、16 的路徑，
對四個 K₄ 點枚舉全部 16 種接點子集；只有四點全接線的五例觸發。
289＋10 例本來就為 K₄ 障礙構造，100% 是該判準的正控制，不能視為一般召回率。
132 份 C₅ 原代表皆無字面 K₄，對「平面圖含 K₄」的校準由 Atlas 負責：
Atlas 中有 **228 張平面圖含 K₄，全部未誤報**。因此「有六條邊的四點」本身不足。

此外逐一測試有指定完整 C₅ 的 458 張資料之 boundary-apex 增廣圖，
合計 2,258 份原圖／增廣記錄及 793 份命中證書，全部逐邊重播通過。
原圖與增廣圖結果分欄，不能把 apex 的非平面性歸給原圖。

## 4. 603 的實際 K₄ 證書

[凍結的 Cell 翻邊實圖](../audits/2026-10-13-k4-nonplanarity-45bc1c3/frozen/artifacts/c5_cell_flip/891_to_987.json)
的 `both_edges`／603 圖有字面 K₄：

```text
Q = {b3, b4, v6, v8} = {3, 4, 6, 8}
H = {b0, b1, b2, v5, v7, v9} = {0, 1, 2, 5, 7, 9}
```

Q 的六條邊為 `3–4, 3–6, 3–8, 4–6, 4–8, 6–8`。
H 的生成樹為 `0–1, 0–7, 7–5, 7–9, 9–2`。
四條 Q 到 H 接線可取 `3–2, 4–0, 6–2, 8–5`，全部是同一 603 實圖的原邊。
所以把 H 收縮成第五點，直接得到 K₅；此處沒有使用外加 apex。
891、刪邊後 1019、翻邊後 987 都未觸發且參考檢查為 disk。

完整實圖及命中證書見
[603_certificate.json](../audits/2026-10-13-k4-nonplanarity-45bc1c3/examples/603_certificate.json)。

## 5. 漏判的兩種原因

Atlas 的 76 張漏判分為 64 張無字面 K₄、12 張有字面 K₄。
對這 76 張 n≤7 實圖另外執行
[misses.py](../audits/2026-10-13-k4-nonplanarity-45bc1c3/misses.py)：
遞迴枚舉所有可用邊收縮與刪頂點，以五點 complete graph 為終點。
不用刪邊，因為多出的邊不妨礙存在 K₅ minor；小於五點或不足十邊便可停止。
命中另外輸出五個一般 branch sets 並核對來源邊。這是本輪小圖的完整診斷搜尋，
沒有納入正式 K₄ 偵測器，也沒有任意大小的效能宣稱。

[分類結果](../audits/2026-10-13-k4-nonplanarity-45bc1c3/misses.json)：

- **25 張有 K₅ minor，但無字面 K₄**：是要求四個 singleton 根的限制。
- **51 張無 K₅ minor**：即使放寬 branch sets，任何只輸出 K₅ 證書的方法也抓不到。
  其中包含全部 12 張「有 K₄ 卻漏判」的圖；其餘 39 張亦無字面 K₄。

兩個值得研究的最小具名例子：

**Atlas 201：有 K₄，仍漏判。** 取 triangle `{0,1,2}`，再加入三個互不相鄰點
`{3,4,5}`，每一個都接到 triangle 全部三點。六點十二邊，包含 K₃,₃ 及三個 K₄。
但刪去任一 K₄ 後，剩兩個獨立點，每個只接到 K₄ 三點，沒有可用第五連通分量。
這圖亦無 K₅ minor：從六點到五點，刪點最多剩九邊；收縮 triangle 邊剩七邊，
收縮跨組邊剩九邊，均不足十邊。這不是漏掉某個 K₄ 的程式錯誤。

**Atlas 948：有 K₅ minor，卻沒有字面 K₄。** 將 K₅ 的兩條互不共享端點的邊
各細分一次，得到七點十二邊。任選四個原根都缺至少一條直接邊，新度數二點
也不可能參與 K₄，故本方法不觸發；收縮兩個細分段便恢復 K₅。
原 Atlas 標號的根為 `{2,3,4,5,6}`，兩條替代路徑為 `3–1–4`、`5–0–6`。

另外具名 K₃,₃ 與每條邊都細分的 K₅ 均漏判。
可能的後續是「可回原圖核對的 K₄ minor 模型」以及 K₃,₃ 障礙偵測；
本輪沒有實作這兩項，也不將完整平面性 oracle 的否定當作已有結構說明。

## 6. 速度與實際使用方式

本機 Python 3.14.7、NetworkX 3.5、WSL2，Atlas 全批重複七次，保存
[最終計時](../audits/2026-10-13-k4-nonplanarity-45bc1c3/benchmark.final.json)。
各方法都從相同 JSON 實圖建立自身資料結構；K₄ 方法包含產生及核對命中證書，
完整參考檢查不抽取 Kuratowski 反例。中位數如下：

| 方法 | 1,253 圖整批時間 |
| --- | ---: |
| K₄ 偵測器 | 23.17 ms |
| 直接完整平面性檢查 | 147.13 ms |
| 先 K₄，未觸發再完整檢查 | 153.29 ms |

K₄ 單獨約快 6.35 倍，但功能較窄。需要完整答案時，這批資料的串接總時間
比直接檢查多約 4.2%，沒有顯示加速；它的收益是容易解釋、可獨立核對的具名障礙。
這是一次小圖／單機量測，不能外推大圖效能或工程部署收益。

## 7. 重播、驗證與精確停止點

從倉庫根目錄執行。正式偵測器和證書檢查無需安裝 NetworkX：

```bash
python3 tools/audit_archive.py restore --artifacts
python3 scripts/k4_nonplanarity.py audits/2026-10-13-k4-nonplanarity-45bc1c3/examples/603_graph.json
python3 scripts/k4_nonplanarity.py --check audits/2026-10-13-k4-nonplanarity-45bc1c3/examples/603_certificate.json
python3 -m unittest tools.tests.test_k4_nonplanarity
uv run --with networkx==3.5 python audits/2026-10-13-k4-nonplanarity-45bc1c3/experiment.py --check
uv run --with networkx==3.5 python audits/2026-10-13-k4-nonplanarity-45bc1c3/misses.py --check
```

`--output PATH` 以 exclusive 建立新證書，不覆寫既有檔。
新 checkout 先用上述 restore 還原兩份大型 JSON；本地原 bytes 與 frozen hash 保持。
`--check` 只驗正證書，未觸發資料不能送入它冒充平面證明。
本輪 9 項測試涵蓋分散附件、任意連通外部、K₄-present 漏判、整圖不連通及
損壞證書（重疊、不連通、缺邊／重複接線、錯誤 ID）的拒絕。
2,258 份比較和 76 份漏判分類均由 final code 實際重播通過。

證據層：判準 soundness 是紙面 minor 論證＋標準外部拓撲事實；效果與分類是
固定域 Python 證據；沒有新 Lean theorem，也沒有完整 Σ、criticality 或任意來源排除。
舊 [K4 block](c5_k4_blocks.md) 的來源定理及其前提不受本輪改變。
所屬 State 導覽與 STATUS 新增入口；其他原來源與 HANDOFF 現況不變，傳播停在 L1。
文件導航與正式 docs DocGraph 檢查通過；全工作樹 DocGraph 因 audits／scratch
凍結副本保留相同 ID 而報 62 項 duplicate-id，包含本輪保留的來源副本，未稱全域通過。
詳細檢查紀錄見 [VERIFICATION](../audits/2026-10-13-k4-nonplanarity-45bc1c3/VERIFICATION.md)。
