# W5-RANK3-C：核心與附件覆蓋的交叉審閱

固定 BASE `50d5474f2446403f3b3001d5943571184c8c9936`。
審閱對象為 `structure/CORE.md`、`structure/ATTACHMENTS.md` 及
`controls/check.py`；本檔作者獨立推導原 block/M 化約，並交叉核對另一作者
的附件證明和主生成器。本檔不代替 `independent/check.py` 的逐圖面與染色
獨立核對。

判定：**PASS（紙面必要域覆蓋與主參數實現的介面）**。

## 1. 原 block 分類與 M 計帳

* 三個 bounded F faces 是原 PPP 三角面；不能把圈秩三解讀成任選三個環。
* maximal 2-connected block 的 bounded face 不得再藏私人點、其他 block
  或 bridge slit，否則 disk 三角化給出更大的私人二連通 block。
* 對 rank h 的 block，`n=h+2−i, b=h+2−2i`；h≤3 完整給出三角形、diamond、
  五邊形 fan，以及有一個原內點的 K4。K4 的內點完整 G-degree 三直接違反
  來源條件。另從原 F face corners 獨立得到：不在 F 無界面上的私人點
  完整 degree 至多三，因此不存在遺漏的內部私人點。
* connecting skeleton 的 cyclic-block incidences 至多 `2(m−1)`；每個未
  用於連接的 ear 可直接供應 M，或注入其獨有附樹的一個 leaf。不同原點
  對應不同 BUP 原面，因其只有一個私人頂點。未假設私人最小 degree 二。
* c=1 的 diamond+triangle、三 triangles 分別至少需 M=3、5；c=2 的
  (2,1)至少需 M=5，均被各自面預算排除。存活域為一個 pentagon block，
  兩 ear tails，以及 c−1 個非平凡 paths。全部原 bridges、cut vertices
  和 subdivisions 保留；M 等號才排除額外分叉或附樹。

## 2. 原 contour、crosscuts 與所有 gap 分支

私人分量恰有兩次 terminal B/U 切換；這是已證 `M=2c` 飽和的結論。
不存在「同一分量四次切換」被 word 編碼暗中漏掉的情形：每個其他分量
本身已至少需兩面，故四次切換會超出全域預算。

每個 BUP 面有唯一 B–U 原邊，且在某 region 的一個 bounding cross-edge
side 上。每個 side 只 incident 一個 annular 原面，所以一個 region
至多兩個 M 面；p=1 的同一 edge 兩份 sides 與 cross edges 共端點均在
證明中保留。這正好把一個私人分量分配給一個 strip。無私人 region
沒有內部 cross edge 或同環 chord，必是單一 terminal triangle。

pentagon 的兩 contour 弧分別經 apex z 和另一側 w,t。`apex=B/U` 兩個
分支皆列入；apex 的私人 degree 四，加其一個／兩個 terminal pins 給
`apex_step=0/1`，另一側兩点各需兩 pins，連續前進兩格。因此四種 gap
前進量 `(0,2),(1,2),(2,0),(2,1)` 全部保留，沒有照抄 diamond 的(1,1)。

背骨 letters 的允許域逐點等同 `d_F+2+δB+δU≥5`。所有非 gap path 邊
均保留兩側原面；gap 明確沒有 xy 原邊，恰有七條五邊形 block 原邊。
U-apex 是整個 gadget faces 的反向，並非單獨反轉 U pin map。指定外面
與 U 空面的方向、共同 ε 的 pin maps 與原文一致。

## 3. 主 generator 的範圍與獨立參數重枚舉

逐行核對 `parameters()`：c=1 的 r=7,…,11、c=2 的 r=7,…,9；c=2 的
path 長 t=2,…,r−5；其餘 backbone 長 s=r−t−3；全部 s−1 gap 位置；
兩 apex sides、兩 apex steps、全部 letters；以兩環剩餘前進量唯一決定
全 terminal B/U triangle 數，取其和另一 path 的全部排列。
`step_words()` 的 degree 是原私人 degree，不是完整 degree。

另以不 import 主程式的臨時 Python 程式，直接用數值對
`{(0,0),(1,0),(0,1),(1,1)}` 和逐點完整 degree 不等式重建 word 域，
用遞迴 multiset 排列（非主程式的 permutations/set）列舉後續 regions，
與 `controls/templates.json` 的全部參數字典作 Counter 相等核對。實跑輸出：

```json
{"by_c":{"1":2162,"2":108},"descriptions":2270,"independent_parameter_domain":"PASS","unique_descriptions":2270}
```

這核對參數介面，不把有限數量當作紙面覆蓋證明。原圖量詞由 CORE 的
block-cut/M 論證以及 ATTACHMENTS 的原 rotation/crosscut 論證共同承擔。

主 `make()` 另由完整有向 faces 恢復 literal edges 與 vertex links，檢查
reverse darts、每個 vertex 單一 rotation、連通與 Euler；重算私人分量
（含樹分量）、圈秩、完整 degree 與面式。其必要域沒有為了得到排除結果
而額外假定全 U-degree、小 cap 或其他未證條件。

## 4. 保存強度與結論界線

source-to-template 是同一原 pins/rotation 的完整圖同構，保所有完整
fibres、空格、十 pins 和中心色；它本身沒有減少私人點，也不是代表。
若主及獨立 checker 證明全部模板補中心的完整 Σ 落在 K132，便可直接
排除來源，不必額外構造 A′。這不意味不同同 Σ 圖有相同 R³。

本覆蓋審閱本身不宣稱有限染色計算已由審閱者重跑；該結果、normal/seed17、
負控制與全部證書完整性以各自正式驗證檔為準。沒有新增 Lean theorem。
