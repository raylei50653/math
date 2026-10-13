# 三色 support 控制的獨立核對

2026-10-13。結果為 `triggered and holds`；完整機讀結果見
[independent_summary.json](independent_summary.json)。重播：

```bash
python3 -B audits/2026-10-13-w5-three-color-support-19209f4c/review/independent_check.py
```

## 獨立性與核對邊界

[independent_check.py](independent_check.py) 只用 Python 標準函式庫，不 import 或執行
主程式、前輪程式或 supplementary 程式。prism、32 個固定 diagonal mask 與
decorated prism 都從數學邊／面規格重新構造；H、G 各自以所有自由頂點的色彩
Cartesian product 直接篩邊，沒有沿用主程式的 DFS。完成枚舉後才讀證書作比較。

對每個圖，核對原 B/U/center labels、完整頂點向量順序、所有原邊、具名 B/U 面、
旋轉、每一個 H fibre（含空格）、每份完整 G lift、R3、all-colour support、Sigma(H)
及 Sigma(G)。另與凍結前輪證書比較 H/G 全資料，確認 34 圖的原控制域未改。
本輪沒有重新獨立枚舉前輪的 170 個商圖；主程式保留的商圖／chord 證據仍屬前輪範圍。

幾何核對採 face permutation 與 dart reversal 合成的頂點旋轉：每個有向邊恰出現一次、
每個具名頂點恰有一個旋轉 orbit、圖連通且 Euler characteristic = 2。
同時固定外 B 面、空 U 面，以及補中心後的五個三角面。這給出構造控制圖的 plane
disk／annulus 槽位證據，沒有將各圖的色框或接口獨立重命名。

除另行標示 literal rows 外，下列 cells／support／lifts 計數均使用十個 canonical
beta 列及每列 1,024 個 literal tau。

## 原 34 圖的有限結果

| 核對量 | 結果 |
|---|---:|
| H/G 嵌入 | 68 |
| canonical beta / literal tau | 10 / 1,024 |
| 完整 cells / 空 cells | 348,160 / 345,580 |
| 完整 H / G lifts | 3,250 / 1,620 |
| 非空三色 support cells | 1,280 |
| 不同圖的 unordered pairs | 561 |
| 相同 R3 的 pairs | 1 |
| 雙向 selector 的完整 G 輸入 | 1,020 |

每一列都由直接 G 枚舉確認 `Sigma(G)(beta) iff exists tau in R3(beta)`；並逐份確認
將三色 H lift 加上唯一缺色，恰為完整 G lifts。561 pairs 中只有 prism／decorated
prism 觸發 R3 相等；其餘 560 pairs 是 `not triggered`，不是普遍定理的排除證據。

對唯一觸發 pair 的兩個方向，重新計算「目標同格最小 H lift + 原中心色」selector，
與證書逐項相比。每一輸入均落入直接枚舉的目標 G 集合，並保持全部 B/U labels
及中心的 literal 顏色。這些 maps 不主張互為逆映射：裝飾圖每個非空 fibre 的
完整 lifts 恰為 prism 的兩倍。

色框另核對全部 24 個共同 S4 permutations，覆蓋全部 240 個 proper literal beta，
共 78,000 份 H lifts 與 38,880 份 G lifts。對 prism 與 triangulated_01 再直接枚舉
全部 240 beta，合計 480 個 literal rows；結果與共同換色所得 H/G 完整集合相等。
沒有只保存獨立正規化的 U 形狀。

## 七項負控制

以下均由重新構造的原邊、完整格與完整 lifts 核對，狀態為 `counterexample`；
證書內的具體 witnesses 也有核對，並非只確認抽象計數。

1. **Sigma(H) 投影損失**：prism 與 triangulated_01 的 Sigma(H) 相同；补中心後
   beta indices 6、7 的 Sigma(G) 不同。
2. **Sigma(G) 不決定 R3**：prism 與 triangulated_00 的 Sigma(G) 相同，但 R3
   大小分別為 340、20。
3. **support 不決定 full lifts**：prism 與 decorated prism 有相同 R3 及 all-colour
   support，而每個非空 H fibre 的 multiplicity 為 1:2。
4. **獨立正規化 U**：beta=01012、tau=10103 是合法三色格；只把 U 改成 01012
   得空格，同時破壞五條原 spoke edges `(bi,ui)`。
5. **單一等式不足接中心**：beta=01012、tau=10123 是合法 H lift，滿足 u0=u2，
   但 U 用四種色，沒有中心色可選。
6. **混合等式 witnesses**：triangulated_01 在 beta=01012 的 u1=u3 與 u2=u4
   各有完整 H witness；兩份 witness 分別為 `0101223231`、`0101212303`，
   完整集合交集為空。
7. **混合 B/U marginals**：prism 的 `(beta index,tau index)`=(0,275)、(1,274)
   均在 R3；(0,274) 為空格，雖然其 beta 與 tau 各自出現在投影中。

前輪固定 witnesses 的所有原欄位與凍結證書一致，且上述數學內容另由新枚舉核對。
新 witnesses 的 literal labels、完整 arrays、空格、中心色與狀態逐項對新枚舉核對。

## R3 與 all-colour support 的補充嚴格性

[strict_support.json](strict_support.json) 是另列的兩圖證書，不混入原 34 圖的計數。
本 checker 從 two-spoke／exterior-apex 的獨立邊與面描述重新構造並核對全部資料，
也以刪除每個頂點後的連通性確認 H/G 都是 2-connected。

| 圖 | R3 | R4 | 完整 H lifts | 完整 G lifts |
|---|---:|---:|---:|---:|
| two_spoke | 700 | 700 | 1,400 | 700 |
| two_spoke_external_apex | 700 | 0 | 700 | 700 |

兩圖有相同具名 R3、相同 Sigma(G)，但 all-colour support 不同。共核對 20,480 格，
其中 18,380 空格、2,100 H lifts、1,400 G lifts，以及雙向合計 1,400 個 selector
輸入。具體差異格為 beta=01012、tau=10123：原圖有 lift，外側 apex 圖為空。
新增 apex 位於 U 外側，所有原 B/U 邊與 labels 保留；由獨立面與旋轉核對認證其
annulus 合法性。這對圖不聲稱 near-triangulated，也不聲稱最小來源身份。

## 未覆蓋範圍

有限枚舉只校準本輪的明確控制圖，普遍充分條件須引用主報告的紙面證明。
原 34 圖內「R3 相同但 all-colour support 不同」為 `not triggered`；補充兩圖在
一般 plane annulus 範圍給出實際反例，不能把此範圍自動縮到更強的來源子類。
沒有構造一般 annulus 小代表、沒有最小來源排除、沒有 Lean 證明，也沒有完成主命題。
