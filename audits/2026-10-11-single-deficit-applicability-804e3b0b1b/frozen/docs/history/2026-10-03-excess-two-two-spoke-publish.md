# 2026-10-03：ε=2 t=2 全分拆成果整理與發布

使用者要求「整理目前進展 commit + push」。接手基準 `1d32997`；
fetch 後 `main=origin/main`，工作樹包含 t=2 研究的三份新 checker、
產物、四份報告及相關索引。本輪核對完整證據包與後續涵蓋關係，
整理後提交並推送。提交 SHA 與遠端同步以即時 Git 為準，本紀錄
不自含提交 SHA。

## 進展與證據界線

在 933／941 固定完整 Σ（含整圖 D₅ 像）、edge-minimal induced-C₅
disk 來源、ε=2、唯一完整 degree-6 root、其餘有效內點完整 degree 四
的前提下，[t=2 合成報告](../c5_excess_two_two_spoke_complete.md)完成
全部五分拆；連同前序 t=1，得到 **t∉{1,2}**。

| 分拆 | 完成範圍 |
| --- | --- |
| (2,2) | [兩原 binary／首橋](../c5_excess_two_two_spoke_binary.md)：40 具名扇區位置、400 查詢全排；純 pair 層留下的 20 份完整十列抽象控制保留，加入同一首橋共用 β 及局部 residual 跨列搬運後全排 |
| (3,1) | [Ternary／unary](../c5_excess_two_two_spoke_ternary.md)：復用 t=1 singleton profiles，16 具名位置、107,296 profile 對全無目標，不需 D 身份篩選 |
| (4) | [四接點／共同 active forest](../c5_excess_two_two_spoke_four.md)：200 查詢全排；100 份三禁色 K₅、100 份固定兩末端袋支援不能並排 |
| (2,1,1)／四 unary | 前序短支援引理的固定跨度下界分別迫六／八跨度，超出五段框邊；原省略與四 unary 證書保留 |

原分量、有序 contacts、全部原邊與實際 attachments、ownership、
共同扇區與真實支援端點，以及完整 relations 的同一字面色框均保留。
β 只在同一列同一首橋兩端共用；局部 E 不等於整份分量的 F。
任意大小與 topology 由紙面 Gallai／原 tethers／crosscut 論證承擔，
Python 核對固定必要域、原 minor controls 及完整 ordered-tuple 接合。

共同下界仍 **ε≥2**，未提高至 ε≥3；其他 t、雙 degree-5 roots
（含 mixed）、一般來源／單側及共同出口、K∞=K≤5 仍保留。未新增
Lean theorem，`lake build` 不表示本輪紙面 topology 已形式化。

## 本次發布重播與產物

以下六份 checker 均以 `PYTHONHASHSEED=17`、`--check` 重播通過；
直接比對保存的證書，沒有重新生成或覆寫 observations：

```bash
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_two_spoke_binary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_two_spoke_four.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_two_spoke_ternary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_short_support_singleton.py --check
PYTHONHASHSEED=17 python3 scripts/c5_single_spoke_first_bridge.py --check
PYTHONHASHSEED=17 python3 scripts/c5_single_spoke_residual_locality.py --check
lake build
uv run --with-requirements requirements.txt python tools/artifacts.py status
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

`lake build` 通過 8,831 jobs，僅有既有 AttachmentOrder／SymRelabel
linter warnings。大型產物檢查 `ok=116`，沒有 missing／changed／stale。
binary（3,455,178 bytes）與 four（1,278,618 bytes）沿用 MANIFEST、
producer fingerprints 與生成的 `.gitignore` 政策保存本機，可由各
producer 重建；ternary（455,240 bytes）直接提交。重建會寫產物，
不能當只讀 replay。

本次只重跑上述六份 checker、Lean build 與產物／文件檢查。
前序 t=1 其他整型、binary 省略、double-spoke 省略、框弧／跨列
helpers 的重播沿用[研究輪次紀錄](2026-10-03-excess-two-two-spoke-complete.md)，
未重跑全部歷史 Gallai／degree-4 分類、全來源 catalogue、R-series、
weak-deletion／Kempe closure 或 Lean axiom audit。

README、STATUS、Kempe 導覽、全線整合頁與舊 t=1／binary 省略報告
同步後續涵蓋；研究紀錄保留當時未提交語境，頁首連到本次發布。
HANDOFF 的研究線與進行中標記沒有變化，依文件治理維持薄索引。
文件檢查通過 461 份 Markdown、4,744 個本地連結及 anchors／index／
handoff；DocGraph 通過 62 documents、213 relations、5 families，
零 errors／notes；`git diff --check` 通過。

## 停止點與跨對話接手

下一窄題由 [Kempe 導覽](../c5_kempe_guide.md#3-停止點與保留缺口)
維護：**t=3、(2,1) 整型來源**。保留兩原分量、有序 contacts、
三條 spokes 的共同扇區、實際支援端點及同一色框，檢查原首橋／
局部 residual 工具是否適用；停止於可證整型排除或具名必要殘留，
不重開來源圖枚舉。原 binary 省略全收仍不能替代整型反證。

> 在 933／941 固定完整 Σ、edge-minimal induced-C₅ disk 來源、ε=2、
> 唯一 degree-6 root 的前提下，t=1、t=2 全部分拆已整型排除，
> 得 t∉{1,2}。先讀 `docs/c5_excess_two_two_spoke_complete.md`、
> `docs/c5_kempe_guide.md` 與本發布紀錄。三份新增及三份直接依賴
> checker 的 hashseed 重播、Lean build、產物與文件檢查通過。
> 完整證據包一併提交推送；紙面＋Python、未 Lean 化，共同 ε≥2
> 不變。下一窄題是 t=3、(2,1) 整型來源；保留同源 contacts、
> 實際支援、共同扇區及色框，不重開來源圖枚舉。
