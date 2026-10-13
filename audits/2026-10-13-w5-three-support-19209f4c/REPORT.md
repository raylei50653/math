# 全內部 W5：三色具名代表契約與私人森林來源排除

2026-10-13。凍結 BASE：`19209f4cf68261fdce5e84a7804cfe04ae0957bf`。
本輪未取得一般或真正最小 933／941 來源的 r≤6 annulus 代表；取得一項新的
來源結構排除：**對每個全內部 W5，annulus 私人 induced graph 必含環。**
這嚴格縮小尚須處理的來源類，而沒有宣稱 K∞=K≤5。

## 1. 本輪交付

| 結果 | 精確範圍 | 證明／證據 |
|---|---|---|
| FOREST-EXCLUSION | 全域最小目錄外、再最大邊數來源；任何全內部 W5 的私人補圖必含環 | [完整新定理](forest/REPORT.md)、[獨立覆核](t1/forest_independent.md) |
| W3-TRANSPORT | 三色具名 support 相等，當且僅當補相同中心後存在保全部 B/U pins 的雙向 total full-lift 對照 | [精確契約與證明](t1/REPORT.md) |
| r_min=2 的障礙及構造 | 一般 annulus 的特定具名 support「b0=u0」；任意單一普通代表 r≤1 不可能，r=2 可實現 | [構造、下界及雙向 lifts](representatives/REPORT.md) |
| 五商圖來源專用 no-go | 固定最小 933／941 來源；依來源挑選五商圖及額外加邊的正聯集無法保 Σ | [精確目錄運算及洩漏見證](conditional/REPORT.md) |

使用者已指示暫不追查「T1」編號，故用 W3-TRANSPORT 明確命名本輪核對。
三色 support 的充分性原已見於上游 THEORY §6；本輪不是把此既有觀察算作
新的代表存在定理，而是補足必要性、完整對照與作用範圍。

## 2. 新增的來源縮小：私人圖不可為森林

固定原 B、U、v，令 P=V(G)\(B∪U∪{v})、r=|P|=k−6。
假設私人圖 G[P] 是森林，分量數 c，原 B–U 邊數 p。
來源的 occupied C4 排除迫每個私人點至多接兩個相鄰 B 點及兩個相鄰 U 點。
原 annulus 的面數與 degree 計數給

\[
 p\ge c,\qquad M=2c,\qquad r\le10-c-p\le10-2c,
\]

其中 M 是一點來自 B、一點來自 U、一點來自 P 的三角面數。每個私人 leaf
必占一個 M 面，故森林每個分量恰為路徑，沒有額外分支；k≥13 使 r≥7，
進而只剩單一七／八点路徑的三組參數。

再按原 path 兩側的 B/U ownership 走過環邊，紙面分類給恰 70 個必要模板：
20+30+10+10。所有模板直接全染色都得到 Σ=1023∈K。因此與最小目錄外身份
矛盾，完成條件性森林來源排除。這裡**先證有限模板完備性，再核對模板**；
沒有從任意截斷大小的搜尋推廣至無界來源。

全部 716,800 cells（701,956 空）、18,282 H full lifts、9,308 G full lifts
均保留，且独立程式用另一種 word 生成、邊表生成與直接 DFS 逐份重算相等。
原來源經具名同構搬到模板時，B/U 起點可各自搬運、方向符號須共用；顏色只做
全圖共同置換。這個對照是同一原圖的完整 lifts，沒有拼湊不同商圖的 witnesses。

此結論限制的是**來源私人圖**；它沒有證明代表私人圖不能為森林，也沒有證明
含環的來源不能壓成小森林代表。剩餘來源的環可為 contractible cycle，尚不能
要求它一定環繞 U。

## 3. 三色 support 已足夠，但存在性尚缺

用原色名保留

\[
 R_A^3=\{(\beta,\tau):J_A(\beta,\tau)\ne\varnothing,
                   |\operatorname{im}\tau|=3\}.
\]

三色是 U 的色數，β 仍遍歷外框全部十列。比較義務為 10×120=1,200 個 cells。
若合法同槽位 A' 有 R_A^3=R_A'^3，取同一 cell 兩側全部 fibres 的 Cartesian
product，再各補唯一缺色中心，便得到兩側 total 且逐 pin 相同的 full-lift 對照。
反向由 total 性即得 support 相等。不同 fibres 不需等基數；完整原 fibres
仍保存供追溯。若只保外框 Σ，僅需此 support 的 β 投影相等，但不再保 U 色列。

補中心後內點數仍為 5+r+1，因此 r≤6 的合法代表將接上 K≤12=K≤5。
本輪沒有證明這類代表對私人含環的最小來源必存在。

## 4. 實際小代表與精確低階障礙

為使小代表嘗試可檢驗，本輪明確構造支持「b0=u0」且其餘 proper B/U 色列自由
的 annulus：兩個私人點 x,y 與 b1 成三角形，b0、u0 同鄰接三角形三點。
故兩者必取相同缺色；反向任意目標 pin 色列都能把剩餘兩色按兩種次序放到 x,y。
完整定向面、旋轉、附件及全部 fibres 見構造報告。

同一 relation 不可能有 r≤1 的單一代表：所有對目標 support sound 的 pin-pin
邊只有兩環及四條指定跨環邊；一份 b0≠u0 的三色 pin 指派仍滿足全部這些邊，
唯一私人點可取未用第四色，故必洩漏。此紙面 no-go 甚至不需平面性，允許改整個
annulus 及新增一點，並非重做已排除的 U-only 零新點方案。

在 r=2 構造的三角面反覆插入三度點，可任意增大來源而保全部具名 support；
本輪保存五次插入的 r7→r2、補中心後 13→8 內點的完整雙向構造。
這是具體成功但**不適用真正最小來源**的類：其三度點與 occupied triangle
恰被上游最小來源前提排除。一般 r≤1 代表定理由此被否定；r=2,...,6 未被否定。

## 5. 來源專用商圖限制及其邏輯邊界

目錄中包含於 933 的關係只有 165；包含於 941 的只有 165、424、429。
它們全缺 `01232`。最小性使每個較小商圖落在目錄，故任何保留 `01232` 的
商圖必洩漏原拒絕列，精確落在 `{01021,01202,01212}` 中至少一列。
原 `01232` full lift 同時落在兩個相鄰單對商圖，所以至少有兩份**不同**的
拒絕列 H full lifts；每份 U 為四色，只有一個同色 pair。

這關閉「特定最小 annulus 自動過濾五商圖的多餘 lifts，再挑 sound 分支正聯集」
的逃生口。它是全域最小性及目錄的直接條件推論，不是來源實現，也不獨立排除
最小來源存在。兩份 formal support 控制顯示普通投影條件仍可同時滿足；它們
明確未宣稱有 annulus 圖實現，不當成來源 full lifts。

## 6. 搜尋範圍、驗證與保留缺口

本輪沒有枚舉所有 r≤6 annuli。構造嘗試的域為上述 equality gadget 與任意
stacked-face 裝飾類；有界來源核對則是先由紙面推得完備的 70 路徑模板。
另有四份 transport 控制及 132 masks 的精確目錄運算。沒有重跑舊 U-only
普遍正聯集搜尋、舊 34 圖證書或上游外部計數證書。

```bash
python3 -B audits/2026-10-13-w5-three-support-19209f4c/t1/check.py
python3 -B audits/2026-10-13-w5-three-support-19209f4c/representatives/check.py --check
python3 -B audits/2026-10-13-w5-three-support-19209f4c/conditional/check.py --check
python3 -B audits/2026-10-13-w5-three-support-19209f4c/forest/check.py --check
python3 -B audits/2026-10-13-w5-three-support-19209f4c/t1/forest_independent.py
```

正常／seed17、破損副本拒絕及原 bytes 未改的紀錄見
[verification](verification.json)、[三子包反控制](representatives/review_checks.json)、
[補入 provenance 核對後的 conditional 最終重播](conditional/final_verification.json)
及 [forest 獨立 seed17 重算](forest/independent_seed17.json)。
凍結輸入逐 hash 保持；執行中其他工作修改了共用入口，差異另存
[SOURCE_DRIFT](SOURCE_DRIFT.json)。已核閱的變化為較強外圈界及另線重接結果，
不改本輪使用的凍結前提；本輪沒有採納或覆寫那些並行成果。

| 層次 | 狀態 |
|---|---|
| 私人森林來源排除 | 條件紙面分類＋完備有限 kernel；獨立審核通過 |
| 合法 literal annuli、完整 cells／lifts 及反控制 | `triggered and holds`／明列 `counterexample` |
| 真正最小 933／941 來源 | `not triggered` |
| 一般或最小來源專用 r≤6 代表 | OPEN |
| 私人含環來源、其他跨區域縮減、K∞=K≤5 | OPEN |
| Lean | 未新增 theorem，未執行 build |
| 上游 K≤12／外部計數 | 沿用凍結依賴，未重跑 |

成果位於本專屬 audit 目錄；尚未接入共用導覽，沒有 commit 或 push。
下一個窄問題是來源私人圖含環時的 annulus 壓縮，保留本輪 1,200-cell 具名契約，
而不再對森林來源投入代表搜尋。
