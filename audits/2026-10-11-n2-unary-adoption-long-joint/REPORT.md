# N2 unary 三列出口採納與限定 long 化約

2026-10-11，HEAD `5f0979793c19e452dbb5fc7e9fe7e43cb8a991cc`。
精確工作樹基準為 [BASE.json](BASE.json)，包含原未提交候選，11份數學輸入
均另存不可變 frozen snapshots。當時既有文件及研究產物保留，沒有 commit／push。
本輪 root 的新推導及整合見
[權威報告](../../docs/c5_excess_two_n2_diagonal_three_row.md)。

## 數學裁決

[獨立紙面審查](paper/independent_review.md)未讀作者審查、未 import 作者 checker，
重建任意大小 block-cut tree 的單 block、兩 leaf、三 leaf case split，
核讀原外部 Gallai 定理，並核對同一列、同一原 pins 的完整接回。
採納以下精確結論：

- 完整 N2 的原 unary k=2／3 至少一指定列允許 owner=D；
  以兩 short 的該同一列完整 lifts 排 `(ℓ,u)=(0,1)` 原55子族。
- 原 mixed 若有 literal shared contact，對每個 proper β／每個同色 pins
  `(a,a)` 有完整 lift；由兩條原 root 邊只禁一色造成 degree-list slack。
- 原 long 的 root incidences 總數≤3時，三列至少一列接受完整 `(D,D)`；
  無 shared 時逐條核對 ownership 無關的原 lists，不合併 roots 或製造新來源。
- 權威報告§4的限定 mask corollaries均採納。兩個各自非滿的拒絕 masks 仍可合覆
  全部指定列，因此兩 long／U及long的同步不由個別出口推出。

關閉範圍是第三 relation 族原55格（與既有 u=2 排除合成），以及列明的 long 子域。
九格七格有覆蓋，另兩個原55格／三個含long參數情形仍 OPEN。
一般 N2、E-ARC2、N1／相鄰／單-root例外、Δ门檻及10–35內點來源未解。
沒有新 Lean theorem 或來源實現。

[long 補充](long/REPORT.md)亦獨立核對共享／低接點證明，並給必要的 D-block pattern：
若同一原 C 三列均拒絕 diagonal，D 出現於哪些原 block palettes 跨列固定；
證明用 block-vertex incidence tree 上的唯一解。此必要限制不承擔上述 closure，
未證其他 palette 色或不同分量的同列同步。

## 完整有限校準

[獨立 controls](controls/REPORT.md)使用動態最小色域 DFS 及 articulation splitting，
与舊 numeric-order DFS／Tarjan 不同；從 BASE snapshots 的原邊重建。

| 控制 | 實際结果與界線 |
| --- | --- |
| 97原U | 970列、15,520完整16-pin cells、2,048空cells；全部tuples與兩原產物一致 |
| U局部前提 | 42 triggered and holds，均k=2；55 not triggered |
| 63原整圖 | 630列、10,080 cells；direct full lifts與literal component joins逐tuple一致，完整Σ重算一致 |
| 原字面色表 | 五點／五邊signatures及25pairs一致；4逐列異色pairs；10triples無actual附件解 |
| split-root P3 | 全部十列(D,D)完整cells等於原unary；指定三列只q3有出口 |
| shared singleton | 全部十列(D,D)完整cells非空；不宣稱disk或target來源 |
| 37既有long | 370列、5,920完整cells、594空cells；全部tuples一致；34份degree4共享接點局部trigger成立 |
| low-contact long | 既有long中完整局部前提0觸發，not triggered；具名split-owner原路徑另作局部校準 |
| 完整Σ933／941 N2 target | 63原圖無任一共同D5像，0觸發，not triggered |

Control zeros不作任意大小排除；原 rotation／disk、Σ-criticality及全部上游分類未重驗。
有限 source、任意大小 paper、外部 Gallai、Lean與來源實現分開。

產物 SHA256與重播／負控制在
[controls verification](controls/verification.json)、
[transfer verification](controls/transfer-verification.json)及
[long verification](long/verification.json)。
normal／seed17通過，毀損副本按預期拒絕；exclusive-create覆寫被拒且原hash保持。
controls首生成的q-summary排序失敗及long首兩次schema／row-order失敗均在寫產物前發生，
失敗log保留，沒有改舊證書或覆寫已生成產物。

## 驗證及完整性

本輪 root 已重播舊 unary checker的normal／seed17，兩次exit0，
原產物 SHA256仍為 `e3ff41e50a5c35de2f2ae021caab93d187f2a349a504dd096f507869e1c9f836`。
本輪 `lake build` 通過8,831 jobs，既有linter warnings保留；沒有新Lean theorem。
正式文件、whitespace與最終完整性结果見 [verification.json](verification.json)。
含凍結副本的全工作樹 DocGraph未重跑，不宣稱全域通過。

```bash
python3 -B audits/2026-10-11-n2-unary-adoption-long-joint/paper/signature_check.py --check
python3 -B audits/2026-10-11-n2-unary-adoption-long-joint/controls/checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-11-n2-unary-adoption-long-joint/controls/checker.py --check
python3 -B audits/2026-10-11-n2-unary-adoption-long-joint/long/checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-11-n2-unary-adoption-long-joint/long/checker.py --check
python3 -B scripts/check_docs.py
python3 -B tools/docgraph --include 'docs/**/*.md' check
lake build
git diff --check
```

整合前11份live／frozen inputs零漂移，见
[pre-integration-integrity](logs/pre-integration-integrity.json)。
採納整合後只更改原候選及統一報告的後續狀態／路由，frozen數學輸入及舊checkers／
證書維持原hash；允許的live文件變更明列於最終verification，不冒稱live全零漂移。

## 文件傳播

Closure scope / Canonical Source + Evidence：上述完整(0,1)原55子族及限定long子域；
權威三列diagonal報告＋三份獨立workers證據。

Updated：原候選與統一報告的後續採納狀態，Kempe導覽、STATUS直接索引、
N45§2.16–2.17／§3及synthesis直接consumer；都保留父N2／E-ARC2 OPEN。

Reviewed-unchanged：原55大小界的上界／Δ後續說法仍適用；README／HANDOFF的
研究線及入口未變，其原55／一般E OPEN摘要仍正確；上游44／N45／SD-A及原artifact不改。

Remaining OPEN：含long三情形的完整同列joint、一般Δ下界、N2外來源及完整E-ARC2。

Propagation stop：直接受影響摘要已同步；研究線／全域路由未變，不擴大改寫其他線。
