# 四色完整消元證明與流程優化整理發布

2026-10-25。所屬研究線：[四色求解導覽](../four_color_guide.md)。
發布前基準為 `bcfae258dd81e6eeec99a1de999a13f35b8b7b38`；實際發布身份以Git及遠端核對為準。

## 本次整理範圍

- [完整消元與回寫的完備性證明](../four_color_completeness.md)：任意有限簡單無向圖、
  部分固定色、全部含點因子的精確投影、可靠且有限次傳播、倒序共同回填及空接口。
  在給足資源的演算法前提下，有解必可構造、無解必判否；紙面證明與Python形式化驗證分開。
- [流程優化](../four_color_flow_optimization.md)：增量傳播、共同接口查詢重用及完整因子起始的
  精確桶枚舉，同四十例超限10→1。
- [儲存容量](../four_color_memory_optimization.md)：生成表及完整紀錄容量可獨立設定；
  百萬列容量下同四十例27可解／13無解／0超限。
- [RAM索引](../four_color_ram_indexes.md)：完整接口分組、涵蓋因子索引及穩定配對；
  同四十例求解15.27→12.82秒、求解後峰值103.6→106.2 MiB，屬當輪有限比較。

原有流程、容量及RAM實驗的來源快照、失敗／超限基準與驗證收據原樣發布。
六份超過1 MB的JSON以exact frozen exceptions登記bytes／SHA；不把目前程式當成歷史產生器。
報告補明目前行為重播與凍結歷史重播的差別，沒有改寫既有證據。

## 本次實際核對

[本次工具測試](2026-10-25-four-color-completeness-publication/tools-tests.log)通過327項，
另有[四色測試](2026-10-25-four-color-completeness-publication/coloring-tests.log)233項通過。
兩份命令均使用 `uv run --with-requirements requirements.txt python -B -m unittest discover`，
分別指定 `test_*.py` 與 `test_four_color*.py`。

本次[只讀證據核對](2026-10-25-four-color-completeness-publication/artifact-audit.json)通過：
280份完整gzip紀錄、160份worker reports、309份不同來源快照及47份目前來源綁定。
其中267份為baseline／optimized，另42份為incremental；不同收據間共393次快照hash核對，
不把重複核對當成新增來源檔。[核對程式](2026-10-25-four-color-completeness-publication/audit_artifacts.py)
可在根目錄重跑：

```bash
python3 docs/history/2026-10-25-four-color-completeness-publication/audit_artifacts.py --root . --out /tmp/four-color-publication-audit.json
```

確定性重播、時間／RSS數字沿用原報告當輪收據，本次沒有重跑大批效能或normal／seed-17實驗。
未修改Lean來源，也未重跑Lean build；本次紙面演算法證明沒有新增Lean定理。
[文件檢查](2026-10-25-four-color-completeness-publication/docs-check.log)通過743份Markdown的
本地連結及導覽／索引／錨點；[正式docs DocGraph](2026-10-25-four-color-completeness-publication/docgraph-docs.log)
通過98份文件、386條關係、零錯誤。
[全工作樹DocGraph](2026-10-25-four-color-completeness-publication/docgraph-whole-tree.log)仍報72項
歷史快照／scratch的重複ID，保留失敗結果，不混稱全域通過。
[staged artifact policy](2026-10-25-four-color-completeness-publication/artifact-policy.log)通過：
193份大型檔案均有精確例外、166份可重建輸出已登記；
[staged whitespace](2026-10-25-four-color-completeness-publication/staged-whitespace.log)通過。

## 收尾與上游核對

- Closure scope：完整關係消元及可靠傳播契約下的有限終止、有解／無解判定、共同回寫，
  權威來源為本次完備性證明；效能仍限原四十例。
- Updated：四色導覽、STATUS、約束引擎與保證缺口入口，明確區分完整消元完備性與一般消元前傳播義務。
- Reviewed-unchanged：README／HANDOFF的研究線入口未改；其他C₅／W7／J1／J2來源義務未因求解器定理改變。
- Remaining OPEN：一般免消元充分性、固定小接口充分性、一般效率與整份Python形式化驗證。
- Propagation stop：停於本研究線及直接使用者；沒有跨線來源排除或全域研究主張需要更新。

發布後的local／tracking／remote SHA與遠端CI狀態分別核對；push成功不代表CI已完成。
