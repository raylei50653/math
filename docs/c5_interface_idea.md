# 研究想法：用額外內部點轉接成 C5 interface

記錄日期：2026-09-12。來源：使用者提出「用額外內部點把一般邊界轉成一個語義上等價的 C5 interface」。本文件記錄研究問題與探索路線，不表示已開始合成、已證可行，或取代目前 normal form → GeoReject 的工作順序。

## 核心構想與等價規格

先以 C6／C7 為測試：在原有序邊界與新有序 C5 之間加入轉接 gadget E，允許額外內部頂點。令

```text
E(b,c) := 原邊界染色 b 與 C5 染色 c 可共同延伸成 E 的 proper 四色染色
E_* S := { c | ∃ b ∈ S, E(b,c) }
```

這是待實現的關係規格。必須先選定「語義等價」的強度：

1. 只保持是否存在完整染色：很弱，不能據此聲稱可替代原介面組合。
2. 可逆編解碼：存在 D，使 `∃ c, E(b,c) ∧ D(c,b') ↔ b=b'`；若在 orbit 上定義，等號改成明確的共同 S4 等價。
3. 相對於指定合法 continuation grammar 的等價：轉接前後，所有允許的後續接線有相同的觀察結果。須指定觀察是染色可延伸、GOOD/BAD，還是也包含 disk 接線合法性，並給出 context 的轉換規則。

主要研究候選是第 3 種（**conjectured / unresolved**）。必須固定 E 的適用範圍，不能先解出每個輸入 patch 的答案，再為它特製一個只保存答案的 C5。

## 容量限制：須區分單次 code 與關係集合

在普通四色染色、無固定色名或外加 lists、唯一對外介面為有序 C5 的前提下，gadget 關係尊重共同 S4 作用。對話中直接枚舉的結果（**computationally observed**）：

| 邊界 | proper 四色 assignments | S4 orbits |
| --- | ---: | ---: |
| C5 | 240 | 10 |
| C6 | 732 | 31 |
| C7 | 2184 | 91 |

C5 計數另已有專案 Lean 證明；C6／C7 此處未新增 Lean 證書。

數學推導、尚未 Lean 化：若要求在 orbit 層完整可逆編解碼，31／91 個狀態不能透過 10 個 code 可逆傳遞。隱藏的內部頂點能改變 E，不能增加 C5 本身的染色數量。

**修正對話末段容易過強的說法：找到超過十個 continuation 可區分狀態，不足以單獨否定任意關係式編碼。** 一個來源狀態可能編成一組 C5 codes；在無外加色名的 orbit 語意下，最多有 2^10 種集合。十的障礙直接適用於可逆／必須使用互不相交 code 的規格，不自動適用於所有觀察等價。保留具體色名的來源 b 時，其 code 集合也不必單獨 S4-saturated；必須先交代商空間和共同顏色對齊。

因此應檢查整個 compatibility relation 是否能經 C5 做 existential relational factorization，而非僅比較 equivalence-class 數量。即使集合數夠，也不表示可由合法 planar gadget 實現。

## 為什麼不直接用 overlapping 五點 windows

C6／C7 的連續五個 boundary 頂點通常是路徑，不是 C5；補封口邊會改變語意。

對話中的反例候選：外邊界 C6，內部 K3 的頂點為 a,b,c；a 接 0,1,2，b 接 3,4,5，c 無 boundary attachment。指定 boundary 染色 `012012`，a,b 都只能取第四色，但相鄰，因此無法延伸。忽略任何一個 boundary 頂點，將其改成第四色，就可以延伸；所以每個五點 restriction 都屬於完整 Σ 的相應投影。

C7 使用相同 attachment、boundary 染色 `0120121`，同樣成立。直接全染色枚舉結果（**computationally observed**）：

| 邊界 | 完整指定染色可延伸 | 通過的全部五點投影 | 完整 Σ 大小 |
| --- | --- | ---: | ---: |
| C6 | 否 | 6 / 6 | 660 |
| C7 | 否 | 21 / 21 | 1968 |

這是指定染色的拒絕，不是整張 patch 的 BAD。兩組 attachment 位於分離的 boundary arcs，支持 disk 畫法；本例未建立 Lean topology certificate。枚舉是對話內 Python 診斷，未保存獨立證書，不作已形式化前提。

它否定「由各五點 Σ 投影直接重建完整 Σ」的方案，沒有否定保留共享內部狀態的 window transducer，也沒有否定新提出的 C5 轉接 gadget。

## 幾何與對齊要求

- 固定 ordered ports；顏色作用採共同／diagonal S4，不對兩端獨立重命名而遺失 alignment。
- 外 Cn、內 C5 的轉接可先用 annular embedding 規格研究；必須明確寫出嵌入與組合條件，不能把兩條邊界的存在當成合法 annulus 的證明。
- 目前已知完整 Σ 相同也可能有不同的 disk context 合法性。因此若目標包含幾何可替代性，須額外描述 rotation、ports 或其他幾何狀態，並計入介面的實際資訊。
- 一般 relation composition 的代數定理不等於 graph-wiring 的 planar soundness。

## 建議續作

1. 完成既定 C5 normal-form／GeoReject 結構目標；利用已不限制 boundary 長度的 list lemmas 推一般 Cn，而非逐個重做枚舉。
2. 明確選定 C6／C7 的 patch grammar、continuation grammar、觀察語意與共同顏色對齊。
3. 建立小型來源狀態 × continuation 的 compatibility 資料，先研究能否透過 C5 的關係分解；保留可重驗的區分 witnesses。
4. 若代數上可分解，再從 primitive relation library 合成轉接 gadget，分別驗證 exact coloring relation 與指定嵌入。
5. 若單一 C5 不足，再研究多個 C5 ports 或帶共享狀態的序列轉接；不能把額外共享通道仍稱為單一五頂點介面。

所有可行性與一般性主張目前皆為 **conjectured / unresolved**。相關背景：[交接](HANDOFF.md)、[normal form](attachment_normal_form.md)、[automata](automata.md)。
