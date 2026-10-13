# 圈秩一交付的最後獨立敵對審閱

審阅 BASE：`3097ef5be241b7777451a5ef8a663f3987d6b866`。
核讀 `structure/STRUCTURE.md`、`controls/check.py`、`independent/check.py`、
主 summary、獨立 normal/seed17 結果，以及 deep-five-wheel 原始 REPORT §§1–4。
本檔不修改主證明、主報告或正式 docs。

**判定：PASS，保留明列上游信任邊界。** 任意大小、多私人分量與原 attachments
已在紙面推導中處理；1652 模板是完備必要域。主／獨立染色結果足以完成
essential 分支排除。無須假設 source edge-critical、N2、ε、Gallai 或私人 degree≥5。

## 1. 來源前提與量詞

來源定義為所有目錄外 disk-C5 圖中最小內點、再最大邊數，而非只在已三角化
或已滿足 degree 條件的子類比較。因而後續代表不必繼承 degree 或飽和性。
本次實際使用的前提是 r≥7、原內面全三角形、B/U induced 且不交、合法原位
wheel cap、每私人點完整 degree≥5、B 附件界與 occupied-C4 排除。

B 附件界已核對上游：若 x 接不相鄰 a,c，短弧 a-b-c 的 C4 cap 清空後，由
三角化迫 bx，從而 b 的完整 degree 三，違反已證 boundary degree≥4。
U 附件界另由 ui-v-uj-x 的 C4 與原 Jordan 槽位推導。它不以 U 是外框為由
直接挪用 B 的論證。私人 leaf 與孤立点的 degree 論證因此合法。

任意被指定的合法全內部 W5 都符合這些條件；後續沒有重選輪的要求。
所以結論可對任取此種 W5 陳述。4CT、普遍 screen、目錄與 K≤12 外部證明
仍是既有來源信任輸入，本次既沒有重播上游大型計算，也沒有新增 Lean 形式化。

## 2. 兩個幾何分支及完備性

Contractible C 內沒有 terminal，任何私人內部樹都會提供沒有 terminal 附件的
leaf，違反完整 degree；C 又不能有 chord。因此 C 為原三角面。三個根各以
自己（沒有附樹）或附樹的 leaf 收取一個不同 M 面；其他樹分量各至少兩個。
這與重算公式 M=2c 矛盾。該收費證明沒有刪枝或默認支援保持。

Essential C 令 p=h=0，重算公式 p=a+c-1 迫 c=1,a=0，再由 M=0 排附枝。
因此全部私人圖就是 C，且 7≤r≤10。其他私人分量、隔離點與附枝都經過明確
排除，不是先假定連通。亦可獨立用 Jordan 檢查：任何 off-cycle leaf 必同時
接 B/U，原 incident edges 將跨 C，矛盾。

兩側 link 的每一步是 (1,0)、(0,1) 或 (1,1)，每條 B/U 原環邊恰在 annulus
側被一次 fan 使用，所以兩個 coordinate sums 精確為五。面方向禁止倒退，
單一 vertex link 與至多兩相鄰 terminal 鄰點禁止跳接；所有原邊由 faces/intervals
重建，Euler 邊數亦恰滿。兩環起點平移與共同方向反轉是完整 embedding map，
不是互相獨立的顏色 normalization。

由此逐 r 的 words 數為 210、560、630、252。主程式以多重集遞迴列詞，
獨立程式以全部三字母 Cartesian product 後按兩個 coordinate sums 過濾，
集合相等比單看數量更強。模板容許違反尚未使用的其他來源前提；這只是必要域
擴大，不削弱排除。

## 3. 完整共同接合與兩套實作

原 C 在兩層中是同一组 vertices 10,...,9+r。主 solver 對整個 A 或 G
同時配置所有原 vertices，沒有計算兩側 marginal 後再拼接。私人 cycle 邊
及兩側 attachments 全在同一 adjacency 中。故每份輸出天然是一個共同 σ。
紙面 J_L Join_σ J_I 公式與 solver 的操作一致，沒有省略的其他私人分量。

主 DFS 每步選一個尚未染色點，列出全部四種 proper 顏色，遞迴分支互斥且
完備；回溯清除該點的色。MRV tie-break 僅改變搜尋次序，不作不安全剪枝。
固定 B 是十個全部 proper S4 代表；由共同 S4 色置換涵蓋 240 literal proper
外框列。improper 外框列在保留的 B-C5 上必拒絕。

G 有實際新中心，主程式獨立直接 DFS，再逐份比較從 A 三色 U fibres 補唯一
缺色的結果。因此沒有僅靠錯誤 support cardinality 判斷 centre acceptance。
每列的全部 1024 U cells（含 improper 與空 cells）均保存。

獨立程式不 import 主程式，改以 neighbor intervals 構邊、固定變數次序直接
對 A/G 搜尋，中心先於私人 cycle 染色。它逐份比較 edges、steps、全部 rows、
完整 lifts 與 Sigma；又從 rotation 沿 darts 重建 faces，而非只信主函數的
planarity 結果。指定 B 外面、U 空內面及補中心五面均核對。

結果檔一致記錄：1652 graphs、16916480 cells、16448400 空 cells、
657580 A full lifts、320840 G full lifts，全部 capped Sigma=1023。
主 mathematical SHA256 為
`2bb83ff21becff13042b4fcefa10085ce3bb1c059fbd6f98470b263a0d91b99a`。
本審阅读取这两套完整运行结果，不把阅码本身冒称为额外独立全域重跑。

## 4. 僅保 capped Sigma 的零私人 prism 代表

這是有限必要核心完成後可採納的附加構造，並非完成排除的必要步驟。
在 canonical 共向 B/U 座標中，A′ 取兩條原 C5 加五條 b_i-u_i，沒有私人點。
其有向面可取

```
B outer: (b0,b4,b3,b2,b1)
annular: (bi,b(i+1),u(i+1),ui), i=0,...,4
U empty: (u0,u1,u2,u3,u4)
```

每條 dart 恰用一次，每點 rotation 是單圈，V-E+F=10-15+7=2。
因此它是具指定 B 外面、U 空內面的有限簡單 annulus。補原位中心與五 spokes
後內點 k′=6。實際來源的代表須經同一 canonical-to-original gB/gU map 搬回；
若原文件以相反邊界面方向記 U，不能直接忽略該 map 連錯 bi-ui。
這保存原 pins、次序、內外側及明列的新附件幾何；舊 annulus 的內部接線由
整區替換改變，並未聲稱新圖繼承原 degree 或三角化。

**每個 proper β 的紙面延伸。** 在 U 上只使用色集 {0,1,2}，令
L_i={0,1,2}\{β_i}。每份 L_i 至少兩色。若某 L_i 有三色，先沿 U−u_i
這條路徑貪婪染色，最後 u_i 避開其兩鄰色，必能完成。若所有 L_i 都兩色，
β 沒有色 3，且 proper β 使相鄰 lists 不同。選一個相鄰 pair L_i≠L_(i−1)，
令 u_i 取 c∈L_i\L_(i−1)，再依環順序貪婪染到 u_(i−1)。最後點的 list
不含首色 c，只須避開前點色，故也能完成。U 奇環的 proper 染色恰使用
三色，中心可取色 3。所有 prism spokes bi-ui proper，故 Σ(A′+v)=1023。

每個必要核心已經完整證得 Σ(A+v)=1023。因此只保 B 的雙向 total 染色搬運
可明確定義：來源→代表依上述 list 演算法；代表→來源依原 graph/template map
以及該 β 的完整已核對非空 fibre 選取首份 full lift，再共同換色搬回。
反向的普遍性依完整 word 覆蓋與完整有限非空證書，不由未證的 list 擴張猜測。
兩方向都輸出完整 proper 染色，保存每個 B pin。無需互逆或保存數量。

得到 `pr_B R_A³=pr_B R_A′³`，`r′=0`，`k′=6<6+r=k`，
內點減少量為 `Δk=r∈{7,8,9,10}`。此可視為整個已分類 essential necessary
kernel 類的非空代表定理；在真正最小目錄外來源上它當然產生矛盾。
Contractible 分支已被結構排除，沒有需要交付的實際代表。

**必須保留的 R³ 邊界。** 這個代表不能宣稱保留 U 染色或中心色。例如首個
必要核心 word `BBDDDUU` 有完整 G lift

```
vertex order: B[0..4], U[5..9], P[10..16], centre[17]
full lift:    010120103123231232
beta:         01012
tau:          01031
```

此 lift 從新完整證書直接讀出；其 tau 用三色，然而 prism 邊 b0u0、b1u1、
b2u2 各同色。因此這個原 R³ cell 在 prism 被拒絕。两圖 capped Sigma 相同，
R³ 確實不同，不只是「尚未證明相等」。這是必要核心弱前提真圖控制，不是最小
933/941 來源反例。

## 5. 採納與停止點

結合 contractible 純紙面排除、essential 完備化約與完整有限核對，可採納：
任意合法全內部 induced W5 的私人圖圈秩不等於一。再接既有私人森林排除，
得 rho(G[P])≥2。這是紙面加有限完備核心的證明；不應寫成新 Lean theorem。

prism 補充結論僅保 capped 完整 Sigma，縮減 7–10 內點。沒有取得新 R³ 代表
定理，也未對圈秩≥2 来源給出 r≤6 代表或 strict reduction。
真正最小 933/941 來源實例 `not triggered`；零触發不是排除原因。
一般私人含環來源縮減及 K∞=K≤5 仍 OPEN。
