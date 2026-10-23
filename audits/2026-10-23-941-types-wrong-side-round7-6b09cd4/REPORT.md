# 941第七輪：七資源含N全排，K8完整關係與部分安全替換

2026-10-23；Git BASE `6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd`。
接[第六輪](../2026-10-23-941-types-wrong-side-round6-6b09cd4/REPORT.md)，
127項前輪輸入逐份核SHA（125份不可變證據、兩份路由快照）、零漂移，另凍結15份直接輸入。
固定同一原G／F、rotation、附件、有序B14、字面φ／ψ、完整原分量、
全部空fibres及full lifts。未commit／push。

**空M2／T6／七資源的兩N、一N一K，經完整有限共同星證書全排。**
七種身份×11型×兩種U身份共154入口；DFS與獨立cycle-catalog join
在前五星的逐步計數一致，完整N共同星皆為0。全稱來源涵蓋由完整R鄰點
封閉性及全部原鄰點包絡承擔，不限制旁觀點數、不封K／U未知外側星。
N1+N1另有三原共鄰短證。詳見[PROOF](PROOF.md)§1–2。

**七資源只餘d≠U、K0+K2的完整K8；整支替換仍OPEN。**
21份有序cap共5754個完整fibres，含3003空列、4236份完整七點lifts；
獨立核101664份字面full lifts。132份八角剖分的4224種加弦／識別標記
給398種非空關係，其中各cap的安全子庫合72份候選，完成後嚴降7／9／10點。
真正01232接受witness只選一次H，該同一H三拒絕列全部拉回同一原外側。

| K8類 | 每份非空fibres | 安全聯集 | 殘餘接受fibres |
| --- | ---: | ---: | ---: |
| 同弧單七度 | 119 | 89 | 30 |
| 相鄰雙六度 | 135 | 50 | 85 |
| 隔一雙六度 | 139 | 23 | 116 |
| 相對雙六度 | 131 | 23 | 108 |

所有實際01232接受witness都必避開安全聯集；殘餘非空不代表來源可實現，
也不表示其他安全候選不存在。此為完整關係上的條件排除，未冒稱K8整支排除。

```sh
python3 -B audits/2026-10-23-941-types-wrong-side-round7-6b09cd4/check.py
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-23-941-types-wrong-side-round7-6b09cd4/check.py --seed 17
python3 -B audits/2026-10-23-941-types-wrong-side-round7-6b09cd4/check.py --negative
```

重播及反控制收據見[VERIFICATION](VERIFICATION.json)，來源／候選審核見
[REVIEW](REVIEW.md)，正式文件與全樹歷史診斷分見[DOC_CHECKS](DOC_CHECKS-v2.json)。
有限控制為`triggered and holds`；實際完整來源仍`not triggered`。
無新Lean或lake build。

下一窄義務：K8殘餘接受fibres與同一實際外側的聯合限制，或新的安全替換；
非空支另接八資源。**空支／11型共同八外點、非空九外點、非單M2十外點、
共同k≥23不變；11整型、一般wrong-side、941／W7／J1／J2、一般較小bad及matching仍OPEN。**
