# W5 小代表：最弱保存契約與合法替換

2026-10-13。Git BASE `6cafdfb02fe5892a49eee21f92aea2369a25c022`；權威輸入為
[BASE](BASE.json) 列出的本輪起始 working bytes，包括既有尚未提交的 K15 文件。
入口：[W5 三色支援](../../docs/c5_w5_three_color_support.md)。目前停止點由
[Kempe 導覽](../../docs/c5_kempe_guide.md#3-停止點與保留缺口)維護。

**本輪完成精確保存契約、102 份合法小代表與兩族任意大小的嚴格替換。
一般 `r′≤9` 代表的存在性仍 OPEN；真正最小目錄外來源沒有被這些構造替換。**

## 1. 同一槽位的幾何契約

固定色集 $C=\{0,1,2,3\}$。原 pins $B=(b_0,\ldots,b_4)$、
$U=(u_0,\ldots,u_4)$ 十點互異，各誘導有序 C5。來源與代表 $A,A′$
均為有限簡單、連通的 plane annulus 圖，指定 B 為外面、U 為空內面。
兩圈的具名次序、方向、內外側、外部接入槽位須共同對齊；全部私人點在環帶中。
來源與代表各自保存原邊、定向面、rotation、ownership 與完整 fibres 的證據。
整個環帶替換可以改變其中的邊，來源原邊的證據不因此覆寫。

在各自的 U 空面放中心 v，恰接五條 $vu_i$，得 $G,G′$。中心無其他鄰點
或額外禁色。待保環境只沿 B 接入。若環境還限制 U 或 v，須擴大介面，不能
只用以下 B 投影契約。代表無須是 near-triangulation、二連通或內點最小度五；
本輪允許面步行中的橋與重複頂點。原來源專用的最小性前提不施加於代表。

## 2. 最弱精確保存條件及完整 Σ 證明

在同一 literal 色框令 $J_A(\beta,\tau)$ 為 A 的所有完整 proper 染色，
其 B/U 色列恰為 $(\beta,\tau)$，並令

\[
R_A^3=\{(\beta,\tau):J_A(\beta,\tau)\ne\varnothing,
                         |\operatorname{im}\tau|=3\}.
\]

U 是奇五環，proper 染色至少三色；能補中心恰好是三色，此時 v 的色唯一。
因此有逐列完整 lift 分解

\[
\mathcal C_G(\beta)\cong
\bigsqcup_{\tau:\,|\operatorname{im}\tau|=3}J_A(\beta,\tau),
\qquad \Sigma(G)=\operatorname{pr}_B R_A^3.
\]

故本目標的**充要條件**為

\[
\boxed{\forall\beta\quad
 (\exists\tau\; (\beta,\tau)\in R_A^3)
 \iff (\exists\tau′\; (\beta,\tau′)\in R_{A′}^3).}
\]

兩側可以使用不同 U 色列及不同中心色。這也等價於在每份非空 B fibre 間有
保全部 B pins 的雙向 total full-lift 搬運：各選一份完整目標 lift 即給兩向函數；
空 fibre 使用空函數。沿 B 接入的外部完整 lift 保留原 β，再接同列目標完整 lift，
所有外接邊仍 proper。反向同理，證明替換後完整外框 Σ 相等。

若額外要求每個 U pin 及中心色也保持，精確條件為 $R_A^3=R_{A′}^3$：
每個共同非空 $(\beta,\tau)$ cell 選完整目標 lift，中心取同一缺色。
這個較強條件仍不要求 fibre 雙射、完整染色數量相等、私人 assignment 可逆或
四色 U support 相等。全十列、每列全部 1,024 cells 包括空 fibres 都保留；
十列涵蓋所有 240 個 literal proper β 時，須對整份 lift 使用同一次 S4 換色。
完整論證及局部刪點／patch／私人共面合併的充分條件見
[保存契約報告](contract/REPORT.md)。

使用者所述「染色數」若指 chromatic number χ，也不要求 χ(A)=χ(A′)。
完整 capped Σ 的目標只查固定四色色集內的外框延拓；§5 另給 χ(A₁)=3、
χ(T)=4 而 capped Σ 相等的實際反控制。χ 與完整染色數量分開記錄。

## 3. K15 前提與九點門檻

本訊息沒有附截圖圖檔；本輪對回截圖所述等式的
[K15 權威入口](../../docs/c5_k15_sphere.md)與原完整報告，而非聲稱已讀圖片。
其結論是一般有限簡單 ordered-C5 disk 圖（允許內側 B chords）的

\[
K_{\le15}=K_{\le5}=K132.
\]

connected、chordless、內面三角化及 degree 下界，是全域最小目錄外反例的
導出性質，並非有界定理要求每份輸入具有的性質。主程式及獨立全染色程序
normal／seed17 四重只讀重播一致：192 份球面嵌入、2,714 根圖、27,140 列、
624,617 完整 lifts，全部完整 Σ=1023。未重跑 plantri 的大生成；沿用其原完整
生成紀錄及外部完備性定理。詳見 [K15 前提審閱及 receipts](k15/REVIEW.md)。

合法 A′ 有五個 U 內點、中心一點、私人 $r′$ 點，故 $k′=6+r′$。在已證
完整 Σ 相等之後，$r′\le9\Rightarrow k′\le15\Rightarrow\Sigma(G)\in K132$。
對真正全域最小目錄外來源，K15 已給 $k\ge16,r\ge10$，九點代表會自動嚴格
縮小並排除該來源。對一般來源，仍須分別核對 $r′<r$。另一條有效路線是任意
$r′<r$ 的合法同 Σ 代表，無須九點上界；它直接違反全域最小內點性。

## 4. 102 份實際代表：已認出的關係有 r′≤5

**定理。** 任一合法 induced-B 環帶 A，若補中心後完整 Σ 已屬 K132，則有
同槽位合法 A′，私人 $r′\le5$，補中心後 $k′\le11$，且完整 Σ 相等。

先證小 witness 的 B 自動 induced。對 G 的每個 B 非鄰對 a,b，在實際外面
畫弧識別兩點；因 ab 不存在，商圖原邊不產生 loop，平行邊可簡化，仍平面。
四色定理給商圖染色，搬回 G 得一份完整染色 a=b。因此任何同 Σ 的 disk witness
不能含 B chord ab，否則它會拒絕此原 β。各非鄰對分別應用這個論證即可。
此處明列依賴既有四色定理，不以它代替有限來源搜尋或染色核對。

取目錄內的至多五內點 witness H。在一個 incident b0 的原有界面 F 內放新 U，
恰加橋 $b_0u_0$，空 U 面再補中心。若 F 的定向面步行含 `(...,b0,x,...)`，
替成 `(...,b0,u0,u4,u3,u2,u1,u0,b0,x,...)` 並加入 U 面。
橋兩方向及全部原 darts 明確出現；中心把 U 面分成五個三角面。
所得 A′ 的私人點就是 H 的內點，B/U 誘導、次序及空槽位都合法。

任何目標 capped lift 限制到 H，故 Σ 只可能縮小。反向任一完整 H lift 可取
三色 U 色列，令 $u_0\ne b_0$，中心取唯一缺色；全圖只有此一跨部件橋，
必得完整目標 lift。所以

\[
\boxed{\Sigma(A′+v)=\Sigma(H)=\Sigma(A+v),\qquad r′\le5.}
\]

凍結的 132 個 stored witnesses 中 102 個 B 無弦；上述論證也證明其餘 30 個
有弦關係不可能由 induced-B disk 實現。對全部 102 個實際構造，私人點分布為
`r′=0,1,2,3,4,5` 對應 `1,6,20,30,25,20` 個關係。
面、rotation、完整 fibres 與雙向搬運見
[構造報告](construction/REPORT.md)和 [完整證書](construction/certificate.json.gz)。
這是已認出完整關係的構造定理，不能先假設目錄外來源也有這份 H。

## 5. 兩族真正嚴格縮小且只保 Σ 的合法替換

**Decorated prism → triangulated prism。** Prism 有十條圈邊與五條 $b_i u_i$。
在 `(b0,b1,u1,u0)` 四邊面插 x1 接 b0,b1,u1，再任意多次在實際三角面插入
接面三點的私人點，得 A_m，$m\ge1$。首次至少有一色可延拓，後續新點各取
唯一缺色，故 A_m 的全部 B/U support 與 prism 相同。
目標 T 在每個 prism 四邊面加入對角邊 $b_i u_{i+1}$，沒有私人點。
[contract 表中的十個 literal 全染色見證](contract/REPORT.md)
證明 T 補中心後全收十列，從而

\[
\Sigma(A_m+v)=\Sigma(T+v)=1023,\quad r=m\to0,\quad k=6+m\to6.
\]

實際 $m=10$ 控制為內點 $16\to6$，完整 capped lifts 為 $485\to20$。
原 β=`01012`、τ=`10103` 的 source cell 非空，target 因新邊 $b_0u_1$ 拒絕，
所以 R³ 不相等，完整 Σ 仍相等。新目標本身二連通且環帶三角化；此族不依賴橋。

另外 m=1 就有**環帶染色數 χ 不同**的嚴格替換。來源 A₁ 的 literal 染色為
β=`01012`、τ=`20101`、x₁=2，所有原邊 proper，恰用三色；B 是奇圈，故
χ(A₁)=3。若目標 T 用三色，它每個四邊面的兩個三角形共邊
`b_i u_(i+1)`，迫 `u_i=b_(i+1)`；對角邊又迫 `b_i≠b_(i+2)`。
於是 B 的五點兩兩異色，不可能只用三色。既有全染色表提供四色 lift，故
χ(T)=4。因此 A₁→T 私人 `1→0`、capped 内點 `7→6`、完整 Σ 相等，
χ 卻 `3→4`。這不要求補中心後 χ 不同：兩個 capped 圖都含 W5，均需四色。

**自由 W5 接入路徑 → 單橋。** 將 §4 的橋換成長 $L\ge2$ 路徑，私人點增
$L-1$。四個色可延拓任意指定兩端色，因此每份完整 H lift 都能接上 capped W5；
縮回單橋後仍完整 Σ=Σ(H)，私人 $p+L-1\to p$。L=2 時來源允許 $b_0=u_0$，
目標拒絕這些 cells，故 R³ 改變。兩個完整控制為 `mask1023:r1→0`、
`mask127:r6→5`；任意長的證明也給實際 `mask127:r10→5,k16→11`，後者不是
額外完整枚舉控制。

兩族均有可移除的低度私人點，不符合真正最小來源的 degree≥5 及小分隔環
限制；該身份均為 **not triggered**。這些是合法嚴格替換存在的具體圖族，
不構成目錄外來源排除。

## 6. 為何一般九點代表仍是主缺口

採用 K15、四色定理與既有最小來源正規形，在本輪允許合法橋面的環帶類中，
下列普遍命題等價：

1. 每份合法環帶都有保完整 capped Σ 的 $r′\le9$ 代表。
2. 每份合法環帶都有保完整 capped Σ 的 $r′\le5$ 代表。
3. 一般 disk-C5 完整關係皆屬 K132，即 $K_\infty=K_{\le5}$。

3⇒2 是 §4；2⇒1 直接。1⇒3：若一般目錄外來源存在，既有正規形提供連通
induced-B 的最小來源 D。在 D 的有界面插入自由 W5 與單橋，完整 Σ 仍為
Σ(D)，得本類環帶。由 1 找九點代表，補中心後至多十五內點；K15 迫其 Σ∈K132，
與 Σ(D) 目錄外矛盾。沒有從有限零觸發或 102 個控制推出普遍量詞。

因此本輪沒有證明上述任何普遍命題。真正最小來源私人圈秩≥5的任意縮減、
一般九點代表、保 R³ 的一般代表、933／941 任意大小排除與主命題仍 OPEN。
新的等價性是紙面歸約，新增的構造閉合範圍是 §4、§5 所列圖類。

## 7. 實際重播、獨立核對與證據層

主構造完整保留 1,044,480 個 annulus cells、1,545 H lifts、278,100 A lifts、
139,050 capped lifts。Prism 控制另有六張完整 fibre 表、61,440 cells，保留所有
空格及 B-preserving 雙向 total transports。主程式 normal／seed17 已重播。
獨立程式不 import producer 或圖庫，從 raw rotation 逐 dart 重建全部原面，再用
propagated-domain／MRV 全搜尋逐字比對全部 graph lifts，含每個空 fibre。

```bash
uv run --with networkx==3.5 python -B audits/2026-10-13-w5-small-representatives-6cafdfb/construction/check.py --check
python3 -B audits/2026-10-13-w5-small-representatives-6cafdfb/contract/check.py --check
python3 -B audits/2026-10-13-w5-small-representatives-6cafdfb/review/independent.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-w5-small-representatives-6cafdfb/review/independent.py
python3 -B audits/2026-10-13-w5-small-representatives-6cafdfb/review/negative.py
python3 -B audits/2026-10-13-w5-small-representatives-6cafdfb/review/chromatic.py
```

實際結果、七種破損證書拒絕、input drift 核對及文件檢查保存於
[本包 verification](verification.json)／logs；各子包亦保留自己的初次 receipts，
當時的 independent pending 由父包 [validation-v2](review/validation-v2.json) 完成。
χ 控制另直接枚舉完整三色圖：A₁ 固定 b0=0 時有 38 份、T 零份，並保存兩側
explicit 三／四色全染色見證。條件等價及幾何的
[最終紙面審閱](review/FINAL_PAPER_REVIEW.md)為 PASS。
正式 docs DocGraph 與文件連結核對通過；全工作樹 DocGraph 仍有既有歷史副本
duplicate-id 錯誤，單獨保留結果，不稱全工作樹通過。
新的全尺寸構造、充要契約及條件等價是紙面證明；
finite controls 是 triggered and holds，真正目錄外最小來源是 not triggered；
四色定理、K15 及其上游外部信任各自沿用，不是本輪重證。沒有新增 Lean theorem，
也沒有把既有 Lean build 當成本輪新證明。未 commit／push，舊證書沒有修改。

文件接入只更新 W5 三色支援入口、Kempe 導覽的 W5 行／停止點，以及 STATUS
對應索引。父 W5 商圖與 degree-5 入口 reviewed-unchanged：原 full-lift 重建及
一般縮減 OPEN 的說法仍成立；cofacial 主命題依然 OPEN，HANDOFF 研究線標記與
README 入口無需因本輪改變。Propagation stop：L2，沒有新的全域來源排除。
