# N2 原55：共同接口及已用色禁色規律

2026-10-12；exact BASE `8b76dcc82adabba679e7b0d2ef6dbe6eb9cc37f3`。
十二份精確快照、bytes及SHA見 [BASE](BASE.json)；只寫本 exclusive audit 及相連docs。
完整證明、量詞、來源契約及停止點見 [canonical report](../../docs/c5_excess_two_n2_partition_rule.md)。
本輪不做來源新枚舉，不替換原圖，不commit／push。

結果由三條共同規律組成：同一具名接口相等分割給完整fibre雙射；degree4外鄰同色
給完整lift；低接線unary在proper三色框至多禁止一個已用色。第三條合原55容量
及已採納三列出口，排三接線U；原七個同步模板再由兩接線bridge後果一起排除。
完整含U父情形的剩餘必 `k_U=2、M_U=∅、M_L=I、4≤k_L≤6`，U每列恰禁
一個支援已用色，L無shared contact且含cycle或root-contact cutpoint。
一般原55／N2／E-ARC2仍OPEN，九格仍七格已有覆蓋。

- [接口作者稿](paper/REPORT.md)：初等分割／26與7代表／共同弧幾何，保留最初停止点。
- [禁色作者稿](review/REPORT.md)：無界已用色引理、來源容量、精確剩餘合同。
- [獨立審查](review/independent_review.md)：另一作者禁色推論獨立核對；接口作者的自身重讀明示。
- [完整fibre與join控制](controls/REPORT.md)：228保存分量，36,480完整local cells，10,400同列joins。
- [禁色引理局部校準](controls/PAPER_REPORT.md)：89份全部前提觸發，445個三色列已用禁色至多一個；9,120完整equal-pin cells重算。
- [原800控制重查](review/equal_pin_full_probe.json)：保存原附件及完整equal-pin lifts；較強全色空列命題有10局部反控制。
- [局部反控制的源界線](review/stronger_lemma.md)：具名unary控制含原K₅ minor，亦違原55容量；非完整target來源。

完整target控制為 `not triggered`，無界排除由紙面及既有採納依賴承擔；Python不證
來源實現或無界完備性，既有Lean build不形式化新論證。完整tuple、空fibres、原ordered
contacts／owner／附件／框／bridges／rotation權威均保留，沒有拼不同列的marginals。

實際checks、stdout／stderr及sealed hashes见 [verification](verification.json)。
重播命令以canonical §8為準；本輪未重跑上游N45／44／SD-A／ES／ER生成、原rotation或全工作樹DocGraph。

文件傳播：

- Updated L0：新canonical及本audit；舊long同步／殘餘統一頁首加有日期的後續範圍。
- Updated L1：Kempe該子節與STATUS對應入口，撤掉目前排程中的七模板逐案處理。
- Updated L3：README同一E入口加已採納共同縮減；主目標／大小界／OPEN語義保留。
- Reviewed-unchanged：HANDOFF研究線清單、arc大小界、diagonal採納及跨線synthesis；原有結論仍成立，沒有新增研究線或父closure。
- Remaining OPEN：共同剩餘合同的off-diagonal完整joint；其他(2,0)/(1,0)、N1／相鄰／單-root例外及一般E-ARC2。
