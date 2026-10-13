# 去四色定理的可轉移範圍：大小餘裕、任意界面與共同 gadgets

2026-10-13。本稿只使用本 audit 的 frozen 輸入，BASE `6943561`。
它是新的條件紙面推論，不修改舊報告的四色定理依賴標記。

**結論。** 原 C8 共面識別只是更一般「相對頂點界」的一個實例。
固定全域最小目錄外 C5 來源的內點数 \(k\)，任意 loopless planar 圖

\[
|V(J)|\le k+5
\]

均有完整四色染色。故一張有 \(n\) 點的原圖 \(H\)，加入 \(a\) 點並合法
識別而減少 \(d\) 點後，只要所得圖平面、沒有真正的 inequality loop 且

\[
\boxed{n+a-d\le k+5,} \tag{1}
\]

便得到**同一原 \(H\) 的一份完整染色**，共同滿足該次構造的所有條件。
這不依賴界面長度、C8 型、度數界或固定層寬。它不能保證某個預先指定
boundary row，也不能把分開所得的 witnesses 合併。

## 1. 凍結前提及基礎下降

直接輸入：

- [no4ct dependency §§1–3](../frozen/audits/2026-10-13-c5-no4ct-dependency-6cafdfb/REPORT.md)。
- [C8 geometry §§4–6](../frozen/audits/2026-10-13-c5-no4ct-c8-6cafdfb/geometry/PROOF.md)。
- [相對 C4 度數修復](../frozen/audits/2026-10-13-c5-no4ct-degrees-6cafdfb/REPORT.md)。
- [W5 完整具名關係](../frozen/docs/c5_w5_marked_relation.md)。
- [W5 小代表報告 §§2、4、6](../frozen/audits/2026-10-13-w5-small-representatives-6cafdfb/REPORT.md)。

\(K\) 是固定的 132 個具體完整 C5 關係；已知 \(932\notin K\)。
假設存在目錄外 C5 disk，令 \(k\) 是**所有**此類來源中最小的內點數。
此處不用最大邊數選取，亦不用 \(k\ge16\) 或後續 C8 分類。

frozen dependency 的引理 A 是：若有至多 \(N\) 點的不可四色平面圖，
便有 \(\Sigma(D)=932\) 的 C5 disk，內點數不超過 \(N-6\)。其證明先取
頂點最少的不可四色平面圖，補成三角剖分，用低度縮減及 Euler 找五度點，
刪去該點。較小平面圖可染性来自這次反例最小性，沒有調用四色定理。

因此，若 loopless planar multigraph \(J\) 有至多 \(k+5\) 點而不可四色，
先刪除平行副本，再用引理 A 得

\[
k(D)\le |V(J)|-6\le k-1,
\]

與全域最小 \(k\) 矛盾。這就證得本文首述的相對可染性。
圖 \(J\) 不必是 C5 disk，不必是原來源的子圖，也不必包含原外框。

## 2. 一般 construction / pullback 引理

固定原圖 \(H\) 的全部頂點名字、邊與共同色集 \(\{0,1,2,3\}\)。
允許在原圖外或指定空面加入 \(a\) 個新點、inequality edges，以及只供
識別用的 equality 連接樹。等式連接線是 contraction scaffolding；
它們不是要被 proper 染色的原邊。

施行全部識別後，令 \(\pi\) 是從原點與新點到商圖 \(J\) 的具名映射，
令 \(d=n+a-|V(J)|\)。要求：

1. 原 \(H\) 每条邊、每条新 inequality edge 的兩端在 \(\pi\) 下互異，
   且像邊保留於 \(J\)；只可簡化平行副本。
2. \(J\) 有平面嵌入。原空面內的共同不交叉 construction 是充分證據；
   单独检查每条操作的平面性不夠。
3. 式 (1) 成立。樹上新點若隨收縮消失，同時計入 \(a\) 和 \(d\)，
   不能漏算最後保留的 gadget 頂點。

由 §1 取一份完整 \(J\) 染色 \(c\)。\(c\circ\pi|_{V(H)}\) 是同一原
\(H\) 的完整 proper 染色，且全部被識別點同色、所有新 inequality
關係異色。這是一份共同 witness，證畢。

更抽象地，只要直接給出 loopless planar \(J\) 及保原邊的具名映射
\(\pi\)，同一論證成立；空面收縮只是方便核對幾何的一種充分構造。
此結論是某份完整染色的存在性，**不是**完整關係相等、fibre 雙射或
可替換 \(H\) 的小代表定理。

精確大小表如下；其中 \(a,d\) 均指同一次共同構造。

| 保留的原圖 | 原頂點數 \(n\) | 可用條件 |
| --- | ---: | --- |
| 原 C5 來源 \(G\) | \(k+5\) | \(a-d\le0\) |
| 刪 \(t\) 個原點後的圖 | \(k+5-t\) | \(a-d\le t\) |
| 刪掉五個原外框點的內圖 \(H\) | \(k\) | \(a-d\le5\) |
| 刪掉一個 W5 中心後的 \(G-v\) | \(k+4\) | \(a-d\le1\) |

「五點餘裕」來源是刪掉原 C5 框，並非任何平面圖免費附帶五點。
原 \(G\) 外加五輪中心有 \(k+6\) 點，仍在引理界外。
若同時有真正合法的識別，可用其實際 \(d\) 抵銷新點；但等式、gadget
與原圖必須一起實現，不能先分別得到染色再宣稱抵銷。

## 3. 任意長 facial boundary、等式與不等式

令 \(C=(c_0,\ldots,c_{b-1})\) 是 \(H\) 的任意長簡單 facial cycle，
指定可用的一側 disk。取 \(C\) 上 noncrossing partition \(\rho\)，
且每個 block 在**整張 \(H\)** 中獨立；若 \(C\) induced，只須檢查
block 不含環上相鄰點。對有 chord 的 \(C\)，只檢查環邊並不足夠。

在該 disk 為各 block 畫彼此不交叉的連接樹並收縮。
若 block 數為 \(q\)，所得圖有 \(n-b+q\) 點，且無原邊變成 loop。
因此，只要 \(n-b+q\le k+5\)，存在一份完整 \(H\) 染色在每個 block
常值。不同 blocks 可再同色。特別地，\(n\le k+5\) 時，所有這類
partition 均給出必要正性，**沒有 C8 或固定 \(b\) 限制**。

還可加入 inequality pattern，甚至帶輔助點的外側 planar gadget。
精確要求是它與 equality trees 在指定 disk 中有**共同**嵌入，或
最後商圖另有已證平面嵌入。純 edge pattern 不花頂點數；輔助點及
識別按式 (1) 計帳。單說「商後 pattern 抽象上 outerplanar」不夠：
原 pins 的循環次序及 equality blocks 的多次出現位置仍須保存。
即使没有等式，按 \(0,1,2,3\) 排列的四點上，兩邊 \(02,13\) 組成
抽象 outerplanar matching，卻不能同畫在指定外側 disk 中。

令 \(x_H(p)\) 是具名界面 literal row \(p\) 的完整延伸數，\(R_T\)
是同一 gadget 的 boundary relation，包括等式及不等式。合法共同
construction 的結論是

\[
\boxed{\sum_{p\in R_T}x_H(p)>0.} \tag{2}
\]

這保證與完整 support 有交集；它不保證 \(R_T\) 的每列都延伸，亦不
給任何指定外框 \(\beta\) 的 positivity。若還要求固定其他 pins，
就必須在同一次 construction 裡實現該要求，重算平面性及大小。

## 4. 新的具體適用族：長圈 hub 與多空面共同要求

若 \(H\) 有 \(k\) 點，且 \(C_b\) 是外側可用的任意長簡單 facial
cycle，在其空 disk 加一個只接全部 \(C_b\) 點的 hub。
新圖平面且有 \(k+1\le k+5\) 點，所以有完整四色染色。
限制回 \(H\) 得

\[
\boxed{\exists\eta\in\mathcal C(H):
       |\eta(V(C_b))|\le3.} \tag{3}
\]

當 \(b\) 為奇數，環上必恰用三色。這是任意長內圖界面的可用必要條件，
不需要內圈固定為 C8。它沒有宣稱整張 \(H\) 可三色。

更一般，對 \(H\) 中 \(q\le5\) 個不同的指定 disk faces，各在空面
放一個 hub，所有 stars 在各自空面共同畫出，便有 \(k+q\le k+5\)
點。故存在**同一份**完整 \(H\) 染色，使這 \(q\) 個 face boundaries
全部至多用三色。各圈缺少的顏色可以不同。
若要求 hub 之間有額外 inequality edges，須再次檢查共同平面性。

它適用於保留內圖的完整 row 上界：若上界拒絕所有滿足式 (3) 或其
多面共同版本的 rows，便可排除該來源上界。它不能在删掉原外框後
私自補回特定 collar row；原來源的完整 collar constraints 仍須
與同一內圖 witness 共同相容。

任意 separator 並不自動是一個可用空面。若 separator 兩側都已有
原邊，不能穿過其中一側放 gadget。可以先取其中一個 cap 作 \(H\)，
但所得 witness 只屬該 cap；把它接回另一側仍需要完整共同界面 join。

## 5. 多 separator 的精確 join 本身完全不需四色定理

令任意有限原圖 \(F\) 被分成 pieces \(F_i\)，所有原邊至少在一片中。
令 \(S\) 包含所有片間共用的原頂點；不同片的私人頂點彼此不交，
所有 shared pins 使用同一物理頂點名字及同一 literal 色值。
對已固定的外部 row \(\beta\)，把與它相容的所有 \(S\) 色列記作
\(\tau\)。若 \(\mathcal C_{F_i}(\beta_i,\tau_i)\) 是完整 piece
fibres，則逐份限制及黏合給自然雙射

\[
\mathcal C_F(\beta)\cong
\bigsqcup_{\tau}
\prod_i\mathcal C_{F_i}(\beta_i,\tau_i). \tag{4}
\]

若按完整 literal rows 計數，式 (4) 就是逐列的 sum-of-products。
若沒有預先固定的外框 row，改用共同 S4 canonical rows 時須恢復
每個共同 row 的 orbit size 權重；若已固定 literal 外框 row，
只能在保該 row 的換色子群下取軌道及相應大小。
不能把兩片的界面各自正規化後直接相乘。

這只是 properness 逐原邊核對：所有共用點已取相同色值，所以每個
tuple 唯一黏成全圖染色；反向限制唯一。空 fibres 及空私人圖均保留，
後者對合法既定 pins 有恰一份空 assignment。橋的兩端仍須異色。
面歩行中同一原點的多次出現，必须用同一 \(\tau\) 值。

式 (4) 適用任意長、任意多、巢狀或非環狀 separator，也不要求
平面性、最小性或可染性。可是它不給非空性，不保證固定寬度，也不
把 pieces 分別非空升格為 full join 非空。只有把全部要求共同做成
§2 的一張合格 \(J\)，才能由相對大小引理額外推出共同非空。

## 6. 有限反控制：分開可染不能合併

取實際 wheel \(W_8\)：rim 順序 \(u_0,\ldots,u_7\)，內 hub \(z\)
接全部 rim 點。四個非鄰對為

\[
P_0=(u_0,u_3),\quad P_1=(u_1,u_5),\quad
P_2=(u_2,u_7),\quad P_3=(u_4,u_6).
\]

每對都可单独在原外面識別；它們也各有明確完整染色。例如 rim
`01201012`、hub `3` 同時滿足 \(P_0,P_2\)；rim `01010101`、hub `2`
同時滿足 \(P_1,P_3\)。但四對合併後，四個 rim blocks 之間的原環邊
恰包含 \(K_4\) 全部六對，原 hub 又接四 blocks，故商圖為 \(K_5\)
（平行副本簡化後）。因此四對不可能由同一完整染色滿足。

[check.py](check.py) 直接枚舉原 \(W_8\) 的全部 literal 完整染色，
不使用四色定理或圖庫：

| 全部 lifts | \(P_0\) | \(P_1\) | \(P_2\) | \(P_3\) | 四對共同 |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1032 | 240 | 432 | 240 | 528 | 0 |

此反控制也說明：即使總頂點數下降很多，若同時商圖不平面，就不能
使用相對大小結論。反例來自實際固定原圖，沒有拼接獨立正規化的 masks。
它沒有聲稱 \(W_8\) 是真正最小目錄外來源。
重播輸出保存在 [RESULTS.json](RESULTS.json)，由
`python3 -B audits/2026-10-13-no4ct-generalization-6943561/transfer/check.py`
直接產生。

## 7. 可移除依賴與保留的邊界

- 可以：把原 C8 的 91 份 noncrossing positivity 解讀為任意長度
  版本的特例；加入相容的外側 inequality pattern；對内圖使用
  最多五個保留輔點的共同 gadgets；沿任意 separator 使用式 (4)。
- 可以：若某張 induced-boundary 圖有 \(n\le k+6\) 點，對每一
  共面非鄰對单独識別後至多 \(k+5\) 點，故各有完整同色 witness。
  因而任何與它完整 boundary relation 相同的代表都不能含該對 chord。
- 尚不能：把 W5 小代表報告 §4 對**任意大小** induced-B 來源的
  普遍 chord 排除直接標成已去 4CT。本文仅供上述相對大小範圍；
  arbitrary-size 來源沒有自動的 \(n\le k+6\) 保證。
- 尚不能：指定每個 row 可延伸、從商圖 positivity 還原 W5 的
  multiplicity-two full lifts、構造一般小 annulus 代表、證固定層寬，
  或排除無界 932／933／941。尤其原 \(G\) 加外側 wheel 中心仍超界。

相對可染性的證明入口、具名 full-lift join、有限 \(W_8\) 控制及一般
來源實現是不同證據層。本稿沒有新增 Lean theorem，也沒有重跑
K15 或外部有限計算。一般 \(K_\infty=K_{\le5}\) 仍 OPEN。
