# 九組本地 commit 與研究現況

日期：2026-10-13。整理 BASE `6943561e644e7598342d1ccd7df44dac0ebcd5cf`
之後的現有工作，按五組隔離 audit 與四組文件內容建立九個本地 commit。
本批只做本地提交；即時提交及工作區狀態以 Git 為準。原 audit 的「未
commit／push」描述其研究完成截點，凍結輸入、seal 及歷史 receipts 均保留。

## 提交分組

| Commit | 範圍 |
| --- | --- |
| `ab62720` | 相對來源可染性、cap 接合、同時 gadget 預算與代表下界 |
| `8228e48` | no4ct 全內部 W5 前提、C8 端部與 h=4 C9 frontier |
| `470b1b8` | C8 完整 joint／signed gadget、共同計數與 Kempe cone 控制 |
| `4ebb16c` | C8 pocket 化約、六私人點殘留核心 |
| `4e50db9` | C6 三型完備接線與指定 C8 gadget 預算域收尾 |
| `0e004c0` | N2／N45 覆蓋鏈、原 E4 橋接與父題 OPEN 界線 |
| `55139b5` | 原證明及 no4ct 替代鏈、K13–K15 與 C8 前提路由 |
| `9679a33` | W5 保存強度、私人圈秩及歷史覆蓋鏈 |
| 本紀錄所在 commit | 八條研究線現況卡、生命週期規則、文件檢查器及本批狀態 |

## 五組隔離成果及停止點

| 權威報告 | 完成範圍 | 保留問題 |
| --- | --- | --- |
| [相對來源／一般 cap](../../audits/2026-10-13-no4ct-generalization-6943561/REPORT.md) | 任意邊界的相對頂點預算與 cap 接合；同時 gadget 預算；C4t 代表內點下界 m≥⌈t/2⌉。2,274 個 cap、18,192 次查詢 | 八項 C8 沒有新增來源排除；一般代表及無界三支 OPEN |
| [W5／C8／C9 frontier](../../audits/2026-10-13-c5-no4ct-frontier-6943561/REPORT.md) | 三支共同 induced W5；排除零端部 PINCH／BRIDGE；h=4 的 C9 必 induced。435 項排351、留84 | h=3 八項、h=4 的84項（932／933／941為20／26／38）、h≥5及一般縮減 OPEN |
| [C8 joint gadget](../../audits/2026-10-13-c8-joint-gadgets-6943561/REPORT.md) | 334,512 個五私人點純 cap、明列 signed 域、八份完整共同計數與 Kempe cone 控制 | 八項沒有新 exclusion／realization；當輪較大 gadget 缺口由以下兩輪接續 |
| [C8 pocket 化約](../../audits/2026-10-13-c8-pocket-reduction-6943561/REPORT.md) | 七／八新點及其他 pocket 化回 signed 五點域；六新點只剩無弦 C6／六私人點最低度五核心 | 當輪剩餘完整接線由下一輪 C6 涵蓋；一般來源排除 OPEN |
| [C6 完整接線](../../audits/2026-10-13-c6-cap-completion-6943561/REPORT.md) | 剩餘核心恰三型；288 attachments、2,304 次 U 查詢皆非空。結合前輪，指定同側 boundary-pin-only gadget 預算域已用盡 | 八份 U 仍留；須增加同一原 H 資料或研究契約外合法操作；來源、主命題及 Lean OPEN |

C6 的合併結論限定所有 Eq scaffold、Diff 原邊及私人點同時畫在同一
exterior disk，只識別原 C8 pins，independent noncrossing、收縮後 loopless，
私人點 a 與框淨省 d 滿足 `a−d≤5`。其量詞是 `∀G∀U∃row(G,U)`；
各 gadget 可用不同 row，亦不證未知 H 實現這些 rows。
整體方法域結論仍引用前輪 signed 五點域的 plantri 完備性。

## 整體項目現況

有界關係等式仍為 `K≤15=K≤5`；一般目錄外來源至少十六內點。
原 E4 完整來源契約的 N2 已排除，E-ARC2 剩 N1 與相鄰 roots。
W5 的私人 `ρ≥5` 保留原完整最小來源及合法五輪前提；本批 no4ct W5
存在引理沒有自行移植此圈秩下界。h=3 八項及無界 932／933／941、一般
單側／共同出口、`K∞=K≤5` 均 **OPEN**。本批沒有新增 Lean theorem。

接續 no4ct／C8 時，使用同一 H 的 actual faces、separator、degrees 與
full lifts 收緊八份 U，或研究使用其他原點／原面的合法操作；h=4 從 C9
84 項 ledger 接同圖 apex／共同計數，932 的20項為具體入口。
完整前提及停止點以以上原報告為準；各線入口見 [HANDOFF](../HANDOFF.md)。

## 本批實際驗證

五包所有 frozen inputs、封存輸出及 manifest 的 bytes／SHA256 已核對。
本輪重播範圍如下，正常執行及所列負控制均通過：

- Generalization：caps `--check --negative`、獨立 cap、scope 與 transfer checker。
- Frontier：主／獨立 C9、端部完整 lifts 及負控制；完整 integration 在 `/tmp`
  的精確 frozen authority 副本以 `verify.py --check --negative` 通過。
- Joint：custody、degree4、共同計數及 Kempe cone checker 與負控制。
- Pocket：custody 與獨立 checker，五份實際破損證書均被拒絕。
- C6：package verifier、custody 及獨立完整 literal fibre 展開，五份破損
  證書均被拒絕；1,890,432 fibres／857,088 lifts 核對。

未重跑 joint／signed 五點完整大枚舉、外部 cone 或全部球面生成；其既有
receipts 和本輪雜湊保管驗證分開記錄。原重播命令由各包 REPORT／VERIFICATION
提供。Frontier 在當前工作樹直接 integration 會拒絕 HANDOFF、STATUS、
no4ct handoff、C8 peeling 及 degree5 reductions 五份文件的 live drift；
這些是本批文件演進，原 frozen 與證書均吻合，舊 verifier 及 receipts 保留。

發布檢查：

- `python3 scripts/check_docs.py`、九項現況卡結構負控制通過。
- `python3 tools/docgraph --include 'docs/**/*.md' check` 通過：95份文件、352條關係。
- `.venv/bin/python -B -m unittest discover -s tools/tests -p 'test_*.py'` 通過94項。
  系統 Python 缺 networkx；改用專案既有環境，沒有更新依賴。
- `lake build --no-ansi` 通過8,831項工作，保留既有 lint warnings；不認證本批紙面證明。
- 各組 staged artifact policy 與差異空白檢查通過。新增六份 sealed／frozen
  大型 JSON 的精確 size／SHA256 例外，沒有更改原 bytes。
- 四份 vendor `plantri.c`／`plantri-guide.txt` 保留上游原始空白；staged whitespace
  檢查僅排除這四份 exact 文件，其餘新增檔均通過。
- 全目錄 `python3 tools/docgraph check` 仍有63個 duplicate-ID，來自保留的
  audit／scratch 快照；正式 docs 檢查通過，未修改快照消除重複。

歷史生命週期試點的當輪未提交／未重播紀錄維持原語境；本次交付與驗證以
本紀錄為準。後續提交狀態由 Git 查核，不改寫各輪封存證據。
