# 任務 D₉：E4、E5、E6 紙面引理的獨立稽核

2026-10-06；固定基準 `b2ca4520da50c9d2898ac6f8f966ac25df3f9609`。
指定 worktree `/home/ray/developer/ai/math-task-d9`、branch `task-d9-audit` 已建立。
以下原文行號全部指該 commit 的 bytes，不指 E4–E6 歷史 worktree 的其他版本。

**總 verdict：指定紙面引理 holds，未發現新的數學缺口或反例。**
結論以各引理明列的 disk、完整 degrees、Σ-critical、同源 contacts／attachments、
必要時指定三拒絕列與被引用的外部定理為前提。
54 NA＋9 AD 控制的完整指定三拒絕列前提皆 **not triggered**，
不能說它們實現或實驗驗證了該假設下的所有來源排除。
已觸發的通用中間機制全部成立；禁型前提沒有實例時明列為未觸發。

原八份 checker 共16次重播，12次 exit0、4次歷史 byte FAIL，八對 stdout 相同。
E4 reductions／E5 controls 的 FAIL 僅是 E3 REPORT 的 provenance 漂移，
數學 payload 與其他來源 provenance 相同。全域文件檢查重現兩個 D₈ known missing paths。
這些既有失敗均保留，不以重寫舊證書換取 PASS。

**交付狀態尚有環境阻擋。** 執行期間 permission profile 改成唯讀，
工具已兩次回報 worktree 的 `Read-only file system`。
使用者已同意恢復寫入，但實際 profile 尚未生效；完成的報告、修訂後獨立
checker／results／validation 暫存 `/tmp/math-task-d9-staging`。
尚未將最終內容放回指定 audit 目錄或 commit；commit SHA **無**。
worktree 中保留中斷前的草稿，不能當作最終交付。沒有 push／merge。

## 1. 每引理總表

來源：[E4](../../artifacts/c5_excess_two_e4/REPORT.md)、
[E5](../../artifacts/c5_excess_two_e5/REPORT.md)、
[E6](../../artifacts/c5_excess_two_e6/REPORT.md)。
`holds` 是在所列前提與引用定理範圍內紙面步驟有效；不是新增 Lean theorem。

| 引理／項目 | 適用範圍 | verdict | b2ca452 原行號、理由與界線 |
| --- | --- | --- | --- |
| E4 N-empty-separating | 原 degree4 mixed 無 B-support，包括 separating sole mixed | holds | E4:56–72；原外路 hubs 或無框單-root appendage 對齊，同源接回反駁接點邊 criticality。 |
| E4 N-theta | 外框 disk 中三份不同原 mixed | holds | E4:219–227；原三路的 Jordan cycle 隔離整份第三 piece，迫 actual support 空。 |
| E4 N1-22-44 | sole mixed22、指定三拒絕、存在兩-root44 core | holds | E4:92–152；實際原44分類／飽和給四點path，三列迫 terminal 真框邊，兩整側各成本≥3而互斥五邊。沒有排除無44core的22。 |
| E4 N-diagonal | one-sided degree4 mixed、full B-touch、support 含於框邊 | holds | E4:166–185；pin-only tight lists 與二／三原 hubs，給每個相同root pin的整份tuple lift。 |
| E4 N2-short-no-unary | 兩 short mixed、無 unary | holds | E4:189–192；兩roots同取未用色，完整pieces在同一β拼回全部三色列。 |
| E4 N2 side-intersection／budget | 兩mixed、原完整side domains與actual盾弧 | holds | E4:194–215；short diagonal給拒絕列side交集空；long／unary各至少二邊，ℓ+u≤2；保留完整joint殘留。 |
| E4 非相鄰 m≤2 | 原非相鄰雙5来源，任意core型 | holds | E4:219–232；theta空支援與N-empty在原圖層矛盾。 |
| E4 N3 全排 | m≥3，45／54／原55 cores | holds | E4:229–232、272；排除的是原來源本身，未漏掉非44core。 |
| E5 L1 | 每個保留B的proper subgraph | holds | E5:81–97；minimal pair-core自身critical，ε2飽和迫等原G，所以ε≤1；E2禁止非相鄰pair。ε0段不能稱proper S本身critical。 |
| E5 L2 | retaining C12／C22或binary-U的指定spoke predecessor | holds | E5:103–123；原contact長環、binary cycle排除後續all4core，degree4 piece全取／全不取，正確取得M自身q-minimal。 |
| E5 L3 | J2 unit-U／J3 binary的a-spoke omission | holds | E5:127–138；L1及degree5相鄰列分離、同一M−U只缺一列，給最多一拒絕；沒有推成Ω。 |
| E5 L4 | 四精確分支與原三spoke set | holds | E5:142–158；literal冗餘spoke集合算得必要域4／2／2／0；932排除只在G2／G3已證L3範圍。 |
| E5 L5 | J3 ternary C12＋unit-U | holds | E5:162–176；L2取得minimal身份，marked-leaf slack及完整避色cover滿足既有single-spoke-(3,1)定理，繞過舊ledger。 |
| E5 L6 | G4 A的C12＋a-unit-U | holds | E5:182–206；N與a-spoke omissions均Ω，完整guard直積空只可能相同singleton。沒有獨立marginals拼接。 |
| E5 L7 | A所有equal actual spoke pairs | holds | E5:210–222；原diamond面及三hub接回，包含舊A₃／A₄，不借額外接受位或NΩ。 |
| E5 L8 | B的mixed22、無unary，所有Gallai terminal blocks | holds | E5:224–299；共同column／edge signatures與原terminal cycle／bridge K₅ bags；shared leaf cut parity允許任意actual單框h。 |
| E5 四分支依賴表 | 941／933／940／932；G1–G4原殘留 | holds | E5:32–77；optional接受性只由精確mask給定，940整圖共同反射；局部證與整型coverage分開，G1等仍明列缺口。 |
| E6-A 相鄰 m≤2／J6 m≥3全排 | 原相鄰雙5、任意core型，四分支 | holds | E6:36–65；zw加三mixed原路，兩種外面邊界均隔離整份原mixed；刪C仍connected，以原zw二hubs接回。 |
| E6-B／C（附帶） | 原incidence／core與通用spoke budget | holds | E6:77–117；省略identity全由原degree4飽和與{0,1}²loss；通用L1欄位沒有偷套較強L3到J6。 |
| G2 U盾弧恰二 | E5 G2原三spoke＋C11＋unit-U | holds | E6:149–161；連續三spoke star的三邊gap被長U佔滿時，端點同色query與完整F_U容量、原hub使C接回。 |
| G3 named support | 原binary-U，保留整份C反像與U tuples | holds | E6:163–192；pin-only endpoint不禁色、F_K⊆L，逐字面query迫S_U与b-spoke；沒有聲稱F_K=L或舊表coverage。 |
| G4 U盾弧恰三 | A unequal frames、原單contact U | holds | E6:196–225；真singleton identity、endpoint引理與同一block-tree的未用色membership排除長二；裸原骨架面排除S_U=B，故長四／五不可。 |
| no-mixed budget／殘留 | 原m0，四分支與兩原整側 | holds | E6:121–145；恰兩U；整側盾弧≥2、三spoke側≥3並非連續支援；共同literal欄位只留941的013或兩側≤2。root刪除仍保留可能單列例外。 |
| E6-H（附帶） | rejecting predecessor已存在時的G1分組 | holds | E6:230–263；原44實際分類給retaining／mixed-onlygroups；只作G2／G3／J4／J6入口轉交，未預填M為Ω或排除J4。 |

逐步理由、外部假設的使用與未觸發限制分見
[E4稽核](audit_e4.md)、[E5與G2–G4稽核](audit_e5.md)、[E6稽核](audit_e6.md)。
沒有把 N1／N2、G1–G4／J6 m≤2 的既有來源殘留當作本輪新proof gap。

## 2. 三類控制結果

三個独立checker都不import原checker決策邏輯；用有限四色DFS與原rotation。
E4取54NA；E5取同54NA＋9AD；E6取9AD，並共同搬運全部十個D₅ images。
9 orbits的90個搬運case不算90張獨立來源圖。每個結果均保存
`triggered and holds`、`not triggered` 或 `counterexample`，不把空集合填PASS。

下表以source orbit計數；括號另列query／搬運case，不能把不同項相加成來源總数。

| 主題 | triggered and holds | not triggered | counterexample | 實際範圍 |
| --- | ---: | ---: | ---: | --- |
| 指定三拒絕列完整來源前提 | 0 | 63 | 0 | 54NA、9AD皆未觸發；AD全十個共同D₅ images亦未觸發。 |
| NA非相鄰m≤2 | 54 | 0 | 0 | 實數m；不等於三branch theta反證前提被控制實現。 |
| AD相鄰m≤2 | 9 | 0 | 0 | 90共同搬運case皆m1。四路反證／m2外面前提仍零。 |
| NA N-diagonal | 11 | 43 | 0 | 22pieces、880完整diagonal fibres。 |
| NA N2 side-intersection／budget（各自） | 11 | 43 | 0 | full-B-touch與原short／m2前提。 |
| N-empty／N-theta／N1-22-44／N2-short-no-unary／N3（各自） | 0 | 54 | 0 | 各自禁型前提沒有NA實例。 |
| L1 proper拒絕輪廓 | 63 | 0 | 0 | 各原single-edge最大proper子圖；任何proper edge-subset的Q是其中一份Q的子集。 |
| L1 retained兩root all-four／L2 incidence（各自） | 6 | 57 | 0 | AD6有實際rejecting44候選；NA54無此觸發。不是所有root-deletion cores的枚舉。 |
| L3 J2 unit-U單spoke機制 | 2 | 61 | 0 | AD2的結構機制，沒有指定三列前提。 |
| E6-F三點U endpoint機制 | 36 | 27 | 0 | NA28＋AD8；AD另有1400搬運後queries。 |
| E6-G單contact未用色membership機制 | 30 | 33 | 0 | NA22＋AD8，各有至少兩個實際拒絕assignments；不是整型G4排除的控制。 |
| G2／G3／G4／no-mixed整型推論（各自） | 0 | 63 | 0 | 指定三列来源為零；no-mixed本身在全部原控制也未出現。 |

NA原完整join獨立核對8640個pin查詢；1289非框刪邊、1385新增列witness。
全部60個minimal qcores原樣重算，55有48、45有10、54有2、44為0。
AD原完整relations與同源factorjoin及兩種G1group等另見E6附件，
固定欄位表重算與四分支輸送不依赖來源接受位的額外filter。
有限零反例只對這些固定控制有效。

## 3. 歷史失敗、最小重現及影響

未發現需補表或反例重現的**新增數學gap**。已保留的重播／交付問題如下；
詳細SHA、logs及source行號見 [validation稽核](audit_validation.md)。

| 問題 | 最小重現 | 實際結果 | 影響 |
| --- | --- | --- | --- |
| D9-P1：E4／E5歷史provenance漂移 | `python3 scripts/c5_excess_two_e4_reductions.py --check`；`python3 scripts/c5_excess_two_e5_controls.py --check` | 各exit1，seed17亦1；僅E3 REPORT SHA／bytes不同 | 原嚴格byte replay仍FAIL；移除該provenance欄位後全部payload相同，不影響本輪paper verdict。 |
| D9-R1：全域封存不完整 | `python3 tools/audit_archive.py restore --artifacts` | exit1，缺E3 degree6 blob，尚未開始寫入 | 全域restore未完成；本輪必要E1缺檔已exclusive還原且核對原SHA，54NA／9AD與各必要輸入可用。 |
| D9-V1：既有文件缺路徑 | `python3 scripts/check_docs.py` | exit1，僅D₈已記錄的D5 c4 ledger及D2 integration diff兩路徑 | 全域文件check仍FAIL；未修改舊tracked文件，無數學影響。 |
| D9-W1：執行中worktree/Git轉唯讀 | 將完成的`audit_validation.md`從staging複製到指定audit目錄 | exit1，Errno30，使用者同意恢復後仍失敗 | 最終落檔／stage／commit未完成，沒有可報的commit SHA；完整可審閱交付在staging。 |

[historical_replay_differences.json](historical_replay_differences.json) 列每一個不同leaf；
E4／E5原fresh replay只保存於audit/staging，沒有重寫原artifact。
所有原checker的八對stdout及stderr皆相同。

## 4. 交付、驗證與停止點

| 檔案 | 用途 |
| --- | --- |
| [audit_e4.md](audit_e4.md)、[audit_e5.md](audit_e5.md)、[audit_e6.md](audit_e6.md) | 固定行號、每引理範圍／verdict、每一步理由與control限制。 |
| [audit_e4_controls.py](audit_e4_controls.py)、[audit_e5_controls.py](audit_e5_controls.py)、[audit_e6_controls.py](audit_e6_controls.py) | 三份獨立原edges／rotation／完整relation有限checkers。 |
| [e4_controls.json](e4_controls.json)、[e5_controls.json](e5_controls.json)、[e6_controls.json](e6_controls.json) | 每圖／query三類判定、SHA、witness或完整lift/fibre摘要。 |
| [run_validation.py](run_validation.py)、[validation.json](validation.json) | 每條驗證命令、exit、完整log路徑與SHA256、seed比對、未做事項。 |
| [audit_validation.md](audit_validation.md)、[historical_replay_differences.json](historical_replay_differences.json) | 原FAIL的可重現診斷與影響；不是独立lemma checker。 |
| [baseline_sha256.json](baseline_sha256.json)、[invariance.json](invariance.json) | 所有既有tracked普通文件零漂移。 |
| [check_audit_outputs.py](check_audit_outputs.py)、[audit_output_checks.json](audit_output_checks.json) | 新Python syntax／新文本whitespace／以指定交付位置解析的local file links／實際引用的heading anchor。 |

獨立checker均stdlib，`--check`普通／seed17逐byte重播；原NetworkX checker以uv指定3.5。
沒有超過12jobs：最多三個稽核subagents加一個root worker，各checker單worker。
Git whitespace與文件命令確實執行，不以empty diff代替新增文件內容檢查。

停止於本輪指定paper audit與固定控制；原來源remaining G1–G4／N1／N2／J6 m≤2
沒有新排除，ε≥3、一般出口、source realization與K∞=K≤5仍未證。
沒有Lean build、push或merge。環境尚未允許最終worktree落檔與task-branch commit。
