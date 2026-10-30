# 雙色唯一缺口的 bridge 路徑定理

**後續（2026-10-11）**：[N2全部真核心排除](../excess/other/c5_excess_two_arc_spoke_closure.md)
以新的末端block／二連通與兩次SD-A路線，涵蓋完整N2目標契約的全部45／54，
包含下文保留的N45 exact-S父身份。本文共用引理的量詞不變；原55、一般R31及E-ARC2仍OPEN。

2026-10-11；整理基準 `fdbef272c9f74ed95a4dac644b1c7f8b071a7722`。
本報告證明不依賴 N45 名稱的任意大小命題，再將同一原圖的 BR-SD-1a／1c／1e／1g
接成一個共同推論。證據層為外部 Gallai degree-list 刻畫＋本輪紙面證明；
沒有新增有限來源、枚舉證書、獨立採納審查或 Lean theorem。
目前接入與剩餘義務見 [N45§2.12–3](../excess/other/c5_excess_two_nonadjacent_unit_core45.md#212-雙色唯一缺口的共同排除)
及 [degree-5 導覽§4](../../../guides/c5_degree5_guide.md#4-r31-保留缺口與重播入口)。

## 1. 命題與完整量詞

取任意有限連通簡單圖 C、任意有限色集 Col，以及 lists
`L(v)⊆Col`，逐點滿足 `|L(v)|≥d_C(v)`。假設 C 不可依 L 著色。
取原頂點 r，令 S 是 C−r 的一份完整連通分量。
若存在不同的固定顏色 T、D 及 q∈S，使

\[
\{T,D\}\subseteq L(v)\quad(v\in S\setminus\{q\}),\qquad
T\in L(q),\quad D\notin L(q),
\]

則

\[
\boxed{|N_C(r)\cap S|=1,\qquad
\text{從 r 到 q 的 block 路徑上全部 blocks 都是原圖 bridges。}}
\]

「block 路徑」指完整 block–all-vertex incidence tree 中 r 到 q 的唯一路徑。
blocks 包含 bridges 視為 K₂。因 r 與 q 不同，C 至少有兩個頂點。
不需要平面性、degree≤4、二連通、minimality、三環骨架或 private witness；
四色只是 §5 原來源接入的特例。結論不宣稱 S 的所有 blocks 都是 bridges。

## 2. 外部依賴與原 incidence tree

採用 Zdeněk Dvořák，*List coloring and Gallai trees*（2018-03-24），
[作者講義](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)印刷 p.5 的 degree assignment
定義／Lemma 7，以及 p.6 的 blockwise-uniform 定義／Theorem 10。
本次沿用已封存的 [PDF](../../../../../audits/2026-10-11-br-sd-1g-dbdc4c35/external/gallai.pdf)；
版本紀錄見 [SOURCE](../../../../../audits/2026-10-11-br-sd-1g-dbdc4c35/external/SOURCE.md)。
本輪重新計算該檔 SHA256 為
`50e998fcb016418698ef31b932c6c2e728007f5e3b3348b93744781196ac1aea`。

外部刻畫給 C 是 Gallai tree，各 maximal block K 有非空 palette P_K，且

\[
L(v)=\bigsqcup_{K\ni v}P_K.
\]

不同 incident blocks 的 palettes 互斥；K_n 的 palette 大小 n−1，奇環大小2，
bridge 大小1。不預先把原 degree-list 不等式改成等式；不可著色本身迫緊性。

令 I 的節點為全部原 C 頂點及全部 maximal blocks，v–K 邊 iff v∈V(K)。
通常的 block-cut tree 加回每個非割點的原葉節點就是 I，因此 I 是有限樹。
以下計數及單出口推論由本報告證明，不把它們歸給外部 Theorem 10。

## 3. Exclusive-block 計數引理

固定不同兩色 T、D。選出全部滿足 `|P_K∩{T,D}|=1` 的 blocks，
保留它們的全部原頂點及全部 incidence edges，得到 I 的子森林 E。
令 F 是 E 的任一含 block 的完整連通分量；V₀(F) 表其原頂點，B(F) 表其 block 節點。
則

\[
\boxed{
\#\{v\in V_0(F):|L(v)\cap\{T,D\}|=1\}
=2+\sum_{K\in\mathcal B(F)}(|V(K)|-2).
}
\tag{1}
\]

證明如下。由 incident palettes 互斥，每種顏色至多由一個 incident block 提供。
出現在 E 的原頂點，若其 list 恰含 T、D 之一，度就是1。
若其 list 同時含兩色，已選中 block 只供其中一色，另一色必由另一個選中 block 提供，
故度就是2。兩色由同一 palette 提供的原頂點不會出現在 E。
相鄰的選中 blocks 必在同一完整 F，因此上述度數在 F 中仍為1或2。
每個 block 節點則有度 `|V(K)|≥2`。

設左側為 n₁。有限非平凡樹的度數式給

\[
-2=\sum_{z\in V(F)}(\deg_F(z)-2)
=-n_1+\sum_{K\in\mathcal B(F)}(|V(K)|-2),
\]

即得 (1)。必須保留全部 block 原頂點；只用割點的 block-cut tree 不能照用此式。
F 也不能任取 E 的連通子樹，否則裁掉的 incidence 可能製造不對應原 list 缺口的葉。

## 4. 唯一缺口與唯一出口

在 I 刪去 r 後，取對應完整 S 的那份連通分量，再接回 r 及其 incident 邊，記為 I_S。
原圖 block 刪掉單點仍連通（bridge 刪端點後剩單點），故 I−r 的分量與 C−r 的分量
一一對應。因 I 是樹，r 在 I_S 中恰有一個 incident block，記為 K_r。
若有兩個，I_S−r 的連通路加上這兩條 incidence edges 會在 I 中構成環。

所有 incident 於 S 原頂點的 blocks 及其全部原頂點都在 I_S 中。
因此在 I_S 中選出全部 exclusive blocks，再取含 q 的分量 F_q 時：

- q 的度為1，因 T∈L(q)、D∉L(q)。
- 其餘出現的 S 原頂點度均為2，因其 lists 同時含 T、D。
- r 若出現，度為1；這來自 I_S 的唯一入口，不假定 r 的原 list 缺色。
- 每個 block 節點的度仍是 `|V(K)|≥2`。

F_q 含至少一個 block。直接對這份樹計算度數，得到帶出口項的等式

\[
\boxed{
1+\mathbf1_{\{r\in F_q\}}
=2+\sum_{K\in\mathcal B(F_q)}(|V(K)|-2).
}
\tag{2}

左側至多2、右側至少2，故 r∈F_q，而且其中每個 block 都恰有兩個原頂點。
於是 F_q 是一條以 q、r 為兩端的路徑，其中 blocks 全為 C 的原 bridges。
它也是完整 I 中 r 到 q 的唯一路徑。K_r 在這條路徑上，故 K_r 是 bridge。
所有 r 到 S 的原邊都屬 K_r；因此 `|N_C(r)∩S|=1`，命題得證。

這裡沒有把 (1) 直接套在裁切後的 F_q 並誤數原 lists；(2) 的 r 項
明確計算 S 側出口。r 的原 list 可同時含 T、D，另一色可由 C−S 的 block 提供。

## 5. 同一原圖的共同排除與四份 BR 接入

先把接入所需的充分條件與 N45 的其餘來源合同分開。固定同一原 M、外框 B、
proper 三色 β、同一四色集 Col，令 D 是 β 未用色。保留下列原圖條件：

1. `C=H_M−s` 是實際 sole connected component，r∈C；M 自己拒絕 β。
2. 原 C 各點完整 M-degree4，原鄰居全由 C、B 及 s 計入。
3. S 是 C−r 的完整連通分量；s 在 S 恰有唯一原鄰點 q。
4. S 的全部原 boundary attachments 在同一 pair，其 β 顏色是不同 A、B′。
   令 T 是 β 使用的第三色，故 `Col={A,B′,T,D}`。
5. C 的完整 list-coloring 與原 M／β／s=D 的延拓存在性等價；
   effective-H 忽略的原坐標也保留非空允許色因子，不能以投影雙射代替完整 lifts。

對每個原 y∈C，以實際原鄰居定義

\[
L^D(y)=\mathrm{Col}\setminus
\bigl(\beta(N_B^M(y))\cup\{D:sy\in E(M)\}\bigr).
\]

完整原 degree 式是
`4=d_C(y)+|N_B^M(y)|+1[sy∈E(M)]`，因而 `|L^D(y)|≥d_C(y)`。
附件同色只可能造成 slack，不先假定 lists 緊。β 未用 D，所以 s 的原 B-spokes 都合法。
將 C 染色與 β、s=D 接合，保每條原邊；被 effective-H 忽略的 B-only 原點之允許色含 D，
真正無鄰居的自由孤點有整份 Col。這些原坐標的乘積因子均非空，故拒絕 β 迫 C 不可著色。
S−{q} 的 lists 全含 T、D，q 含 T 且不含 D，恰滿足 §1。

所以 **上述同一原圖前提加 `|N_C(r)∩S|≥2` 不可能成立**。
原附件支援「包含於」這份異色 pair 已足以給雙色形狀；四份既有 BR 合同更強，
要求 actual support 聯集恰為同一真框邊兩端。本推論不擅自改寫其原來源身份。

| 已有來源合同 | 對回共同前提 | 本推論不再需要的形狀條件 |
| --- | --- | --- |
| [BR-SD-1a](../excess/other/c5_excess_two_nonadjacent_unit_core45.md#211-單缺額查證與無-u-二連通子域) 合同1–3、5 | 原 sole C、S 完整、actual pair、唯一 q、r split22、同 β 拒絕及 degree／full lifts | 合同4的三環、單 bridge、無旁支及雙 private witnesses |
| [BR-SD-1c](../../../../../audits/2026-10-11-br-sd-1c-fd6e1112/PROOF.md) 與 canonical 合同 | 沿用1a共同前提；全部原 W 屬原分量，附件／唯一 q／S pair／split22 全保 | W 只接 J1/J2、未改動 J3／q 外臂與 terminal lemma |
| [BR-SD-1e](../../../../../audits/2026-10-11-br-sd-1e-337d018b/PROOF.md) 與 canonical 合同 | 同一完整 C／S 及原 W 附件保共同前提與兩個 r-contacts | W 只接 J3／q 外臂及雙 private-witness preservation |
| [BR-SD-1g](../../../../../audits/2026-10-11-br-sd-1g-dbdc4c35/PROOF.md) 合同1–4、6–7及 canonical 八項合同 | W1/W2 的原 ownership／完整附件保 S 為完整分量；無額外 s-contact，r split22 | J1 triangle、兩份 W 的數量／位置與 J2 witness／palette 屏障 |

四份各自的 G／M、完整 Σ、critical／minimal witnesses、contacts、attachments、ownership、
rotation、原 bridges、共同 literal 色框、完整 relations／空 fibres／full lifts 均保留。
共同證明只使用上述必要資料；沒有把 components 各自正規化，也不以邊際禁色或抽象 palettes
替代原圖。四份歷史 scoped 排除及獨立採納證據保留；新共同證明本輪未另經獨立審查。

## 6. 精確界線與紙面例子

以下為直接可驗的抽象 degree-list 例子，不是 N45／disk 來源實現或有限搜尋證書。

- **單一 r-contact 可存活。** C=K₂，兩點 r、q 的 lists 都為 `{T}`，
  S={q}，D≠T。C 不可著色且滿足全部命題前提；結論只限制其出口與路徑，不排除它。
- **r 的原 list 不必缺色。** 路徑 z–r–q 的兩個 bridge palettes 分別為 `{D}`、`{T}`。
  原 lists 為 `{D}`、`{D,T}`、`{T}`，不可著色。S={q}；S 側計數必把 r 當出口葉。
  若只取選中 forest 的子樹 r–K_rq–q，原 list 缺口只有 q，(1) 的右側卻為2；
  這也證明「完整連通分量」不能換成「任意連通子樹」。
- **S 可有路徑外的非 bridge block。** 取 bridge rq palette `{T}`、triangle qab
  palette `{A,B′}`，再在 a、b 各接一個只共該點的 triangle，兩 palettes 都為 `{T,D}`。
  incident palettes 互斥且生成 degree lists，故 C 不可著色。S=C−r；唯有 q 缺 D，
  r–q 路徑只有 bridge rq，而 S 含三個 triangles，q 也不是 C 的末端。

共同排除未涵蓋：r 對 S 只有一個 contact；S 有多個 s-contacts；原附件未保所需 pair
而雙色 list 條件尚未另證；或 S 只是片段、有 r 以外的內部出口。
失去 pair support 只表示這份原圖接入失效；若仍能直接證明雙色 lists，抽象定理仍適用。
「旁支多／位置不同／三環形狀不同」本身已不是存活理由：只要共同前提與至少兩個
r-contacts 全部成立，任意有限形狀都排除。

完整 N45-S-NOU-LS-PAIR、其他 core／原55、一般 N45／N2／E、ε≥3、一般單側／共同出口、
R31 任意長來源 minor 與 `K∞=K≤5` 均不因本結果完成。
本輪沒有建立有限來源存在，也沒有把舊 `not triggered` controls 升級。
驗證、傳播停止及本地提交範圍見 [整理紀錄](../../../../history/2026-10-11-two-color-single-gap.md)。
