# 任務 D：最新五輪與前置證書只讀稽核

2026-10-04。稽核截點為 **2026-10-04 08:58:32 Asia/Taipei**（00:58:32 UTC），
HEAD=`0e3812712b68f57927df86f30a07bb8074e090f9`。本報告針對截點副本，
不包含其後併行研究新建的 mixed12／mixed22 程式或產物。

**47／75 份 mixed-(1,1) 身份完整、互斥，最後殘留 0／0。** 最新五輪的
10 次 byte-check 全通過；四／五角色投影與指定列完整 joint 的精確宣稱一致。
22 份相關證書共執行 44 次 `--check`：40 次通過，4 次為兩份歷史證書在
兩個 hashseed 下的已知文件 hash 失敗。兩份證書完整重算後，除直接
`input_sha256` 映射外全部 payload 相同，沒有非文件 input 差異。

需要整合者修訂的是文件現況與少數措辭。另有一個嵌入見證邊界：root swap
保留身份與合法搬運後 rotation，但 16 份共用 pair 自交換身份的搬運後
rotation 不等於另行選出的 canonical rotation。這不破壞現有排除證據。

交付入口：[具體修訂清單](REVISION_CHECKLIST.md)、[文件子稽核](docs/documentation_audit.md)、
[身份／搬運結果](identity/identity_results.json)、[投影子稽核](projection/notes.md)、
[所有重播結果](checks.json)。本次只新增此獨立 `audits/` 目錄；未整合
README、STATUS、導覽、專題正文、history、MANIFEST 或歷史 artifacts，未 commit／push。

## 範圍、前提與截點

最新五輪為 short_face、long_face、crosscut、short_arc、disjoint_pairs。
直接前置為 equal_pair、short-support singleton、single-spoke 具名來源域；
另重播已發布的 four-spoke `(3,1)` 相關證書、leaf fibres、歷史 singles
payload audit，以及 941 ε=1 全三分支和容量／subcover 證書，以核對沿用範圍
與 synthesis 所指舊停止點。完整命令、hashseed、stdout、stderr、exit code
見 `checks.json` 及兩個 replays 子目錄。

全部數學檢查在 `/tmp/math-task-d-audit-_l2g06k7/snapshot` 執行；它是原
scripts、docs、tools、artifacts 的複本，後補只讀文件連結目標。
[baseline.json](baseline.json) 記錄 1,209 份原文件的 SHA256 與大小。
所有生產器只以 `--check` 呼叫；兩份失敗證書另以記憶體中的 `build()`
比較 JSON，從未以無參數生成模式覆寫證書。

沿用數學結論的前提仍是固定完整 Σ=933／941 或整圖 D₅ 像、
Σ-edge-minimal induced-C₅ disk、有效內圖連通、ε=2、相鄰雙完整 degree-5
roots、其餘有效內點完整 degree 四；本子型另有兩側各兩原 spokes、
唯一原 mixed incidence `(1,1)`、各側一原單接點 unary。contacts 可共鄰，
不複製原頂點；actual attachments／supports、原分量、bridges、ownership、
環序及共同色框不能丟失。

本稽核核對固定證書、serialized 原圖／relation／witness 與文件合約。
任意大小 disk crosscut／Gallai／短支援論證仍屬紙面依賴；未新增 Lean
定理、未建立來源實現、ε≥3、一般出口或 `K∞=K≤5`。没有重播 degree-6
全分拆、前序雙 unary 的完整 SAT／接合搜尋、R 系列、全倉來源 catalogue
或 Lean axiom audit；沒有執行 `lake build`。舊研究紀錄的 build 通過只是
舊紀錄，本次不把它列作實際檢查。

## 逐 identity 的完整性與搬運

[獨立身份程式](identity/audit_identity.py) 不匯入研究 checker；從原
single-spoke source 的 `necessary_skeleton_only`、原 spoke 長度 `[2,2]`
重新篩出完整域，逐一比對 index、root order、spokes、retained edges、
apex rotation。原 completion ledger 只核對首域的完整身份，後續依 set
相減；本稽核另檢查每階段 exclusion／residual 陣列沒有重複，以及所有
203＋349 次攜帶的身份與同一來源一致，避免 set 轉換掩蓋重複。

| 階段 | 933 新排 | 933 殘留 | 941 新排 | 941 殘留 |
| --- | ---: | ---: | ---: | ---: |
| equal_pair | 7 | 40 | 9 | 66 |
| short_face | 8 | 32 | 16 | 50 |
| long_face | 10 | 22 | 10 | 40 |
| crosscut | 8 | 14 | 16 | 24 |
| short_arc | 0 | 14 | 6 | 18 |
| disjoint_pairs | 14 | 0 | 18 | 0 |
| 合計 | **47** | **0** | **75** | **0** |

Exact indices 全部保存在 [identity_results.json](identity/identity_results.json)，
不是只比對總數。六階段互斥且聯集正好等於各來源的原具名域；disjoint
最後再分一側全短 4／8 與共同兩段長 face 10／10。

root swap 在完整 122 份域形成 involution：933 有 20 組互換與 7 份
自交換，941 有 33 組互換與 9 份自交換。spokes、原 root edges、owner
角色及原分量隨同一映射搬運；不是從另一份來源抽取 marginal。
另逐份驗證搬運後 rotation 的 dart、鄰接、Euler characteristic 與原
兩-root faces。106 份 unequal identities 的 canonical partner face 集
相符；16 份 equal-pair 自交換身份的 canonical face 集不具交換協變性，
但搬運原 rotation 仍合法，共享 roots 的兩個封閉三角區域保持。例子
933 index 96 及全部 16 份差異均保存。不能把合法 relabeling 寫成
「重新選取的 canonical embedding 字面相同」。

D₅ 獨立檢查包含 1,220 份具名骨架搬運、12,200 份 row／共同 S₄
色框、195,200 份字面 root-pair guards，及 6,400 actual support pairs
的 64,000 份搬運。外路徑、support span 與次序共同搬運，不逐分量
重新正規化。short_arc 六份來源另檢查 606,690 個完整 tuple pullbacks。
source mask 隨 rows 一起搬運：crosscut 的 933 幾何比較例實際變成
940，並非 941；short_arc 的部分 941 身份變成 949。此類比較只能
沿用同一幾何機制，不能把 mask 或固定拒絕列留在原值。

## 投影、完整 joint 與 witnesses

[獨立投影程式](projection/audit_projection.py) 以另寫的 MRV 回溯枚舉
component relations 與整圖 joints，不匯入原枚舉器、joint helper 或
witness validator。從 actual attachments、internal edges、contacts、
owners 與 spokes 重建全部控制圖，再核對每個完整 tuple、字面纖維及
coloring witness。

| 證據 | 精確宣稱 | 本次確認 |
| --- | --- | --- |
| equal_pair | 忘記 C contacts 後，`π_(a,b,u,v) J_G = J_(G−C)` | 紙面 sealed triangle 合約清楚；固定 controls 的完整圖 relation 與原邊接回相符。固定圖本身不驗證任意大小幾何結論。 |
| short_face／long_face | 替換固定短 U 或 V；五角色投影相等，該 unary 外頂點逐點保持 | short_face 的 108 個多色 U 列與 3,736 witnesses；long_face 的 U／V 66／90 列與 680／1,012 witnesses 通過。singleton 負控制保留。 |
| crosscut | 替換原 C；四角色 `(a,b,u,v)` 投影相等，C 外逐點保持 | 540 個投影等式、7,752 witnesses 通過；G−ax／G−by 各 180 列的六角色 joints 都不相等。 |
| short_arc | 指定拒絕列 `01021` 的完整六角色 joint 有延拓 | 12 份原整圖 coloring 及 101,115 份抽象 tuple witnesses 通過；没有 all-root-pair 或全 Σ 不變宣稱。 |
| disjoint_pairs | 固定短 unary 的五角色替換；原 C 與另一 unary 保持 | 重算原 long_face 的 01／04 conditional operator payload 完全相同；未把這些控制圖改稱 disjoint-spoke source 圖。 |

獨立枚舉總計：108 份固定 degree 圖、3,240 份完整 component relations、
8,340 份完整整圖 joints、133,440 份字面 pinned fibres（其中 111,952
為空）、117,032 份整圖 witnesses、9,440 份 component witnesses。
4,170 次原圖 root relabel 同時核對 edges／contacts／owners／ports／
joint／fibres。38 份共鄰圖的 `x=y` 保持同一頂點。

保存的反例清楚展示投影不能升為完整 joint 等式：crosscut control 0、
row 0=`01012`，`G−ax` 的 `(3,2,3,0,2,3)` 違反原 `a≠x`；四角色投影
仍能接回原 C。short_face control 0、row 1=`01021`，`G−au` 的
`(2,1,3,3,2,2)` 違反 `a≠u`，五角色投影仍相等。原圖字面 edge filter
接回等式與未接回的刪邊圖 joint 相等，是不同宣稱。

short_arc 從全部 65,535 個非空 16-tuple subsets 獨立篩出恰 963 份
stable、`F_C=∅` 的完整 relations，其中 5 份 diagonal，與原證書一致。
這是有限 relation-schema 全域核對；不是這些 schemas 的來源圖實現證明。

## 實際 `--check`、文件 hash 與 payload 差異

每份下表證書皆跑 default（移除環境中的 PYTHONHASHSEED）與
`PYTHONHASHSEED=17`。需要 networkx 的四份以報告指定的
`uv run --with networkx==3.5 python` 執行，其餘以 `python3` 執行。

| 22 份重播證書（名稱省略 `.py`） | default／17 |
| --- | --- |
| `c5_excess_two_mixed_core_four_spoke_short_face` | PASS／PASS |
| `c5_excess_two_mixed_core_four_spoke_long_face` | PASS／PASS |
| `c5_excess_two_mixed_core_four_spoke_crosscut` | PASS／PASS |
| `c5_excess_two_mixed_core_four_spoke_short_arc` | PASS／PASS |
| `c5_excess_two_mixed_core_four_spoke_disjoint_pairs` | PASS／PASS |
| `c5_excess_two_mixed_core_four_spoke_equal_pair` | PASS／PASS |
| `c5_short_support_singleton` | PASS／PASS |
| `c5_excess_two_mixed_core_leaf_fibers` | PASS／PASS |
| `c5_excess_two_mixed_core_single_spoke` | **FAIL／FAIL：文件 hash** |
| `c5_excess_two_mixed_core_four_spoke_singles` | **FAIL／FAIL：文件 hash** |
| `c5_excess_two_four_spoke_progress_audit` | PASS／PASS |
| `c5_excess_two_mixed_core_four_spoke_binary` | PASS／PASS |
| `c5_excess_two_four_spoke_binary_star` | PASS／PASS |
| `c5_excess_two_four_spoke_binary_hubs` | PASS／PASS |
| `c5_excess_two_mixed_core_four_spoke_ternary` | PASS／PASS |
| `c5_excess_two_mixed_core_four_spoke_quaternary` | PASS／PASS |
| `c5_single_spoke_three_one` | PASS／PASS |
| `c5_941_single_spoke` | PASS／PASS |
| `c5_941_two_spoke` | PASS／PASS |
| `c5_941_three_spoke` | PASS／PASS |
| `c5_excess_one_subcovers` | PASS／PASS |
| `c5_independent_support_capacity` | PASS／PASS |

兩份歷史失敗均是 `AssertionError: certificate differs`；不是 import／
環境／數學 assert 失敗。[semantic_payload_results.json](semantic_payload_results.json)
記錄重新計算全部 JSON 後，**只移除直接 `input_sha256` 字段**的完整
深比較：兩份皆相同，非文件 hash 差異為零，原 artifact bytes 未改動。
沒有只比摘要、marginals、orbit 數或控制數字。

| 歷史證書 | 漂移文件 | 記錄 SHA256 → 截點 SHA256 |
| --- | --- | --- |
| single_spoke | `docs/c5_excess_two_mixed_core_spokes.md` | `4f98574856982f7ed417305cc49bd6830913be662942662b96cc05ccd4184fcc` → `a829d98ebf84a952445e9aebb443cca1b8e0d7129ceaf1a5353b51379f059061` |
| single_spoke | `docs/c5_excess_two_mixed_omission.md` | `635d8276527e21e8fc7fdebc809ce0971528f4c99d2fa66e084943fe534d97b4` → `8ac99e4a5899b94c4bdcf271f20e2028d3af7d433cd81d48fd06e4995d7f7590` |
| single_spoke | `docs/c5_excess_two_root_deletions.md` | `075f82d2488c298ad7b54f38dcf22b0d37afabdaad591274418c43508098f268` → `a8d356c724808f87ed2f4e30a49f0a59e8c970789ce05fdec2934cfde9ed5af2` |
| singles | `docs/c5_excess_two_mixed_core_leaf_fibers.md` | `e79485da8e52529b339c9f782fca7cde7551ad635417b48fc4d95f7cb6c29cb5` → `e5e4155c680814c94a24df638240be5d3a5f33e1a3638333330c4c26f9747981` |

[input_hash_audit.json](input_hash_audit.json) 核對全部 22 份證書記錄的
151 份 input hashes（含不同 schema 的 hash-map 字段），恰上述四份
文件漂移，零非文件漂移。最新五輪的直接 input hashes 均相同。
查過每份漂移文件的 Git 文件歷史，沒有找到與 recorded hash 相符的
已提交完整版本，見 [document_drift_history.json](document_drift_history.json)。
因此不聲稱已重建原文件文本或證明文字改動只涉及何種句子；可確認的是
當前完整 producer payload 的差異只在文件 hashes。文件證明前提另由
子稽核核對，而 byte-check 的失敗保留為失敗。

single-spoke 原證書只給當輪必要域與五-spoke 上界；後續 leaf 證書把
兩候選總 spokes 降至 ≤4。原 progress-audit 的 40／66 是 equal-pair
當時 frontier，不能當成本次零殘留的反例。941 的 single／two-spoke
證書分別留 `[2,3]`／`[3]`，three-spoke 最後留空並合成固定前提下
ε≥2；本次逐份重播確認，這些沿用與後續關係沒有互相覆寫。

## 文件檢查與具體修訂

`check_docs.py` 在補齊副本的只讀 link targets 後通過：510 Markdown、
5,242 local links，anchors／index／handoff 通過。初始副本缺少 Lean／
LICENSE 等目標的 81 次報錯另存原 log；属于副本打包問題，不是原
工作樹文件錯誤。DocGraph 通過：62 documents、213 relations、5 families，
零 errors／notes。`tools/artifacts.py status` 得 `ok=137`；這是
MANIFEST／fingerprint 狀態，不取代 producer byte-check 或數學證明。
源工作樹 `git diff --check` 通過。

人工發現未被結構 checker 捕捉的修訂包括：

- synthesis 後段 `:107`、`:134`、H1 `:209-220`、優先序 `:270`、
  結論 `:298` 沿用「941 ε=1 等待 t=2、t=3」。頁面已有歷史快照註記，
  但後段仍有當前式標題／指引；應局部標明原輪次，並加入固定來源前提下
  H1 已由後續成立的連結，保留 H2／H3 與一般推廣的未證界線。
- STATUS `:172` 的「整個子型未完成」落後於本次 47／75 完成；
  `:170-171`、`:234` 的後續關係及假設狀態亦須更新。
- equal_pair、short_face、long_face 頁首同時寫 subtype 未完成與已完成，
  應把中間輪次日期與最终現況合成清楚的一段後續註記。
- 「原 joint／witness 保持」縮句可精確成「完整 relations 保留；只替換
  指定原分量的整份 witness，其外頂點逐點保持」，並寫明投影角色。

[REVISION_CHECKLIST.md](REVISION_CHECKLIST.md) 提供逐項位置、替換措辭
與驗收方式；[文件子稽核](docs/documentation_audit.md) 保留完整證據。
line numbers 對應截點副本，整合時請以句子定位。歷史正文、當輪停止點、
驗證範圍及 artifact bytes／hash 保持原樣；改現況前綴與導覽，不把
全部舊 frontier 改成 0／0，也不為通過 byte-check 重写歷史證書。

## 重播與保存

以下命令只讀提供的 repo；請把 output 指向獨立稽核目錄。當 repo 在
截點後有新成果，hash 比較可能報新的漂移，需另外記錄，不覆寫舊證書。

```bash
python3 audits/2026-10-04-task-d/replay_checks.py --repo . --output /tmp/task-d-replay --scope all
uv run --with networkx==3.5 python audits/2026-10-04-task-d/semantic_payload_audit.py --repo . --output /tmp/task-d-payload.json
python3 audits/2026-10-04-task-d/identity/audit_identity.py --repo . --output /tmp/task-d-identity
python3 audits/2026-10-04-task-d/projection/audit_projection.py --repo . --output /tmp/task-d-projection
```

[integrity_results.json](integrity_results.json) 比對截點的全部 1,209 份
baseline 文件：副本與共用源文件均無 bytes 差異，HEAD 相同。併行研究
其後新增的 mixed12／mixed22 paths 另列於結果，不納入本報告結論。
獨立報告包自身 hashes 見 [DELIVERY_SHA256.json](DELIVERY_SHA256.json)。
