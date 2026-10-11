# Mixed P₃ 對稱分支：原五環與完整側支援排除

2026-09-29，前層報告的研究基準為 `773cdf8`；本輪驗證時核對 Git
`11335c15de58aa123ba2b364fb500a8573533e01`（artifacts 工具的另項提交）。
工作樹已有未提交的 mixed 容量 checker／證書／報告及入口更新；保留它們，
接續[導覽](../c5_weak_deletion_guide.md)指定的 P₃ 對稱兩色分支。
新證明見[專題報告](../c5_mixed_p3_symmetric.md)。

## 結果與證據層

- 在 induced-C5 disk minimal q-core、相鄰雙 degree-5、其餘 degree-4、
  唯一 mixed 原 P₃=x₀x₁x₂、root incidences 恰為 zx₀、wx₂ 前提下，
  E_z(q)=E_w(q) 為同 pair 的來源不存在。
- 紙面推導三個原 lists 相同、每份 unary 實際碰 B，故原五環
  z–x₀–x₁–x₂–w–z 內側為空。原 unary contact-to-boundary 路徑及
  z–x₀–B、w–x₂–B 路徑保留。
- 兩份 root 側的完整實際支援，加上三份 P₃ 星狀附件，形成原五環
  的五個同序區塊。Pair residual 的整側不變性給正跨度，五份支援恰
  用完五條框邊；包含未用色 3 的共同 pair 迫五邊只見同一色對，矛盾。
- 不限制 unary 分量大小、bridges 或旁支；不需 T4、Gallai／degree-list
  或其他新增外部定理；未新增 Lean theorem、target 接受或出口類別。

[新 checker](../../scripts/c5_mixed_p3_symmetric.py)與
[證書](../../artifacts/c5_mixed_p3_symmetric/observations.json)保存 1,000
份實際 P₃ 支援、16,000 個獨立 pinned queries、80 份完整對稱關係；
每份有 25 組側角色，共 2,000 必要附件／角色候選。1,950 組不符原
五環次序，50 組由實際側支援不變性排除；零保留、零 target 查詢。
這些是必要資料計數，不是來源圖的計數。

十份飽和幾何另由 120 份 cyclic-hull packing 獨立重算，保留原具名
附件、整體反射與 root 交換；有限 annulus 正控制驗證有向面、rotation
及 Euler characteristic=2，只控制拓撲，不主張 degree／minimality 實現。
證書 581,265 bytes，小於 1 MB，不登錄大型檔案 manifest。

## 驗證

```bash
python3 scripts/c5_mixed_p3_symmetric.py
python3 scripts/c5_mixed_p3_symmetric.py --check
PYTHONHASHSEED=17 python3 scripts/c5_mixed_p3_symmetric.py --check
python3 scripts/c5_mixed_capacity_contacts.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

新 checker 的一般與 seed=17 重播逐 byte 相等；本層及兩個直接／間接
載入的前層 Python SHA 綁定在新證書。Mixed 容量 checker 通過，
仍保存原非平面 minimal P₃ 控制的 31 份刪邊見證及全部 240 proper rows。
完整介面 checker 通過 34,560 原圖 pinned queries、318,720 刪邊 pinned
queries、19,920 分量解除關係與 53,040 全圖 queries。

`lake build` 通過 8,827 jobs，保留既有 longLine、unusedSimpArgs 與
show tactic 警告。未改 Lean 檔案，build 不形式化本輪紙面拓撲與支援
論證。文件檢查通過 357 份 Markdown／3,629 本地連結；DocGraph 通過
62 documents／213 relations／5 families，零 errors／notes。
`git diff --check` 通過；四份本輪新增檔案另核對尾端空白與最終換行。

未單獨重跑 no-mixed 十五類、增長／無增長、搬運、舊 mixed singleton／K2
各家族、root 預算、唯一 degree-5、雙拒絕 atlas、R 系列、profiles／閉包
或 Lean axiom audit。未重讀外部 Gallai 文獻，本輪證明沒有該依賴。
Checker 重用前層完整介面及 pinned 回溯，不是整個引擎的獨立重寫。

## 交接與工作樹

新專題與證書連入 README、STATUS、weak-deletion 導覽及單側出口的
失敗核心限制；容量原報告頁首加後續連結，保留正文與原 artifacts。
研究線與進行中 tag 未變，依文件治理保持 HANDOFF 的短導覽格式。

下一窄題：唯一 mixed 原 P₃、兩端各一 incidence 的非對稱 residual
(1,2) 及整份 root 交換型，先推必要附件與一色側跨度，再研究指定雙列。
不能把本輪整側二元 residual 的正跨度界套到一色側。
其他接線、更大／多 mixed、完整 Σ、逐染色 repair、一般／共同出口
及 `K∞=K≤5` 仍未證。

未開 sub-agents、未使用 Graphify、未 commit／push、未更新 Codex 記憶。
起始另見 `tools/artifacts.py`／`artifacts/MANIFEST.json` 變更，本輪未修改它們。

## 同日提交前核對

後續依使用者 `commit + push` 指示，將 mixed 容量與 P₃ 對稱分支的
兩份 checker、兩份證書、兩份專題、兩份研究紀錄，以及 README、STATUS、
weak-deletion 導覽、前層完整介面及單側出口的相連更新一併提交。
前文「未 commit／push」保留研究輪當時的語境。

提交前 fetch 後，HEAD 與 origin/main 均為 `11335c1`，沒有分歧。
重跑 P₃ checker 的一般／seed=17、mixed 容量、完整有序介面及
`lake build`，全部通過；Lean 仍為 8,827 jobs 與既有警告。
補入前層介面到 P₃ 排除的後續連結後，文件檢查通過 357 份 Markdown／
3,630 本地連結；DocGraph 仍為 62 documents／213 relations／5 families，
零 errors／notes，`git diff --check` 通過。未擴大研究或重跑其他家族。
推送後另以本地 HEAD、origin/main、遠端 refs/heads/main 及工作樹狀態核對；
實際發布結果以 Git readback 為準。
