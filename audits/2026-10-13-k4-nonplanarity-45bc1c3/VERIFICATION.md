# K₄ 實驗驗證紀錄

2026-10-13。完整前提、效果及信任界線見 [權威報告](../../docs/k4_nonplanarity.md)。
BASE 為 `45bc1c3dc9dacaee1b10df9d64f1c6a27bb0e954`。
當時工作樹已有其他研究變更，初始狀態保存在 `initial_status.txt`；
本輪輸入 byte-for-byte 凍結，沒有重建舊 catalogue 或修改舊證書。
執行期間其他工作使 live HEAD 變為 `50d5474f2446403f3b3001d5943571184c8c9936`；
實驗仍使用 BASE.json 指定的 frozen bytes，七份輸入在重播時亦未出現 live byte drift。
本輪沒有 commit、push 或 stage。

實際執行與結果：

| 檢查 | 結果 |
| --- | --- |
| `python3 -m unittest tools.tests.test_k4_nonplanarity` | 9 項通過；分散附件及損壞證書拒絕 |
| `experiment.py --check`，NetworkX 3.5 | 2,258 原圖／apex 記錄逐份重播一致；793 正證書核對原邊；零平面誤報 |
| `misses.py --check`，NetworkX 3.5 | 76 個 Atlas 漏判重播一致；25 有 K₅ minor、51 無，其中 12 有字面 K₄ |
| CLI `603_graph.json --output .../603_certificate.json` | `triggered and holds`，輸出新證書 |
| CLI `--check .../603_certificate.json` | 原圖 K₅ minor PASS，checker 無平面性 oracle |
| `python3 -m py_compile` 四份新增 Python | 通過 |
| `python3 scripts/check_docs.py` | 通過；654 Markdown、8,177 本地連結（首次執行快照） |
| `python3 tools/docgraph --include 'docs/**/*.md' check` | 通過；62 文件、213 relations、5 families |
| `python3 tools/docgraph check` | **失敗**：62 duplicate-id；audits／scratch 凍結副本重複 ID，本輪 frozen 文件也保留原 ID，未刪歷史或改 frozen bytes |
| `git diff --check` | 通過 |

計時為七輪相同 Atlas 全批實圖，final code 的 `benchmark.final.json` 為報告引用資料：
K₄ 23.17 ms，直接完整檢查 147.13 ms，先 K₄ 再 fallback 153.29 ms（中位數）。
`benchmark.json` 保留初次探索計時，當時尚未補 certificate 整數 ID 校驗及 fallback 計時；
它沒有用來支撐最終速度宣稱。小圖效能不外推至大圖。

獨立 read-only reviewer 以組合枚舉＋NetworkX 分量求解，重得 Atlas 161／237、
平面零誤報、289＋10 正控制全命中、603 實際 Q/H 證書，及 76 漏判的 25／51 分類。
review 指出 certificate 布林／浮點數 ID 可利用 Python equality 等同整數，
已補精確整數型別檢查，final code 重播及反向控制通過。

Closure scope：只完成既有充分判準的工具與固定域效果研究。
Updated：新增專題報告、偵測器、證書、State guide 與 STATUS 入口。
Reviewed-unchanged：既有 K4 block 紙面定理、Cell flip、Sector 的前提及停止點。
Remaining OPEN：完整平面性判定的結構覆蓋、一般 K₄ minor 與 K₃,₃ 偵測；未做 Lean。
Propagation stop：L1；不提升 C₅ 原來源排除或完整 Σ 結論。

## 本地提交封裝

使用者後續授權 `commit`，提交只包含 K₄ 工具、測試、報告、frozen 證據與
兩個共享索引中的 K₄ 條目；同時進行的 Cell 翻邊與分類工作保留在工作區。
603 的報告連結指向已凍結實圖，無需依賴尚未提交的翻邊報告或工具。

依現行大型 generated-file 規則，兩份大型 JSON（共 10,375,358 原 bytes）
追加到 ARCHIVE，只有一個新 blob（194,509 compressed bytes），另一份去重重用
已提交的 blob。原 2,482 個路徑與 1,546 個 blob records 逐項保持。
新 checkout 先使用 `python3 tools/audit_archive.py restore --artifacts`，再依權威報告重播。
原 bytes、frozen SHA-256、當輪比較及失敗紀錄保持。

從 staged index 匯出獨立 checkout，核對 23 項 MANIFEST，逐 byte 還原本輪兩份
大型證據及文件直接引用的既有封存路徑；9 項測試、2,258 份比較與 76 份漏判分類
全部重播通過。索引大型產物規則、正式 docs DocGraph 及 cached diff whitespace 通過。
read-only reviewer 核對 28 檔提交範圍，兩個共享索引各只新增一條 K₄ 記錄。

隔離 checkout 的完整文件導航檢查報 18 個既有缺路徑，涉及
`n45-high1-supervision/REPORT.md`、`n45-low2-supervision/REPORT.md`、
`n45-pa/REPORT.md` 與 `n45-h3a/frozen/authority/common-contract.md`。
以原 HEAD 的 STATUS／State guide 對照、移除本輪新報告後，仍為相同 18 項；
因此本輪沒有新增缺路徑，亦未把本地工作區的通過結果稱為 clean-checkout 全域通過。
