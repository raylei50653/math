# W5 私人圈秩四兩分支排除

2026-10-13。本頁為圈秩四合併結論的權威入口；兩份隔離證據分別是
[contractible 完整排除](../audits/2026-10-13-w5-rank4-contractible-acd2b1b/REPORT.md)
與 [essential 完整排除](../audits/2026-10-13-w5-rank4-essential-acd2b1b/REPORT.md)。
目前停止點由 [Kempe 導覽](c5_kempe_guide.md#3-停止點與保留缺口)維護。

## 1. 精確合併結論

G 在全部完整外框關係不屬 K132 的 disk-C₅ 圖中先最小化內點數 k，再
最大化邊數。任取合法全內部 induced W5，原中心為 v、原鄰環為 U、原外框
為 B。令 P=V(G)\(B∪U∪{v})、F=G[P]，保留十個有序 pins、原面、rotation、
原附件、所有私人分量、bridges 及 subdivisions。則

\[
\boxed{\rho(F)=|E(F)|-|V(F)|+c(F)\ge5.}
\]

既有結果已排ρ≤3。若ρ=4，U/v位於F的無界面，就是contractible分支；
否則F含分隔B/U的essential原環。兩支窮盡原嵌入，現均完成排除。
不加入N2、edge-critical、Gallai或F連通假設，也沒有把同Σ當成同R³。

## 2. 两支的完備化約與完整關係

| 分支 | 任意來源的化約 | 完整必要模板與結果 |
|---|---|---|
| contractible | 原面計帳給c≤2；block-ear／BUP面預算只留兩-ear hexagon、雙diamond及容許path分量，原tails／共cutvertex保留 | 6,389份，完整Σ屬於511、639、767、895、1019、1023，全部在K132 |
| essential | 原面計帳給c=1、p=a=M=0、三個PPP面；私人excess六迫三角化pentagon fan與唯一原ear-to-ear外路 | 2,872份，完整Σ全部1023 |

Essential 原來源必有8≤|P|≤13；兩種B/U方位、fan短側apex的一／二附件、
兩ears與全部路徑細分的字串都有完整覆蓋。大小上界來自度數計帳，
不是任意設定的搜尋截斷。新獨立分類審查亦核對三個PPP面只可能給fan或
違反完整度數的K₄，及全部參數係數計數。

兩支均保存每份原圖十個β rows，每列全部1,024個literal U cells，含空
fibres與全部A=G−v及G full lifts。主搜尋直接計算G，另比對三色U補中心；
獨立搜尋重建原edges／rotation／faces，逐字比對完整染色。
新essential證書有29,409,280 cells、28,345,408空格、2,051,516份A lifts
及1,017,324份G lifts。證明依據是完備化約接全模板關係，實际目錄外
來源仍為`not triggered`。

## 3. 合併採納與重播

Contractible audit 是接手時已存在的未追蹤成果；原檔與舊seal未改。
本輪讀取其完整分類／獨立審查，重新執行verify、主完整checker及獨立
完整checker，均符合原6,389份與digest，再與新essential结果合併。
它的工作樹來源及HEAD來源由新audit的BASE分開凍結，未冒稱已提交成果。
本輪交接及驗證 receipts 見[研究紀錄](history/2026-10-13-c5-k14-rank4-progress.md)。

```bash
python3 -B audits/2026-10-13-w5-rank4-essential-acd2b1b/controls/check.py --check
python3 -B audits/2026-10-13-w5-rank4-essential-acd2b1b/independent/check.py
python3 -B audits/2026-10-13-w5-rank4-contractible-acd2b1b/controls/check.py --check
python3 -B audits/2026-10-13-w5-rank4-contractible-acd2b1b/independent/check.py
```

兩支normal／seed17、負控制及完整命令由各原報告維護。紙面、有限Python、
上游外部定理分層；沒有新增Lean theorem，沒有聲稱不同圖間R³等價或嚴格小代表。
一般ρ≥5來源的排除／縮減、annulus小代表、933／941及`K∞=K≤5`仍 **OPEN**。
