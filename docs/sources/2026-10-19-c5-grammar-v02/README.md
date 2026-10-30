# C₅ P/R 文法 v0.2：附件匯入說明

匯入日期：2026-10-19。來源為使用者提供的三個附件；原檔逐位元組保存。
本頁是項目的整理入口，**不是附件原本引用但未隨附的 README.md**。
附件中的執行敘述及 `pass: true` 屬來源紀錄；本輪核對範圍另列如下。

後續（2026-10-19）：[四列三步觀察與十列解碼](../../../audits/2026-10-19-c5-observation-depth-ed59843/REPORT.md)
新增獨立重播及紙面代數證明：RR／PRR／RRR三探測還原完整支援，最小統一深度恰3。
這項後續以所附矩陣為定義，仍未重播原圖構造與完整 fibre 驗證；下文保留匯入時紀錄。

## 檔案與來源

| 檔案 | 用途 |
| --- | --- |
| [RESULTS.md](RESULTS.md) | 原始成果摘要、範圍與未跨越的界線 |
| [certificate_v02.json](certificate_v02.json) | `boundary-grammar-certificates/v2`；模型、可達性、最小成本、細分及控制資料 |
| [verification_v02.json](verification_v02.json) | 來源所附的驗證結果及 22 項污染拒絕原因 |
| [SHA256SUMS](SHA256SUMS) | 上述三份原檔的 SHA-256 |
| [IMPORT.json](IMPORT.json) | 匯入來源、當時 HEAD、大小、雜湊、本地核對與缺件紀錄 |

證書的 `provenance.legacy_commit` 為
`ed59843ff8aad66cf3dd895da101787b3daec7a0`，與匯入時項目 HEAD 相同。
`legacy_certificate_sha256` 為來源自述，本輪未識別及核對其對應舊證書。
原文的「沒有修改或推送 repository」及證書中的相應欄位描述來源生成時的狀態，
不是本次匯入後的工作樹狀態。

## 附件結果與適用範圍

以下數字已對所附有限模型核對；圖構造語義及原完整驗證流程尚待原程式補齊。

| 項目 | 所附模型的結果 | 範圍 |
| --- | --- | --- |
| 狀態及轉移 | 132 個不同狀態、264 條 P/R 轉移 | 有序的目前 C₅ 外框；字母僅 P、R |
| 目標 319 | 56 Live、76 Dead | 任意有限 P/R 後綴的抽象轉移可達性 |
| 前綴排除 | `FPPPRP` 到 mask 1002；後續閉包 61 態皆在 Dead | 僅此前綴的文法族 |
| 其他目標 | 932、933、941 及四列聯合 predicate 各為 0 Live、132 Dead | 四列指接受 01232 且拒絕 01021、01202、01212 |
| 文法內最小代表 | F 文法最大最小內點數 6；F/C 文法為 5 | C 是另加的無弦 C₅ 種子；不保證內面全三角 |
| 四列觀察細分 | 15 → 66 → 97 → 132 | 保四列輸出及全部 P/R 後續 |
| 精確 319 觀察細分 | 最後 57 類：56 個 Live 單點類及一個 Dead 類 | 僅保指定目標的未來判斷 |

四列相同仍可有不同後繼：`FP` 與 `FPPPRR` 分別為 91、219，
目前四列均為 `(0,1,1,1)`；接同一個 R 後為 91、603，四列分別為
`(0,1,1,1)`、`(1,1,1,1)`。

這批資料與 [state／grammar 導覽](../../archive/guides/c5_state_guide.md)、
[完整 relation 語言](../../reference/interfaces/state_language.md)及
[C₅ 組合圖譜](../../archive/reports/c5/structure/c5_combinatorial_atlas.md)相接。
四列目標的原來源問題另見
[較寬替換接口](../../../audits/2026-10-18-abstraction-bottleneck-9f1fe84/REPORT.md)；
此處的文法族排除不替代該處所需的同一合法較小 disk、完整接合及來源證明。

## 本輪核對與重播界線

- 三份複本與附件逐位元組相同；兩份 JSON 可解析，狀態及全部轉移的域／值域閉合。
- 獨立核對所附抽象模型的 P/R 矩陣與轉移一致性、兩種種子閉包、Live／Dead、
  下降 rank／policy、61 態閉包、兩套最小成本及 witness、528 條 Bellman 不等式、
  兩種細分與區分例子；摘要數字一致。這是有限模型內部核對，未獨立建立操作的圖層語義。
- 原紀錄中的 5,120 份字面指派、792 個全圖案例、8,020 個 fibres、40＋31 項測試、
  22 項污染拒絕、seed17 逐位元組一致及 UI 檢查，均保存為**來源報告，未在本輪重播**。
- 缺件：原 README、圖構造／生成器／獨立驗證器程式碼、測試與污染輸入、HTML 及 UI 測試。
  因此目前不能提供原完整驗證流程的可執行重播命令。

從專案根目錄核對原檔完整性及 JSON 格式：

```bash
(cd docs/sources/2026-10-19-c5-grammar-v02 && sha256sum -c SHA256SUMS)
python3 -m json.tool docs/sources/2026-10-19-c5-grammar-v02/certificate_v02.json >/dev/null
python3 -m json.tool docs/sources/2026-10-19-c5-grammar-v02/verification_v02.json >/dev/null
```

文件檢查使用 `python3 scripts/check_docs.py`、
`python3 tools/docgraph --include 'docs/**/*.md' check` 及 `git diff --check`。
三項均通過；全工作樹 `python3 tools/docgraph check` 仍有 72 個既有重複 ID 錯誤，
錯誤輸出與匯入前逐字相同，詳細結果記於 `IMPORT.json`。
本輪是來源整理；未重跑研究枚舉或 Lean build。

## 保留界線與接續入口

P 改變目前外框的頂點身份，不能直接套用固定原 B 的保壞或單調性論證。
同支援不代表同圖、同著色計數或相同操作合法性；三角面插點不在此 P/R 字母域內。
319 在此僅是示範目標，不能因此稱為 bad 或推出一般 r6 原圖排除。

一般 C₅ disk／指定剩餘 r6 來源是否有此文法中的行為代表，以及主命題
`K∞=K≤5`，仍為 **OPEN**；本次沒有新增 Lean theorem 或文獻新穎性判定。
若接續驗證此包，先補齊上述原始程式與規格，再核對操作語義、完整 fibres 及原測試；
本研究線的當前停止點仍由 [state 導覽](../../archive/guides/c5_state_guide.md#3-停止點與保留缺口)維護。
