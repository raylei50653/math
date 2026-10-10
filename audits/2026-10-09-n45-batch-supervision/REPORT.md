# N45 第一批：A 首輪驗收與 S／U 預審裁決

2026-10-09；BASE／實際 HEAD：
`dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`。

**A 首輪依賴稽核已驗收；S／U 新紙面窄結論預審通過，仍待獨立增量交叉驗收。**
J 已在 [先前監督報告](../2026-10-09-n45-j-supervision/REPORT.md) 驗收工具與固定控制。
四份第一批均已收到，沒有因 A 首輪完成就把尚未審的新 S／U proof 當作已獨立採納。
兩份合併後的 [S／U 增量發布全文](../2026-10-09-n45-s-supervision/cross-audit-tasks.md)
可同時發布：N45-SU-A 審 paper、N45-SU-J 審有限證據；均只寫新獨立目錄。

## 1. A 首輪裁決

原交付：[N45-A REPORT](../2026-10-09-n45-a/REPORT.md)。
已讀全 checker／只讀 verifier、全部九項 CLAIM 與四項 finding，逐項對回 BASE 紙面依賴。

| 範圍 | 裁決 |
| --- | --- |
| N45A-01／02 | 接受精確來源的 triple-critical、full B-touch、N2 刪 roots 全收，及同一原 degree4 piece 飽和／45或54省略分類；U1–U4只關44，不提升55或來源全排。 |
| N45A-03／04 | 接受先保同 Σ minimalize 的 ε 單調及 E2 出口；X criticality另證。E4-D仍需原重色 spoke 前提，不得取 converse。 |
| N45A-05／06 | 接受原 G 的局部 N-diagonal、完整 joint 與逐原 piece 拒絕見證／外路／盾弧收費接口；不用 X 自己 full B-touch，省略者仍付原費用。 |
| N45A-07 | 接受搬用邊界：U4 retained44／O11 不給一般45／54 mixed下界。S／U的新下界須增量審，不由首輪稽核代證。 |
| N45A-08／09 | 接受χ0完整逐欄 B-C2 paper式與固定 controls 的精確 coverage；原G右值1、下降側 derivative右值0须在自己的 degree上計算。沒有精確target來源正控制。 |

沿用 E2 任意大小化約／既有有限末端分類、全四分類、U1–U4及原 hub／Gallai 依賴，
本輪未重跑全部上游或新增 Lean。A 首輪沒有讀 S／U／J，新 proof 不屬其原驗收範圍。

### 1.1 四項 finding 的處置

- F01 保留。原 E4 core／reductions `--check` 普通及 seed17 在 clean BASE均 exit1；
  逐字段比對只有 `sources.artifacts/c5_excess_two_e3/REPORT.md` 的 bytes／SHA256 漂移。
  非 sources payload相同；舊30573 bytes／`6d385639…`、新32469 bytes／`73ed652a…`。
  fresh檔的歷史 `baseline_commit` 不改稱本輪HEAD；不覆寫原 artifact。
- F02 保留。54圖與其172個units不能補N2精確933／941的45／54正控制；N1的12個occurrences分列。
- F03 保留一般義務。S／U各自另證窄支援下界是新候選，待SU-A驗收；incidence≥4的mixed仍無一般下界。
- F04 保留。fresh BASE docs缺兩個既有未入Git的歷史audit目標，與來源紙面命題分列。

上述 finding 不構成新數學反例或撤銷已列 BASE 引理的理由。

## 2. U 紙面逐 claim 預審

凍結原交付：[N45-U REPORT](../2026-10-09-n45-u/REPORT.md)，
SHA256 `0c3d117f1c804bc0695fc97fd570f2ede6451d5a21ca036f337f4d11c5de72a7`；
final certificate SHA256 `1f7dc2f13fa372150f2d915fd10494986c2f0a3aa08fa965c8b2f013315980d0`。
讀全513行 checker，核其只讀重播及生成exclusive-create；draft、failed attempts、final 分開保存。
以下均保持 U REPORT §1 的同原G／原U／β／X=M前提、完整原relations與root交換。

| CLAIM | 預審判定與界線 |
| --- | --- |
| N45-U-REL | 通過。唯一contact供strict slack，使完整U relation非空；F只可空或singleton。刪contact與整U省略的完整root-pair relations相等，full lifts分開。對新接受γ的所有X lifts，U palette及r投影均是同一singleton；core拒絕β不推出F_U(β)非空。 |
| N45-U-WIT | 通過。各piece原critical-contact full lift限制成不可接回的outside witness。fullB-touch與H−piece連通給原外路；不同γ只供同原圖幾何費，不加跨列禁色容量；省略U仍付原σ_G(U)。 |
| N45-U-CROSS | 通過。先同Σ minimalize、ε1單調後用E2；七格933／941的Q(X)必要域含β，保933的q2。Δ上forcing屬同列全部X lifts，不把逐列relation獨立拼來源。 |
| N45-U-CAP | 通過。E_s≥m_s−1>0，X低度側B-C2五費全零，逐b兩mixed欄滿額、不交、覆蓋E_r^X。恢復U的一單位分D／O／λ三處，raw columns未變；F空是合法D型，不能一律預填singleton。 |
| N45-U-S3 | 通過預審，必交增量A。原critical-contact witness使degree lists不可染，Gallai block分析逐項排K4、大clique、多末端blocks、單bridge及最後triangle；原hub只證非平面性，沒有染色收縮。只給總root incidence≤3的mixed支援≥2；不推incidence≥4。另有§2.1獨立核對。 |
| N45-U-U2 | 通過預審。兩原unary先排long，再由X拒絕及diagonal給m_r+m_s≤5，兩mixed各≤3，用S3得到pair支援，原1+1+2+2>5。這是指定整U省略身份的兩原unary子型，未關一般45／54。 |
| N45-U-SHORT | 通過預審。U2後只剩被省略的一份U；若兩mixed都short，X無unary且β為三色，共同未用色D避spokes，原mixed的完整(D,D) lifts接回X，矛盾。不要求X fullB-touch。 |
| N45-U-RES | 通過必要化約。兩long與原U收費6排除；餘唯一被省略U、一long L、一short S。pair S迫盾長(2,2,1)；singleton S只能有總incidence≥4。β上L禁止(D,D)、各欄滿額，Δ上U／X singletonforcing须同源跨列成立，未證此來源可實現或不存在。 |

### 2.1 S3 的獨立接口核對

另由已核的原 N-empty／N-diagonal 與 S 的色軌道步驟給同一窄下界：
支援為空時，H−P連通的原root外路使N-empty接回每份outside witness，
與critical contact矛盾。支援為{h}時，原fullB-touch／one-sided讓所有diagonal pins接受；
局部relation固定c=β(h)的S3色置換不變，三個off-diagonal軌道的行／欄需求為
(k_s≥3)、(k_r≥3)、(k_r,k_s≥2)。總incidence≤3且两側正，因此三軌道皆不能禁。
完整relation為Col²，於是critical contact刪邊的合法G−P outside lift可填回整P，亦矛盾。

這是紙面交叉核對，不是固定22個控制的完備性，也不把S或U新claim先視作已由A獨立驗收。
U原Gallai證明仍須SU-A核其末端與tethers／原K5 minor細節。

## 3. 新有限重播、provenance與交叉核對

[review.py](review.py) 只重用監督端已有的固定順序完整原邊枚舉，
不import任何執行者checker。普通／seed17新重播與獨立結果見
[replay_records.json](replay_records.json)、[independent_review.json](independent_review.json)。

| 範圍 | 實際結果 |
| --- | --- |
| A frozen來源 | 136權威＋validation掃描來源去重720份，逐項對BASE Git objects及clean checkout，零byte漂移 |
| A交付 | MANIFEST.json的56項hash/bytes、精確inventory均相符，含manifest共57檔；sealed verifier exit0，另照實報共同導航3檔漂移 |
| U frozen來源／交付 | 70份對BASE及clean source相等；7項payload／所有宣告log hashes相符；另凍結39份authored files，source70份分列 |
| A／U普通、seed17 | 四次新 `--check` 均exit0，沒有改原交付 |
| A歷史E4 replays | core/reductions各普通／seed17共4次exit1；provenance之外payload相同 |
| A獨立原Σ | 54圖×10列＝540列重算；172units×10列＝1720列重算，接受／拒絕與原證書相等 |
| A criticality／B-C2 | 1289條critical edge的新接受full witness逐邊合法；74個N2 columns與已驗收J精確費用向量相同 |
| U原图／省略／contact刪除 | 3680＋1760＋1760＝7200個完整pins，枚舉包含所有空fibres，與U及J相同 |
| U完整localrelations | 690份tuple/full-lift groups及fibres與J相同，2986份full piece lifts一致；原contacts/support/attachments/rotation核對 |
| U容量 | 原G90＋X12＝102欄與J費用向量相同；低度側4個N1 placement全λ型，D／O及N2拒絕derivative沒有正控制 |
| 原檔 | A／U authored bytes＋mtime前後零漂移；各clean BASE sources零byte漂移；S／J未改 |

精確target來源、N2 45／54、两unary排除前提仍0觸發；表中校準不是新來源排除證據。
23圖的22個小incidence支援instance滿足必要式，但沒有singleton反證支枝／任意大小控制。
保留U的初次tuple schema生成失敗、初版與final兩個版本、路由漂移及文件fail。

## 4. 管理、文件及停止点

| 任務 | 本輪結束狀態 |
| --- | --- |
| N45-J | 工具／固定控制已驗收；沒有新來源排除 |
| N45-A | 首輪BASE依賴與固定控制已驗收，4 finding保留；未審新S／U paper |
| N45-S | [六項預審](../2026-10-09-n45-s-supervision/REPORT.md)通過，正式採納待增量 |
| N45-U | 本報告八項預審通過，正式採納待增量 |
| N45-SU-A／N45-SU-J | 合併兩份可發布增量任務，凍結S／U／J版本；未啟動或代使用者發布 |

S候選只排指定spoke省略的原u2子型；U候選排指定整U省略的原u2與兩short子型。
U餘唯一U＋一long／一short；S餘LOW／HIGH及long身份。
原55、沒有45／54來源、一般mixed incidence≥4支援義務、N2與猜想E仍OPEN。
第一批先完成新proof的獨立增量裁決，再選第二批最小residual，不發廣域新搜尋。

本輪文件驗證見 [checks.json](checks.json)。共享正式docs檢查與formal DocGraph通過；
fresh BASE兩缺檔及whole-worktree DocGraph的62 duplicate IDs保留，不把formal PASS當全域PASS。
L0 reports/evidence與L1 guide/STATUS/派工狀態更新；新子型尚待採納，未觸發父題closure。
BASE E4／Phase B仍保留其原範圍，不改原來源來提前採納新結果；上層routing不變，停止L1。
未新增Lean、重跑全上游、commit、push、外部訊息或sub-agent。
