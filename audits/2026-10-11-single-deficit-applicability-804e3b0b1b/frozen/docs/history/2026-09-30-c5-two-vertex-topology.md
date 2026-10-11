# C₅ 兩點接合主例的原框與區域拓撲

2026-09-30。Git 基準 `e751c4b`，接手時工作樹乾淨，`main` 比本地
`origin/main` 多一筆提交。依最新接合成果推進其明列的主例拓撲缺口；
本輪未要求也未執行 commit／push，沒有查驗遠端 SHA。

## 成果及界線

- 新增[拓撲 checker](../../scripts/c5_two_vertex_join_topology.py)、
  [companion artifact](../../artifacts/c5_two_vertex_overlap/reference_topology.json)
  及[報告](../c5_two_vertex_join_topology.md)。只讀取既有 `reference`
  的同一八點十邊圖；舊接合與點對 artifacts 未重寫。
- 四條原路徑的全部 36 組端點環序中，六份為球面嵌入。各指定四種
  外面，得到 24 份具名配置：內部互斥 8、B⊊A 4、A⊊B 4、真正重疊 8。
  A、B 原框各自可作整圖外界，同一平面配置不能同時以兩框為整圖外界。
- 每份配置保存具名環序、逐面串、原框方向的左／右側、有界 disk 面集
  及逐原邊 inside／outside／boundary。一般 transition 政策仍 unknown；
  若明定兩 disk 內部互斥，恰八份符合。
- 原圖只有六條 simple cycles，長度 3、4、5、5、6、7，沒有含全部
  八個接口點的 simple 外框。完整八點 relation 保留原 140 軌道，
  A=R1016／B=R1023；65,536 份賦色另以逐實際邊檢查完整重算。
- 證據是紙面拓撲與 Python 固定圖證書，沒有新增 Lean theorem；
  不外推到同 Σ 所有圖實現，也不將其餘五例 geometry 改為已驗證。

Artifact 為 149,660 bytes，未達大型檔門檻，不改 manifest。
更新主例報告、舊接合報告的後續狀態、兩點導覽、state 導覽及 STATUS。
研究入口及進行中標記沒有改變，依 DOCUMENTATION 不逐輪改寫 README／HANDOFF。

## 驗證

```bash
python3 scripts/c5_two_vertex_join_topology.py
python3 scripts/c5_two_vertex_join_topology.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_join_topology.py --check
python3 scripts/c5_two_vertex_join.py --check
python3 scripts/c5_two_vertex_overlap.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

新 artifact 產生、一般及不同 hash seed 的只讀逐 byte 重播通過；
舊六例的完整接合／整圖染色，以及 132 類／1,320 點對重播均通過。
`lake build` 通過 8,827 jobs，只有原 AttachmentOrder／SymRelabel
linter warnings。沒有新增或修改 Lean 檔案，未跑 axiom audit。

文件檢查通過 368 份 Markdown／3,749 個本地連結；DocGraph 通過
62 documents／213 relations／5 families，零 errors／notes。
`git diff --check` 及四份新檔的尾端空白／最終換行檢查通過。
未重跑來源圖大枚舉、目錄最小性、weak-deletion／其他研究線或完整後繼表。

## 停止點

主例固定圖的抽象平面性、原 A／B disk 外框及區域側別已完成。
下一個窄題是既有 `private_interiors`：R127 `(0,2)` 接 R167 `(1,3)`，
保留十五點三十五邊與七個原私有內點，判定兩原框可行性；見
[導覽](../c5_two_vertex_overlap_guide.md)。一般接合政策、多步充分性、
任意大小目錄完備性及 `K∞=K≤5` 保留。
