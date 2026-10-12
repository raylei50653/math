# N2 原55含 U 子情形：紙面 closure 與固定 fibres 稽核

2026-10-12。新 exclusive audit；基準 HEAD
`8b76dcc82adabba679e7b0d2ef6dbe6eb9cc37f3`，包含前輪未提交成果。
十八份精確原輸入的 bytes／SHA 及初始 Git 狀態見 [BASE](BASE.json)。
凍結輸入、前輪證書與其他 workers 的產物均保留；沒有 commit／push。

**採納範圍：** [U2-DIFF-ALL](paper/REPORT.md) 為任意大小局部紙面引理，
在已採納完整來源的原結構、兩接線 U、三點弧支援及 planarity 下，
Diff 列每個 owner pin 都有全部原 U 的完整 lift。
原 block-tree 與兩條實際附件邊容量給五原形；唯一局部拒絕的六點 barbell
有明確原 K₅ minor。以同列 G−U 的實際 owner pin 接回，排完整原55 `(1,1)`。

[独立審查](review/REPORT.md) 逐量詞採納；
[另份重建](joint/REPORT.md) 保存並更正把內部 bridge 色誤限為不同於 owner 色
的 scratch 推導，最終證明使用正確 palette 與原 K₅。
Canonical source 是 [專題報告](../../docs/c5_excess_two_n2_unary_diff_closure.md)。

## 固定控制與界線

[checker](controls/checker.py) 是 stdlib-only、exclusive-create／read-only replay。
五份導出原 skeleton 的 1,050 份附件控制保留原 ordered vertices／contacts／owner，
十份 proper 框代表與四 owner pins；每份完整 tuple 都由原邊 DFS 和獨立全 tuple
filter 重算相等。Ambient 非 owner pin 的四份等值副本仍完整保存。

[完整證書](controls/observations.json.gz) SHA256：
`050351cfd54c129db748053a48a82447762b7185ff66b20f57011fadc3c87989`。
确定性 gzip 1,088,012 bytes，解壓完整 JSON 35,291,724 bytes。
共 42,000 獨立 owner cells、168,000 ambient ordered cells、3,880 空 fibres、
2,119,000 完整 tuples。1,040 份局部出口控制 `triggered and holds`；
十份 barbell 為去掉 planarity 的 `counterexample`，各有原 K₅ 的互斥、連通五 bags
及全部十條原 inter-bag witnesses。
全部完整 target **`not triggered`**、`source_inputs_verified=0`。

有限附件校準不是整圖來源枚舉，不證無界 skeleton 窮盡；任意大小排除由紙面
證明承擔。沿用上游 capacity／Gallai／N45／44／SD-A 信任鏈；沒有新外部 theorem
或 Lean theorem。既有 `lake build` 不形式化新紙面結果。

## 重播與文件接回

```bash
python3 -B audits/2026-10-12-n2-two-contact-unary/controls/checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-12-n2-two-contact-unary/controls/checker.py --check
python3 -B audits/2026-10-12-n2-two-contact-unary/controls/checker.py --check --artifact audits/2026-10-12-n2-two-contact-unary/controls/negative-missing-lift.json.gz
python3 -B scripts/check_docs.py
python3 -B tools/docgraph --include 'docs/**/*.md' check
lake build
git diff --check
```

第三行是刻意缺一份完整 lift 的負控制，預期 exit1／`artifact mismatch`；
其餘實際結果、stdout／stderr hashes 與 frozen drift 見 [verification](verification.json)。
正常／seed17 重播 bytes 相同，負證書按預期拒絕，十八份 frozen inputs 零漂移。
沒有重跑前輪全部 partition／N45／44／SD-A 證書或 ES／ER 搜尋。

**Closure scope：** 完整原55 `(1,1)`；合既有 `(0,1)` 及 u=2 排除，
完整目標 N2 原55必 u=0、H 二連通。
**Updated：** canonical source、Kempe guide／STATUS、partition／long／diagonal／
residual 的有日期後續提示、N45直接父題§2.18與目前殘留、synthesis／README
的受影響 N2 摘要。
**Reviewed-unchanged：** HANDOFF 只有研究線導覽，線與標記未變；
原55大小界仍有效，新來源只是縮小其 u 域；上游 spoke／N45 真core closure
範圍不變，歷史 frozen reports 保留原語境。
**Remaining OPEN：** `(1,0)`、`(2,0)`，N1／相鄰／單-root 及契約外 N2，
一般原55／N2／E-ARC2、一般出口及 `K∞=K≤5`。九格仍七格，第二 relation
格仍含 `(1,0)`。
**Propagation stop：** 直接父題與已知摘要 consumers 的相關 N2 段落；
沒有推升 E-ARC2 closure 或更高層全域命題。
