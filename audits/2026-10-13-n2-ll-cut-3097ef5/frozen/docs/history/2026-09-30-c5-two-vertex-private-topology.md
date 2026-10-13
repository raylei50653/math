# C₅ 私有內點接合的平面與原框可行性

2026-09-30。Git 基準 `e751c4b`；接手時已有主例拓撲的八份未提交
變更，予以保留。`main` 比本地 `origin/main` 多一筆提交；本輪未要求
也未執行 commit／push，未查驗遠端 SHA。

## 成果與停止點

- 新增[checker](../../scripts/c5_two_vertex_private_topology.py)、
  [companion artifact](../../artifacts/c5_two_vertex_overlap/private_topology.json)
  及[報告](../c5_two_vertex_private_topology.md)，只處理既有
  `private_interiors` 的十五點三十五邊與七個原私有內點。
- 完整環序見證有 22 面、70 條有向邊，Euler=2。指定六邊形外面後，
  兩來源各在自己的原 disk 內，兩 disk 內部互斥，只共用識別的兩點。
- A 原框由 B 路徑 a0–b2–a2 與 A 原內部
  a1–A_inner9–A_inner5–A_inner7–a3 阻斷；B 原框由 A 路徑
  a0–a1–a2 與 B 原內部 b0–B_inner6–b2 阻斷。
  兩組各自端點交錯且路徑互斥，排除所有以該原框作整圖外界的嵌入。
- 完整 J 仍為 60 軌道／1,440 份具名賦色，兩投影仍為 R127／R167。
  未排除 class 或刪減 relation；未遍歷此圖所有環序，未新增 Lean theorem。
- 更新兩點導覽、state 導覽、接合／主例報告後續狀態及 STATUS。README 的
  研究路徑與 HANDOFF 進行中標記不變，依 DOCUMENTATION 不逐輪改寫。

新 artifact 為 52,791 bytes，未達大型檔門檻。原點對、六例接合與
主例拓撲 artifacts 都未重寫。下一窄題由[導覽](../c5_two_vertex_overlap_guide.md)
維護：反向雙射 `private_interiors_reverse` 的具名拓撲核對；保留其與
正向完整 J 不同的事實，不從相同軌道數或投影 mask 合併兩例。

## 驗證

```bash
python3 scripts/c5_two_vertex_private_topology.py
python3 scripts/c5_two_vertex_private_topology.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_private_topology.py --check
python3 scripts/c5_two_vertex_join.py --check
python3 scripts/c5_two_vertex_overlap.py --check
python3 scripts/c5_two_vertex_join_topology.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

新 artifact 產生及兩次逐 byte 重播通過；完整八點賦色加七原內點
backtracking、兩投影及 60 份全圖 witnesses 均一致。原六份接合、
132 類／1,320 點對及主例 36 環序／24 外面配置重播亦通過。

`lake build` 通過 8,827 jobs，只有既有 AttachmentOrder／SymRelabel
linter warnings；本輪沒有新增或修改 Lean 檔案。文件檢查通過
370 份 Markdown／3,767 個本地連結；DocGraph 通過 62 documents／
213 relations／5 families，零 errors／notes。`git diff --check` 及八份
新檔的最終換行／尾端空白檢查通過。

環序探索讀取本機 NetworkX 3.6.1 快取；預設 uv 嘗試因快取唯讀而
未啟動，改採只讀匯入。正式 checker 不依賴 NetworkX 或探索暫存檔。
未修改 requirements、未安裝依賴。

未重跑來源圖大枚舉、代表最小性、其他研究線、Lean axiom audit 或
完整後繼表；未替反向接合圖建立拓撲證書。
