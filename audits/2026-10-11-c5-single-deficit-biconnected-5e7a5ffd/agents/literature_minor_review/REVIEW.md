# 正式版文獻與 minor 構造獨立核讀

BASE：`4dd11f422c6fa49265a412085116b088786d0344`。本子工作只寫本專屬目錄，沒有修改共享文件、舊證書或其他工作者輸出；沒有來源枚舉、commit、push 或發布。

## 文獻身份與視覺核讀

Daniel W. Cranston and Landon Rabern, *Beyond Degree Choosability*, The Electronic Journal of Combinatorics **24**(3) (2017), #P3.29；正式版載明 Published: Aug 11, 2017，共 14 個印刷頁。原始 PDF：<https://www.combinatorics.org/ojs/index.php/eljc/article/download/v24i3p29/pdf/>。PDF SHA-256：`8b6b26981671cb839f96667653913e63b690d917a891483d32a44e1d1adc2271`。

已直接視讀所存正式 PDF 的印刷第 2、3、4、11、12 頁，圖像保存在 `formal-02.png`、`formal-03.png`、`formal-04.png`、`formal-11.png`、`formal-12.png`。Figure 1 另有 450 dpi 裁圖 `figure-04.png` 與原 PDF 的 Cairo SVG 向量轉出 `figure-page4.svg`。PDF 文字抽取只作定位，沒有用文字抽取代替圖的核讀。

第 2 頁 Theorem B 是 f-AT ⇒ f-choosable。第 3 頁 Main Lemma：對二連通 H 與指定點 s，(H,h_s) 為 AT 當且僅當下列之一：(i) d_H(s)=2 且 H−s 不是 Gallai tree；(ii) d_H(s)≥3，H 不 complete，且 (H,h_s) 不屬於 D。否定後，當 d_H(s)≥3 时非 AT 的所有例外確為 complete 或 D，沒有另一個高內度 odd-cycle 分支。

第 11 頁 Theorem 3.6 是 connected 版本，其非 AT 的例外依次包括 Gallai tree、d_H(s)=1、d_H(s)=2 且 H−s 有 Gallai-tree 分量、根所在 D-block 加其他 Gallai blocks、以及根為 cutvertex 的 lobe 例外。這個版本不能把「有一個 Gallai-tree 分量」改寫成「全部 H−s 為 Gallai tree」。第 12 頁 Theorem 4.1 證明 connected 單 deficit pairs 的非 choosable、非 AT 分類一致，亦涵蓋 paintable。當有兩個 deficit roots，該文已說明三種分類不再一致；不能把單根 Main Lemma直接套到雙根。

## Figure 1：三 seed 與允許 stretches

令 s 為 Figure 1 上的 label 1。

1. 左 seed 是 K4：其餘三點 a_1,a_2,a_3 構成 unbolded triangle；三條 s a_i 全為 bold。每次 stretch 將指定 bold edge subdivide twice。任意次重複後三條 spoke paths P_i 各有奇數長度 1+2k_i。
2. 中 seed 是上述 K4 的三條 spoke 各 subdivide once；每條 spoke 的兩個 edges 全為 bold，共 6 個 bold edges。若分別 stretch 六條原 bold edges 0 次以上，三條 P_i 各有偶數長度 2+2k_i；k_i 是該 spoke 上 stretch 次數總和。三角形的三 edges 不允許 stretch。
3. 右 seed 是 Moser spindle，沒有任何 bold edge；故 D 的此支只有該 seed，不允許由此伸長任意 edge。

高解析圖與 SVG stroke width 同時確認 bold counts 3/6/0。`figure-page4.svg` 第 523–525 行為左 seed 三 spokes 的 stroke-width=2.98883；第 521–522、526 行 triangle 是 0.79701。第 558–563 行為中 seed 六 spoke edges 的 2.98883；第 555–557 行 triangle 是 0.79701。第 592–602 行 spindle 全部 11 edges 是 0.79701。本段是圖像／向量交叉核讀，不是有限來源枚舉。

## 無界 D 家族的 K4 branch sets

對左、中 seed 的所有允許 stretch，同時令

- Q_0={s}；
- Q_i=V(P_i)\{s}，i=1,2,3。

每個 Q_i 都是非空 connected vertex set，四者互斥。Q_0 與每個 Q_i 由 P_i 第一 edge 相接；Q_i 與 Q_j 由原 triangle edge a_i a_j 相接。這直接給出 K4 minor 的四個 bags，與 spoke 長度、stretch 次數及奇偶無關；不用先縮成另一張無附件圖。

Spindle 用如下名字標記原點：根 s；左半 diamond 的其餘三點 a,b,e；右半 diamond 的其餘三點 c,d,f。edge set 是

`sa,sb,ab,ae,be,sc,sd,cd,cf,df,ef`。

四個 K4 bags 為

`Q_0={s,c,d,f}, Q_1={a}, Q_2={b}, Q_3={e}`。

Q_0 由 sc、sd、cf、df connected，其他三 bags 是 singletons。六個 bag-pair edges 可取 `sa,sb,fe,ab,ae,be`，因此也是同一原 H 的明確 K4 minor。

## 完整 M degrees 強迫原 B 附件

因 H=M−V(B) 是刪除 B 後的 induced graph，對每個內點

`t(v)=|N_M(v)∩V(B)|=d_M(v)−d_H(v)`。

在兩個 spoke seeds 的所有允許 stretches中：d_H(s)=3，故 t(s)=5−3=2；三角點的內度為 3、完整 M degree 為 4，故 t(a_i)=1；所有 spoke 內點（含中 seed 原 subdivision 點）內度 2、完整 M degree 為 4，故 t=2。Spindle：d_H(s)=4，故 t(s)=1；其餘六點 d_H=3，故 t=1。因此每一 D 頂點都在同一原 M 中有至少一條真實 B-spoke。

此計數不是從 G 中的 degree、另一張 reduced graph 的 degree 或抽象 list tightness 導出；必須在此原 M 內計算完整 degree。拒絕本身不要求 lists 全緊。

## 同一原 M 的 K5 lift 與 complete 情況

將上述四個原 H bags 保留，並加入 Q_4=V(B)。原外框 C5 使 Q_4 connected；Q_4 與四個 H bags 互斥。每個 Q_i 均含某個有原 B-spoke 的頂點，故它與 Q_4 有一條原 M edge。原 K4 的六個 bag pairs 已有原 H edges，至此五個 bags 的十個 pairs 全相接，構成原 M 的 K5 minor。planar disk 因而不可能有 D 高內度例外。

若 H complete 且 d_H(s)≥3，令 n=|V(H)|。存在非根點而其完整 M degree 為 4，故 n−1≤4；因此只有 K4 或 K5。K5 本身已是原 M 的 K5 subgraph。K4 的根有 t(s)=2，其餘三點各有 t=1；四個 singleton H bags 加 Q_4=V(B) 就給原 M 的 K5 minor。n≥6 與非根的完整 degree=4 直接矛盾，不需額外圖論。

此 K5 argument 只用 B 的 connectedness、完整原 degree、原 spokes 與 planarity；沒有把 boundary contacts 改到新的 frame，也沒有要求 frame bags 的 spokes 用相異 B 端點。把整個 connected B 當成一個 bag 正好允許不同 bags 的 spokes 共用 boundary endpoints。

## list 化約及最後一步的獨立檢查

對 proper 原 B-coloring β，定義 L_β(v)={0,1,2,3}\β(N_M(v)∩V(B))，則

`|L_β(v)|=4−|β(N_B(v))| ≥4−t(v)=d_H(v)−1[v=s]`。

原 M 的 extension 與 H 的 L_β-coloring 等價。令 f(v)=d_H(v)−1[v=s]。因 H 二連通，f(v)≥1。若 β 拒絕，逐點任取 f(v)-元素 subset L'(v)⊆L_β(v)；若 H 可由 L' 著色則亦可由 L_β 著色，矛盾。因此這個 L' 是恰 f-sized 的拒絕 assignment，證實 H 非 f-choosable。由 Theorem B 反向否定得 (H,h_s) 非 AT；這個推理沒有假定原 L_β 全緊。

Main Lemma 與上述 K5 排除高內度，二連通給 d_H(s)≥2，故 d_H(s)=2；再次由 Main Lemma 得 H−s 為 Gallai tree。也可獨立重證最後一步：H−s connected；先取 c∈L_β(s) 給 s 著色，再從 s 的鄰居 lists 刪 c。每個非根 v 的剩餘 list 至少 d_H(v)−1[vs∈E(H)]=d_{H−s}(v)。若 H−s 不是 Gallai tree，正式版第 2 頁 Theorem A 將它著色，便延拓 β，矛盾。

## 裁定與證據邊界

指定前提下推論成立，紙面證明可依正式版 Theorem B + Main Lemma + Figure 1，並以 Theorems 3.6／4.1 校準 connected／choosability 界線。任意大小由上述參數化 branch sets 直接涵蓋，不由 finite controls 外推。此核讀没有新增 Lean theorem；不能從此推出全部 45/54/55、ε≥3、一般出口、K∞=K≤5 或雙 degree-5 分類。

本子工作的四份指定輸入 SHA-256：

- docs/HANDOFF.md：`3a5f57439de95350fc322ab6a9a7062782a7fcb7b293e4563e1cae2f65d9299f`。
- docs/STATUS.md：`b77fa94239f8cb411ac4c5d3f0eed1bd3d4c8b6a22410e518ee8cdefc3ec6aac`。
- docs/c5_weak_list_cores.md：`49929fbc63a64ba093413a4ff2a80ef5eb4033835de4fd96167c784b6accfee3`。
- docs/c5_degree5_guide.md：`6a2517e3b939c6384338ba264a96c0d99067823d0f9f6c18420a62563e257fab`。
