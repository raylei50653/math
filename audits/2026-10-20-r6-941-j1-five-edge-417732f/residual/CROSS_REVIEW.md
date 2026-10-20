# 獨立交叉審查：幾何、全源計數與殘餘接口

審查者為 residual 分支，僅讀其他分支，未改寫其輸出。
審查當時的檔案 SHA256 及獨立 cap 枚舉記錄列於 [checks.json](checks.json)。

[geometry/PROOF.md](../geometry/PROOF.md) 沒有將 R 五度錯移到一般五邊路。
一般 type III 固定實際五邊路後，先逐項排除 C7 的十四條弦；其中三條
異色長弦明確使用已完成的同染色三邊路排除。R 的內部位置沿原 h 扇形固定。
一般 induced C7 與 only-R 的額外前提有分開；只有後者才從內三角化推出
完整 R 七度及四點私有。九框外弦表保留唯一 a-u4 例外，C13 也沒有被誤稱
induced。二內點真 C7 控制只反駁局部 only-R 覆蓋，沒有被用作完整 J1 來源。

[counting/PROOF.md](../counting/PROOF.md) 使用同一實際 F13 的全部完整染色 Z。
三份 cap 對 R 重新量化四色、保六個原 rim 鄰點，且 G 的 hR 邊仍在；
完整右 cap 的 x/y/r 不等式與原 stars 一致。不同候選與兩個接受 sector 都投影
同一 Z。未將 selected path/type III/historical residual 當成全源 count vector。

[review_caps.py](review_caps.py) 另從原 cap 邊、原等式與全部 cap 變數的笛卡兒積
作直接 whole-cap 枚舉，以本審查者的 canonical 函數分類，對 60 個字面 C13
state 核對三張圖的十列及兩個原接受 sector，全部相同。樣本包括兩個具名
正目標的所有 24 份 S4 像；這是獨立有界核對，不聲稱取代 parent 的全矩陣重播。
完整逐列資料在 [review-caps.json](review-caps.json)。

完整 orbit 紙證把不碰框私有分量的重數 `2^c` 留下，H-half-row 大小 8 與
每列 entry 4 的來源解釋一致。正規化只用於全源；不對 residual Y 宣稱全域
色置換對稱或 orbit invariance。支持閉包的 61308 存活、兩個正目標存活與
同源 cone 有解清楚區分。LP 無 primal/dual 的停止也未被稱作 feasible。
C11 λ 的直接 deletion pullback 有完整 C13 column 非零 pairing 控制；只否決
該操作，不宣稱不存在其他恆等式。

本分支的真 disk 另給 full 字面 counts 3/3、selected counts 2/0，以及刪 R
core action 令 cap multiplicity 1→0 的反例。它們支持上述兩項接口限制：
歷史遮罩不能直接替換完整 Z；若主張原 completed-source 見證沿 core action
守恆，必須另證 restriction/lift 交換圖。未見需要阻擋本輪窄結論的問題。

審查不把任意大小來源紙證冒稱 Lean 形式化，也不提供一般五邊路覆蓋、
完整來源實現、J1 排除或較小 bad。
