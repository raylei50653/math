# C5：換色後的精確 connectivity 更新與強制 C–D 接口

2026-09-15。接續 [class 計數定位](c5_kempe_class_counts.md) 的停止點。

**本輪結果（§1 的 surgery 引理已於 2026-09-15 Lean 化，見 §1 末；§2–3 仍為紙面）**：一次 Kempe swap 的四個混合色對，可用
「先刪頂點、收縮剩餘 components、再加入星形連接」精確重建 connectivity。
在 `P(G)⊆{0,2}`、`c|C5=(A,B,A,C,D)` 下，得到下述強制 C–D 接口邊引理。
它把跨染色的必要條件定位到同一張圖的實際內部邊，但尚未導出矛盾。

**computationally verified**：132 個既有 witnesses、1,810 個完整染色 S₄ representatives、
16,680 次實際 component swaps、66,720 次混合色對更新全部吻合。
另有一個既有 8 頂點 disk witness 同時通過兩個新生連通測試；它有禁止的 singleton
延伸，故只是局部條件不足的控制例。沒有新增圖 catalogue 搜尋。

## 1. 一次交換的六個色對

設 c 是任意有限圖 G 的 proper 四色染色，S 是 G[A∪C] 的一個完整 component，
c′ 由交換 S 內 A、C 得到。記 A_S=A∩S、C_S=C∩S，色集合皆以 **c** 定義。

| c′ 的色對 | c 中表示的 induced vertex set | connectivity 的更新 |
|---|---|---|
| AC | A∪C | induced graph 與全部 components 原封不動 |
| BD | B∪D | induced graph 與全部 components 原封不動 |
| AB | (A\S)∪B∪C_S | 刪 A_S，加入 C_S 的 B-neighbor stars |
| AD | (A\S)∪D∪C_S | 刪 A_S，加入 C_S 的 D-neighbor stars |
| BC | (C\S)∪B∪A_S | 刪 C_S，加入 A_S 的 B-neighbor stars |
| CD | (C\S)∪D∪A_S | 刪 C_S，加入 A_S 的 D-neighbor stars |

例如重建 AD：先取 H=G[(A\S)∪D]，將 H 的每個 component 收縮成一點；
對每個 z∈C_S 加入一個新點，連到包含其各個 D 鄰居的 H-components。
所得二分圖 Q 的 connectivity，提升回原頂點後，**恰等於** G[c′⁻¹({A,D})]。
孤立 component／孤立新點也必須保留。

**證明**：目標 induced vertex set 正是 V(H)∪C_S。C_S 內無邊；C_S 與 A\S
也無邊，否則該 AC 邊會把外部 A 頂點連入 S。因此 H 外的邊恰是上述 D-neighbor
stars。收縮連通塊保持剩餘頂點間的可達性，得精確對應。其他三對同理。
此引理不需要平面性，亦適用於平行邊。

**2026-09-15 Lean 化**（[Math/KempeSurgery.lean](../Math/KempeSurgery.lean)，普通證明，
無 `native_decide`）：`swapOn c a b S` 在任意頂點型別上交換 Kempe set `S`
（`KempeSet`：含於 `{a,b}` 頂點且對 `{a,b}` 鄰接封閉）。`swapOn_proper` 保持 proper；
`pairGraph_swap_same`／`pairGraph_swap_complementary` 給 AC、BD 兩列的「原封不動」；
`pairGraph_swap_mixed` 是上表四個混合列的精確等式
`pairGraph (swapOn c a b S) a d = retained G c a d S ⊔ stars G c b d S`；
`mixed_reachable_iff_quotient` 把混合色對的 connectivity 化為 retained components 的
quotient graph 加 stars 的可達性。`swapOn_univPair` 是「全域 transposition＝交換全部
`{a,b}` 頂點」，`swapOn_comm_of_disjoint`／`swapOn_swapOn` 是交換的可交換性與對合。
上述負控制與本節以下的 disk separation 仍是紙面層。

不能先收縮原本的 AD components 再刪 A_S：刪除可能把一個 component 切開。
最小負控制是 D–A–D 路徑，交換單點 A 的 AC component；兩端 D 從連通變成不連通。
也不能只保留「舊 boundary component partition」：它沒有記錄刪除後的內部分裂
以及新 stars 接在哪些剩餘 components。

## 2. 從反例假設得到兩次新生連通

保留**全圖** `P(G)⊆{0,2}`，固定完整染色 c 的邊界為 `(A,B,A,C,D)`。
由缺失 singleton 4、3，分別得到 BC 路徑 1↔3 與 BD 路徑 1↔4。
定義

\[
S=\operatorname{Comp}_{AC}^c(0),\qquad
T=\operatorname{Comp}_{AD}^c(2).
\]

BD 路徑 1↔4 與假想 AC 路徑 0↔2 端點交錯，且兩個色對不相交，
故 disk 平面性排除後者。因 2–3 是 AC 邊，`S∩C5={0}`。
同理，BC 路徑 1↔3 排除 AD 路徑 0↔2；因 0–4 是 AD 邊，`T∩C5={2}`。
這裡的 disjoint-path disk separation 是紙面拓撲論證，未 Lean 化。

| 操作 | 新邊界 | 必定保留 | 必須新生的混合色對連通 |
|---|---|---|---|
| 在 S 交換 AC，得到 c_S | (C,B,A,C,D) | BD 的 1↔4；AC 的 component partition | AD 的 2↔4 |
| 在 T 交換 AD，得到 c_T | (A,B,D,C,D) | BC 的 1↔3；AD 的 component partition | AC 的 0↔3 |

第一列：若 c_S 中 AD 的 2 與 4 不連通，只交換含 2 的 AD component，就得到
`(C,B,D,C,D)`，其 singleton 為 1，違反全圖假設。原 c 中 2、4 不連通，
故這條連通確實是新生的。第二列對稱：若 c_T 中 0、3 的 AC 不連通，交換含 0
的 component 得到同一 boundary word，仍違反缺失 singleton 1。

## 3. 強制接口邊引理

上述假設強迫

\[
E_G(C\cap S,\ D\cap T)\ne\varnothing.
\]

**證明**：取 c_S 中一條 AD 路徑 2↔4。它始於原 AD component T，終於 T 外。
沿路第一次離開 T 的邊 uv，u∈T、v∉T。若兩端皆是原 AD 頂點，這條邊會違反
T 是完整 component。因此外端必是新加入的 A 頂點，即 v∈C∩S；內端 u 的新色
為 D，S 的 swap 不改 D，所以 u∈D∩T。這就是所需的 C–D 邊。

由 c_T 的 AC 路徑也能對稱地得到一條此類邊，**兩個證明不保證得到同一條邊**。
兩端都是內點，因 S、T 的唯一 boundary 頂點原色都是 A。
S 與 T 可能共享 A 頂點；本證明不假定它們不相交，也不需要把兩條原 blocking paths
當成 vertex-disjoint paths。

**可執行的反面敘述**：若初始 BC／BD blockers 存在但接口邊集為空，
先交換 S，再交換新 AD component(2)，便在至多兩步得到 singleton-1。
此時第二個 component 包含於原 T，故不碰 boundary 4。

接口非空只是必要條件。§1 的 quotient Q 還要求 component(2) 與 component(4)
經一串 stars 相連；單有一條接口邊不足以保證完整新生路徑。

## 4. 真實 disk 控制例：不相交的區域仍會改變彼此的 component

既有 catalogue 的 mask **935**，3 個內點 5、6、7，有邊界 C5，加上

```
0–6, 1–6, 1–7, 2–7, 3–5, 3–7, 4–5, 4–6, 5–6, 5–7, 6–7.
```

可從內三角形 5–6–7 與外 C5 間的三角面
`016,127,237,345,406,167,375,456` 直接給出 disk triangulation。
連同內面 `567` 共 9 面；完整 edge list 亦保存在證書中。

取完整染色 `(A,B,A,C,D,B,C,D)`。初始 blocking paths 可取
`1–7–5–4`（BD）與 `1–6–5–3`（BC）。此時

\[
S=\{0,6\},\quad T=\{2,7\},\quad E(C\cap S,D\cap T)=\{67\}.
\]

- 交換 S 後，AD 新路徑為 `2–7–6–4`，新 component(2) 是 `{2,4,6,7}`。
- 交換 T 後，AC 新路徑為 `0–6–7–3`，新 component(0) 是 `{0,3,6,7}`。

所以兩個必需的新生連通可以同時出現於平面圖；`S∩T=∅` 也不保證在一次交換後
另一集合仍是 Kempe component。作為頂點上的色置換，兩個固定集合上的操作可交換，
但第二個操作已不是合法的完整 component swap，甚至可破壞 proper coloring。
在本例同時交換原 S、T 會使 6、7 同為 A，直接衝突。

**本例不是反例**：全圖 singleton support 是 `{3,4}`，不滿足 `P(G)⊆{0,2}`。
從上述 c 出發，最短逃逸恰為兩個實際 Kempe moves：

1. 交換 AB component `{0,1,2}`，得到 `(B,A,B,C,D,B,C,D)`。
2. 交換此時的 AC component `{1,6}`，得到 `(B,C,B,C,D,B,A,D)`，singleton 為 4。

這說明接口機制可阻擋兩個指定操作，卻沒有控制第三個色對 AB 的操作。
不能把通過這兩個局部測試當成全圖 singleton 缺失的證據。

## 5. 下一個缺口已縮小到什麼

**2026-09-15 續作**：[AB 交換立方體報告](c5_ab_swap_cube.md) 已否定僅憑下述局部
條件就能只靠 AB 序列逃逸的命題：固定 Errera disk 的全部 AB 狀態都通過，卻能由
CD 操作起始三步逃逸。最新入口為該報告 §6；以下保留本輪原停止點。

在每一個 `(A,B,A,C,D)` 完整染色中，反例都必須滿足 §2 的 blockers 與 §3 的接口，
且換色後兩個 quotient 的指定端點必須相連。這些現在都是**同圖明確頂點／邊集合**
的條件，不再用未指定的 existential boundary partitions 代替。

具體下一入口是含 boundary `{0,1,2}` 的 AB component U。交換 U 後邊界仍屬 x₀₂
（成為 `(B,A,B,C,D)`），必要時全域交換 A、B 便回到相同記號。
全圖假設要求此新染色再次滿足兩個 blockers 與接口；§4 的控制例就在此步失敗。
可進一步對 AB 的全部 components 任意選擇交換，要求每個所得染色都滿足這些條件。
§1 可精確計算這一輪更新，但尚無定理證明其中必有一次失敗，亦無單調下降量。

**仍未證**：無法由接口存在本身推出交錯路徑或平面矛盾；沒有證明 AB 操作必破壞
blocker，也沒有證明有限步長的普遍逃逸。Adjacent-singleton lemma 與 K∞=K≤5 仍未證。
對單一 class 不套 exterior／4CT；本輪未增加新的 mask 排除。

指定文獻 [Dvořák–Swart §1](https://arxiv.org/html/2504.07764v1) 將保持 terminal cyclic
order 的 planar realizability 與 Kempe constraints 相連；本輪接口引理是上述直接
推導，沒有把該文的一般 rooted-minor realization 結果當成 disk realization 定理。

## 6. 重播與信任範圍

```bash
python3 scripts/c5_kempe_connectivity.py --check
python3 scripts/c5_kempe_class_counts.py --check
python3 scripts/c5_adjacent_singleton_counts.py --check
python3 scripts/c5_kempe_screen.py --check
lake build
git diff --check
```

[新 checker](../scripts/c5_kempe_connectivity.py) 與
[精確證書](../artifacts/c5_cells/kempe_connectivity.json) 記錄 source hashes、逐 witness
驗證數與完整控制例。混合色對使用 quotient 算法重建，再與換色後直接 BFS 比對。
176 個固定 x₀₂ extensions 中，24 個具有兩條初始 blockers；左、右新生連通各有
2 個通過，同時通過恰 1 個，即 §4。這些數字只描述既有 witness 樣本。
最短兩步 escape 使用該固定圖的完整有標號 Kempe BFS，沒有預先假定可逃逸。

一般圖的 surgery 證明與 disk separation／接口證明為紙面層；有限重播不是一般定理的
Lean 認證。未修改 Lean 原始碼、既有 catalogue 或先前證書。
本報告與後續 AB 交換立方體成果一併整理提交；最新接手入口見 [HANDOFF](HANDOFF.md)。
上述四個 checkers、文件連結、`git diff --check` 與 `lake build` 全部通過；
Lean build 僅重播既有 lint 警告。
