# 2026-09-27：同染色 dual 路徑有序重接

報告見 [共同路徑與 record 110](../c5_dual_path_surgery.md)。接續當時已有、
尚未提交的 edge-pair 座標工作，保留其檔案及 HANDOFF／STATUS 變更。

本輪完成任意大小 dual 雙色路徑的一步更新：保留共同 ordered cut ports，
將兩個外部色對分別與原路徑的另一色 local links 重接。兩份外部配對
必使用同一側別、同一切口環序與同一批實際 c 邊；閉圈亦保留。
這給指定一步的充分資料，尚未給有限可迭代 state。

既有 mask 701 的同一張 induced-C5 disk 圖上，兩份完整 α=01023 染色
具有完全相同的三配對；交換唯一 23 boundary path 之後，13 配對卻不同。
初始配對正是 record 110 必需的 α 配對。一份違反交換後必要重接等式，
並在下一次實際交換得到 q；另一份通過這次等式。控制圖本身接受 q，
不能充當 record 110 來源或反例。

對假想 record 110 來源，minimality 加既有 T4 染色先證 2-connectedness，
再逐面補完一份 α 染色，保留整份具名來源作為子圖。沒有假設補完保留
degree、minimality、全部 T4 或原二分量關係。所有交換在同一個選定補完
中進行，所得染色皆可限制回來源。下一步是把原兩份 bridge 路徑／旁支
tethers 接到共同切口，證是否必違反兩個重接等式；record 110 仍未排除。

新增 checker 與 JSON 證書。重播既有 56 個 induced-C5 triangulations，
驗證 oriented faces、vertex rotations、Euler characteristic；710 個
完整染色模 S4、3,550 次 boundary path 交換、660 次閉圈交換、8,420 個
混合色對更新、4,210 次 primal 積分，以及 3,550 份共同切口側別與次序。
未生成新來源圖 catalogue；未重跑舊 (2,1,1) 或 R-series 枚舉。

本輪實際驗證：

- `python3 scripts/c5_dual_path_surgery.py --check`：上述重接、切口次序、同圖
  反例、record 110 必要配對及兩步 q escape 全部通過，逐 byte 比對證書。
- `python3 scripts/c5_edge_pair_coordinates.py --check`：既有 240 assignments、
  60 edge words、20 clauses 及 1,024 masks 等價重播通過。
- `python3 scripts/c5_single_spoke_two_two.py --check`：來源必要表原樣重播，
  保留 380 筆／190 型、104 筆雙列已證；沒有改寫這份 artifact。
- `python3 scripts/check_docs.py`：181 Markdown 頁／2,217 本地連結通過。
- `python3 tools/docgraph check`：20 documents、43 relations、4 families，
  0 errors／notes。
- `lake build`：8,826 jobs 成功，只重播既有 linter warnings。
- `git diff --check`：通過。

未新增 Lean theorem；build 是既有形式化整合檢查，不認證新紙面 topology
或 surgery 定理。研究輪結束時未 commit／push。

同日後續依使用者要求整理 commit＋push：將相連的 edge-pair 座標及有序
重接程式、兩份證書、報告、README 與交接索引一併納入。發布前核對兩份
證書的全部來源 SHA256 仍相符，沿用上述已通過的研究重播與 Lean build，
並重跑文件、DocGraph 及空白檢查；提交與遠端狀態以 Git 為準。
