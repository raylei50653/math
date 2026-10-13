# C8 反覆剝層：原接點三型與完整染色轉移

2026-10-13 整理補註：[無四色定理前提 C8 接入](../audits/2026-10-13-c5-no4ct-c8-6cafdfb/REPORT.md)
已在新的全域最小 932／933／941 契約下重證所需小 cap 與相對商圖可染性，
完整 105 查詢排 97、留原八項；932 分支必 `h≥4,n₅≥10`。
本頁原八項的三型、完整轉移及 `h=3⇒k≥19` 已接入；無界三支與固定寬度仍 OPEN。
[目前交接與下一窄任務](tasks/c5_no4ct_handoff.md)；下文原證明／證書保留。

2026-10-13。接續 [C8 原短弧與 m=9 內圈](c5_c8_inner_collar.md)。
本頁為剝層題的權威入口；[隔離報告](../audits/2026-10-13-c8-peeling-6cafdfb/REPORT.md)
串接任意大小的 [結構證明](../audits/2026-10-13-c8-peeling-6cafdfb/structure/PROOF.md)、
[完整轉移公式](../audits/2026-10-13-c8-peeling-6cafdfb/TRANSFER.md)及
[m=10 校準](../audits/2026-10-13-c8-peeling-6cafdfb/calibration/PROOF.md)。
目前停止點見 [Kempe 導覽](c5_kempe_guide.md#3-停止點與保留缺口)。

## 1. 適用前提與任意大小分類

沿用全域最小內點、再最大邊數的目錄外 disk-C5 原來源及八項 h=3 契約，
固定同一原有序 C=(c0,…,c7)、內側 H、I=V(H)\C、Q=H[I]。
C induced、H 內面三角化、C 點 H-degree≥4、I 點 H-degree≥5；
原內 C3／C4 cap 空，C5 cap 空或 W5。上游短弧定理已證每 I 點至多接
兩個 C 點，雙接只能相鄰或正對，八條 C 邊的第三點 t_i 全異。
**相鄰雙接唯一性另外使用無 occupied C3，不能只由「至多兩接點」推出。**

相鄰雙接點恰為 t_i。令 s 為單接點數、p 為正對雙接點數、r 為無接點數。
原 C 點的內 link paths 依原 rotation 接成 Q 的完整外面 walk W；其外面
原點集合 S 精確等於全部 C 接點，有

\[
m=8+s+p+r,\qquad |S|=8+s+p,\qquad |W|=8+s+2p.
\]

正對點是 Q 的全部 cut vertices，各自切成兩個 components。所有正對點
使用同一 antipodal pair，且 p≤2；這是 disk crosscut 與空 C4 cap 的普遍證明。

| 具名類 | 適用條件 | 原圖內側外面 |
| --- | --- | --- |
| **C8-LINK-RING** | p=0 | 長 8+s 的簡單環；內 disk 仍可能有 boundary chord。 |
| **C8-LINK-PINCH(i;x)** | p=1，x 同接 c_i、c_(i+4) | 兩個三角化 disk 共用同一原點 x；W 中 x 出現兩次。 |
| **C8-LINK-BRIDGE(i;x,y)** | p=2，x、y 同接該 pair | 兩個 terminal disk 由唯一原 bridge xy 相連；W 往返 xy。 |

因此內側外面為簡單環 **當且僅當 p=0**，沒有未分類的額外分支點。
PINCH 兩側、BRIDGE 兩端的外環分別長 5+s_+、5+s_-，各至少有一個
嚴格內點：否則空 polygon 的兩耳至少一個違反 Q 度數下界。
故 PINCH 必 m≥11+s，BRIDGE 必 m≥12+s。

## 2. 完整染色轉移與任意大小反覆剝層

四色始終為 A={0,1,2,3}。對 S 的 literal 指派 b，令 F_Q(b) 保存全部完整
lifts，包括空 fibre。固定原 C 指派 a，則

\[
\boxed{F_H(a)=\bigsqcup_{b\in A^S:\ a(c)\ne b(x)\ \forall cx\in E(C,S)}
\{a\cup f:f\in F_Q(b)\}.}
\]

improper 的 a 給空集。PINCH 使用
\(F_Q(b)=F_L(b_L)\Join_xF_R(b_R)\)；BRIDGE 使用
\(F_Q(b)=F_L(b_L)\Join_xF_{xy}(b_x,b_y)\Join_yF_R(b_R)\)，
其中原邊 xy 強制 b_x≠b_y。重複 walk 位置必滿足同一原點同色，不能建立
兩份 x，也不能把各側投影的非空性當作共同 witness。

一般反覆剝層取 R_0=Q，每步取各分量無界面原點集合 S_l，令
R_(l+1)=R_l−S_l。刪除外面點後，每條跨層原邊的內端都 incident 於下一層
無界面，故所有原邊只連同層或相鄰兩層。完整公式為

\[
F_l(a)=\bigsqcup_{b:\ K_l(a,b)=1}\{a\cup f:f\in F_{l+1}(b)\},\quad
N_l(a)=[a\text{ proper}]\sum_bK_l(a,b)N_{l+1}(b),
\]

K_l 檢查全部具名跨層邊，空圖基底為 F(∅)={∅}、N(∅)=1。
每步嚴格減少原點數，所以適用**任意有限內側大小**。分量可分別計算，
articulation 須同色 join，孤點及單邊亦有明確終止公式。
[完整公式 T1–T9](../audits/2026-10-13-c8-peeling-6cafdfb/TRANSFER.md)另列
精確 counts、block-cut join、重複位置一致性及接回原 B 的全部十列。

這個定理保存任意大小原圖的完整關係；沒有證明固定八點介面、固定型錄、
多項式時間，或每層可直接沿用第一層的 C8 前提。

## 3. m=10 完備分類與原來源排除

上述任意大小結構先排除 p>0。若 r=0，outerplane 耳違反度數；若 r=1，
boundary chord 的空側又有低度耳，故只可能 wheel，其單接點 H-degree=4，
與來源界矛盾。因此 m=10 必 s=p=0、r=2，內側外環就是具名 T8。

| 具名族 | 原核心與前提 | 固定 C/T 次序的位置數 |
| --- | --- | ---: |
| **CHORD-55**（正對弦雙 W5） | T 的唯一 chord 為 t_a t_(a+4)，兩側各含一中心；中心不相鄰。 | 4 |
| **EDGE-35** | T 無 chord；兩中心相鄰，沿 T 的兩 fan 弧長 3、5。 | 8 |
| **EDGE-44** | T 無 chord；兩中心相鄰，兩 fan 弧長各 4。 | 4 |

結構證明使用 Euler 及兩中心 degree≥5，排除額外 chord 或其他接線；
中心名字只是一次固定重命名，不在不同色列改圖。這 16 個具名 H 是 m=10
全部可能局部配置，並非任意大小圖搜尋的截斷。

逐份回接八個原 B–C collars，共 128 原具名圖的完整十列全為 Σ1023；
1,280 fibres 保存 75,936 full lifts。另有 16×274 個 C8 orbit 代表 fibres，
其中 1,500 空，7,408 full lifts；內介面使用全部 6,564 literal T8 指派。
direct 整圖染色與逐層同色框 full join 比對全部 lifts。
因此 m=10 也不是 933／941 原來源，接上游 m≤9 排除，得到

\[
\boxed{h=3\Longrightarrow m\ge11\Longrightarrow k(G)\ge19.}
\]

## 4. 不能照搬 C8 契約的具名障礙與停止點

| 障礙 | 實際觸發與處理方式 |
| --- | --- |
| **OPP-PINCH** | 同一 x 在 walk 重複；改用兩 disk 的共享 x join。 |
| **OPP-BRIDGE** | xy 往返；保留原端點及異色邊約束。 |
| **DEGREE-LOSS** | m=10 EDGE 的普通 t 在 Q 度三；下一層 degree≥4 不傳遞。 |
| **CHORD-INHERITANCE** | CHORD-55 的 T8 有 chord；下一層不是 induced C8。 |
| **MULTI-CONTACT** | EDGE-35 兩中心接 T 的 4／6 點、EDGE-44 各接 5 點；至多雙接不傳遞。 |
| **DISCONNECTED-CORE** | CHORD-55 再剝 T 後剩兩個孤點；下一層不是單一 disk。 |
| **WIDTH-GROWTH** | 具名 m=11 控制的內側外面為簡單九環；固定八點寬度不傳遞。 |

這些原嵌入局部控制滿足所用幾何前提；接回 B 後屬 Σ1023，不能當成真正
目錄外來源。它們證明**局部前提不足以保證同型 C8 遞迴**，沒有反駁可能另由
完整 933／941 最小性導出的更強結構。

第一層三型、一般完整 separator 剝層與 m=10 來源排除已交付；
八個 h=3 任意大小來源的染色排除、固定寬度壓縮及一般 K∞=K≤5 仍 OPEN。
一般 k≥16、h≥3、n5≥9 均不提高；新結果是 h=3 的 k≥19。
證據為紙面結構與完整 Python 證書，沒有新增 Lean theorem。

```bash
python3 -B audits/2026-10-13-c8-peeling-6cafdfb/check.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-c8-peeling-6cafdfb/check.py --check
python3 -B audits/2026-10-13-c8-peeling-6cafdfb/check.py --negative
```
