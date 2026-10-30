# Bernhart 六葉來源：通用標記、唯一 lift 與來源限制

2026-10-30，接續[含標記 bond 的存在性](ck_bernhart_marked_bond_existence.md)。
**原題仍 OPEN：未證目標來源不存在，亦未找到符合全部條件的完整反例。**
本輪將剩餘義務化為無標記六葉計數向量 h 的來源存在性：任何這樣的來源都可插入一個
固定二端構件，完整計數乘 12，得到符合目標且沒有含標記二邊 bond 的來源。
另證 h 的 lift 唯一、補來源小割限制，並精確分離文獻的有限 K₆ 錐。

## 1. 剩餘義務只需研究 h 的無標記來源

令 U 為連通 plane near-cubic 六葉網路，其具名原邊、rotation 及外面六葉正序固定，
容許平行邊，且全部 literal 計數 `n=μh`，μ>0。這裡先不要求標記，也不預設 μ 被 6 整除。
h、k 固定為[原 r₂ 六葉降階](ck_bernhart_endpoint_ray_continuation.md#2-選定-r₂完整支援的全稱限制)，
包含全部零座標。h 有值 1，故 μ 是正整數。
實際 μ 亦必偶：全六葉取色 1 時有 μ 份染色，非空 cubic 內部的 23 系統為偶閉圈族；
依最小具名原邊選一圈交換，給保持該字的無不動點 involution。

本輪證明每個 U 中來源自動滿足完整 `y=μk`，見第 4 節。
令 T 為前輪的標記目標類：完整 `(y,n)=μ(k,h)`、μ∈6ℤ₊，同一外面標記在每份染色的
兩個相關雙色系統均為閉圈。令 P 為「所有 T 中來源都有含標記的實際二邊 bond」。則

\[
\boxed{P\ \Longleftrightarrow\ T=\varnothing\ \Longleftrightarrow\ U=\varnothing.}
\]

更強地，任一 U 中來源可直接構造出 T 中的**反例物件**：增加 40 個 cubic 頂點，
尺度改為 12μ；新標記不在任何實際二邊割內。此為條件構造，仍缺任一實際 U 中來源作起點。
它適用全部輸入大小與正比例，並非已找到完整目標反例。

## 2. 固定二端構件 R：閉圈完全在構件內

從 [MC40 具名輸入](../../../../audits/2026-10-30-bernhart-marked-separation/control-input.json)
取原 cubic 頂點集 `{0,…,39}`，保留所有至少一端在此集合的原邊。
原外端 40、45 作兩個 degree-one 端點，得 40 個 cubic 頂點、兩葉、61 條邊的二端網路 R。
兩條 stems 為原邊 59、64，標記仍為原邊 `f=12=(14,38)`；原邊身份與限制的 rotation 保留。
完整邊表、rotation、逐 dart 面及全部染色見[證書](../../../../audits/2026-10-30-bernhart-universal-marking/verification.json)。

對 R 的完整有限核對有以下精確結果：

- 全部完整染色恰 36 份；兩端必同色，各固定共同色恰 12 份。
- 每份局部染色中，標記的兩個相關分量均在 R 內閉合，共 72 次核對，沒有經過端點。
- 原 rotation 為球面嵌入；同含兩端點的面也含標記，可選為二端插入的外面。
- 標記兩端有三條完全在原 40 點內的邊不交路，原邊序列為

```text
[12]
[11,0,13,14]
[30,4,2,3,51,28,54,56]
```

這些是對一個固定構件的完整有限證書。MC40 本身不符合目標 lift；此處只使用其抽出的
二端構件，沒有把整張 MC40 或局部 36 份染色當作六葉目標反例。

## 3. 任意外面原邊皆可插入，完整倍率為 12

取任一 U 中來源 Q 及任一外面原邊 e=pq。刪 e，將 R 兩個葉端分別接到 p、q，
使兩條 stems 佔原 e 的 dart 位置；在局部 ribbon 中選 R 的鏡向，使其指定外面朝 Q 外面。
原頂點其餘 rotation 與六葉次序保留，新標記 f 就是 R 內上述具名邊。
原 e 可以是 bridge 或 leaf edge；這項插入不要求 e 具有閉圈性。

由二端 flow，任何輸出完整染色的兩條 stems 必同色，反向換回 e 即得到唯一原完整染色。
每份原染色恰有 12 份完整 R extensions，因此對全部 729 個字（含空 fibres）有逐份雙射

\[
F_{Q_R}(u)\cong F_Q(u)\times\{1,\ldots,12\}.
\]

用[完整二端手術契約](ck_bernhart_marked_separation.md#2-條件式二端分離完整-fibressignatures-與倍率)：
含端口色的系統在 R 中有唯一端口到端口路，兩端邊同色，故此段奇長；換成原單邊時長度差偶數。
其餘 boundary 路不變。因此同一份染色的三個 signed signatures 同時保留，包括零 fibres，

\[
(y_{Q_R},n_{Q_R})=12(y_Q,n_Q)=12\mu(k,h).
\]

R 內標記的兩個分量已在局部閉合，外部接線不能改變它們；故輸出全部染色均滿足雙閉圈。
上述三條路仍在 R 內，任何含標記的實際割必跨三路，大小至少三。
新尺度 12μ 自動在 6ℤ₊，所以 Q_R 確為 T 中沒有含標記二邊 bond 的物件。

U 非空因而蘊含 T 非空並且 P 為假；反向 T⊆U。配合前輪 `P⇔T=∅` 即得第 1 節等價。
此處每個輸出物件的全部原邊、rotation、葉序與標記一次固定，沒有逐染色另選標記。

## 4. h 已唯一決定完整 lift，並且是投影錐極射線

對完整六葉 incidence 系統，191 個 signed signatures 各有 compatible literal word。
逐一核對 h 的全部零字：其中 168 欄各有一個 compatible 零字見證，非負性迫其 y=0。
剩餘欄恰為 k 的 23 個正欄，沒有其他 eligible signature。

在這 23 欄上，同字三個 split 的計數相等給出整數齊次矩陣。
其 rank=22，kernel 恰為全 1 向量的張成；證書有 22×22 minor determinant −1。
故任何非負 lift 且 `supp(n)⊆supp(h)`，皆有

\[
y=t k,\qquad n=t h,\qquad t\ge0.
\]

所以對任何實際 `n=μh` 來源，完整 y 必為 μk，未遺漏零座標。
這也證 h 是 **n 投影錐 B₆ 的極射線**：若 h=n₁+n₂ 且各 nᵢ 有非負 incidence lift，
零字先將兩份支援限制在 supp(h)，再由上述一維性得各 nᵢ 與 h 成比例。
此處 B₆ 指全部標準 incidence 非負 lift 的 n 投影，不等同全部實際平面來源的集合。

全部 168 個見證、矩陣、minor 及精確 kernel 重播見
[來源化約證書](../../../../audits/2026-10-30-bernhart-universal-marking/six-source-reductions.json)。
這項結論補強前輪僅對指定 23 欄證 rank 23 的固定 n 唯一性，沒有把 cone 可行性當成圖實現。

### 不含標記假設的來源小割限制

以下皆對 U 中來源成立，不要求某條邊全染色閉圈。

**bridge 只能分開 1／5 葉。** 對 bridge 的一側求 flow，其葉字 XOR 必等於該 bridge 的
非零顏色。逐一核對 64 個葉子集，只有六個 singleton 及其六個補集在全部正 h 字上 XOR
始終非零。因此 bridge 的兩側必分別有一葉、五葉，無葉 bridge 亦不可能。

**二邊割不能分開 3／3 葉。** 固定任一三葉集合 A，將 h 按 A／Aᶜ 展開，限制兩側字
XOR 都為零，得 6×6 矩陣。若有實際二邊割，兩 cut 色須相同，只有三個有序端口狀態；
對同一切開來源的完整 fibres 求和，該矩陣為三個非負外積之和，rank 至多三。
但全部 20 個 A 的矩陣各有具名非零 4×4 minor，故皆 rank 至少四，矛盾。
這是完整來源的 cut factorization，不使用不同染色的邊際拼接。

**有 2／4 葉 bond 的來源可嚴格降階為另一個 U 中來源。**
切出包含兩個原葉的連通側 R₄，補側連通且有四個外面葉。
補側必位於 R₄ 的無界面，否則其原葉不可能在原圖外面；故 R₄ 的兩葉及兩 cut ports
同面，可沿同一 rotation 當成 plane 四端網路。

依四端環序，記四個 canonical counts 為 `(a,b,c,d)=(1111,1122,1212,1221)`。
其兩個非交叉全端配對的全 −1／全 +1 signature 權重記為 α、β、γ、δ，皆非負。
完整 incidence 方程直接給

\[
(a,b,c,d)=(\alpha+\beta,\ \alpha+\delta,\ \gamma+\delta,\ \beta+\gamma).
\]

所以 R₄ 的全部 n 是四張真 plane 小網路的非負組合：兩種不交叉的兩條 wires，
以及兩種只有兩個 cubic 頂點的 H 網路。把這四個代表分別接回**同一補側**，
得到四個計數向量 xᵢ，且 `n_Q=Σ tᵢxᵢ`；無 proper 染色的拼接項計為零，
其餘每個非零項皆由真 plane 六葉來源給出。
由 h 的投影極射線性，每個係數正、向量非零的 xᵢ 必正比 h。

若代表把兩個原葉直接互配，會迫該兩葉始終同色，但每個葉 pair 都有異色的正 h 字，矛盾；
非相對 pair 可用 `123123`，三個相對 pair 可用 `112323`。
若把兩個原葉接到同一 cubic 頂點，會迫兩葉始終異色，與 `111111` 矛盾。
其餘 H 代表中，每個原葉與一個 cut port 接在同一 cubic 頂點。
固定其餘四葉字，令 C₁、C₂、C₃ 為補側兩 cut ports 同色 1、2、3 的完整 fibre 大小，
則兩個原葉同色的三份計數必為

\[
(N_1,N_2,N_3)=(C_2+C_3,\ C_1+C_3,\ C_1+C_2).
\]

故它們須滿足三角不等式。但 h 的每個葉 pair 都有具名其餘四字，使這三值為
`(1,0,0)` 的某個置換；全部 15 個 pair 的見證均保存。因此 H 代表也不能正比 h。
若兩個原葉在四端局部環序中相對，兩種 H 都屬此類，論證相同。

尚可能非零的代表僅將每個原葉分別直接 wire 到一個 cut port。
原非零總計數保證至少有一個這樣的非零分量；選它並刪掉 R₄ 的全部 cubic 頂點，
得到連通 plane 六葉來源、同一葉序及 `n=νh`。由 h 有值 1，ν 為正整數；
由本節唯一性，其完整 y 也為 νk。因此這是嚴格較小的 U 中來源。

所以，**若 U 非空，cubic 頂點最少的來源沒有 2／4 葉 bond**。
這是最小來源化約，沒有排除任意大小的全部來源，亦沒有聲稱原標記在化約中保留。
此化約保存正比例來源的存在性；其契約是完整計數的非負分解，再選一個非零真來源成分。
它沒有提供原 Q 與單一所選替換圖的完整 fibres 雙射、固定倍率或原染色的回寫映射。
本段的 bridge 見證、20 個 rank minor、四端代表全部染色及 15 個 pair 的三角反證
皆在同一[來源化約證書](../../../../audits/2026-10-30-bernhart-universal-marking/six-source-reductions.json)中。

### 最小無標記來源的 cubic core 正規形

若 U 非空，選 cubic 頂點數最少的來源 Q，記為 v。下述兩種額外手術都有完整 fibres 契約。

對內部 bridge，取含一葉的一側，連同該原葉與 cut stem 當二端網路。
兩端同色、固定端色延伸數為共同正整數 t；以一條 leaf edge 替換，全部六葉 fibres 與三 split
signatures 除以 t。若該側含 cubic 頂點便嚴降，故 Q 的 bridges 只能是原 leaf edges。
對無葉二邊 bond，同樣由既有二端契約以單邊替換而嚴降，故最小 Q 也沒有這種 bond。

對有一葉側的二邊 bond，該側連同原葉及兩 cut stems 是三端網路。
三個端色的 XOR 為零，故恰為三個不同色；全域 S₃ 置換使六種有序不同色 tuple 的完整
extension fibres 等勢，記共同正整數為 t。以單一 cubic 頂點及三條 stems 替換，
每份縮圖完整染色恰有 t 份原 extension。每個雙色系統只有兩個不同色端點，端口路為偶長；
單一 cubic 的兩邊路也為偶長，故三 split signatures 同時保留。
若此側超過一個 cubic 頂點便嚴降。因此 Q 的每個二邊 bond 只可能隔出
**一個原葉及其單一 cubic 鄰點**；其餘葉分割已由上段的 2／4 化約、3／3 rank 排除覆蓋。

所有上述替換的縮圖比例仍為正整數：它有真實完整 counts，且 h 有值 1。
不要求縮圖比例維持在 6ℤ₊，因本節使用無標記類 U，之後可再作通用標記插入。

全單色正字保證六葉接到六個不同 cubic 鄰點。兩個鄰點之間不能有雙平行邊，
否則這兩點與兩葉已是獨立分量，違反六葉連通性。這些鄰點也不能彼此相鄰：若兩者相鄰，
它們與兩葉形成兩邊 cut；其餘兩條 cut 邊皆非 bridge，故補側必連通，得到已排的 2／4 bond。
刪去六葉並 suppress 這六個 degree-two 鄰點，得到連通 plane cubic 圖 H，有 v−6 點。
H 中任一 bridge 或二邊 bond，可沿各 subdivision path 選一條跨側原邊，提升成 Q 的內部
bridge 或二邊 bond；兩側都含未被 suppress 的 cubic 頂點，違反 Q 的上述限制。
故 H 為 3-edge-connected。H 的 loop 會使該點唯一外接邊成 bridge；兩條平行邊會形成
二邊 cut，除非整圖只有兩點三平行邊。該例的面邊數不足以下述六個插入位置，故 H 為簡單圖。

因此最小 Q 必可由一張**簡單、3-edge-connected 的 plane cubic 圖 H**，
在同一面上的六條不同邊各 subdivide 一次，再各接一葉取得，且沿該面保留原六葉次序。
這是存在性正規形，尚未證這個無界圖類不能實現 h。

## 5. r₂ 與 free-edge 分支的正向化約

若六葉來源允許不連通，先逐分量求 Klein-four flow。前輪已核對 h 的全部 62 個 proper
非空葉子集：每個子集都有正 h 字使該子集 XOR 非零。因此六葉必全在同一連通分量。
其他分量為閉 cubic 圖；原圖有染色，故它們各自的完整染色數為正整數，僅提供計數倍率。
刪去它們後，六葉連通分量仍是正比例 `(k,h)`；正 k 座標值 1 迫新比例為正整數。
所以不連通的無標記來源也能先取此分量，再作第 3 節插入。

對[原 r₂ 全部來源的正向封口](ck_bernhart_endpoint_ray_continuation.md#2-選定-r₂完整支援的全稱限制)：
非 free 分支直接給 T 中物件；free-edge 分支給無標記六葉 `(k,h)` 來源，現在也可經 R 插入轉入 T。
因此 **T 若證空，兩個分支的 r₂ 來源都會被排除**；前輪留下的 free 分支缺口已取得此正向化約。

若八葉來源類允許獨立 free edge，反向從 U 中來源加這一分量，便按原完整公式得到真正的 μr₂，
而不是只得到等色 sector。於此允許不連通的來源類，三項非空性等價：

\[
U\ne\varnothing\quad\Longleftrightarrow\quad T\ne\varnothing
\quad\Longleftrightarrow\quad r_2\text{ 有實際完整來源}.
\]

若另限八葉來源連通，上式最後一個反向構造不適用；仍有 r₂ 來源到 T 的正向化約。
本輪沒有裁決任一非空性，也未以切 f 的等色 sector 推論完整八葉 lift。

## 6. 與文獻 K₆ 的精確分離及外部下界

作者論文的 Lemma 12 指定一個有 102 條生成射線的 K₆。
本輪從[作者原始資料](https://lidicky.name/pub/4cone/proof.tar.bz2)只取前 2 MiB 壓縮 bytes，
重新解出 `proof-corr.txt` 第 52–153 行的全部 K₆ ray 宣告，保存原始前綴、SHA256 與解析結果。
沒有下載或重播完整大型 closure 證書。

把 h 化為 31 個 S₃ canonical parity-word 座標，令 L 為其中 17 個零座標之和。
對全部作者射線逐項精確核對有

\[
L(h)=0,\qquad L(r_i)\ge1\quad(1\le i\le102).
\]

故每個正比例 h 都在此 K₆ 之外。完整 17 座標、102 個值及具名零字見證見
[分離證書](../../../../audits/2026-10-30-bernhart-universal-marking/k6-separation.json)。
這只排除由該 102 rays 非負生成的向量，**K₆ 的全部平面來源涵蓋性尚未建立**，故不構成來源排除。

若沿用論文 computer-assisted Lemma 12 及 Lemmas 13–19，任何 U 中來源至少有
**28 個 cubic 內點**：將六葉封到單一 degree-six 外部頂點，原 capped 圖有 v+1 點；
Lemma 13 給 K₇ 外、至多 v 點的七端圖，再取 extremal minor，由 Lemma 19 至少 28 點，故 v≥28。
這是外部定理依賴的下界，完整 closure 證書未由本輪獨立重播。
依據：[Dvořák–Lidický, Coloring count cones of planar graphs](https://arxiv.org/pdf/1907.04066)。

## 7. 證據、重播與停止點

通用插入及非空性化約為一般紙面論證，構件的 36 份完整局部染色與三條路由 Python
精確有限證書核對；唯一 lift／極射線為非負性與整數矩陣紙證，數值證書可重播。
K₆ 分離為作者原始數值資料的精確有限核對；28 點下界另依賴上述外部 computer-assisted 引理。
未新增 Lean，沒有使用四色定理作 oracle。

```bash
python3 tools/audit_archive.py restore --artifacts
python3 scripts/ck_bernhart_universal_marking.py --check audits/2026-10-30-bernhart-universal-marking/verification.json
python3 scripts/ck_bernhart_six_source_reductions.py --check audits/2026-10-30-bernhart-universal-marking/six-source-reductions.json
python3 scripts/ck_bernhart_k6_separation.py --check audits/2026-10-30-bernhart-universal-marking/k6-separation.json
```

插入的非目標控制以 C₆ 六葉來源為 core：原 66 份染色中，被替邊沒有一份同時雙閉圈；
插入後 792 份染色全部滿足新標記雙閉圈，66 個完整 fibres 各 12 份；
729 字、191 signatures（包括零）及逐份三 split tuple 全保留。控制仍非目標，正字數為 63，
目標為 81；具名目標正字 `112323` 在控制為空。沒有將此控制充當反例。

[收據](../../../../audits/2026-10-30-bernhart-universal-marking/RECEIPT.json)記錄重播、雜湊、封存及文件檢查。
大型證書及原始資料前綴按[既有規則](../../../../audits/README.md#新-checkout-的還原)保存原 bytes。
三個數學 checker、文件連結／索引檢查、正式 docs DocGraph 及 `git diff --check` 通過。
全工作樹 DocGraph 仍因歷史快照有 72 項 duplicate-id 失敗，未將正式 docs 通過當成全樹通過。
原題、實際來源非空性與 r₂ 排除仍 **OPEN**；原 76 列新增必零座標 **0**。
尚缺對所有任意大小的 U 來源一般非實現證明，或一份實際 U 來源及其完整證書。
28 點下界、K₆ 分離與最小來源子類化約都不代替此項驗收。

文件閉包：更新前輪兩份標記來源、r₂ 封口來源的直接後續、任務二父報告、4CT 導覽及 STATUS。
研究線標記不變，停止於直接 consumers；未 commit／push。
