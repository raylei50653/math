# 933／941 稀疏 singleton 支援：文獻與定理適用性

2026-10-13。入口：[adjacent-singleton 計數](../../docs/c5_adjacent_singleton_counts.md)。
本次核對原始論文、正式出版版本及目前來源契約；不作新的圖枚舉。

**結論：本次查核未找到可在目前任意大小的來源契約下直接排除 933／941 的已證定理。**
可直接使用的是有大小限制的 count-cone 定理，以及另需全內點偶度的條件式排除。
Dvořák–Lidický 的純特殊射線排除不涵蓋混合面；Conjectures 8／9 不列為排除工具。
較新的 Kempe-family 引理同樣與兩個候選相容。這是有界檢索結果，不是「不存在其他定理」的證明。

## 1. 本題的精確來源契約

固定**同一張有限簡單 disk 圖、同一有序 C5 邊界及同一四色框**。
計數是每個固定 boundary assignment 的全部完整延伸數，內部允許使用第四色。
令 `x_uv` 為 repeated-pair `{u,v}` 的計數，`y_i` 為 singleton-i 的計數。

| 完整關係 | 接受的三色邊界列 | singleton 支援 P | 接受的四色邊界列 |
|---|---|---|---|
| 933 | `01012` | `{4}` | 全部 T4 |
| 941 | `01012,01201` | `{4,2}` | 全部 T4 |

`T4={01023,01203,01213,01231,01232}`。數字 mask 只是這份完整十列關係的編碼。
整圖 D5 搬運必須一起搬運 labels、色框、附件、支援與全部 fibres，不能分別正規化不同列。
定義及定位：[凍結 screen §4.3](frozen/docs/c5_kempe_screen.md)、
[凍結計數 §1–2](frozen/docs/c5_adjacent_singleton_counts.md)。

已證計數恆等式給

\[
x_{uv}=m+\sum_{i\notin\{u,v\}}y_i,
\qquad
\sum_{uv}x_{uv}=5m+3\sum_i y_i.
\]

取 `e={2,4}`，兩類都滿足 `P⊆e` 且 `x_24>0`，所以 `m=x_24>0`。
**真正較弱的待證目標**是只排除 `P⊆e 且 x_e>0` 的圖來源，無須先對所有圖證 `m≤0`。
這個特殊目標仍未證；例如抽象向量 `y_i=1,x_e=4` 的支援含相鄰點，卻有 `m=1`，
說明兩種陳述不是純代數等價。這個向量不是實現圖。

來源轉換分三層，不能混用其前提：

| 來源層 | 現有證據 | 不自動保留的條件 |
|---|---|---|
| 一般 disk 反例 → 近三角化圖 | 保留一個 `x_e` 完整染色；`P` 不增；恆等式重新推出全部 T4 | 可能新增 hubs／平行邊；不保內點數，也不必保完整 Σ 恰為原 mask |
| 所有目錄外來源中全域最少內點，再最多邊 | 簡單、二連通、chordless-C5、內面皆三角形，且不增加內點；內度≥5、框度≥4 | 不是每張原圖的逐步同 Σ 補完演算法；不具舊 edge-critical 前提 |
| 完整 Σ 的 edge-minimal／ε=2 分支 | 具名原邊、接點、支援、owner、root 與 full lifts 的局部論證 | 不等同全域最少內點／最多邊，更不等同 D–L 的 degree-7 minor-extremal |

原論證：[count-cone §2–3](frozen/docs/c5_count_cone_bridge.md)、
[共面正規形 §2](frozen/docs/c5_cofacial_normal_form.md)、
[度數界 §1、3–4](frozen/docs/c5_saturation_degree_bound.md)、
[edge-minimal 契約](frozen/docs/c5_independent_support_capacity.md)。

## 2. 已知定理 → 所需前提 → 現有證據 → 尚缺義務

頁數以下均指**原文印刷頁**；PDF `#page=` 則從第一個 PDF 頁算起。
D–L 指 *Coloring count cones of planar graphs*，arXiv v2／JGT 100 (2022), 84–100。

| 已知定理與原文定位 | 所需前提 | 現有證據／實際排除力 | 尚缺義務 |
|---|---|---|---|
| D–L Observation 3，[v2 p.3](https://arxiv.org/pdf/1907.04066v2#page=3)，JGT p.86 | plane near-cubic、指定 cyclic ports，dual 外面為 cycle | 近三角化橋已給；固定 assignment 計數相等 | 一般圖須先完成上述橋；固定計數不乘 4／24 |
| D–L Theorem 5＋Lemma 6，[v2 pp.5–6](https://arxiv.org/pdf/1907.04066v2#page=5)，JGT pp.88,90 | plane near-cubic；指定點度五、其餘點度三 | B5 有十二射線；本題混合面仍在 B5 | 必須補上真正平面來源的額外限制；cone membership 本身不排除 |
| D–L Lemma 7＋4CT，[v2 pp.6–8](https://arxiv.org/pdf/1907.04066v2#page=6)，JGT pp.90–91 | **整個非零向量**位於純特殊 ray | 排 `P=∅`；兩類都有正 fan 係數 | 缺將混合向量合法化為純 ray 的同圖機制 |
| D–L Corollary 20，[v2 p.16](https://arxiv.org/pdf/1907.04066v2#page=16)，JGT p.98 | plane near-cubic，**頂點數 <30** | dual 有 `2k+4` 點，故近三角化 `k≤12` 全排；全域最小來源橋接到一般 disk 的同界 | 任意大小缺大小上界；不得把 <30 改成 ≤30 |
| D–L Lemmas 12–19 及 Cor20 後的 38-minor 條件，[v2 pp.11–17](https://arxiv.org/pdf/1907.04066v2#page=11)，JGT pp.94–99 | 指定 Kd cones／gluing；degree-7 minor-extremal 歸約 | 可提供条件性分解或禁 minor 路線 | 須給完整來源分解／排盡指定 minors；原 C5 的 max-edge minimality 不等於該 extremal 前提 |
| Inoue 等 Lemma 13.2，[最新 v3 pp.51–52](https://arxiv.org/pdf/2603.24880v3#page=52) | 同一完整四色染色的 near-triangulation，outer C5 恰用三色 | 兩類有起始染色；至多六次 Kempe changes 的三種 family 中只剩 fan family，仍相容 | 缺 fan 之外的必要轉移／跨 fibres 相容性；不是 component confinement 定理 |
| Dvořák–Moore–Seifrtová–Šámal Observation 5、Theorem 7、Corollary 8，[正式版 pp.4–6](https://research-explorer.ista.ac.at/download/19879/19887#page=4) | 三角面 patch，**同圖完整三色 hue**；等價要求全內點偶度 | viable 必要條件可排除 T4 全收，見 §4 的直接推論 | 本题沒有全內點偶度；邊界三色延伸不提供完整三色 hue |
| Mohar Theorem 4.4，[p.295](https://users.fmf.uni-lj.si/mohar/Reprints/2006/BM06_GTP06_Bondy_KempeEquivalence.pdf#page=9)；Feghali Theorem 1，[v3 p.2](https://arxiv.org/pdf/2101.04065v3#page=2) | 分別是整圖三色可染；或 chromatic **4-critical** planar graph | 各受限類別的全部四色染色 Kempe equivalent | 尚未證本來源在該類；Σ-critical 不等於 chromatic critical。即使單一 class，也仍需 boundary 逃逸論證 |
| Dvořák–Lidický–Mohar，Theorem 10＋§2 Table 1，[v2 §1–2](https://arxiv.org/html/2504.08327v2#S2) | 簡單 one-crossing 類；相應 C4 candidate 無非面三角形、內度≥5，有限驗證≤28點 | 是四邊界 rainbow-forbidding 問題的等價／有界證據 | 缺保完整拒絕条件、度數與頂點界的 C5→C4／one-crossing 轉換；不能直接套入 |
| DeVos–Seymour 定理（Dvořák–Swart 所引 Theorem 1）及 Dvořák–Swart Theorem 3，[v1 §1](https://arxiv.org/html/2504.07764v1#S1) | 全圖三色的 realizability；或 rooted-minor-free realization 類 | 說明 extension relations／rooted minors 的界線 | 與「邊界三色、內部四色」及 planar disk realization 都不相同，不能用來排除或構造本題來源 |

Inoue 的原引用是 v1 p.53；本輪核對到 2026-10-01 提交的 v3，Lemma 13.2 的陳述相同。
§13.1 只有 C4 的 Lemma 13.1 及 C5 的 Lemma 13.2，沒有「框度≠3」的補強排除。
完整三角化圖中的 D-reducibility 允許改變 ring precoloring，還需另證保留本題完整 Σ 的契約。
各 paper 結果與以上本地適用性推論分開：表格不是宣稱作者原文討論了 masks 933／941。

## 3. Dvořák–Lidický 的定理／猜想界線

原文 §1.1 允許 loops／parallel edges；要求 connected plane graph、指定半邊順序 ν，
指定點度五、其餘點全度三。這使本題的平行邊補完可走 dual 橋，但不省略嵌入／外 cycle 義務。

| 原文項目 | 正確身份 | 本題翻譯／使用界線 |
|---|---|---|
| Lemma 7 | 已證的等價，搭配 4CT 可用 | 排除非零純 `ct`；不能排除混合向量中的正 t 係數 |
| Conjecture 8，[v2 p.8](https://arxiv.org/pdf/1907.04066v2#page=8)，JGT p.91 | **普遍猜想** | 真正 plane counts 屬於刪去特殊 ray 後的 B′5 |
| Conjecture 9，[v2 p.9](https://arxiv.org/pdf/1907.04066v2#page=9)，JGT p.92 | **與 Conj8 等價的普遍猜想** | `3Σy≥Σx`，等價 `m≤0`；本輪禁止作排除工具 |
| Corollary 20 | 上述猜想的**有界已證版本** | 僅在 dual 頂點數 <30 使用；外部計算證書未由本 repo 重播 |

正式 [JGT PDF](https://onlinelibrary.wiley.com/doi/pdf/10.1002/jgt.22767) 與 arXiv v2 的身份一致。
§4 開頭的非正式大小敘述不能取代 Cor20 的嚴格界。
本次以原題名、Conjecture 8／9、pentagon precoloring、Kempe equivalence 及作者／arXiv
來源搜尋，未查得一篇主張解決普遍 Conj8／9 的後續原始論文；不宣稱完整查清所有文獻。
另須注意：本篇編號 10 是 **Observation 10**，不是 Theorem 10；one-crossing 論文的
Theorem 10 又是等價定理。不能把編號相同或「Theorem」字樣當成無條件排除。

混合面已有精確本地證據。令 t 的五個 x 全為 1、五個 y 全為 0，Fi 為 singleton-i fan 計數。
引用十二 ray 完備性後，[B5-face §3–5](frozen/docs/c5_b5_face.md) 得

\[
N_{933}=ct+aF_4\quad(c,a>0),\qquad
N_{941}=ct+aF_2+bF_4\quad(c,a,b>0),\qquad c=m=x_{24}.
\]

三係數由同一來源的固定計數唯一讀出。這些向量實際滿足已證 B5 必要條件；
`t+F4`、`t+F2+F4` 是完整整數反控制，**不是**實現圖。
wheel 黏合的邊染色數分別為 `6a`／`6(a+b)`；fan filter 量到 `6c`，都為正。
更一般，含正 t 及正 fan 的向量對任意非零 `q∈B5` 的普通同五-port pairing 皆正。
所以單次普通 closure 無法產生 Lemma7 的零染色矛盾；不排除其他圖變換。
不能將「不同 splits 各有非負分解」當成同圖 connectivity 證據。

## 4. 一項真正可用、但前提未滿足的條件式排除

由 near-Eulerian 文獻的 **已證** Theorem 7／Corollary 8，直接得到：
**outer C5 的三角面 patch 若全部內點偶度，就不可能全收 T4。**
這是本次由原定理推出的受限類別 corollary，不是一般稀疏支援定理。

Observation 5 提供整圖 proper 三色 hue。共同旋轉及色名排列後，其邊界可寫成
`ψ=(0,1,0,1,2)`。若全收 T4，則 `φ=(0,1,2,3,1)` 必有完整延伸。
四色依序標為 `(0,0),(1,0),(0,1),(1,1)`。依原文 δ 定義，五條定向框邊給

\[
(1,0),(1,1),(1,0),(0,1),(1,0),\qquad \delta(C5)=(4,2)\ne(0,0).
\]

但原文 Theorem7 的證明使同圖每個 closed walk 的 δ 總和為零，矛盾。
本題全域最小來源目前反而有至少九個五度內點，故不屬全內點偶度的類別；
一般補完也未保證偶度。不能把 `y_i>0` 轉成整圖三色 hue。
該文 Theorem2 的線性時間判定演算法也沒有承諾任意 precoloring 都可延伸。

## 5. 仍缺的精確義務與證據範圍

最直接的未解義務是：對真正 plane 來源在上述稀疏面證明 `c=0`，
或在 `P⊆e,x_e>0` 的同圖契約下，證明必可達到某個 `y_i>0,i∉e`。
若沿文獻 restricted class，須先證保反例的大小／偶度／minor／C4 轉換前提。
所有轉換都須明列原 labels、rotation、實際附件及共同色框中的原／新完整 relations、空 fibres 與 full lifts，
逐項證明所需反例條件保留；只有另有證明的轉換才宣稱完整 Σ 相等。
目前既有 [classwise 計數 §3](frozen/docs/c5_kempe_class_counts.md) 已能把正 c 定位到同一 Kempe class，仍未供給必要的逃逸定理；
不能以「整個 extension space 是單一 class」代替這項義務。

**本地當前狀態與文獻界分列。** 凍結時工作區的
[K15-SPHERE](frozen/docs/c5_k15_sphere.md) 已記 `K≤15=K≤5`、一般來源 `k≥16`；
[C8 內圈](frozen/docs/c5_c8_inner_collar.md) 記 `h=3⇒k≥18`。
這是當前未提交工作區的本地紙面／有限證據，本輪未重播其證书，不歸於 Cor20，
不據此關閉任意大小的 933／941。數值定位以凍結檔為準。

本輪 normal 與 `PYTHONHASHSEED=17` 各重播三項既有唯讀 `--check`：

```bash
python3 scripts/c5_adjacent_singleton_counts.py --check
python3 scripts/c5_count_cone_bridge.py --check
python3 scripts/c5_b5_face.py --check
```

結果均通過：132 witnesses、42 partitions、11 抽象向量及 142-state push 閉包；
count-cone 翻譯、十二轉錄 rays、完整 faces／pairing 一致。結果保存在 [replays.json](checks/replays.json)。
另將 PDF source hash 破壞後注入唯讀 replay，checker 如預期拒絕；舊證書未寫入。
凍結 hashes 全吻合、live 輸入漂移為零、報告直接本地連結全通過；見 [最終核對](checks/final-review.json)。
這些 checks 不重證外部 ray completeness、平面來源實現性、Cor20 的計算證書或一般猜想。
本輪沒有實際完整 Σ=933／941 的來源正控制（`not triggered`）；抽象向量不建立來源實現性。
沒有新增 Lean 定理或改 Python 實作，因此未跑 Lean build；沒有廣域 graph catalogue 搜尋。

`manifest.json` 保存 HEAD `6cafdfb02fe5892a49eee21f92aea2369a25c022`、原始 dirty status、
凍結輸入及原始 PDF 的 SHA-256。主 D–L v2 PDF hash 與舊證書一致。
本輪只寫本獨立目錄；未改共享文件、舊證書或既有並行成果，未 commit／push。
L1 已核對 guide 的 count-cone 列與 STATUS 對應索引；兩者的 OPEN 判定不變。
本報告作獨立稽核交付，由本次回覆直接提供入口；共享路由未更新。
