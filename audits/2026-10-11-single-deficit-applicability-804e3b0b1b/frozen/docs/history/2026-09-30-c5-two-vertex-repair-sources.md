# 2026-09-30：共同 repair 的來源充分條件

接手 HEAD `6f8b3c3`，共同 repair lemma 的 checker、證書與文件已在工作樹，
尚未提交。本輪保留該批成果，依使用者指示推進保證 W／C 的可檢查來源
結構。未 commit／push，未開 sub-agents，未新增 class-pair 搜尋。
現況由[兩點重疊導覽](../c5_two_vertex_overlap_guide.md)維護；
完整前提與證明見[來源報告](../c5_two_vertex_repair_sources.md)。

## 新成果

- 保留原 A 五內點路徑及 B 兩相鄰內點的全部附件，直接由可用色證明
  兩側完整延拓公式；不依賴來源 mask 計數作充分性證明。
- 每個方向十一份構造補全，以改動點集合證明全部七十 scopes 的三種
  exact rejector witnesses；色數論證統一證明十五份覆蓋等式。
- 指定 induced 核心、來源 ownership、密封私有點的度數至多三消去與
  兩混合框／原來源 disk 的 rotation 證書，保證任意有限大小來源的
  完整 J/P 與核心相同。全部十五組極小 repairs 與 r*=4 因而保留。
  任意大小來自紙面反向接回歸納；有限較大圖只作控制。
- 任意兩來源的精確兩點接合，若兩原框都可作整圖外界，則 P=J，
  唯一極小 repair 為空集合；不需指定核心或消去條件。

這些都是充分條件；未證所有同 class disk 代表可化到指定核心，未證
來源條件必要。未新增 Lean theorem、`native_decide` 或外部染色定理。

## 證書與驗證

[新 checker](../../scripts/c5_two_vertex_repair_sources.py)使用標準函式庫；
[新證書](../../artifacts/c5_two_vertex_overlap/repair_sources.json)為94,052 bytes，
保存原六圖核對、兩個增加六私有內點的二十一點圖、完整原邊與 rotations、
消去次序／鄰點、稀疏補全及全圖染色、完整 J/P/Δ 軌道關係。
四個非平凡控制各1,440份 J 都以構造法延拓，共5,760份。
十二個負控制均被拒絕，含確實改變 J 的度數四 star 見證。

以下均實際通過：

```bash
python3 scripts/c5_two_vertex_repair_sources.py
python3 scripts/c5_two_vertex_repair_sources.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_repair_sources.py --check
python3 scripts/c5_two_vertex_common_repair.py --check
python3 scripts/c5_two_vertex_repair_transport.py --check
lake build
```

既有共同 lemma 重播六圖、384份接受 scope 延拓及88次統一不可省核對；
transport 重播六圖／二十候選框／十四可用框／完整 repairs 及88份刪除見證。
`lake build` 通過8,827 jobs，只有既有 SymRelabel／AttachmentOrder
linter warnings；新來源定理仍未 Lean 化。

文件檢查通過391份 Markdown／3,973個本地連結；DocGraph 通過
62 documents／213 relations／5 families，零 errors／notes。
`git diff --check` 及新檔的 whitespace／final-newline 核對通過。
未重跑來源大枚舉、class 最小性、獨立舊單框／拓撲 checkers 或大型三點／
四點 standalone checkers；未作 Lean axiom audit。既有 artifacts 保留原 bytes，
本輪只新增來源證書；小於1 MB，無須修改 manifest／gitignore。

更新新報告、共同 lemma 的後續入口、兩點重疊／state 導覽及 STATUS。
依文件治理，README／HANDOFF 的研究線與基本入口不變，不追加逐輪摘要。
停止點為指定來源族的充分定理；下一窄題是不能作該私有消去的其他來源
結構，須保留完整附件來構造 witness／覆蓋。一般出口及 K∞=K≤5 仍未證。
