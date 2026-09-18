# 唯一 degree-5 的三-spoke 型：disk 區域化約

發布整理（2026-09-18）：本報告隨 R11–R15 五輪成果一併提交。下文的
「未提交／HEAD／下一題」保留各輪當時狀態；最新停止點見
[HANDOFF](HANDOFF.md)，發布前核對見 [STATUS §16](STATUS.md)。

後續（2026-09-18）：[任意樹分量報告](c5_degree5_tree_components.md) 已排除
本分拆中任意大小的樹 C，並排除連通外框下的 K4 block；下一題為含 triangle 的 C。

2026-09-18。從乾淨 HEAD `be97121` 接續
[完整接點介面](c5_degree5_interfaces.md) 的分拆 (2)。
**任意大小的這一型，在 minimal q 與接受全部 T4 的前提下，只剩兩個互為
鏡像的長區域。** 可將問題改寫成一個帶指定二接點 boundary 頂點的 C5
四色延拓問題。尚未排除剩下的型，也未證一般 degree-5 單缺失。

成果是紙面 disk 化約、有限 boundary 代數及一個具名反向控制；未新增 Lean
theorem，未增加內點數或 block catalog。新控制尤其表明：即使 disk、degree
序列、相鄰雙缺失及全部 T4 都成立，也不能省略逐邊 minimality。

## 1. 三條 spokes 將連通分量限制在同一區域

沿用 q=(0,1,0,1,2)、U={0,1,2,3}、D=3，並稱三個 q 色為 A、B、C。
G 為 chordless C5 disk，唯一 degree-5 內點 z 有三條 boundary spokes；
H−z 是一個連通分量 C，經兩個不同接點連到 z，其餘內點完整 degree=4。
假設 G 是 minimal q-obstruction 且接受全部 T4。

minimality 使 z 的三個 boundary 鄰居顏色互異。因此其鄰集 S 恰從
{b0,b2} 選一個、{b1,b3} 選一個，另加 b4；A_z(q)={D}，而
[介面 minimality 等價式](c5_degree5_interfaces.md#4-minimality-的充要條件與接點限制)
給出 **F_C(q)={D}**，不只是 D∈F_C(q)。

在固定 disk embedding 中，三條 z-spokes 的內部互不相交，將開 disk
分成三區，各區的閉包邊界是 z、兩條相鄰 spokes 及其間一段 C5 arc。
C 不含 z 或 boundary 頂點，且連通，所以全部位於同一開區域。
每條 C 到 boundary 的邊也只能終於該區域的閉 boundary arc。
兩條 zC 邊在 z 處屬同一區域；不能把同一 C 的兩接點放到不同區域。
這是固定嵌入的平面分離論證，沒有使用枚舉或四色定理。

## 2. 十二種位置只剩兩個鏡像

四個可能的 S，各有三個區域，共十二種。依序用兩個必要條件：

**缺色交換。** 若該 arc 未使用某個 q 色 c，則 C 的全部 boundary 約束
同時不含 c 與 D。交換 C coloring 中的 c、D 保持約束，故完整禁色集
F_C(q) 在此交換下不變。D∈F_C(q) 因而推出 c∈F_C(q)，違反 F_C(q)={D}。
這一步排除八種位置，不需 T4，也沒有拆開兩接點的共同關係。

**未碰頂點改色。** 若有 boundary 頂點 v 不在 arc∪S，且其 q 色重複，
只將 v 改為 D。新列仍 proper、使用四色，但 C 的全部 boundary lists
及 z 的三個鄰居顏色均不變，因此仍拒絕此 T4 row。這與接受全部 T4 矛盾。
餘下兩個短區域恰分別可取 v=b0、b3。

| 通過缺色交換的位置 | arc（依 C5 正向） | 後續判定 |
| --- | --- | --- |
| S={b0,b1,b4} | b1,b2,b3,b4 | 保留 |
| S={b1,b2,b4} | b2,b3,b4 | 改 b0 為 D，拒絕 T4 |
| S={b1,b2,b4} | b4,b0,b1 | 改 b3 為 D，拒絕 T4 |
| S={b2,b3,b4} | b4,b0,b1,b2 | 保留 |

反射 i↦3−i（mod 5），再交換 A、B，將第一個保留型變成第二個。
故只需研究第一型；上述覆蓋對 C 的大小、環長及 block 數沒有上限。

## 3. 剩餘問題的精確五邊形重寫

固定第一型。令 K 是由 C 及有序 boundary

```
(z,b1,b2,b3,b4)
```

組成的 disk 子圖。K 的 boundary 是一個 C5，C 的每點仍完整 degree=4，
z 有恰兩條朝 C 的邊；在 K 中 z 是 boundary 頂點，不是內點。
原圖恰是加入 b0 及 b0b1、b0b4、b0z 三邊。
此操作保留具體圖及共同色框，不是宣稱一個較小內點代表。

令 S_K 為 K 的完整有序 boundary relation。對任意 proper 原 boundary b，

```
b∈Σ(G)  iff  ∃a∈U\{b0,b1,b4}, (a,b1,b2,b3,b4)∈S_K.       (1)
```

在 q 下唯一可選 a=D，故 K 拒絕的 boundary 是
**(D,B,A,B,C)**，使用四色，重複的位置是 b1、b3。
原 minimality 對每條碰 C 的邊給出此四色列的刪邊延拓。
但仍須另保留 F_C(q)={D}：它還要求在移除 z-spokes 約束後，C 可配合
z=A、B、C 各自著色。特別 z=B 或 C 與 K 的一條 boundary 邊衝突，
這兩個測試不在 proper-C5 relation S_K 的域內，不能直接查詢；尚未證明
它們可由 S_K 的其他列推出。此處沒有宣稱找到同 S_K、不同 minimality 的碰撞。

這也說明為何不能直接套用已完成的全 degree-4 theorem：K 的指定拒絕列
使用四色，且尚未知道它接受全部 T4；原圖中 z 則仍 degree=5。

對所有 2^10 個抽象 S4-invariant proper-C5 relations 檢查 (1)，恰有
24 個輸入同時使 G 接受全部 T4、拒絕 q，形成 12 個不同輸出 relations。
其中容許相鄰三色雙缺失。這只核對接合公式，**不聲稱這些抽象輸入都是
disk 可實現，更不聲稱符合指定 degrees 或 minimality**。
checker 以全部 240 個有標號 boundary rows 核對共同色框，共 245,760 次。

## 4. 具體 disk 反向控制：minimality 不能省

沿用既有 cell catalogue 的一張二內點 sector witness，按 §3 加入外側頂點，
得到以下圖。boundary 為原 C5，內點是 u、v、z：

```
N_B(z)={b0,b1,b4},    z~u,v;
N_B(u)={b2,b3},      N_B(v)={b1,b2},    u~v.
```

z 完整 degree=5，u、v 各 degree=4，H−z 正是一個二接點 edge 分量。
該圖確是 disk、接受全部 T4，恰拒絕 q 及 (0,1,2,1,2)；兩個缺失的
singleton boundary 位置 b4、b0 相鄰。

然而 q 下 u、v 的 lists 都是 {C,D}，又彼此相鄰，所以
**F_C(q)={C,D}**。z 的 b4-spoke 排除的 C 早已被分量排除；刪去它仍拒絕
q。因此這張圖不是 minimal q-obstruction，不能當成目標反例。
其餘非 boundary 邊的刪邊均可延拓 q，checker 保存相應 coloring。

控制來源 graph 與數字索引保存在證書中；新 checker 沒有重建 catalogue。
為這一張明列的圖產生 boundary-apex rotation，另核對來源邊、面追蹤與
Euler 等式。此一具名 planarity 控制仍含 NetworkX／既有 apex-disk 等價的
信任，不是一般 topology 或圖分類證明。

## 5. 重播與停止點

[checker](../scripts/c5_degree5_sectors.py)、
[certificate](../artifacts/c5_degree5_sectors/observations.json)。
保存直接依賴程式及來源 catalogue SHA256；`--check` 重算並逐 byte 比對。

```bash
uv run --with networkx==3.5 python scripts/c5_degree5_sectors.py --check
uv run --with networkx==3.5 python scripts/c5_degree5_interfaces.py --check
lake build
git diff --check
```

本輪實際核對見 [STATUS §11](STATUS.md#11-三-spoke-區域化約基準-be97121)。
任意大小的區域限制與缺色交換由紙面論證承擔；有限控制只核對 boundary
位置、接合代數和具名非 minimal witness，沒有新增 Lean theorem。

**下一個窄問題：** 在 K=(z,b1,b2,b3,b4) 的單一 pentagon 區域內，保留 z
的兩接點、C 的實際 spokes 與 F_C(q)={D}，研究四色列 (D,B,A,B,C) 的
degree-list block palettes，判定 (1) 是否仍可能拒絕相鄰三色 p 而接受全部
T4。首要處理 z=B、C 的刪-spoke 延拓條件；只存 proper S_K 會漏掉它們。
Gallai-tree 必要條件沿用前報告及其
[外部 degree-choosability 定理](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，
本輪區域化約本身不需該定理。不可將上述非 minimal 控制誤當新反例。

分拆 (2) 的最終排除、其餘十二個必要接點分拆、一般 degree≥5、單側／共同
出口、候選 A 與 `K∞=K≤5` 均仍開放。研究產物未 commit／push。
