# 大 k 的 C5 真 disk 隨機反例搜尋

2026-10-23。BASE `78375cc0e995c868c221605c24835d7e622f0091`。

已完成 k=25,…,60 的兩階段非窮舉搜尋：**14,400 個不同帶標號原圖、144,000 個
完整圖上的精確邊界列判定，沒有出現 K132 以外的 Σ**。第一階段生成與 SAT 約103秒，
第二階段約79秒；另作獨立核驗及 seed17 重播。一般 `K∞=K132` 仍 **OPEN**。

[第一階段提議](PROPOSAL.md)及[第二階段提議](TARGETED_PROPOSAL.md)各在對應實驗前建立。
兩個 pilot 分別已包含於正式10,800／3,600圖中，不重複計數。

## 凍結的問題與判定契約

`k=|V|−5` 是私人內點數，總頂點30–65；原有序邊界固定 `(0,1,2,3,4)`。
每圖保存全部原邊、有向內三角面及十列；並不以較小目錄代表代換原圖。
比較 [凍結 cells.json](frozen/artifacts/c5_cells/cells.json) 的132個帶標號 key，
SHA256 `04650cea947a5086360e895c1a7350690f53da745314379a3328b97ee02d81b8`。

十列依序為 `01012,01021,01023,01201,01202,01203,01212,01213,01231,01232`，
第 j 列的存在延拓性給 `2^j`。只作 S4 色正規化；主比較不商 D5。
Glucose4 對同一完整原圖逐列作 SAT／UNSAT；每 SAT 列保存一份全頂點著色，
UNSAT 列保留 `null`。這完整決定存在性的 Σ，沒有枚舉或宣稱保存全部 fibres／計數。
未完成搜尋不當作拒絕。本輪所有主 SAT 判定均完成。

既有共同 `k≥23` 與固定 r6 的 `k≥25` 沿用各原權限；本實驗未限制 r6，
未提高下界，也未搜尋23／24。近三角化是最小反例的來源正規形，
不主張任意稀疏圖都能保持 Σ 補成三角化。

## 抽樣方法與結果

每個模式、每個 k 各100個獨立派生種子的短鏈端點。
前三級從五輪隨機插三角面內點，再提議40n次內邊翻轉；主種子20261023。
`degree-biased` 以 `exp(−1.5ΔE)` 接受升能翻轉，
`E=Σ內 max(0,5−deg)+Σ框 max(0,4−deg)`。
這是有限步數非均勻抽樣，沒有穩態、混合或所有來源可達性保證。

| 模式 | 圖數 | 已知 keys | Σ=1023 | R1 core平均內點 | 指定必要幾何子集 |
| --- | ---: | ---: | ---: | ---: | ---: |
| free，允許框弦 | 3,600 | 113 | 786 | 26.64 | 0 |
| chordless，保 induced C5 | 3,600 | 94 | 1,676 | 26.70 | 0 |
| degree-biased，保 induced C5 | 3,600 | 80 | 2,791 | 39.10 | 0 |
| minimum-geometry，硬保指定幾何 | 3,600 | 1 | 3,600 | 42.50 | 3,600 |

指定必要幾何子集指：內點度≥5、框點度≥4、原C5無弦、無非面三角形、
無內點同時接兩個不相鄰框點的二邊crosscut。這不是全部最小來源條件，
通過不表示來源最小、目錄外、critical 或可實現932／933／941。

僅三角面插點會保持原Σ，故特別記錄反覆刪除私人度≤3點的 R1 core。
free／chordless 的全部7,200圖仍有三度內點和非面三角形；
degree-biased 的3,309圖最低內度三、291圖最低內度四，仍全部 E>0。
因此第一階段雖有真正的大 core，沒有進入上述必要幾何子集。

第二階段改用同心五圈三角環帶與末端五輪中心，再由保嵌入的內點vertex split
補足 k；主種子20261024，每圖提議200n次硬保上述條件的翻邊。
獨立核對種子完整有向面、每次split與終點幾何。
每個固定 k 都有100個不同帶標號終點；未檢查彼此非同構。
3,600圖的R1 core都等於原k，內部n₅在11–40間，每圖至少四個無框鄰的內部五度中心；
其中3,027圖另滿足 `h=Σ框(deg−4)≥3`，其餘573圖不滿足這一更強必要條件。
全部Σ都是1023，即完整十列皆可延拓；這一集中現象仍可能受起始族與鏈長影響。
無分離三角形／crosscut是此模式硬保的條件，不把它們當作抽樣新發現的強迫定理。

合計見到126個已知帶標號keys、23個D5軌道；D5僅作附加統計。
未見的六個已知key為127、251、383、475、607、859，均有既存小witness，
所以這也直接顯示本生成器的頻率偏差。完整分層表見
[production.summary.json](production.summary.json)、[targeted.summary.json](targeted.summary.json)
與[analysis.json](analysis.json)；抽樣審查見 [SAMPLING_REVIEW](review/SAMPLING_REVIEW.md)。

## 獨立驗證與重播

主 SAT 程式先以凍結132份小代表重算全部十列，零分歧；另對內部K5非平面控制
得到目錄外Σ=0，確認 evaluator 沒有先套目錄或平面必要screen。

獨立程式不匯入 sampler、SAT套件或 NetworkX，從實際原邊及有向三角面核
邊的相反方向incidence、頂點link、Euler、連通性及唯一原外框，
以原圖全點著色核每份接受witness，再用獨立finite-domain回溯判定拒絕列。
每圖的度數、R1 core、非面三角形、crosscut、種子與邊集SHA及全部分層表另獨立重建。

第一階段108,000列含91,940份合法全點接受witness及16,060個完成的獨立UNSAT判定。
獨立CSP的100,000節點上限曾在兩圖的三個接受列停止；這三列的原完整witness
已逐邊獨立核實，足以完成存在性判定，沒有未完成的拒絕列被當作UNSAT。
此差別保存在 [production.completed.json](review/production.completed.json)，
原有cap結果亦保留。正常與seed17的CSP輸出一致。

第二階段的36,000列與3,600圖之完整核驗，見
[targeted.completed.json](review/targeted.completed.json)及
[targeted.metadata.json](review/targeted.metadata.json)。
兩階段全部原圖另由主種子於seed17重新生成，逐圖、逐列及每份全點witness吻合：
[第一階段重播](production.seed17-replay.json)、[第二階段重播](targeted.seed17-replay.json)。
控制另包含132份catalogue、320個暴力對照列、11種污染拒絕及明示UNRESOLVED控制，
見[控制證據](review/controls.json)及[獨立checker說明](review/README.md)。

純Python獨立核驗命令（output須為尚未存在的新檔）：

```sh
python3 audits/2026-10-23-c5-large-k-random-78375cc/review/independent_check.py \
  audits/2026-10-23-c5-large-k-random-78375cc/production.samples.jsonl \
  --catalogue audits/2026-10-23-c5-large-k-random-78375cc/frozen/artifacts/c5_cells/cells.json \
  --max-nodes 100000 --output /tmp/c5-production-new-review.json
```

上述保留原節點cap，會忠實報兩圖的接受列搜尋未完成；
直接完整witness完成權限及正常／seed17合併核對由
`review/complete_reviews.py`重建。幾何統計分別用
`review/check_metadata.py`、`review/check_targeted_metadata.py`。

主程式依賴 `python-sat==1.9.dev17`、solver `g4`；本輪裝於隔離的
`/tmp/c5-large-k-sat-78375cc`，未改專案依賴。新環境可用：

```sh
uv run --with python-sat==1.9.dev17 python \
  audits/2026-10-23-c5-large-k-random-78375cc/sampler.py replay \
  audits/2026-10-23-c5-large-k-random-78375cc/production.samples.jsonl \
  --output /tmp/c5-production-new-replay.json
```

第二階段以`targeted.py replay targeted.samples.jsonl`重播；指定`PYTHONHASHSEED=17`
可核雜湊種子獨立性。相同求解器版本用於逐份witness的完全重現，
異求解器可另用合法witness及精確Σ作語義重驗。

## 停止點與文件範圍

本輪完成已記錄的有限隨機實驗，沒有找到反例；零命中只支持這些生成器的經驗結果，
不提供未知圖母體的漏失率上界，亦不證一般排除、較小bad或新Lean定理。
特別是定向樣本都從五圈環帶起始，k≡1 mod5時甚至沒有初始split；
接受很多翻邊與不同帶標號終點，都不足證明已探索全部必要幾何子集。

下一個窄實驗義務：採獨立起始族，並在固定k比較不同鏈長的完整十列分布，
優先尋指定幾何內Σ≠1023的實際來源；維持同一原圖、同一有序框及完整十列，
任何K外命中先獨立核完。再次實驗之前另先記錄提議。

核對／更新範圍停於L1：State導覽新增此實驗入口，STATUS新增短索引；
既有一般覆蓋及具名幾何來源仍OPEN，故HANDOFF及其他研究線不變。
本輪未commit／push；原先未追蹤的941外側工作未修改。

最終核對：六份凍結來源與BASE／目前原檔逐byte相同；9份Python程式可解析。
`scripts/check_docs.py`通過（713份Markdown、9,478個本地連結），
正式docs的DocGraph通過（97份metadata文件、383條關係、零錯誤），
`git diff --check`通過；這不是全工作樹的歷史封存DocGraph裁定。
本輪沒有Lean變更，未重跑`lake build`。
