# D₆ 項 2：第二次獨立反駁審查

本補查試圖反駁主線的 unary 長盾弧論證。結論：**確認**，未找到偷用
固定完整 Σ、T4、恰缺兩列或 source 全框碰齊的步驟。

## 接點邊與 lists

取原 unary D 與其唯一 root r 的原邊 rp。M−rp 接受同一字面 q；
其一份完整延拓限制到 M−D 得合法 ψ。若 ψ 能延拓 D，就得到 M 的
q 延拓，與原拒絕相矛盾。故 D 確有拒絕見證；不需要 Σ 933/941 的
跨列私有色結論。

D 每點完整 degree 四是原 C 前提，而 D 為 H−{z,w} 的原分量且 unary，
故所有外鄰僅是框點及 r。令 L(v)=U∖ψ(N(v)∖D)，則
|L(v)|≥4−|N(v)∖D|=deg_D(v)。若任一點有 slack，按以它為根的
生成樹逆序貪婪可著色：每個非根點尚有一個未染父點，根點自身多一個
可用色。因此拒絕迫處處 tight，即每點外鄰顏色全異。

## 真實外路及 hubs

假設 S_D⊆{a,b}，ab 為原框邊。|S₀|=3，故選 h∈S₀∖{a,b}。
兩 roots 均有原 x₂ 接點，所以 L=r–x₂–x₁–x₀–b_h 是原簡單路徑，
內點屬 C*、避開 D，且只有終點碰框。不同原 pieces 沒有直接接線，
故 L 的內點不會成為 D 的其他外鄰。

寫 c=ψ(r)。若 c 不等 q(a),q(b)，取 {a}、{b}、
(B∖{a,b})∪V(L)。若 c=q(a)，取 {b}、(B∖{b})∪V(L)；
c=q(b) 對稱。各集合互斥、連通，原框邊給两兩鄰接；全部 D 外鄰
被覆蓋，每個集合與 D 外鄰的交集只見指定一色，各指定色不同。
所謂「hub 同色」只要求其 D 外鄰同色，並不聲稱整條 L 或整個框路徑
在原 ψ 中同色。這正是定理 B 的條件。

空支援、單點支援仍包含於任一適當框邊，外路選擇不變；未碰 D 的
hub 的單色條件為空條件。Tightness 排除同一點同接合併後同色的
r,a（或 r,b），所以收縮後 D 每點完整 degree 仍四、lists 不變。

## K₄ 排除與二／三 hub 推理

原 K₄ 引理文件 `docs/c5_degree5_tree_components.md:32–36` 字面先寫
較窄的 q-minimal／單 root 設定；不可原樣把它當更廣定理引用。
但四 tether 論證可自行以拒絕 degree lists 補足，並不需那些窄前提：
若 D 有 K₄ block，每個 clique 點的第四條邊不是外 hub 附件，就是
向 block 外的 bridge。切該 bridge 後兩側各在端點有 slack，因此各
可著色。若兩端可取不同色便能接回，所以拒絕迫兩側端點可取色集合
均為同一 singleton。外側若不碰任何外 hub，則全四色置換保持其
完整著色，端點可取色不可能是 singleton。因此每個 clique 點有
到外 hub 的 tether，四條非 clique 部分互斥；外 hubs 的聯集連通，
合為第五袋得 K₅ minor。這個重推排除 K₄ block；更大的 clique block
本身已含 K₅，亦被平面性排除。因此剩餘 Gallai blocks 只有 bridges
與 odd cycles（含 triangles）。

外部定理確實需要完整的 blockwise-uniform 結論，而非只知道 D 是
Gallai tree。此次重新打開 [Dvořák 的原講義](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)：
Lemma 7 位於 PDF 第 5 頁，Theorem 10 及其 blockwise-uniform 定義位於
PDF 第 6 頁。定理適用於任意連通圖及 degree assignment，沒有上述
Σ、T4 或缺列條件。

兩 hubs 時 min deg_D≥2，K₄-free Gallai tree 的末端 block 不可為
bridge，故為 odd cycle。取相鄰 private u,w；它們都碰兩 hubs。
D−{u,w} 連通、非空，且仍含原內部 degree 二的點（單 block 的
剩餘點，或另一末端 block 的 private 點），故也碰兩 hubs。得到
兩 hub singleton、u、w、其餘 D 的五袋 K₅。

三 hubs 時：末端 odd cycle 的 private lists 同為一個二元 palette，
因此各碰同一對 hubs。取相鄰 private u,w，D−{u,w} 連通非空；
第三 hub 若碰 D，只能碰這個剩餘部分，把兩者合成第五袋即得 K₅；
若它完全不碰 D，刪除後回到兩 hub 情形。

末端 bridge uv、u private 時，u 接全三 hubs，list 為第四色 δ。
D−u 在 v 有 slack，故可著色；拒絕迫其 v domain 恰 {δ}。
若 D−u 不碰某色為 A 的 hub，交換 δ,A 保持全部 lists，卻使 v=A，
矛盾。故剩餘 D 碰全三 hubs，三 hubs、u、剩餘 D 即是五袋 K₅。

實際活躍 hub 若只剩一個（例如空框支援），min deg_D≥3。
K₄-free Gallai tree 的末端 block 私有點內部 degree 至多二，立即矛盾。
因此「刪掉未碰 D 的 hubs」也不留下空支援缺口。

證據層：此補查是**紙面推導＋已核對的外部 degree-list 定理**；
沒有新增有限枚舉或 Lean 結果。原來源三份補讀文件另以
`hub_sha256_before.json`、`hub_sha256_after.json` 核對無漂移。
