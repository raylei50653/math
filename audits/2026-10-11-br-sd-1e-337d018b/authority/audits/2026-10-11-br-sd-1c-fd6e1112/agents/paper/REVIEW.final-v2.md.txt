# BR-SD-1c：最終 PROOF／REPORT 整合審查

日期：2026-10-11。Reviewer：paper worker。研究 BASE：`fd6e1112e6f5e9fd23c50d2f3b5d2ef874954d69`。

本次精確接受的 bytes：

| 審查輸入 | SHA256 |
| --- | --- |
| 父端 PROOF.md | `abbdfcd48eadb2e2ca56ad74802c4ca21a98394d54b8b114aec27ebc58a5c4f0` |
| 父端 REPORT.md | `937262167c4011abec6f2297ec26468a07e028b7bb4d058fd16bcae7917e86ec` |
| 原接受版本 PROOF.reviewed-v2.md | `e3f88f1a01c12b6c428b829e215ee33d59185fa7dbd57f3c56548277867d23d5` |

判定：**接受最終 PROOF 的 scoped one-W 任意大小來源排除及明列前提的局部引理；
接受 REPORT 的數學 scope、控制數值與證據分層陳述。沒有新增紙面或 scope finding。**
Prior PAPER／REVIEW／REVIEW.final 與受審版本都保存，不覆寫。

## PROOF 的最終變動

與 PROOF.reviewed-v2.md 逐行 diff 後，只有§7 controls 導航由原 REPORT.md
改為 REPORT.v2.md；所有定理前提、lists、palette 分解、q 臂三案及 scope 句子完全相同。
原 REVIEW.final 已接受的 terminal q／臂內點無額外 C 邊條件仍完整明列。
不存在只由更新導航而改變數學結論的情形。

## REPORT 對回 PROOF

完整讀取 REPORT，逐項核其精確前提、核心四步、獨立審查紀錄、finite controls 表、
來源狀態與 remaining OPEN：

- 研究量詞是同一 N45-S-NOU-LS-PAIR／split22 來源家族：原骨架再有一份來源自己的 W
  接在 J1/J2，完整保原 G／M 身份及 actual S pair support。沒有把已 degree4 舊圖任意增邊。
- 覆蓋所有 x 位置的理由足夠：r degree 排除；其他合法接點由 untouched J3／q 臂的 actual
  pair-supported palette 矛盾排除，包含 triangles、a3=v、任意奇環長、原臂長與有限 W 大小。
- REPORT 明列局部引理必要前提，包括實際 pair 附件、未佔用的私有環點、bridge 臂及
  臂端點無其他 C 邊；沒有將 generic cutpoint D-presence 誤報為對所有 Gallai trees 有效的傳遞。
- 前三個 finite M 接受 β，第四個拒絕但撤去 pair support。報告沒有把 normal fixtures
  當作拒絕來源，也沒有將負控制升格 actual disk 反例。
- 完整父身份、一般三環／Gallai trees／非二連通來源、R31、55、ε≥3、主命題仍 OPEN；
  canonical 採納、actual source realization、Lean 與 finite evidence 均明確分開。

## 控制資料與重播紀錄核對

讀取 controls REPORT.v2、root-controls-checks.json、六份 root stdout／stderr raw logs，
並直接讀取 normal／seed17 原 JSON 證書與 corruption-mutation.json。
沒有再跑枚舉、重生證書或覆寫控制產物。

| 核對項 | 結果 |
| --- | --- |
| 四份固定 C | 每份10點12邊，與 REPORT 表／raw checker log 相符 |
| normal／seed17 證書 bytes | byte-equal，皆87402 bytes |
| normal／seed17 SHA256 | 皆 `0b2193d4d13f715272f78f3df2431aca915efd2dd77f60ef52de3549d230906a` |
| 四份完整 M-β fibres 數 | 54／12／48／0，原 JSON summary 與兩 checker logs 一致 |
| S actual pair flags | true／true／false／false；negative 與 J2 leaf fixture 皆碰 B0/B1/B4 |
| root checker normal／seed17 | root execution record exit0，raw logs 相同並保存完整 counts |
| independent_edges normal／seed17 | root execution record exit0，raw logs 相同並保存 actual supports／query counts |
| corrupted tuple | 原 mutation 明記1→9，與 REPORT.v2 更正一致 |
| root checker corruption | expected exit1、actual exit1，stderr `illegal complete coloring tuple` |
| independent_edges corruption | expected exit1、actual exit1，stderr AssertionError |
| actual source 層 | 證書全部 `not triggered`；disk embedding 明記未提交／未宣稱 |

另讀 independent_edges.py，確認只 import 標準函式庫；C／附件／lists／contact fibres
從 supplied M 原邊重建，回溯固定原點序，完整 tuple sets 與 M/G lifts 逐集合比較。
它不 import checker.py，也沒有直接借第一份 solver 的 list assignment 作新回溯的輸入。
本次沒有重新審查兩 solver 的一般 correctness；它們只負責這四份固定域的校準，
任意大小結論仍由紙面 PROOF 承擔。

docs-checks.json 亦與 REPORT 的既有正式文件檢查數值相符：600 Markdown／7353 links、
62 docs／213 relations／0 errors、git whitespace exit0。REPORT 正確說明這些 checks
不掃新 audit 連結或決定數學真假。

## 最後驗證的分工與限制

REPORT 所列 authority custody、BASE blobs、舊89份 audit bytes、exclusive output、
seal-v1／validation 最終核對，將由 root 在加入本審查後跑 final verifier。
本次沒有獨立重算那些 custody 集合，也沒有把當時尚待生成的 seal／validation
導航當作完成的數學證據。接受 scope／evidence 陳述不代替 root 的最後 bytes／links 檢查。

最終 acceptance 不授權 canonical 修改、commit、push 或外部發布。
本 worker 本次只新增專屬目錄 REVIEW.final-v2.md。
