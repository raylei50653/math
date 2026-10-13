# 2026-09-29：無 mixed (2,2) 重疊型全來源排除與五類覆蓋

Git 基準 `c1be8fb`；接手時工作區乾淨。使用者要求繼續推進交換或幾何阻斷的
覆蓋範圍，依 HANDOFF 處理 t_z=2,(2)、t_w=0,(2,2)、D_w=0、O_w=1。
研究完成時成果先留於工作區；後續使用者明確要求 commit／push，
提交範圍包含新 checker、JSON／支援表、報告、README、HANDOFF、STATUS、
範圍報告、缺額型後續入口及出口定理。

## 成果與證據界線

- [新報告](../c5_adjacent_degree5_no_mixed_t2_t0_overlap.md) 與 checker 逐 ID／SHA
  綁定原 96 份接合；直接從兩個相交 pair 的完整禁色式獨立重建同一集合。
- lifts 與兩側 hull 算法重算同得 910 份幾何，接上本輪完整 schemas 得 212
  份支援；40 份原資料有支援、56 份纖維空。未沿用缺額型的支援保留表。
- 212 份全由原分量 source K5 排除：188 份兩分量皆可，另各 12 份只由
  C_w 或 D_w 的固定框弧規則成功。全部成功項可用原 w–z–b_i 外部路徑。
- 1,968 份具名 minor skeletons、13 個負控制、7,280 次 contact rotations；
  全部 212 份另核反射、整分量交換、整圖 root 交換。0 target 查詢及新增接受。
- 覆蓋增加正反向 192 份，累計五種交換型／936 份原接合，恰為所有含 t=2
  側的格；十類／2,612 份仍開放。出口第九類移除另一 root 的分拆限制。

本輪重讀 [Dvořák 的 degree-list 講義](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
Lemma 7 及 Theorem 10（第 5–6 頁），核對 tightness／Gallai block palettes 前提。
任意大小結論還使用已證的 disk annulus 次序、原 bridge 路徑及固定框弧抽取；
Python 控制不替代這些紙面引理，skeletons 不具完整 degree-list 來源保證。
未新增 Lean theorem，未證一般機制完備性、一般／共同出口或 K∞=K≤5。

## 驗證

新 checker／JSON／Markdown 已生成，以下六個 checker 及四項整合檢查均 exit 0。
新 checker 另指定 `PYTHONHASHSEED=17`，重算與原生成檔逐 byte 相同。
`lake build` 完成 8,827 jobs，只有既有 AttachmentOrder／SymRelabel linter 警告。
文件檢查涵蓋 307 份 Markdown、3,232 個本地連結；DocGraph 為 62 documents、
213 relations、5 families，0 errors／0 notes。HANDOFF 為 126 行。

```bash
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t0_overlap.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t0_pairs.py --check
python3 scripts/c5_adjacent_degree5_no_mixed.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t1_bridge.py --check
python3 scripts/c5_single_spoke_frame_arc.py --check
python3 scripts/c5_exchange_geometry_scope.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

未單獨重跑：t2 初層／interfaces、其他 mixed／唯一 degree-5 完成表、
Root 預算全控制、雙拒絕 atlas、R 系列、profiles／閉包與 Lean axiom audit。
舊 single-spoke (2,2) 嚴格 provenance 差異沿用[缺額型紀錄](2026-09-29-adjacent-no-mixed-t2-t0-pairs.md)；
本輪重播 pairs checker 時仍以其 legacy_two_contact_replay 核對數學 payload／生成表，
不覆寫原證書或把舊 byte-level provenance 檢查記為通過。

發布沿用上述同一工作區已通過的六個 checker 與 Lean build；研究程式、
證書及 Lean 檔未再修改。提交前另核對新證書的 checker／全部輸入 SHA256，
並重跑文件、DocGraph 與 diff 檢查。提交／遠端 SHA 與乾淨狀態以發布後
Git readback 為準，不預先將推送結果寫成通過。

## 停止點

新證書只綁定下一 B–B 型的 236 份原 IDs，未開始其支援覆蓋或 target 遍歷。
首項 retained-join ID=2142、sides=(91,91)，兩 root 各一 spoke，均落 b0；
各有二接點 singleton F={1} 與單接點 F={2}，共同 c=3。
保留四原分量、六接點、兩條獨立原 spokes、zw 及共同色框，優先序見 [HANDOFF](../HANDOFF.md)。
