# No-mixed 無增長：短側弧與共同 singleton 排除

2026-09-29，起始 Git `3174f088880392485aca53ffe46f01e80831243b`。
接手時工作樹已有上一輪局部篩選的 checker、artifact、報告、歷史及
README／STATUS／導覽／前層報告變更，全部保留並在其上推進。
本輪未 fetch、未開 sub-agents、未 commit／push。

專題證明見[無增長報告](../c5_no_mixed_no_growth.md)，目前停止點由
[weak-deletion 導覽](../c5_weak_deletion_guide.md)維護。

## 本輪結果

完成原導覽指定的窄題：在既有 no-mixed 圖類與任意大小共同支援引理
下，所有 F_C(p) 的大小不增長時，E_z、E_w 必有異色 pair。這是不用
必要支援表的紙面證明；舊 7,848 joins 的全域重播保留為控制。

核心推導：

1. 容量保證兩側非空；target singleton 迫每份 F 不縮小且禁色互不重疊。
2. 共同側跨度和至多五、各側至少二，必有長度二的短側。
3. 短側若 E singleton，只能是中間框色或第四色；禁第四色的原分量
   必占滿三點支援，兩條 spokes 由共同單位次序迫在端點。
4. Source 單現點只能在短弧端點；若在中間，另一側看不到其中間色與
   第四色，其 E 對交換兩色不變，不可能與短側同為 singleton。
5. q 與 p₁／p₂ 的單現點相鄰；target 短弧若非三色，E 至少二色；
   若為三色，target 單現點必在中間，另一側的相同交換不變性排除
   同 singleton。

保留完整原分量、contacts、bridges、旁支、actual support、共同環序、
spokes／zw 與字面色框。使用的是完整關係的置換不變性，沒有投影為
接點邊際，也沒有指定一份 source 染色作單分量 repair。

新 [checker](../../scripts/c5_no_mixed_no_growth.py) 只用標準函式庫，
[JSON](../../artifacts/c5_no_mixed_no_growth/observations.json) 綁定 11 份
既有輸入 SHA、完整來源 record／geometry pointer/hash、重新建立的
共同 lifts、全部候選域 hash、原 join index 與實際異色 root pair。
不讀舊 target acceptance／classification 決定新結果。

固定域控制包括 1,872 份短側賦值（216 份 singleton）、120 個 proper
三色 C5、600 份三點弧、5,760 對相鄰單現點的兩列與 11,520 份共同
三色弧。沒有枚舉新來源圖或必要支援；丟掉原單位次序的失敗配置
保留為負控制，不宣稱它是 disk 反例。

重建原 2,082 placements／2,264 短側與 4,164 查詢／11,096 joins。
7,848 個無增長 joins 全有異色 pair。查詢級理由分成短弧非三色及
單現中點交換不變性，各 2,082。這些不是新增 source 排除或 target
接受；32 個無害增長 joins 及原 434 失敗的排除由前層繼續承擔。

## 實際驗證與未重跑範圍

```bash
python3 scripts/c5_no_mixed_no_growth.py
python3 scripts/c5_no_mixed_no_growth.py --check
PYTHONHASHSEED=17 python3 scripts/c5_no_mixed_no_growth.py --check
python3 scripts/c5_no_mixed_local_screen.py --check
python3 scripts/c5_no_mixed_root_transport.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

新 checker 一般及 seed=17 均逐 byte 通過，所有 11 份輸入前後 hash
不變。前層 local-screen 重播通過原 2,208 排除／32 無害 pair 與
7,880 保留 joins；root-transport 重播通過 4,164 查詢／11,096 joins，
仍為原 434 個失敗候選，未改寫舊證書。

`lake build` 通過 8,827 jobs，保留既有長行、unused simp 與 show tactic
警告。無 Lean 檔案修改，這不表示新紙面引理已形式化。

文件檢查通過 351 份 Markdown／3,564 本地連結；DocGraph 通過
62 documents／213 relations／5 families，零 errors／notes。
`git diff --check` 通過；另以文字掃描檢查本輪未追蹤檔案的尾端空白。

| 檔案 | SHA-256 |
| --- | --- |
| `scripts/c5_no_mixed_no_growth.py` | `c085f9dec3f58a809e16a5d84c7831a3123a5be9073d8d462d70cb8efcfb71f8` |
| `artifacts/c5_no_mixed_no_growth/observations.json` | `7e4faefc3abccdbaeeff9465551153efc811e413c590ca7a1c2e87db3582de81` |

未單獨重跑十五類全部完成 checker、三份舊 hypothesis checker、
跨度／root 預算 checker、mixed／唯一 degree-5 家族、雙拒絕 atlas、
R 系列、profiles／閉包或 Lean axiom audit。外部 Gallai 文獻與原
annulus／飽和分量引理沿用前層，本輪未重讀外部文獻。

## 交接界線

下一窄題收斂為：影響 root 可用色的 singleton→pair 增長，為何必被
既有守恆／非守恆局部規則排除。32 個不影響 R 的 pair 無須排除；
AA54 全路徑交換、AB22 非守恆原端點保留。有增長時的全域成功仍依
必要表，不能從無增長定理提升成完整的免表共同 repair。

新報告／歷史／checker／artifact 與導覽、STATUS、README 互連；
局部篩選、假設稽核與跨度報告加後續連結，原當輪數字及語境保留。
研究線與進行中 tag 未變，依文件治理不在 HANDOFF 堆疊逐輪摘要。
未更新 Codex 記憶。

未證來源實現、完整 Σ、一般／共同出口、K∞=K≤5；未新增 Lean
theorem 或 `native_decide`。即時發布狀態以 Git 為準。
