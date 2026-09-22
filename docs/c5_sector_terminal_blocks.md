# 3903：末端 block 的兩列 root 接合與非空分支排除

後續：[空分支末端 block 排除](c5_sector_empty_terminal.md) 已完成空交集分支；
合併非空分支，只排除具指定 sector 前提與兩拒絕列的 397→330 交換。
一般 3903 仍開放；以下保留本報告研究輪的狀態。

2026-09-21，從乾淨 `1c608a8` 接續
[拒絕列緊 list](c5_sector_rejection_lists.md)。
**在既有非空分支、同一實際圖／attachments、第二種 corner 的前提下，
01212、01213 不可能同時被拒絕。故此非空 3903 分支不存在。**
空交集分支及一般 3903 仍未解；沒有刪除 603 profiles 或重算固定點。

結論先經完整單一 block root 介面，再經 disk 拓撲；不把 12 種逐點
list pair 當作完整 block state。中間 bridges 全程保留，不假設
S′−{1} 中 b、2 連通，亦不假設兩個飽和 stars 存在。

## 1. 精確前提與單一 block 接合

沿用原 G、C、c、S、c′、J、S′、p,q,r,b,w 的身份。Γ={0,…,4}，
G 保留框路徑 1–2–3–4，K=G+{01,04} 有指定框圈作外面的 disk embedding。
舊框列 c|Γ=01021，c(w)=c(b)=1、c(p)=2、c(q)=c(r)=3；
p,q,r,w,b 互異。C 連通，N_G(0)={b,w}，N_G(w)={0,p,q,r}。
非空分支的第二種 corner 是 `1,4,r,p,q,b`。

引用前報告已證的必要條件：每內點完整 degree=4；對兩個拒絕列
α=01212、δ=01213，Lβ(v)=U\β(A(v)) 的大小都是 deg_C(v)，
其中 U={0,1,2,3}、A(v)=N_G(v)∩Γ。b2 不存在，
A(b)={0} 或 {0,3}，deg_C(w)=3，且 δ(C)≥2。
這些前置條件仍涵蓋刪 1 已切斷 b、2 的情形。

由 [degree-choosability 標準定理](https://arxiv.org/abs/1511.00350)，
C 是 Gallai tree；既有 proper c 排除 K5，故 blocks 只有 bridges、
奇圈、K4。末端 bridge 會產生 C 葉點，已排除。

令 B 是末端非平凡 block，x 是它與其餘 C 的唯一共用點。
在 B−x 上使用實際 attachments 給出的 Lβ；暫時讓 x 的 list 是 U，定義

```
Rβ(B,x) = {a∈U：B 有 Lβ 著色且 x=a}；
Fβ(B,x) = U\Rβ(B,x)。
H = C−(V(B)\{x})。
```

若 Tβ(H,x) 是 H 按原 lists 著色時 x 的完整可用色集，則精確接合為

```
β 可延拓到 C  ⇔  Rβ(B,x) ∩ Tβ(H,x) ≠ ∅。
```

等價地，只須在 H 把 x 的 list 換成 **Lβ(x)\Fβ(B,x)**。
這兩個公式對任意 lists 都成立，並未預設共同 palette 或拒絕。
兩列分別計算色集，但 B、x、所有框鄰接與循環位置完全共用。

### 奇圈的全部 root 色集

寫 B=xv₁…v₂ₘx，每個私有點恰有兩條框邊，Lβ(vᵢ) 是二色集合。
對每個 x 色 a，以 X₀={a} 及下式計算完整 root 介面：

```
Xᵢ={d∈Lβ(vᵢ)：Xᵢ₋₁\{d}≠∅}；
a∈Rβ ⇔ X₂ₘ\{a}≠∅。
```

若所有私有 lists 同為 P，則 Fβ=P；否則 |Fβ|≤1。
證明：若禁了兩色 a,b，讓 x 的 list 為 {a,b}，整圈不可染。
二色-list 圈不可染恰當圈為奇數且全部 lists 相同：若相鄰 lists
不同，可先給一端不在另一端 list 的色，再沿反向路徑貪婪完成。
故所有私有 lists 必為 {a,b}。共同 pair 的反向由奇圈二色交替得到。
因此一般完整 Rβ 可以是二色、三色或四色，不能預先壓成二色。

### K4 的全部 root 色集

三個私有點各有一條框邊、三色 list。若三個 lists 同為 P，則
Fβ=P、Rβ=U\P；否則 Fβ=∅、Rβ=U。
固定 root 色 a 後，剩餘 triangle 的 lists 至少二色；不可染恰當
三個縮後 lists 都是同一 pair。這迫使原來三個 lists 都是該 pair 加 a。

### 拒絕迫使滿額禁色，但共同 palette 本身不充分

設 d_B(x)=k（奇圈 k=2，K4 k=3）。上述介面給 |Fβ|≤k。
消去 B−x 後，其他點仍 list 緊，且

```
|Lβ(x)\Fβ| ≥ deg_C(x)−k = deg_H(x)。
```

若嚴格大於，H 連通，以 x 為生成樹根、子點先染的貪婪論證便可完成
H，再由精確介面接回 B，與拒絕矛盾。因此對每一拒絕列都必有

```
Fβ=Pβ，|Pβ|=k，Pβ⊆Lβ(x)，所有私有 lists 同為 Pβ。
```

仍須檢查 H 的縮後 lists 是否拒絕；不能由共同 palette 單獨推出整圖拒絕。
此步不使用 minimality，也不刪除 H 中的任何 bridge。

## 2. 從共同 palette 回到實際框鄰接

兩列都共同，故每一私有點的 **同一個** A(v) 必屬同一 joint-list 類。
奇圈的完整五類如下；i 可逐點選 1 或 3，不能真的識別這兩個框點。

| 私有點的 A(v) | Pα | Pδ |
| --- | --- | --- |
| {0,i} | 23 | 23 |
| {0,2} | 13 | 13 |
| {0,4} | 13 | 12 |
| {i,2} | 03 | 03 |
| {i,4} | 03 | 02 |

前三類使至少兩個私有點都鄰接 0；但 w 的內部度數 3，不能是奇圈
私有點，唯一剩下的 b 不夠。因此只剩最後兩族，記共同框點 j=2 或 4。
每個私有點 A(v)={i(v),j}，i(v)∈{1,3}；**j 必須全圈一致**。
尤其不能把 α 中同色的框點 2、4 合併。

這兩族的 Pα、Pδ 都含色 0；Pβ⊆Lβ(x) 迫使 x 不鄰接框點 0。
私有點亦不鄰接 0，故 **b、w 均不在末端奇圈中**。
p,q,r 若在其中，只能是 x：私有點不能另有通往圈外 w 的內邊。
所以至多一個具名點 p,q,r 落在這個 block。

對 K4，私有點的框鄰居各只有一個。共同 list pair 只允許全部為 0、
全部為 2、全部為 4、或逐點選 1／3。全部為 0 需要三個 0 鄰居，
與 N(0)={b,w} 矛盾。其餘類的私有點都不鄰接 0；x 的三條 K4 邊
加至少一條其餘 C 的邊已用盡完整度數，A(x)=∅。所以 b,w 也都在 K4 外。

於是對上述每個存活 block，H 中都有一條從 x 到 {b,w} 再到 0 的
路徑 Z；取簡單路徑，其內部避開 B 與所有框點。後面用 Z 作為真實
接回證據，不把抽象 root list 誤當成這條路徑。

代數層的奇圈 root 候選（尚未套用拓撲）為：

| j | A(x) | Lα(x)\Fα | Lδ(x)\Fδ |
| --- | --- | --- | --- |
| 2 | ∅ | 12 | 12 |
| 2 | {1} 或 {3} | 2 | 2 |
| 2 | {2} | 1 | 1 |
| 4 | ∅ | 12 | 13 |
| 4 | {1} 或 {3} | 2 | 3 |
| 4 | {4} | 1 | 1 |

此表保留 root 的原框鄰接；它是精確消去單一共同-palette block 後的
list，而不是整張 H 的 root 可用色集。

## 3. 單一 block 的 disk 排除與精確局部存活型

在 K 的外面加一個新 apex z，接到所有五個框點。disk 前提保證這張
增廣圖 planar。下列 minors 只用於非平面證明；不宣稱是保持 Σ 的化約。
所有證書均檢查**沒有 branch set 同時包含框點 2、4**。

**K4 全排除。** 保留 K4 四點作 singleton branch sets。第五組取 z、
所有私有框鄰點、框點 0 與 Z 去掉 x 的部分；這組連通，碰到 K4 的
三個私有點及 x，構成 K5 minor。共同 attachment 類保證此組不會同時
包含 2、4。這是來源圖上的路徑構造，不依賴其餘部分沒有 bridges。

**長奇圈全排除。** 長度至少 5 時，將圈分成三個互斥連通 branch sets，
各包含一個私有點，且三組兩兩相鄰。例如 {v₁}、{v₂}、{x,v₃,…,v₂ₘ}。
另取 {j} 與 {z,1,3}；它們互相有邊，且各自碰全部三個圈 branch sets。
得到 K5 minor。此論證涵蓋任意長度與任意 i(v) 序列。

只剩三角形 xuv。若 u,v 選同一 i，則兩側

```
{u}, {v}, {z,0}∪(Z 的內部)   versus   {i}, {j}, {x}
```

給 K3,3 minor。因此必須（交換 u,v 名稱後）
A(u)={1,j}、A(v)={3,j}。

**j=4 的混合型亦排除。** 同一 disk 中，路徑 1–u–4 與
0–Z–x–v–3 互斥，而四個框端點循環次序為 0,1,3,4，彼此交錯，矛盾。
第二條路徑的 Z 按 0→x 方向使用。有限模板另外保存 apex 增廣圖的
Kuratowski subdivision，重播直接檢查來源邊與路徑互斥。

**root 不能再鄰接 j。** 若有 xj，取三角形的三個 singleton、{j}、
{z,0,1,3}∪(Z 的內部)，得到 K5 minor。

故單一 block 所剩的精確必要型只有

```
B=xuvx，A(u)={1,2}，A(v)={2,3}；
Fα=Fδ={0,3}，Rα=Rδ={1,2}（尚未加 x 自身 list）；
A(x)=∅、{1} 或 {3}。
```

A(x)=∅ 時 x 在 H 的度數為 2，縮後兩列 list 均為 {1,2}；
A(x)={1} 或 {3} 時 x 以一條 bridge 接回，縮後兩列 list 均為 {2}。
保存三份單 block 的 apex planar rotations 作局部正控制；它們未補全
其餘圖的度數或 transition，**不是非空 3903 的實現**。

### 具名接合點的進一步位置限制

b,w 都不能位於 B；p,q,r 至多一個，且必為 x。
若 x 以唯一 bridge 接回且是 p/q/r，該 bridge 就是 xw。
在 J 刪掉 w 後，此 block 只能經其列出的框邊接回。

| A(x) | x=p | x=q | x=r |
| --- | --- | --- | --- |
| {1} | 局部保留 | 局部保留 | 排除 |
| {3} | 排除 | 排除 | 排除 |
| ∅ | 尚無此局部排除 | 尚無此局部排除 | 尚無此局部排除 |

理由：p 色 2 禁止 p3；在 A(x)={1} 的 p 型，舊 (c(u),c(v))=(3,1)，
v 經框點 2 屬 S，交換後 p–v–3 是新 02 路徑。q/r 色 3 強迫
(c(u),c(v))=(2,1)；若 A(x)={1}，舊 13 接回的是 1，容許 q 卻不容許 r；
若 A(x)={3}，舊 13 在 J 完全沒有通往框的出口，q/r 都不可能。
A(x)=∅ 有另一條圈外內邊，不能沿用「只剩框邊」論證。
表中的保留只表示這些局部檢查未排除，沒有完整 sector 見證。

## 4. 兩個末端 blocks 完成非空分支排除

C 不可能只有一個 block：bridge 與 δ(C)≥2 不符；奇圈與 deg_C(w)=3
不符；K4 中 w 的三個鄰居 p,q,r 兩兩相鄰，卻有 c(q)=c(r)=3；K5
已由 proper c 排除。因此 C 的 block-cut tree 至少有兩個末端 blocks。

由 §2–3，它們全是上述 j=2 混合三角形。兩個末端三角形若共享 x，
x 已有四條圈邊，沒有其他內邊可接出；其他四點又都是私有點。
C 連通便迫使 C 恰是這兩個三角形，所有內部度數只能是 2 或 4，
與 deg_C(w)=3 矛盾。因此任取兩個末端三角形都頂點互斥。

把兩個三角形各自整體取作一個連通 branch set，第三組取 exterior
apex {z}；另一側取 {1}、{2}、{3}。每個三角形都鄰接這三個**實際**
框點，apex 亦然，故得到 K3,3 minor。這個證書根本不需要碰兩個
三角形之間的 blocks 或 bridges，亦沒有合併任何框點。

矛盾完成：**本題非空 3903 分支不存在。** 第一種 corner 的既有排除
不變；本輪第二種排除沒有使用 S′−{1} 中 b–2 路徑的存在，故包括
刪 1 已切斷的分支。一般 3903 的空交集分支仍須獨立處理。

## 5. 反向控制、重播與信任範圍

[checker](../scripts/c5_sector_terminal_blocks.py) 與
[JSON](../artifacts/c5_sector_terminal_blocks/observations.json) 保存：

- 47,988 組長度 3、5、7 的私有 pair lists，完整 root transfer；長度 3、5
  另與直接四色指派比對。一般長度結論由 §1 證明，有限核對不代替證明。
- K4 的 64 組三色 lists；實際 attachments 的五個共同 pair 類及完整 root 表。
- 177 份明示 K5／K3,3 branch-set 證書、一份 subdivision、三份局部 disk
  rotations；重播只檢查來源邊、連通、互斥與 Euler 條件，不用 planarity oracle。
- 六組具名 bridge-root 位置控制及五份保留完整 bridge path 的雙列控制。

兩個必要反向控制使用**同一張 C5 block 與每點相同的實際 attachments**：
私有點依序為 `{1,2},{1,2},{1,4},{1,4}` 時，完整 root 集
Rα={1,2}、Rδ={1,2,3}。第二列不是共同二色 palette；不能只看 α。
將順序改成 `{1,2},{1,4},{1,2},{1,4}`，逐點 list-pair 的多重集不變，
但 Rδ 變成 U。這直接否定忽略循環位置的粗介面。

bridge 控制將兩個上述存活三角形用長 ℓ 路徑接起，端點 root 各有框邊
到 1，中間點各有實際 attachments {0,3}。所有內點完整 degree=4；
兩列的端點剩餘 list 都是 {2}、路徑中間 lists 都是 {2,3}。
ℓ=1,3,5 都拒絕兩列，ℓ=2,4 都接受並保存完整著色。
它們是**非 disk、沒有具名 w/b 或所需 transition 的控制**；只證明不能
直接刪除中間 bridges 或忽略傳遞的奇偶性。
一般 bridge 接合保留完整訊息：給定一側 root 集 R，另一側色 a
可接上恰當 R\{a} 非空；空集、singleton、多色集的效果不同。

生成 subdivision／rotations 使用 NetworkX 3.5；`--check` 不載入 NetworkX。
生成器僅建立明列局部模板，沒有擴大 sector 或 profile 搜尋。

```bash
uv run python scripts/c5_sector_terminal_blocks.py --check
uv run python scripts/c5_sector_rejection_lists.py --check
uv run python scripts/c5_sector_corner_gates.py --check
uv run python scripts/c5_sector_leaf_corners.py --check
lake build
git diff --check
```

新 checker、三份直接前置 checker、依賴 hashes、禁用 NetworkX 的重播、
Lean build 及變更文件連結／whitespace 均通過。transition-control、R 系列、
minimality 等其他 standalone checker 本輪未重跑。

紙面證明＋Python 有限控制；Gallai 化約依賴外部 degree-choosability
定理，disk apex／路徑拓撲為紙面證明，**未新增 Lean theorem**。
非空 ≥8 下界成為已排除分支的歷史必要條件；一般總體 ≥6 下界未提高。
603 profiles 沿用、零刪除、固定點未重算。空交集分支、一般 3903、R31、
共同出口及 `K∞=K≤5` 仍未證。未 commit／push。
