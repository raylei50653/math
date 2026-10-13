# W5-NO4CT-BRIDGE：逐項依賴與三支覆蓋表

BASE `d5211633ba80c2b10cb12eaa8189421e35a31cc3`。完整證明見 [PROOF](PROOF.md)。
「接通」指新 no4ct 全域最小來源的條件定理，不代表一般來源已排除。

| 真正需要的事實 | 舊入口的依賴或風險 | 本輪採用的新依據 | 狀態／使用處 |
|---|---|---|---|
| 所有目錄外圖先最小 k、再最大邊數 | 固定 933／941 mask 最小性不足替代 | no4ct 全域契約；[交接 §2](../../docs/tasks/c5_no4ct_handoff.md#2-接手必須保留的精確契約) | 已供應，三支共同 |
| 簡單二連通、B induced、原內面三角、非空 Σ | 舊共面正規形曾消費 universal screen | [no4ct dependency](../2026-10-13-c5-no4ct-dependency-6cafdfb/REPORT.md)及[度數](../2026-10-13-c5-no4ct-degrees-6cafdfb/REPORT.md) | 已供應；932 本身非空 |
| 完整 d_G(B)≥4、d_G(內點)≥5 | 不可移為 d_F≥5 | 同上度數修復；frontier W5 §1 | 已供應；所有 degree 比較明寫 G |
| k≥16，故 r=k−6≥10 | 舊 q≤3 用 k≥13、q=4 用 k≥14 | no4ct K≤15／球面接入，保留上游外部有限計算信任 | 已供應；新域包含於舊域，不改舊 BASE |
| 原 C4 cap 空，含接觸 B 者 | 舊任意大小 C4 三內點代表曾用普遍 4CT screen | [frontier PROOF §§2–3](../2026-10-13-c5-no4ct-frontier-6943561/w5/PROOF.md)：i(C)≥1，s≤k−i(C)<k，受限代表＋degree | 相對大小修復已供應；CAP-REL |
| proper 原 C5 cap 空或一個 W5 | 不得把 C=B 當較小 cap | 同上：C≠B ⇒ i(C)≥1 ⇒ s<k；K 五內點代表＋degree | 已供應上游；取得局部 L 後模板分類不另消費 |
| 原框 B 每點附件≤2、雙接相鄰 | 舊外圈報告範圍寫 933／941 | frontier §4 以原 C4 空 cap、B induced、d_G(B)≥4 直接重證 | 已供應，ATT-B，含 932 |
| 原 U 每點附件≤2、雙接相鄰 | 不能只憑 B 版或 W5 存在性省略 | 原 x-ui-v-uj C4 的兩個非空 U 開弧；[PROOF §2](PROOF.md#2-新契約供應-l相對-cap-與雙環附件) | 本輪明示 ATT-U，任取合法 W5 |
| 合法全內部 induced W5 存在 | 存在不會自動給每個 W5 的圈秩界 | frontier §5；本輪在任意選取後重新供應 L | 已供應；量詞為任取 |
| 孤立點／葉、所有原分量與橋 | 不能先假設連通或無葉 | d_G=d_F+d_T、d_T≤4；一般面 incidence 把 bridge 算兩側 | 已證共同接點 |
| essential／contractible 互斥窮盡 | 不能只按抽象 cycle basis 分類 | U/v 所在原 F 面、boundary walk／Jordan、PPP 空面引理 | 已證 FACE-SPLIT；slits、多邊界不漏項 |
| blocks、ears、tails、subdivisions 及附件編碼 | Σ∈K 不等於來源已落入模板 | [PROOF §§4–5](PROOF.md#4-森林至圈秩二的來源覆蓋)及三份 branch reviews，逐原面反向讀出全部參數 | 全部接通，分類不消費來源 mask |
| 原 B/U pin 映回、完整十列 K membership | 不可獨立反 U 或拼不同 full lifts | 原嵌入同構、共同 ε／S4；K132 全 D5 封閉 | 紙面＋本輪有限 D5 核對 |
| 每份原模板完整 Σ∈K | 保留舊有限證書的信任，不以本輪 hashes 代替染色證明 | 七份原 seal，正常／seed17／獨立 receipts；[INPUTS](INPUTS.json)逐 SHA 接入 | 沿用原完整計算，本輪只驗 custody／摘要接點 |
| 普遍 4CT exterior screen／任意 C4 代表 | 舊來源鏈中確實存在，不能修改其歷史說明 | 所需小 cap 已由 s<k 修復；低圈秩局部 L 以後完全不用 screen | 本輪不消費；未宣稱普遍 screen 已證 |
| 相對 planar 可染性 N≤k+5 | 可修其他商圖，但需逐圖數點 | 本輪低圈秩來源到模板均是原圖同構，沒有可染性商圖步驟 | 本輪不直接消費；不放大其量詞 |
| 非空 singleton support、933／941 專用 identities | 932 沒有 singleton 支援 | 原模板最終 membership 矛盾只需 Σ∉K | 無一分支需要；舊敘述以新共同矛盾取代 |
| 一般九點 W5 代表 | 是另項與主命題條件等價的目標 | 不列為引理或必要依賴 | 不在任務；OPEN |

| 圈秩／位置 | 932 | 933 | 941 | 覆蓋／有限證據 |
|---|---|---|---|---|
| 0 | 接通 | 接通 | 接通 | 新 r≥10 與森林 r≤8 直接矛盾 |
| 1 contractible | 接通 | 接通 | 接通 | 三角三 charges 超過 M；純紙面 |
| 1 essential | 接通 | 接通 | 接通 | 純 C10；沿用 1,652 模板，必要子域 252 |
| 2 essential | 接通 | 接通 | 接通 | PPP 三角角 excess≥3>2；純紙面 |
| 2 contractible | 接通 | 接通 | 接通 | 四型覆蓋後 diamond strip；沿用 974，子域 70 |
| 3 essential | 接通 | 接通 | 接通 | diamond＋完整原外路；沿用 1,283，子域 790 |
| 3 contractible | 接通 | 接通 | 接通 | pentagon／ear tails；沿用 2,270，子域 484 |
| 4 essential | 接通 | 接通 | 接通 | pentagon fan＋完整原外路；沿用 2,872，子域 2,368 |
| 4 contractible | 接通 | 接通 | 接通 | H／DD／H+P／DD+P／D+D；沿用 6,389，子域 2,955 |

表中子域只是以 r≥10 限制原摘要，保留額外模板，不是新增來源枚舉或來源
實現性宣稱。所有原未觸發、失敗紀錄、BASE 與 seal 照原樣保存。
新橋接沒有尚未修復的低圈秩具名引理。一般 ρ≥5 縮減、無界三支排除與
K∞=K≤5 仍 OPEN；紙面及 Python 與 Lean 分層，沒有新增 Lean theorem。
