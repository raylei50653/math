# r 六度與低 p/q 的共同 fibre，以及高 h 來源排除

2026-10-14。凍結 BASE `3953c85e334b96533e44652df065640f5463715a`，
在獨立 detached worktree 研究。完整來源與 SHA256 見 [INPUTS](INPUTS.json)。

**本輪得到兩項新結論：r=6,p=5 時原 ell-v、ell-w 都是非邊；固定三個
原框點四度的分支中，k≤27 已迫 h≤12。** 第一項仍未排除整個 r6p5，
第二項排除原 h=18 極端格，並一併排除 k≤27 的 h=13…17。
一般 `K≤22=K≤5=K132`、最小來源 `k≥23`、高 p,q 條件 `k≥28` 均不變。

## 1. 同一來源及證據範圍

G 在全部完整 C5 關係不屬 K132 的合法 disk 中先取最小內點數 k、再取最多
邊數。原框共同對齊 `B=(x,y,a,b,c)`，完整關係為 932／933／941，且
`d_G(x)=d_G(y)=d_G(b)=4`。五個原 apex 依序是 r,t,p,q,s。
所有 degree 都指原 G；保留原 rotation、附件、完整 fibres 及全部同份接回色。

| 攻線 | 新結果 | 證明／停止點 |
| --- | --- | --- |
| 第一優先：r6p5 的同圖兩面 | ell-v、ell-w 原非邊；兩份指定完整 fibre 聯集分別非空 | [共同 W 證明](r6/PROOF.md)；整個 r6p5 與反射仍 OPEN |
| 第二優先：h=18 極端 | 原 collar 無弦，私人圖連通、無葉且圈秩≥2；`k≥ceil((3h+16)/2)`，所以 k≤27⇒h≤12 | [原圖幾何與計數證明](h18/PROOF.md)；不需要交集兩個刪點圖的 masks |

這兩項都是任意大小原來源上的紙面條件式推論；有限 checker 僅核對局部色算術
與整數等式。沒有新增來源實現、外部圖枚舉、4CT 前提或 Lean theorem。

## 2. r6p5：同一 W 的兩個合法商圖

保留原 link `N_G(r)=(x,y,t,w,v,s)`、`N_G(p)=(a,b,q,ell,m)`。
既有 p5⇒a≥6 及所有指定非邊使

`W=R−{r,p}`

有兩個僅共享 z 的實際面 `(z,s,v,w,t)`、`(z,q,ell,m)`。
在兩面內同時識別 s=w、z=ell；兩條弧不交叉，兩個識別類都是原非邊。
商圖加薄 C5 cap 後只有 k−5 個內點，全域最小性供應一份完整 W 染色。
z=ell 保證至少一個 p lift 到原 U；U 的完整支持319與 s=w 迫外列 ABABC，
所以同份染色有 ell=v，從而原 ell-v 必不存在。

另作 v=t、z=ell 的合法商圖，319 迫 ABCAC，得到 ell=w 及原 ell-w 非邊。
兩個商圖供應的是兩份分別存在的完整染色；不能合併等式。

八接點順序固定為 `(z,s,v,w,t,q,ell,m)`，更精確地：

| 商圖等式 | 非空的完整 fibre 聯集 | 該份染色的全部 cap lifts |
| --- | --- | --- |
| s=w、z=ell | ABABCBAD 或 ABABCCAD | r=m=D；pq=CB 或 BC；xy=CB |
| v=t、z=ell | ABCACBAD 或 ABCACCAD | r=m=D；pq=CB 或 BC；xy=CB |

每行只斷言聯集非空，不斷言其兩個個別 fibre 都非空。原 mv、mw、ms、mt，
以及 ell-s、ell-t、ell-r 非邊全部保留。反射整份來源得到 r6q5 的對應結論。

新的非邊使 `{z,v,ell}`、`{z,w,ell}` 三點商圖合法，但每個仍有16個局部必要列。
再加另一條交叉對角線無法由原面內不交叉弧實現，因此停止這個指定商圖探索。
局部存活列不表示真實來源存在，也不宣稱已窮盡所有合法手術。

## 3. h=18：原幾何直接給更強界

令 `alpha=d_G(a)−4`、`gamma=d_G(c)−4`、`h=alpha+gamma`。
原簡單 collar 是

`C=(r,t,A1,…,A_alpha,p,q,C1,…,C_gamma,s)`，長 h+5。

四連通 T0 的 z-link 是 induced cycle；刪去 x,y 後的剩餘路徑沒有弦。
既有 `N_R(z)∩N_R(r)={s,t}` 又排除所有經 r 的額外邊，因此整條原 C 無弦。

令 P 是 C 嚴格內側的全部私人內點，`E=sum_{v∉B}(d_G(v)−5)`，
`E_C=sum_{v∈C}(d_G(v)−5)`。由 Euler，`k=h+6+E`、`|P|=E+1`。
內三角面連通與無弦 C 保證 G[P] 連通。

若 P 有葉點 u，其原 link 中至少四個連續 collar 鄰點的中間兩點必是相鄰
五度 apex。已知 r≥6、a4⇒t≥6、c4⇒s≥6，使唯一可能的相鄰五度對是 p,q。
這迫 u 正是原五度 ell，卻與 p=q=5⇒ell≥6 矛盾。因此私人圖沒有葉點。
原度數界另給 E≥3，故 |P|≥4；若其圈秩恰一，私人圖必為長至少四的單圈，
其空內側無法在沒有額外私人邊的情況下三角化。故私人圈秩 `rho≥2`。

同一原圖的 C–P 邊數恰為 `5+2h+E_C`。逐點計私人 degree 後得到

\[
\boxed{h=2E-E_C-\rho,\qquad 2k=3h+12+E_C+\rho.}
\]

r6 時 r,s,t 各有 excess，故 E_C≥3；r≥7 時 r 自己給 E_C≥2。
因此本固定分支在任意大小皆滿足

\[
\boxed{k\ge\left\lceil\frac{3h+16}{2}\right\rceil},
\qquad \boxed{k\le27\Longrightarrow h\le12}.
\]

原 h=18 極端格甚至不必用連通性：k=27 只有四個私人點；LH／HL 要44條
C–P 邊，而私人 degree 總和只有20；LL 則是43對21，均直接矛盾。
完整推導及各低 p/q、r 子型的不等式見 [證明 §§4–6](h18/PROOF.md)。
956／1012／1020 及反射限制保留在各自刪點圖；本輪無須將它們合併。

## 4. 更新的活躍來源域與剩餘義務

本表與[前輪完整來源表](../2026-10-14-lowpq-source-676b102/classification/SOURCE_TABLE.md)
的全部 degree、旋轉、fibre、原非邊及預算條件取交集；前輪 h 上界由本輪取代。

| k≤27 的固定 x,y,b 四度來源 | 更新後必要域 |
| --- | --- |
| Σ=933 或941 | 4≤h≤12 |
| Σ=932 | 5≤h≤12 |
| p/q | 至少一側恰五度；該側 a/c≥6；雙低另有 ell≥6 |
| r6 | s,t≥6；原 U 完整支持319；低 p/q 另有本輪 ell-v、ell-w 非邊 |
| r≥7 | 保原 mask13 全 lifts、既有低 t/s 與 C6 必要條件，另套新精確計數式 |

仍 OPEN：整個 r6p5、反射側、其餘低 p/q、mask319、一般 r≥7、一般指定
T／T0 延拓與保壞嚴格下降。h≤12 不表示殘格可實現，也不給一般 K≤27。
E-ARC2、C8 RING 與 W5 私人圈秩使用各自原來源；本輪的 P 是原 collar
內側頂點集，不能與 W5 私人圖混用。

## 5. 驗證、文件傳播與交付

[驗證紀錄](VERIFICATION.md)列出實際命令、正常／seed17 重播、負控制及來源 seal。
主色表與不 import 主 checker 的[獨立原邊核算](validation/direct_joint.py)
逐份比對全部210個 proper 色軌道、完整接回與空格；120個必要列不是來源證書。
私人圖拓撲由紙面證明及[獨立審查](review/GEOMETRY.md)支持，有限整數算術不取代它。

Closure scope：本固定分支的 k≤27,h≥13；r6低p/q 中含 ell-v 或 ell-w 的原邊子支。
Updated：本報告、證明與證據，以及隔離工作樹中的 C4 父入口、Kempe 導覽、
STATUS、no4ct 直接入口與 synthesis 對應列。
Reviewed-unchanged：一般 K≤22／k≥23、高 p,q⇒k≥28 的條件域、一般 T／T0、
README／HANDOFF 的路由、外部計算與 Lean 信任邊界。
Propagation stop：只同步直接 consumers 的新來源限制；其他研究線不擴張。
主工作樹及遠端保持原 BASE；本輪未 commit／push。
