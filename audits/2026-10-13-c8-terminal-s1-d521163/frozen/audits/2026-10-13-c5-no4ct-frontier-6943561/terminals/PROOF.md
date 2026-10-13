# 原 C8 的零單接 terminal：W5 原子、六點完整轉移與來源排除

2026-10-13。BASE `6943561e644e7598342d1ccd7df44dac0ebcd5cf`。
本文只使用父包凍結的原來源契約；不使用四色定理，不修改舊證书。

## 1. 同一原圖與適用契約

固定全域最小內點、再最大邊數的目錄外原 C5 disk G。其完整關係為
932／933／941，k≥16；取 h=3 時的同一原有序 induced C8
`C=(c0,…,c7)` 與內側 H，`I=V(H)\C`，`Q=H[I]`，`m=|I|=k−8`。
已接入八份 933／941 h=3 必要來源契約；932 的 h=3 已排除。

原 H 內面三角化、C 點 H-degree≥4、I 點 H-degree≥5；原內部 C3／C4
cap 空，C5 cap 空或 W5。小 cap 使用原內點介面上的
`s_cap≤k−|C_cap|<k`，故僅使用受限 C4 及真正較小的 C5 最小性。
不可把此處的 `s_cap` 與下文單接點數 s 混為一談。

每個 I 點至多接兩個 C 點，雙接相鄰或正對；八條原 C 邊的原面第三點
`t0,…,t7` 全異。無 occupied C3 保證相鄰雙接點精確是這八個 t。
令 s 為單接點數，p 為正對雙接點數，r 為無 C 接點數。
已有任意大小分類：

* p=0：RING，Q 外框 D 是長 `8+s` 的簡單環，允許原 boundary chords。
* p=1：PINCH，兩個 terminal disk 在同一原點 x 相交；兩側外框長
  `5+s_+`、`5+s_-`，`s_++s_-=s`。
* p=2：BRIDGE，兩個 terminal disk 的原接點 x、y 由唯一原 bridge xy
  連接；兩側外框亦長 `5+s_+`、`5+s_-`。

正對點全部接同一原 pair `{c_i,c_(i+4)}`。PINCH／BRIDGE 每個 terminal
各有嚴格內點；否則空 polygon 的兩個耳中至少一個不是 distinguished
endpoint，其完整 Q-degree=2，違反 t 的 Q-degree≥3、單接點 Q-degree≥4。
已有下界 PINCH `m≥11+s`、BRIDGE `m≥12+s`。

上述來源：父包
`frozen/audits/2026-10-13-c8-peeling-6cafdfb/structure/PROOF.md` §§1–4，
及 `frozen/audits/2026-10-13-c5-no4ct-c8-6cafdfb/geometry/PROOF.md` §§1–2。

## 2. 任意大小的零單接 terminal 精確是原 W5

**引理 T0。** 在 PINCH 或 BRIDGE 中，若指定側 `s_side=0`，則該側
terminal disk 精確是以原 endpoint e 及該側四個 t 作 rim 的原 W5。
另一側的大小、單接點數及內部形狀任意。

證明：其外框長五，由原結構分類精確是

`(e,t_i,t_(i+1),t_(i+2),t_(i+3))`，

或另一側的相同原順序。terminal 至少有一個嚴格內點。五個框點都是原
G 的內點，故這是 proper C5 cap，嚴格內點數小於 k；原小 cap 定理使
非空 cap 恰為單中心 W5。故 rim 無 chord，中心 z 接全部五點，除此之外
没有任何該側嚴格內點或邊。此結論不設 m 上限，不從小图控制外推。

特別地，若整體 s=0：PINCH 恰有一個 x、八個 t、兩個中心，故 m=11；
BRIDGE 恰有 x,y、八個 t、兩個中心，故 m=12。這是任意大小的**精確
停止**：該幾何子域沒有較大後繼，不是只搜尋到 m=11／12。

## 3. 原六點 separator 與完整 terminal 原子

選一個滿足 T0 的 terminal。依原 C clockwise 半弧，把介面固定為

`J=(c_i,c_(i+1),c_(i+2),c_(i+3),c_(i+4),e)`，

私人內點固定為 `U=(t_i,t_(i+1),t_(i+2),t_(i+3),z)`。
J 是原 induced 六環：C 無 chord，e 只接半弧兩端。
J 所指定的 terminal 側恰含 U 的五個原點。

原面是四個 `c_j c_(j+1) t_j`、三個中間 C 點的 t-link 面、兩個端點
面，以及 W5 的五個中心面。合計14個原三角面、24條原邊、11個原點；
每個 U 點在此 cap 中 degree=5。所有名字、面側及 endpoint ownership
來自原圖，一次固定；不得在不同色列另選半弧或交換另一側。

對每份 literal J 指派 `a∈{0,1,2,3}^6`，定義

\[
\mathcal W(a)=\{u\in\{0,1,2,3\}^{U}:a\cup u
\text{ 是這份原 cap 的完整 proper colouring}\}.
\]

包括 improper a 和 proper 空 fibres。若記 C 半弧色為 `a0,…,a4`、
endpoint 色為 b、中心色為 q，則每份 full lift 精確滿足

\[
q\ne b,\quad
u_j\notin\{q,a_j,a_{j+1}\}\ (0\le j<4),\quad
u_j\ne u_{j+1}\ (0\le j<3),\quad
b\ne u_0,u_3.                                     \tag{1}
\]

J 自身還須 proper：相鄰 C 色異，b 異於半弧兩端。
式(1)按 q 和四個 t 色枚舉，給全部 lifts；與直接整份 cap 染色一一對應。

對任意大的另一側／外側原圖 E，只在同一具名 J 上交接。則

\[
\mathcal F_G(\beta)=
\bigsqcup_{a\in A^J}\bigl(
\mathcal F_E(\beta,a)\Join_J\mathcal W(a)\bigr).       \tag{2}
\]

這保留原 G 的全部頂點著色和所有空 fibres。PINCH 的 e 在兩側都是同一
原點；BRIDGE 的另一端 y 與原邊 ey 保留在 E，必須檢查 `a(e)≠colour(y)`。
若 E 的介面只取其中一部份，仍須對全部 literal J 色共同求和；不能把
兩側各自非空的投影相乘。

這是**有限完整原子的 separator 壓縮**：可直接保存 W 取代反覆搜尋五個
私人原點，重建時再接回其 full lifts。它不主張找到少於五內點的圖代表，
不據此作來源最小性下降，亦不保證每個 J 指派都延伸。

## 4. 完整原子證書

[check.py](check.py) 從上列14個原面重建原點、邊、boundary 與各 vertex
link；逐份直接 MRV 染色與獨立中心色分解(1)比較**全部完整 lifts**。
[full_lifts.v2.json.gz](full_lifts.v2.json.gz) 包含4096份 literal J 指派及每份
U 染色，包含3652個空 fibre；不以 S4 代表取代 literal 資料。

* 732份 proper J 指派，其中288份空、144份各一份 lift、300份各兩份。
* cap 合計744份 full lifts。
* proper J 有31個全域 S4 軌道，其中19個接受；此數只作校準，不獨立
  正規化任何 terminal 或外側染色。

例如 proper 原列 `J=010102` 的 fibre 為空，故不能將 terminal 原子標成
對所有原六環指派普遍可延伸。負控制包括把此 proper 空列改成非空、刪去
一份真正 lift，以及在兩個本可個別延伸且半弧兩端色一致的 terminal
指派中，給共享原點 e 不同色；最後一種原 join 必為空。

## 5. 完備的 s=0 PINCH／BRIDGE 回接八份來源

由 T0，s=0 的兩種形狀均只有上述兩個原 W5，沒有任意大小內部尚待枚舉。
正對 pair 有四份原位置 `{c_i,c_(i+4)}`，`0≤i<4`；每份固定 clockwise
半弧 ownership。BRIDGE 用一次私人命名使左 terminal endpoint 為 x、
右 terminal endpoint 為 y，保留同一原邊 xy；不改動 C 名字。

全部八份原 collar 如父包 C8 接入表：

`c15-933,c18-933,c04-941,c07-941,c15-941,c18-941,c20-941,c30-941`。

checker 按每份原 e 重建五個 a、三個 y 的 C 順序和所有 B–C 原面，不按
不同列再旋轉。兩類 ×四個 pair ×八份 collar 共64份原 G；每份原 B
十列均直接搜尋整圖 full lifts，並與兩份 literal 原子 W 的式(2)完整
joins 比較。bridge 已在共同 skeleton 中檢查端點異色。

[certificate.v2.json](certificate.v2.json) 保存每份原圖完整點序、邊、全部有向
三角面、原 vertex links／rotations、C 原名對應、兩份 J/U ownership，以及原 H
的每條 C3/C4/C5 的面對偶內域檢查。全部640個 B fibres 與61752份原 G
full lifts 保存在壓縮 archive；direct 與完整原子 joins 逐份相等。
所有64份的完整十列皆為 `Σ=1023`，均異於其原來源 target933／941。

因此有新來源排除：

\[
\boxed{h=3,\ p>0\Longrightarrow s\ge1.}              \tag{3}
\]

接既有 terminal 耳下界，可得實際來源的

\[
\boxed{\text{PINCH}:m\ge12,\qquad\text{BRIDGE}:m\ge13.} \tag{4}
\]

這不排除只有一側 `s_side=0`、另一側有單接點的任意大小來源；該子域現已
有可直接使用的完整原子(2)。实际目標來源仍未觸發：新排除是紙面精確
分類加全部完整關係的結果，不以搜尋零反例或 `not triggered` 作排除。

## 6. RING 的窄無弦修復

**引理 R0。** 若 RING `p=s=0` 且 m≥11，Q 的原外框
`T=(t0,…,t7)` 必為 induced T8。

證明：每個 T 點 Q-degree≥3。任一 T chord 的較短弧長為2、3或4。
弧長2／3時，其小側是原 C3／C4 cap，嚴格內域空；空 polygon 有一個
不在 chord endpoints 的耳。該耳的全部 Q sector 在此 cap，故完整
Q-degree=2，矛盾。

只剩正對 chord，兩側外框皆為 C5。任一空側仍有一個非 endpoint 的
degree2耳，矛盾；故兩側都 occupied，由 proper C5 cap 定理恰為 W5。
chord 將整個 T disk 分成這兩側，因此只有兩個無 C 接點的中心，
`m=8+2=10`，與 m≥11 矛盾。故無 chord。

這修復原來源的一個窄前提：s=0 的剩餘 RING 可沿原 induced T8 繼續
separator 研究。此 T8 仍只知 boundary Q-degree≥3；下一層每點至多
雙接、boundary degree≥4、內側連通及固定寬度均未由 R0 得到。

## 7. 本輪可採納與 OPEN

可採納：任意大小 T0、原 literal 六點 full-fibre 壓縮(2)、全部 s=0
PINCH／BRIDGE 原來源排除(3)及(4)，與 RING `s=0,m≥11` induced T8。

後續精確入口是：PINCH／BRIDGE 具有一個零單接 terminal 時，用同一
原子 W 對任意另一側做 literal 完整 join；兩側均有單接點時仍須處理
原大 terminal。RING s=0 可先保原 T8，另證 degree3 的替代義務；s>0
外框長8+s不能回寫成固定 C8。

無界八份來源、h≥4的932／933／941、一般 `K∞=K≤5`、固定寬度剝層及
新論證 Lean 形式化仍 OPEN。本輪不新增 paper 外部定理或 4CT 前提；
已承繼的來源分類／有界結果仍保留父包所列外部有限計算與生成信任。

重播：

```bash
python3 -B audits/2026-10-13-c5-no4ct-frontier-6943561/terminals/check.py --check --negative
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-c5-no4ct-frontier-6943561/terminals/check.py --check --negative
```

本交付不 commit／push，不改共享證據，也不把正常執行當作紙面拓撲的 Lean
證明。父包驗證帳本記錄 exact frozen inputs 及本輪命令。
初始 prototype `certificate.json`／`full_lifts.json.gz` 保留；最终 checker
只讀 v2。v2 生成使用 exclusive-create，已有檔案時拒絕寫入。
