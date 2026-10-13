# 3903：空交集分支的末端 block 排除

系列索引：[3903 導讀與推導順序](c5_sector_3903_guide.md)。

後續狀態（2026-09-23）：[雙拒絕分類](c5_two_rejection_proof_zh.md)
已在指定 induced-C5 disk／連通內部／degree≤4／兩接點圖類內排除
一般 3903，無須假設 397→330 交換。以下「不是一般 3903 排除」
仍準確描述本報告局部論證的範圍；一般排除須引用後續分類。

發布紀錄：本報告與相關證書合併於 [STATUS §70](STATUS.md#70-3903-空分支後繼與-331-四輪成果發布)；
以下「未提交」及停止點描述本研究輪當時狀態，目前入口見 [HANDOFF](HANDOFF.md)。

後續：[全部後繼核對](c5_sector_successor_audit.md) 確認 action 2 有十個存活
後繼；禁 330 後可改選 331，單條禁令不縮小原 603 閉合集合。
以下保留本輪圖層成果與當時的下一問。

2026-09-22，接續尚未提交的 [空分支身份與葉點排除](c5_sector_empty_branch.md)。
**在指定 397→330 單次交換與 3903 兩拒絕列的共同前提下，
N(0)∩B₃=∅ 分支亦不可能是 disk。** 與前輪非空排除合成，
這一指定交換不能在該 sector 中發生。
這不是一般 397→330 排除：既有接受全部開口列的 disk 控制仍保留。
也不是一般 3903 排除：尚未證明任意 3903 必須具有這個交換。

## 1. 精確前提與 Gallai 化約

沿用前報告同一 G、C、Γ、c、S、c′、B₃；K=G+{01,04} 以 Γ 為
induced disk 外框，C 非空連通、內點完整 degree≤4、deg_G(0)=2。
舊框列 01021，S∩Γ={0,1,2}，原始新框列 10121；交換前後完整框分割
分別為 397 與正規化 330。另要求同一圖拒絕 α=01212、δ=01213。
本輪假設 N(0)∩B₃=∅。

前報告已給出每內點完整 degree=4、δ(C)≥2，以及一個實際內點 b：

```
c(b)=1，b∈N_G(0)∩S，A(b)={0}，deg_C(b)=3。
```

不限定另一個 0 鄰點的顏色，不引入 w,p,q,r，不假設 corner 次序。
對 β∈{α,δ}，Lβ(v)=U\β(A(v)) 的大小恰為 deg_C(v)，且 C 不可染。
依 [degree-choosability 定理](https://arxiv.org/abs/1511.00350)，C 是 Gallai tree。
proper c 排除 K5；內部最大度數≤4，所以 blocks 只有 bridges、奇圈、K4。
δ(C)≥2 排除末端 bridge，未排除中間 bridges。

## 2. 單一 block 先排除

若 C 只有一個 block，bridge 與 δ(C)≥2 矛盾，奇圈與 deg_C(b)=3 矛盾。
剩餘 C=K4 時，每點恰有一個框鄰居；deg_G(0)=2 迫使恰兩點鄰接 0。
對 α，它們的 list 為 {1,2,3}；另外兩點的 list 禁色為 1 或 2，故含 0。
選後者之一先染 0，剩餘 triangle 的 lists 至少二色，其中前兩點仍有
三色。以其中一個有餘量的點作根，貪婪染完 triangle，得到 α 延拓，矛盾。
此處使用完整四點圖，不把末端 block 的「私有三點共同」偷套到無 root 圖。

因此 C 至少有兩個 blocks，block-cut tree 至少有兩個末端非平凡 blocks。

## 3. 每個末端 block 都避開所有 0 鄰點

取末端 B，唯一 cut vertex 為 x，令 H=C−(V(B)\{x})。
H 連通。重用 [完整 root 接合](c5_sector_terminal_blocks.md#1-精確前提與單一-block-接合)：
令 Rβ 是 x 暫用完整 U 時的 block root 色集，Fβ=U\Rβ，則
在 H 將 x 的 list 改成 Lβ(x)\Fβ，恰等價於原圖延拓。

奇圈的 |Fβ|≤2，且等號恰當所有私有 lists 是同一 pair Pβ；
K4 的 |Fβ|≤3，等號恰當三個私有 lists 是共同三色 Pβ。
若消去 block 後 x 的 list 嚴格大於 deg_H(x)，H 由根餘量貪婪可染，
再由 root 介面接回便與拒絕矛盾。因此每一列必有
**Fβ=Pβ⊆Lβ(x)**，且所有私有 lists 共同。
這部分只用 root 接合、degree 緊性與拒絕，不用非空分支身份。

兩列共用同一實際 attachments，奇圈私有點只有五個共同類：

| A(v)，其中 i∈{1,3} | Pα | Pδ |
| --- | --- | --- |
| {0,i} | 23 | 23 |
| {0,2} | 13 | 13 |
| {0,4} | 13 | 12 |
| {i,2} | 03 | 03 |
| {i,4} | 03 | 02 |

前三類至少有兩個私有點鄰接 0。每個私有點的內部度數為 2，故都不是
deg_C(b)=3 的 b；連同 b 便有至少三個 0 鄰點，違反 deg_G(0)=2。
這不需知道 b 在 root 還是 block 外。

只剩共同框點 j=2 或 4 的後兩類。私有點不鄰接 0；兩列 Pβ 均含 0，
Pβ⊆Lβ(x) 又禁止 x 鄰接 0。所以 **B 中沒有任何 0 鄰點，特別是 b∉B**。

K4 的共同私有類為全部接 0、全部接 2、全部接 4，或逐點選 1／3。
全部接 0 需要三個 0 鄰點，立即矛盾。其他類私有點避開 0；root 有三條
K4 邊及至少一條 H 邊，完整 degree=4 使 A(x)=∅。所以 K4 亦有 b∉B。

於是每個剩餘 B 都有 **H 中的簡單 x–b 路徑接上 b0**，記為 Z。
Z 的內點全在 C−B，除 x 外不碰 B，除終點 0 外不碰任何框點。
它可以經過任意多個中間 bridges；沒有刪除或縮短原圖中的那些 bridges。

## 4. 來源路徑上的拓撲合成

在 K 外面加 apex z 並連到五個框點，disk 前提保證增廣圖 planar。
以下直接用同一來源的 Z，沿用既有 branch-set 構造；z 僅是 exterior apex。

- **K4**：四個 block 點各一組；第五組取 z、0、全部私有框鄰點及
  Z 的內部。此組連通且碰四個 block 點，得到 K5 minor。
- **長奇圈**：將圈分成三個連通、兩兩相鄰且各含私有點的組；另取
  {j}、{z,1,3}，得到 K5 minor。
- **三角形私有點同選 i**：兩個私有點及 {z,0}∪Z內部作一側，
  {i}、{j}、{x} 作另一側，得到 K3,3 minor。
- **三角形混選且 j=4**：框路徑 1–u–4 與 0–Z–x–v–3 頂點互斥，
  框端點交錯，違反 disk；另重播明示 subdivision。
- **root 再鄰接 j**：三角形三點、{j}、{z,0,1,3}∪Z內部給 K5 minor。

所以唯一未被單 block 拓撲排除的必要型是

```
B=xuvx，A(u)={1,2}，A(v)={2,3}，A(x)=∅、{1} 或 {3}；
Fα=Fδ={0,3}，且 b∉B。
```

沒有識別框點 2、4，也不把 root 色集換成逐點 list 多重集。
這一單 block 的局部 disk 控制仍然有效，不是整個 sector 的實現。

## 5. 兩個末端 blocks 的矛盾

§2 保證至少兩個末端 blocks，§4 迫使它們都是上述三角形。
若兩者共用 root x，四條圈邊用滿 x 的內部 degree≤4；私有點又沒有
圈外內邊。C 連通便迫使 C 恰是這兩個三角形，其內部度數只有 2、4，
與實際 b 的內部度數 3 矛盾。因此兩個末端三角形頂點互斥。

各取整個三角形及 {z} 為三個 branch sets，另一側取 {1}、{2}、{3}。
每個三角形都碰到這三個實際框點，apex 亦然，得到 K3,3 minor。
不需要改動兩個三角形之間的任何 blocks 或 bridges。空交集分支排除完成。

合併既有非空分支排除，得到：**具上述 sector 結構、同時拒絕 α、δ 的
disk，不可能以指定 maximal 01 分量實現完整 profile 397→330。**
兩個 B₃ 分支窮盡這次指定交換，但未窮盡所有交換或 3903 的全部實現。

## 6. 證書、信任範圍與下一步

[checker](../scripts/c5_sector_empty_terminal.py) 與
[JSON](../artifacts/c5_sector_empty_terminal/observations.json) 保存五個共同
attachment 類、96 個單 K4 接線的 α 著色、共用 root 度數控制。
直接核對既有 177 份 minors，再將十個代表構造的接回路徑替成長度
1、2、5 的 x–b 路徑，保存 **30 份 lifted minors、3 份 lifted subdivisions**。
每個 lifted skeleton 都核對 A(b)={0}、deg_C(b)=3、來源邊、branch sets
連通與互斥；沒有 branch set 同時含框點 2、4。
這些只是局部必要配置，其餘內點未補全度數，不是新 sector 候選或 disk 實現。
任意路徑長度與任意 block tree 的論證由 §1–5 紙面證明承擔。

原先的三色 root、循環次序、局部 disk 與 bridge 奇偶控制沿用並由
terminal-blocks standalone 重播。checker 不用 NetworkX 或 planarity oracle。
Gallai 化約依賴外部 degree-choosability，disk 路徑／minor 論證尚未 Lean 化。

下一個窄問題回到 [抽象交換表](c5_sector_cross_row.md)：核對 397 的指定
action 是否只有 330，或 330 只是已保存的一個可選後繼；再把這個
**有結構前提的轉移禁令**與同圖其他後繼聯立。不能由一條轉移不可能，
直接刪除來源 profile 或宣稱一般 3903 排除。
本輪維持 603 profiles、零刪除、固定點未重算；R31、一般 3903、共同出口
及 K∞=K≤5 仍未證，未 commit／push。

```bash
uv run python scripts/c5_sector_empty_terminal.py --check
uv run python scripts/c5_sector_empty_branch.py --check
uv run python scripts/c5_sector_terminal_blocks.py --check
lake build
git diff --check
```

本輪以上三份 checker、依賴 hashes、Lean build、變更文件連結及 whitespace
通過。rejection-lists 與 saturated-cuts standalone 沿用上一輪核對；
transition-control、其他 standalone、minimality 與 R 系列未重跑。
