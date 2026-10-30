# 雙色唯一缺口：紙面證明、BR 共同接入與整理

2026-10-11；開始整理時 HEAD 為 `fdbef272c9f74ed95a4dac644b1c7f8b071a7722`。
使用者要求整理前一輪證明、commit 並提供相關文件位置；本輪授權為本地 commit。

## 1. 成果與證據層

權威新論證為 [雙色唯一缺口的 bridge 路徑定理](../archive/reports/c5/structure/c5_two_color_single_gap_bridge.md)。
在任意有限連通簡單圖的不可著色 degree lists 下，S 是 C−r 的完整分量，
S−{q} 的 lists 均含 T、D，而 q 含 T 缺 D，則 r 只有一個 S-contact，
且 r–q 的全部路徑 blocks 都是原 bridges。色集不必限四色。

一般 exclusive-block 森林的完整分量滿足原缺口數
`2+Σ_K(|V(K)|−2)`；限制到 S 側時，另以出口葉 r 的 indicator 正確計數。
新證明不假定 r 的原 list 缺色，不把割點 list 含 D 傳給全部 incident palettes。

同一原 M 的完整 degree／拒絕／延拓映射，把 actual 異色 pair、唯一 s-contact q、
至少兩個原 r-contacts 的 S 全部排除；BR-SD-1a／1c／1e／1g 是四個既有特例。
任意有限旁支數、位置、三環形狀與 private witness 不再是這個共同推論的必要參數。
完整原來源合同與四份歷史獨立採納不改寫；本輪新共同論證是紙面結果，未另經獨立審查。
外部信任為 Dvořák Theorem 10；封存 PDF 的 SHA256 已重新核對，見新報告§2。
新增 Lean theorem、有限來源實現及有限枚舉證書均為0。

## 2. 文件與反向核對

- Updated：新報告；N45§2.12 的共同接入與§3的精確 residual；degree-5 guide；
  degree-5 interfaces／Kempe guide 的直接 consumer；STATUS 對應索引與本紀錄。
- Reviewed-unchanged：README／HANDOFF 的研究線 routing，無研究線增減；
  Phase B／common-language／synthesis 的一般 N45／N2／E 仍 OPEN；
  complexity 盤點明確排除 BR-SD 子域，無需改七個身份的統計。
- Remaining OPEN：單一 r-contact、多個 s-contacts、未證雙色情形的非 pair support、
  不完整 S／其他內部出口及更廣父身份；R31 minor 義務不由本證明替代。
- Propagation stop：L2。共同推論改變 BR residual 的形狀分類，但沒有完成一般父題；
  不展開全線快照或重新枚舉。

開始整理時 README、HANDOFF、STATUS、Kempe guide、synthesis 已有其他修改。
本次只提交本成果的相連變更；共用文件採逐差異 staging，保留既有未提交內容。
沒有委派代理、改寫 audit／seal 或執行遠端 push。

## 3. 本輪驗證

| 實際執行命令 | 結果與界線 |
| --- | --- |
| `python3 -B scripts/check_docs.py` | PASS；612 Markdown files、7,538 local links，anchors／index／handoff 均通過 |
| `python3 -B tools/docgraph --include 'docs/**/*.md' check` | PASS；62 documents、213 relations、5 families，0 errors／notes；範圍為正式 docs |
| `lake build` | PASS；8,831 jobs，只有既有 AttachmentOrder／SymRelabel linter warnings；沒有新增 Lean 證明 |
| `git diff --check` | PASS；本輪文件變更無 whitespace errors |
| `sha256sum audits/2026-10-11-br-sd-1g-dbdc4c35/external/gallai.pdf` | 與新報告§2及既有 SOURCE 記錄一致 |

本次沒有新的 executable 數學 checker；紙面一般量詞由新報告§3–4承擔。
既有 BR source controls、獨立採納 verifier 及來源搜尋不重跑，亦不宣稱其新驗收。
