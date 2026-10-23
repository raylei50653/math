# 932 round2：排除原 C9 的全部三接點分支

**新定理：在原全域最小 no4ct `Σ=932,h=4` 的全部二十份來源合同中，
每個嚴格內點至多接兩個原 C9 點。** 九個原邊面第三點 t_i 的 C9 contacts
因而恰為自己原邊的兩端。前輪「至多一個」現在推進為「沒有」。
無三接點的 h=4 來源仍 OPEN；現行共同 k≥23 不變。

BASE `cb8f8593e273a7426ecadd59797a6e643cc4768e`。
[固定來源合同](SOURCE_CONTRACT.md)、[任意大小紙證](paper/PROOF.md)、
[完整有限證書](certificate.json.gz)、[獨立唯讀 checker](check.py)。

新增的來源限制來自兩個**實際原 C6 cell** 的完整接合。兩側只沿原邊
`t_i c_(i+5)` 相交，完整 H fibres 是按原 t_i literal color 分類的
Cartesian products 互斥聯集。當三個 C9 contacts 使用三色，t_i 第四色
唯一；固定這三個 literal anchors 後，兩條原三點弧所索引的完整 C9
20×20 extension-count matrix 是一個 outer product，正支持必為 rectangle。
兩色 anchors 只保留 rank≤2，未套用 rank-one 規則。

對原 H 每份實際全圖 coloring，其實際 Kempe 分量給一份完整 boundary
orbit；整個 orbit 均正。用上述同一原 H 的 rectangle 必要補閉，逐步
核對各 orbit 與當前必要支持。全部 `20×9=180` 個原 collar／原三接點位置
在 3–7 批後刪空，共 815 批、64800 次**有三接點假設的** row 刪除。
原完整 Σ932 非空，故180個原三接點假設逐一排除。這不是把幾個各自可行
的 cell、顏色邊際或來源見證拼成一張圖。

獨立 checker 不 import producer，從頭重建4862份 noncrossing partitions、
49356個 whole-Kempe options、九份20×20 literal mixing grids，並逐批核對
每個刪除的當時前提與全20×9覆蓋。它另重建二十份完整原 annulus：
164000 fibres，包含151605空 fibres，以及13990 full lifts。原名、attachments、
有向面、rotation 與完整 case SHA 全部保留。

一張前輪具名有向 disk 另校準 complete full-lift join：兩份 cell 各20
full lifts，其 Cartesian join 與直接 whole graph 的400份 full lifts
逐tuple完全相等；全部400份固定anchor fibres（其中231空）也比較。
此控制沒有原 B、完整932或全域最小性，其完整來源狀態為 `not triggered`。
原三接點排除由完整180份必要條件證書承擔，不由控制圖承擔。

正常／`PYTHONHASHSEED=17` 唯讀重播、九項語義負控制與 frozen-input drift
結果見 [VERIFICATION.json](VERIFICATION.json)。15份 immutable authority
均封存 exact bytes／SHA；四份共享 routing entry drift 獨立報告，strict
入場檢查另由 `--check-entry-shared` 啟用。產物只寫本子目錄，舊 audit、
共享文件、其他分工與 Lean 均不改，不 commit／push。

```bash
python3 -B audits/2026-10-23-three-mask-round2-cb8f859/932/check.py --check --negative
PYTHONHASHSEED=17 python3 -B audits/2026-10-23-three-mask-round2-cb8f859/932/check.py --check --negative
```

本輪沒有對來源內側大小設界，也沒有新 smaller patch／隱藏完成成本。
所有接合均使用原頂點、原邊及完整色 tuple，新增頂點與邊均為零。
不帶三接點假設的全部820列 catalogue、annulus fibres與full lifts不變；
沒有宣稱無條件 row deletion、計數錐可行解或原來源實現。

下一窄義務是**無三接點**原來源中，距四 double contacts 的共同嵌入或
具名 cell 的可回填化約。一般932、h≥5、smaller bad、K∞及新Lean仍OPEN。
