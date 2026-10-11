# BR-SD-1c：獨立紙面推導與第一個失敗步驟

日期：2026-10-11。研究 BASE：`fd6e1112e6f5e9fd23c50d2f3b5d2ef874954d69`。
此 worker 在父端 PROOF 尚未交付時，先重推 BR-SD-1a 的同源列表與旁支情況。
其後獨立驗證父端提出的 actual edge-pair support 路線。本文不是來源實現證书。
只在本 worker 目錄寫入；舊 BR-SD-1a／1b、canonical docs 與其他 worker 檔案不修改。

## 1. 同一來源與旁支量詞

保留任務完整 G／M 合同。原 G 是 ordered induced-C5 disk，原非相鄰 roots r/s
完整 degree5，原 U=0、L long、S short 且實際 boundary support 恰一條真框邊兩端。
僅省略原 r-spoke，`X=M=G−e` 自己拒絕同一 literal proper 三色 β，M 的唯一
完整 degree5 root 為 s，每個 C 點完整 M-degree4，`C=H_M−s` 為實際 sole connected component。
完整 Σ、所有原 contacts、原附件、rotation、ownership、逐邊 witnesses、完整 relations／fibres／full lifts
均保留；以下較短論證只取其中明列使用的必要條件。

原 skeleton 為三 odd-cycle blocks J1/J2/J3，`J1∩J2={r}`，J3 與兩者不交，
J2 私有 u 與 J3 私有 v 以原 bridge uv 相接。p/q 的原簡單外臂分別在 a1/a3
接入 J1/J3，長度為任意非負整數。零長臂時 p=a1、q=a3。不假定 a3≠v。
原 s 內鄰仍恰 p/q。

只加入一份在來源中實際具名的 pendant branch W，與原 skeleton 只共用
`x∈J1∪J2`，其他 W 點／邊／附件全取自同一候選原來源，沒有新的 s-contact。
W 不碰 J3 或 q 臂。W 的 blocks、大小及原 B 附件由來源給出，不從抽象 palettes 反造。
W 可有任意有限大小；若拒絕後其 blocks 不是 Gallai blocks，外部刻畫已直接排除。

舊同源 MAPPING 明確識別：刪原 r/s 後，`J1−r` 與 p 臂在 L；
`J2−r`、uv、J3 與 q 臂在 S。接在 J1 的 W 同屬 L，接在 J2 的 W 同屬 S。
這只保持候選身份，並不證明附件／embedding 已有實例。

## 2. 原 degree 的第一層核對

令 δ 為旁支在 x 貢獻的新 C 鄰居數，k(x) 為實際 B 附件數。由完整 degree4：

| x 的位置 | 原 C-degree／s-contact | 必要 degree 上界 |
| --- | --- | --- |
| r | 4／否 | δ≥1 已矛盾，故不得接在 r |
| J1 的 a1，零 p 臂 | 2／是 | δ≤1 |
| J1 的 a1，正 p 臂 | 3／否 | δ≤1 |
| J1 其他私有點 | 2／否 | δ≤2 |
| J2 的 u | 3／否 | δ≤1 |
| J2 其他私有點 | 2／否 | δ≤2 |

這些只是必要 degree 條件。它們沒有提供 actual attachments、disk rotation、完整 Σ 或來源存在性。
原 r 已飽和，故 r 接新旁支屬結構排除；其他列仍需由候選原合同供完整資料。

對每個實際 v∈C，令 `t(v)=1_{sv∈E(M)}`、`k(v)=|N_B^M(v)|`。
沒有額外內部分量或未計鄰居，因此逐原點有

\[
4=d_M(v)=d_C(v)+k(v)+t(v).
\]

按同一原邊定義

\[
L^D(v)=Col\setminus\left(\beta(N_B^M(v))\cup
(\{D\}\text{ if }t(v)=1\text{ else }\varnothing)\right).
\]

刪去的不同色數至多 k+t，故 `|L^D(v)|≥4−k−t=d_C(v)`，包括 W 全部點。
D 未出現在 β 中，故 s=D 合法於全部原 s–B spokes。若 C 有完整 L^D 著色，
沿全部原邊接上 β 與 s=D 就得同一原 M 的完整著色，違反拒絕。
因此 C 是不可著色的 connected degree assignment。

正式外部依賴為 [Dvořák, Theorem 10 與 blockwise-uniform 定義，p.6](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)。
本 worker 即時重讀作者 PDF 第6頁文字；凍結來源沿用 BR-SD-1a `external/SOURCE.md` 的 hash。
其給出各 block palette S_K、每點 list 的 incident palettes 聯集、相交 blocks 的 palettes 互斥。
Odd-cycle palette 大小2，bridge palette 大小1。這不是 Python 或 Lean 證明。

## 3. Private witnesses：可保留範圍與 triangle 例外

若 W 接在 J2，J1 的 `w1∈J1−{r,a1}` 未受影響，永遠存在。
若 W 接在 J1，J2 的 `w2∈J2−{r,u}` 未受影響，永遠存在。
受影響的 cycle 可改取

\[
w_1∈J_1\setminus\{r,a_1,x\},\qquad
w_2∈J_2\setminus\{r,u,x\}.
\]

當 cycle 長度≥5，最多排除三點，選取必存在；當 x 就是 a1 或 u，最多排除兩點，
triangle 也有剩餘私有點。所選點只屬本環、非 C 割點、非 s-contact，其 list 含 D，
所以本環 palette 含 D。兩環都有這種 witness 時，在 r 的 palette 互斥給矛盾。

原 witness 選取唯一可能失效的形狀：受影響環是 triangle，x 是原來唯一
`J1−{r,a1}` 或 `J2−{r,u}` 的點，旁支使 x 成為 C 割點。
此時 `D∈L^D(x)` 只迫某一個 incident palette 含 D，不能直接迫原環 palette 含 D。

## 4. 未使用 actual pair support 的 palette routing

未受旁支影響的 J3 仍可選 `w3∈J3−{v,a3}`，包括 triangle 及 a3=v。
它非 C 割點、非 s-contact，故 D∈S_J3。

若 J2 的唯一私有 triangle witness 被旁支佔用，x 與 u 不同，u 仍只 incident J2 和 uv。
u 非 s-contact，所以 D∈L(u)。uv palette 不能含 D，因其在 v 與 S_J3 相交須互斥。
因此 D∈S_J2。若 x=u，原 J2 private witness 未失效。所以不論 W 接在何處，J2 palette 仍被迫含 D。

J1 triangle 例外可沿原 p 臂得到部分 route。正長臂設長度 ℓ≥1。
最後 bridge 觸及 s-contact p，其 palette 不含 D。每個內部臂點度2、非 s-contact，
list 含 D；兩 incident singleton palettes 互斥，所以恰一條 incident bridge 含 D。
沿路向 a1 反推：第一橋 palette 不含 D iff ℓ 為奇數。a1 此時非 s-contact，
其 incident blocks 恰 J1 與第一橋，所以正奇數臂長迫 D∈S_J1，與 S_J2 矛盾。
正偶數臂長允許第一橋含 D；零長臂 a1=p 本身是 s-contact，不能用 D-presence。

第一個無效步驟仍是：由 triangle 割點 x 的 D-presence 直接說 D∈S_J1。
例如 abstract palettes `S_J1={A,B}`、`S_W={D}` 可以把 D 分配給 W 的第一橋。
這是 palette-routing 阻礙，沒有稱為 disk source、沒有建立原 Σ 或 embedding。
β-minimality 也不單獨修補該步：連通不可著色 degree assignment 刪任何 C 邊後可由 degree slack
著色，並不自行排除旁支。必須再用原實際附件／support 條件。

## 5. 對原 short-S support 的獨立核查

父端提出沿 S 的原真 edge-pair support 排除 J3/q 臂；本 worker 獨立確認如下。
支援在既有來源語言中指全部原 B 鄰點：例如 `docs/c5_excess_two_mixed_omission.md`
§3 明寫 `S=N_B(C)`；`docs/c5_excess_two_ternary_two_unary.md` §3 明寫 `A_W=N_B(W)`。
N45§2.11 完整採納合同1保留 S actual support 恰真框邊兩端，並非 abstract 包絡。
因此同一原 S 中每個點的 B 鄰居，都在固定實際相鄰框點 h0/h1。

令 A=β(h0)、B'=β(h1)，proper β 與原真框邊迫 A≠B'。
令 T 是 β 使用的第三色，D 是唯一未用色；這是同一 literal Col 內的命名，
不對 J3 或 q 臂獨立正規化。原 J3 與全部原 q 臂都在同一 S，故其 B 鄰色只可能 A/B'。

原 `w3∈J3−{v,a3}` 的 C-degree2、非 s-contact、完整 M-degree4，迫它有恰兩條實際 B 附件。
圖 simple 且 S 只有兩個可能 B 鄰點，因此兩附件必恰 h0/h1。故

\[
L^D(w_3)=\{T,D\},\qquad S_{J_3}=\{T,D\}.
\]

這裡先用实际 full degree 與实际 support 推原 list，再用非割點 palette 等式。
不是先任意放一個二色 palette，再推測附件。

### 5.1 原 q 臂零長

q=a3，原 sq 邊扣去 D，因此 D∉L^D(a3)。但 J3 含 a3，
`S_J3⊆L^D(a3)`，而 D∈S_J3，矛盾。a3=v 時完全相同；不需要 H 二連通。

### 5.2 原 q 臂長度一

令 e=a3q 為唯一原臂 bridge。q 的原 C-degree1、s-contact、完整 M-degree4，
故 k(q)=2，其附件恰 h0/h1。原 list 恰 `L^D(q)={T}`，所以 S_e={T}。
e 與 J3 在 a3 相交，但 S_e∩S_J3={T} 非空，矛盾。

### 5.3 原 q 臂長度至少二

令 z 為從 a3 沿原臂的第一鄰點；z 是內部臂點，不是 q，沒有 s 邊或旁支。
原 C-degree2、完整 M-degree4 迫兩附件恰 h0/h1，故 `L^D(z)={T,D}`。
第一臂 bridge e=a3z 的 palette 是非空 singleton，且 `S_e⊆L^D(z)={T,D}`。
J3 palette 也恰 {T,D}，兩者在 a3 相交卻 palette 必互斥，矛盾。

三種長度無上界且窮盡所有原臂。第一臂 palette 的禁止由实际附件迫出的**整個二色集**負責，
不需要宣稱 D 從 W 或從某 cutpoint 必然路由回 J1。

## 6. 可重用局部引理與結論

**二色 palette／原臂局部障礙。** Connected uncolorable degree assignment 中，
若 odd-cycle K 有一個只屬 K 的點 w，其实际 list 恰 P、|P|=2，則 S_K=P。
若某 K 頂點 a 的 list 缺 P 內一色，立即矛盾。若另一 incident bridge e=az 的
另一端 actual list 包含於 P，則 bridge 的非空 palette 包含於 P，亦與 S_K 互斥矛盾。
引理是 arbitrary finite size；其 source 應用須先從原附件證 actual lists，不准由 abstract lists 反推實現。

本候選一份原 pendant branch 子域完全保留 actual S edge-pair、未動 J3／q 臂，
因此§5的任意大小 source exclusion 成立，不受 J1 triangle 的 private-witness 失效影響。
這是精確 scoped exclusion 的紙面候選；不是 canonical 採納、不提供 actual source、沒有新增 Lean theorem。

任務A路線在一般保留 witnesses 情況可成立；B路線不允許錯用 cutpoint D-presence。
若撤去 actual edge-pair 或改動 J3／q 臂，§5不再覆蓋，§4具名 triangle／偶數臂阻礙必須保留。
一般 Gallai trees、其他三環接線、更多旁支、一般 N45、R31、55、ε≥3及主命題仍不由本文關閉。

本文未新增有限搜尋；任意大小結論由原 degree 計算、actual support 與正式 block palette 刻畫承擔。
Abstract routing fixture 只能標為必要前提的負控制，不能標為原 disk 反例。
Actual target source 沒有供應，來源實現層為 `not triggered`。
