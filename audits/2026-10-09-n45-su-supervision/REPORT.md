# N45-SU：增量交叉驗收與第一批正式採納

2026-10-09。BASE／實際 HEAD 均為 `dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`。
[SU-A 紙面交付](../2026-10-09-n45-su-a/REPORT.md)與
[SU-J 有限交付](../2026-10-09-n45-su-j/REPORT.md)已分層驗收。
**正式採納 S 六項／U 八項 claim，僅限明列前提內的窄排除與必要化約。**
統一權威入口是 [N45原unit省略45／54](../../docs/c5_excess_two_nonadjacent_unit_core45.md)。

## 1. 紙面裁決與 closure scope

量化任意大小有限簡單 induced-C5 disk 圖、完整Σ933／941或整圖D5像、非框Σ-critical、
ε2、兩個非相鄰原degree5 roots、其餘原degree4、恰兩完整mixed，並保原contacts／
shared identity／actual support／ownership／bridges／rotation／字面框／全部relations及full lifts。
指定拒絕β的45／54 inclusion-minimal core，恰省略一原spoke或整份原incidence-one unary。

| 已採納項 | 裁決及未覆蓋範圍 |
| --- | --- |
| S-01–03 | ε1同Σ minimalization／Q必要域、χ0 degree4每欄五項零、spoke blocker二分成立；933 q2、unary blocker例外保留 |
| S-04–06 | singleton總incidence≤3通用relation、指定spoke省略u2排除、兩short的u1及2／3 LOW／HIGH必要身份成立；LOW／HIGH與long仍OPEN |
| U-REL／WIT／CROSS／CAP | 整U與contact刪除root-pairs等價、新γ全部lift singleton forcing、原見證與原收費、七格Q表、D/O/λ原一單位分配成立；coreβ不迫F非空 |
| U-S3 | 原fullB／one-sided／degree4／critical-contact witness與兩側正總incidence≤3足以排singleton support；總≥4不涵蓋 |
| U-U2／SHORT／RES | 指定整U省略u2及兩short子型排除；僅留唯一U＋一long／一short的完整同源跨列接合，必要式不給實現或排除 |

S-06 的原 H−t 連通、star 唯一長3面與三份原盾弧包含重新核對，沒有偷用 U4 的
retained44／O11 下界。U-S3 的 K4 四tethers／branch奇偶握手、兩末端private計數與最後
triangle五袋核適用性；N-empty＋原N-diagonal＋固定c軌道另給獨立交叉論證。
SU-A先封存十四裁決，再對監督預審，hash與封存／比較時間順序相符。
這是稽核者的獨立閱讀聲明與封存紀錄；工具不能證明人員此前未看其他檔案。

新任意大小步驟在既有 BASE E2／E3／E4／B-S0／B-C2／unary shield 信任界內成立。
Dvořák原講義Lemma7 strict slack及Theorem10 degree-list/Gallai另屬外部依賴，
凍結PDF hash相同。本輪讀SU-A完整論證及局部原文，未重新完成所有上游分類。
沒有新增Lean證明或形式化新拓撲。原55、其他core、無45／54來源、一般N2／E、ε≥3保持OPEN。

## 2. 交付、provenance 與有限驗收

獨立 [review.py](review.py)只用標準函式庫，不 import workerchecker；對回實際
Git BASE blobs、原檔bytes／mtime、兩份精確inventory及封存裁決。
SU-J checker433行已讀，solver由原edges重建、完整解枚舉、共享contact單一坐標，
與所有16 fibres比較；保存lift按原edges及literal pins核合法，不要求不同solver選同一lift。
本輪正常／seed17只讀重播均exit0，certificate逐byte相同。

| 核對 | 結果 |
| --- | --- |
| SU-A manifest／delivery | 56payload＋manifest＋delivery共58檔；精確inventory／hash／bytes通過 |
| SU-A輸入及封存 | 213 frozen檔、139 S/U BASE rows及17額外BASE rows，bytes／mtime相符；十四裁決hash不變 |
| SU-J manifest／delivery | 5952 entries＝53 authored＋5899 archive；另manifest／delivery，共55 authored；exactinventory及所有hash通過 |
| 跨兩稽核的BASE reads | 87 unique authority paths、432 declared reads逐byte對Git objects；重複來源不冒稱432獨立路徑 |
| S/U/J原交付 | S22、U39 authored及J90均與兩稽核初始bytes／mtime相同；原source另列 |
| SU-A verifier正常／seed17 | fresh結果寫本supervisor目錄，各exit0；兩結果byte相等 |
| 本独立provenance review正常／seed17 | 各exit0，結果byte相等 |
| SU-J正常／seed17 | 各exit0；7952不同指定整圖pin cases、690relations／2986lifts、102欄、555edgecuts／619新增lift、69原piece witnesses |

SU-J certificate SHA256：`a4b5b4c148f823f8df22a2672700eb40516bae0fd673edf8210a477af3b508ee`。
SU-A封存十四裁決 SHA256：`97ba9e80fedeb1fef95c767f525b17ffde6e676cd4b06131a8b295741ac95872`。
詳細 counts／fingerprints 見 [inputs.json](inputs.json)、[independent-review.json](independent-review.json)。
逐命令結果及最終immutable核對見 [checks.json](checks.json)與logs/。

7952不是兩次重複加總原N2域：U域7200＋S省略spoke域752，原S3040已含於U域。
19 N2目標來源／degree4拒絕X仍0觸發；12個45／54 occurrences與4個λ placement都屬N1。
288軌道候選的92界成立／196不觸發是抽象界；3模型4欄沒有來源／full lifts。
38個F空負控制僅反駁過強palette宣稱，22支援控制沒有singleton反證支枝。
上述有限證據不代替paper排除、disk實現、任意大小Gallai或Lean。

原A四findings、S/U coverage與provenance、SU-A-COV-01及SUJ-F01–05均保留。
歷史E4 core／reductions兩個checker普通／seed17的四份exit1沿用已驗收批次log；
這輪沒有重跑或改舊artifact。fresh BASE兩份歷史缺檔與whole-tree副本duplicate-ID仍FAIL。
本輪文件檢查及逐層傳播在checks.json，沒有把正式docs PASS改稱全工作樹PASS。

## 3. 整合、反向核對與下一批

Closure scope：只關上表S-spoke/u2、U-whole/u2、U-whole/two-short子型。
Canonical Source＋Evidence：新N45入口，導向原S/U、SU-A／SU-J與本監督採納。

- Updated：N45權威頁；E4 REPORT頁首有日期的後續及§4.3入口；Phase B §2.1
  的「缺支援下界」前提與窄分支效益；Kempe相關子節、STATUS直接索引、第一批歷史。
- Reviewed-unchanged：E4當輪正文／§9三列停止點、CORE_CONSTRAINTS原身份分類，
  E3 N2原化約、U1–U4的44成果；完整Σ窄結果不能更改它們的原三列量詞或當輪控制。
- Remaining OPEN：S LOW／HIGH與long；U唯一U＋long／short；singleton總incidence≥4；
  原55／一般N2／E等未涵蓋範圍。
- Propagation stop：L2。直接父題與B-S0 consumer更新窄效益，父N2仍OPEN；
  跨線common language、HANDOFF、README的語義／研究線tag不變，無需L3改寫。

第一批四份與兩份增量均已在各自scope驗收。
下一批只選 **N45-U-LP：唯一原U＋long L＋short edge-pair S，整U省略45／54 core**；
原盾費(2,2,1)分割五邊，是比singleton分支更窄的具名義務。
[三份可併行任務](../../docs/history/2026-10-09-n45-u-long-short-pair-tasks.md)
分別處理原幾何、完整跨列關係與固定控制，沒有互相等待的新結果依賴。
使用者發布；尚未啟動、未代為對外發訊息。singleton及S分支留待後續。

所有原worker目錄與封存檔只讀；只新增本supervisor／N45 source／下一批任務及必要共同入口。
共享導航由監督在輸入凍結與重播後更新；此管理diff另記，不冒稱原路由現時零漂移。
未commit／push／開PR／sub-agents。未跑全上游枚舉、廣域source搜尋或Lean，沒有相應新宣稱。
