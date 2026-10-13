---
docgraph:
  id: c5.w5-private-rank4
  family: [c5, c5.w5]
  requires: [c5.k13-collar]
  derives_from: [c5.w5-private-rank3-contractible]
  verified_by:
    - audits/2026-10-13-w5-rank4-contractible-acd2b1b/REPORT.md
    - audits/2026-10-13-w5-rank4-essential-acd2b1b/REPORT.md
---

# W5 私人圈秩四兩分支排除

2026-10-13。本頁為圈秩四合併結論的權威入口；兩份隔離證據分別是
[contractible 完整排除](../audits/2026-10-13-w5-rank4-contractible-acd2b1b/REPORT.md)
與 [essential 完整排除](../audits/2026-10-13-w5-rank4-essential-acd2b1b/REPORT.md)。
前置下界見[圈秩三兩支合併](c5_w5_private_rank3_contractible.md)；全鏈及
保存層次見[具名關係總表](c5_w5_marked_relation.md#0-保存強度與私人圈秩覆蓋鏈)。
目前停止點由 [Kempe 導覽](c5_kempe_guide.md#3-停止點與保留缺口)維護。

## 1. 精確合併結論

G 在全部完整外框關係不屬 K132 的 disk-C₅ 圖中先最小化內點數 k，再
最大化邊數。任取合法全內部 induced W5，原中心為 v、原鄰環為 U、原外框
為 B。令 P=V(G)\(B∪U∪{v})、F=G[P]，保留十個有序 pins、原面、rotation、
原附件、所有私人分量、bridges 及 subdivisions。則

\[
\boxed{\rho(F)=|E(F)|-|V(F)|+c(F)\ge5.}
\]

上述合法 W5 要求十 pins 互異、v 的完整鄰集恰為 U、U 的有界 disk 恰有
v 與五個原三角面。來源正規形、完整 G-degree、小 C4 cap 及每環附件界
沿用[全內部五輪前置來源](c5_degree5_link_reductions.md)。因此此結論保留
**全部目錄外來源先最小內點、再最大邊數，任取合法全內部 W5** 的原量詞，
不適用於普通 annulus 或任意 disk 圖。

[雙環及上游鏈](c5_w5_private_rank2.md)已排 ρ≤2，
[圈秩三 essential](c5_w5_private_rank3_essential.md)與
[contractible](c5_w5_private_rank3_contractible.md)再排 ρ=3。若 ρ=4，U/v
位於 F 的無界面，就是 contractible 分支；否則 F 含分隔 B/U 的 essential
原環。兩支互斥且窮盡原嵌入，現均完成排除。
不加入 N2、ε、edge-critical、Gallai 或 F 連通假設，也沒有把同 Σ 當成同 R³。

## 2. 兩支的完備化約與完整關係

兩支原 BASE 均為 `acd2b1beea6c909edade565a00eeeeac05d2b3a7`，沿用
`K≤13=K≤5`，故 `k≥14、r=k−6≥8`；沒有使用後來 K14／K15 結果改寫
原分類或證書。上游圈秩三兩支的 `k≥13、r≥7` 起點亦保留各原輪次語境。
metadata 的 `requires` 記此 K13 新前提，`derives_from` 接前置 `ρ≥4`，
`verified_by` 同時指向本輪兩支證據；essential 分支的結構證明不依賴
contractible 分支，兩者是在本頁合併採納。

| 分支 | 任意來源的化約與已證大小域 | 完整必要模板與結果 |
|---|---|---|
| contractible | U/v 在 F 無界面；t_P=4、M=2c、p=a+c。c=1 時 8≤r≤12，c=2 時 8≤r≤10；block-ear／BUP 預算只留兩-ear hexagon、雙 diamond 及容許 path 分量，原 tails／共 cutvertex 保留 | c=1：5,921，c=2：468，共 6,389 份；完整 Σ 屬 511、639、767、895、1019、1023，全部在 K132 |
| essential | 含分隔 B/U 的原環；c=1、p=a=M=0、t_P=3，8≤r≤13。私人 excess 六迫三角化 pentagon fan 與唯一原 ear-to-ear 外路 | 2,872 份，完整 Σ 全部 1023∈K132 |

Contractible 的五族為 H 4,256、DD 1,665、H+P 212、DD+P 4、D+D 252；
全部 block 分配、原 tails、共 ear、橋路徑及細分均先由紙面分類覆蓋。
一般計帳、完整分類與原附件恢復分別見
[FORMULAS](../audits/2026-10-13-w5-rank4-contractible-acd2b1b/structure/FORMULAS.md)、
[CORE](../audits/2026-10-13-w5-rank4-contractible-acd2b1b/structure/CORE.md)與
[ATTACHMENTS](../audits/2026-10-13-w5-rank4-contractible-acd2b1b/structure/ATTACHMENTS.md)。

Essential 原來源必有8≤|P|≤13；兩種B/U方位、fan短側apex的一／二附件、
兩ears與全部路徑細分的字串都有完整覆蓋。大小上界來自度數計帳，
不是任意設定的搜尋截斷。新獨立分類審查亦核對三個PPP面只可能給fan或
違反完整度數的K₄，及全部參數係數計數；見
[完整來源化約](../audits/2026-10-13-w5-rank4-essential-acd2b1b/structure/PROOF.md)。

兩支都是必要域超集，不宣稱每份模板是真正最小目錄外來源。
Contractible 有 816 份不符尚未用於分類的 B degree≥4 或 U degree≥5；
保留它們不影響全超集 Σ∈K132 的排除。Essential 全部滿足這兩項 degree
條件，也不因此得到來源充分性。實際最小目錄外來源仍為 `not triggered`；
排除依據是任意來源完備化約接全模板關係，零觸發不承擔排除。

兩支均保存每份原圖十個β rows，每列全部1,024個literal U cells，含空
fibres與全部A=G−v及G full lifts。主搜尋直接計算G，另比對三色U補中心；
獨立搜尋重建原edges／rotation／faces，逐字比對完整染色。

| 分支 | cells | 空 fibres | A full lifts | G full lifts |
|---|---:|---:|---:|---:|
| contractible | 65,423,360 | 63,749,179 | 3,343,426 | 1,645,614 |
| essential | 29,409,280 | 28,345,408 | 2,051,516 | 1,017,324 |

source-to-template 是保原邊、面、rotation、十 pins、中心 ownership 及全部
空／非空 fibres、A/G full lifts 的同構；兩環搬運共用方向、各自起點可不同，
全圖只能共同更名顏色。它不減少頂點，也不構造縮減代表。按
[三色支援契約](c5_w5_three_color_support.md#1-同槽位契約與精確保存目標)，
保補中心後完整 Σ 僅要求 `pr_B R³` 相等；保 R³ 要求具名三色 U support
相等，仍不保 fibre 重數。本輪同構與證書保留較完整資料，最終只需以
每份原來源拉回後 `Σ∈K132` 直接反駁目錄外身份；沒有宣稱不同圖間 R³
等價。Contractible 的實際 prism 同 Σ 異 R³ 反控制亦保留於原報告。

## 3. 合併採納與重播

原 contractible audit 完成時 essential 圈秩四仍 OPEN、一般下界仍為四；
原 essential audit 又明列：另行審查採納 contractible 後才可合併提高為五。
兩份隔離報告的原輪次 OPEN、未 commit／push、失敗紀錄與舊 seal 均保留。

歷史合併輪次接手 contractible audit 時，它是已存在的未追蹤成果；該輪
讀取完整分類／獨立審查，重播 verify、主完整 checker 及獨立完整 checker，
均符合原 6,389 份與 digest，再與新 essential 結果合併。工作樹與 HEAD
來源由新 audit 的 BASE 分開凍結；詳見
[研究紀錄](history/2026-10-13-c5-k14-rank4-progress.md)及
[後續發布紀錄](history/2026-10-13-k14-rank4-atlas-publish.md)。
本次文件整理沿用這些 receipts，未重跑以下完整枚舉。

```bash
python3 -B audits/2026-10-13-w5-rank4-essential-acd2b1b/controls/check.py --check
python3 -B audits/2026-10-13-w5-rank4-essential-acd2b1b/independent/check.py
python3 -B audits/2026-10-13-w5-rank4-contractible-acd2b1b/controls/check.py --check
python3 -B audits/2026-10-13-w5-rank4-contractible-acd2b1b/independent/check.py
```

兩支normal／seed17、負控制及完整命令由各原報告維護。紙面、有限Python、
上游外部定理分層；沒有新增Lean theorem，沒有聲稱不同圖間R³等價或嚴格小代表。
一般ρ≥5來源的排除／縮減、annulus小代表、933／941及`K∞=K≤5`仍 **OPEN**。
