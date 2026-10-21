# 嚴格 only-R／W7：凍結的完整同源必要錐

2026-10-20；BASE `d5b8a8605bcbcef7aebbcf1934dad7ba255ccf02`。
權威輸入為前輪[完整來源契約](../2026-10-20-r6-941-j1-five-edge-417732f/SOURCE_CONTRACT.md)、
[幾何證明](../2026-10-20-r6-941-j1-five-edge-417732f/geometry/PROOF.md)及
[完整計數證明](../2026-10-20-r6-941-j1-five-edge-417732f/counting/PROOF.md)。
全部前輪檔案的 bytes／SHA256 已在證據工作前記入 [BASE.json](BASE.json)。
本輪使用同一 Git BASE 與輸入檔，不改寫前輪證據。

## 來源與量詞

承接任意大小原 plane C5 disk G、原框 `(x,y,a,b,c)`、支持941、全域最小
內點再最大邊數、原 r 六度、p,h 五度、全部附件、rotation、非邊與原
C3/C4/C5 pocket 條件。固定 Q1 接受零的 J1 分支，以及同一完整核心著色
的 type III 實際12色五邊路 `n–u4–u3–u2–u1–L`。
只處理原 induced C7 `n–h–L–u1–u2–u3–u4–n` 的 h 側內部恰只有 R
的嚴格子型。此時 R 的完整原 star 為 `(n,h,L,u1,u2,u3,u4)`，恰七度。

同一核心 `D=G−{b,p,h,R,x,y,r}` 的有序 rim 是
`(a,n,u4,u3,u2,u1,L,q,c,s,v,w,t)`。原 n 及其全部額外鄰點、任意大小
外側私有圖及可能原弦都保留。沒有把選路後殘餘當成全部來源著色。

## 精確系統

`Z_i` 是 D 在 canonical C13 state i 的固定字面框色下全部完整著色數。
有66,430個 proper S4 states；所有空 fibres 也有座標。相同 Z 同時用於
G、Q1、J1 的完整 cap，包含重新量化的 R 色與左右完整 lifts。

既有零值包含 G 的 `01021,01202,01212`、Q1 的 `01232`、J1 的
`01202,01212`，以及所有能接回 frozen C10 零 fibre 的 R lifts。
初始5,098格為零；完整 orbit 支援閉包再排24格。
因此 live 集合 L 有61,308格，其他 Z 全為零。

前輪完整必要 orbit 家族固定為307,197個欄 `C_j`；欄ID採凍結清單的
0-based index。全部199,290個 H-half-rows 中有183,924個對應 live state。
`i(h)` 是 half-row 的 canonical state。每個 active half-row 都要求

```
2 Z_i(h) − Σ_{j: h∈C_j} X_j = 0,      Z≥0, X≥0.
```

這是 `8Z=4ΣX` 精確除以4；private components 的重數已在 X 中。
所有 half-rows 必須使用同一組 Z、同一組 X；不能逐 palette 各選來源。
矩陣 E 的大小是183,924×368,505，共4,448,132個非零項。

十個必有正量的固定順序為 G 的
`01012,01023,01201,01203,01213,01231,01232` 七列，接著是原 G 的
`01232,h=a` 與 `01232,h=b` 兩個 sectors，最後為
`Z_44459+Z_44466`。它們的係數向量記為 P_l，全都要求 `P_l Z>0`。
前九量可由同一原圖的其他完整著色供應，不移用其選路或私有顏色。

齊次性使共同嚴格正性等價於全部 `P_l Z≥1`；任意有理可行點可共同
放大成整數 Z,X。求解器只使用此等價尺度，不改變來源量詞。

## 證書與驗證邊界

[獨立 checker](independent/check.py) 只用 Python 標準函式庫，從原邊重建
全部 cap／sector 係數、canonical states、half-row map 與初始零值，
並釘死凍結 orbit 家族的 gzip bytes SHA256。它不 import solver。
orbit 家族的完整生成另由前輪 `orbits.py` 唯讀重建核對。

可行證書以 sorted unique 稀疏正整數 `z:[[state_id,value],…]`、
`x:[[column_id,value],…]` 記錄，省略的座標全為零。
checker 在全部183,924條方程逐項算整數和，再檢查十個正量。
通過只證既有必要線性錐可行，不證任何原圖、來源或較小bad存在。

不可行證書以 signed integer `y:[[half_row_encoded_id,value],…]` 及
十個非負整數 `lambda` 記錄，要求 `Σlambda>0`，並精確核對

```
2 Σ_{h:i(h)=i} y_h ≥ Σ_l lambda_l P_l[i]    (每個 live i),
Σ_{h∈C_j} y_h ≤ 0                          (每個 surviving j).
```

將原方程以 y 加權，左側恰為零；上述逐座標條件與非負 Z,X 卻迫它
至少為 `Σ_l lambda_l P_l Z>0`，矛盾。此時可排除上述嚴格子型。
若只對 target 正性求出這種證書，取前九個 lambda 為零，仍然有效。

數值最優／不可行訊息、未核對的 ray、近似零殘差及 restricted 子錐的
不可行都不是裁定。沒有任一精確證書時，保留完整模型、實際停止原因及
數值殘餘，維持 OPEN。一般 C7 多內點、type I／更長路、一般 J1／J2、
嚴格較小bad、主命題及 Lean 不由本輪必要錐的裁定自動解決。

112個共同接觸型尚未逐型加入本輪既有模型；它們所迫原弦的同色零 fibre
是可能的後續必要限制，不能在本輪求解時默認已納入。
