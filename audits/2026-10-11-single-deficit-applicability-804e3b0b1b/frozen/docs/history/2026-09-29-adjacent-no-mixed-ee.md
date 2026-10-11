# 2026-09-29：E–E 六份正跨度來源排除

Git 基準 `47ebbbc`。接手時已有 B–E checker、artifacts、報告及相關文件的
未提交成果，本輪保留並接續。使用者要求推進 E–E class；完成本型的
任意大小 disk 來源排除，未 commit／push。完整前提及證據界線見
[E–E 報告](../c5_adjacent_degree5_no_mixed_ee.md)。

## 成果與停止點

- E–E 兩側 t=0,(2,1,1)，六原分量皆有非空 singleton 禁色，因此皆碰 B。
  每份原 C 可經 zw 與另一側原分量取得避開自身的外部路徑。既有 K4
  排除及 degree-list 論證遂給每份 actual support 至少兩個 q 色。
- 保留六原分量、八具名接點、zw、全部 bridges／旁支及完整 ordered
  relations。Annulus 次序給六份正跨度，與總跨度≤5 矛盾。
- 綁定全部 144 份原 retained joins／sides，與直接重建的 4·6·6 集合
  相同；全部來源纖維空。0 target 查詢、0 target 接受，無新增有限 minor
  skeleton，不需 T4；不是必要圖的 disk 實現分類。
- 36 個 cyclic words、144 份 contact rotations；ordered lifts 與放寬
  次序的 hull masks 都排除六跨度 C5。C6 正控制有 216 份 lifts／720 份
  masks；四種錯降 unary 為零跨度的控制各有 180 份 C5 placements。
- 380 個完整 binary schemas、四份完整 unary 關係、marginal 負控制；
  144 次 root 交換、144 次反射、576 次具名 unary 交換與 3,456 次共同
  色框核對通過。
- 新增 144 個 source join IDs，累計八類／1,676 份覆蓋，七類／1,872 份
  保留。第九類出口加入 E–E 來源排除分支。下一窄入口 B–C；已綁定
  180 份有序原 IDs，未建立其支援／target 表。

證據為任意大小紙面論證、沿用外部 degree-list 定理及 Python 固定域
控制；未新增 Lean theorem，沒有獨立第二審稿者。未證一般／共同出口、
任意來源完整 Σ、交換機制一般完備性或 K∞=K≤5。

## 驗證

新 checker 預設及 `PYTHONHASHSEED=17` 的 `--check` 均 exit 0，逐 byte
符合本輪 JSON／Markdown。原 no-mixed 與工作區 B–E checker 均 exit 0，
原 artifacts 未改寫。`lake build` 成功，8,827 jobs，只有既有
AttachmentOrder／SymRelabel linter 警告。
文件檢查通過（320 Markdown、3,253 本地連結）；DocGraph 通過
（62 documents、213 relations、0 errors）；`git diff --check` 通過。

```bash
python3 scripts/c5_adjacent_degree5_no_mixed_ee.py --check
PYTHONHASHSEED=17 python3 scripts/c5_adjacent_degree5_no_mixed_ee.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_be.py --check
python3 scripts/c5_adjacent_degree5_no_mixed.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

未單獨重跑：B–B、t2 各分拆及原路徑／雙端點、mixed 各型、唯一 degree-5
完成表、Root 預算全控制、範圍遍歷、雙拒絕 atlas、R 系列、profiles／閉包
與 Lean axiom audit。新 checker 重核完整 binary schema 表；輸入 SHA 綁定
不等於重驗全部前序證明。外部 Gallai 定理依既有報告使用；本輪開啟原文
確認 Lemma 7 的 tightness，未宣稱重新審核全文證明。

更新 checker、JSON／逐筆排除表、新報告、weak-deletion 導覽、STATUS、
出口及範圍報告；B–E／原 no-mixed 報告加後續連結。依
[文件治理](../DOCUMENTATION.md)，研究線及使用方式未變，HANDOFF／README
保持原入口，不追加逐輪數字。歷史 B–E 紀錄保留原輪的停止點。
