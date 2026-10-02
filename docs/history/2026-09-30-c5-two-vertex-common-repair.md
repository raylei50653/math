# 2026-09-30：共同 repair 充要 lemma

接手基準 `6f8b3c3`，工作樹乾淨。依使用者選定方向，將六例 transport
audit 的共同公式抽成 witness／覆蓋前提明確的 lemma，四個 P=J 案例
保留為退化支。未搜尋新 class pair，未修改 Lean，未 commit／push。
現況由[兩點重疊導覽](../c5_two_vertex_overlap_guide.md)維護；
完整前提與證明見[專題報告](../c5_two_vertex_common_repair.md)。

## 成果與證據

對 J⊆P 及保留 J 的有限候選條件集，三種 exact rejector witnesses
`{A}`、`{B,T}`、`{B}∪𝓔` 與兩類完整覆蓋等式，充要刻畫全部 repairs
為 `{A,B}` 或某個 `{A,T,E}` 的上閉包。反向由三個極大失敗集合抽出
witnesses；每例三個 witnesses 可統一證明全部極小解的逐項不可省性。
退化 lemma 單獨給出 P=J 時唯一空極小 repair，不設 forced core。

紙面 lemma 不要求 Ω 有限或候選條件為四點投影；它不給 arity 下界、
逐染色換色操作或來源圖的普遍性。既有兩例 r*=4 仍依獨立三點下界。

- [新 checker](../../scripts/c5_two_vertex_common_repair.py)：標準函式庫，
  從原代表及整圖染色重建六份 J/P，重驗可用框證書；由具名角色先驗前提，
  之後才比對前輪極小 repair 分類。
- [新證書](../../artifacts/c5_two_vertex_overlap/common_repair.json)：151,000 bytes，
  六個 witness、30份完整覆蓋等式、384份接受 scope 原圖延拓、12份 frame
  延拓、88次共用 witness 的逐項刪除核對；四例 J=P 及空 repair 分支。
- 保存三個極大失敗集合的完整殘留，正／反向軌道數分別為
  `4,4,26`／`4,2,26`，未混同完整排除資料。
- 五個抽象小模型逐一只違反一條 W／C 前提，其他四條成立，完整枚舉
  32個 scope 子集合確證答案改變；verifier 均拒絕。它們不是 disk 圖實現。

## 驗證

生成器、一般及 `PYTHONHASHSEED=17` 的新 `--check` 均逐 byte 通過；
既有 transport checker 的 `--check` 通過，六份原圖／全部二十候選框、
arity ladder、完整修復分類及前輪八十八份刪除見證由該 checker 重播。

`lake build` 通過8,827 jobs，只有既有 AttachmentOrder／SymRelabel
linter warnings；這不表示新紙面 lemma 已 Lean 化。
文件檢查通過389份 Markdown／3,953個本地連結；DocGraph 通過
62 documents／213 relations／5 families，零 errors／notes。
`git diff --check` 及新檔的 whitespace／final-newline 檢查通過。

```bash
python3 scripts/c5_two_vertex_common_repair.py
python3 scripts/c5_two_vertex_common_repair.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_common_repair.py --check
python3 scripts/c5_two_vertex_repair_transport.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

未重跑來源大枚舉、class 最小性、獨立舊單框／拓撲 checkers 或大型三點／
四點 standalone checkers，未作 Lean axiom audit。原六圖、transport 與
所有舊 artifacts 保留原 bytes，來源 hash 鏈核對；新證書小於1 MB，
無須修改 manifest／gitignore。

更新專題報告、原 transport 的後續狀態、兩點重疊／state 導覽與 STATUS。
依文件治理，研究線與基本入口未變，README／HANDOFF 不追加逐輪摘要。
停止點是抽象 lemma 與固定六圖實例完成；下一個窄題為保證 W／C 前提的
可檢查來源結構。一般後繼表、多步充分性、完整 Σ 及 K∞=K≤5 仍未證。
