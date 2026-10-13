# W5-RANK3-C：contractible 私人圈秩三全部來源排除

2026-10-13。固定 BASE `50d5474f2446403f3b3001d5943571184c8c9936`。
工作區 `/home/ray/developer/ai/math-w5-rank3-contractible-50d5474` 為 detached
隔離 worktree；主 checkout 的 Cell 等未提交修改、並行 K13 結果均未使用。
本輪只授權本地研究與驗證，未 commit、push、PR、Issue 或外部留言。
正式入口：[私人圈秩至少四](../../docs/c5_w5_private_rank3_contractible.md)。

## 1. 結論、前提及任取 W5 量詞

在**全部**目錄外 disk-C5 圖中，先最小化內點數 k、再最大化邊數，取 G。
任取合法全內部 induced W5，原中心 v、具名原 U=(u0,…,u4)、原 B=(b0,…,b4)，
十 pins 互異，U 內恰由 v 與五個原三角面填滿。
A=G−v，P=V(G)\(B∪U∪{v})，F=G[P]，r=k−6，c=c(F)，ρ=e(F)−r+c。
本輪證明 **ρ=3 且 U/v 位於 F 無界面的 contractible 分支不可能**。

c=1 的全部來源及 c=2 的 (3,0)/(2,1) 分配、交換型、全部附樹、bridges、
cutvertices、原 subdivisions 及附件均被涵蓋。接 BASE 已採納的 ρ≥3 與
essential 排除，得到 **任取合法全內部 W5，ρ(G[P])≥4**。

仍以 k≥13、r≥7 為起點；沒有使用尚未採納的 K13-COLLAR、Cell flip 或
其他本地 K4 結果。無 N2、ε、edge-critical、Gallai、F 連通或私人度≥5
的新增前提。[BASE.json](BASE.json)凍結19份正式輸入；另由
[CATALOGUE_INPUT.json](CATALOGUE_INPUT.json)凍結同 BASE 的完整 K132 檔。

## 2. 完整紙面覆蓋

[FORMULAS](structure/FORMULAS.md)逐原面及原邊重新推導一般圈秩式：

\[
M=2(c-\rho+t_P),\quad p=a+c-\rho+t_P,\quad
\sum_Pd_G=4r+10+\rho-c-p.
\]

本分支全部三個有界 F 面均是原 PPP 三角面，包括不連通及 slit 面的排除。
所以 t_P=3、M=2c、p=a+c、7≤r≤13−2c−a。
附件上界與完整 G-degree≥5 排孤立點；c≥4 迫 r≤5，c=3 迫大小3,2,2、
最多5私人邊卻需要7條。因此本輪正式確認 c≤2，而非直接接受任務文字。

| c | 必要 r | a | M | 完整分類及處理 |
|---|---|---|---:|---|
| 1 | 7…11 | 0…11−r | 2 | rank3 K4及多blocks紙面排除；fan＋兩耳原尾路徑全部2,162模板 |
| 2 | 7…9 | 0…9−r | 4 | (2,1)紙面排除；(3,0)只剩fan＋兩尾及另一非平凡path，全部108模板 |

[CORE](structure/CORE.md)以原 block 的 `ℓ+2i=ρ(H)+2` 完備分類，先保留
內部私人頂點，再直接以 K4 內點完整 degree三矛盾排除。最強可重用引理是
**block-cut connecting skeleton 的 ear/leaf 注入式 M 計帳**：m個 cyclic
blocks 最多失去2(m−1)個 ear charges，每個未使用 ear 或其原附樹 leaf
供應不同 BUP 面，額外樹分量另供應至少兩個。其等號條件嚴格控制所有
附樹及 terminal switches，沒有誤用 essential 的 M=0／無葉結論。

[ATTACHMENTS](structure/ATTACHMENTS.md)再从原 contour及B–U crosscuts
推出完整 strip 域；包括短側 apex一／兩pins、兩種B/U方位、全部原橋兩側、
全部 terminal triangles與cross edges、每條框邊恰一次使用及同一原pin map。
字域恢復全部literal edges和原面；必要模板數如下，不作同構去重：

| c | r=7 | r=8 | r=9 | r=10 | r=11 | 合計 |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 444 | 608 | 626 | 384 | 100 | 2,162 |
| 2 | 48 | 44 | 16 | — | — | 108 |

模板可以保留違反未使用的 U-degree／小cap等更強來源條件的圖；每份仍是
經原rotation驗證的合法annulus。紙面完備性先於有限運算，沒有憑r≤11
任選小圖，也沒有省略方便編碼之外的配置。

## 3. 完整關係證書與直接排除

[主 checker](controls/check.py)由原有向面重建原邊、rotation，核對B外面、
U空面、完整G/F-degree、私人分量及一般計帳。MRV DFS保存全部A lifts；
同一份三色U指派補唯一缺色中心，再與直接完整G DFS逐列比較。
[獨立 checker](independent/check.py)沒有import主checker；另枚舉完整字域，
由鄰點區間建literal edges，從rotation走面，重算分量與每分量圈秩，再以
固定頂點順序直接枚舉A/G全部染色。兩層使用同一具名pins指派，沒有拼接
來自不同色框或不同來源的marginals。

[gzip完整證書](controls/certificate.jsonl.gz)逐圖記錄十列×1,024cells、
空fibres、全部full lifts、補中心前後關係及原圖幾何。
[模板索引](controls/templates.json)與[完整摘要](controls/summary.json)保存
逐圖hash與數量。解壓後數學串流SHA256：
`4cab09423e33b04109669daed9f5c3388ade6486b9943f55ec0cd32bcb5edd2b`。

| 完整Σ | 91 | 511 | 639 | 767 | 1007 | 1021 | 1022 | 1023 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 份數 | 2 | 8 | 32 | 8 | 2 | 1 | 1 | 2,216 |

[目錄核對](controls/catalogue.py)驗證凍結K132 hash、十列順序、全部membership
及132關係的D5封閉；[結果](controls/catalogue.json)含每種mask的所有原B拉回。
獨立checker另直接核對每份自己算得的Σ屬同一凍結K132。c=2的108份全為1023；c=1的2,162份含2,108份1023與上述54份非全收關係。
八種mask及其原B整圖拉回都在K132，直接矛盾來源目錄外身份。因此**不需要另造嚴格代表**。

本輪不宣稱任何縮減代表保Σ或R³；source-to-template是保全部pins及lifts的
同構，並非縮減。負控制中的prism有完整圖與fibres，但只是保存強度控制。
相同Σ=1023的原模板與prism，在同一β=`01012`、τ=`10103`之R³ cell
分別空／非空；故相同Σ不能升格為相同R³或保U／中心色的搬運。

## 4. 實際驗證與負控制

主normal／seed17與獨立checker完全相同：

| 項目 | 數量 |
|---|---:|
| 必要模板 | 2,270 |
| 全部cells | 23,244,800 |
| 空cells | 22,713,170 |
| A完整lifts | 928,404 |
| G完整lifts | 465,866 |

```bash
python3 -B audits/2026-10-13-w5-rank3-contractible-50d5474/controls/check.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-w5-rank3-contractible-50d5474/controls/check.py --check
python3 -B audits/2026-10-13-w5-rank3-contractible-50d5474/independent/check.py
python3 -B audits/2026-10-13-w5-rank3-contractible-50d5474/controls/catalogue.py --check
python3 -B audits/2026-10-13-w5-rank3-contractible-50d5474/independent/negative.py --check
python3 -B audits/2026-10-13-w5-rank3-contractible-50d5474/verify.py
```

主重播記錄：[normal](validation/normal.log)、[seed17](validation/seed17.log)；
獨立重播：[independent](logs/independent.log)。
[獨立紙面審閱](review/REVIEW.md)及[核心覆蓋交叉審閱](review/CORE_REVIEW.md)
另檢查任意大小化約，並非只共用主生成器的結論。

[負控制](independent/negative.py)使用c=1與c=2正控制，八種破損各被主／獨立
validator拒絕，共16次：漏私人原邊、錯圈秩、漏樹分量、錯U pin map、反U面、
以F-degree替G-degree、漏必要full lift、把essential的M=0套入本域。
另有上述相同Σ卻不同R³的完整實際反例。[負控制證據](independent/negative-controls.json.gz)
保存來源key/hash、精確破損patch/hash及完整prism幾何、十列fibres和lifts；
[重播紀錄](logs/negative-replay.log)保留實際结果。
有限合法模板是 `triggered and holds`；保存強度候選是 `counterexample`；
真正最小目錄外來源實例是 `not triggered`，後者不構成排除理由。

本輪沿用上游4CT及外部有界計數信任範圍，未重播外部論文證書、未新增外部
定理或Lean theorem。`lake build`完成8,831 jobs，僅作既有專案回歸。
正式文件653份／8,172本地連結、正式DocGraph及臨時index的儲存規則通過。
第一次文件檢查的18項歷史N45缺檔留在原log；依原工具還原第二層封存後通過，
未改寫歷史報告。20份凍結輸入及交付逐檔hash由[verify.py](verify.py)核對。
文件、儲存及逐檔保存狀態見 [VERIFICATION.json](VERIFICATION.json)；
全域DocGraph的62項舊duplicate-ID不修復，也不改稱全域通過。

## 5. 精確殘留與文件邊界

Closure scope：完整最小來源、任取合法W5的全部contractible圈秩三。
接既有essential分支採納ρ≥4；本輪沒有任何c=1/c=2、r或附件型殘留。
Source／Evidence：上述三份紙面推導、兩套完整checker、全關係證書、目錄及負控制。
Updated：新正式入口、直接W5父入口、Kempe導覽、STATUS相應條目及五輪交付入口。
Reviewed-unchanged：README／HANDOFF研究線及用法不變；全域共面正規形、C8、
外圈collar與E-ARC2不由本包修改。
Remaining OPEN：一般圈秩≥4來源的縮減、一般小annulus代表、R³代表及K∞=K≤5。
Propagation stop：L2；本輪下界及可重用結構引理不等於一般主命題完成。
