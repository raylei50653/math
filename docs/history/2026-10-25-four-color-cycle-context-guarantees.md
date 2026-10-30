# 共同條件接口的數學保障整理與發布

2026-10-25。權威來源：[共同條件接口的數學保障](../tools/solver/four_color_cycle_contexts.md#數學保障範圍)。
本次整理已實作操作的紙面論證與停止點，不改求解器、不重建凍結實驗資料。
發布前基準為 `cb5adc6c6b769902dadb5b982c4fadffecbe6c34`；開始時工作樹乾淨，
fetch 後本地與 `origin/main` 相同。

## 整理範圍

- 有限簡單無向圖、同一字面四色及固定色下，可靠候選域、完整原約束與整列接口傳播保持全部整圖解。
- 任意長度中心環在其環邊、實際輻條及當前單點域下有精確局部查詢；弦與外側附件仍由原因子保留。
- 共同三色域奇輪的紙面排除適用任意奇數環長；零消元另要求首次消元前命中並完成查詢且未超限。
- 九點反例保留現有傳播缺口；不推成所有二／三元方法皆不足。樹形接合的充分條件與尚未輸出證書分開。

證據層為紙面不變式、環遞推及既有接合論證；171項測試、96份控制解和40例比較
仍屬原輪有限證據，不因本次整理升為一般完備性或整份 Python 的形式化驗證。
沒有新增 Lean 定理；跨區共同關係仍 OPEN。

## 路由核對

- Updated：共同條件接口報告、四色導覽及 STATUS 對應短索引。
- Reviewed-unchanged：README 使用入口及 HANDOFF 研究線清單仍有效，無研究線增減或排程變更。
- Propagation stop：L1；沒有推升 C₅／W7／J1／J2 父題或改變其停止點。

## 本次驗證

本次執行下列檢查；使用既有測試，不新增只重述實作的測試。

```sh
uv run --with-requirements requirements.txt python -m unittest discover -s tools/tests -p 'test_four_color*.py'
lake build --no-ansi
python3 scripts/check_docs.py
python3 tools/docgraph --include 'docs/**/*.md' check
python3 tools/check_generated_artifacts.py
git diff --check
git diff --cached --check
```

相關單元測試171項通過；Lean build完成8832 jobs，保留既有lint警告。
文件檢查通過（734份Markdown／9740條本地連結）；docs範圍DocGraph通過
（98份文件／386條關係／12族，0 errors／0 notes）。staged artifact policy與
diff空白檢查通過；只暫存上述四份連貫文件。獨立只讀數學審查已完成，
並採納「每張完整表皆非空」的樹形接合前提措辭修正。

原批次40例、normal／seed-17、瀏覽器與凍結來源hash核對本次未重跑，沿用原報告及原收據，
不把單元測試改稱批次語義重播。全工作樹DocGraph本次未重跑，docs通過不外推成全域通過。
推送及遠端CI狀態以本次即時Git與GitHub核對為準。
