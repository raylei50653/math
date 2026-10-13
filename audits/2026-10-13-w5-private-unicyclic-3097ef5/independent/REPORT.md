# 單環有限核心的獨立全 fibre 核對

本 checker 不 import 主程式，也不 import 舊森林程式。完整來源的任意大小化約
由 [結構稿](../structure/STRUCTURE.md) 負責；本檔核對該完備必要域的實際圖、
指定 annulus embedding 與全部 literal 染色 fibres，不以零來源觸發代替紙面證明。

## 獨立方法與完備性

[check.py](check.py) 枚舉長度 7 至 10 的所有三字母詞，保留兩座標總和均為 5
的詞。若 `(1,0),(0,1),(1,1)` 數量為 `a,b,d`，則
`a+d=b+d=5`、`a+b+d=r`，所以 `a=b=r−5,d=10−r`。
四個長度的完整 linear words 數為 210、560、630、252，共 1652。
這是對結構稿導出的必要詞域做完整枚舉，不是一般 annulus 搜尋。

主程式以 oriented faces 構邊；獨立程式直接把每個私人點接到 B/U 的實際
一點或兩點鄰居區間，另加入三個原環。完整 edge set 必須逐條相等。
獨立程式再由每條 dart 沿 rotation 走面，驗證 sphere Euler、全部 faces、
指定反向 B 外面及正向 U 空內面；補中心後再次核對所有原邊與面。
其私人誘導度數一律是 2，私人點在完整 G 中的度數為 5 或 6，防止把来源
degree≥5 誤套到 F。

主程式以 MRV 選變數；獨立程式按固定 literal 順序 U、實際中心（如有）、
私人環搜尋。A 與 G 都直接 DFS；G 的染色搜尋不由 A 的三色支援推得。
每份 A full lift 依原 `U=τ` 放入其唯一 cell，每個 β 的全部 1024 個 τ cells
（包括 improper τ 與空 cells）逐格比對。G 全部 full lifts 亦逐份相等。
十個 β 由所有 proper 四色 C5 色列同時正規化獨立導出；任意 literal β 以
同一全域色置換搬運至其中一列，沒有分開正規化 B、U 或私人染色。

## 實際結果

[normal.json](normal.json) 與 [seed17.json](seed17.json) 全文 bytes 相等，
SHA-256 記於 [verification.json](verification.json)。兩次皆 exit 0：

| 量 | 完整核對結果 |
|---|---:|
| 模板 | 1652 |
| 全部 B/U cells | 16,916,480 |
| 空 cells | 16,448,400 |
| A full lifts | 657,580 |
| G full lifts | 320,840 |
| 完整 capped Σ=1023 | 1652 / 1652 |

第一次獨立探索也得到相同計數，保留於 [exploration.json](exploration.json)。
真正最小 933／941 來源的實現仍是 **not triggered**。
必要模板與所有 finite cells 的控制為 **triggered and holds**。
結合紙面完備化約，這些模板全部 Σ=1023 與真正來源 Σ=933／941 的整圖 D5 像
不相容；本程式本身沒有代替或重新證明來源正規形、k≥13、occupied C3/C4 排除。

## 主程式審核

已逐函數閱讀主 [controls/check.py](../controls/check.py)。MRV 選點完整遍歷
所有未指派頂點及全部可用色，每次遞迴返回後重設指派；零可用色只剪掉當前
不可能分支。直接 G DFS 與 A 補中心缺色的結果逐份相等。
三字母多重集生成沒有遺漏或重複；stream 每一行與完整重算的 graph bytes 相等，
並核對 header、末尾 EOF、summary 及完整 1652 詞 index。沒有只核對哈希或 mask
而忽略 fibres 的捷徑。獨立 checker 另外以獨立生成的完整詞集合核對覆蓋。

## 必要的反控制

[negative_controls.py](negative_controls.py) 不 import 任一 checker；它讀取原證書
第一圖 `BBDDDUU`，各自寫出一份有意破損的 header+first-graph stream。
每份都要求兩個 checker 在第一圖即拒絕，不能以後續 truncation 充當成功反控制。
六次實際 exit 1 及細節在 [negative/summary.json](negative/summary.json) 與其 logs。

1. 刪去 `β=01012, τ=01031` cell 唯一 A lift `01012010312323123`，並同步刪掉
   其唯一補中心 full lift；這使一個必要 support cell 變空，而 Σ 欄位仍為 1023。
   兩個 checker 都因第一圖完整 rows 不符拒絕，證明不只核對投影。
2. 把原邊 `(0,10)` 改成原本不存在的 `(0,11)`，兩個 checker 在第一圖拒絕。
3. 只反轉指定 U face，抽象 graph edges 不變；兩個 checker 都拒絕，獨立 checker
   具體在指定 U 面的方向檢查拒絕。

這些是證據完整性的反控制，不能稱為最小來源命題的反例。
同 Σ 不同 R³、同 R³ 不同 fibre 重數的真實 annulus 控制另由
[既有結果回歸](../review/regression.json) 及 [來源審核](../review/forest_review.md) 負責。

實際命令：

```text
python3 -B audits/2026-10-13-w5-private-unicyclic-3097ef5/independent/check.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-w5-private-unicyclic-3097ef5/independent/check.py
python3 -B audits/2026-10-13-w5-private-unicyclic-3097ef5/independent/negative_controls.py
```

本次只新增 `independent/` 下的檔案，沒有覆蓋舊 audit 或改動其他 session 的檔案。

## 同槽位 r′=0 代表與新保存強度控制的獨立補核

[strength_check.py](strength_check.py) 不 import 主程式，只重用本目錄的獨立
fixed-order DFS。五個圖的原邊重新明列：prism 的兩環及五條對位邊；加入五條
對角的 triangulated prism；對 `(b0,u0)` 同接一個二度私人點；用一條 bridge
把私人三角形接到 b0；最後以五個 `(1,1)` 步重建 r=5 essential 私人環。
全部 rotation/face orbits 由獨立方法重建；bridge 面的合法重複頂點特別容許，
不把「所有面都是 simple cycles」錯當成弱前提 annulus 的普遍限制。

五圖完整核對共 51,200 cells（48,965 空）、14,380 A full lifts、7,260 G full
lifts；全部 capped Σ=1023。normal 與 `PYTHONHASHSEED=17` 皆 exit 0，
兩份完整輸出 bytes 一致，見 [strength_normal.json](strength_normal.json)、
[strength_seed17.json](strength_seed17.json)、[strength_verification.json](strength_verification.json)。

| 圖 | 私人點數 | R³ 非空 cells |
|---|---:|---:|
| prism 代表 | 0 | 340 |
| triangulated prism | 0 | 20 |
| prism 二度私人點裝飾 | 1 | 340 |
| contractible 私人三角形弱前提圖 | 3 | 340 |
| essential r=5 弱前提圖 | 5 | 70 |

prism 與 triangulated prism 的 Σ 相同而 R³ 不同；二度裝飾保留全部 R³，
每一非空 fibre 大小恰乘 2。私人三角形控制也保留全部 R³，大小恰乘 18。
每個倍率均逐一核對全部 10,240 cells，空格亦保持。兩份圈秩 1 弱前提圖的
`rho_private`、完整 G 度數與私人度數由原邊重算；來源最小性仍是 not triggered。

必要模板 `BBDDDUU` 到 r′=0 prism 只保 Σ，不能聲稱保 R³。完整差異 witness
亦獨立 DFS：`β=01012, τ=01031` 在模板有且僅有 lift `01012010312323123`，
在 prism 的 fibre 為空。這與刪失必要 lift 的反控制使用同一具名 cell；
同一 β 在 prism 仍有其他 τ 被接受，因此完整外框投影保持。

```text
python3 -B audits/2026-10-13-w5-private-unicyclic-3097ef5/independent/strength_check.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-w5-private-unicyclic-3097ef5/independent/strength_check.py
```
