# 單缺額查證與適用性的相連證據整理

2026-10-11。使用者明確授權「整理目前進展 commit +push」。
整理起始 BASE：`4dd11f422c6fa49265a412085116b088786d0344`；起始工作樹僅兩份新audit未追蹤。
本目錄保存其後的整理／查核，不修改原A/B封存bytes；Git發布結果以即時SHA回讀為準。
目前入口：[degree-5精確定理](../../docs/c5_degree5_interfaces.md#7-二連通單缺額查證與-4554-接入)、
[N45適用性](../../docs/c5_excess_two_nonadjacent_unit_core45.md#211-單缺額查證與無-u-二連通子域)、
[Kempe停止點](../../docs/c5_kempe_guide.md#3-停止點與保留缺口)。

## 本輪已確認的進展

[A獨立查證](../2026-10-11-c5-single-deficit-biconnected-5e7a5ffd/REPORT.md)裁定指定前提成立：
有限簡單ordered induced-C5 disk M、H=M−B二連通、唯一s完整M-degree5、其餘4、
proper β拒絕，推出d_H(s)=2且H−s Gallai tree。不需minimality、T4或lists全緊。
無界量詞由正式版Cranston–Rabern定理與參數化原圖branch sets負責。
三類撤前提反例、960 assignments、758 minor controls分層保存，未新增Lean。

[B適用性](../2026-10-11-single-deficit-applicability-804e3b0b1b/REPORT.md)封存時A仍待驗，
其原conditional欄位保持歷史語境。A現在已查證，應用仍須核同一actual X=M、
M完整degree與H_M二連通。無U兩long、long／singleton short及相鄰兩mixed45／54
的二連通subsets有紙面排除；真edge-pair short縮為兩原接點間的無旁支Gallai鏈。
完整OPEN身份新增無條件關閉0；540凍結輸入與literal控制不證actual target來源存在，
所有精確來源控制均not triggered。

## BR-SD-1a：本輪紙面 screening，待獨立封存

舊B的[BR-SD-1合同](../2026-10-11-single-deficit-applicability-804e3b0b1b/NEXT-TASK.md)
明列無旁支、J1/J2共用r、J2/J3經單uv、末端各一臂的精確三環域。
它可先驗直接矛盾，不預設存在能保持額外染色資料的uv收縮。

固定β未使用色D於s，從原M定義C的L^D列表。每點完整度4給|L^D(v)|≥d_C(v)；
M拒絕β且D可用，故C沒有L^D-coloring。由已在degree-5介面§2引用的
Dvořák [Theorem10，p.6](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，
拒絕的degree assignment為blockwise uniform：相交blocks的palettes互斥，
非割點的列表恰等其block palette。主端與獨立review均核對此原文。

J1只需避開r及外臂錨點；J2只需避開r及u。odd cycles至少三點，
故各有一個既非C割點、亦非s-contact的原私有w_i。
D∈L^D(w_i)=S_{J_i}，於是D同時在兩環palettes中；
但J1∩J2={r}迫S_J1∩S_J2=∅，矛盾。
這段screening不依A、T4區域定位或R27 minor。它只對所列精確域給紙面判斷，
尚未在N45覆蓋表標adopted／closed；新[NEXT-TASK](NEXT-TASK.md)要求獨立封存。
一般三環bridges、旁支、非二連通、55及主命題仍OPEN。

另精化旧任務的四query措辭：F_C(β)查詢同一C的附件與s–C約束，
暫不施加s–B spokes；完整M拒絕β，四個s色全圖延拓皆空。
如果另走R26 target拓撲合成路線，target四query／β-minimality是額外保持要求，
失敗不能單憑它否定所有來源minor。兩原audit不因本段更正而被覆寫。

## 原封存、重播與出版後入口

[custody-before.json](custody-before.json)綁兩audit的630個regular檔、48,427,730原bytes。
修改共享docs前，A seal、前提normal／seed17、minor normal／seed17、兩份corrupted certificate
預期exit1及B normal／seed17均實跑；[checks-before.json](checks-before.json)與logs保存raw輸出。
A原manifest核57payload、11個frozen BASE文檔，所有起始tracked live bytes當時零漂移；
B核540 frozen inputs／571payload，normal／seed17相同。

A原verify_seal要求HEAD==BASE與舊live docs不變；前提checker亦綁四份live docs hash。
出版後改用新[verify.py](verify.py)：核兩包原payload／frozen BASE，
`--replay`在TEMP複製原A並從Git BASE重建四份依賴docs，使用既有NetworkX3.5 Python，
原前提／minor checker不變。這是明示的frozen-BASE overlay，不冒稱live HEAD或完整checkout零漂移。
B原verify_audit只綁frozen bytes與Git BASE，可在新HEAD原樣重播。

```sh
python3 -B audits/2026-10-11-single-deficit-publication/verify.py --check
python3 -B audits/2026-10-11-single-deficit-publication/verify.py --check --replay
PYTHONHASHSEED=17 python3 -B audits/2026-10-11-single-deficit-publication/verify.py --check --replay --seed17
```

大型證書與歷史whitespace原bytes依既有audit archive工具壓縮封存；fresh checkout先
`python3 tools/audit_archive.py restore`，不以重生成替換舊證書。
本輪限定追加7個A/B原路徑與6個blobs，舊2,414個file records／1,485個blob records全保留，
詳細見[archive-append.json](archive-append.json)。
[Git index還原核對](stage-reconstruction.json)從待提交Git bytes與compressed blobs
獨立重建630個原檔、48,427,730 bytes，逐SHA256通過；623檔直接追蹤、7檔封存還原。
文件、DocGraph與Lean的本輪實跑結果見[checks-after.json](checks-after.json)及
[歷史紀錄](../../docs/history/2026-10-11-single-deficit-progress.md)。沒有重跑舊R／N45大型枚舉，
沒有新actual來源搜尋，lake build不提升本批紙面定理為Lean證明。
