# C₅ 私有內點反向接合的具名拓撲核對

2026-09-30。Git 基準 `e751c4b`；接手時有主例及正向私有內點拓撲的
十二份未提交變更，予以保留。`main` 比本地 `origin/main` 多一筆提交；
本輪未要求也未執行 commit／push，未查驗遠端 SHA。

## 成果與停止點

- 新增[反向 checker](../../scripts/c5_two_vertex_private_reverse_topology.py)、
  [完整 companion](../../artifacts/c5_two_vertex_overlap/private_reverse_topology.json)
  及[報告](../c5_two_vertex_private_reverse_topology.md)。只核對既有
  `private_interiors_reverse` 的原十五點三十五邊與七個私有內點。
- R127 `(0,2)` 接 R167 `(3,1)`，即 a0=b3、a2=b1。反向 B 原框是
  `(b0,a2,b2,a0,b4)`；全部原映射、來源邊與具名環序重新核對。
- 完整 rotation 有 22 面、70 條有向邊、Euler=2；面長是 20 個
  三角形、兩個五邊形。外面選 `(a0,a4,a3,a2,b2)`，兩來源 disk
  內部互斥，只共用 a0、a2；七個私有內點在各自原 disk 內。
- A 原框的阻斷是 a0–b2–a2 與
  a1–A_inner9–A_inner5–A_inner7–a3；B 原框的阻斷是
  a0–a1–a2 與 b0–B_inner6–b2。B 的循環端點次序改為
  b0、a2、b2、a0。兩組各自頂點互斥、端點交錯，排除所有以該原框
  作整圖外界的嵌入；不只排除保存的 rotation。
- 完整反向 J 仍 60 軌道／1,440 份賦色，兩個完整五點投影為
  R127／R167。正反向 J 在同一欄序共同 44 軌道、各獨有 16 軌道。
  Companion 保存三份完整 pattern 集合與兩個可直接用另一圖原框邊
  拒絕的具名染色控制，正例另存全圖染色。
- 原框阻斷不排除混合 C₅ 作整圖外界；本見證已提供一個。下一窄題
  是沿同圖、同外面核對該混合框的完整 relation，詳見
  [導覽](../c5_two_vertex_overlap_guide.md)。本輪尚未計算此新五點投影。

新 artifact 為 62,617 bytes，未達大型檔門檻。未改寫原點對、六例
接合、主例拓撲或正向私有內點 artifacts。新 checker 只匯入舊 checker
的 verifier，不修改舊程式。更新兩點／state 導覽、接合及正向報告
後續狀態與 STATUS 直接索引；README 入口與 HANDOFF 研究線沒有變動，
依 DOCUMENTATION 不逐輪複述。

## 驗證

```bash
python3 scripts/c5_two_vertex_private_reverse_topology.py
python3 scripts/c5_two_vertex_private_reverse_topology.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_private_reverse_topology.py --check
python3 scripts/c5_two_vertex_private_topology.py --check
python3 scripts/c5_two_vertex_join_topology.py --check
python3 scripts/c5_two_vertex_join.py --check
python3 scripts/c5_two_vertex_overlap.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

新 artifact 產生及兩次逐 byte 重播均通過。新 checker 各自以原圖
重算正反向全部 `4^8` 份賦色的七內點延拓；接受集、全部保存的染色
witnesses、反向兩個完整五點投影及正反向差集一致。舊正向、主例
36 組環序／24 外面、六份接合與 132 類／1,320 點對重播亦通過。

另直接匯入 verifier 執行三項負控制，全部按預期拒絕：正向 rotation
配反向原邊、正向 B 框配反向原邊，以及 A 框的非交錯路徑對
`a0–b2–a2`／`a3–A_inner8–a4`。前兩項不得把正向具名資料直接當成
反向證據；第三項確認僅有互斥路徑不足以通過交錯性檢查。

`lake build` 通過 8,827 jobs，只有既有 AttachmentOrder／SymRelabel
linter warnings；本輪沒有新增或修改 Lean 檔案。
文件檢查通過 372 份 Markdown／3,786 個本地連結；DocGraph 通過
62 documents／213 relations／5 families，零 errors／notes。
`git diff --check` 及十二份未追蹤檔案的最終換行／尾端空白檢查通過。

環序由既有來源局部環序重新接入 B 構造，沒有使用 NetworkX、新增
依賴或安裝套件。由 Euler=2 推球面、面對偶推 disk 側別及 Jordan
crosscut 阻斷仍是紙面推論，未 Lean 化、未新增 `native_decide` 證明。

未重跑來源大枚舉、代表最小性、其他研究線或 Lean axiom audit；
未核對其餘三份控制的 topology、未枚舉反向所有環序／區域型，
未計算混合新框的 relation、完整後繼表或多步摘要充分性。
