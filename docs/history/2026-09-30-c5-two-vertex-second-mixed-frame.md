# 2026-09-30：C₅ 反向接合第二混合外框的完整 relation 核對

本輪承接第一混合框 R255 的未提交成果，只計算同一反向見證的另一
五邊形面 `(a0,b4,b0,a2,a1)`。未 commit／push；發布狀態以即時 Git
為準。現況與下一窄題由[兩點重疊導覽](../c5_two_vertex_overlap_guide.md)維護。

## 成果與界線

- 新增[報告](../c5_two_vertex_second_mixed_frame.md)、
  [checker](../../scripts/c5_two_vertex_second_mixed_frame.py)及
  [完整證書](../../artifacts/c5_two_vertex_overlap/second_mixed_frame_relation.json)。
  沿用原十五點三十五邊圖、原八點 J 及反向 rotation，將外面由 19
  改為 21；核對 C₂-disk、十內點、30 內側邊與零外側邊。
- 完整 relation 恰為 R1022／9 軌道／216 賦色，只拒絕 `01012`。
  精確條件是 proper C₅ 且前四點至少用三色，等價於
  `q0!=q2 or q1!=q3`。拒絕由原 B 三角形的共同兩色 list 證成，
  保存 b2 的兩個分支與具名衝突原邊。
- 完整 J 投影、原圖十內點延拓、來源部分關係、公式及既有雙內點
  代表全相等；十列完整纖維大小為 `0,4,4,12,12,12,4,4,4,4`。
  60 份原 J 軌道及全部原圖 witnesses 同色框保存，不改寫舊證書。
- R1022 的七點十二邊代表另有完整染色及 disk rotation 證書；
  具名順序直接對應。D₅ 軌道 masks 為 `959,1007,1015,1021,1022`，
  stabilizer 大小 2；第一框 R255 與此框非 D₅ 等價。
- 全部十組點對投影仍接受 240 份，誤收 `01012` 的 24 份軌道。
  替換須未來只接觸 C₂、其餘十點密封；不宣稱原圖 minor、八點
  替換、最小內點數或一般政策合法性。未 Lean 化。

新 artifact 為 133,951 bytes，未達大型檔門檻。更新兩篇前置報告
後續狀態、兩點／state 導覽及 STATUS 報告／歷史直接索引。
README 入口與 HANDOFF 研究線未改變，依 DOCUMENTATION 不逐輪複述。
未啟動 Graphify、來源大枚舉或其他環序搜索。

## 驗證

```bash
python3 scripts/c5_two_vertex_second_mixed_frame.py
python3 scripts/c5_two_vertex_second_mixed_frame.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_second_mixed_frame.py --check
python3 scripts/c5_two_vertex_mixed_frame.py --check
python3 scripts/c5_two_vertex_private_reverse_topology.py --check
python3 scripts/c5_two_vertex_join.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

新 artifact 產生及兩次逐 byte 重播通過。原 J 由 `4^8` 賦色的
七內點回溯重建；第二框與小代表各窮查 `4^5` 賦色。Checker 每次
均重算完整纖維、點對負控制及三項 verifier 擾動：錯外面、假拒絕
pattern、刪掉原衝突邊，皆按預期拒絕。

第一框 checker、反向拓撲（含正反向完整 J 差集）與既有六份接合／
四個來源代表均重播通過。`lake build` 通過 8,827 jobs，只有既有
AttachmentOrder／SymRelabel linter warnings，未修改 Lean。

文件檢查通過 376 份 Markdown／3,828 個本地連結；DocGraph 通過
62 documents／213 relations／5 families，零 errors／notes。
`git diff --check` 及全部二十份未追蹤文字檔的最終換行／尾端空白
檢查通過。工作樹保留前輪未提交成果，本輪未操作 Git index。

未重跑來源大枚舉、目錄最小性、主例所有環序／外面、正向獨立拓撲
checker、1,320 份點對索引或 Lean axiom audit；未改變的既有證據
沿用各原報告。兩混合框共同拉回是否等於原 J、其他可能外框及一般
多步摘要仍未計算。
