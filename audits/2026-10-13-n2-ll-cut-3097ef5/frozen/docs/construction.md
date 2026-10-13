# 反例構造續篇：induced C5 仍可強迫四色

日期：2026-09-11。延續 [第一階段](phase1.md)，不使用四色定理作搜尋 oracle，不假設 boundary-state conjecture。

後續：[primitive gadget 與目標導向合成](gadgets.md)，改以排色 constraints 建立 relation library，再合成 exact T4。

## 結果與分類

找到 **11 頂點、26 邊**的 BAD 圖，指定邊界是 induced C5：

* **proved in Lean**：圖的邊資料、induced C5、BAD、exact Σ、Σ 的 120 個元素，以及兩側的 exact Σ 與 intersection。有限計算使用 `native_decide`，仍信任原生編譯及其產生的計算公理；不是純 kernel reduction。
* **computationally observed**：平面 embedding、兩側各為 disk patch、整圖 C5 不 cofacial；刪點／刪邊最小化；n≤9 的有限無反例搜尋。平面性尚未在 Lean 形式化。
* **conjectured / unresolved**：是否存在 10 頂點的 induced-C5 planar BAD；此構造的全域最小性；relevant-patch transition grammar。沒有把這些當成前提。

這推翻的是「planar + induced C5 就足以 GOOD」，**不是**「以 C5 為外邊界的 disk patch 必為 GOOD」。

## 可直接重建的圖

Boundary 為 `(0,1,2,3,4)`，先放入五環邊 `01,12,23,34,40`。再加入兩個互不相交的內部三角形：

| 內部頂點 | 相鄰的 boundary vertices |
| --- | --- |
| 5 | 2,3,4 |
| 6 | 1,2 |
| 7 | 0,1,4 |
| 8 | 1,2,3 |
| 9 | 3,4 |
| 10 | 0,4 |

另有三角形邊 `56,57,67` 與 `89,8–10,9–10`；沒有其他邊。兩個三角形及其連接分別畫在 C5 的兩側。

原始找到的是 11 頂點、27 邊的圖，比上圖多 `08`，其 Σ 有 72 個 coloring。刪除 `08` 後仍 BAD，且

\[
\Sigma_B(G)=\{c\in\operatorname{Col}_4(C_5):|\operatorname{im}(c)|=4\}.
\]

因此 exact Σ 的 S4 canonical representatives 是：

```text
01023  01203  01213  01231  01232
```

每類 24 個，共 120 個。再容許 D5 位置作用只有 `01023` 這一個個別-coloring orbit。完整 labeled Σ、240-bit mask、rotation system、faces 與 SHA-256 都在 [minimized.jsonl](../artifacts/construction/minimized.jsonl)。

## 構造的關鍵：兩側三色模式互斥

令 L 為頂點 `0..7` 的一側，R 為 boundary 加頂點 `8,9,10` 的另一側。固定同一個 boundary ordering：

| 可延伸的 S4 boundary patterns | L | R |
| --- | --- | --- |
| 三色 | `01201,01202` | `01012,01021,01212` |
| 四色 | 全部五類 | 全部五類 |

所以 L、R 各自 GOOD，三色部分卻互不相交；黏合後正好只留下全部四色部分。兩側內部沒有共用頂點，沒有跨側邊，因此符合原始 Sigma intersection 契約。

這個例子也展示：**兩個 disk patches 沿完整邊界黏合後，指定 C5 未必還是外邊界**。結果是具有 separating C5 的平面圖，不能拿它當 BAD disk patch。

## 最小化與搜尋邊界

決定性刪除流程已嘗試每個 interior vertex 與每條非 boundary 邊；26 邊版本不能再單次刪點或刪邊而保持 BAD。這是 deletion-minimal，不是全域 vertex/edge minimum。另外逐一測試保留 induced C5 的單邊 contraction，未得到更小 BAD；此項仍是計算觀察。

完整 induced-C5 edge-subset 搜尋如下。先用平面 simple graph 必要邊數上界 `m≤3n−6`；只對染色結果可能 BAD 的圖呼叫平面性檢查。

| n | 邊數上界內候選數 | planar BAD |
| --- | ---: | ---: |
| 5 | 1 | 0 |
| 6 | 32 | 0 |
| 7 | 2,047 | 0 |
| 8 | 258,096 | 0 |
| 9 | 61,450,327 | 0 |

`search_induced.py` 以完整內部 assignment 的 bit masks 計算十個 boundary patterns 的延伸性。只有空延伸集合會剪去其所有 supergraphs，因為 empty 不是 BAD。summary 保存 visited 與剪枝覆蓋數，兩者相加等於候選數。**n=10 尚未窮舉**，故目前只能說最少頂點数在計算證據下介於 10 與 11。

構造式搜尋使用固定 seed `20260911`：對 induced-C5 disk triangulations 做內部 edge flips，保留各 exact state 的一個小圖，測試 aligned intersections。實際在 8 頂點階段找到候選即停止：共 2,023 次 sample、37 張不同 labeled 圖、11 個 state、48 次不同已存 state 配對檢查。不是枚舉所有 8 頂點 disk patches，也沒有跑到參數上限 10 頂點。

## 哪些條件仍不足／已失敗

新反例不再依賴 boundary chord 或 boundary K4。26 邊圖的 boundary degrees 是 `(4,5,5,5,6)`，整圖 vertex connectivity 的計算值是 4。

但它仍不符合刪去平面最小反例中 degree-5 頂點的來源要求：

* C5 不 cofacial；補一個鄰接所有 boundary vertices 的 apex 後不 planar。
* Interior vertices `6,9,10` 的 degree 都是 4；補 boundary apex 不會增加這些 degree。
* 因而 `induced C5`、boundary degree ≥4、排除 2-cut 都不足以單獨保證 GOOD；cofacial/source 條件不能省略。

原始 27 邊圖的 interior degree 同樣有 4。沒有證明加入 interior degree ≥5 後就沒有 BAD。

## Lean 與不信任搜尋器

`Math/SplitCertificate.lean` 證明：逐邊檢查等價於 proper coloring，分開枚舉 boundary 與全部 interior assignments 等價於原本 existential Σ。它不是新的 boundary conjecture，也不信任 Python backtracking。

`ConstructedOriginal.lean` 與 `ConstructedMinimal.lean` 為閉合證書資料；Lean 重算 exact Σ，包括三色 assignment 不可延伸的否定性主張。`ConstructedAnalysis.lean` 給出 `minimal_bad`、`minimal_induced`、`minimal_sigma_exact`、`minimal_sigma_card` 及兩側 intersection。獨立 Python replay 另外直接跑全部 `4^11` 完整 assignments，兩張圖都通過；也重驗 rotation system 結構。

此外，`AlignmentCounterexample.lean` 補強原有 alignment 反例：`C5+02` 與 `C5+03` 的**整個 Σ**互為 D5 reflection；固定 context `C5+03+13` 後，前者 intersection 是 BAD、後者 GOOD。因此獨立忘掉整個 state 的 D5 alignment 也不安全，不只是不安全地壓成兩個 coloring orbit。

此次沒有定義新的 closed-SCC 規則，也不把一個 BAD state 的存在當成 closed SCC 的證據。

## 重現

```bash
uv run --with networkx==3.5 python scripts/search_induced.py
uv run --with networkx==3.5 python scripts/construct_boundary.py
uv run --with networkx==3.5 python scripts/minimize_boundary.py
python3 scripts/export_certificates.py --split --namespace FiveBoundary.ConstructedOriginal --input artifacts/construction/bad_certificates.jsonl --output Math/ConstructedOriginal.lean
python3 scripts/export_certificates.py --split --namespace FiveBoundary.ConstructedMinimal --input artifacts/construction/minimized.jsonl --output Math/ConstructedMinimal.lean
lake build
uv run --with networkx==3.5 python scripts/check_construction.py
lake env lean Math/ConstructionAudit.lean
```

驗證完成：`lake build` 通過；原始／最小化兩份證書的獨立 `4^11` replay 通過；既有 250 份證書回歸通過。固定 seed 重跑構造、最小化與 Lean exporter，產物逐 byte 一致；預設 exporter 的既有 250 份 Lean 產物保持逐 byte 不變。實際 axiom dependencies 見 [lean-audit.txt](../artifacts/construction/lean-audit.txt)。
