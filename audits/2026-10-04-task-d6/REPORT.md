# D₆：獨立稽核 W／共鄰 P₃ 的 3,497 葉來源排除

2026-10-04；工作根目錄 `/home/ray/developer/ai/math`，分支
`shield-budget-hub-principle`，HEAD `ca3870f9b79684c2100480d0dc04523899666928`。
以未提交工作區為準。全程只在本 D₆ 目錄新增檔案；不 commit、push、ledger
`--write`，不修改原報告、checker、artifact、導覽、STATUS 或 README。

**總判定：有缺口，尚不能對現行交付給出完整驗收通過。**
在 C §1 的原前提下，C-W 的任意大小來源排除經自行重推成立；3,497 個
開放 key 全部適用，且補上本文的零-unary 側排除後，可排除 C §1 的整個
共鄰端點 P₃ 來源分支。然而現存 verdict 綁定更正前的盾弧文件，現行 W
`--check` 實際 exit 1；這是交付 provenance 缺口，不能當作通過。
另外，題述不帶 criticality／degree 等前提的「任何平面 disk」強化命題是錯的，
有獨立 disk 反例；它不是 C-W 原定理的反例。

## 1. 固定輸入、證據界線與重播入口

開始前先保存 [SHA-256 清單](sha256_before.json)及 [輸入快照](snapshot/)。
後續讀取的依賴亦先封存；子任務的額外依賴各有自己的 before／after 清單。
實體快照保存在 `.snapshot/`，`snapshot/` 為同目錄 symlink；不把封存副本
再次登錄為 live DocGraph 文件。
最後的 [穩定性核對](sha256_after.json)將原檔期間漂移與 artifact 已有舊 hash
分開記錄。起始 Git 狀態見 [workspace_before.txt](workspace_before.txt)。

| 被稽核物 | 開始時 SHA-256 |
| --- | --- |
| `docs/c5_qcore_shield_budget.md` | `9a2ea9d32c79206cb8c9808d24b1a234ffcd1e0e0c334175244acc89c90f0792` |
| `scripts/c5_qcore_shield_screen.py` | `56bebdc217128b0140f485c1c4d245f9756ab32e58e726571a063a89dfb05e14` |
| `artifacts/c5_qcore_shield_budget/verdicts.json` | `cad8ea9367a96a15be61b117b0a318cddc572bea131ffbebd6888f9c5398a25a` |

本輪只接受以下具名來源：induced C₅ 是 disk 外框；q=01012；拒絕 q 且每條
非框邊刪後接受同一 q；H 非空連通；唯一 degree-5 roots z,w 相鄰；其他
內點完整 degree 恰四；唯一 mixed 原分量 C*=x₀x₁x₂，root masks=(0,0,3)，
其餘分量 unary。路徑反向 (3,0,0) 可整份換名涵蓋。這些是原 C 報告
§1:45–55 的前提，不加入 T4、Σ=933／941 或「恰缺兩列」。

| 證據層 | 本輪實際承擔 |
| --- | --- |
| 紙面證明 | 原接點 criticality、slack／tightness、外路及 hubs、任意大小末端 block minor、盾弧互斥、零-unary 側排除 |
| 外部定理 | 連通拒絕 degree lists 的 Gallai／blockwise-uniform 刻畫；K₅ minor 非平面；拓撲部分用 Jordan 分離 |
| Python 有限域證書 | D₅ 原身份、3,497 個開放 key、完整 P₃ triples／16 fibres、逐份 contacts／owners、800 hub wiring 控制、有限目錄覆蓋與保存真圖核對 |
| Lean 普通證明 | 無新增 theorem，沒有把紙面拓撲或 Gallai 論證稱為 Lean 已證 |
| Lean native_decide | 本輪沒有此類證書，未執行 lake build |

重新打開外部原文：[Dvořák，List coloring and Gallai trees](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
的 Lemma 7、Corollary 8、Theorem 10，確實適用於連通圖及 degree assignment，
且含 blockwise-uniform；沒有 Σ、T4 或缺列條件。原 PDF 與 hash 保存於
[external](external/SOURCE.json)。W 引用的
[Cranston–Rabern 摘要](https://arxiv.org/abs/1511.00350)確有非 Gallai tree
degree-choosability，但末端 cycle 的同 palette 步驟須明列上述更完整的依賴。

主 checker [audit_d6.py](audit_d6.py)只 import Python 標準函式庫，從保存的資料
重建小型關係與計數，沒有 import W 或其他被稽核 checker。逐 key 結果在
[independent_results.json](independent_results.json)。

```bash
python3 audits/2026-10-04-task-d6/audit_d6.py --output audits/2026-10-04-task-d6/independent_results.json
python3 audits/2026-10-04-task-d6/scope_history/check_scope_history.py
.venv/bin/python audits/2026-10-04-task-d6/topology/check_small_fans.py
python3 audits/2026-10-04-task-d6/calibration/check_calibration.py
```

子 checker 的輸出路徑只在 D₆ 內；沒有既有大枚舉或 producer 重跑。
[本輪獨立執行紀錄](independent_execution.json)保存以上四份 checker 的實際
命令與輸出，全部 exit 0。
W 的原程式另僅執行小型只讀重播，目的是記錄現行 byte-check 狀態，沒有
用它的通過與否取代獨立推導。

## 2. 逐項判定

| 項目 | 判定 | 原位置與稽核結論 |
| --- | --- | --- |
| 1. C* 盾弧至少兩邊 | **確認** | W §5:205–207；連通與三個具名框附件已足夠 |
| 2. unary 長盾弧、拒絕見證及 hubs | **確認** | W §3.3:159–171、§5:209–218；以下逐步補出完整原圖構造與外部依賴 |
| 3. 跨 root 互斥、開面更正 | **確認** | 盾弧引理 1(d):92–98；更正有效，舊閉包句字面仍錯，宜直接替換 |
| 4. 獨立重數與原分量身份 | **確認** | D₅ scope ledger `/ledger/*`；每葉兩側各至少一份，按分量而非 contact 計數 |
| 5. C 的來源分支完整性 | **確認** | C §1、§3–5；零-unary 側也能由原 criticality 排除，完整性短證應寫回 |
| 6. 舊工作為何保留短支援 | **確認** | C:35、77、248、292–295；原工作明示不用 Gallai，只保留必要 profile／幾何 |
| 7a. 保存真實圖的合理性對照 | **確認** | 兩批保存輸入去重 71 圖，無第三長 piece 加兩份不同 unary 的圖 |
| 7b. 題述無條件「任何平面 disk」推論 | **錯誤** | 遺漏拒絕／criticality 等前提；獨立小型 disk 反例見 §2.7，不能用這個強化命題批刪其他來源 |
| 交付／現行 byte replay | **有缺口** | verdict `/sources/docs~1c5_unary_shield_budget.md` 綁舊文件，現行 `--check` exit 1；可用版本化新證書補上 |

### 2.1 C* 的下界

C* 自身連通。刪 C* 後 z,w 與 zw 仍在，各其他原分量連到其唯一 root，
故 H−C* 非空連通，盾弧有定義。|S₀|=3 是完整 degree 四減去 x₀x₁ 原邊
得到的三個**不同框點**，所以 S_C* 不包含於任一框邊的兩端點。

重推支援標記：若支援點 v 的兩條框邊都鄰接 F_C*，在該開面以短弧連接
兩邊近 v 的內點，再接框角得到閉曲線。v 的附件進入其內側，連通 C*
全在同側；另一支援點的附件必穿出，違反嵌入。故每個支援點至少關聯
一條盾弧邊，單邊不能標記三個不同框點，得到 |σ_C*|≥2。
這一步不需要 S₀ 的三種 q 色，更不需要 T4。詳見 [拓撲筆記](topology/NOTES.md)。

### 2.2 unary 的六個子步驟

**拒絕見證。** 原 unary D 的唯一 root 為 r，取實際邊 rp。M−rp 有同一
字面 q 的完整延拓 f；限制到 M−D 得 ψ。若 ψ 可延拓 D，就是 M 的 q
延拓，矛盾。不能只取 tuple 的邊際或改換色框。原 C 的每邊 q-criticality
直接供應此見證，不必搬用固定 Σ 的「新接受某列」結論。

**實際外路。** 若 S_D⊆{a,b} 且 ab 是框邊，選 h∈S₀−{a,b}；S₀ 有三點
保證可選。兩 roots 都由原 mask=3 直接接 x₂，故
L=r–x₂–x₁–x₀–b_h 是原簡單路徑，內部全在不同的原分量 C*，避開 D
與其他框點。h 的附件是 x₀ 的實際原邊，不是從其他來源拼入的路徑。

**三 hubs。** c=ψ(r) 不在 {q(a),q(b)} 時，取
X={a}、Y={b}、Z=(B−{a,b})∪V(L)。a,b 相鄰，餘三框點構成路徑；
L 接到其中的 h，所以 Z 連通。三集合互斥；ab 與補框弧兩端的原邊給
三對鄰接。N(D)⊆{a,b,r}，各 hub 在與 N(D) 的交集上分別只見 q(a)、
q(b)、c，三色異色。

**兩 hubs。** c=q(a) 時，取 X={b}、Y=(B−{b})∪V(L)；c=q(b) 對稱。
框路徑與 L 使 Y 連通，ab 給 X–Y 鄰接；N(D) 上的顏色分別為 q(b)、c。
要求的是 hub **在 N(D) 上**單色，整條 L 或整段框路徑在 ψ 中無須單色。

**degree 與收縮。** 原 C §1 規定除 z,w 外每個內點完整 degree 恰四，
故 D 每點都恰四。令 L_D(v)=U−ψ(N(v)−D)，則
|L_D(v)|≥4−|N(v)−D|=deg_D(v)。任一 slack 点作生成樹根，由葉到根
貪婪可著色；拒絕因此迫處處 tight，即每點外鄰顏色全部不同。特別是
兩-hub 情形，不能有同一 D 點同接 r,a；合併同色 hub 不會丟 incident
邊數，lists 與完整 degree 四都保留。

**空／單點支援。** 同樣包含於某框邊，仍能選 h 與 L。未碰 D 的 hub
單色條件為空條件；刪掉非活躍 hubs 不影響 lists。只剩一個活躍 hub 時，
min deg_D≥3，與下述 K₄-free Gallai tree 的末端 block 私有點 degree≤2
矛盾。因此沒有這兩種支援的遺漏。

不能只因「定理 B 已寫過」接受最後的 K₅。重新核對原引用後，重推如下：
拒絕 degree lists 由外部 Theorem 10 給 Gallai tree 及 blockwise-uniform。
若有 K₄ block，其各點完整 degree 四只餘一個外方向；它是外 hub 附件，
或通向 block 外的 bridge。切 bridge 後兩側根均有 slack、均可色；拒絕
迫兩根可取色集合是同一 singleton。外側若不碰任何 hub，四色置換全
保留，根不可能只取一色，所以四個 clique 點各有互斥 tether 到連通
外 hub 聯集；四 singleton 加外 hub／tethers 得 K₅。這也補足原
`c5_degree5_tree_components.md:32–36` 字面较窄的 minimal／單 root 設定，
没有把它直接無條件引用。較大 clique 本身含 K₅，亦排除。

餘下末端 blocks 只有 bridges、odd cycles。兩 hubs 時 min degree≥2，
末端不能是 bridge；取末端 cycle 的相鄰私有 u,v，兩者都接兩 hubs。
D−{u,v} 非空連通，且有原 degree 二點（單 block 的剩餘點，或另一末端
block 私有點），也接兩 hubs。兩 hubs、u、v、餘下 D 是五袋 K₅。

三 hubs 時，末端 cycle 的私有二元 lists 是同一 palette，所以相鄰私有
u,v 接同一對 hubs。第三 hub 若碰 D，只能碰餘下 D；把它與餘下 D 合成
第五袋就有 K₅。若不碰 D，回到兩 hubs。末端 bridge uv、u 私有時，u
接三 hubs，只能取第四色 δ。D−u 在 v 有 slack、可色；拒絕迫 v 的完整
domain={δ}。若餘下 D 漏某個色 A 的 hub，交换 δ,A 會保持全部 lists
而使 v=A，矛盾。因此三 hubs、u、D−u 也是五袋 K₅。

每步都使用原圖中的連通 branch sets；收縮只供非平面反證，不保持完整
Σ 或 boundary-state 語意。完整補查見 [HUB_RECHECK](topology/HUB_RECHECK.md)。
得到 S_D 不包含於任何框邊兩端點，再用純拓撲 1(b) 得 |σ_D|≥2。

### 2.3 跨 root 互斥與措辭更正

所有原 pieces 都是 one-sided：刪它們後原 zw 把 roots 連在一起。互斥證明
不要求 pieces 接同一 root。反設 e 同在 σ_P、σ_Q，聯合圖鄰 e 的內面 Z
包含於 K_P 鄰 e 的面 E，且 E≠F_P。Q 及附件的所有非框點在**開** F_P；
逐點存在完全位於 F_P 的小鄰域，所以不在 closure(E)，也不在 ∂Z。
對稱排掉 P 的非框點，剩 ∂Z⊆B。Z 在連通開 disk 內非空、開且閉，
只能是整个開 disk，與非空 P 在其外矛盾。

2026-10-04 的開面修補有效。舊句「F_P 與 E 的閉包不交」確實錯，兩面
甚至可共享整條 b₀–p–b₂ 內部路徑，不只框點。已有更正指明有效證明，
但整合者應直接替換舊正文，避免再誤引。

### 2.4 逐 key 的分量計數

從 D₅ 原 scope 的 `z_role.unary_contacts`、`w_role.unary_contacts` 分拆重數，
與 `original_unary_components` 逐份名稱、owner、完整 ordered contacts 核對。
例如分拆 (2,1) 是兩份連通分量，分拆 (3) 是一份三接點分量；不是按邊數
收費。每葉原 contact 符號互異，兩 roots 的 component 名稱互異，未發現把
同一分量的不同接點冒充多份 unary 的 key。

| unary 原分量數 | 開放 keys | 加 C* 的框邊下界 |
| ---: | ---: | ---: |
| 2 | 1,258 | 6 |
| 3 | 1,679 | 8 |
| 4 | 560 | 10 |
| 合計 | 3,497 | 全部超過 5 |

共 9,793 個「key 內分量」實例，其中 8,398 份 own support 未知。沒有替它們
猜內部圖、relation、或從 A_r 分配 own support。這些是具名必要來源**類**：
「它們確為不同 H−R 分量」來自 C 原分量定義及原側分拆，並非已存在圖的
連通性證書；Python 另核對刪 piece 後的 incidence 骨架連通。

獨立重算完整 P₃ tuples／全部 16 root fibres、原 row canonical SHA、verdict
key／ID／JSON pointers／28 certificates 均一致。全圖支援分布亦重數為
2,300 份全框、597 份缺 b₃、600 份缺 b₀。因此沒有偷用 W0／W2 的 T4 前提。

### 2.5 來源分支完整性與零-unary 側

不以「36 案例」數字當完備性證明。獨立小型控制重建全部 500 份 (3,2,1)
具名附件、112 份非空 F*、560 residual，再在 C 的雙扇區／tether 必要域
內重建 19,340 個子集 products；與保存的 36 cases／140 geometries／3,500
keys 比較**完整集合**，不只是比較 counts。三個 a 的完整必要側接合各 125
份；沒有零-unary root。重推與結果見 [scope notes](scope_history/NOTES.md)及
[independent_scope_results.json](scope_history/independent_scope_results.json)。

更直接的任意大小完備性短證不需要該表：P₃ 拒絕 pair 由原 lists 迫
F*={(a,3),(3,a)}；刪 zw 釋放對角，刪 mixed 接點釋放非對角，原拒絕遂迫
E_z,E_w 是 C §1 的五型，即至少一側是 T={a,3}，另一側 T、{a} 或 {3}。
具體地，非對角釋放只能是 (a,3) 或 (3,a)；若某側另含 T 外的色，它與
另一側既有的 a 或 3 組成合法非對角且不在 F*，已延拓原 M，矛盾。因此
兩側都包含於 T；再要求可用對角及非對角，恰得該五型。這一步也不用
其他報告的完整 Σ 容量分類。

若某側沒有 unary，degree 五扣 zw、rx₂ 後恰有三條 spokes。它們的 q 色
必互異：兩條同色時刪其中一條不改任何染色限制，違 q-criticality。
所以三條 spokes 禁掉三個已用色，該側 E={3}，不可能是 T 或 {a}。
若該側 E={3}，另一側必為 T；刪它的 a 色 spoke 後只新增 root 色 a。
新增 (a,a) 撞 zw，新增 (a,3) 撞 F*；其餘配對原本已拒絕。因此刪這條
spoke 仍不接受 q，亦違 criticality。兩 roots 所以各至少有一份 unary。

原 C 未把這短證明列為獨立完備性段落，但零-unary 不是目錄外遺漏。
補上後 C-W 可排除 C §1 的整個來源分支，而不僅報「目錄清空」。適用
範圍仍是指定原 degree、唯一 mixed P₃ 與共鄰端點 masks；不能寫成所有
P₃／其他 mixed／一般 weak-deletion 都完成。無 target、repair 或一般出口結論。

### 2.6 舊工作保留 {1,2} 的原因

原 C:35 明寫「不需 T4／Gallai」，§1:77 明寫不加入完整 Σ，§5:248 與
292–295 區分必要支援和真正 degree／minimality 實現。D₅ 第一列
(CPP-131-0,0,0) 的 D_z_0 own support={1,2}、f={0,1}，給 E_z={2,3}。
它對舊穩定子／整側幾何是合法**必要 profile**；不是可實現的 degree-four
q-critical unary 證書。舊論證不能從這些必要資料推出不存在，刻意保留
它們；新 hub 論證加入 lists／Gallai／外路後才排除。不存在舊 Gallai
定理已覆蓋卻被數值 checker 漏套的證據。

### 2.7 真實圖对照與過強推論反例

[獨立 calibration checker](calibration/check_calibration.py)從保存 edges 重建
degree、R、H−R components、owners、own support、one-sided，逐份重算保存
rotation 的 darts／Euler／C₅ 面，以及完整 boundary relation／刪邊 minimality。
131 次保存圖出現去重為 71 個 labelled 圖；15 圖有兩 unary，全部只有
兩個 pieces 與單一 root，沒有第三個長支援 piece。沒有保存真圖違反
帶完整前提的 C-W／三 piece 預算推論。這是有限 saved-witness 對照，不是
重新枚舉整個 catalogue，也不是任意大小定理的證明。

題述「任何平面 disk 圖，只要一份長支援 one-sided 分量加兩份 unary 就
不能存在」漏掉拒絕與 criticality。獨立負控制甚至可保持全體非-root
degree 四、單 root degree 五，仍有三個 one-sided pieces：長支援 piece
加兩個框邊支援的 triangle unary。它有合法 q 延拓，所以不具有 unary
拒絕見證；不能對它們主張長盾弧。另有拒絕 q 但 unary 非 critical 的
degree-nine root 控制，同樣说明「拒絕」不能代替接點 criticality。
完整原邊、rotation、degree、piece 名稱與延拓／刪邊證據保存在
[calibration results](calibration/results.json)，詳見 [calibration report](calibration/REPORT.md)。
這些反例針對強化轉述；C-W 原定理的每條非框邊 critical、原 degree 與
共鄰 P₃ 前提沒有反例。三件收費物還必須是**三個不同**原 pieces，不能
把同一長支援 unary 重算為額外長 piece。

## 3. 交付缺口與 ledger 合併前置

verdict 保存的盾弧文件是 20,625 bytes、SHA
`e4a3515a7e5e38d5e8b10b34b18e33d1d890fb29a1613e1a202842e8388da110`；
本輪開始時更正後文件為 20,896 bytes、SHA
`11a0b9f9422396dad22927de003764bf5218e6f3e2967fd7c3984748294d6c2b`。
其他已記錄來源 hash 全部一致。這個舊 hash 在本輪開始時就已存在，與
本輪 input 漂移不同。

實際 `python3 scripts/c5_qcore_shield_screen.py --check` exit 1，訊息
`verdict artifact differs from replay`，見 [original_w_replay.json](original_w_replay.json)。
另只讀執行 default，將舊 artifact 的唯一文件 source binding 在記憶體
改為現行 hash，獨立編碼所得 SHA 與 producer 當次輸出一致：
`206b94469b2b0a0b80dc2d38fa3bd5abbd68d9244eb1884decc2f45d320082bf`。
這確認數學 verdict／keys／certificates payload 沒有其他差異，見
[payload comparison](original_w_payload_comparison.json)。沒有寫回 artifact。

W §6:272 的成功紀錄可保留為原輪歷史，必須加註更正後的現行 replay
失敗；不能把這次失敗抹成已驗收通過。可保存舊 artifact 及版本，產出
新的修訂版 verdict，明列僅來源文件 hash 變更，再重新驗證。

雖然數學排除確認，**目前不能直接在 STAGES 添一列後覆寫 canonical
ledger**。原重算器只接受單 key `observations.json` 的 `/identity`，還
硬核對 D₅ 恰三個 closures、3,497 open、下一 key 開放；W 是多 key
`verdicts.json`。W 另外讀取並 hash 綁定現行 C4 ledger：若覆寫成 0 open，
其後續重播會改讀新狀態，原 3,497 verdict 就不能重播。

具體的版本化合併設計及 `--write` 前後集合／hash 檢查見
[MERGE_PLAN](scope_history/MERGE_PLAN.md)。這份是供補足交付後使用的條件式
整合說明，本輪沒有執行任何 `--write`，也沒有改重算器。

## 4. 整合者應寫回的更正

1. 盾弧引理 1(d) 直接替換旧「閉包不交」句；兩閉包可以共用內部路徑，
   正確需求是另一 piece 非框點在開面中，逐點有避開非所在面的鄰域。
2. W §3.3／§5 明列原 contact q-criticality、同圖外路與實際雙 root–x₂ 邊；
   hub 在 N(D) 上單色，空／單點支援及非活躍 hub 均涵蓋。
3. 明列 Gallai 的 blockwise-uniform 外部版本與較窄 K₄ 引理的四 tether
   補證；不能僅引用 Gallai tree 摘要或固定 Σ 的短支援結論。
4. 將 §2.5 的零-unary 側 criticality 短證寫入 C/W，才能精確說「C §1
   共鄰端點 P₃ 來源分支排除完成」。其他前提／接線不由此推出。
5. 對三個不同 pieces 收費；不要把長支援 unary 同時計成第三份長 piece。
   刪去不帶 criticality／degree 條件的任意 disk 強化說法。
6. 保存原 verdict 的舊文件 hash 與歷史 replay；新增修訂證書／版本化
   前驅路由，補現行 replay 失敗，不覆寫歷史來取得 PASS。
7. 合併時保留 3,500 原 key、36／140／900 舊表、原完整 relations／fibres
   與三份繼承閉合；W 只新增原開放集合 3,497 個來源排除，目標查詢仍為零。

## 5. 本輪要求的最終檢查

| 命令 | 實際結果 |
| --- | --- |
| `python3 scripts/check_docs.py` | exit 0；545 Markdown、5,775 local links，anchors／index／handoff 通過 |
| `python3 tools/docgraph check` | 最終 exit 0；62 documents、213 relations、5 families，0 errors／0 notes |
| `git diff --check` | exit 0，無輸出 |
| `python3 audits/2026-10-04-task-d6/verify_inputs.py` | exit 0；31 份原檔及對應快照皆無漂移，新增稽核文件本地連結／whitespace 通過 |
| 原 W `--check` | exit 1；舊文件 hash 導致 artifact differs from replay，不能列為通過 |

[validation_results.json](validation_results.json)保留第一次 DocGraph 失敗與
最終三項檢查結果：第一次本輪 snapshot 中的
`c5.adjacent-degree5-interfaces` 被當成 live 文件，造成 duplicate-id；
只將本輪快照移到 `.snapshot` 並保留 symlink 後重新檢查通過。原文件沒有改。
另 [verification_attempt1.json](verification_attempt1.json)保留交付驗證中途的
未完成狀態；最終 verifier 將「輸入 hash 不變」與外部 Git 狀態變化分開。

原 HEAD、分支不變；本任務沒有 commit／push。結束時 Git 狀態另出現
`audits/2026-10-04-task-d7/`，是本任務目錄外的並行新增觀測，沒有因而聲稱
整個工作區狀態完全未變；被稽核物及本輪全部 31 份原讀取檔案 SHA 仍一致。
沒有覆寫歷史 artifact 來消除舊 hash、没有執行任何 ledger `--write`。
