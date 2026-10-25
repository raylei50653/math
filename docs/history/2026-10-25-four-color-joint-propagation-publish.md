# 九點共同限制與自動傳播整理發布

2026-10-25。入口：[四色實驗導覽](../four_color_guide.md)。
發布前基準 `f823b2fb4ea1f8d62bc8b25e852d1f9cabbdf187`；fetch後本地與`origin/main`相同。
本次依使用者要求，整理並發布本對話連續三輪的程式、文件、完整來源及有限證據。

## 結果與邊界

- [部分輻條搜尋](../four_color_partial_spokes.md)補上指定九點固定色的零消元判否；
  四十例模式為17可解／13無解／10工作超限，超限保留為未判定，歷史模式仍為預設。
- [共同限制登記](../four_color_joint_constraints.md)證明九個互異原頂點及21條必要原邊
  迫`u=v=h`，本例為`0=6=9`；保存全部64份三元fibres，含60空列及四列各12份完整延伸。
- [自動找型與主傳播](../four_color_joint_propagation.md)將同一必要三元表接入主因子網路；
  未固定主例在事件1推出等色表，首次消元在事件24，仍未選共同字面色。
  30份條件、兩模式60份完整執行，3,168份原邊解記錄全保留；原主例48／48份解保留。
- 異色固定及額外`0–6`原邊例皆由4次消元提前到0次；額外原邊例另使用完整接口交集。
  必要表非空不當成完整目標圖有解，沒有一般跨區完備性、效率或新Lean定理的宣稱。

## 整理範圍與來源

共用solver／CLI／viewer與三輪證據作一個連貫提交。README補新選項，導覽與STATUS反映
目前停止點；HANDOFF已核對，研究線及進行中tag不變，因此不改動。
Propagation stop為L1；不改其他C₅／W7／J1／J2研究線或推升四色定理主目標。

[本次只讀custody核對](2026-10-25-four-color-joint-publication/custody.json)保存217份新產物的hash。
三輪54份來源快照均與各自當輪摘要相符，最新19份也與現況程式相符；舊輪共用程式的
預期後續變動不回寫到歷史快照。140份報告連結的gzip執行及另存未固定控制核對通過。
唯一新增大於1 MB的JSON為部分輻條摘要，已登記2,985,056 bytes及精確SHA256例外。

## 本次實際驗證

```sh
.venv/bin/python -m unittest discover -s tools/tests -p 'test_*.py'
lake build --no-ansi
python3 scripts/check_docs.py
python3 tools/docgraph --include 'docs/**/*.md' check
python3 tools/check_generated_artifacts.py
git diff --check
git diff --cached --check
```

Python 3.14.8、NetworkX 3.5、NumPy 2.4.3、rustworkx 0.17.1；本地完整工具測試289項通過，
保存[工具測試紀錄](2026-10-25-four-color-joint-publication/tool-tests.log)；
[Lean build](2026-10-25-four-color-joint-publication/lean-build.log)完成8832 jobs，保留既有lint警告。
文件檢查通過（738份Markdown／9796條本地連結）；docs範圍DocGraph通過
（98份文件／386條關係／12族，0 errors／0 notes）。staged artifact policy通過
（10112份索引產物、187份大型例外、166份已登記輸出），240份暫存檔案符合連貫白名單；
staged及工作樹空白檢查皆通過。

各輪normal／seed-17批次與完整解核對沿用研究當輪收據，發布輪未重新生成批次；
本輪重跑工具測試並只讀核對完整產物、來源與關係保留。播放器沿用Node語法及10份面板函式核對，
沒有瀏覽器版面覆蓋；當輪Chromium因沙箱`shutdown EPERM`未能啟動。
本次沒有重跑全工作樹DocGraph，docs通過不外推為全域通過。

只暫存上述連貫範圍；commit／push及遠端CI狀態依即時Git及GitHub核對，不預稱CI成功。
