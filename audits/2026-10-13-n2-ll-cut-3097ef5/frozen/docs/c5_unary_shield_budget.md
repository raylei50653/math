# 不依賴 ε 的盾弧預算與 hub 原則

2026-10-04，基準 `83ca618`。這是 [Kempe 導覽](c5_kempe_guide.md) 候選來源線上
「把反覆出現的機制抽成統一預算」的第一步；目前停止點仍由導覽維護。

**結論。** 在固定完整 Σ=933／941 的 Σ-edge-minimal disk 來源中，
**不論 ε 多大、有幾個 roots、roots 是否相鄰**：

1. 每份 one-sided 分量（定義見 §1）的實際支援是一段連續框弧，且不同分量的框弧
   **邊集互斥**（定理 A、引理 2）。
2. 全圖至多兩份 unary 分量；若恰兩份，它們的盾弧長為 (2,2) 或 (2,3)，所有
   roots 的 spokes 與所有 mixed 分量的支援只能落在 3 個或 2 個指定框點（定理 A）。
3. 短支援引理、二／三-hub Gallai K₅ 與同列端點 hub 都是同一個 **hub 原則**的特例，
   連通外框 K₄ 引理則是它的證明步驟。這個原則允許 roots 放進 hubs，因此也適用於
   mixed 分量（定理 B）。其直接推論是：短支援的 one-sided mixed 分量，在每份拒絕見證中，
   相鄰 roots 都不能同色（推論 B2）。

既有報告已在單一 root 的扇形或相鄰雙 root 的 zw 鄰域分別證過「三份分量要六段跨度」。
本頁把它改寫成不依賴 ε、跨 root 的面論證，並補上連續性與 spokes 限制。

**用在現存殘留上的效果：** 任務 A 系列在 A₄ 之後保留 40／58 份 actual U 支援紀錄，
其中 12／22 份是不連續支援（013、023、134），另有 4／6 份的 spoke 落在 U 盾弧內點。
兩者直接刪去後剩 **24／30 份紀錄**，完整 singleton schedules 由 50／84 降為 **30／50**。
16／20 個具名 frames 各至少留一份，所以**沒有整份 frame 被排除，也沒有排除任一候選**（§6）。
證據層：§2–§4 是任意大小紙面證明。定理 B 沿用外部 degree-list／Gallai 刻畫
及既有二／三-hub 引理。Python 只做有限控制（§7），沒有新增 Lean theorem。

## 1. 前提與記號

**固定來源前提（S）。** G 有限簡單平面圖，B=(b₀,…,b₄) 是指定有序 induced C₅，
圍出外面；Σ(G) 屬於 933 或 941 的 D₅ 軌道；每條非框邊都 Σ-critical。
沿用 [容量報告 §1](c5_independent_support_capacity.md#1-兩種-minimality-與來源的基本結構) 的已證事實：

- 有效內部 H=G−B 連通；
- 每個內點完整 degree≥4；
- G 碰齊五個框點；
- R={v∈H : deg_G v≥5} 非空（ε≥2）。

**分量（piece）。** G[H∖R] 的連通分量，所有頂點完整 degree 恰 4。
若只鄰接一個 root 則稱 *unary*，否則稱 *mixed*。S_P=N_B(P) 為實際支援。
若 H−P 非空且連通，稱 P 為 *one-sided*。

**引理 0。** (i) H−P 的每個連通分量都含一個與 P 相鄰的 root。
(ii) 因此 unary 分量必為 one-sided；若 G[R] 連通，則所有分量都 one-sided。

*證明。* H 連通，所以 H−P 的每個分量都與 P 相鄰。P 是 H−R 的分量，
它在 H 中的鄰點只能是 roots，故 (i) 成立。unary 分量只有一個 root 鄰點；
若 G[R] 連通，所有 roots 落在 H−P 的同一分量。∎

特別是現有 ε=2 的相鄰雙 root 分支，以及唯一 root 分支，所有分量都是 one-sided。

## 2. 盾弧：純平面拓撲

本節只用到：平面圖 G、B 圍外面、H 連通。不用到顏色。

對 one-sided 分量 P，令 K_P=B∪G[P]∪E(P,B)。H−P 連同其所有邊都不與 K_P 相交，
因此整個落在 K_P 的同一個內面 F_P 中。每條框邊恰在一個內面上。定義

\[
\sigma_P=\{\text{不在 }\partial F_P\text{ 上的框邊}\}\qquad(\text{盾弧}).
\]

**引理 1。** 設 P, P′ 為互斥的 one-sided 分量。

- (a) **連續。** σ_P 是 B 上一段連續弧（可為空或全 B）。
- (b) **支援標記。** 若 |S_P|≥2，則每個 v∈S_P 至少關聯一條 σ_P 邊。
  因此，若 S_P 不包含於某條框邊的兩端點，則 |σ_P|≥2。
- (c) **限制。** 若 σ_P≠B，則 N_B(H−P) 的每一點都關聯一條非 σ_P 的框邊；
  也就是說，H−P 不會接到 σ_P 的內點。
- (d) **互斥。** σ_P∩σ_{P′}=∅。

*證明 (a)。* 設 e、e′ 都在 ∂F_P 上，在 F_P 內取一條簡單弧 α 連接兩邊的內點。
α 把 disk 切成兩塊，各含 B 在 e、e′ 之間的一段弧。P 連同其附件邊是連通的，
且與 α 不交，所以整個落在其中一側。另一側的開區域不含 K_P 的點，因此屬於同一個面；
它與 α⊆F_P 相鄰，所以就是 F_P。於是該側的所有框邊都在 ∂F_P 上。
換言之，任兩條 ∂F_P 框邊之間總有一側全由 ∂F_P 框邊組成，
所以 ∂F_P 框邊構成連續弧，其補集 σ_P 也是。

*證明 (b)。* 反設 v∈S_P 的兩條框邊都在 ∂F_P 上。在兩邊上靠近 v 處各取一點，
用 F_P 內的弧 α 連起來，與框角 p⁻vp⁺ 合成閉曲線 γ。disk 內靠近 v 的點都在 γ 內部，
所以從 v 出發的附件邊 vc（c∈P）進入 γ 內，因而整個 P 都在 γ 內（P 與 γ 不交）。
另取 s*∈S_P∖{v}。框點 s* 不在 γ 上，且其附近有 disk 外的點，故 s* 在 γ 外。
附件邊 c*s* 只在 s* 碰到 B，又不碰 α⊆F_P，卻必須從內部穿到外部，矛盾。
若 S_P 不包含於任一框邊的兩端點，則 S_P 含兩個不相鄰框點，
同一條邊不能同時關聯它們，所以 |σ_P|≥2。

*證明 (c)。* 設 xu 是邊，x∈B，u∈H−P。這條邊位於 F_P，所以 F_P 包含 x 處、
含 xu 的那個角扇區。若扇區兩側的 K_P 邊至少一條是框邊，那條框邊就在 ∂F_P 上。
否則兩側都是附件邊 xc₁、xc₂。取 P 內一條 c₁–c₂ 路徑，得到只在 x 碰 B 的閉曲線；
扇區在它的內部，於是 F_P 也整個在內部，∂F_P 不含任何框邊，即 σ_P=B，矛盾。

*證明 (d)。*（2026-10-04 更正：原稿寫「F_P 與 E 的閉包不交」，此句錯誤，兩面的閉包可共用框點
甚至整段內部路徑；見 [q-core 報告 §3.1](c5_qcore_shield_budget.md#31-引理-1-不需修改) 與
[D₆ 稽核 §2.3](../audits/2026-10-04-task-d6/REPORT.md#23-跨-root-互斥與措辭更正)。下文已改為只用開面，結論不變。）
反設 e∈σ_P∩σ_{P′}。令 K=K_P∪K_{P′}，Z 是 K 中以 e 為邊界的內面。
Z 包含於 K_P 中以 e 為邊界的面 E；因 e∈σ_P，E≠F_P。
P′ 的每個非框點（含其附件邊的非框部分）都在**開面** F_P 中，因而有一個完全落在 F_P 的小鄰域，
與 E 不交；所以它不在 E 的閉包裡，也就不在 ∂Z 上。對稱地，∂Z 也不含 P 的非框點。於是 ∂Z⊆B。這樣 Z 在開 disk 內既開又閉，只能是整個開 disk，
與 P≠∅ 矛盾。∎

**引理 2（固定來源的支援區間）。** 在前提 (S) 下，若 one-sided 分量 P 有 |S_P|≥2，
則 S_P=V(σ_P)。也就是說，實際支援恰好是一段連續框弧的全部頂點，
其邊數為 |S_P|−1（S_P=B 時為 4 或 5）。

*證明。* 先看 σ_P=B 的情形：∂F_P 沒有框邊，它碰到的框點都是附件點，
所以 N_B(H−P)⊆S_P。G 碰齊五框點，得 B∖S_P⊆N_B(H−P)⊆S_P，即 S_P=B。
其餘情形下 σ_P≠B，且由 (b) 知 σ_P≠∅。
σ_P 的內點 x 若不在 S_P，它被 H−P 的某點碰到，與 (c) 矛盾。
σ_P 的端點 v 恰有一條框邊在 ∂F_P 上；若 v∉S_P，v 的 K_P 邊只有兩條框邊，
同一個內角扇區會讓兩邊同屬一面，矛盾。所以 V(σ_P)⊆S_P；反向包含即 (b)。∎

例如支援 {b₀,b₂} 的 one-sided 分量不可能出現：b₁ 必須被別的點碰到，
但它被夾在盾弧內。

## 3. 定理 A：全圖至多兩份 unary 分量

**定理 A。** 在前提 (S) 下，對任意 ε：

1. 每份 unary 分量 U 都滿足 |σ_U|≥2，且 S_U 是至少三個連續框點；
2. 所有 one-sided 分量的盾弧兩兩邊互斥，所以 Σ_P|σ_P|≤5；
3. 全圖至多兩份 unary 分量；
4. 若恰有兩份 U₁、U₂，則 (|σ₁|,|σ₂|)∈{(2,2),(2,3)}。所有 roots 的 spokes 與所有 mixed
   分量的支援都避開 σ₁、σ₂ 的內點：

   - (2,2) 時，旋轉後 σ₁=b₀b₁b₂、σ₂=b₂b₃b₄，可用框點只剩 {b₄,b₀,b₂}；
   - (2,3) 時，σ₁=b₀b₁b₂、σ₂=b₂b₃b₄b₀，可用框點只剩 {b₀,b₂}。

   此時其他 one-sided 分量的盾弧至多一條邊。

*證明。* 對 unary U 與它的 root r，取一條接點邊 e=rp。G−e 新接受某列 q，取一份延拓 f。
因為 G 不接受 q，必有 f(r)=f(p)=a，且 a∈F_U(q)：否則 U 可以重新著色避開 a，
G 就能延拓 q。所以 F_U(q)≠∅。

若 S_U 包含於某條框邊 {a′,b′}，五框點中另有 h∉{a′,b′} 被 G 碰到。
碰到 h 的內點不在 U，所以在 H−U 中，並在 H−U 內連到 r，構成避開 U 的外部路徑 L。
[短支援引理](c5_short_support_singleton.md#4-三-hub-引理排除未見色接點數不設上限)
（連同 [t=0 的外部路徑補註](c5_excess_two_no_spoke_complete.md#2-無-spoke-的真實外部-hub-與共同跨度)）
於是給出 F_U≡∅，矛盾。因此 S_U 不包含於任一框邊；由引理 1(b) 與引理 2 得第 1 點。

第 2 點即引理 0 加上引理 1(d)。第 3 點由 2+2+2>5 得到。
第 4 點：兩段長度至少 2 的互斥連續弧在 C₅ 上只有這兩種配置；
spokes 與 mixed 支援都屬於 N_B(H−U_i)，再用引理 1(c) 即可。∎

**推論。** 只有一個 root（任意 degree 4+ε）時，所有分量都是 unary，
所以至多兩份分量，deg r=t+k₁+k₂，且 t≤3。

既有結果與定理 A 的關係：唯一 degree-6 的 t=0／1／2／3 各分拆、
[四-spoke (3,1) 的兩原 unary 六跨度](c5_excess_two_mixed_core_four_spoke_singles.md)、
[no-mixed 的 ℓ_z+ℓ_w≤5](c5_no_mixed_span_budget.md#21-同序支援與兩側框弧)，
都是本定理在特定 ε、特定 root 配置下的實例。
新增的部分是：跨 root（包括非相鄰 roots）、任意 ε、支援的連續性，以及 spokes 的限制。

## 4. 定理 B：hub 原則

**定理 B。** 設 G 為平面圖，P⊆V(G) 連通，P 的每點在 G 中 degree 恰 4。
ψ 是 G−P 的合法四色染色，且無法延拓到 P（稱 ψ 為 P 的*拒絕見證*）。
若存在 k≤4 個兩兩互斥、各自連通、兩兩相鄰的集合 X₁,…,X_k⊆V(G)∖P，滿足

- N(P)⊆⋃X_i；
- ψ 在每個 X_i∩N(P) 上取常數 c_i，且這些常數兩兩不同，

則得到矛盾（G 含 K₅ minor）。

*證明。* 令 L(v)=U∖ψ(N(v)∖P)，則 |L(v)|≥deg_P v。若某點不等號嚴格成立，
沿以它為根的生成樹貪婪著色即可延拓，所以每點都是 tight 的：
每點的外鄰顏色兩兩不同，特別是每點在每個 X_i 至多有一個鄰點。
把各 X_i 收縮成 x_i 並刪除其他頂點，得到 G 的 minor J。在 J 中，P 的每點 degree 仍為 4，
list 不變，所以 P 在 J 中仍不可著色。刪去不與 P 相鄰的 x_i，剩 k′ 個：

- k′=4：連通的 P 加上兩兩相鄰的四個 hub，直接是 K₅；
- k′=2,3：即 [兩-hub 引理](c5_short_support_singleton.md#3-兩-hub-gallai-引理五個-branch-sets)
  與 [三-hub 引理](c5_short_support_singleton.md#4-三-hub-引理排除未見色接點數不設上限)。
  兩者所需的 K₄-free 由 [連通外框 K₄ 引理](c5_degree5_tree_components.md#1-連通外框排除-degree-4-分量的-k4)
  給出，因為 ⋃x_i 是連通的；
- k′=1：每點至多一個外鄰，所以 min deg_P≥3。由外部 Gallai 刻畫，P 是 Gallai tree，
  每個末端 block 都是 K_m（m≥4）。若 m≥5，P 本身含 K₅。若 m=4，取該 block 的三個私有點
  p₁,p₂,p₃ 與割點 w（若無割點，四點全接 x₁，直接得 K₅）。
  branch sets 取 {p₁},{p₂},{p₃},{w}，以及 {x₁}∪(P 的其餘部分)。
  後者連通，因為其餘每個分支都含一個末端 K₄，其私有點接 x₁。∎

**與現有機制的對應。**

| 既有機制 | 對應的 hubs |
| --- | --- |
| 短支援（已見色） | X={b}，Y=(B∖{b})∪{r}∪L，k=2 |
| 短支援（未見色） | {a}、{b}、(B∖{a,b})∪{r}∪L，k=3 |
| 連通外框 K₄ 引理 | 定理 B 證明中排除 K₄ block 的步驟（hub 只需連通，不需同色） |
| [同列端點 hub](c5_excess_two_mixed_core_four_spoke_hubs.md)、[原 crosscut](c5_excess_two_mixed_core_four_spoke_crosscut.md) | 二／三 hubs，以同色 tightness 保持 degree |
| [B₂](c5_excess_two_mixed_core_four_spoke_mixed22_short_face.md)／[B₃](c5_excess_two_mixed_core_four_spoke_mixed22_long_face.md) 的 leaf K₅ | 末端 block 私有點接到經原外路徑連通的 hubs |

**推論 B2（短支援 one-sided 分量的 roots 不能同色）。** 在前提 (S) 下，
設 P 是 one-sided 分量（unary 或 mixed），S_P 包含於某條框邊 {a,b}。
則 P 的每份拒絕見證都讓 P 的相鄰 roots 至少用兩種顏色。

*證明。* 反設所有相鄰 roots 都是色 c。H−P 連通；它在 P 的鄰點恰為這些 roots；
它碰到 B∖{a,b} 的每一點（G 碰齊五框點，而這些點不在 S_P）。

- 若 c∉{ψ(a),ψ(b)}，取 {a}、{b}、Z=(B∖{a,b})∪(H−P)，k=3；
- 若 c=ψ(a)，取 {b}、Z′={a}∪(B∖{b})∪(H−P)，k=2。

兩種情形都滿足定理 B 的條件，矛盾。∎

每份分量至少有一份拒絕見證：取任一接點邊 e，G−e 的新列延拓限制到 G−P 即是。
unary 時 B2 就是短支援引理。mixed 時它是新的、不依賴 ε 的限制，
但它只約束相鄰 roots 可以同色的情形。現有 ε=2 相鄰雙 root 分支中，z、w 永遠異色，
所以 B2 在那裡是空的。

## 5. 機制帳本

依各報告自己標示的主要論證，現有排除大致分成六族。
代表報告只舉例，不是逐份完整分類。

| 族 | 內容 | 是否已不依賴 ε | 代表報告 |
| --- | --- | --- | --- |
| Φ1 預算／省略身份 | D+O(+κ)=deg−4；全 degree-4 省略圖恰缺一列，所以省略身份跨列不重用；unary 的 D 身份守恆與奇偶矛盾 | 恆等式是；跨列身份只在 ε 小時有力 | [四容量子覆蓋](c5_excess_one_subcovers.md)、[root 預算](c5_root_degree_excess.md) |
| Φ2 盾弧／跨度 | 穩定子 ℓ≥3−\|F\|、短支援 ℓ≥2、共同 lifts≤5 | **是（定理 A）** | [容量與六跨度](c5_independent_support_capacity.md)、[t=1 全分拆](c5_excess_two_single_spoke_complete.md)、[四-spoke singles](c5_excess_two_mixed_core_four_spoke_singles.md) |
| Φ3 hub K₅ | 同色 tightness 收縮成 hubs 後得 K₅ | **是（定理 B）**；但 hubs 的存在要逐例構造 | [短支援](c5_short_support_singleton.md)、[同列端點 hub](c5_excess_two_mixed_core_four_spoke_hubs.md)、[B₂](c5_excess_two_mixed_core_four_spoke_mixed22_short_face.md)、[B₃](c5_excess_two_mixed_core_four_spoke_mixed22_long_face.md) |
| Φ4 延拓／非 critical | lists 有 slack 時用貪婪或三-hub 延拓整份分量，使某邊非 critical | 原理是，配置要逐例 | [A₄](c5_excess_two_mixed_core_four_spoke_mixed12_04_04.md)、[crosscut](c5_excess_two_mixed_core_four_spoke_crosscut.md)、[leaf-slack](c5_excess_two_mixed_core_four_spoke_quaternary.md) |
| Φ5 指定列完整 joint | 在指定拒絕列上構造或否定完整 joint | 否 | [A](c5_excess_two_mixed_core_four_spoke_mixed12.md)、[A₂](c5_excess_two_mixed_core_four_spoke_mixed12_01_12.md)、[短框弧](c5_excess_two_mixed_core_four_spoke_short_arc.md)、[leaf 纖維](c5_excess_two_mixed_core_leaf_fibers.md) |
| Φ6 parity | 完整 degree 握手式迫奇數附件 | 否 | [B₄](c5_excess_two_mixed_core_four_spoke_mixed22_shared4.md) |

Φ2、Φ3 現在都有不依賴 ε 的陳述。案例樹最近的增長幾乎都發生在 Φ4／Φ5：
固定 spoke-pair、face、附件後，對 mixed 分量逐一核對 joint 或延拓。
這與定理 A 的結構一致：unary 分量已被框住，剩下的自由度都在 mixed 分量與 root 骨架上。

## 6. 對現有案例樹的影響與剩餘缺口

**立即可用。**

- ε≥3 與非相鄰 roots：任何含三份以上 unary 分量的分拆直接為空；
  兩份時 spokes 與 mixed 支援被限制在 2–3 個框點。
- 任何 one-sided 分量的支援都是連續框弧。必要域表若含稀疏支援（例如 {0,2}），
  可直接刪去；每份 one-sided mixed 分量的盾弧也必須與 unary 盾弧邊互斥。

**沒有關閉的部分（誠實界線）。**

- 任務 A 的殘留：引理 2 與 1(c) 只刪支援紀錄（見上），沒有清空任何 frame。
  剩下的 24／30 份全是連續支援，關閉它們仍要處理 mixed 分量 C。
- 任務 B 的 W933-129 沒有 unary 分量；z、w 相鄰，所以 B2 為空。
  引理 2 仍要求 C 的支援是連續框弧，但該 artifact 沒有逐份列出 C 的支援，本輪未套用。
- 任務 C（weak-deletion 的共鄰 P₃）屬於單列 minimal q-core 的設定，
  不是固定完整 Σ 來源，前提 (S) 不成立，本頁結論不能直接套用。
- mixed 分量的盾弧沒有下界：[容量報告 §6](c5_independent_support_capacity.md#6-小型控制重播與信任範圍)
  的條件 mixed 控制顯示，支援 {b₀,b₁} 仍可能有非空禁色。

**不依賴 ε 的下一題（建議取代逐 pair 細拆）。** 第 1 題已登記為 [Kempe 導覽 §3](c5_kempe_guide.md#3-停止點與保留缺口) 的優先入口。

1. **雙色 roots 的 hub linkage。** 設 one-sided mixed 分量 P 的支援在框邊 {a,b} 內，
   拒絕見證讓相鄰 roots 用兩色 c₁≠c₂（相鄰 z、w 正是這個情形）。
   問題是在 disk 中，哪些環序配置讓 {a}、{b}、X_{c₁}、X_{c₂} 可以兩兩相鄰地連通。
   可以連通就由定理 B 排除；不能連通時，應該只剩交錯環序 a–c₁–b–c₂ 這類 Kempe 型阻擋。
   若能分類這些阻擋，就能一次涵蓋 B₂／B₃／crosscut 及 A 系列的大部分 hub 論證，
   而不必逐 spoke-pair 處理。
2. **分隔型 mixed 分量。** G[R] 不連通時，mixed 分量可能把 disk 分隔，引理 1 不適用。
   需要證明它們是 one-sided，或給出分隔型的獨立預算。
3. **與 Φ1 接合。** 把 Σ_P|σ_P|≤5 與逐列的 D+O 恆等式放進同一個不等式：
   每列的禁色需求要由有限的框弧容量支付。這是把整條線變成 ε 歸納或 ε 上界的候選途徑。

## 7. 有限控制與重播

[Checker](../scripts/c5_unary_shield_budget.py) 產生
[observations.json](../artifacts/c5_unary_shield_budget/observations.json)，包含三部分。

**A：盾弧拓撲。** 用固定種子生成 2,700 張平面 disk 圖：先隨機三角化五邊形、
再隨機翻邊（不產生框弦）、隨機刪內邊，並隨機選 R。
用三角面直接計算 F_P 與 σ_P，逐一檢查：

- 引理 1(a)(c)：連續性與限制；
- 引理 1(d)：兩兩互斥，共 441 對非平凡盾弧；
- 「長盾弧≤2」從未違反，有 30 張圖恰兩份；
- 引理 2：在內部碰齊五框點的 1,094 個情形中，支援都等於盾弧頂點集。

另外 258 例屬於「兩個 gap 都容納其餘附件」的歧義情形。
最初版本用「任選 gap」定義盾弧，會在此類例子失敗。這說明盾弧必須按面定義，
本頁的陳述與證明都採面定義。這些隨機圖不是 933／941 來源，只檢驗純拓撲引理。

**B：hub 原則。** 窮舉所有至多 7 點、最大 degree≤4 的連通圖 P，以及所有接法：
k=1..4 個兩兩相鄰、顏色互異的 hubs，使每點 degree 恰 4 且每個 hub 至多一條邊。
共 6,091,827 份接法，其中 8,853 份不可著色；每份都經 networkx 驗證 J 非平面
（k=1／2／3／4 分別為 2／10／119／8,722 份）。這是有限控制，不取代 §4 的紙面證明。

**C：A₄ 殘留支援的刪減。** 讀取
[A₄ artifact](../artifacts/c5_excess_two_mixed_core_four_spoke_mixed12_04_04/observations.json)
（記錄輸入 SHA-256）。對每個殘留 frame 中標記為 `necessary_original_U_relation_only`
的 U 支援紀錄，刪去以下兩類：

- 不連續的支援（引理 2）；
- 兩 roots 的 spokes 落在 U 支援區間內點的紀錄（引理 1(c)）。
  S_U=B 時盾弧可能是整個 B，所以這類紀錄一律保留，不作限制。

結果為 933：40→24 份紀錄、50→30 份 schedules；941：58→30 份、84→50 份；
每個 frame 至少保留一份，逐 frame 的保留紀錄存於 artifact。
這一層只刪必要支援紀錄，不涉及 C 的完整 relation，也不涉及來源實現。

```bash
.venv/bin/python scripts/c5_unary_shield_budget.py --check
PYTHONHASHSEED=17 .venv/bin/python scripts/c5_unary_shield_budget.py --check
python3 scripts/check_docs.py
python3 tools/docgraph check
```

Part C 讀取的 A₄ artifact 超過 1 MB、不進 git；新 checkout 先依
[封存還原說明](../audits/README.md)執行 `python3 tools/audit_archive.py restore --artifacts`。
本輪實際執行了上述四條命令。
引理 1、2 與定理 A、B 未 Lean 化。
