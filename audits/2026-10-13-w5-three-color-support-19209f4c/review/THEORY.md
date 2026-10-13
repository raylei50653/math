# W₅ 三色 support 充分條件：獨立理論審查

基準 `19209f4c`；2026-10-13。此稿以
[正式 W₅ 契約](../../../docs/c5_w5_marked_relation.md) 為原始入口。
本輪沒有援引四色定理或最小性來保證任何指定外框可染。
以下是對任意有限合法 annulus 的紙面證明；有限枚舉只核對指定控制圖。

## 1. 精確前提及結論

色集固定為 `C={0,1,2,3}`，各頂點皆可使用全部四種顏色，染色指普通 proper
頂點染色。固定互不相交的具名有序圈
`B=(b0,...,b4)`、`U=(u0,...,u4)`；兩圖中的名稱逐點對應，不許旋轉或反轉
索引，也不許只對 U 獨立更名顏色。

令 H、H′ 是嵌入同一 annulus 槽位的有限簡單 plane 圖。外邊界是原 B；U 是
induced C₅，圍出的有界內面為空。两圖的邊及私人頂點均在 annulus 中；替換
時保留兩條具名邊界的方向、標籤及所有另行宣告的外部接合。此处兩圖可有
不同的私人頂點集和 annular 邊，不能默認彼此存在 minor 映射。

令 `G=H+v`、`G′=H′+v′`：把中心放入指定 U 空面，恰加五條 `vu_i` 或
`v′u_i`，中心沒有其他鄰點。五條 spokes 在空面內作 cone，形成五個三角面。
將 v 與 v′ 視為同一個替換槽位的中心名稱。這明確給出兩個合法 plane disk
圖，沒有交叉識別或省略未記錄附件。

對每一字面外框染色 `β∈C^5`、字面鄰環染色 `τ∈C^5`，定义完整 fibre

\[
J_H(\beta,\tau)=\{\eta:V(H)\to C:\eta\text{ proper},
\eta|_B=\beta,\eta|_U=\tau\},
\quad
R_H^{(3)}=\{(\beta,\tau):J_H(\beta,\tau)\ne\varnothing,
|\operatorname{im}\tau|=3\}.
\]

`Σ(G)` 是在原 B 標籤及相同 C 色框下可延伸的全部 β，等價地可記為既有十列
代表的接受集合。不存在的格子仍是空，不得刪掉空格後重新編號。

**命題 W5-3SUP。** 在上述前提下，

\[
\boxed{\quad\Sigma(G)=\pi_B R_H^{(3)}.\quad} \tag{1}
\]

因此 `R_H^(3)=R_H′^(3)` 蘊含 `Σ(G)=Σ(G′)`。更精確地，兩個完整外框關係
相等的充要條件是 `π_B R_H^(3)=π_B R_H′^(3)`；三色 support 相等是較強的
充分條件。若只有單向 support 包含，則得到同方向的外框關係包含及下述
單向完整染色傳送。

## 2. 證明及雙向延伸構造

**中心延伸引理。** U 上任何 proper 染色至少用三色，因為奇圈不能二染；
色集 C 又只有四色。因此 proper τ 只可能用三或四色。中心必須避開全部
`im τ`，故可以補中心當且僅當 τ 用三色；此時中心顏色唯一，記為
`m(τ)∈C\im τ`。

具體地，對每個 β 有自然雙射

\[
E_H:\coprod_{\tau:(\beta,\tau)\in R_H^{(3)}}J_H(\beta,\tau)
\longrightarrow\mathcal C_G(\beta),\qquad
E_H(\eta)=\eta\cup\{v\mapsto m(\eta|_U)\}.
\tag{2}
\]

逆映射只刪去中心的色值。原 H 邊 proper；新五條 spokes 也因缺色而 proper；
反向則因中心避開 U，proper U 至多用三色而又至少用三色。這證明雙射及
(1)，不需要任何有限枚舉。□

現在假定 `R_H^(3)=R_H′^(3)`。為兩圖各自的私人頂點固定一個順序。
對每個三色非空 cell，以有限窮舉選出字典序最小的完整 witness，記為
`s_H(β,τ)∈J_H(β,τ)` 及 `s_H′(β,τ)∈J_H′(β,τ)`。
給定任意 `γ∈C_G(β)`，令 `τ=γ|_U`，定義

\[
F_{H\to H'}(\gamma)=
s_{H'}(\beta,\tau)\cup\{v'\mapsto\gamma(v)\}.
\tag{3}
\]

式 (2) 保證 τ 用三色，support 相等保證目標 fibre 非空，而且
`γ(v)=m(τ)`，所以 (3) 是 G′ 的完整 proper 染色。逐字保留原 B、原 U 及
中心色值；私人點用目標的實際合法 witness，沒有拼湊不同 cells。
交換 H、H′ 即得另一方向。

這個「構造」是有限、可停止的染色演算法：按固定私人頂點順序窮舉四色
assignments，檢查全部目標邊，取第一份通過者。它不是多項式時間承諾，也
不是 graph minor 構造。幾何合法性由指定 annulus 嵌入與空面 cone 預先提供，
而非從 support 相等反推平面性。

兩向函數一般不互為逆、不單射，也不保留 fibre 基數。式 (2) 才是對單一圖
H 與其補中心圖 G 的自然雙射；不可將它誤套成 H 與 H′ 之間的雙射。

## 3. 十列代表與完整字面色框

既有資料以「由左至右首次出現依次命名 0,1,2,3」取 proper C₅ 外框的十個
代表，仍保留每列全部 `4^5=1024` 個字面 τ。任何 proper B 染色使用三或
四色；其在 S₄ 下的 stabilizer 是平凡群：已用三色逐一固定，至多剩一個
未用色，也只能固定。因此每個字面 β 都有唯一的 `p∈S₄` 將其 canonical
代表 β₀ 送到 β。proper B 字面染色共 `10×24=240` 個。

全圖共同更名給出

\[
J_H(p\beta_0,p\tau)=pJ_H(\beta_0,\tau).
\tag{4}
\]

所以核對十個代表列、各列全部字面 τ，便足以表示所有字面 β 的 support
等式；improper β 的 fibre 自動為空。不得把 U 自己 canonicalize，因為它
與 B 的相對色名恰是附件相容性的一部分。

若另要求 selectors 對全圖共同更名 equivariant，可先在 canonical β₀ 上
選 witness，再以唯一的 p 搬運：`s_H(β,τ)=p s_H(β₀,p⁻¹τ)`。這同樣保留
所有 pins，且唯一性消除了挑選 stabilizer 的歧義。單純對每一字面色框
重新取字典序最小值則不必 equivariant，但仍足以證明 (3)。

## 4. 資料強度與各層嚴格性

令 `R_H={(β,τ):J_H(β,τ)≠∅}`。資訊投影鏈為

\[
\text{全部具名完整 fibres }J_H
\longrightarrow R_H
\longrightarrow R_H^{(3)}
\longrightarrow\Sigma(H+v).
\tag{5}
\]

最後一箭只對本文指定中心 cap 成立。`Σ(H)` 是尚未補中心的外框關係，
不是鏈末的 `Σ(H+v)`；既有 prism／triangulated_01 負控制已顯示
`Σ(H)=Σ(H′)` 不能推出 `Σ(H+v)=Σ(H′+v′)`。

以下格數皆按十個 canonical beta 列計算；完整 240 literal beta 的關係由共同
S₄ 搬運涵蓋，不混用兩種域的計數。三條投影都確實可能失去資訊：

1. **Σ 不決定 R³。** 舊 34 圖中的 prism 與 triangulated_00 補中心後皆
   接受十個 β，但 R³ 分別有 340 與 20 格。例
   `β=01012, τ=10103` 在 prism 支援、在 triangulated_00 不支援。
2. **R³ 不決定全部 R。** 下一節給出兩個新的同槽位合法 annulus；R³
   都有 700 格，但全部 R 分別有 1400 與 700 格。
3. **R 不保留全部 lifts。** 舊 prism_decorated 在原 prism 的 b0u0 邊
   旁加入私人點 x，連 b0 及 u0。原邊已迫兩端異色，故每份原完整 H 染色
   恰有兩種 x 延伸；全部 R 及 R³ 相同，但每個非空 fibre 的基數加倍。
   例如 `β=01012,τ=10103` 的 prism fibre 為一份，裝飾圖為兩份。

不同圖的私人頂點集合可能不同，「完整 fibres 相同」不能無說明地作字面
集合等式。這裡第三項是指保存全部实际 assignments／重建資料的強度；基數
已是其必須保存的資訊之一。雙向存在性 selectors 是 support 等式的見證，
不等於無損保存每份完整 lift。

## 5. R³ 相等但 R 不同的幾何嚴格例

採整數標籤 `B=(0,1,2,3,4)`、`U=(5,6,7,8,9)`、中心 10。H₀ 只有兩圈邊
及兩條 spokes `0–5`、`1–6`。H₁ 再於 annulus 加私人點 `w=11`，連到全部
五個 U 頂點。這個 w 位於 U 空面的外側；待補中心 10 位於空面內側。

H₀ 的有向面表是

```text
outer: [4,3,2,1,0]
inner: [5,6,7,8,9]
annular: [0,1,6,5]
         [1,2,3,4,0,5,9,8,7,6]
```

H₁ 保留 outer、inner 及第一個 annular 面，把最後一面換為

```text
[1,2,3,4,0,5,11,6]
[11,5,9]
[11,9,8]
[11,8,7]
[11,7,6]
```

每条邊的兩個方向各在面表出現一次、每個頂點 link 為一圈、Euler
characteristic 為 2，圖亦連通。故這些表給出定向 sphere 嵌入；去掉指定
outer 及 inner 開面便是同一 B/U 槽位的 annulus。補中心時只用五個
`[10,5+i,5+(i+1 mod 5)]` 三角面替換 inner。程式另外逐點刪除檢查連通，
證實 H₀、H₁ 及兩個 cap 均為 2-connected，沒有藉斷開分量或橋藏住例外。
它們不是 near-triangulations，亦不主張是最小來源。

任何 H₀ 的三色 τ 都可且只能令 `w=m(τ)` 延伸為 H₁ 染色；刪 w 給出逆向。
因此 R³ 完全相同。任何四色 τ 卻無法染 w，故 H₁ 的 R⁴ 為空，而 H₀ 例如
接受 `β=01012,τ=10123`。這直接證明 (5) 中間箭的資訊損失，並未假設
有限枚舉域代表全部 annuli。

[獨立程式](strict_support_check.py) 不 import 舊或本輪 primary checker；
以 Cartesian product 直接列舉完整 H 與 G 染色，以面 darts／頂點 links／
Euler 檢查幾何，再核對中心重建及兩向 selectors。
[完整資料](strict_support.json) 保存兩圖在十個 canonical beta 列的全部 20,480 格，含所有空格：

| 圖 | R³ 格數 | R⁴ 格數 | 完整 H lifts | 完整 G lifts |
| --- | ---: | ---: | ---: | ---: |
| H₀ two_spoke | 700 | 700 | 1400 | 700 |
| H₁ two_spoke_external_apex | 700 | 0 | 700 | 700 |

兩個 Σ(G) 皆為十列全收；700+700 次完整染色傳送逐次保留 B、U、中心色。
此二圖是額外控制，與既有 34 圖的數量和證書分開記錄。

```bash
python3 -B audits/2026-10-13-w5-three-color-support-19209f4c/review/strict_support_check.py --check audits/2026-10-13-w5-three-color-support-19209f4c/review/strict_support.json
```

## 6. 誤投影、混合 witnesses 及未涵蓋範圍

正確的格子鍵是完整 `(β,τ)`。只保存兩邊 marginals、τ 的色數、τ 的獨立
canonical 型，或商圖中分別存在的兩個相等 pair，都不能替代同一格的完整
H witness。既有 triangulated_01 在 β=01012 的兩份單對商 lifts 可以各自
成立而交集為空；它們不是可共同補中心的一份染色。這類負控制需要保存
兩個 witnesses、所謂共同 cell 的空 fibre，以及違反的原邊或共同条件，
而不能只保存「FAIL」文字。

本命題給任意大小的合法 annulus 一個正確充分條件，但不提供相等 support
代表的存在定理，也未構造一般私人點數 `r≤6` 的代表。若另有這樣的同槽位
合法代表，其補中心圖才有 `5+r+1≤12` 個內點，且本命題可用來保留 Σ。
沒有證明其保留最小性、criticality、near-triangulation 身份或全部 lifts。

固定四種自由色、proper 原 C₅、中心恰鄰 U、同一字面色框及合法接回槽位
是適用前提。額外中心鄰點／lists、不同 cap、更多顏色、未宣告外部附件，
都不由 (1) 自動涵蓋。更多顏色可能讓四色 τ 也可接回，中心額外鄰點可能
排掉原來唯一缺色。當保留目標還包含 annulus 外其他接點，必須把它們加入
support 鍵及延伸契約；本結果不能把它們隱藏在私人點中。

有限控制標記為 `triggered and holds`；錯誤投影候選由具體
`counterexample` 否定。最小目錄外 933／941 來源、一般 annulus 小代表、
十三內點以上一般來源及 `K∞=K≤5` 均為 `not triggered` 或既有 OPEN，
本輪無新增 Lean theorem，亦不宣稱主命題完成。
