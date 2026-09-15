# C5：AB 操作可一直維持 blockers 與接口，甚至兩次新生連通

2026-09-15。接續 [connectivity surgery 與接口引理](c5_kempe_connectivity.md)。

**結論**：只假設上一輪的局部 blockers、接口及兩次新生連通，不能證明「某個 AB
交換序列必將它們打破」。有一張明確的 **16 頂點 disk 圖**，這些條件在其一個染色的
**所有 AB 交換序列**下始終成立。證明結合一般的 AB 交換立方體引理與完整固定圖證書。
這個例子沒有滿足全圖 `P(G)⊆{0,2}`；它排除的是上述局部逃逸命題，不是原主引理。

另外，這個例子的兩條 blockers 都不存在一條由所有 AB 交換共同保留的固定路徑。
`∀交換 ∃blocking path` 不能換成 `∃path ∀交換`。
改用一個內部 CD component，則可打破接口，再兩步得到 singleton-1。

**信任範圍**：一般交換立方體／signed connectivity 是紙面證明；固定圖與路徑、
全部交換、最短 escape 是精確 Python 證書。disk 由定向三角複形證書及紙面 surface
判準確認。全部未 Lean 化；Adjacent-singleton lemma 與 K∞=K≤5 仍未證。

## 1. 任意長 AB 操作，其實只是一個固定立方體

固定 `c|C5=(A,B,A,C,D)`。令 `U₀,…,Uᵣ₋₁` 為 **c 的完整 AB components**，其中
U₀ 包含 boundary `{0,1,2}`；邊 01、12 保證它們在同一個 component。

交換任一 Uⱼ，不改變 AB induced vertex set 或其全部邊，因此不改變任一 Uᵢ。
每個交換是 involution，不同 Uᵢ 上的交換互相可交換。因此任意有限 AB 操作序列的
結果，恰由每個 Uⱼ 被交換次數的奇偶決定；共有 `2ʳ` 個有標號結果。
這裡沒有假設不同色對的交換也有此性質。

若交換過 U₀，邊界變成 `(B,A,B,C,D)`。以**同一個全域 A/B 置換**恢復記號，
相當於改為交換所有原本未選取的 Uⱼ。因此可固定 U₀ 不動，只用 `r−1` 個自由 bits
表示全部 `2ʳ⁻¹` 個對齊結果。沒有獨立重命名不同圖或不同 ports。

所以「AB 永遠維持某條件」的精確判準是：這個固定有限立方體的每個頂點都通過條件。
不必假設步數上界；也不能期待反覆 AB 操作產生新的 AB component。
若只交換 U₀，對齊後只會在全 0 與全 1 兩組 bits 間切換；`r≥3` 時不涵蓋全部立方體。

## 2. blockers 是同一組 bits 控制的 signed connectivity

以 0、1 表示原 A、B。對 v∈A∪B，令 σ(v) 為原顏色，h(v) 為其 AB component 編號。
固定 t₀=0，其餘 tⱼ 表示是否交換 Uⱼ。則新 B 色頂點集恰為

\[
B(t)=\{v\in A\cup B:\ \sigma(v)\mathbin{\mathrm{xor}}t_{h(v)}=1\}.
\]

新 BC／BD blockers，分別就是 **同一張 G** 上

\[
1\leftrightarrow3\text{ in }G[B(t)\cup C],\qquad
1\leftrightarrow4\text{ in }G[B(t)\cup D].
\]

這提供一般圖的精確更新公式，不需平面性。原 B 頂點的啟用條件是 `¬tⱼ`，原 A
頂點是 `tⱼ`；同一 component 內所有頂點受**同一個 bit**約束。
每條候選 alternating path 對應其頂點啟用條件的合取，連通性則是這些 path 條件的析取。
同一路徑若同時要求 `tⱼ` 與 `¬tⱼ`，便不可能啟用。

因此這不是可獨立打開每個頂點的模型，也沒有「多交換幾個 component 只會增加路徑」
的單調性。checker 由原圖與 bits 直接構造上述 induced graphs，再與真正換色後的
component BFS 比對。接口及兩次新生連通則在每個所得完整染色中重新計算。

## 3. 固定控制圖與全部 AB 狀態

使用 [Sage 10.6 的 ErreraGraph 邊資料](https://raw.githubusercontent.com/sagemath/sage/10.6/src/sage/graphs/generators/smallgraphs.py)，
刪去舊頂點 0，依下列 `新標號 → 舊標號` 重排：

```
0..15 → 1,14,16,7,15,2,3,4,5,6,8,9,10,11,12,13
```

舊 0 的鄰居依 `1,14,16,7,15` 成 C5，即新 boundary 0–1–2–3–4–0。
新圖有 16 頂點、40 邊、25 個內部三角面。完整邊表與定向面表見
[證書](../artifacts/c5_cells/ab_swap_cube.json)。checker 檢查：內邊被兩個面反向使用、
唯一 boundary 恰為指定 C5、每個內點的 link 為 cycle／boundary 點的 link 為 path、
面鄰接連通，以及 `16−40+25=1`。故此有限複形是 disk；不靠圖名推定平面性。

取完整染色

```
v     0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
c₀    A B A C D C D A D B  D  B  B  C  C  A
```

完整 AB components 恰為

\[
U_0=\{0,1,2,9,11,15\},\qquad U_1=\{7,12\}.
\]

所以原始 AB orbit 有 4 個染色，按 §1 對齊後只有兩個：c₀ 與交換 U₁ 得到的 c₁。
c₁ 只把頂點 7 改為 B、12 改為 A。**下表已涵蓋任意長 AB 序列。**

| 觀察 | c₀：t₁=0 | c₁：t₁=1 |
|---|---|---|
| BC blocker 1↔3 | 1–5–12–14–9–3 | 1–5–11–13–7–14–9–3 |
| BD blocker 1↔4 | 1–10–12–6–11–4 | 1–10–9–8–7–6–11–4 |
| S=Comp_AC(0) | {0,5} | {0,5,12,14} |
| T=Comp_AD(2) | {2,10} | {2,6,10,12} |
| C–D 接口邊 | 5–10 | 5–6、5–10、14–10 |
| 交換 S 後的新 AD 2↔4 | 2–10–5–6–7–8–15–4 | 2–10–14–8–15–4 |
| 交換 T 後的新 AC 0↔3 | 0–5–10–14–7–13–15–3 | 0–5–6–13–15–3 |

這不只是有一個可永遠重複的安全循環：**所有** AB 選擇都留在這兩個通過的狀態。
接口邊 5–10 在兩者中都有效；接口邊數卻在 1、3 之間往返，不能當成 AB 必下降量。

## 4. 每次都有路徑，不等於存在共同不變路徑

上表 c₀ 的兩條 blocker paths 都使用內部頂點 12，對應 literal `¬t₁`；
c₁ 的兩條 paths 都改用 7，對應 literal `t₁`。兩者合起來覆蓋 `¬t₁∨t₁`。
更強地，可以直接證明**不存在其他共同路徑**：

- 在兩個狀態都屬於 BC 的頂點所誘導的圖中，1 的 component 是 `{1,5,11,13}`，
  不含 3。
- 在兩個狀態都屬於 BD 的頂點所誘導的圖中，1 的 component 是 `{1,8,9,10}`，
  不含 4。

任何共同保留的 BC／BD path 都必須位於這些交集圖，因此不可能存在。
後續證明若要追蹤固定 paths，必須另證固定性；不能從全立方體的連通性自行補上。

## 5. CD 操作能打破本例，但尚無一般必破定理

原 c₀ 的 CD components 是

\[
V_0=\{3,4\},\qquad V_1=\{5,6,8,10,13,14\}.
\]

AB 與 CD 是 complementary pairs；其 components 各自且彼此保持，所以這兩組交換
合起來仍是同一個固定立方體。原始大小 16，全域 A/B、C/D 對齊後大小 4。

| 內部 AB bit t₁ | 內部 CD bit s₁ | 兩條 blockers | 接口邊數 | 兩次新生連通 |
|---|---|---|---|---|
| 0 | 0 | 均存在 | 1 | 均存在 |
| 1 | 0 | 均存在 | 3 | 均存在 |
| 0 | 1 | 均存在 | 0 | 均不存在 |
| 1 | 1 | 均存在 | 0 | 均不存在 |

交換 V₁ 後，兩個狀態都有 `S={0}`、`T={2}`。於是有下列三步實際 Kempe escape：

1. 在 c₀ 交換 CD component V₁，boundary 不變。
2. 交換 AC component `{0}`，boundary 成為 `(C,B,A,C,D)`。
3. 交換 AD component `{2}`，boundary 成為 `(C,B,D,C,D)`，singleton 為 1。

每一步皆重新驗證完整 component 與 proper coloring。完整有標號 Kempe BFS
另驗證本起點的最短 escape 長度恰為 **3**；證書也保存 BFS 找到的另一條三步路線。

**本例不是原主引理的反例**：枚舉完整染色得到每個 x 座標為 12、每個 y 座標為 8，
全圖 `P(G)={0,1,2,3,4}`。100 個完整染色 S₄ orbits 都屬於同一 Kempe class。
因此沒有證明 class confinement，更沒有構造 independent-singleton relation。

## 6. 既有樣本對照、文獻範圍與下一步

132 個既有 witnesses 的 176 個固定 x₀₂ extensions，分成 166 個對齊 AB cubes：

| 在整個 AB cube 始終成立的條件 | cubes 數 |
|---|---|
| 兩條初始 blockers | 20 |
| blockers 加非空接口 | 4 |
| blockers 加兩次新生連通 | 0 |

中列四例的 masks 為 636、956、1012、1020，皆只有一個對齊 AB 狀態。
因此僅 blockers／接口的全 AB 不變性，在舊小圖中已可發生；較強的兩次新生連通
則由 §3 的固定 Errera disk 控制例補足。沒有推論其頂點數最小，也沒有枚舉新的圖族。

[Gethner 等人的原始研究，§2–3](https://msp.org/involve/2009/2-3/involve-v2-n3-p01-s.pdf)
把這類五鄰點的 chain tangle 與後續 Kempe–Kittell 操作分開分析；其 Theorem 4
指出兩次指定交換的順序可影響成敗。該文 p.259 當時未給一般成功保證。
本輪「固定 AB orbit 的全部狀態均通過」及明確 CD escape 是上述圖的直接有限驗證，
不是引用該文得到的一般定理；不據此宣稱相關問題目前的完整文獻狀態。

**下一個可檢驗命題**：擴大到固定 complementary split `AB|CD` 的全部獨立交換，
是否仍能有一張 disk 圖與起點，讓所有對齊狀態都通過 blockers 與兩次新生連通？
本例對這個更強問題給的是「會失敗」，尚未回答一般情形。
可用同一個共用 bits 模型檢查；不能讓各狀態分別選不相干的圖或 partition。

另一路是利用全圖 `P(G)⊆{0,2}` 的額外結構，超出本輪局部條件。
本輪只排除「局部條件＋任意 AB 序列必逃逸」這個候選引理，**不排除 AB 操作參與
更完整證明的可能性**。主 Adjacent-singleton lemma 與 K∞=K≤5 仍未證。

## 7. 重播

```bash
python3 scripts/c5_ab_swap_cube.py --check
python3 scripts/c5_kempe_connectivity.py --check
python3 scripts/c5_kempe_class_counts.py --check
python3 scripts/c5_adjacent_singleton_counts.py --check
python3 scripts/c5_kempe_screen.py --check
lake build
git diff --check
```

[checker](../scripts/c5_ab_swap_cube.py)／[證書](../artifacts/c5_cells/ab_swap_cube.json)
保存 source hashes、固定圖的來源與重標號、面表、所有對齊狀態、blocking paths、
新生 paths、共同路徑負控制、兩種三步 escape、完整 counts/classes 與既有樣本對照。
另用三個 AB components 的固定小圖驗證「只交換 boundary component」漏掉狀態，
並以缺一面負控制確認 disk 證書驗證會拒絕。
重播不需網路、Sage 或 NetworkX；未修改 production catalogue、Lean 原始碼或前輪證書。
上述五個 checkers、文件連結、`git diff --check` 與 `lake build` 全通過；
Lean build 僅重播既有 lint 警告。本報告與前輪 connectivity surgery 成果一併整理提交；
研究停在 §6 的下一個命題，最新接手順序見 [HANDOFF](HANDOFF.md)。
