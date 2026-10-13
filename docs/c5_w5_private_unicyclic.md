# 最小來源 W5 的私人圈秩至少二

2026-10-13 後續：[圈秩三兩分支排除](c5_w5_private_rank3_contractible.md)接既有結果，
任取合法全內部 W5 的完整最小來源私人圈秩至少四；一般縮減仍 OPEN。
下文保留原單環研究及其後續雙環排除的日期語境。

**後續（2026-10-13，BASE 243a125）**：[私人雙環排除](c5_w5_private_rank2.md)
已覆蓋圈秩二的四型及全部 essential 位置，將完整最小來源的私人圈秩提高至至少三。
四個實際 annulus 代表只保完整 Σ、不保 R³；下文保留原單環證明與當輪停止點。

2026-10-13。接續 [三色支援與私人森林排除](c5_w5_three_color_support.md)。
完整來源、紙面分類及可重播證據見
[隔離 REPORT](../audits/2026-10-13-w5-private-unicyclic-3097ef5/REPORT.md)，
BASE 為 `3097ef5be241b7777451a5ef8a663f3987d6b866`。
後續發布核對與原證據保存見[整理紀錄](history/2026-10-13-c8-w5-n2-publish.md)；
下文「未commit／push」保留本地研究完成截點。

**在全部目錄外 disk-C5 圖中先最小化內點、再最大化邊數的完整來源前提下，
任取合法全內部 induced W5，其私人誘導圖的圈秩至少二。**
本定理不假設私人圖連通，不加入 edge-critical、N2、ε 或 Gallai 前提。
一般私人含環代表存在與 K∞=K≤5 仍 OPEN。

## 1. 來源與任意大小結構化約

沿用 [共面正規形](c5_cofacial_normal_form.md)、[完整度數界](c5_saturation_degree_bound.md)
及 [全內部五輪](c5_degree5_link_reductions.md) 的精確前提：原外框 B、原全內部
五輪中心 v 及其循環鄰點 U，十 pins 互異，U 內恰為中心與五個三角面。
令 P=V(G)\(B∪U∪{v})、r=|P|=k−6≥7、F=G[P]。
原內點的完整 G-degree≥5；這不是私人 degree≥5。

反設 ρ(F)=1，c 為包括孤立點的私人分量數。附件界先排孤立點；
唯一單環分量可以帶任意根樹，其餘可以是任意樹分量。
令 p 為 B–U 邊數、a 為全 terminal 面數、h 為全私人三角面數、M 為 BUP 面數。
從全部原面與完整度數重算得

\[
M=2(c-1+h),\quad p=a+c-1+h,\quad r\le11-c-p.
\]

**Contractible 分支完全排除。** 唯一環內無 B/U，內側樹葉的完整 degree
迫圈內為空，三角化再迫唯一環是 facial triangle，h=1。其三根各由本身或
原附樹的葉供應一份不同 M 面；其他 c−1 棵樹各至少兩份。因此
`M≥3+2(c−1)>2c`，與面式矛盾。此分支是任意大小的純紙面排除。

**環繞 U 分支完整化成純環。** Jordan 分隔給 p=h=0，故 a=0、c=1、M=0；
私人附枝的葉會迫 M 面，故也不存在。私人圖恰是 C_r，7≤r≤10。
兩側 attachments 每步為 `(1,0),(0,1),(1,1)`，各原環恰前進五次，字母數
為 `(r−5,r−5,10−r)`。全部必要 linear words 是 210+560+630+252=1,652。
紙面證明先確立模板完備，沒有以有限搜尋上限取代無界論證。

## 2. 完整染色核心與合法代表

每個模板均交付原邊、定向面、rotation、pin map、全部十列×1024 cells 及 full lifts。
主、獨立程式重算均得 **全部 1,652 個 capped Σ=1023**，與目錄外身份矛盾。
因此 ρ≠1；再接既有私人森林排除，得任意合法 W5 的 **ρ≥2**。
兩層使用同一私人環指派，計算直接枚舉全 A/G，未拼接獨立 marginals。

這份 essential 必要域另有只保完整 Σ 的合法 prism annulus 代表：原 B/U
兩環加五條對應跨環邊，無私人點；指定 B 外面與 U 空面後補中心。
紙面 list 染色證明它接受每個 beta。故 r=7,…,10 可變 r′=0，
k=13,…,16 變 k′=6，減少 7–10 個內點。嚴格縮減本已足夠，不必要求 r′≤6。

此搬運保 B，容許 U 與中心色改变，**只保 `pr_B R³`，不保 R³**。
必要模板與 prism 的實際不同 R³ cell 已保存；沒有把相同 Σ 提升為十 pin
染色對照。代表不必保持來源的 degree、三角化或私人含環性。
[代表完整證明及槽位資料](../audits/2026-10-13-w5-private-unicyclic-3097ef5/structure/REPRESENTATIVE.md)

## 3. 驗證及精確停止點

新核心核對 16,916,480 cells、16,448,400 空格、657,580 A／320,840 G lifts。
normal／seed17 完整數學產物一致；獨立固定次序 DFS 與主 MRV DFS 逐份相等。
三種破損證書——漏必要 full lift、改原邊、反 U 面——各被兩套 checker 拒絕。
另有同 Σ 異 R³、同 R³ 異 fibre 重數、較弱前提的兩種單環圖及完整 degree 防錯控制。
既有森林 70 模板與保存強度結果只讀回歸通過。

```bash
python3 -B audits/2026-10-13-w5-private-unicyclic-3097ef5/controls/check.py --check
python3 -B audits/2026-10-13-w5-private-unicyclic-3097ef5/independent/check.py
python3 -B audits/2026-10-13-w5-private-unicyclic-3097ef5/controls/strength.py --check
```

真正最小 933／941 來源是 **not triggered**。來源排除来自紙面完備化約及
有限核心，不来自零觸發。上游外部計數信任邊界不變；沒有新增 Lean theorem。
剩餘來源的私人圈秩至少二；其一般嚴格縮減、r≤6 代表、R³ 代表及 K∞=K≤5
均未證。本輪僅本地採納，未 commit／push。
