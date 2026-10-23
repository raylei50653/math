# C5 cell 翻邊：完整四格引理與核對工具

2026-10-13。本文把 `891 + b3v8 − b4v6` 整理成可引用的局部引理與
可重播的有限核對。工具為
[`scripts/c5_cell_transform.py`](../scripts/c5_cell_transform.py)；研究狀態入口見
[State 導覽](c5_state_guide.md)，既有重接界線見
[共面正規形 §4](c5_cofacial_normal_form.md#4-完整-fibres-與重接界線)。

**後續分類實驗**：[翻邊距離與有限分類](c5_cell_flip_classification.md) 從 132 份目錄代表
保留實圖作三步 BFS，給出 132×132 距離表與 29 組三步特徵；步數限指定嵌入規則，
不將同 Σ 代表互換當成免費操作。

## 1. 操作及平面前提

固定有限簡單 disk 圖 $G$ 與具名、有序的外框

\[
B=(b_0,b_1,b_2,b_3,b_4).
\]

設非框邊 $e=st$ 的兩側是內部三角面 $stu$、$stv$，四個頂點
$s,t,u,v$ 互異，且 $uv\notin E(G)$。這裡要求兩個**面**，只有兩個三角形
子圖不足夠。刪除 $st$ 後，兩面合成四邊形 $u-s-v-t-u$；在同一區域加入
$uv$，得到

\[
H=G-st,\qquad G'=H+uv.
\]

這是對角線翻轉（edge flip）。四邊形外的嵌入、全部具名頂點與原 C5 外框
保持不變，故 $H,G'$ 仍是同外框的簡單 disk 圖。此結論是平面合法性，
尚未斷言染色關係不變。

## 2. 完整四格引理

固定顏色集合 $C=\{0,1,2,3\}$。對每一個合法外框色型代表 $p$，在**同一張**
$H$ 上定義

\[
J_p(i,j)=\{c:V(H)\to C:\ c\text{ 為 proper},\ c|_B=p,
\ [c(s)\ne c(t)]=i,\ [c(u)\ne c(v)]=j\},
\quad i,j\in\{0,1\}.
\]

四格保存全部完整延伸（full lifts），包括空格；不可先將內部顏色獨立正規化，
或把不同來源、不同外框列、不同固定顏色條件的見證混合。如果另有固定點及指定
顏色條件，須在四格中施加同一份條件；以下集合恆等式仍成立。
但固定某些具體顏色可能破壞全域 $S_4$ 對稱，此時須逐一檢查相容的實際外框
染色，不能直接以原十列代替；本工具的十列模式沒有額外固定顏色條件。

**引理。** 記 $F_p(X)$ 為 $X$ 對固定 $p$ 的完整延伸集合，則

\[
\begin{aligned}
F_p(G)&=J_p(1,0)\mathbin{\dot\cup}J_p(1,1),\\
F_p(G')&=J_p(0,1)\mathbin{\dot\cup}J_p(1,1),\\
F_p(G+uv)&=J_p(1,1),\\
F_p(H)&=\mathop{\dot\bigcup}_{i,j\in\{0,1\}}J_p(i,j).
\end{aligned}
\]

**證明。** $H$ 的每份 proper 染色由兩個是否異色的布林值唯一落入一格。
恢復 $st$ 恰要求第一值為 1；加入 $uv$ 恰要求第二值為 1。兩邊都在時
恰落入 $J_p(1,1)$。逐列篩選即得所有等式。這個集合論證本身不要求平面性；
§1 的面條件另行保證 flip 前後屬於 disk 類別。證畢。

四邊形周邊四條邊都保留，因此四格也有直接的顏色意義：$J_p(0,0)$ 在四邊形
恰用兩色；$J_p(1,0)$、$J_p(0,1)$ 恰用三色；$J_p(1,1)$ 恰用四色。這裡只
計算四邊形上的顏色數，沒有要求整圖使用同樣多的顏色。

令 $S_{ij}=\{p:J_p(i,j)\ne\varnothing\}$，則完整邊界關係滿足

\[
\Sigma(G)=S_{10}\cup S_{11},\qquad
\Sigma(G')=S_{01}\cup S_{11}.
\]

因此在上述無額外固定顏色條件的 C5 模式，flip 保完整 $\Sigma$ 的
**充要條件**為：對全部十列 $p$，

\[
J_p(1,0)\cup J_p(1,1)\ne\varnothing
\iff J_p(0,1)\cup J_p(1,1)\ne\varnothing.
\]

等價地，只需在 $J_p(1,1)=\varnothing$ 的列比較 $J_p(1,0)$、$J_p(0,1)$
是否同時非空或同時為空。失去及新增的列恰為

\[
\begin{aligned}
\mathrm{Lost}&=S_{10}\setminus(S_{01}\cup S_{11}),\\
\mathrm{Gained}&=S_{01}\setminus(S_{10}\cup S_{11}).
\end{aligned}
\]

一個簡單充分條件是每列 $J_p(1,0)=J_p(0,1)=\varnothing$，此時連完整延伸
集合也相等。若只有全部 $J_p(1,0)$ 為空，則
$\Sigma(G)\subseteq\Sigma(G')$；若只有全部 $J_p(0,1)$ 為空，包含方向相反。
只保留一列、只比延伸總數，或只看兩個端點條件各自可行，都不足以推出上述充要條件。

**共同延伸不能用兩個 mask 的交集代替。** 一般只有

\[
\Sigma(H+st+uv)=S_{11}\subseteq\Sigma(G)\cap\Sigma(G'),
\]

不保證等號。右側可能以一份 $J_p(1,0)$ 延伸接受原圖、另一份 $J_p(0,1)$ 延伸
接受翻邊圖，卻沒有同時滿足兩條對角線的延伸。也就是先取「存在完整延伸」再交集，
不能替代在同一份完整延伸上加入兩個條件；論證中必須保留共同圖的四格。

## 3. 891 代表上的完整例子

使用 [cells.json](../artifacts/c5_cells/cells.json) 的具名 `891` 代表，
$s=b_4,t=v_6,u=b_3,v=v_8$。原兩面為
$(b_3,b_4,v_6)$、$(b_4,v_6,v_8)$，四邊形為
$b_3-b_4-v_8-v_6-b_3$。固定目錄中每列的實際顏色，完整四格大小如下：

| 外框色型 $p$ | $J_p(0,0)$ 大小 | $J_p(0,1)$ 大小 | $J_p(1,0)$ 大小 | $J_p(1,1)$ 大小 |
|---|---:|---:|---:|---:|
| `01012` | 0 | 0 | 1 | 1 |
| `01021` | 1 | 1 | 2 | 1 |
| `01023` | 0 | 0 | 0 | 0 |
| `01201` | 2 | 1 | 3 | 1 |
| `01202` | 0 | 0 | 3 | 1 |
| `01203` | 1 | 0 | 1 | 0 |
| `01212` | 0 | 0 | 1 | 2 |
| `01213` | 0 | 1 | 0 | 0 |
| `01231` | 1 | 2 | 1 | 0 |
| `01232` | 0 | 0 | 0 | 1 |

依目錄 bit 次序，四格 support mask 分別是 `298, 394, 379, 603`。
共同圖 $H$ 的 mask 為 `1019`。同一目標邊集合的兩種執行次序為：

\[
\begin{array}{lllll}
\text{先加後刪：}&891&\xrightarrow{+b_3v_8}603&\xrightarrow{-b_4v_6}987,\\
\text{先刪後加：}&891&\xrightarrow{-b_4v_6}1019&\xrightarrow{+b_3v_8}987.
\end{array}
\]

`603` 中間圖非平面：內點 $v_5,\ldots,v_9$ 提供 $K_5$ 的八條邊，缺少的
$v_6v_7$、$v_8v_9$ 分別由內點互不相交的路徑
$v_6-b_4-v_7$、$v_8-b_3-b_2-v_9$ 補成，得到 $K_5$ 細分。
先刪後加的 `1019` 中間圖則維持同一 disk 嵌入。

本次 flip 失去 `01203`、新增 `01213`，所以不保原 `891` 的完整關係。
`01231` 在先加邊時消失，刪除舊邊後由 $J_p(0,1)$ 恢復。
這列的 $J_p(1,0)$、$J_p(0,1)$ 都非空，$J_p(1,1)$ 卻為空，恰示範上述
交集陷阱：mask 的 bitwise 交集 `891 & 987 = 859`，而同時保留兩條對角線的
實際 mask 是 `603`；差出的 bit `256` 正是 `01231`。

最後 `987` 可由一個內點 $x$ 連至 $b_1,b_2,b_3,b_4$ 表示：可補上 $x$
當且僅當這四個邊界點未用盡四種顏色，故恰拒絕 `01023, 01203`。
這是**翻邊後**整個 cell 的同外框等價代表；不等於原 `891` 的等價壓縮。
依 [封閉介面替換原理](c5_boundary_relations.md#32-一般規則以相同介面關係替換-patch)，
只有外部僅透過該 C5 互動時，才可用它替換整個 cell。它不保留舊內點名稱、
延伸數量，或後續對舊內點加邊的語義。

## 4. 工具用法與界線

從倉庫根目錄執行；依賴沿用 `networkx==3.5`。工具以 apex 接全部外框點來取得 disk
嵌入並保存計算出的 rotation；一般平面性與指定 C5 可作外框分開核對。
每輪由實圖重新求一份嵌入；目前不接受使用者指定 rotation，也不承諾跨輪固定
同一 rotation。嚴格 `--flip`／`--list-flips` 限連通圖；一般加刪邊及完整染色
分析可處理不連通內部，此時報告的面表是各連通分量的面邊界遍歷，不記錄分量巢狀位置。

```bash
uv run --with networkx==3.5 python scripts/c5_cell_transform.py --cell 891 --flip b4 v6 b3 v8
uv run --with networkx==3.5 python scripts/c5_cell_transform.py --cell 891 --add b3 v8
uv run --with networkx==3.5 python scripts/c5_cell_transform.py --cell 891 --remove b4 v6
uv run --with networkx==3.5 python scripts/c5_cell_transform.py --cell 891 --list-flips
uv run --with networkx==3.5 python scripts/c5_cell_transform.py --cell 891 --flip b4 v6 b3 v8 --output /tmp/c5-flip.json
uv run --with networkx==3.5 python scripts/c5_cell_transform.py --graph /tmp/c5-flip.json --flip b3 v8 b4 v6
uv run --with networkx==3.5 python scripts/c5_cell_transform.py --check /tmp/c5-flip.json
```

`--cell` 載入指定目錄代表的實際邊表，並非宣稱同 mask 的所有圖都有同樣可翻邊。
`--graph` 接續保存結果中的實圖；逐步探索須保留它，不能每步只傳 mask 再換成
另一份目錄代表。`--output` 以 exclusive 建立 JSON，既有路徑不覆寫。
也可輸入自備 JSON：`vertices` 是全部整數頂點 ID，`boundary` 是有序五點，
`edges` 必須包含全部原邊及五條框邊。`b0` 至 `b4` 依 `boundary` 解析，
`v8` 表示字面頂點 ID 8；完整染色的座標次序明列於 `vertex_order`。

報告核對每列固定顏色下的完整延伸、前後關係及新增／失去列；flip 另保存共同圖
的全部四格。`--list-flips` 只列計算所得 disk 嵌入中的候選，不聲稱窮盡其他
嵌入下的候選。完整枚舉隨內點數呈指數成長，預設上限為八個內點；可用
`--max-inner` 明確調整。

`--check FILE` 重新計算整份有限報告；核對通過表示該具體來源與報告一致。
§2 的普遍引理由紙面集合證明給出，Python 計算不替代該證明，也沒有新增 Lean
定理。工具不證明任意圖可經保 $\Sigma$ 的 flip 序列縮至五內點，亦不把本例
提升為一般 `891 → 987` 等價規則。

## 5. 有限證據與重播

[891 翻邊完整證書](../artifacts/c5_cell_flip/891_to_987.json)保存原圖、刪邊圖、
雙對角線圖、結果圖的完整邊表與逐列延伸，四格包括空格；另保存平面檢查、
disk rotation、目錄來源 SHA-256，以及重新驗過的一內點代表。
證書中的小代表使用新的內點 ID，沒有自動替換研究中的實圖。

```bash
uv run --with networkx==3.5 python scripts/c5_cell_transform.py --check artifacts/c5_cell_flip/891_to_987.json
uv run --with networkx==3.5 python -m unittest discover -s tools/tests -p test_c5_cell_transform.py
```

本例與[獨立測試](../tools/tests/test_c5_cell_transform.py)使用的逐內點笛卡兒積
枚舉對比完整 lifts；生產工具使用逐頂點最小候選色回溯，沒有以 mask 表當判定。
測試涵蓋四個中間狀態、反向恢復原邊表及全部 lifts、同框小代表的關係相等但
計數不同、任意頂點 ID 搬運、不連通內部、平面卻非 disk 的負控制及非法操作拒絕。
證據限這些具體控制；一般可縮減性與 Lean 形式化仍未處理。

2026-10-13 實際驗證：15 項測試通過；完整證書重播與 `PYTHONHASHSEED=17`
重播通過。CLI 另驗保存後反向恢復、拒絕覆寫既有檔案、拒絕四格計數遭修改的
證書及非法翻邊。一般文件檢查與正式 `docs/` DocGraph 檢查通過；全工作樹
DocGraph 仍因既有 frozen audits／scratch 複本的 62 個重複 ID 失敗。
本輪不更動這些舊證據，也不將這項文件索引失敗混作染色核對失敗。

## 6. Σ 的數字能否直接表示操作？

可以為特定操作選擇更自然的座標；一般內部翻邊則需要補充原 Σ 未保存的資訊。
以下保留原 catalogue mask 作 ID，只增加輔助編碼，不改動目錄或既有距離證書。

### 6.1 幾何上的五格加五格

proper C5 的三色色型必為重數 $(2,2,1)$，四色色型必為 $(2,1,1,1)$。
因 C5 的獨立集最多兩點，這恰給十個色型：

- $A_i$：三色色型中，唯一出現一次的顏色位於 $b_i$。
- $B_i$：四色色型中，唯一重複色對是 $b_{i-1},b_{i+1}$。

索引皆模 5。將是否可延拓寫成兩個五位元數 $a,b$，第 $i$ 位分別代表 $A_i,B_i$：

| 幾何座標 | 原 catalogue bit 索引 |
| --- | --- |
| $A_0,A_1,A_2,A_3,A_4$ | `6,4,3,1,0` |
| $B_0,B_1,B_2,B_3,B_4$ | `8,2,7,9,5` |

這是十個 bit 的可逆重排，不增加或丟失資訊。全域重標 $b_i\mapsto b_{i+1}$
使兩個五位元數同時循環位移；反射 $b_i\mapsto b_{-i}$ 使兩組索引同時反轉。
這是邊界重標的操作，不計為固定外框的實圖翻邊。

例如 `891` 對應 $(a,b)=(31,25)$，接受全部 $A_i$ 與 $B_0,B_3,B_4$；
`987` 對應 $(31,13)$，接受全部 $A_i$ 與 $B_0,B_2,B_3$。
故 §3 的翻邊效果可讀作 **$B_4\to B_2$，其餘色型保留**。
原座標中即清掉 bit 5、設置 bit 7：

\[
987=(891\mathbin{\&}(1023\mathbin{\oplus}32))\mathbin{|}128,
\qquad 891\mathbin{\oplus}987=160.
\]

這描述該次操作的效果；`160` 的兩個置位不表示做了兩次 flip。

### 6.2 加入邊界弦有通用 bit 公式

加入弦 $b_{i-1}b_{i+1}$，只要求已固定的兩個邊界顏色不同。
恰有 $A_{i-2},A_{i+2},B_i$ 三列使它們同色。因此對**任何**原圖，

\[
a'=a\mathbin{\&}\bigl(31\mathbin{\oplus}(2^{(i-2)\bmod5}+2^{(i+2)\bmod5})\bigr),
\qquad
b'=b\mathbin{\&}(31\mathbin{\oplus}2^i).
\]

這個公式直接由 Σ 決定結果，不必讀內部圖。例：裸 C5 的 `1023` 加 $b_0b_2$
（$i=1$）得到 `1016`。公式保證染色關係的正確性；加入該弦能否保原 disk 嵌入仍另核。
刪弦沒有相同的反向清位公式：原 Σ 已遺失那些被弦拒絕的列是否能延拓的資訊。

### 6.3 反例：相同 Σ 與相同翻邊仍可有不同結果

固定同一 C5 及內點 $x=v_5$。兩張來源的框外邊分別如下：

| 來源 | C5 以外全部邊 | 原 Σ | 共同操作 | 結果 Σ |
| --- | --- | ---: | --- | ---: |
| A | $b_0x,b_2b_4,b_2x,b_4x$ | 431 | $-b_2b_4+b_3x$ | 639 |
| B | $b_1x,b_2b_4,b_2x,b_4x$ | 431 | $-b_2b_4+b_3x$ | 987 |

兩圖的原內點都只有三個鄰點，因此任何滿足弦 $b_2b_4$ 的邊界染色都可延伸；
原 Σ 都是 `431`。兩圖都有相同的三角面 $(b_2,b_3,b_4)$、$(b_2,b_4,x)$，
也有相同 $k=1,m=9$ 及具名局部操作。
翻後 $x$ 的四個鄰點分別為 $\{b_0,b_2,b_3,b_4\}$ 與 $\{b_1,b_2,b_3,b_4\}$，
故兩者拒絕不同的四色列，得到不同 Σ。

因此不存在適用所有此類實圖的函數
$f(\Sigma,k,m,\text{具名翻邊與局部面})=\Sigma'$。
對 Σ 作任何確定性重新編碼也無法修復：上述兩個輸入仍會被編成同一個數。

連加入十列**完整延伸數**也不足。另兩張 $k=2,m=12$ 圖有原 Σ `199`，
逐列計數同為 `(4,2,2,0,0,0,2,2,0,0)`；共同面為 $(b_0,b_3,b_4)$、
$(b_0,v_6,b_3)$，同作 $-b_0b_3+b_4v_6$，分別得到 `91`、`255`。
兩圖的全部具名邊及完整 lifts 保存在下述證書，沒有把計數相等當成 fibres 相等。

### 6.4 指定翻邊可用四十位元的局部描述

固定 §2 的共同刪邊圖 $H$ 和具名兩對角線，以 $Q_{ij}$ 編碼 $S_{ij}$ 的十列 support。
則四個 mask

\[
Q=(Q_{00},Q_{01},Q_{10},Q_{11})
\]

足以直接讀出

\[
\Sigma(G)=Q_{10}\mathbin{|}Q_{11},\qquad
\Sigma(G')=Q_{01}\mathbin{|}Q_{11}.
\]

可打包成 $Q_{00}+2^{10}Q_{01}+2^{20}Q_{10}+2^{30}Q_{11}$。
到達 $G'$ 後，若以新對角線為「舊邊」描述同一個反向 flip，共同 $H$ 不變，
新四格就是 $Q^\mathrm{rev}_{ij}=Q_{ji}$：**交換中間兩個十位元區塊**。
這是在補足局部資訊後，翻邊／反向翻邊確實能對應的固定 bit 置換。
§3 的數值是 $(298,394,379,603)$。

四十位元只回答**這一個指定 flip**的關係問題；它不保存 full lifts，也不自動
給出下一條不同翻邊需要的四格。可迭代研究仍須保留實圖及相應共同圖的完整 fibres。
若要直接編碼實圖操作，固定具名頂點及邊宇宙後，邊集 mask $M$ 已有精確更新
$M'=M\mathbin{\oplus}2^{\mathrm{index}(st)}\mathbin{\oplus}2^{\mathrm{index}(uv)}$，
前提是舊邊存在、新邊不存在；facial 合法性與 $M'\mapsto\Sigma(G')$ 仍需另外計算。

### 6.5 編碼與反例的重播

[編碼證據目錄](../artifacts/c5_cell_encoding/BASE.json) 保存本輪輸入 SHA-256；
四份報告保存全部原圖、中間圖、結果圖、rotation、十列完整 lifts 及四格（含空格）。
[獨立 checker](../artifacts/c5_cell_encoding/check.py) 用逐賦色笛卡兒積核對四份報告，
另核對幾何重編碼及全部五條弦對全部 1024 個抽象 mask 的清位公式。
抽象 mask 控制不是宣稱 1024 個 mask 都有 disk 來源。

```bash
python3 artifacts/c5_cell_encoding/check.py
uv run --with networkx==3.5 python scripts/c5_cell_transform.py \
  --check artifacts/c5_cell_encoding/collision-1-708.json
```

實際驗證範圍見[驗證紀錄](../artifacts/c5_cell_encoding/verification.json)。
本節新增 bit 座標、直接的邊界弦規則與兩組具名反例；不新增一般翻邊閉包或 Lean 定理。
