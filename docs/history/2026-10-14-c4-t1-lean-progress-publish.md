# C4 來源橋、T1 正對切口與具名 Lean 替換整理發布

2026-10-14。依使用者「整理目前進展 commit + push」授權，整理 BASE
`77fbd5da7ba273f0af7c75175dc08376d2282f46` 後的三包連接成果與工具變更。
本提交是共同發布檢查點；原 audit／研究歷史的「未 commit／push」保留當輪語境，
實際提交、遠端同步及工作樹狀態以即時 Git 為準。

## 成果、證據層與停止點

| 來源 | 本次發布的精確成果 | 保留界線 |
| --- | --- | --- |
| [C5→C4 來源橋](../c5_c4_boundary_pivot.md) | 原 G 全部頂點與邊保留，只加外側四-spoke 點；完整 fibres 雙射給 `n_H(ABCB)=y0+y1=0`。正規形／度數使 H 為非 diamond 4-candidate，總點數 k+6；接外部完整≤28總點計算得 `K≤22=K≤5`、三支共同 k≥23 | 紙面＋本地有限控制＋外部計算；未重跑外部枚舉、無新 Lean，無界具名 C4 子類及 `K∞=K≤5` OPEN |
| [T1-CROSSCUT](../c5_c8_peeling.md#t1-crosscut) | 原 no4ct 全域最小來源契約下 h=3⇒p=0，全部 PINCH／BRIDGE 排除，不限單接點數或兩片大小；完整共同支援與安全矩形證書保留 | 紙面＋Python，無新 Lean；RING、h≥4、一般來源縮減 OPEN。剝層自身 k≥19、T2自身 k≥18 與當前共同 k≥23 分開 |
| [Lean 具名首層替換](../lean_named_replacement.md) | 兩方向、A單側、B單側及雙側各一次替換，32個普通 theorem 保十三點外部完整接受關係、原 U 的 J、指定框 P、repair 分類及 r*=4；實際原邊表與既有六份首層圖一致 | 無 `native_decide` 或新增公理；沒有宣稱內部 fibre 數量相等。任意層數接線／ownership、disk 嵌入與全部可用框、一般分類 OPEN |

W5 任取合法輪的私人圈秩至少五、C9-932 的20項較高度數來源及
E-ARC2 的 N1／相鄰 roots／基本 LL-CUT 均保留原契約，不由本次有界結論關閉。

## 本次實際驗證

以下命令在本次發布整理中重新執行；主／獨立 C4 checker 與新 Lean
來源核對另以 `PYTHONHASHSEED=17` 重播。

```bash
python3 -B audits/2026-10-14-c5-c4-boundary-pivot-77fbd5d/controls/check_transfer.py --check
python3 -B audits/2026-10-14-c5-c4-boundary-pivot-77fbd5d/review/check_independent.py --check
python3 -B audits/2026-10-14-t1-crosscut-review-77fbd5d/check_adoption.py --check --negative
python3 scripts/c5_lean_named_repair.py --check
python3 scripts/c5_lean_named_replacement.py --check
lake build --no-ansi
lake env lean Math/NamedRepairReplacementAudit.lean
python3 tools/audit_archive.py verify --artifacts
UV_CACHE_DIR=/tmp/math-publish-uv-cache uv run --with-requirements requirements.txt python -m unittest discover -s tools/tests -p 'test_*.py'
python3 scripts/check_docs.py
python3 tools/docgraph --include 'docs/**/*.md' check
python3 tools/docgraph check
git diff --check
```

- C4 主 checker：132實圖、528完整 fibres、1,024 supports 通過；獨立
  430,080 literal查詢、1,080 cap lifts、W5／icosahedron控制及負控制通過。
  24檔 SEAL 的完整 inventory、bytes、SHA256 一致；有限真正目標來源仍0。
- T1：161 sealed files、14 BASE inputs、41 manifest、64 cases／701,020矩形／
  59,156份 P lifts、7種 disk controls、12項負控制核對通過。
  本次未重算所有安全矩形；完整普通／seed17重建沿用原封存紀錄。
- Lean：8,832 jobs通過；新模組無警告，既有 linter warnings沿用。
  普通／seed17來源核對輸出一致；32項審計逐名與保存 artifact 相同，
  公理聯集恰為 `propext`、`Classical.choice`、`Quot.sound`，無
  `sorryAx`／`Lean.ofReduceBool`。
- Archive含MANIFEST核對：3,484原路徑、1,980 unique blobs全通過。
  本提交只新增T1的97份封存路徑及57個blobs，既有archive記錄不變。
- 工具測試：94 tests通過。Generated artifacts workflow補Python 3.14與
  requirements安裝，符合既有測試依賴；本次沒有新增測試或修改依賴鎖定。
- 文件檢查：680份Markdown、8,831個本地連結，索引、anchors與導覽現況卡通過；
  正式docs DocGraph：96份文件、365條關係、12個families，零errors／notes。
  全樹DocGraph仍FAIL：68項 frozen／scratch duplicate-ID；保留原證據，
  不將正式docs PASS稱作全樹PASS。

生成物政策在stage後執行 `python3 tools/check_generated_artifacts.py` 通過：
4,947 indexed files、8份有明列例外的大檔、166 registered outputs；
`git diff --cached --check` 通過。遠端CI狀態另以GitHub為準。
未重播外部十億級枚舉、無關大型生成器或舊來源分類，未更新Lean／mathlib鎖檔。

## 文件傳播與發布範圍

Updated：C4來源入口及證據、C8權威頁、no4ct交接、Kempe／Lean／兩點重疊導覽、
STATUS直接索引；degree-bound／apex、共面／K15及repair consumers補有日期的後續入口。
修正當前索引中的「十六內點以上／K≤16仍OPEN」及「RING只沿用k≥19」，
區分當輪局部界與當前共同k≥23，保留原論證與凍結證書。

Reviewed-unchanged：HANDOFF研究線與活躍tags；跨線synthesis的一般主命題仍OPEN，
沒有因本次有界計算或具名首層形式化而改變無界closure。
README核對新來源／模組與CI使用入口，未新增研究線。

Propagation stop：直接父主題／consumers的L2及已改變的使用入口。
發布白名單只含上述報告、Lean／checker／artifact、兩包audit、T1 archive增量、
README／STATUS／導覽／歷史與相關workflow；不刪改歷史payload、不展開新枚舉。
