# 接手與 D₁₃ 密封替換形式化紀錄

日期：2026-10-02。使用者要求確認接手、選方向並開始推進。
基準 `8b91f9f`，起始工作樹乾淨；讀取 HANDOFF、STATUS、兩條進行中
導覽及最新 CommonRepair 形式化報告後，選定 D₁₃ 的局部圖關係與
密封替換，未重啟 class-pair 或來源骨架枚舉。

專題報告見 [Lean 四接點與密封替換](../lean_sealed_four_port.md)，
下一接口及圖論停止點由 [Lean 導覽](../lean_guide.md)與
[兩點重疊導覽](../c5_two_vertex_overlap_guide.md)維護。

## 成果與證據界線

新增 [SealedFourPort.lean](../../Math/SealedFourPort.lean) 及
[22條 axiom audit](../../Math/SealedFourPortAudit.lean)，由
[Math.lean](../../Math.lean) 匯入。原32邊逐一接到 `Proper`／`graphOfEdges`，
證 D₁₃ 與四輪星完整具名四接點等價。密封模型直接量化九個／一個
內點，證任意共同外部關係下整份外部染色不變，再推任意外部投影相等。
額外證明中心作第五接點失效，以及刪邊4–6後接受四色框。

22 條定理至多依賴 `propext`、`Classical.choice`、`Quot.sound`；
無 `sorryAx`、`Lean.ofReduceBool`、新增 axioms 或 `native_decide`。
小型有限色引理與固定接線檢查使用 kernel `decide`。
disk 嵌入、來源族／ownership、可用框、J/P 及 W／C 具體實例仍未
形式化；一般出口與 `K∞=K≤5` 未證。

## 驗證與來源對照

```bash
python3 scripts/c5_two_vertex_repair_caps.py --check
lake build
lake env lean Math/SealedFourPortAudit.lean
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

原 D₁₃ checker 通過8圖、11,520份完整延拓、88份稀疏延拓及16項
負控制，artifact 逐 byte 相同。舊 `new_lean_theorem=false` 保留原輪次
語境，不改既有證書或來源 hash。

`lake build` 通過8,829 jobs；新模組無警告，僅回放既有
AttachmentOrder／SymRelabel 警告。22 條 axiom audit 全通過。
文件檢查通過406份 Markdown／4,127個本地連結、錨點、索引與 HANDOFF
格式；DocGraph 通過62份文件／213條關係／五個 families，零 errors／notes。
`git diff --check` 及新檔 whitespace 檢查通過。

另以以下只讀對照核對 Lean 的具名邊表與既存 JSON 完全相同；
這是資料匯入的 Python 來源核對，與 Lean 定理的 kernel 驗證分開。

```bash
python3 - <<'PY'
from pathlib import Path
import ast, json, re
text = Path('Math/SealedFourPort.lean').read_text()
match = re.search(r'def capEdges.*?:=\s*(\[.*?\])', text, re.S)
edges = ast.literal_eval(match[1])
saved = json.loads(Path('artifacts/c5_two_vertex_overlap/repair_caps.json').read_text())
assert edges == [tuple(e) for e in saved['local_certificate']['edges']]
assert len(edges) == len(set(edges)) == 32
assert all(0 <= u < v < 13 for u, v in edges)
print('All 32 named D13 edges agree.')
PY
```

未重跑其他來源族、大枚舉、CommonRepair Python checker 或其他
Lean 模組的獨立 audit；未 `lake update`，未重新生成 artifacts。
依[文件治理](../DOCUMENTATION.md)更新專題報告、兩條導覽、README
及 STATUS。研究線與 tags 未變，HANDOFF 保持原薄索引。
本輪未要求或執行 commit／push。
