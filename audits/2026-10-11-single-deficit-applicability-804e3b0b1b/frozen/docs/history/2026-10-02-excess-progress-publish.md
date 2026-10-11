# 2026-10-02：933／941 excess 進展整理與發布

使用者要求「整理目前進展 commit + push」。接手基準 `b97b107`；
`main` 有一個尚未推送的全線整合／關係階數 commit，以及五組未提交的
941／ε=2 成果。本輪核對現行 HANDOFF、STATUS、文件治理與原報告，
整理連結及發布範圍，重播後將連續成果一併提交、推送至 `origin/main`。
精確 commit 與遠端狀態以 Git 為準；本紀錄不自含提交 SHA。

## 進展與證據界線

全部來源結論保留原報告的有限簡單 induced-C₅ disk、指定有序外框、
完整 Σ、T4 全收與逐非框邊 edge-minimal 前提，亦保留整圖共同 D₅／S4
搬運、原分量身份、具名接點、實際附件及完整有序關係。

| 成果 | 已完成範圍 | 報告 |
| --- | --- | --- |
| 933／941 共同 ε≥2 | 941 的 ε=1、t=2／3 經原接點關係保持及全部具名接回排除，接上既有 t=1；933 沿用四容量子覆蓋下界 | [Two-spoke](../c5_941_two_spoke.md)、[three-spoke](../c5_941_three_spoke.md) |
| ε=2 雙 spoke 省略分支 | 唯一 degree-6 root；刪兩條原 spokes 仍拒絕列的條件分支，148 marked cores／888 次接回全排除兩候選 | [雙 spoke](../c5_excess_two_double_spoke.md) |
| ε=2、t=2 spoke＋unary 省略分支 | 完整五接點接合保留任意大小原 V；592 次接回、5,920 次候選比較全部排除 | [t=2 spoke＋unary](../c5_excess_two_spoke_unary.md) |
| ε=2、t=3 triangle root 的同種省略 | 完整四接點接合及共享省略限制；11,940 次比較全排除，兩色存活留下的 1,254 個由同一 binary 省略圖排除 1,200、雙 spoke 省略排除 54 | [t=3 triangle](../c5_excess_two_three_spoke_unary.md) |

任意大小涵蓋及共享省略論證是紙面推論，沿用全 degree-4 分類、外部
degree-list 定理及既有拓撲證據；Python 重播驗證固定必要域及具名
tuple／完整染色 witnesses。沒有新 Lean theorem，沒有證 ε≥3、ε=2
實現、一般候選來源排除、一般共同出口或 `K∞=K≤5`。

既有 `b97b107` 的全線整合與關係階數成果亦在此次推送範圍，沿用
[原紀錄](2026-10-02-c5-research-synthesis.md)，並重播其獨立 checker。
README、STATUS、Kempe 導覽及前序報告的後續入口已連接；HANDOFF
研究線與 tags 沒有變動，依文件治理保留薄入口。

## 本輪實際重播

以下九個 Python checker 全部通過，均以 `--check` 比對既有證書，
沒有重新產生或覆寫 artifact；最新 t=3 checker 使用另一 hash seed：

```bash
python3 scripts/c5_941_two_spoke.py --check
python3 scripts/c5_941_three_spoke.py --check
python3 scripts/c5_excess_two_double_spoke.py --check
python3 scripts/c5_excess_two_spoke_unary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_three_spoke_unary.py --check
python3 scripts/c5_941_single_spoke.py --check
python3 scripts/c5_excess_one_subcovers.py --check
python3 scripts/c5_independent_support_capacity.py --check
python3 scripts/c5_relation_arity_audit.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
uv run --with-requirements requirements.txt python tools/artifacts.py status
git diff --check
```

`lake build` 通過 8,831 jobs，只有既有 AttachmentOrder／SymRelabel lint。
最終文件檢查涵蓋 428 份 Markdown／4,384 個本地連結，anchors、索引與
HANDOFF 契約均通過。
DocGraph 為 62 documents、213 relations、5 families，零 errors／notes；
artifact 狀態 `ok=108`，沒有 missing／changed／stale。
新增五份大型證書依既有政策保留本機，以 manifest 的檔案 SHA、producer
fingerprints／依賴及 `.gitignore` 登錄，checker 與報告一併發布。

未重跑原全 degree-4 大模板生成器、分叉分類、degree-5／sector 系列、
其他出口／repair 全表、cell enumeration 或 Lean axiom audits。
`lake build` 不形式化本輪紙面拓撲與任意大小化約。

## 精確停止點與接手

當前入口由 [Kempe 導覽](../c5_kempe_guide.md#3-停止點與保留缺口)維護。
下一個窄問題是同一 ε=2、唯一 degree-6 root、t=3 的 spoke＋unary
省略分支，改限 r 位於全 degree-4 核心的 path／tail。保留原 G−r 的
U₁、U₂、V 三份 unary、全部附件、三條 spokes 與共享省略身份；若需
縮路徑，另證原 (r,x,y,v) 關係保持，不能沿用 triangle 的 398 位置涵蓋。
其餘省略型、無全 degree-4 真子核心及兩個 degree-5 roots（含 mixed）保留。

> 目前 933／941 均已證 ε≥2，並排除三個明列的唯一 degree-6 條件分支。
> 最新報告是 `docs/c5_excess_two_three_spoke_unary.md`，重播
> `python3 scripts/c5_excess_two_three_spoke_unary.py --check`。
> 下一題是 t=3 path／tail root 的同源省略限制；紙面＋Python，未 Lean 化。
