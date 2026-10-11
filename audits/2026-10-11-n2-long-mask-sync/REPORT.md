# N2-55 long masks、原同列同步與 leaf-contact tree

2026-10-11。接續完整原 N2-55 的三個含 long 情形；本輪停止於限定紙面排除，
沒有搜尋10–35內點、來源生成、Graphify、Lean theorem、commit 或 push。
基準 HEAD `5f0979793c19e452dbb5fc7e9fe7e43cb8a991cc`；前輪採納及現況檔原有
未提交變更保留。精確13份原輸入、bytes／SHA、初始 Git 狀態在 [BASE](BASE.json)。
凍結副本一律 `.snapshot`；各 worker 只寫本輪各自專屬子目錄。

## 1. 完整契約與採納结果

所有 source corollaries 使用 frozen diagonal §1／spoke §1 全部前提，保留有序
induced-C5 disk、完整Σ933／941／共同D5像、T4全收、Σ-critical、ε2、有效H及
原degree5 roots／degree4 pieces、全部原contacts／ownership／attachments／rotation、
bridges／完整relations／空fibres／full lifts。同一字面三列 q0=01212、q1=01202、
q3=01021、未用 D=3，没有逐piece正規化。

| 紙面成果 | 独立裁決／實際來源範圍 |
| --- | --- |
| 原同框邊雙spokes K5 | root 起草，[synchrony §5](synchrony/REPORT.md#5-對原-topology-證明的獨立核對)及[high-contact §3](high-contact/REPORT.md#3-independent-audit-of-the-common-two-spoke-edge-minor)另人接受；原中央block的兩點fan及兩mixed路給五袋十鄰接 |
| 两long都k≤3 | 原 degree＋原盾弧迫兩roots各兩spokes接同一框邊，K5排除；shared情形由已採納full lifts接回；剩至少一long k≥4 |
| 全葉接點tree任意k escape | high_contact 提出，root與[synchrony另人審查](synchrony/high_tree_independent_review.md)接受；排(1,0)子域，另long shared時排(2,0)子域 |
| 兩邊弧低接點mask精確三類 | synchrony 提出，root及[controls另人核對](controls/independent_code_review.md)接受；不漏原五／六點cactus形，M只為空／Eq／Diff |
| 含U的Eq-Diff同步 | 原盾弧長2+2+1，異類mask必有同列；short及U/L全原lifts接回，限定排除(1,1)；同類只留七個必要弧模板 |

詳細採納見 [root獨立紙面審閱](review/independent_paper_review.md)，完整新報告為
[long同步與tree化約](../../docs/c5_excess_two_n2_long_synchrony.md)。
九格覆蓋數仍七格。三個含long父情形、一般原55、完整N2、E-ARC2全OPEN。

## 2. 完整 fibres／joins 與保留的反控制

[controls](controls/REPORT.md)獨立重算全部179原分量的28,640 cells，含3,372空cells；
1,790份完整外部tuple重算及63原圖10,080同列同ordered-pins joins均對回原全圖DFS／SHA。
原37份long masks皆空，但兩long在同圖及support≥3/k≤3原long均零觸發；沒有把
這些零覆蓋解讀為source exclusion。全部target source status為 `not triggered`。

固定7份motifs的800份實際附件控制、45份完整十列16-pin exemplars及810份弧
signature pairs保留，其中56份沒有common diagonal row。它們校準mask算術，
任意大小形狀完備性由紙面承擔。加原四spokes的兩path圖保存原K5bags／十條邊。

[high-contact](high-contact/REPORT.md)另保存四接點path三列diagonal全拒的
`counterexample`，反駁由純局部前提將escape推至k4；不是完整target反例。
兩份具名局部圖全320 ambient cells含40空cells保存。新shape/source層分開。

## 3. 驗證入口及實際 receipt

[verification.json](verification.json)保存root最後的獨立重播、文件及build實際結果。
各worker也保留各自正常／seed17／毀損副本receipt；三份checker都採exclusive-create，
以正常 `--check --artifact` 路徑拒絕保留的毀損副本。Signature checker最初非exclusive
寫入已由獨立code review指出並修正；原artifact bytes未變，記錄未刪。
Global tuple SHA serializer的首次失敗與missing-networkx exploratory failure亦保留。

```bash
python3 -B audits/2026-10-11-n2-long-mask-sync/controls/checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-11-n2-long-mask-sync/controls/checker.py --check
python3 -B audits/2026-10-11-n2-long-mask-sync/high-contact/checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-11-n2-long-mask-sync/high-contact/checker.py --check
python3 -B audits/2026-10-11-n2-long-mask-sync/synchrony/signatures.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-11-n2-long-mask-sync/synchrony/signatures.py --check
python3 -B scripts/check_docs.py
python3 -B tools/docgraph --include 'docs/**/*.md' check
lake build
git diff --check
```

新paper依賴既有外部Gallai定理；未重審全部上游44／N45／SD-A、ES／ER生成、
來源rotation或全工作樹DocGraph。成功build只驗證既有Lean專案。

## 4. 文件傳播與停止

Closure scope：以上限定原來源子域；canonical source及evidence見§1，不推升父族。
Updated：新增long同步報告，前輪diagonal／residual加有日期的後續狀態，STATUS、
Kempe guide、N45直接停止點及已有synthesis摘要同步。前輪九格／採納表及當輪語境保留。
Reviewed-unchanged：README仍正確路由E-ARC2且父N2 OPEN；HANDOFF研究線未變；
size-bound的35及Δ後續入口仍正確；Phase B一般B-C2及OPEN跨列義務不改。
Propagation stop：直接L2消費者；上層父命題仍OPEN，未重寫歷史或新增總帳。

Remaining OPEN：(2,0)至少一long k≥4；(1,0)無shared的k≥4 long含cycle或
C-cutpoint接root；(1,1)高接點或低接點七個同類弧模板。下一窄入口以同一原
ownership、root度數及實際spokes分析這七個模板；或取得k≥4的完整off-diagonal
joint。一般N2／E-ARC2及Lean化均未完成。
