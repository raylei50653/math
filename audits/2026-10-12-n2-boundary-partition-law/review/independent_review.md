# 統一分割與 unary 容量規律的逐量詞核對

2026-10-12。只讀 authority 是 [BASE](../BASE.json) 的十二份凍結輸入。
核對對象是 [canonical 分割報告](../../../docs/c5_excess_two_n2_partition_rule.md)、
[paper 分割報告](../paper/REPORT.md)及另一作者的
[unary 容量報告](REPORT.md)。本 reviewer 是原 paper 分割報告的作者；
對 P／C／D 作重新逐量詞核對，對另一作者的 unary 新證明作獨立邏輯審查，
不把同一作者的重讀冒稱第二份獨立證明。

**採納結論：** P／C／D、26／7 quotient、同列 full-lift join、共同弧幾何、
U-USED-ONE、N2-U-TWO及 N2-UL-LOW 的論證成立，範圍如下。
canonical 若加入後續推論，必保留來源契約及 general N2／E-ARC2 OPEN。

## 1. 分割與 complete fibres

P 的量詞是同一原 piece、同一具名實際接口、同一原邊。相等分割完全相同才有
已用色間雙射；擴張到四色置換後逐座標作用於全部原 tuple。反置換證滿射，
故保存空 fibres 和完整集合，沒有用 fibre 大小替代 tuples。固定字面 root pins
確實被該置換固定；額外未用 anchors 必須加入分割才可要求固定。

C 的 strict slack 論證成立：原 degree 四使 `|L(v)|≥d_C(v)`；外鄰同色使一點嚴格。
以該點為 spanning-tree root，遠到近染色，非 root 有未染 parent；root 的 list
比全部內鄰數大。輸出是整份原 C 的 lift。這是既有 slack 的分割表述，沒有新增
外部定理或把必要拒絕 filter 當充分條件。`K_C` 是輔助記錄，沒有向來源加邊。

D 只使用 actual support 恰為連續三點及未用 pin 色。proper 框強制兩種 endpoint
分割，故兩個 diagonal bits 給 `∅ / Eq / Diff / I`，任意 k／大小成立。
沒有證高 k 排除 `I`。支援四／五點不適用兩位元，仍須用 P 的完整接口分割。

26／7 counts 重新直接計算：Eq 支援 `010` 的 mixed ordered pins 有 10 個相等
分割，Diff `012` 有16；unary 分別3及4。代表置換重建全部 ordered tuples，
ambient 非 owner 維度仍保留等值副本；沒有把26格聲稱為所有 piece 的同一 relation。

## 2. 同列接回與共同弧幾何

G 的 piece 頂點互斥，跨 piece 所有原邊只通過保留的原 B／roots。
固定同一 `q_i,x,y` 後，external factor 加各原完整 fibre 的 join 正好是全圖 fibre，
兩個方向都逐原邊成立。每份代表可以先 transport 到這份共同目標 cell，
不能把不同列或 independently normalized pins 拼成 coloring。

兩份 edge-disjoint 長2弧的原五點次序是 `a,b,h,c,d`，剩餘邊 `da`。
Eq／Eq 會使 `a=h=d`，直接違反原剩餘邊，所以 Eq sets 不相交，無需五份弧對證明。
混類 mask 的 escape 選 Diff-mask 弧的一份 Eq 列，另一弧此列必 Diff，
兩份原 fibres 都接受。這是任意 k 的**條件定理**，沒有假设高 k 都只有 Eq／Diff。
Diff／Diff 對所有 proper 三色框的共同未用色 diagonal 都失敗，亦正確。

## 3. U-USED-ONE 的獨立核對

採用已凍結 source-derived 局部前提：連通 unary、原 degree 四、`2≤k≤3`、
bridge／odd-cycle cactus、每 leaf block 有私有 contact、每 odd-cycle 至多一個
普通私有點、兩個相鄰框附件上限、actual support 至少三點。所有 contacts 只有同一
原 owner，不是將 mixed 的兩個 owner 合併後推回來源。

任一 odd cycle 的每個 cutpoint 外分支可取一份原 leaf block 的私有 contact。
不同 cutpoints 的外分支互斥；再加環的私有 contacts及至多一個普通私有點，
得 `|cycle|≤1+k≤4`，所以是 triangle。這步獨立於 root pin。

若同一 proper 三色列有兩個不同 used colors `a,b` 同為 forbidden，C 的 strict
slack contrapositive 使每份 owner contact 的全部框鄰色避開 `a,b`，只能是第三色。
leaf bridge contact 按 degree 四有兩個相鄰框鄰，二色互異，故不可能。
leaf triangle 若一 contact、一普通私有點，ordinary 的兩色 list 不隨 pin 改變，
而 contact lists 在 pin `a,b` 下不同，不能同時等於原 block palette。
每份剩餘 leaf triangle 因而至少耗兩個私有 contacts；多block 至少兩 leaves，
需 `k≥4`。single block 的 singleton／bridge 亦不成立；single triangle 的 ordinary
私有點同理排除，全contact則框附件全落第三色 class，proper C5 該 class 至多兩點，
與 support 至少三點矛盾。這完成所有大小的 block tree 論證。

所以 `|F_U(q)∩q(B)|≤1` 成立；它不說 used color 永不 forbidden，也不說 local U
一定有一列 `F_U=∅`。證明只比較同一列兩個 owner pins，没有跨列 palette 合併。

## 4. 來源容量接回：k_U=2 與七模板共同排除

凍結完整 source 共同容量等式在每個 `i∈I` 給
`0≤k_U−|F_U(q_i)|≤1`。兩側 external E 非空的既有結論確保容量欄可用；
這是來源 law，不能用到任意 local motif。

若 `k_U=3`，每列 `|F_U|≥2`；U-USED-ONE 迫每列的唯一 unused `D` forbidden。
這與已採納同一原 U 的三列 D escape 直接矛盾。故 `k_U=2`，不限 U 的大小或三點弧。
沒有把三列容量費用相加，也沒有重用跨列 witness。

在 `(1,1)` 若 long `k_L≤3`，低接點 long 有指定列 D escape。
如果 U 的 mask 空，直接在該列 join。否则 U 的 `k=2` 加已有任意大小
M-LOW-ARC 窮盡，迫 U 是原 single bridge，兩 ends 接弧兩條不同框邊。
任一 `Diff(A)` 列，其 used owner color必碰某 contact 框鄰而有 slack lift；
unused `D` 則兩端的 missing-used singleton colors 不同，可直接染 bridge。
所以此列四個 owner colors 全接受。原 `G−U` 該列的完整 lift 可原樣補回 U，
與拒絕矛盾。這共同排除七模板，不是七個專門證明。

## 5. 更窄剩餘 corollary

以下 corollary 亦通過核對：一般 `(1,1)` 的來源如果 `M_U≠∅`，仍由 k_U=2 及
M-LOW-ARC 迫 U bridge，上一段 `F_U=∅` 的 Diff 列接回與 long k 無關，故不可能。
剩餘必有

\[
k_U=2,\quad M_U=\varnothing,\quad M_L=I,\quad k_L\ge4.
\]

原因是每指定列都已 U／short 接受 `(D,D)`；全圖拒絕迫同列 long 拒絕。
M-LOW-ARC 又排 long≤3。共同容量的 `|F_U|≥1`、D 全接受與 U-USED-ONE 合成
每指定列 `F_U` 是一個 used color 的 singleton。
該 singleton 必在 `q_i(A_U)`：若某全框 used 色沒有出现在 local support，可交換它
與 D，固定全部原 support，其 complete owner fibre與 D fibre雙射，不能一空一非空。

这只是必要 residual，沒有來源實現、parent closure 或任意高接點 long 排除。

## 6. 有限反控制與 evidence 界線

另獨立以直接 `4^5` 全 tuple 窮舉核回 frozen tailtriangle entry34：
四個 owner pin 的 fibre counts 分別
`q0=(0,8,16,4)`、`q1=(0,8,16,4)`、`q3=(8,4,0,0)`；
tuple 集合與 [equal-pin probe](equal_pin_full_probe.json) 逐份相同。
此例证明 local `F_U=∅` 每列存在的更強說法不能只由那些局部前提推出。
它不反駁 full disk source 版本，因为 unary interpretation 有原 K5 minor；
詳見 [stronger-lemma note](stronger_lemma.md)。它亦違反 full source 容量。

初等紙面證明承擔無界結論；有限重算只校準保存的控制。完整 target 來源仍
`not triggered`。沒有新 Lean theorem，沒有 N1／相鄰／單-root外推，
完整原55、N2及 E-ARC2保留 OPEN。
