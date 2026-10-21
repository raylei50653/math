# 嚴格 only-R／W7 計數合同的獨立審核

審核以 `d5b8a8605bcbcef7aebbcf1934dad7ba255ccf02` 的既有完整 W7
介面為準，沒有把 112 份共同接觸型的額外原弦或零 fibre 偷加進來。
所讀權威是既有 [來源合同](../../2026-10-20-r6-941-j1-five-edge-417732f/SOURCE_CONTRACT.md)、
[完整計數證明](../../2026-10-20-r6-941-j1-five-edge-417732f/counting/PROOF.md)、
cap/orbit 生成器與壓縮整數表，以及舊 C11 的
[orbit 紙證](../../2026-10-20-r6-941-j1-c11-1148ce0/reduction/ORBIT_LEMMA.md)
與獨立整數核對。本文審核模型及探索方法；最終 cone 裁定須另以父層的精確證書
和獨立 checker 為準。

## 原來源到必要錐

來源是同一實際 J1 type III 完整著色中的具名五邊路，且具名 C7 內恰只有 R；
三角化及 induced C7 才迫原 R 七度和完整 W7。一般五邊路、C7 多內點、其他
type、更長路都沒有被這項嚴格假設覆蓋。核心是同一實際
`G−{b,p,h,R,x,y,r}`，全部原私有點、原弦及額外 n 附件都留下。

`Z_i` 是固定 canonical 字面 C13 色框的全部完整著色數，不是選路後殘餘，
也不是某份可重新選擇的著色。各 cap 均枚舉同一份完整核心著色的所有原星
lifts，R 重新量化。特別是某框色沒有合法 R lift，只能使相關 G cap 為零，
不能逕把核心 `Z_i` 判零。既有生成器保留了這個區別。

cap 所列零值及舊 C10 的空 fibre 都是必要零值；非負 orbit 支援閉包再消去
24 states。對偶或可行點應核對完整 66,430 states，或明確把所有被消去
states 與 touching columns 回補為零。61,308 個 live states 的存活只表示
支援閉包未證零。

固定 `01|23`，每份完整著色的兩 palette 全部分量生成完整交換 orbit。
若有 c 個不碰框的私有分量，不能丟掉 `2^c` 完整重數。保持 unordered
palette pair 的全域群 H 有八個元素；proper 奇 C13 至少用三色，所以每個
half-row 含八份字面 tuple。同一實際 orbit 對一個 half-row 的非零 entry
恰為四。故來源供應同一組非負整數 `Z,X`，滿足

```
8 Z_i = 4 sum_{j containing h} X_j,
即 2 Z_i = sum_{j containing h} X_j。
```

每個 canonical state 對應三個 half-rows，三式共用同一個 Z。把全域 S4
正規化、H-half-row 大小與完整 orbit 重數混為單一任意倍率會破壞合同；
現有 8/4 約分本身則完全精確。相同 boundary columns 可以合併其 X，
不減弱來源覆蓋。來源覆蓋依賴平面三角 disk 的完整 orbit 紙證，不能只用
與 C11 生成器校準成功替代。

## 嚴格正性與精確結果能說什麼

選定完整五邊路見證只供應 `Z_44459+Z_44466>0`。不能各自強加正性。
原七個 G 正列是 `01012,01023,01201,01203,01213,01231,01232`；另外原
`01232` 的 h=a、h=b 兩 sectors 皆正。它們可以由同一圖的不同完整著色
供應，但全部必須作用在同一 Z 上。

全部十個正量的係數非負。齊次錐中，它們能同時嚴格正，等價於各正量
各有一個錐可行點：把十個點相加即可。因此先裁定只有目標和正的放寬模型
是合法路徑；其精確不可行就已足排除本具名嚴格子型。反之，只有目標和正
的可行點，尚不是使用者要求的十項共同可行證書。

任何一組有理可行 `Z,X` 都可共同乘分母得到整數，並把十個正量同時縮放至
至少一；對這個齊次線性必要模型，不需額外先驗 parity 條件。有理可行只證
當前必要線性條件不足，不能證原圖存在，也不能證 112 份共同接觸型任一型
可實現。精確不可行則只排目前來源合同中的 only-R／W7 分支，不構造
smaller bad、不排一般五邊路、不新增 Lean 定理。

## 獨立結構探索與停止原因

`singleton_reduction.py` 直接讀取凍結格式整數 columns，沒有用 LP 的稀疏 E。
它從 singleton half-row 的 `X_j=2Z_i` 導出所有 `Z_k>=Z_i`，再對 inequalities
的有向圖求 SCC；SCC 內等值若飽和某 row，該 row 其他 columns 必零。
[精確輸出](singleton-reduction.json)顯示共有 740 singleton rows，SCC 大小
分布為 `{1:60852,2:140,3:8,4:22,8:8}`，沒有新增零欄，兩個目標仍存活。
這是該指定 facial reduction 的完整停止點，不是錐可行結論。

兩個目標的三份 half-row degrees 都是 `10,32,1`。其 singleton 欄精確給

```
X_306985 = 2 Z_44459，column states = 44050,44111,44459,44520；
X_306993 = 2 Z_44466，column states = 44046,44107,44466,44527。
```

完整 column/state incidence 為一個 61,308-state 連通塊，普通連通分解不能
縮小問題。另一個無損改寫是消去每個 Z：三個 half-row 的 X 欄和必相等，
每個 state 只需兩條差等式；從任一欄和除二可回復 Z。目標正量可直接寫為
`X_306985+X_306993>0`。

`local_dual.py` 的小模型只搜尋指定 y 支援：令每個 column 的 y 和非正，
非目標 state 的 y 和為零，兩目標 state 的 y 和各為一。若找到精確解，
同源等式即給 `2*(Z_44459+Z_44466)<=0`。小模型無解只限制該 y 支援，
不能推論原錐可行。

已保存四份實際數值停止記錄及原始 OptimizeResult：

| 探索 | y 變數 | touching columns | 實際停止 |
| --- | ---: | ---: | --- |
| 目標的一層 incidence 鄰近 states | 948 | 10,585 | 指定 dual-support LP 數值 infeasible |
| C11 deletion pullback 缺陷欄涉及的 states | 15,585 | 120,319 | 指定 dual-support LP 數值 infeasible |
| 同上一支援，容許非負 core slacks | 15,585 | 120,319 | 指定 dual-support LP 數值 infeasible |
| 全部 live half-rows，容許非負 core slacks | 183,924 | 307,197 | 300 秒 solver 時限；總計 302.90 秒 |

這四份探索沒有精確證書。數值結果從未升格為對原錐的裁定；相應 JSON
明載 `exact_certificate=false`。全 dual 結果見 `full-dual.json`，原始
`OptimizeResult` 全部保存在 `full-dual.pickle`；該次 SciPy 回傳 `x=None`，
不能改稱可核驗的 primal／dual iterate。沒有再啟動其他全模型 LP。

## 適合最終 checker 的負控制

對偶可選用一個已確認破壞整數恆等式的非零 y 竄改、漏掉一個必核對的
surviving column、改 target ID 或漏掉目標正性、把 inequality sign 翻向、
以及使用不同輸入 SHA 的證書，確認 checker 拒絕。
可行點應拒絕負係數、在已證零的 state/column 放正值、改一份共享 Z、漏核
三個 half-rows 中一個、以及漏核十項正量之一。兩類 checker 都必須把 cap
矩陣與 full-fibre 零值綁定到相同來源資料；只驗 discovery 用的 E 殘差不夠。
