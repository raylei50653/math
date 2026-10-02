# 2026-09-30：不能逐點消去的來源與密封 clique 補片

接手 HEAD `6f8b3c3`；共同 repair lemma 與來源充分定理的未提交成果
已在工作樹，全部保留。使用者要求推進不能作私有度數三消去的來源
代表。本輪未 commit／push，未開 sub-agents，未搜尋新 class pair。
現況見[研究線導覽](../c5_two_vertex_overlap_guide.md)，完整前提、證明及
反例見[補片報告](../c5_two_vertex_repair_patches.md)。

## 新成果及證據邊界

- 任意大小的密封 clique 補片引理：G−H 每個完整分量的全部附件是
  核心的至多三點 clique 時，一份正常四色染色足以延拓 H 的每份染色。
  同時對齊共用接點的同一份核心色框，保持全部核心顏色。
- 原 A／B 核心的十三／七個內面皆三角形。保核心的來源 disk 擴張
  自動具有 clique 附件；不需要補片插入歷史或逐點消去順序。
- 配合完整整圖外框 rotations，保持 J、P、十五組極小 repairs 及 r*=4。
  六圖新增點最低度數四或五，任意保核心度數三消去都無第一步，故
  舊消去條件不是必要條件。反覆私有面填入二十面體給任意大小族。
- 非 clique 兩接點補片及四接點 disk star 各有完整 relation 反例，
  說明不能省略實際附件條件。沒有完成全部同 class 來源代表的必要分類。

任意大小為紙面證明，有限圖為 Python 控制；未引用四色定理、未新增
Lean theorem／`native_decide`。`lake build` 不把新染色或 topology 證明
升格為形式化結果。

## 新證書與實際檢查

[checker](../../scripts/c5_two_vertex_repair_patches.py)與
[artifact](../../artifacts/c5_two_vertex_overlap/repair_patches.json)使用標準
函式庫，證書182,368 bytes。兩方向各21／33／51點圖，共六圖，保留
全部原邊、密封分量及完整附件、來源 ownership、一份正常染色、全部
候選框肯定／否定證書、完整 J/P/Δ 及具名 repair scopes。

各圖獨立掃全部 `4^8` 並依原邊回溯，不讀來源公式作染色 oracle。
另核對8,640份構造全圖延拓、66份完整稀疏補全、兩補片全部48份三角形
賦色、十二項負控制，以及兩個完整附件反例。兩層補片按每側十八個
額外點的完整分量處理，沒有拆成獨立換色的局部片段。

以下均實際通過：

```bash
python3 scripts/c5_two_vertex_repair_patches.py
python3 scripts/c5_two_vertex_repair_patches.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_repair_patches.py --check
python3 scripts/c5_two_vertex_repair_sources.py --check
python3 scripts/c5_two_vertex_common_repair.py --check
python3 scripts/c5_two_vertex_repair_transport.py --check
lake build
```

舊來源證書重播原六圖、兩個增大控制、5,760份構造延拓及十二項負控制；
共同 lemma 重播六圖、384份接受 scope 延拓、88次不可省核對；transport
重播二十候選框、十四可用框及完整 repairs。`lake build` 通過8,827 jobs，
只有既有 AttachmentOrder／SymRelabel linter warnings。

`python3 scripts/check_docs.py` 通過393份 Markdown／3,992個本地連結，
含 anchors、索引覆蓋與 HANDOFF 檢查；`python3 tools/docgraph check`
通過62 documents／213 relations／5 families，零 errors／notes。
`git diff --check` 與新檔／修改未追蹤報告的 whitespace、final-newline
檢查通過。

未重跑來源大枚舉、class 最小性、獨立舊單框／拓撲與大型三點／四點
standalone checkers，未作 Lean axiom audit。舊 artifacts 保留原 bytes；
新 artifact 小於1 MB，不改 manifest／gitignore。

## 交接與下一個窄問題

新增補片報告與歷史；更新來源報告的後續註記、兩點重疊／state 導覽
及 STATUS。依文件治理，README／HANDOFF 的研究線與基本入口不變。

停止點為保指定三角剖分核心、密封完整 clique 附件、一份染色及保框
證書的任意大小來源定理。下一窄題是不含此核心或化約後留下不同骨架
的同 class disk 代表；仍須保留完整附件、來源 ownership、共同色框
與可用框，另證完整補全／覆蓋。一般出口與 `K∞=K≤5` 仍未證。
