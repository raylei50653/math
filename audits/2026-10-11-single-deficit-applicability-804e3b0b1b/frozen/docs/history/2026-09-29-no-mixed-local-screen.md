# No-mixed 統一局部增長篩選

2026-09-29，起始 Git `3174f088880392485aca53ffe46f01e80831243b`，
工作樹乾淨，本地 HEAD 與 origin/main 相同。本輪未 fetch 遠端，
未開 sub-agents，未 commit／push。

專題證明及數字見[局部篩選報告](../c5_no_mixed_local_screen.md)；
目前停止點由[weak-deletion 導覽](../c5_weak_deletion_guide.md)維護。
接手先確認 no-mixed 全十五類及逐 root 界已完成，沒有沿用舊記憶中
B–B 尚待處理的優先序，也沒有重新枚舉來源圖。

## 本輪產出

- 新 [checker](../../scripts/c5_no_mixed_local_screen.py) 與
  [證書](../../artifacts/c5_no_mixed_local_screen/observations.json)：
  同一局部規則，不按家族分支，不用保存的 target acceptance 或
  `eliminated` flags 代替計算。
- 紙面容量引理說明空 root 必有 singleton→pair 增長；不把它提升為
  排除同 singleton。另證 pair∩R_r=∅、自身 R 至少二色、另一側已知
  非空時的延拓充分條件。
- 守恆分支重算 1,780 個候選的端點／奇數 bridge／全路徑交換；
  非守恆分支重算 460 個候選的原端點聯集，428 排除、32 保留。
- 原 11,096 joins 中 3,216 因局部不可能排除，7,880 保留者全有異色
  root pair。原 434 失敗 joins 由守恆 204／非守恆 230 互斥涵蓋；
  沒有新增 source 排除或 target 接受。
- 全部 32 個未排除局部 pair 都與其 root 的 R 不交；不是 32 個未決
  target，也不宣稱這些局部 pair 可實現。

檢查器綁定 root-transport 及十份原輸入的 SHA，保留每份來源 record
pointer/hash、完整原分量 context、具名接點／支援、原 join index、
局部規則及實際 root pair。全部 source schemas、placements 與環序沿
原證書保留。重算 2,324 份 topology skeletons，驗證固定框弧與原路徑
branch sets；skeletons 並非 degree-list 來源圖。規則重用既有研究
函式，非第二套完全獨立的幾何證明。

## 驗證與未重跑範圍

本輪實際執行：

```bash
python3 scripts/c5_no_mixed_local_screen.py
python3 scripts/c5_no_mixed_local_screen.py --check
PYTHONHASHSEED=17 python3 scripts/c5_no_mixed_local_screen.py --check
python3 scripts/c5_no_mixed_root_transport.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

新 checker 一般／seed=17 均逐 byte 比對通過；11 份 artifact 輸入的
前後 hashes 相同，22 份載入研究 script hashes 保存於新 JSON。
Root-transport 重播通過原 4,164 查詢／11,096 joins 與 434 失敗分類。
每個查詢在新局部篩選後至少保留一個 join，全部保留 joins 都有原
異色 root pair。

`lake build` 通過 8,827 jobs，保留既有長行、unused simp 與 show tactic
警告；不表示本輪紙面引理已形式化。文件檢查通過 349 份 Markdown、
3,544 個本地連結；DocGraph 通過 62 documents／213 relations／5 families，
零 errors／notes。`git diff --check` 通過；新未追蹤檔另核對無尾端空白。

| 檔案 | SHA-256 |
| --- | --- |
| `scripts/c5_no_mixed_local_screen.py` | `6fe5c949f0ad6ead51e5b181c3b694c9f12a0bc1f80526476435502a8afc3a46` |
| `artifacts/c5_no_mixed_local_screen/observations.json` | `657d667754466a49e970e2d00799456b1e344495577e86bc491dac800d0d215c` |

本輪沒有修改 Lean 檔案。未單獨重跑十五類的全部完成 checker、三份
舊 hypothesis checker、跨度／root 預算 checker、mixed／唯一 degree-5
家族、雙拒絕 atlas、R 系列、profiles／閉包或 Lean axiom audit。
新 checker 載入既有支援穩定子、固定框弧與兩種 minor 控制函式並實際
重算本輪所需的 witnesses；這不同於執行各舊 script 的完整 `--check`。
外部 Gallai 定理及任意長原路徑紙面引理沿用，未重讀外部文獻。

## 接手界線

保留 7,848 個無增長 joins 的全表相容證書，以及 32 個不影響 R 的
增長候選。下一個窄問題是以共同支援幾何證明無增長不能留下同
singleton；容量本身只保證兩側非空。接著才處理有效增長的免表
局部排除完備性。AA54 全路徑交換與 AB22 非守恆端點均保留為控制。

新專題、研究線導覽、STATUS 與 README 入口互連；原 hypothesis／
跨度報告加入後續連結，保留各輪數字。HANDOFF 的研究線與進行中 tag
沒有改變，依文件治理不加逐輪摘要。未更新 Codex 記憶。

沒有新增來源可實現性、完整 Σ、免表共同 repair、一般共同出口、
`K∞=K≤5` 或 Lean 結論。即時發布狀態以 Git 為準。
