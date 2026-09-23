# C5 boundary relations：有界代表與特殊反例路線

文件狀態補註（2026-09-23）：本頁維護主命題、全域較小代表與局部壓縮的區別；
各路線的後續成果與保留缺口由 STATUS 維護，不以本文的早期路線描述作進度摘要。
當前優先順序見 [研究交接](HANDOFF.md)，完整索引與可能變化見 [STATUS.md](STATUS.md)。

2026-09-15。本文是研究目標與證明路線總覽；主命題仍待證。
現有結果與信任範圍見 [研究交接](HANDOFF.md)。

本文區分三個層次：

1. **主命題**：所有可實現的 C5 boundary relations，都有至多五個內部頂點的代表。
2. **主證明路線**：假設存在新 relation，將反例限制到特殊結構，再排除該結構。
3. **加強猜想**：存在明確的局部化簡規則，能將任意大圖逐步壓縮成小代表。

其中，主命題與「每張大圖存在較小等價圖」等價；要求由指定局部操作實現壓縮，才是額外的結構性要求。

## 1. 定義與研究目標

令 \(\mathcal C\) 為本項目研究的 C5 planar cells 類別。所有圖均保留指定且帶標號的 C5 邊界，並令

$$
k(G)=|V_{\mathrm{int}}(G)|.
$$

\(\Sigma(G)\) 表示可延伸至 \(G\) 的合法邊界四色染色，按全域顏色置換 \(S_4\) 取軌道後所得的集合。本項目使用 10-bit key 表示此集合；邊界位置不因 \(D_5\) 對稱而合併。

因此，

$$
\Sigma(G)=\Sigma(H)
$$

表示對每個固定邊界染色 \(b\)，

$$
b\text{ 可延伸至 }G
\iff
b\text{ 可延伸至 }H.
$$

這比「兩張圖都可四色染色」更強：它保留每一種邊界條件下的延伸可行性，但不要求延伸數量相同。

定義

$$
K_{\le r}=\{\Sigma(G):G\in\mathcal C,\ k(G)\le r\},
\qquad
K_\infty=\bigcup_{r\ge0}K_{\le r}.
$$

本文採用 \(K_{\le5}\)，避免與「恰有五個內點」的 relation 集合混淆。
本倉庫既有報告的 `K5` 在此目標中對應本文的 \(K_{\le5}\)。
cell 與 10-bit key 的具體規格見 [枚舉器規格 §0](c5_cell_enumerator.md)。
這裡的 cell 要求指定 C5 是 disk 邊界，不能只要求整張圖 planar。

研究目標為：

$$
\boxed{K_\infty=K_{\le5}.}
$$

目前應將此式視為待證主命題，不能僅由有限階枚舉沒有發現新 relation 推出。

## 2. 有界代表與全域壓縮的等價性

對每個可實現 relation \(S\)，定義其最小代表大小：

$$
\mu(S)=\min\{k(G):G\in\mathcal C,\ \Sigma(G)=S\}.
$$

下列三個敘述等價：

**有界代表：**

$$
K_\infty=K_{\le5}.
$$

**最小代表上界：**

$$
\forall S\in K_\infty,\qquad \mu(S)\le5.
$$

**全域縮小的存在性：**

$$
\forall G\in\mathcal C,\quad
k(G)>5
\Longrightarrow
\exists H\in\mathcal C,\quad
k(H)<k(G),\quad \Sigma(H)=\Sigma(G).
$$

若每張大圖都有較小等價圖，反覆套用即可由內點數的嚴格下降得到 \(k\le5\) 的代表。反之，若每種 relation 都有至多五個內點的代表，直接選取該代表即可。

這裡不要求 \(H\) 是 \(G\) 的子圖、minor，或能由局部操作得到。因此，「全域小代表存在」與「最小反例排除」並非強弱不同的結論，而是同一目標的不同證明方式。

另外，10-bit relation 空間有限，已保證某個有限代表上界存在：對每個可實現 relation 選取最小代表，再取其大小的最大值即可。

真正需要證明的是**具體上界為五**；有限性本身不提供這個數值。

## 3. 加強方向：局部 relation-preserving 壓縮

更強的結構性目標，是指定一組局部規則 \(\mathcal R\)，使每個 \(k(G)>5\) 的圖都存在有限操作序列

$$
G=G_0\to G_1\to\cdots\to G_t=H,
$$

滿足

$$
G_i\in\mathcal C,\qquad
\Sigma(G_i)=\Sigma(G),\qquad
k(H)<k(G).
$$

中間步驟可以加入邊或重組 patch，不必每一步都減少內點；但每輪必須得到嚴格較小的圖，才能反覆壓縮。

「局部規則」需要明確限制適用構型、介面及替換方式。若允許直接替換整張內部，這個敘述就退回小代表存在性，失去額外的結構內容。

### 3.1 基本規則：低度內點刪除

對內部頂點 \(v\)，四色染色有

$$
\deg_G(v)\le3
\Longrightarrow
\Sigma(G)=\Sigma(G-v).
$$

理由是任何 \(G-v\) 的合法四色染色，在 \(v\) 的鄰居上至多使用三種顏色，因此總能補回 \(v\)。

此處度數包含所有內部及邊界鄰居。將它用作 \(\mathcal C\) 內的 reduction 時，還須確認刪除後仍符合 cell 類別要求。

反覆使用此規則後，剩餘待處理結構的所有內部頂點都有度數至少四。

### 3.2 一般規則：以相同介面關係替換 patch

若區域 \(A\) 只透過介面 \(S\) 與外部互動，定義

$$
R_A=\{\text{可延伸至 }A\text{ 的 }S\text{ 上染色}\}.
$$

如果另一個區域 \(B\) 滿足

$$
R_A=R_B,
$$

則在相同外部環境下，用 \(B\) 替換 \(A\) 保留完整的邊界延伸關係。要作為合法 cell 化簡，還須維持平面嵌入、介面接合與指定 C5 邊界。

例如，兩點介面的 relation 若恰好是「兩端不同色」，可考慮用一條邊表示；若恰好是「兩端同色」，可考慮識別端點。

一般情況則可能需要小 gadget。只比對所有兩點投影並不足夠，因為多點聯合限制可能無法由邊約束完整表達。

### 3.3 尚需證明的完備性

證明個別規則保留 \(\Sigma\)，並不等於證明所有大圖都能縮小。還需要：

> 每個內點數大於五的目標圖，都能套用某個規則或有限規則序列，得到較小等價圖。

若規則系統卡住，只能先說該系統尚未完成壓縮；不能據此否定小代表存在性。

## 4. 主路線：最小反例與特殊分支

假設主命題不成立，選取內點數最少的圖 \(G\)，使

$$
\Sigma(G)\notin K_{\le5}.
$$

則 \(k(G)>5\)。任何保持 \(\Sigma\)、留在 \(\mathcal C\) 內且減少內點的操作，都會與最小性矛盾。

例如，在低度刪除適用的前提下，可立即推出

$$
\forall v\in V_{\mathrm{int}}(G),\qquad \deg_G(v)\ge4.
$$

接下來的目標，是利用最小性、平面結構及 relation 限制，逐步縮小反例的可能形態。

這條證法不需要為所有圖提供壓縮演算法，也不需要每個中間轉換都保留完整 \(\Sigma\)。但若某一步改變 relation，就必須說清楚：**它保留了哪個足以導向最終矛盾的性質。**

## 5. 特殊 support／fibre 路線的接合義務

以下沿用項目中的 \(T_4,P,x_e,m\) 記號：
\(T_4\) 是五種四色 boundary orbits；\(y_i\) 是 singleton 位於 i 的固定
boundary assignment 延伸數，\(P(G)=\{i:y_i(G)>0\}\)；\(e\) 是 C5
非相鄰頂點對（chord 的端點集合），\(x_e\) 是 repeated-pair e 的固定 assignment 延伸數。
\(m=L-\sum_i y_i\)，其中 \(L=x_{uv}+y_u+y_v\) 是共同 chord total。
完整定義與恆等式見 [計數報告 §1–2](c5_adjacent_singleton_counts.md)。
這裡整理的是論證接合義務，不將各箭頭自動視為已證結果。

目前提出的路線為：

$$
\Sigma(G)\notin K_{\le5}
\Longrightarrow
T_4\subseteq\Sigma(G),\qquad P(G)\text{ independent},
$$

再利用 C5 上的 support 結構選取 \(e\)，使

$$
P(G)\subseteq e,\qquad x_e(G)>0.
$$

接著構造 near-triangulation \(H\)，希望保留

$$
P(H)\subseteq P(G)\subseteq e,
\qquad
x_e(H)>0.
$$

若相應 count identity 在此類 \(H\) 上適用，則進一步得到

$$
m(H)=x_e(H)>0,
$$

並推出其他所需 fibre 的正性，恢復

$$
T_4\subseteq\Sigma(H).
$$

這條鏈需要逐項確認：

* finite／Kempe／exterior screen 是否涵蓋所有可能的新 relation。
* support 條件是否確實允許選到同一個滿足 \(x_e(G)>0\) 的 \(e\)。
* completion 是否保持目標圖類別、指定邊界及該 fibre。
* count identity 的全部前提是否成立。
* 得到的特殊條件如何導向矛盾。

最後一項有兩種合法完成方式。

**方式一：保留反例資格。**

證明 completion 後仍有

$$
\Sigma(H)\notin K_{\le5},
$$

再排除這類特殊反例。恢復 \(T_4\) 本身是否足夠，必須由 relation 分類結果支持。

**方式二：直接排除特殊結構。**

不要求 \(H\) 仍是新 relation，而直接證明

$$
H\text{ 為 near-triangulation},\quad
P(H)\subseteq e,\quad x_e(H)>0
$$

這組條件不可能同時成立。

若能證明這個更強的 obstruction lemma，便不需要另外保留反例資格。但應先檢查已知小圖是否滿足上述條件；若有，就表示特殊條件仍缺少必要假設。

兩種方式都可行，不能混用。尤其必須區分：

$$
\text{新 relation}\Longrightarrow\text{特殊條件}
$$

與

$$
\text{特殊條件}\Longrightarrow\text{新 relation}.
$$

前者並不自動給出後者。

### 5.1 與現有成果的對照

- [Edge／pairing state 實驗](c5_edge_states.md) 精確核對 primal Kempe swap 的 dual
  cut 規則，列出五個 fibres 的一步 blockers；三組 pairings 能恢復 boundary connectivity，
  但固定 Errera disk 中同 T、同 cycle counts 的兩個染色有 3／2 步 escape 差異，
  故尚不能作精確的後繼狀態。H1–H5 與 polygon interface 完備性仍未證。
- [高度數 disk 家族續作](c5_corner_disks.md) 找到三個完整 `AB|CD` 立方體 survivor
  （所有對齊狀態維持 blockers＋接口＋兩次新生連通，escape 全從 split 之外開始），
  否定「固定立方體必失敗」的局部命題；corner-compliant CD 翻轉有六種機制，無單一 CD 引理。
- [完整 AB|CD 立方體續作](c5_complementary_cube.md) 在既有 corpus 與 Errera 刪點家族
  中都找不到全程維持 blockers＋接口＋兩次新生連通的立方體；所有 CD bit 失敗都是
  0 或 2 鄰域的 corner collapse，給出一個必要 corner 條件，但屬低度數產物，非一般定理。
- [AB 全交換續作](c5_ab_swap_cube.md) 以交換立方體引理與固定 16 頂點 Errera disk
  證明局部 blockers／接口／兩次新生連通可在任意 AB 序列下保持；該圖仍有三步 CD
  起始 escape。排除局部 AB 必逃逸引理，未排除全圖 independent-singleton 分支。
- [換色 connectivity 續作](c5_kempe_connectivity.md) 給混合色對的精確刪除／收縮／star
  更新公式，並從特殊反例推出兩個指定 components 間的實際 C–D 接口邊。
  既有 disk 控制例顯示兩次新生連通可同時存在；後續 AB 相容性結果見上一項。
  一般論證為紙面證明，有限驗證重播既有 witnesses，未新增 mask 排除。
- [Kempe-class 計數續作](c5_kempe_class_counts.md) 將 chord-total 恆等式限制到
  同一完整染色 class，並定位特殊分支的正參數；這是紙面證明加有限證書，未 Lean 化。
  不對單一 class 套 exterior 條件；最終 connectivity obstruction 仍缺。

- [Kempe／exterior screen](c5_kempe_screen.md) 記錄新 relation 的候選分類；
  有限 mask 檢查與一般 disk／4CT 必要性論證的信任範圍分開保留。
- [count-cone bridge §2–3](c5_count_cone_bridge.md) 已給保留一個 fibre 的
  completion 與恢復全部 \(T_4\) 的紙面論證；completion 允許平行邊且可能增加內點。
  它在擴大的 near-triangulation 類別中保留 adjacent-singleton 反例性質，
  不要求輸出仍是原枚舉的簡單 cell，也不是 §2 的縮小操作。
- [C5Counts.lean](../Math/C5Counts.lean) 的 `independent_subset_chord` 與
  `all_chords_positive` 已證選 chord 及恢復正性的代數部分；
  從 disk graph 導出計數恆等式與補完的拓撲前提仍未 Lean 化。
- [B₅ face 報告 §3–5](c5_b5_face.md) 已整理特殊分支的 cone 分解，並釐清
  單一非零五端點 context 的普通 pairing 無法排除帶正 fan 的候選。
  最終 obstruction 仍缺；不能把上述接合進展視為主命題的證明。

## 6. 項目與論文定位

| 層次   | 內容                               | 證明要求                     |
| ---- | -------------------------------- | ------------------------ |
| 主命題  | \(K_\infty=K_{\le5}\)            | 排除所有需要超過五個內點的新 relation  |
| 等價敘述 | 每張大圖存在較小的 \(\Sigma\)-等價代表        | 與主命題等價                   |
| 主證法  | 最小反例經 screen 與 completion 進入特殊分支 | 接合每一步前提，完成最終 obstruction |
| 加強猜想 | 指定局部規則能壓縮任意大圖                    | 規則正確性及全域完備性              |
| 有限枚舉 | 搜尋新 relation、最小代表及候選構型           | 提供有限範圍證據，不能單獨推出全域上界      |

目前主線應優先完成特殊分支的論證接合與 obstruction lemma。局部壓縮可作為額外結構方向探索，但不應成為主結果必須等待的前提。

若最終僅完成主命題，可宣稱：

> 每個可實現的 C5 planar boundary relation，都有至多五個內部頂點的代表。

只有在指定規則的完備性也完成後，才可進一步宣稱：

> 任意 C5 planar cell 都能透過保留 boundary relation 的局部操作，壓縮至至多五個內部頂點的代表。
