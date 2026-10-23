# 932 round2：原 C9 三接點來源排除合同

BASE `cb8f8593e273a7426ecadd59797a6e643cc4768e`。唯一寫入範圍為本 `932/`
子目錄；不改舊 audit、共享文件、其他分工、Lean，不 commit／push。
[INPUTS.json](INPUTS.json) 封存 15 份 exact bytes／SHA；前輪未提交檔由
round2 BASE 的 predecessor ledger 綁定，已追蹤參考檔另核 exact Git BASE。
全部 immutable 數學／custody 檔的 live drift 均 fail closed。四份共享
routing entry 只比較 SHA、獨立報告，`--check-entry-shared` 可另要求零 drift。

來源仍是全部完整 C5 relations 位於 K132 外的 disk 圖中，先最小化原內點
數 k，再最大化邊數的**同一**原 G；完整 `Σ(G)=932,h=4`。不是在 mask932
內另取最小圖。完整 outer row order 為

```
01012 01021 01023 01201 01202 01203 01212 01213 01231 01232
```

932 接受第 2、5、7、8、9 列（零起算）。保留原 B、五個 A apices、四個 Y
私人點、原有向 induced C9、所有原 attachments、annulus edges/faces/rotation、
820 inner row orbits、每列十份完整 annulus fibres（含空）與所有 full lifts。
20 個 `case_bindings` 保留前輪原 case canonical SHA，實際 C9 真名及每個
原邊面第三點 t_i 的定義。不同 query 的 c_i 不是同一來源。

繼承前輪任意大小定理：若原 I 點接三個 C9 點，恰為原 t_i，contacts
`{c_i,c_(i+1),c_(i+5)}`，並分出兩個實際 induced C6 cells 及空三角面。
本輪新輸入是這兩個原 cell 沿共同原邊 `t_i c_(i+5)` 的 full-fibre 雙射；
三個 anchors 的 literal colors 相異時，原 t_i 第四色唯一，完整 C9 count
matrix 因而 rank≤1，正支持是 rectangle。兩色 anchors 只給 rank≤2，
不得套用 rank-one 規則。所有 color restoration 均為一次 whole-S4 map。

本輪有限證書覆蓋20個原來源合同×9個原三接點位置；用原 whole Kempe
orbits 的必要 rectangle closure 將這180個假設的支持逐一刪空。這是
**原三接點分支排除**，不是全體原 h=4 來源排除。沒有假設 cell 內點數
有上界、沒有較大來源圖枚舉、沒有 count-cone 可行性替代原圖。

full-lift mesh 控制未提供原 B、完整932及全域最小性，所以完整來源狀態
明記 `not triggered`。本 checker 不接受 `--source`：未知具名來源提案
一律由 argparse 拒絕，不能把介面校準當成新的 source realization。

一般932、無三接點h=4、h≥5、smaller bad及新Lean仍OPEN；共同k≥23繼承不變。
