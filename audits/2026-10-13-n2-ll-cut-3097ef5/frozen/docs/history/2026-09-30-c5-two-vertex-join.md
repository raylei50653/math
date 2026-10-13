# C₅ 具名八點接合與同代表整圖核對

2026-09-30。Git 基準 `e700ff91e0b24ed432dc23c5713f3a4a3f8e226a`。
接手時已有未提交的[兩點重疊交接整理](2026-09-30-c5-two-vertex-overlap-handoff.md)：
README、HANDOFF、STATUS、state 導覽的修改，以及點對 checker／artifact、
規格報告、導覽與交接歷史。全部保留；本輪不 commit／push。

## 成果與精確範圍

- 新增[具名 evaluator](../../scripts/c5_two_vertex_join.py)、
  [完整八點 artifact](../../artifacts/c5_two_vertex_overlap/eight_point_joins.json)及
  [報告](../c5_two_vertex_join.md)。支援任選既有 class IDs、兩點有序雙射
  的單次求值；預設只重播六份固定控制。
- 主例 A=B=R1023、A `(0,2)` 接 B `(0,1)` 的 J 有 140 色軌道／3,360
  具名賦色，回投影 A=R1016、B=R1023。反向雙射與自由點對另存。
- 共同弦／框邊與 R127、R167 的七個私有內點控制均保留原代表實際邊。
  全部補入原五條 C₅ 框邊，六份共同 relation 與整圖回溯逐集合相等。
- 每份 J 保存全部 canonical patterns 及每軌道一份整圖染色 witness，
  另存兩份原五點完整投影及 guard 核對。四份來源代表亦獨立重算完整 Σ。
- 保存「兩側獨立 canonical 後直接拼列」及「僅保留兩框與所選共享點對」
  的負控制；後者在私有內點例多收 92 個不可延拓軌道。

新 artifact 為 421,943 bytes；原點對 artifact 仍為 544,201 bytes，
未重寫其內容。未達大型 artifact 門檻，不改 manifest。
更新報告、README、研究線導覽、state 導覽與 STATUS；HANDOFF 的研究線
及進行中標記已正確，依文件治理不新增輪次細節。

## 驗證

```bash
python3 scripts/c5_two_vertex_overlap.py --check
python3 scripts/c5_two_vertex_join.py
python3 scripts/c5_two_vertex_join.py --check
PYTHONHASHSEED=42 python3 scripts/c5_two_vertex_join.py --check
python3 scripts/c5_two_vertex_join.py \
  --class-a 1023 --pair-a 0,2 --class-b 1023 --pair-b 0,1 \
  --output /tmp/c5_two_vertex_join_reference.json
python3 scripts/c5_two_vertex_join.py \
  --class-a 1023 --pair-a 0,2 --class-b 1023 --pair-b 0,1 \
  --output /tmp/c5_two_vertex_join_reference.json --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

原點對重播、六份接合的產生／只讀逐 byte 重播、不同 hash seed 及單例
CLI 產生／重播均通過。每份遍歷 65,536 個具名八點賦色，分別以完整
relation 定義及只看實際圖的 backtracking 核對；四份來源各查 1,024 個
五點賦色。`lake build` 通過 8,827 jobs，只有既有 SymRelabel／
AttachmentOrder linter warnings；沒有新增 Lean theorem，也未跑 axiom audit。

文件檢查通過 366 份 Markdown／3,733 個本地連結；DocGraph 通過
62 documents／213 relations／5 families，零 errors／notes。
`git diff --check` 及新檔尾端空白／最終換行檢查通過；另查四組非法
CLI 輸入（缺參數、目錄外 ID、重複點、越界點）均明確拒絕。

## 停止點與保留界線

一次八點語義與同圖核對已完成。接下來沿用主例分開檢查抽象平面性、
指定 A／B disk 外框及兩份 disk 區域的側別規則，見[導覽](../c5_two_vertex_overlap_guide.md)。
本輪只記錄共同邊身份，未跑 planarity／embedding；各拓撲欄保持 unknown。
沒有重跑來源大枚舉、其他研究家族、弱刪除證書或目錄最小性。
完整八點後繼表、拓撲分類、多步充分性與 `K∞=K≤5` 均未完成。
沒有 Graphify、sub-agents、commit／push、遠端 SHA 驗證或記憶更新。

## 後續提交整理

同日使用者在研究完成後明確要求 `Commit`。將前述尚未提交的兩點
交接資料與本輪八點 evaluator／artifact／報告／導覽一併提交。
提交前再次通過兩個 `--check`、文件檢查、DocGraph 及 `git diff --check`；
Lean 檔案未變，沿用上節本次工作已通過的 `lake build`。
本次只作本地 commit，未推送或驗證遠端 SHA。提交雜湊以 Git 歷史為準。
