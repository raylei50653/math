# C₅ 反向接合混合外框的完整 relation 核對

2026-09-30。Git 基準 `e751c4b`；接手時有十六份未提交變更，涵蓋
主例、正向及反向私有內點拓撲，全部保留。`main` 比本地
`origin/main` 多一筆提交；本輪未要求也未執行 commit／push，未查遠端 SHA。

## 成果與停止點

- 新增[報告](../c5_two_vertex_mixed_frame.md)、
  [checker](../../scripts/c5_two_vertex_mixed_frame.py)與
  [完整證書](../../artifacts/c5_two_vertex_overlap/mixed_frame_relation.json)。
  沿用反向原十五點三十五邊圖與面 19，不改原圖或既有 artifacts。
- 混合外框 C=`(a0,a4,a3,a2,b2)` 的完整 relation 是 R255，
  8 軌道／192 份具名賦色。十列完整 J 纖維大小為
  `6,6,6,12,12,12,3,3,0,0`；合計 60 軌道／1,440 份八點賦色。
- 相對新框量化 a1、b0、b4 及七個原私有內點，共十內點。
  原 rotation 重播有 22 面，五條框邊、30 條內側邊、零外側邊。
- 正確條件為 proper C₅ 且前四點未用滿四色。`01231`、`01232`
  兩個拒絕 patterns 有具名原邊強迫染色矛盾；全部接受軌道均存
  原十五點染色 witnesses。保存每份 q 的全部八點纖維，共同換色。
- 已有 R255 代表是一個內點連到新框 0、1、2、3，不需 D₅ 再對齊。
  重播六點九邊的完整 relation 及其 disk rotation，與原圖完全相等。
  替換僅適用於未來只接觸新 C 的染色 contexts，不是八點／幾何
  無條件替換；一般政策仍 unknown，未 Lean 化。
- 全部十組點對投影的合取仍接受 240 份，誤收上述 48 份，作為
  高階條件不可省略的負控制。下一個窄入口是同見證另一五邊形面
  `(a0,b4,b0,a2,a1)` 的完整 relation，詳見[導覽](../c5_two_vertex_overlap_guide.md)。

新 artifact 為 128,303 bytes，未達大型檔門檻。更新反向報告後續狀態、
兩點／state 導覽與 STATUS 報告／歷史直接索引。README 的入口與
HANDOFF 的研究線未改變，依 DOCUMENTATION 不逐輪複述。

## 驗證

```bash
python3 scripts/c5_two_vertex_mixed_frame.py
python3 scripts/c5_two_vertex_mixed_frame.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_mixed_frame.py --check
python3 scripts/c5_two_vertex_private_reverse_topology.py --check
python3 scripts/c5_two_vertex_join.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

新 artifact 產生及兩次逐 byte 重播均通過。原八點 J 由 `4^8` 賦色的
七內點回溯重建；新框及小代表各窮查 `4^5` 賦色。完整 J 投影、原圖
十內點延拓、來源部分關係合取、四點公式、小代表接受集全部一致。
另重播反向拓撲（含正反向完整 J 差集）與既有六份接合及四個來源代表。

三項直接匯入 verifier 的擾動控制全按預期拒絕：不是原圖 cycle 的
具名新框、錯將另一個五邊形面 21 當成 C 的外面，以及將接受列
`01012` 當成四點滿四色的強迫矛盾。Checker 內另重算全部十組點對
的負控制，不只讀取保存的預期數字。

`lake build` 通過 8,827 jobs，只有既有 AttachmentOrder／SymRelabel
linter warnings；未修改 Lean。文件檢查通過 374 份 Markdown／3,805
個本地連結；DocGraph 通過 62 documents／213 relations／5 families，
零 errors／notes。`git diff --check` 及十六份未追蹤檔案的最終換行／
尾端空白檢查通過。

未重跑來源大枚舉、目錄最小性、主例所有環序／外面、正向獨立拓撲
checker、1,320 份點對索引或 Lean axiom audit；這些未改變的既有證據
沿用各原報告。未計算另一新框、完整後繼表或一般多步摘要。
