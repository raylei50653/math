# Mixed P₃ 非對稱六跨度與兩端各一 root 接線完成

2026-09-30，Git 基準 `d72b6cb`；起始工作樹乾淨，main 與本地
origin/main 一致。本輪未作遠端查詢，未 commit／push。
依 [weak-deletion 導覽](../c5_weak_deletion_guide.md)的窄問題接續，
完整成果見[專題報告](../c5_mixed_p3_asymmetric.md)。

## 結果與證據界線

在 induced-C5 disk minimal q-core、相鄰雙 degree-5、其餘 degree-4、
唯一 mixed 原 P₃=x₀x₁x₂、contacts 恰為 zx₀、wx₂ 的前提下，
非對稱 residual (1,2) 及整份 root 交換型均不存在來源。

紙面證明保留完整 P₃ 關係、原五環、全部 unary／spokes、實際支援
與外部路徑。被拒絕的 root 對必含第四色 3。一色側若剩 3，支援
必見三色、跨度至少二；若剩已用色 a，另一側 {a,3} 必見另外兩色，
沿原環序把那兩色與 a 共同計費。兩分支皆需至少六條框邊，後者
明確允許一色側零跨度。結合前層對稱排除，兩端各一 incidence 接線
的全部 residual 都已覆蓋。

不限制 unary 的大小、bridges 或旁支；不需 T4、Gallai／degree-list
或新外部定理。屬任意大小紙面來源排除，未新增 Lean theorem、
target 接受、完整 Σ 分類或一般出口定理。

## 證書與驗證

[新 checker](../../scripts/c5_mixed_p3_asymmetric.py)／
[證書](../../artifacts/c5_mixed_p3_asymmetric/observations.json)保存：

- 1,000 組實際 P₃ 附件、完整 triple／contact／F masks、16,000 次
  獨立 pinned queries；與既有完整介面函式一致。
- 一色側正規化為 z 的 384 組附件／residual，26,400 組完整側角色。
  340 組／23,200 側角色無原環序支援；44 組／3,200 側角色在 84 份
  相容幾何中均有整側不變性反證。零保留，零 target。
- 兩種獨立方法得到相同 110 份同序幾何，包括單點 A_z。保存共同
  lifts、間隙和原框點；共享端點合法，開框邊不可重用。
- 384 組的整體反射／共同色置換、完整 root 交換及全部側角色交換；
  224 個支援不變性控制，以及成本恰六的必要支援正控制。

這些是必要資料的有限核對，不是 disk 來源數或實現證書。新檔為
490,163 bytes，小於 1 MB，未改大型 artifact manifest。新證書綁定
本 checker、capacity 與 base interface Python SHA；舊 artifacts 不變。

本輪執行：

```bash
python3 scripts/c5_mixed_p3_asymmetric.py
python3 scripts/c5_mixed_p3_asymmetric.py --check
PYTHONHASHSEED=17 python3 scripts/c5_mixed_p3_asymmetric.py --check
python3 scripts/c5_mixed_p3_symmetric.py --check
python3 scripts/c5_mixed_capacity_contacts.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

新 checker 一般與 seed=17 的逐 byte 重播、前層對稱、mixed 容量、
完整有序介面均通過。完整介面仍核對 34,560 原圖 pinned queries、
318,720 刪邊 pinned queries、19,920 分量解除關係與 53,040 全圖 queries。
既有 Lean build 通過 8,827 jobs，保留既有 linter 警告；未改 Lean
檔案，這不形式化本輪 Jordan／跨度證明。

文件檢查通過 359 份 Markdown／3,652 本地連結；DocGraph 通過
62 documents／213 relations／5 families，零 errors／notes。
`git diff --check` 通過，新加入的四份檔案另查尾端空白與最終換行。

未單獨重跑 no-mixed 十五類／增長／搬運、舊 mixed singleton／K2
各家族、root 預算、唯一 degree-5、雙拒絕 atlas、R 系列、profiles／
閉包或 Lean axiom audit。未重讀外部 Gallai 文獻，本輪沒有該依賴。

## 交接

報告、checker、證書、研究紀錄已接入 README、STATUS、weak-deletion
導覽及單側出口的失敗核心限制；兩份前層報告新增有日期的後續連結。
研究線與進行中 tag 不變，依文件治理保持 HANDOFF 的短導覽。

下一窄題為原 P₃ 的 root masks=(0,1,2)：z 接中點 x₁、w 接端點 x₂，
保留另一原端點 x₀ 與其三份 boundary 附件。前層已有六份必要色配置，
各點 boundary 鄰點數 (3,1,2)，尚須實際支援／原四環內外側分析。
不能刪 x₀ 後套 K2；其他 P₃ 接線、triangle、更大／多 mixed、
逐染色 repair、完整 Σ、一般／共同出口與 `K∞=K≤5` 仍未證。

未開 sub-agents、未使用 Graphify、未 commit／push、未更新 Codex 記憶。
