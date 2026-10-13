# 2026-10-03：ε=2 四-spoke 七輪進展整理與發布

使用者要求「整理目前進展並 commit + push，過程中有發現可以記錄」。
接手基準 `b63a096`，工作目錄 `/home/ray/developer/ai/math`；本地
比 `origin/main` 的 `722bfa6` 多一筆已驗證、尚未推送的雙 root 提交。
本次整理後續七輪報告、checker／helper、產物登錄與交接入口，
連同前序本地提交發布；提交 SHA 與遠端狀態以即時 Git 為準。
沒有重開來源圖枚舉，沒有新增來源排除或 Lean theorem。

## 完成範圍與證據層

共同前提為固定完整 Σ=933／941 或其整圖 D₅ 像、每條非框邊
Σ-critical、指定有序 induced-C₅ disk 外框、有效內部連通、ε=2。
前序已排除唯一 degree-6 分支；本批限定相鄰兩個完整 degree-5
roots、恰一份原 mixed，其餘有效內點完整 degree 四。原分量、
contacts、全部實際 attachments／supports、ownership、嵌入環序
及同一字面四色框始終保留。

| 本批報告 | 最新完成範圍與後續關係 |
| --- | --- |
| [兩原 unary](../c5_excess_two_mixed_core_four_spoke_singles.md) | (3,1)、mixed-(1,1) 加兩單接點 unary：共同支援六跨度來源排除，含 root 交換 |
| [一原 binary](../c5_excess_two_mixed_core_four_spoke_binary.md) | 完整 leaf 反像保留 116／256 必要域；後由原 star 及同列端點 hub 全排，當輪證書保留 |
| [原 star](../c5_excess_two_mixed_core_four_spoke_star.md) | 116／256 縮為 32／64，276 個 K₃,₃ subdivisions；殘留已由同列 hub 涵蓋 |
| [同列端點 hub](../c5_excess_two_mixed_core_four_spoke_hubs.md) | 原 32／64 全排，完成 mixed-(1,1) 加一原 binary；192 queries、10,752 完整 U schemas、2,208 tightness 控制 |
| [原三接點](../c5_excess_two_mixed_core_four_spoke_ternary.md) | mixed-(1,2) 加一 unary 全排；20／60 框架、50 完整 degree 圖、1,500 joints／24,000 fibres |
| [原四接點](../c5_excess_two_mixed_core_four_spoke_quaternary.md) | mixed-(1,3) 無 unary 全排；20／60 框架、80 完整 degree 圖、2,400 全圖貪婪 witnesses；結合前三子型完成 (3,1) 全 incidence 分拆 |
| [共用原 pair](../c5_excess_two_mixed_core_four_spoke_equal_pair.md) | (2,2)、mixed-(1,1) 加各側一 unary：同 pair 的 7／9 份全排，仍有 40／66 unequal-pair 必要框架；36 完整 degree 圖、2,520 joints／40,320 fibres |

**共同下界仍是 ε≥2，ε≥3 未證。** 任意大小來源排除由各報告
紙面證明及明列外部引理承擔；Python 保存完整固定域 relations、
同框 joints、空 fibres、全染色 witnesses 與具名 minors。
必要框架不表示 disk 實現；完整 degree 控制圖也不自動滿足候選
Σ、criticality 或封閉幾何。一般出口及 K∞=K≤5 未證。

## 整理時核對的發現

新增 [整理 audit](../../scripts/c5_excess_two_four_spoke_progress_audit.py)
及 [小型證書](../../artifacts/c5_excess_two_four_spoke_progress_audit/observations.json)，
只核對既存證據，不枚舉來源圖、不刪除必要框架。

1. **(3,1) 封閉的範圍可由原 degree 預算核對。** 扣除 ab 與
   spokes 後兩 root 剩 incidence=(1,3)。唯一 mixed 的 a 側只能
   用一條 incidence，b 側可以用一、二、三條；其餘原 unary
   contacts 的分拆恰為下表四份。這是 incidence 完備性核對，
   各份來源排除仍由原報告承擔。

| 原 mixed incidence | a 側 unary 分拆 | b 側 unary 分拆 | 最新狀態 |
| --- | --- | --- | --- |
| (1,1) | 空 | (1,1) | 兩 unary 六跨度全排 |
| (1,1) | 空 | (2) | 同列端點 hub 全排 |
| (1,2) | 空 | (1) | 三接點身份全排 |
| (1,3) | 空 | 空 | 四接點 leaf-slack 全排 |

2. **(2,2) 的共用 pair 結論只覆蓋第一份 incidence 子型的一部分。**
   原剩餘 incidence=(2,2)，唯一 mixed 的四份具名配置是
   `(1,1)` 加各側一 unary、`(1,2)` 加 a 側一 unary、
   `(2,1)` 加 b 側一 unary、`(2,2)` 無 unary。後兩個相反側型
   可整圖交換 roots，但不可獨立正規化分量。共用 pair 排除尚未
   封閉第一份，更未封閉整個 (2,2)。

3. **unequal pairs 可按原 spoke 支援的交集大小分組。** audit
   逐份核對原 source index、root order、全部骨架邊與 apex rotation，
   保存全部 106 份具名 records，不以統計取代原 relations。

| 保留的原 pair 關係 | 933 | 941 | 具名代表：933／941 source indices |
| --- | ---: | ---: | --- |
| 只共用一個原框點 | 26 | 48 | 01／02：97／133 |
| 兩份 pair 不相交 | 14 | 18 | 01／23：101／139 |
| 合計 | **40** | **66** | 均保留原 roots=(5,6) 的命名 |

   此表是必要框架分類，不聲稱兩組具有相同的實際 C 支援包絡、
   可實現性或完整 tuple 關係。原 01／02 仍為選定的下一窄入口。

4. **兩 unary 的舊 byte-check 有一份純文件 hash 漂移。** 本次
   實際執行原 `singles --check` 未通過；唯讀重算並比較其全部
   JSON 數學 payload 後，唯一差異是 `input_sha256` 中的
   `docs/c5_excess_two_mixed_core_leaf_fibers.md`。記錄 hash 為
   `e79485da8e52529b339c9f782fca7cde7551ad635417b48fc4d95f7cb6c29cb5`，
   目前為 `e5e4155c680814c94a24df638240be5d3a5f33e1a3638333330c4c26f9747981`。
   所有非文件 input hashes、全部 relations／fibres／witnesses、
   支援表及 summary 均一致。新 audit 將這項漂移明示為唯一允許
   的差異；原嚴格 byte-check 維持，原 singles artifact 未覆寫。
   這不抹去既有 single-spoke 三份及 two-two 一份歷史文件漂移。

## 本次實際驗證與產物

六份本批 checker 的 `PYTHONHASHSEED=17 --check` 逐 byte 通過；
第七份 singles 的數學 payload／非文件 inputs 由新 audit 完整
重算相同，**原 singles byte-check 仍不通過**，不能寫成七份均通過。
前序 leaf 與短支援 checker 另重播通過。NetworkX 使用本地 cache
中的 pinned 3.5，Python 3.14.7；實際命令：

```bash
PYTHONHASHSEED=17 uv run --offline --with networkx==3.5 python scripts/c5_excess_two_mixed_core_four_spoke_binary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_four_spoke_binary_star.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_four_spoke_binary_hubs.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_ternary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_quaternary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_equal_pair.py --check
PYTHONHASHSEED=17 uv run --offline --with networkx==3.5 python scripts/c5_excess_two_four_spoke_progress_audit.py --check
PYTHONHASHSEED=17 uv run --offline --with networkx==3.5 python scripts/c5_excess_two_mixed_core_leaf_fibers.py --check
PYTHONHASHSEED=17 python3 scripts/c5_short_support_singleton.py --check
lake build
python3 tools/artifacts.py status
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

原失敗命令為
`PYTHONHASHSEED=17 uv run --offline --with networkx==3.5 python scripts/c5_excess_two_mixed_core_four_spoke_singles.py --check`。
新 audit 的生成只寫新小型 artifact；上述 `--check` 不覆寫產物。

`lake build` 通過 8,831 jobs，只有既有 AttachmentOrder／SymRelabel
linter warnings，沒有新增 Lean theorem。本批七份大型 observations
共 **158,056,468 bytes**，依政策保留本地；Git 提交其 producers、
helpers、MANIFEST 的大小／SHA256／fingerprints／依賴次序及
`.gitignore`。新小型 audit 證書 **150,807 bytes**，直接進 Git，
保留舊大型產物。其 SHA256 為
`a69d319fdde895718af954e8400c77d7df2f149b0b60d04aa5a1f1cdfc69cd70`。
文件檢查通過 **500 份 Markdown／5,129 個本地連結**，anchors、
index、HANDOFF 全通過；DocGraph 通過 **62 documents／213 relations／
5 families**，零 errors／notes；大型產物 `ok=132`，無 missing／
changed／stale；`git diff --check` 通過。這些檢查不形式化紙面 topology。

前序 `b63a096` 九輪已在該整理紀錄驗證，本次只重跑其中 leaf；
其餘八份、唯一 degree-6 分拆、歷史來源 catalogue、R-series、
weak-deletion／Kempe closure、Lean axiom audit 及本批預設 hashseed
未重跑，不宣稱全倉研究重新驗證。README、STATUS、Kempe 導覽、
全線整合頁與 singles 後續說明同步；HANDOFF 的研究線與 tags 未變，
依治理維持薄索引。

## 停止點與貼用摘要

```text
cwd=/home/ray/developer/ai/math；先讀docs/HANDOFF.md、docs/STATUS.md、
docs/c5_kempe_guide.md及本整理發布紀錄，再查即時Git。
前序本地b63a096與後續四spoke七輪已納入本次commit+push。
固定完整Σ=933/941、edge-minimal induced-C5 disk下共同ε≥2；唯一degree6已全排。
相鄰唯一mixed：全部(4,4) q-core、五spoke及四spoke(3,1)全incidence已排。
(2,2)、mixed(1,1)+各側一unary：共用pair排7/9，unequal保留40/66。
unequal中共一框點26/48，不相交14/18；全106具名骨架及rotations保存於新audit。
下一入口原a5/b6、spokes01/02、indices97/133，root交換111/153。
保留同一原C/U/V、R_C(x,y)及六點joint，先分析C所在face的實際支援包絡。
不以marginals、整sector或獨立色框代替；不重開來源圖枚舉。
六份新byte-check通過；singles唯一leaf文件hash漂移，完整數學payload新audit通過。
原singles嚴格byte-check仍失敗且舊artifact保留；前序leaf、短支援及lake build通過。
其他(2,2) incidence、較少spokes、單省略、原(5,5)、多mixed/no-mixed/非相鄰保留。
紙面+Python；ε≥3、一般出口、新Lean theorem、來源實現及K∞=K≤5未證。
```
