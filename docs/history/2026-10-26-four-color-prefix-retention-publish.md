# 四色前綴剪枝與無損回填壓縮整理發布

2026-10-26。所屬研究線：[四色求解導覽](../four_color_guide.md)。
發布前基準為 `ad82986cae9713f0d4aa08e8c9458e499b341c78`；實際提交與遠端身份以Git核對為準。

## 本次進展

- [完整因子前綴剪枝](../four_color_logic_optimization.md)：新增可選 `bucket_method="prefix"`
  及 `--bucket-method prefix`。當一張完整因子的座標都已補齊，立即核對並排除不相容後綴；
  預設仍為 `anchor`，全部有序邊界、完整fibres、來源與最後共同回寫保持。
  同四十例仍為27可解／13無解／0超限，工作檢查11,968,026→10,433,208，減12.82%。
  工作計數單位及單輪時間各有限制，不能推成一般加速比例。
- [回填可能性與無損壓縮](../four_color_retention.md)：完整邊界每列留一個合法見證可保求一解，
  但一般不保全部原解；主程式採4-bit mask保存每列全部色，公開紀錄仍列完整排序色列表。
  原四十例共149,040個邊界列、201,747個回填色選項均保留；重建回填map的估計物件體積
  30,351,392→21,583,496 bytes，減28.89%，不是程序RSS或整體記憶體降幅。
- 指定有限證據包含2,240份小圖條件、164份新圖的原邊／完整fibres核對及八份截斷反例。
  五點星形圖即使保留231／232列，仍可能丟失外側唯一合法邊界；不能任意截斷邊界關係。

前綴與逐因子接合的探索來源、正式模式來源、完整gzip結果及normal／seed-17歷史收據原樣保存。
無損表示前後80份完整結果相同，以及seed-17重播等主張，沿用原報告具名收據；
本次發布未重跑整批效能與normal／seed-17實驗。

## 本次實際驗證

[工具測試](2026-10-26-four-color-prefix-retention-publication/tool-tests.log)通過342項：

```bash
uv run --with-requirements requirements.txt python -m unittest discover -s tools/tests -p 'test_*.py'
```

其中新增15項測試核對完整Cartesian連接、空fibres、固定色、非連續ID、
工作／儲存中斷切點、CLI及比較器負控制。系統Python未安裝networkx，測試使用既有uv依賴環境。
本次未修改Lean來源，未重跑Lean build，沒有新增Lean定理。

[只讀證據核對](2026-10-26-four-color-prefix-retention-publication/artifact-audit.json)
通過120份完整gzip、131份不同來源快照（含49份前綴正式來源），
另核40對anchor／prefix完整語義相同、40對prefix／mask完整gzip逐位元組相同，
以及retention摘要29份目前scripts的來源hash。核對只讀取既存結果，不冒充當輪重新求解。
使用新輸出路徑可重跑，不覆寫歷史驗證：

```bash
python3 docs/history/2026-10-26-four-color-prefix-retention-publication/audit_artifacts.py --root . --out /tmp/four-color-prefix-retention-publication-audit.json
```

前綴歷史 `verify_replay.py` 要求工作樹等於當輪來源，且會寫入歷史收據；目前mask版本
應使用上述只讀核對，不能把歷史來源檢查失敗誤認為求解器退步。
發布時為retention完整執行索引補回 `inputs.json` 及 `baseline-manifest.json`，
從既有flow證據複製原始bytes並核原report的hash，沒有更改既有完整結果。

[文件檢查](2026-10-26-four-color-prefix-retention-publication/docs-check.log)及
[正式docs DocGraph](2026-10-26-four-color-prefix-retention-publication/docgraph-docs.log)通過。
[全工作樹DocGraph](2026-10-26-four-color-prefix-retention-publication/docgraph-whole-tree.log)
仍有72個保留歷史快照／scratch的重複ID；不混稱全域通過。
[Git index產物政策](2026-10-26-four-color-prefix-retention-publication/artifact-policy.log)與
[提交空白檢查](2026-10-26-four-color-prefix-retention-publication/staged-whitespace.log)另存發布前結果。

## 範圍與停止點

- Closure scope：只完成指定消元流程／表示改動及有限核對；完整消元的一般演算法證明仍見
  [原完備性報告](../four_color_completeness.md)，本批沒有整份Python形式化驗證。
- Updated：四色導覽、STATUS、約束引擎使用入口與兩份專題報告；發布紀錄由STATUS歷史區連入。
- Reviewed-unchanged：README／HANDOFF入口與研究線排程未變；C₅／W7／J1／J2來源義務未受影響。
- Remaining OPEN：一般消元前傳播完備性、一般效率、固定小接口充分性，以及從同一平面來源
  推出必有可延伸邊界的四色定理義務；本批沒有越過既有C₅／932結構缺口。
- Propagation stop：停於本研究線及直接使用者；沒有跨線來源排除或全域證明主張需要更新。

發布後分別核對local／tracking／remote SHA及遠端CI；push成功不表示CI已完成。
