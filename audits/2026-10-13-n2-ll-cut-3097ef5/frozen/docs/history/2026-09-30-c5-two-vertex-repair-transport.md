# 2026-09-30：六例 C₅ local-repair transport audit

接手時 main 工作樹乾淨。依使用者要求，只審核既有六份具名接合圖，
未搜尋新 class pair、未修改 Lean；研究階段未 commit／push，同日提交整理見文末。
目前入口見[兩點重疊導覽](../c5_two_vertex_overlap_guide.md)，
完整數字及推論見[專題報告](../c5_two_vertex_repair_transport.md)。

## 範圍與結果

使用者確認「可用五框」統一定義為原八點 U 上能作整張原圖 disk 外界的
全部 C₅。完整檢查二十條候選：十四條有 sphere rotation／指定面證書，
六條有兩條交錯、互不相交的原路徑阻斷。正向私有內點例新增合法
rotation，證明既有四邊形／六邊形面嵌入並非全部可用框的判準。

四個控制例 P=J、r*=0，唯一 inclusion-minimal repair 為空集合。
正反向私有內點例各為 J=60、P=114、Δ=54 軌道，arity=0,…,8 的
殘留為 `54,54,16,16,0,0,0,0,0`。各有八類完整排除集合、三組極小
類組合，展開成一組二份與十四組三份具名 repair。

唯一 forced scope 是 `(a0,a1,a2,a3)`。最優 B 正向為 `(a0,b0,b2,b4)`，
反向為 `(a2,b0,b2,b4)`。兩例共保存八十八份逐項不可省記錄、forced
witnesses、各階下界 witnesses 與其全部接受 scopes 的原圖延拓。
全部34個 repairs（含四個空集合）各掃完整 `4^8` 域，共2,228,224次查詢，
逐 tuple 核對恰等於原 J。兩例均獨立重建，未預設四點充分或同型。

兩例 repair 家族有十三個相同的具名成員，各兩個獨有。全部40,320個
U 頂點雙射中只有兩個可搬運家族，均不能搬運 J、P 或完整排除資料。
選擇下一步抽象有明確 witness／覆蓋前提的共同 repair lemma；四個
frame-exact 案例保留為退化支。本輪沒有推論一般圖或多步充分性。

## 產物與驗證

- [新 checker](../../scripts/c5_two_vertex_repair_transport.py)。
- [Frame witnesses](../../artifacts/c5_two_vertex_overlap/repair_transport_frames.json)：
  15,706 bytes，固定原圖的發現資料，全部由新 checker 獨立驗證。
- [完整 audit](../../artifacts/c5_two_vertex_overlap/repair_transport.json)：
  468,251 bytes，含完整 J/P/Δ 的全域 S₄ 軌道、frame relations、arity ladder、
  scope projections、排除集合、全部 repairs、witnesses 及跨例矩陣。

新生成器、一般及 `PYTHONHASHSEED=17` 的 `--check` 均逐 byte 通過。六份原接合 checker 與前輪
inclusion-minimal checker 只讀重播通過；反向 J/P/Δ、全部八類完整
排除集合及十五組 repair 另與前輪逐項一致。
新 checker 每個 frame-exact 案例有五項、每個非平凡案例有十項負控制，
共四十項按預期拒絕；包含同基數錯誤排除集、殘留集及修復 relation。
最後報告數字核對另抓出一處合併描述：特殊 W 分支刪 T 後，正向殘留4軌道、
反向2軌道。已改成分例敘述；生成器與完整證書原已保存各例正確集合，無須改寫。

`lake build` 通過8,827 jobs，只有既有 AttachmentOrder／SymRelabel
linter warnings；這是既有專案建置，沒有新增 Lean theorem 或 `native_decide`。

文件檢查通過387份 Markdown／3,933個本地連結；DocGraph 通過
62 documents／213 relations／5 families，零 errors／notes。
`git diff --check`、全部新檔的 whitespace／final-newline 與報告數字核對通過。

```bash
python3 scripts/c5_two_vertex_repair_transport.py
python3 scripts/c5_two_vertex_repair_transport.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_repair_transport.py --check
python3 scripts/c5_two_vertex_join.py --check
python3 scripts/c5_two_vertex_minimal_repairs.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

Frame 發現階段使用本機既有 NetworkX 3.6.1；新 checker 只用標準函式庫，
逐 dart、面及原路徑驗證，不信任發現器。uv 預設 cache 為唯讀，沒有
更改權限或安裝套件，改以本機已存在的套件作一次發現。
本輪未重跑來源大枚舉、class 最小性、點對索引、全部舊單框／拓撲
standalone checkers、三點／四點大型 checker 或 Lean axiom audit。
來源 hash 鏈核對，原接合與大型 artifacts 保持原 bytes。

更新導覽、STATUS、state 導覽及相關報告後續狀態；依文件治理，
研究線和基本閱讀入口沒有變動，README／HANDOFF 不追加逐輪摘要。
兩份新 JSON 都小於1 MB，無須修改 manifest 或 gitignore。

## 同日提交整理（基準 26c63a0）

依使用者 `commit` 要求，將 checker、兩份新證書、專題報告、本紀錄及
相關導覽／後續狀態整理成單一提交。原接合、既有大型 artifacts 及其
manifest 維持原 bytes；本次只提交本機，不推送。

提交前重新執行新 checker 的 `--check`、`lake build`、文件與 DocGraph
檢查，並核對 staged diff。不同 hash seed、六份原接合及前輪極小修復
checker 沿用同次對話對相同程式／證書的通過結果。提交後確認工作樹狀態；
不在本檔預寫尚未產生的 commit SHA。
