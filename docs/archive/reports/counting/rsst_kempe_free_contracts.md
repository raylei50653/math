# RSST 633 構形：RSST contract 規格下沒有免換色歸約

2026-10-31。執行 [4CT 導覽 §7 提議 KF](../../../research/4ct_guide.md#7-停止點與候選路線)。

**結果與停止裁決。** 633 個構形共 22,110,409 個合法 contract，**沒有一個**滿足
\(\emptyset\ne A(K/X)\subseteq A(K)\)。RSST 自己的 384 個 contract 也全部需要 Kempe 交換。
因此「以縮邊型填色規則提前處理」在 RSST 規格內一個構形都省不掉。依提議停止：
不擴大到 \(|X|>4\)、非縮邊 reducer 或 discharging。這不是新可約性結果；可約性本身已由 RSST 證明。

## 1. 定義

`K` 為 `unavoidable.conf` 中的構形，`S` 為其 free completion，環 `R=(r₁,…,r_k)` 依檔案次序。
環著色取全部 proper 四色指派在共同 \(S_4\) 作用下的等色型（不取旋轉或反射商），
與 RSST 的三邊色 code 一一對應。

- \(A(K)\)：可延伸到整個 `S` 的 proper 環著色。
- contract `X`：依 [arXiv:1401.6481](https://arxiv.org/abs/1401.6481) 附檔 `reduce.c` 的 `findangles` 規則，
  `1≤|X|≤4`、不含環邊、sparse（沒有三角面含兩條 X 邊）、`|X|=4` 時有 triad
  （某內點鄰接至少三個 X 端點，且其度數至少六或有 X 端點不與它相鄰）。
- \(A(K/X)\)：存在 `S` 的著色，其單色邊集**恰為** X，且限制在環上為該著色。這與 `checkcontract`
  的「X 邊取 0、其餘三角面和為 0」邊著色語義相同。
- **免換色**：\(A(K/X)\ne\emptyset\) 且 \(A(K/X)\subseteq A(K)\)。RSST 的 C-可約只要求
  \(A(K/X)\) 落在 D 閉包內；本條件把閉包換成 \(A(K)\) 本身，因此縮圖的任一著色都能直接回填。

## 2. 方法

[`kempe_free_contracts.cpp`](../../../../scripts/cpp/kempe_free_contracts.cpp) 對每個構形：

1. 以首次出現正規化列出環著色，逐一判定能否延伸，得 \(A(K)\)。
2. 列出全部合法 contract，建立「存活 contract 的子集計數」。
3. **一次通過擊殺。** 對每個 \(c\notin A(K)\)，在內點上允許單色邊地延伸；
   部分單色邊集若不含於任何存活 contract 就剪枝。完成的著色若單色邊集為存活 contract `D`，
   則 \(c\in A(K/D)\setminus A(K)\)，`D` 被擊殺。
4. 對倖存者，用 \(A(K)\) 內的著色找單色邊集恰為該 contract 的見證，以排除空真。

[`four_color_kempe_free_contracts.py`](../../../../scripts/four_color_kempe_free_contracts.py) 負責驗證來源 sha256、
編譯執行，並做以下獨立核對。

## 3. 核對

| 核對 | 結果 |
| --- | --- |
| \(\lvert A(K)\rvert\) 與檔案第二行的 RSST extending-colouring 數 | 633 筆逐筆相等 |
| 原 `reduce.c` 去掉 signed-matching（Kempe）迭代後，以 \(C_0\) 執行 `checkcontract` | 384 個 RSST contract 全 FAIL、249 個無 contract，與本程式逐筆一致；其內建計數檢查亦全過 |
| 不剪枝 Python 列舉（全部 ≤4 條 sparse 單色邊的著色）重算每個 contract | 環長 ≤9 的 15 個構形：合法數、免換色數、空真數逐尺寸一致 |
| 擊殺見證重播 | 384 個 RSST contract 各有一份環著色：Python 證明它不在 \(A(K)\)，且有單色邊集恰為該 contract 的延伸 |
| 輪形控制 | W₃ 最小 1、W₄ 最小 2（恰為兩組「黏對角鄰點」）、W₅、W₆ 無；C++ 與 Python 一致 |
| 重現 | 兩次執行（32／16 執行緒）`results.json` 逐位元相同 |

## 4. 結果

| 項目 | 數量 |
| --- | ---: |
| 構形（D-可約／C-可約） | 633（249／384） |
| 測試的合法 contract | 22,110,409 |
| 有免換色 contract 的構形 | **0** |
| RSST 指定 contract 為免換色 | 0／384 |
| 空真 contract | 0 |

**最接近的 contract**（環長 ≤9，不剪枝列舉；「壞著色」指 \(A(K/X)\setminus A(K)\)）：

| # | 名稱 | 環長 | \(\lvert A(K)\rvert\)／環著色 | 最少壞著色 | 其 \(\lvert X\rvert\) |
| ---: | --- | ---: | ---: | ---: | ---: |
| 1 | 0.7322（Birkhoff diamond） | 6 | 16／31 | 1 | 3 |
| 2 | 2.122 | 7 | 39／91 | 2 | 4 |
| 3 | 3.442802 | 8 | 111／274 | 3 | 4 |
| 4 | 2.126 | 8 | 81／274 | 5 | 3 |
| 5 | 0.453962 | 8 | 100／274 | 3 | 4 |
| 8 | 0.79077722 | 8 | 104／274 | 3 | 4 |
| 24 | 122.122 | 8 | 95／274 | 5 | 4 |
| 6 | 3.1306802 | 9 | 266／820 | 5 | 4 |
| 7 | 2.7566 | 9 | 211／820 | 12 | 4 |
| 12 | 0.79077962 | 9 | 257／820 | 11 | 4 |
| 25 | 122.442802 | 9 | 258／820 | 10 | 4 |
| 26 | 122.126 | 9 | 203／820 | 11 | 3 |
| 27 | 122.363 | 9 | 240／820 | 11 | 4 |
| 38 | 0.260517722 | 9 | 270／820 | 5 | 4 |
| 324 | 7322.122 | 9 | 235／820 | 10 | 4 |

壞著色從不歸零；環長越大，最少壞著色大致越多。W₅ 的最少壞著色也是 1（五環用滿四色），
與單一五度點無法免換色的紙上論證相符。

## 5. 解讀與範圍

- **結論範圍。** 在 RSST 的 contract 規格與這份不可避免集內，每個構形都至少有一種環著色
  需要回頭換色；縮邊型局部填色規則無法取代 Kempe 交換。
  這和 [線性時間演算法](https://arxiv.org/abs/2610.39753) 只用 D-可約構形、並把瓶頸放在 Kempe 交換相容。
- **沒有排除的事。** `|X|>4` 或非縮邊的 reducer、另一組不可避免集、跨多個構形攜帶的規則
  （強化歸納假設，如 Thomassen 五選色式的邊界條件），以及短分隔環的免換色黏合，均未測試。
- **證據層。** 有限計算（computationally observed），依 RSST contract 引理解讀；沒有使用 4CT，沒有新增 Lean。

**OPEN：** 是否存在任何（非 RSST 規格的）有限、免換色可約的不可避免集；
跨構形攜帶的邊界條件能否降低殘餘集。

## 證據

- 程式：[`scripts/four_color_kempe_free_contracts.py`](../../../../scripts/four_color_kempe_free_contracts.py)、
  [`scripts/cpp/kempe_free_contracts.cpp`](../../../../scripts/cpp/kempe_free_contracts.cpp)。
- 輸出：[`audits/2026-10-31-kempe-free-contracts-12e2604/`](../../../../audits/2026-10-31-kempe-free-contracts-12e2604/results.json)
  （逐構形紀錄、核對、控制、sha256）。
- 來源（不入庫，sha256 由腳本檢查）：`https://arxiv.org/src/1401.6481v1/anc/unavoidable.conf`、`…/reduce.c`。
- 重跑：`python3 -I scripts/four_color_kempe_free_contracts.py --conf unavoidable.conf --reduce-c reduce.c --out-dir <新目錄>`，約 80 秒（32 執行緒）。
