# W5-RANK3-E：圈秩三 essential 來源排除

2026-10-13，BASE `45bc1c3dc9dacaee1b10df9d64f1c6a27bb0e954`。
開始工作樹乾淨；本包為本地研究與驗證，不含 commit／push。
來源及凍結輸入 SHA256 見 [BASE.json](BASE.json)。
正式入口：[私人圈秩三環繞分支](../../docs/c5_w5_private_rank3_essential.md)。

## 結論及來源量詞

在全部目錄外 disk-C5 圖中，先最小化內點、再最大化邊數，取原來源 G。
任取全內部 induced W5，保留 B/U 十 pins、中心 v、原 rotation 及全部
完整染色。令 P=V(G)\(B∪U∪{v})、F=G[P]，圈秩為 ρ。
**若 F 含分隔 B/U 的 essential 環，則 ρ≥4。**
既有無條件下界仍是 ρ≥3；本輪只排掉 ρ=3 的 essential 分支。
尚餘 ρ=3 的 contractible 分支，其私人點數必要範圍收為 7≤r≤11。
一般圈秩至少四、任意大小小代表及 K∞=K≤5 保持 OPEN。

## 任意大小覆蓋及有限證據

[完整紙面證明](structure/PROOF.md)先由原面／完整 degree 計帳，推出 essential
來源私人圖連通、沒有 B–U 邊或 BUP 面、恰有兩個 PPP 三角面、7≤r≤12。
私人度數 excess 恰四迫兩面形成 diamond；其餘原邊恰為連接 tips 的一條
路徑。原 rotation 唯一決定兩側 fan 編碼，並保留原 pin maps 及共同色框。
這把任意大小來源完備涵蓋於 1,283 份必要模板；不是任選搜尋上限。

[主 checker](controls/check.py)重建所有 oriented faces、原邊及 rotations，
以 MRV DFS 保存每一份 A=G−v 完整 lift、十列各 1,024 cells（包含空格），
再以 U 三色唯一接回中心，與直接 G DFS 比較。
[獨立 checker](independent/check.py)以另一種步長預算遞迴枚舉完整域，
從鄰點區間重建原邊、從 rotation 走面，再用固定頂點順序對 A/G 分別直接
枚舉全部著色，沒有 import 主 checker。

| 核對項目 | 結果 |
|---|---:|
| 必要模板 | 1,283 |
| 全部 cells | 13,137,920 |
| 空 cells | 12,714,781 |
| A 完整 lifts | 730,480 |
| G 完整 lifts | 352,020 |
| 完整 Σ 分佈 | 1,283 份皆為 1023 |

每個目標來源在自己的原 B 下拉回後仍是 1023，與 933／941 矛盾。
模板可以保留尚未符合全部來源度數／小環條件的圖；擴大的必要域已全被相同
十列結論排除，故不需以額外 pruning 支持結論。
此處沒有構造或宣稱 R³ 小代表，也不聲稱 fibre 基數保持。

## 審閱、重播及負控制

[獨立紙面審閱](review/REVIEW.md)核對 general-ρ 公式、全部 essential 位置、
diamond 覆蓋、原 rotation、字域及 literal pin 拉回。
正常／seed17 主重播結果相同；[摘要](controls/summary.json)與
[模板索引](controls/templates.json)逐圖保存雜湊。
完整 [gzip 證書](controls/certificate.jsonl.gz)的解壓後數學串流 SHA256 為
`98ecc77b4b7affbd61dbdb5e84f7818f96f2128ff057dbe539de5e6c47d30a2c`。

```bash
python3 -B audits/2026-10-13-w5-rank3-essential-45bc1c3/controls/check.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-w5-rank3-essential-45bc1c3/controls/check.py --check
python3 -B audits/2026-10-13-w5-rank3-essential-45bc1c3/independent/check.py
python3 -B audits/2026-10-13-w5-rank3-essential-45bc1c3/independent/negative.py
```

主結果見 [normal](controls/replay.log)、[seed17](controls/seed17.log)；獨立結果見
[完整重算](logs/independent.log)。[負控制](independent/negative.py)在同一具體
正控制上注入四種破損：漏 diamond 原邊、錯 U pin map、反 U 面、漏 full A lift。
兩個 validator 均拒絕，八次結果見 [negative.log](logs/negative.log)。
它們是 `counterexample to corrupted certificate`；正常必要模板檢查是
`triggered and holds`；真正最小 933／941 來源實例是 `not triggered`。

紙面證明與 Python 固定完整域分開；沿用既有 K132、4CT 及外部有界計數定理
的信任邊界，不重新驗證該文獻的計算證書。原外部來源為
[Dvořák–Lidický 原論文](https://arxiv.org/abs/1907.04066)；本輪新增結論來自
上述原面化約及有限完整字域，未將外部猜想當定理。
沒有新增 Lean theorem；既有專案 `lake build`（8,831 jobs）通過，只作回歸。
正式文件／DocGraph 檢查通過；全工作樹 DocGraph 保留 62 項既有 duplicate-ID
失敗，原 audit／scratch 不為本輪刪除或改寫。

## 文件接入與停止點

Closure scope：只閉合完整最小來源的 ρ=3 essential 分支。
Source／Evidence：本包紙面證明、兩套完整 checker 與 full-lift 證書。
Updated：正式入口、W5 父入口、五度交付入口、Kempe 導覽及 STATUS。
Reviewed-unchanged：README／HANDOFF 的研究線及使用方式不變；全域正規形、
C8 的八項殘留及 E-ARC2 範圍不由本包修改。
Remaining OPEN：contractible ρ=3、ρ≥4、一般 marked annulus 小代表及主命題。
Propagation stop：L2；普遍 ρ≥3 及一般主命題的真假狀態沒有改變。
完整本輪驗證狀態另見 [VERIFICATION.json](VERIFICATION.json)。
