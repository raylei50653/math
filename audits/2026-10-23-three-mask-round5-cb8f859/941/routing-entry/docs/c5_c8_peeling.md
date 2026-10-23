---
docgraph:
  id: c5.c8-peeling
  family: [c5, c5.c8]
  requires: [c5.c8-inner-collar]
  verified_by:
    - audits/2026-10-13-c8-peeling-6cafdfb/structure/PROOF.md
    - audits/2026-10-13-c8-peeling-6cafdfb/TRANSFER.md
    - audits/2026-10-13-c8-peeling-6cafdfb/calibration/PROOF.md
    - audits/2026-10-13-c5-no4ct-c8-6cafdfb/REPORT.md
    - audits/2026-10-14-t1-crosscut-review-77fbd5d/REPORT.md
    - audits/2026-10-14-t1-crosscut-review-77fbd5d/ADOPTION.md
    - audits/2026-10-14-t1-crosscut-review-77fbd5d/check_adoption.py
    - audits/2026-10-14-t1-crosscut-review-77fbd5d/review/SOURCE_COVERAGE.md
    - audits/2026-10-14-t1-crosscut-review-77fbd5d/review/SUPPORT_LOGIC.md
---
# C8 反覆剝層：原接點分類、正對點排除與完整染色轉移

更新：2026-10-14。本頁是 **第一層接點分類、正對點排除、完整 separator
轉移及 m=10 排除**的權威入口。在原 no4ct 全域最小來源契約下，
[T1 一般正對切口採納](../audits/2026-10-14-t1-crosscut-review-77fbd5d/ADOPTION.md)
已採納 **`h=3⇒p=0`**：全部 PINCH／BRIDGE 排除，不限制單接點數或兩側
內點數。[同一八項契約](c5_c8_apex_degree.md#八項必要殘留)只剩 RING；
剝層自身的大小界為 **`h=3⇒m≥11⇒k≥19`**；後續
[C4 來源橋](c5_c4_boundary_pivot.md)另得三支共同 **`k≥23`**。
RING、h≥4 及一般主命題仍 OPEN。
任意有限原嵌入的完整剝層轉移已證，下一層的 C8 度數、無弦與接點限制
尚不自動傳遞。h≥4 的義務另列於 [§5](#5-h4-的另列義務)。

## 前置來源與交付角色

| 來源／交付 | 所消費的前提與涵蓋範圍 |
| --- | --- |
| [apex 度數](c5_c8_apex_degree.md)、[原短弧與 m=9 內圈](c5_c8_inner_collar.md) | 同一具名 induced C8、H 內面三角化、d_H(C)≥4、d_H(I)≥5；每 I 點至多雙接，相鄰或正對，八個原面第三點全異；m≤9 已排除。 |
| [新三支 C8 接入 §4](../audits/2026-10-13-c5-no4ct-c8-6cafdfb/REPORT.md#4-接回-apex原內圈與剝層)、[原 cap 修復](../audits/2026-10-13-c5-no4ct-c8-6cafdfb/geometry/PROOF.md) | 在全域 k 最小、再邊數最大的 932／933／941 契約下，保留 s<k 的小 cap 與 N≤k+5 的相對可染性；原 C3／C4 cap 空、C5 cap 空或 W5。本頁歷史證明鏈已接入此契約。 |
| [第一層結構證明](../audits/2026-10-13-c8-peeling-6cafdfb/structure/PROOF.md) → [§1](#1-適用前提與任意大小分類) | 另消費原 rotation 及無 occupied C3，證相鄰雙接唯一性與 RING／PINCH／BRIDGE 完備分類；量詞為任意有限 m 的第一層。 |
| [T1 一般正對切口審查](../audits/2026-10-14-t1-crosscut-review-77fbd5d/REPORT.md) → [T1-CROSSCUT](#t1-crosscut) | 原正對點切成兩個具名 C6；同一 literal 外側接合兩片完整支援。32份核心的512,568個安全矩形全缺原接受列01232，得原 no4ct 最小來源 h=3⇒p=0，兩片大小與單接點數無上限。 |
| [完整轉移 T1–T9](../audits/2026-10-13-c8-peeling-6cafdfb/TRANSFER.md) → [§2](#2-完整染色轉移與任意大小反覆剝層) | 轉移本身只需有限簡單平面圖、固定嵌入、全部原邊與同一 literal 色框；保存完整 fibres／空 fibres／full lifts，逐層終止並接回原 B 十列。原三角面保留另使用既有三角化嵌入。 |
| [m=10 完備校準](../audits/2026-10-13-c8-peeling-6cafdfb/calibration/PROOF.md) → [§3](#3-m10-完備分類與原來源排除) | 紙面三族共16份具名 H，接回八 collars 的128圖完整 Σ1023；配合上游 m≤9 排除，才推出 h=3⇒k≥19。 |
| [七項具名障礙](#4-不能照搬-c8-契約的具名障礙與停止點) | 說明局部前提不足以保證同型 C8 遞迴；完整 separator 轉移本身不給來源排除、固定寬度或可染性存在。 |

[原隔離報告](../audits/2026-10-13-c8-peeling-6cafdfb/REPORT.md)保存 BASE `6cafdfb`
的分類與 m=10 證書；新採納審查固定 BASE `77fbd5d`，保存來源覆蓋、
完整有限重播及另一份獨立重建。兩輪證據均沒有新增 Lean theorem。
目前停止點由 [Kempe 導覽](c5_kempe_guide.md#3-停止點與保留缺口)及
[無四色定理前提交接](tasks/c5_no4ct_handoff.md#4-精確停止點與未完成項目)維護。

歷史進度（2026-10-13）：[T1](../audits/2026-10-13-c8-terminal-s1-d521163/REPORT.md) 在指定 no4ct 契約下
完成 s=1 的640份原外側完整轉移排除，連同 s=0 得 h=3、p>0⇒s≥2。
當時得到 PINCH m≥13／k≥21、BRIDGE m≥14／k≥22，剩餘 C6 內點數無上限。
此輪的「s≥2兩型仍 OPEN」停止點已由 [T1-CROSSCUT](#t1-crosscut) 全部涵蓋；
原 s=0／1 結果、三型分類與歷史證書保留，當前來源只剩 RING。

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

上表保存原局部結構分類；加入完整原 target 後，以下定理排除後兩型。

<a id="t1-crosscut"></a>

### 1.1 T1-CROSSCUT：一般正對切口排除

在所有目錄外 disk-C5 來源中先全域最小化內點數 k，再最大化邊數，
沿用 no4ct 正規形與一次共同 D5 對齊；不是對 933、941 分別最小化。
h=3 時 932 已由上游排除，所餘八份原 collar／target 滿足

\[
\boxed{h=3\Longrightarrow p=0.}
\]

任取原正對點 x 同接 c_i、c_(i+4)。原路徑 c_i–x–c_(i+4) 將 H 切成
兩個閉 disk L±，邊界依原次序為（下標模8）

\[
D_+=(x,c_i,c_{i+1},c_{i+2},c_{i+3},c_{i+4}),\qquad
D_-=(x,c_{i+4},c_{i+5},c_{i+6},c_{i+7},c_i).
\]

兩片恰共享同一 x、c_i、c_(i+4) 及兩條原 spokes。P 保留完整原 B–C8
annulus 與此路徑，所有其餘原點、邊及 rotation sectors 留在實際所在的
L±；有 G=P∪L+∪L−、P∩L±=D±。BRIDGE 的另一端及原橋完整留在其中
一片。因此這個單 x 切口同時覆蓋 PINCH、BRIDGE 及任意單接點數。
任意來源證明與原 collar 映射見 [來源覆蓋審查](../audits/2026-10-14-t1-crosscut-review-77fbd5d/review/SOURCE_COVERAGE.md)。

對原 B row β，以每份完整 P 染色 f 同時固定兩個 literal 界面，完整
fibres（包括空 fibre）有雙射

\[
F_G(\beta)\cong\bigsqcup_{f\in F_P(\beta)}
F_{L_+}(f|_{D_+})\times F_{L_-}(f|_{D_-}).
\]

每一份 f 及兩份選定 full lifts 唯一接成原 G 染色。令 R± 是同一固定
L± 的完整 C6 軌道支援，先由同一份 literal f 讀取兩個軌道再定義
M_P(q,r)，才有

\[
\Sigma_B(G)=\bigcup_{q\in R_+,\,r\in R_-}M_P(q,r).
\]

對完整 target τ，
同一份 **R+×R−** 必包含於 Eτ={(q,r):M_P(q,r)⊆τ}，包括零輸出 pair。

完整枚舉每個極大安全矩形 A×B，分別用平面 disk 的必要 Kempe 交換
條件收縮為 κ(A)、κ(B)，仍有 R+⊆κ(A)、R−⊆κ(B)。八份原 collar-target
契約乘四個正對位置，共 **32份核心、512,568個矩形**，收縮後的外框
聯集全缺原接受列 `01232`，與 933、941 矛盾。這32份已足夠排除任意
有限兩側內點數；額外32份雙正對點及橋外側是補充核對。
[支援邏輯審查](../audits/2026-10-14-t1-crosscut-review-77fbd5d/review/SUPPORT_LOGIC.md)
給出直積、矩形完備性及 Kempe 刪除的 soundness；
[審查報告](../audits/2026-10-14-t1-crosscut-review-77fbd5d/REPORT.md#4-本次實際重播及獨立重建)
保存正常／seed-17 重播、負控制及第三份完整重建。

本定理消費完整同圖支援，不假設通過抽象條件的支援可實現，也不引用
普遍四色可染性。它只把第一剝層收到 RING；不提高 k 的下界，不證
RING 或 h≥4 排除，也沒有新增 Lean theorem。證據為 agent 輔助紙面
審查及完整 Python 證書，不稱為第三方人類數學審查。

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

T1–T3 處理原 C 與 Q 外面點集合，T4–T6 處理共享原點與 bridge，
T7–T8 處理以下一般剝層，T9 將結果沿原 B–C collar 接回完整十列。
這是一條同一色框、同一原點身份的完整轉移鏈，不能在中途改用各側 marginals。

一般反覆剝層取 R_0=Q，每步取各分量無界面原點集合 S_l，令
R_(l+1)=R_l−S_l。刪除外面點後，每條跨層原邊的內端都 incident 於下一層
無界面，故所有原邊只連同層或相鄰兩層。完整公式為

\[
F_l(a)=\bigsqcup_{b:\ K_l(a,b)=1}\{a\cup f:f\in F_{l+1}(b)\},\quad
N_l(a)=[a\text{ proper}]\sum_bK_l(a,b)N_{l+1}(b),
\]

K_l 檢查全部具名跨層邊，空圖基底為 F(∅)={∅}、N(∅)=1。
若 a improper，F_l(a)=∅；其餘分解保留每個 b 的空 fibre。
每步嚴格減少原點數，所以適用**任意有限內側大小**。分量可分別計算，
articulation 須同色 join，孤點及單邊亦有明確終止公式。
[完整公式 T1–T9](../audits/2026-10-13-c8-peeling-6cafdfb/TRANSFER.md)另列
精確 counts、block-cut join、重複位置一致性及接回原 B 的全部十列。

這個定理保存任意大小原圖的完整關係；沒有證明固定八點介面、固定型錄、
多項式時間，或每層可直接沿用第一層的 C8 前提。

## 3. m=10 完備分類與原來源排除

以下保留原 m=10 證明，其結構下界在 m=10 已先排除 p>0，不依賴新定理。
若 r=0，outerplane 耳違反度數；若 r=1，
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
完整 933／941 最小性導出的更強結構。OPP-PINCH／OPP-BRIDGE 保留作
一般 separator 的歷史控制；T1-CROSSCUT 已在原最小來源的第一層排除兩型。

第一層分類、一般完整 separator 剝層、m=10 來源排除及 h=3⇒p=0 已採納；
八個 h=3 契約的 RING 來源排除、固定寬度壓縮及一般 K∞=K≤5 仍 OPEN。
正對點排除本身不提高採納當輪的一般 k≥16、h≥3、n5≥9 與 h=3 的 k≥19；
當前 k 的共同界另由 [C4 來源橋](c5_c4_boundary_pivot.md)提高至 k≥23。
證據為紙面結構與完整 Python 證書，沒有新增 Lean theorem。

<a id="5-h4-的另列義務"></a>

## 5. h≥4 的另列義務

下列義務沿用[新三支契約與停止點](tasks/c5_no4ct_handoff.md#4-精確停止點與未完成項目)，
不由本頁 h=3 的分類或十九內點界完成。

| 分支／義務 | 已有輸入與尚未完成的部分 |
| --- | --- |
| h≥4 的 932 | h≥4、n₅≥10；[T2](../audits/2026-10-13-c9-932-source-d521163/REPORT.md)的apex下界保留。h=4三接點已排，[第四輪](../audits/2026-10-23-three-mask-round4-cb8f859/932/REPORT.md)以同一原C6／C7群平均OR接合排全部距四接點，每collar只餘零pair。原下一層Q長9+s、可有弦，至少一個深點；零pair h=4與h≥5仍OPEN，共同k≥23不變；原E4／N2排除不能刪一般分支。 |
| h≥4 的 933／941 | 當前共同 k≥23、原內圈 C_(5+h)、原度數與小 cap 的受限前提；仍須將較長內圈的具名附件接入既有完整 transfer，另證共同計數限制與來源排除，不能沿用八份 h=3 collars。 |
| 下一層結構 | 完整 separator 轉移可使用實際外面點集合；若要重用 C8 結構簡化，必須另證其度數、induced／無弦、接點限制、連通性及寬度。§4 的控制已顯示局部前提不足。 |
| 固定寬度與一般主命題 | 大小無關的介面壓縮及 K∞=K≤5 仍 OPEN；有限終止與精確轉移不完成這兩項義務。 |

h=3 的剩餘義務是對同一八項、m≥11、p=0 的原 H 給出共同圖層矛盾。
當前只剩 RING，其下一層外環長 8+s，仍可有 chord；不再逐級研究
PINCH／BRIDGE 的 s=2、3、…，也不能把本次兩個 C6 切口推給 RING。
[交接的下一窄入口](tasks/c5_no4ct_handoff.md#5-建議的第一個窄任務)維護這項研究安排。
[K15-SPHERE](c5_k15_sphere.md)的一般 k≥16 與本頁 h=3⇒k≥19 是各輪獨立界；
**十九內點界不能套到 h≥4。** 當前 [C4 來源橋](c5_c4_boundary_pivot.md)
另證 `K≤22=K≤5` 及全部三支的共同 k≥23，未完成此處無界義務。

## 6. 重播入口與本次整理範圍

本次入口整合採納已完成的[正對切口審查與重播](../audits/2026-10-14-t1-crosscut-review-77fbd5d/REPORT.md#6-重播)，
原 REPORT 保留隔離審查當輪狀態；目前整合身份由
[ADOPTION.md](../audits/2026-10-14-t1-crosscut-review-77fbd5d/ADOPTION.md)
與採納 checker 維護。只讀核對採納 receipt／凍結來源，或完整重算64份：

```bash
python3 -B audits/2026-10-14-t1-crosscut-review-77fbd5d/check_adoption.py --check
python3 -B audits/2026-10-14-t1-crosscut-review-77fbd5d/check_adoption.py --replay
```

以下保留原剝層證書的重播入口；整合文件時未再次重算這些歷史證書，
亦未執行 Lean build。

```bash
python3 -B audits/2026-10-13-c8-peeling-6cafdfb/check.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-c8-peeling-6cafdfb/check.py --check
python3 -B audits/2026-10-13-c8-peeling-6cafdfb/check.py --negative
```
