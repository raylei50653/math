# 2026-09-29：B–E 五份正跨度與完整關係搬運

Git 基準 `47ebbbc`，接手時工作區乾淨。使用者要求推進 B–E class；本輪
完成此型及整圖 root 交換型的指定雙列分離，成果留在工作區，未 commit／push。
完整前提、任意大小必要化約與證據界線見 [B–E 報告](../c5_adjacent_degree5_no_mixed_be.md)。

## 成果與停止點

- 五原分量各有避開自身的原 root-to-boundary 路徑：z 側用原 spoke，
  w 側用 zw 再接原 spoke。由既有 degree-list／K4 排除論證得五份正跨度。
- C5 五框邊預算迫使每份 actual support 恰是一條相鄰框邊。兩獨立算法
  同得 180 份幾何／placements，保留七具名接點及 720 份 root rotations。
- 原 180 份 IDs／sides 有 60 份非空纖維、120 份空纖維，得到 144 份
  必要支援。完整 binary schemas 與三個 unary relations 都保留，不能視作
  分量獨立可實現或將 unary 當 root-spoke。
- 288 個指定 target 全以完整關係精確搬運接受，無 target minor 查詢、
  無額外 source minor 排除。10,656 次關係搬運、4,896 次 contact reversal、
  288 個字面反射、144 份整來源 root swaps、432 個含 q 的交換接合及
  六項負控制核對通過。
- 第九類出口加入 B–E 及 E–B。新增 360 個原必要 join IDs，累計七類／
  1,532 份覆蓋，八類／2,016 份保留。下一窄入口 E–E，尚未對其支援／
  targets 執行枚舉，也不把預期六跨度矛盾計為本輪成果。

證據為紙面任意大小化約、沿用外部 degree-list 定理及 Python 有限證書。
未新增 Lean theorem，未證必要資料的 disk 實現、一般／共同出口、任意來源
完整 Σ、一般交換完備性或 K∞=K≤5。

## 驗證

新 checker 預設及 `PYTHONHASHSEED=17` 的 `--check` 均 exit 0，逐 byte
符合本輪 JSON／Markdown。原 no-mixed 與 B–B checker 均 exit 0，原 artifacts
保持不變。`lake build` 完成 8,827 jobs，只有既有 AttachmentOrder／SymRelabel
linter 警告。文件、DocGraph 及 diff 檢查亦通過。

```bash
python3 scripts/c5_adjacent_degree5_no_mixed_be.py --check
PYTHONHASHSEED=17 python3 scripts/c5_adjacent_degree5_no_mixed_be.py --check
python3 scripts/c5_adjacent_degree5_no_mixed.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_bb.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

未單獨重跑：t2 各分拆與原路徑／雙端點報告、mixed 各型、唯一 degree-5
完成表、Root 預算全控制、範圍遍歷、雙拒絕 atlas、R 系列、profiles／閉包
及 Lean axiom audit。新 checker 會重核完整 binary schema 表；輸入 SHA 綁定
不表示重驗所有前序結果。外部文獻沿用既有報告，本輪未重新查核。

更新 checker、JSON／逐筆表、專題報告、weak-deletion 導覽、STATUS、出口
及範圍報告；B–B 報告加後續連結。依 [文件治理](../DOCUMENTATION.md)，
研究線及使用方式未變，HANDOFF／README 不加入逐輪數字。
