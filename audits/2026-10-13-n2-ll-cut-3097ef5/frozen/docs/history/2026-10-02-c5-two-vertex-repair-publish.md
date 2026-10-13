# C₅ 共同 repair 與來源替換族發布核對

日期：2026-10-02。依使用者要求 commit + push，發布既有共同 repair
lemma、來源充分條件、密封補片、私有路徑、輪環、偶長雙扇及 D₁₃
七份 checker／證書／專題報告／研究紀錄，連同導覽與 STATUS 更新。
本次推送亦包含既有本地提交 `6f8b3c3` 的六例 transport audit；
發布完成狀態以即時 Git 為準。目前入口及停止點見
[兩點重疊導覽](../c5_two_vertex_overlap_guide.md)。

## 範圍與證據界線

[共同 lemma](../c5_two_vertex_common_repair.md)以完整 witness／覆蓋
條件刻畫全部極小 repairs；[來源定理](../c5_two_vertex_repair_sources.md)
及後續指定替換族保留完整 J/P、十五組 repairs 與 r*=4。
最前沿為[D₁₃ 完整四接點替換](../c5_two_vertex_repair_caps.md)；
加入該規則後的其他骨架、全部代表必要分類與改寫完備性仍未完成。
一般大小結論由各報告紙面證明負責，Python 證書只核對明列有限控制；
沒有新增 Lean theorem。一般出口與 `K∞=K≤5` 仍未證。

本次只整理、重播及發布既有成果。七份新增 JSON 皆小於1 MB，直接
隨 Git 保存；不需新增 manifest 條目。研究線、tag 與基本使用方式
未變，依[文件治理](../DOCUMENTATION.md)保留 HANDOFF／README。
舊 transport 報告的後續說明補上來源定理連結，歷史正文保留。

## 本次重播命令

Python 3.14.7；八個 checker 均採 `PYTHONHASHSEED=17`，以 `--check`
重新計算並逐 byte 比對既存證書，不重寫來源或輸出：

```bash
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_common_repair.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_repair_sources.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_repair_patches.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_repair_strips.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_repair_rings.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_repair_fans.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_repair_caps.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_repair_transport.py --check
lake build
python3 tools/artifacts.py status
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --cached --check
```

以上八份證書重播均通過，包含 D₁₃ 八圖11,520份完整延拓及十六項
負控制。`lake build` 通過8,827 jobs，只有既有 `SymRelabel`／
`AttachmentOrder` linter warnings；不表示新紙面結果已形式化。
Artifact audit 為 `ok=103`，無 missing、changed 或 stale。
文件檢查通過402份 Markdown／4,075個本地連結、錨點、索引及
HANDOFF 格式；DocGraph 通過62份文件／213條關係／五個 families，
零 errors／notes。完整暫存發布包的 whitespace 檢查亦通過。

未重跑來源大枚舉、其餘研究線、較早八點接合／投影層的獨立 checker
或 Lean axiom audit；來源 hash 與本輪使用的完整關係由上述 checker
直接核對。此次不重新生成已登錄的大型 artifacts。
