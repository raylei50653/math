# C4 共同 Tait 化約、全染色雙環鎖定與偶補完美匹配判準

2026-10-14。整理使用者先提供的第 1 份回覆，來源基準為
`fdd3e2289254e3f0844e2c595af50080b19f8a05`；初次整理時未 commit／push。
第 2 份回覆到齊後的統一採納與發布範圍另見
[整理紀錄](../../docs/history/2026-10-14-c4-tait-return-publish.md)。
既有 JOINT6 與遞迴 audit 保留各自來源與證據。

**可採納：兩個 XOR 等價式、球面 Tait 反積分、全染色雙環必要條件，
以及涵蓋全部染色的偶補完美匹配等價判準。無界來源排除仍 OPEN；
共同 `K≤22=K≤5` 與 `k≥23` 不變，沒有新增 Lean theorem。**

原來源與完整 fibres 由 [C4 權威入口](../../docs/c5_c4_triangle_core.md)及
[T／T0 完整證明](../2026-10-14-c4-triangle-core-b66f592/PROOF.md)維護。
本報告只整理這兩支的共同代數介面與控制，不補稱完整來源可實現性或一般延拓。

## 1. 同一原圖、指定位置與兩個等價式

令四色為加法群 `F₂²={0,1,2,3}`，加法寫作 XOR。對完整頂點染色 f 定義

\[
\Delta_f(vw)=f(v)\oplus f(w)\in\{1,2,3\}.
\]

以 `T*` 表示本節選定的 T 或 T0；所有指定邊仍是同一張圖中的具名原邊。

| 原分支 | `T*` 及指定原邊 | 原目標的失敗條件 |
| --- | --- | --- |
| 原 `d_G(b)≥5` | `T*=T`，`e₁=xy,e₂=zb`；zxy 是指定三角面，b 不接 x,y | 每份完整染色都令 b 取 zxy 的缺失色 |
| 原 `d_G(b)=4` | `T*=T0`，`e₁=xy,e₂=pq`；zxy、zpq 是只共享 z 的指定三角面，x,y,p,q 互異，xp,xq,yp,yq 均非邊 | 每份完整染色都令兩面使用相同色集合 |

兩支的 `e₁,e₂` 均互不相交。度數、小圈與完整最小來源契約仍須沿用原證明，
不能以任意四連通三角化圖取代。固定 `(z,x,y)=(B,C,D)` 時，第一支原目標為
`f(b)∈{C,D}`，第二支須在同一份完整染色中比較兩面。

四個群元素 XOR 為零，故三角 zxy 的缺失色為
`μ_f(zxy)=f(z)⊕f(x)⊕f(y)`。因而

\[
f(b)=\mu_f(zxy)
\iff \Delta_f(zb)=\Delta_f(xy).
\]

兩個三角共有 z，且各自三色相異。從另外三個可用色取兩色，
每個無序色對的 XOR 互異；所以

\[
\{f(z),f(x),f(y)\}=\{f(z),f(p),f(q)\}
\iff \Delta_f(xy)=\Delta_f(pq).
\]

因此兩支的成功條件都是：存在一份完整染色使 `Δ_f(e₁)≠Δ_f(e₂)`。
這只是原完整 fibres 的精確重述，沒有合併不同染色的可行投影。

## 2. 球面 Tait 染色的反向積分與原色框

取指定球面 embedding 的對偶 `Q=(T*)^∨`，令 `εᵢ=eᵢ^∨`。
頂點染色 f 的原邊色差給 Q 一份以 `1,2,3` 為色的 Tait 染色 c：
每個原三角面三色相異，其三條色差恰為三個非零元素。

反向給定完整 Tait 染色 c，把每條對偶邊的色放回其原邊。
每個原三角面的三條值 XOR 為 `1⊕2⊕3=0`。球面圖的 cycle space
由面邊界生成，所以任意閉路的 XOR 亦為零。從一個固定 root 沿路徑
累加即可得到 f，與路徑選擇無關；每條原邊色差非零，故 f 是 proper 四色染色。
同一 c 的積分只差整圖加一常數。

任意四色名置換都是 `F₂²` 上的仿射置換 `a↦L(a)⊕t`，其中 L 可逆。
對整份 f 同時換色可恢復 `(z,x,y)=(B,C,D)`，所有色差則共同變為 `L(Δ)`，
保持兩條指定邊色差相等或不等。於是搜尋 Q 的全部 Tait 染色，恰能測試
原固定三角色框的存在性；不要求搜尋先停留在某個 Kempe 類。
這個反積分使用球面前提，沒有假設任意 planar graph 可染，也沒有使用四色定理。

## 3. 完全失敗迫出的全染色雙環必要條件

在 cubic Q 的 Tait 染色 c 中，任取兩色 α、β，其雙色子圖是互不相交的偶環。
記 `C^c_{αβ}(ε)` 為含色為 α 或 β 的指定邊 ε 的那個環。

若原目標完全失敗，則**每份**完整 Tait 染色 c 都滿足

\[
c(\varepsilon_1)=c(\varepsilon_2)=\alpha_c,
\qquad
\forall\beta\ne\alpha_c:\quad
C^c_{\alpha_c\beta}(\varepsilon_1)
=C^c_{\alpha_c\beta}(\varepsilon_2).
\]

證明：若某個 αβ 環只含其中一條指定邊，交換那個環上的 α、β，
仍是一份完整 Tait 染色，且指定邊變為異色，與完全失敗矛盾。
任意合法交換所得的新染色也屬全稱量詞範圍，故須重新滿足同一條件。
當前染色畫出的兩條環只是這個全稱必要條件的一個截面。

本節的 **Kempe 類專指 Q 上的 edge-Kempe 類**，交換單一雙色環；
沒有宣稱它與原頂點染色的所有 vertex-Kempe 操作等同。
若全稱條件只在一個 edge-Kempe 類成立，只能證那一類不能解鎖。
以下三個陳述的量詞不同，不能相互替代：

1. 一份當前染色的兩個相關環都含兩條指定邊。
2. 一個完整 edge-Kempe 類的所有染色都令兩條指定邊同色。
3. Q 的全部完整 Tait 染色都令兩條指定邊同色。

由 1 升到 2 仍須處理其他交換；由 2 升到 3 仍須處理其他類。
正二十面體控制在第 2 層受阻，卻在第 3 層存在成功染色。

## 4. 平面性與四連通性的使用界線

同一份 c 的 αγ 環與 αβ 環可能共用 α 色邊，尤其共同包含 ε₁、ε₂。
它們不是頂點互不相交的互補色跨路；不能只由交錯端點圖示套 Jordan 矛盾。

原 T* 四連通，使 Q 沒有非平凡三邊割：球面對偶中的三邊 bond 對應
原三角形，四連通性排除 separating triangle，facial triangle 對應
只隔出一個對偶頂點的平凡割。若想用這項限制排除全染色鎖定，
仍須另外證明鎖定真的迫出非平凡三邊割；本報告沒有這一步。

| 控制圖 | 已確認的鎖定 | 適用界線 |
| --- | --- | --- |
| 五角雙錐：C₅ 加兩個皆接全部環點的頂點 u,v | 四連通；每份 proper 四色染色都迫 `f(u)=f(v)`，故任何環點 r 都有 `Δ(ur)=Δ(vr)` | 指定原邊共享 r，不符合本題互不相交的位置；也未滿足原最小來源契約 |
| 正二十面體及其正十二面體對偶 | 五連通、全部五度，合法 zxy／zb 位置；一個完整 edge-Kempe 類鎖定，另一完整染色可解鎖 | 只有 T 層位置、連通性及度數控制；沒有完整最小來源契約，不能作原命題反例 |

五角雙錐的全染色強迫可直接證明：若 u,v 異色，奇環 C₅ 每點只能用
其餘兩色，不可能 proper 染色。刪至多三點後仍連通：若保留某 apex，
它連著所有剩餘環點；若兩 apex 都刪，最多再刪一個環點，剩餘環路徑連通。
刪除 u,v 及環上兩個不相鄰點，剩餘環分成兩條非空路徑，故連通度恰四。

兩個控制沒有證明符合本題互不相交位置的四連通圖能有全部染色鎖定。
四連通與平面性尚未提供這項全稱鎖定的已證排除；控制只裁定上述局部／單類推理界線。

正二十面體控制原程式已從使用者提供的 `/tmp/verify_icosahedron_lock.py`
原樣保存為 [verify_icosahedron_lock.py](controls/verify_icosahedron_lock.py)。
其頂點標記為 `0,…,11`，角色 `(z,x,y,b)=(0,2,3,5)`；原邊
`xy=(2,3)`、`zb=(0,5)` 互不相交，zxy 是面，b 不接 x,y。兩份完整染色為

```text
f=(0,1,2,1,2,3,3,0,3,0,2,1)
g=(0,1,2,1,3,2,0,3,0,1,3,2)
```

兩份都已同用 `z=0,x=2,y=1` 的色框。f 的指定色差為 `3,3`，
三組雙色子圖都是長 20 的 Hamilton 環；每次 edge-Kempe 交換只能
全域交換兩個色名，後繼仍有此 Hamilton 性質，故整類鎖定。
g 的指定色差為 `3,2`，提供另一類的成功完整染色。
共同換色 `0→B,2→C,1→D,3→A`，便得原固定框的 `f(b)=A,g(b)=C`。

## 5. 涵蓋全部染色的偶補完美匹配等價判準

定義

\[
\mathcal M_{\rm even}(Q)=
\{M: M\text{ 是完美匹配，且 }Q-M\text{ 的每個環皆為偶環}\}.
\]

對同一張 cubic Q 及同一對指定邊，精確地有

\[
\boxed{
\exists c\text{ 完整 Tait 染色}:c(\varepsilon_1)\ne c(\varepsilon_2)
\iff
\exists M\in\mathcal M_{\rm even}(Q):
|M\cap\{\varepsilon_1,\varepsilon_2\}|=1.
}
\]

正向取 c 中 ε₁ 所用色的整個色類為 M；每個 cubic 頂點恰有一條該色邊，
故 M 完美匹配，而其餘兩色交替成偶環。ε₂ 異色，所以 M 恰含一條指定邊。
反向把 M 染一色，再將 Q−M 的每個偶環交替染另外兩色，得完整 Tait 染色；
唯一位於 M 中的指定邊即與另一條異色。

因此完全鎖定等價於：每個 M_even 中的匹配，都同時包含兩條指定邊，
或同時不包含。這個測試遍及全部 Tait 染色，不假設 edge-Kempe 連通性。
若 `M_even=∅`，兩側的存在性都為假，全稱鎖定為 vacuous；原來源的已知
非空 fibre 則保證至少有一份完整染色，不能略去這項來源前提。

有限測試應保存具名 embedding、全部匹配與偶環補圖、指定邊身份及由匹配
交替染色／反積分得到的一份 full lift。匹配不存在的結論只適用於所列固定 Q，
不能升成所有原來源排除；獨立可行匹配也不能拼成同一來源的共同 witness。

## 6. 最小性接回仍 OPEN

取得原來源矛盾，尚須在同一份來源中完成以下一項：

- 由全染色鎖定迫出違反已採納結構限制的具體小割集。
- 在同一完整染色中證得真正的平面交叉矛盾，保留原 paths 與共同端點關係。
- 構造合法較小來源，內點嚴格減少，且保留所需完整關係與接回資料。

任意刪環、縮環、換外框或抽取一個染色的環，都未自動取得上述接回保證。
較小圖的相對可染性只可在已採納點數範圍使用，不能改成任意 planar graph 可染。
本輪精確窄問題為：**原來源的指定邊位置、度數與小圈限制，是否迫使
某個 `M∈M_even(Q)` 恰好包含其中一條指定邊？**
目前排程與其他 C4 六接點子域見 [Kempe 導覽 §3](../../docs/c5_kempe_guide.md#3-停止點與保留缺口)。

## 7. 證據、重播與整理範圍

紙面部分為 §§1–6 的代數化約、環交換必要條件與匹配等價式。
正二十面體是具體有限控制；沒有證目標來源存在，也沒有一般來源排除。

```bash
python3 -B audits/2026-10-14-c4-tait-lock-review-fdd3e22/controls/verify_icosahedron_lock.py
python3 -B audits/2026-10-14-c4-tait-lock-review-fdd3e22/controls/check_matchings.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-14-c4-tait-lock-review-fdd3e22/controls/check_matchings.py --check
python3 scripts/check_docs.py
python3 tools/docgraph --include 'docs/**/*.md' check
python3 tools/docgraph check
lake build --no-ansi
git diff --check
```

原控制輸出保存於 [icosahedron.stdout.log](controls/icosahedron.stdout.log)；
匹配控制及整理檢查的實際結果列於 [VERIFICATION](VERIFICATION.md)。
控制程式不依賴 networkx、四色定理 oracle 或外部枚舉。

相關研究僅作術語與信任界線的背景：belcastro–Haas，
[Counting edge-Kempe-equivalence classes for 3-edge-colored cubic graphs](https://arxiv.org/abs/1209.1730)
證明的是 2-connected **planar bipartite** cubic 圖的單一類結果，不能只憑 planar cubic
套用；Goedgebeur–Östergård，
[Switching 3-edge-colorings of cubic graphs](https://arxiv.org/abs/2105.01363)
研究類數、switching 與有限計算。本輪鎖定控制與匹配等價式的證據在本地，
無界來源排除不依賴這兩篇作未核實的普遍定理。

Updated：C4 權威入口、Kempe 導覽及 STATUS 對應摘要，補共同測試與全稱界線。
Reviewed-unchanged：HANDOFF 研究線／tags、README 路由、跨線 synthesis 的一般界、
既有 JOINT6 結果與其他 audit 原證書。主題仍 OPEN，propagation 停在直接主題摘要。
Remaining OPEN：全染色鎖定的來源排除、嚴格較小合法替換及一般 `K∞=K≤5`。
