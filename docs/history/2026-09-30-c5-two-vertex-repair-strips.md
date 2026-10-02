# 2026-09-30：不含舊核心的同 class 私有路徑族

接手 HEAD `6f8b3c3`；共同 repair、來源及密封補片成果已在未提交工作樹，
全部保留。本輪沿使用者指定的「不含指定核心或化約後不同骨架」缺口，
處理前一支的明列任意長度來源族。未 commit／push、未開 sub-agents，
未重啟來源大枚舉。現況見[導覽](../c5_two_vertex_overlap_guide.md)，
完整前提及證明見[奇偶定理](../c5_two_vertex_repair_strips.md)。

## 新成果及界線

- 保留兩來源全部實際附件，只改私有路徑長度。A 的兩臂 L,R≥2、
  B 的 K≥1 具有精確 relation 公式；在此接線族內，L,R 偶及 K 奇
  充要保持完整 R127／R167。任意長度證明使用二色交替與三色 path
  延拓，無外部染色定理。
- 加長後不含保持框點及 ownership 的舊核心子圖副本。紙面由唯一
  端點附件及私有路徑距離排除，有限 checker 另窮盡子圖單射；不是
  單純換名或只驗指定標號。私有最低度數四，度數三消去無第一步。
- 兩個三角面內的路徑施工延伸完整 rotations；舊三個阻斷框的交錯
  路徑沿 subdivision 保留。全部可用框恰為原兩個，故 J/P 相同，
  全部十五組 repairs 及 r*=4 不變。
- 固定 hub、原私有端點的四點 relation 在局部替換下可能嚴格增大；
  保存 `0011` 的原邊反例。保真性限整個來源的原五框，不能當任意
  四接點替換，也不容許未來額外觀察已密封私有點。

本輪證成「含舊核心＋密封補片」也不是必要條件。但新來源可用已證的
整來源奇偶化約回舊骨架，沒有處理所有化約後仍為不同骨架的代表。
必要分類、一般接合政策、多步 state、一般出口與 `K∞=K≤5` 仍未證。
紙面與 Python 分開；沒有新 Lean theorem／`native_decide`。

## 證書與實際驗證

[checker](../../scripts/c5_two_vertex_repair_strips.py) 使用標準函式庫，
[artifact](../../artifacts/c5_two_vertex_overlap/repair_strips.json) 為348,316 bytes，
保存全部圖邊、ownership、完整私有路徑、來源 relation、rotations／交錯
路徑、完整 J/P/Δ、repair scopes、稀疏完整補全及 class 分離賦色。

兩方向各核對 `(4,2,1)`、`(2,4,1)`、`(2,2,3)`、`(4,4,3)`、`(6,8,5)`，
共十個17／21／29點圖。每圖獨立由原邊掃全部 `4^8`、另核對兩份
`4^5` 來源，與 path 公式及自然接合作完整集合相等比較。合計14,400份
構造全圖延拓、110份稀疏補全、八個奇偶控制、十二項結構負控制及一個
完整四接點反例。沒有用舊核心染色作新圖接受／拒絕 oracle。

本輪實際通過：

```bash
python3 scripts/c5_two_vertex_repair_strips.py
python3 scripts/c5_two_vertex_repair_strips.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_repair_strips.py --check
python3 scripts/c5_two_vertex_repair_patches.py --check
python3 scripts/c5_two_vertex_repair_sources.py --check
python3 scripts/c5_two_vertex_common_repair.py --check
python3 scripts/c5_two_vertex_repair_transport.py --check
lake build
```

`lake build` 通過8,827 jobs，只有既有 AttachmentOrder／SymRelabel linter
warnings；不表示新紙面染色及拓撲證明已形式化。重播既有補片六圖／
8,640延拓、來源5,760延拓、共同 lemma 六圖／384延拓及 transport 六圖／
二十候選框，全部通過，舊 artifacts 未改寫。

一般與 `PYTHONHASHSEED=17` 的新 checker 逐 byte 重播均通過。
`python3 scripts/check_docs.py` 通過395份 Markdown／4,010個本地連結，
含 anchors、索引與 HANDOFF；`python3 tools/docgraph check` 通過
62 documents／213 relations／5 families，零 errors／notes。
`git diff --check` 及新檔的行尾空白、final-newline 檢查通過。

未重跑來源大枚舉、class 最小性、各單框與大型三點／四點 standalone
checkers，未作 Lean axiom audit。它們仍保留原證據，未聲稱本輪重驗。

## 文件及交接

新增定理報告、checker、artifact 及本紀錄；更新補片報告後續註記、
兩點重疊／state 導覽及 STATUS。依文件治理，README／HANDOFF 的研究線
與基本入口未改變，不追加逐輪摘要。新 artifact 小於1 MB，無需 manifest
或 gitignore 變更。

停止點：指定完整接線路徑族已完成任意長度的必要及充分奇偶分類。
下一窄題是密封 clique 補片與此整來源奇偶化約之後，仍留下其他骨架
的同 class disk 代表；須繼續保留完整附件、來源 ownership、共同色框
及全部可用框。沒有證明全部同 class 代表必有上述化約。
