# 2026-10-03：ε=2 省略證書與 t=1 全分拆成果整理、發布

使用者要求「整理目前進展 commit + push」。接手基準 `bbd900a`；
fetch 後 `main=origin/main`，工作樹包含 2026-10-02 至 10-03 的連續
省略核心及整型排除成果。本輪整理完整證據包、核對後續涵蓋關係，
以本紀錄連接研究結果、實際重播及發布範圍。提交 SHA 與遠端同步
以即時 Git 為準，本紀錄不自含提交 SHA。

## 進展與證據界線

全部新來源結論保留原報告的有限簡單、有序 induced-C₅ disk 外框、
933／941 完整 Σ、T4 全收、逐非框邊 edge-minimal、ε=2 及唯一
完整 degree-6 root 前提。原分量、原邊、具名有序 contacts、全部
附件、ownership、實際支援、環序及同一字面色框均保留。

| 成果 | 完成範圍及報告 |
| --- | --- |
| t=1 全七分拆整型排除 | [總報告](../c5_excess_two_single_spoke_complete.md)完成 (5)、(4,1)、(3,2)、(3,1,1)、(2,2,1)、(2,1,1,1) 及五 unary；不以無全 degree-4 真子核心代替整型排除 |
| 通用短支援 | [兩／三外部 hubs 引理](../c5_short_support_singleton.md)不限原接點數，迫每份原分量至少兩段跨度；另保留[四接點 pair 獨立證明](../c5_short_support_four_contact.md) |
| t=2 整型排除 | (2,1,1) 由短支援引理六跨度排除；[四 unary](../c5_excess_two_four_unary.md)由固定三點支援排除 |
| t=2、(2,2) 及 t=3、(2,1) | [雙 binary 省略](../c5_excess_two_two_binary.md)及 [binary 省略](../c5_excess_two_binary_omission.md)均全收，兩型無全 degree-4 真子核心；整型仍保留 |
| t=3 spoke＋unary 省略 | [三 unary 共同扇區](../c5_excess_two_three_unary.md)關閉 path／tail，連同前序原 triangle 結果完成該條件分支 |

t=1 原 binary／兩 unary 及 t=2 原 binary／兩 unary 的省略證書
仍一併保留，可獨立重播。新結果為任意大小紙面論證與 Python 固定
必要域、完整 tuple 接合及原邊 minor controls；外部 degree-list／
Gallai 定理與前序 topology 仍是各報告明列依賴。未新增 Lean theorem。

共同下界仍 ε≥2，未證 ε≥3、ε=2 實現、一般候選來源排除、一般
共同出口或 K∞=K≤5。README、STATUS、Kempe 導覽及全線整合頁均已
同步，前序報告頁首標明後續整型涵蓋；歷史正文保留當輪語境。
HANDOFF 的研究線及進行中標記沒有變化，依文件治理維持薄索引。

## 本輪實際重播與產物

16 個新增 checker 均以 `PYTHONHASHSEED=17`、`--check` 比對既有
證書，全部通過；沒有重新產生或覆寫 observations：

```bash
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_three_unary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_binary_omission.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_two_binary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_two_unary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_binary_two_unary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_four_unary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_single_spoke_two_unary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_single_spoke_binary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_five_unary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_binary_three_unary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_ternary_two_unary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_five_contact.py --check
PYTHONHASHSEED=17 python3 scripts/c5_short_support_four_contact.py --check
PYTHONHASHSEED=17 python3 scripts/c5_short_support_singleton.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_ternary_binary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_four_one.py --check
lake build
uv run --with-requirements requirements.txt python tools/artifacts.py status
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

`lake build` 通過 8,831 jobs，只有既有 AttachmentOrder／SymRelabel
linter warnings。大型產物狀態 `ok=114`，沒有 missing／changed／stale。
六份新增 ≥1 MB 證書依既有 MANIFEST／producer fingerprints／依賴與
`.gitignore` 政策保留本機；十份較小證書隨 checker、報告及研究紀錄
提交。大型產物可由 manifest 的 producer 重建，不能把重建當只讀檢查。

文件檢查通過 455 份 Markdown／4,669 個本地連結及 anchors／index／
handoff 契約；DocGraph 通過 62 documents、213 relations、5 families，
零 errors／notes；`git diff --check` 通過。

未重跑歷史全 degree-4 大生成器、全部 Gallai／disk topology、
degree-5／sector 系列、全來源 catalogue、其他出口／repair 全表或
Lean axiom audits。前序依賴沿用原報告證據；`lake build` 不表示本輪
任意大小紙面拓撲已形式化。

## 停止點與跨對話接手

目前窄入口由 [Kempe 導覽](../c5_kempe_guide.md#3-停止點與保留缺口)
維護：ε=2、唯一 degree-6 root、t=2、(2,2) 的整型來源。保留兩份
原 binary、有序原接點、共同色框、全部實際支援及省略身份；停止於
可證整型排除或具名必要殘留，不重開來源圖枚舉。其他 t、兩個
degree-5 roots（含 mixed）及一般來源仍保留。

> 已完成 933／941 固定完整 Σ、edge-minimal C₅ disk 來源、ε=2、
> 唯一 degree-6 root 的全部 t=1 七分拆整型排除，並排除 t=2 的
> (2,1,1) 與四 unary 整型。先讀 `docs/c5_excess_two_single_spoke_complete.md`、
> `docs/c5_short_support_singleton.md` 及 `docs/c5_kempe_guide.md`。
> 16 個新增 checker、Lean build 與大型產物檢查通過，完整發布範圍
> 見本紀錄。紙面＋Python、未 Lean 化，共同 ε≥2 不變；下一窄題
> 是 t=2、(2,2)，省略全收仍不能代替整型排除。
