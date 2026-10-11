# 2026-09-28：single-spoke／no-spoke 六組成果整理與發布驗證

本次依使用者「整理目前進展後 commit + push」要求，整理基準
`2de13f78602b2267376c5eb08ee2957603d549b5` 上的六組既有未提交成果。
發布前 `git fetch origin` 確認 HEAD 與 origin/main 仍同於此基準。
目前研究優先序見 [HANDOFF](../HANDOFF.md)；最終提交及遠端狀態以 Git 為準。

## 成果與停止點

| 成果 | 本次保留的精確結論 |
| --- | --- |
| [局部 residual](../c5_single_spoke_residual_locality.md) | record 90／282 的 p₂ 已證；single-spoke (2,2) 來源排除仍 278，保留 102 筆／51 型全部雙列已證，0 查詢未決 |
| [(3,1) 排除](../c5_single_spoke_three_one.md) | 三接點 active triangle、原 boundary tethers 與唯一 spoke 給來源 K5；不需 T4 |
| [(4) 排除](../c5_single_spoke_four.md) | 三拒絕共同結構給兩 triangle 加單 bridge，再給原圖 K5；全部 t=1 接回條件式出口 |
| [No-spoke 外部連通](../c5_no_spoke_exterior.md) | 六種 t=0 分拆排除四種；保留 (2,2,1)、(2,1,1,1)，多分量皆 K4-free |
| [No-spoke 環狀支援](../c5_no_spoke_supports.md) | (2,1,1,1) 的 48 筆全部指定雙列延拓；唯一 degree-5 的失敗側只剩 (2,2,1) |
| [No-spoke 原外部路徑 K5](../c5_no_spoke_path_minor.md) | 616 筆排除 500 筆來源，再新增 104 個延拓；剩 116 筆，108 筆雙列已證、12 個未決查詢 |

下一入口仍是 **record 84／p₁**：q=01012，支援 (014,123,34)，
q 禁色 ({0},{2,3},{1})；p₂=01212 可取 z=2。p₁=01021 拒絕候選只剩
({0,1},{3},{2})，C₀ 的 target 路徑塊支援為 01／04／014。
須比較同一 source singleton palette 與 target 首橋，保留五個原接點、
完整有序關係及 C₁／C₂ 的實際外部路徑；不能套雙列 pair residual 引理。

本次沒有推進新數學結論。六組成果均保留 checker、JSON／支援表、報告與
各輪歷史，並同步 README、STATUS、出口接合及直接相關報告的後續狀態。
HANDOFF 的重複歷史摘要收斂為完成分支表、當前數字與精確下一入口；
舊報告／artifact 的當輪數字和歷史「未提交」敘述保持原語境。

## 本次實際驗證

六支新 checker 與八支相關既有 checker 全部通過：

```bash
python3 scripts/c5_single_spoke_residual_locality.py --check
python3 scripts/c5_single_spoke_three_one.py --check
python3 scripts/c5_single_spoke_four.py --check
python3 scripts/c5_no_spoke_exterior.py --check
python3 scripts/c5_no_spoke_supports.py --check
python3 scripts/c5_no_spoke_path_minor.py --check
python3 scripts/c5_single_spoke_first_bridge.py --check
python3 scripts/c5_single_spoke_cross_row.py --check
python3 scripts/c5_single_spoke_frame_arc.py --check
python3 scripts/c5_single_spoke_branch_palettes.py --check
python3 scripts/c5_single_spoke_single_contact_bounds.py --check
python3 scripts/c5_single_spoke_cores.py --check
python3 scripts/c5_two_spoke_three_contacts.py --check
python3 scripts/c5_single_spoke_root_conservation.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
git diff --cached --check
```

新證書重算一致，既有 artifacts 未改寫；no-spoke 支援 checker 亦重播其
內含的既有 completion 接線 audit，未另跑 completion 的完整命令。
`lake build` 成功（8,827 jobs），只有既有 AttachmentOrder／SymRelabel
linter warnings；未變更 Lean 源碼，也未新增 Lean theorem。
文件、DocGraph 與工作樹／暫存區 whitespace 檢查均通過。

未重跑 single-spoke (2,2) 全部中間層的獨立 checker、two-spoke 全表、
雙拒絕 atlas、R 系列大覆蓋、一般 profiles／閉包、來源圖枚舉或 Lean
axiom audit；未重新查閱外部定理。未列出的證據沿用各原研究紀錄，
不能把這次發布重播解讀為整個專案或任意大小紙面證明的重新驗證。

任意大小結論仍由各報告的紙面論證與外部 degree-list 定理承擔；Python
為固定域控制，minor skeletons 不是來源可實現性證書，`lake build`
不形式化新拓撲。一般單側／共同出口、degree≥6、多 degree-5、
(2,2,1) 完整分離、保留型可實現性及 `K∞=K≤5` 仍未證。
