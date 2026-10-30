# BR-SD-1g：雙原旁支／J2 屏障的正式採納

2026-10-11，owner 明確批准以 `main@c15a635e17d4be814e19aeeeeb765f3d6024099a`
為基準，執行已獨立審查的精確子域採納、必要文件同步與驗證後的 main 發布。
本紀錄與原 audit 的 candidate／未採納歷史分開；新舊 audit、frozen artifacts、
原始結果、seals 與歷史 verifier 均不改寫。

## 1. 採納範圍與不變界線

**BR-SD-1g scoped exclusion（雙原旁支／J2 屏障）正式 ACCEPTED，限
[N45 canonical §2.11](../archive/reports/c5/excess/other/c5_excess_two_nonadjacent_unit_core45.md#211-單缺額查證與無-u-二連通子域)
列出的完整八項來源合同。** 依據是
[精確量詞提案](../../audits/2026-10-11-br-sd-1g-adopt-6eae3597/CANONICAL_DELTA_PROPOSAL.md)、
[獨立 proof review](../../audits/2026-10-11-br-sd-1g-adopt-6eae3597/REVIEW.md)、
[mapping review](../../audits/2026-10-11-br-sd-1g-adopt-6eae3597/MAPPING_REVIEW.md)、
[ACCEPTABLE 裁決](../../audits/2026-10-11-br-sd-1g-adopt-6eae3597/ADOPTION_DECISION.md)、
[最終 acceptance](../../audits/2026-10-11-br-sd-1g-adopt-6eae3597/final_review/ACCEPTANCE.json)、
[SEAL](../../audits/2026-10-11-br-sd-1g-adopt-6eae3597/SEAL.json) 及
[DELIVERY](../../audits/2026-10-11-br-sd-1g-adopt-6eae3597/DELIVERY.json)。

任意大小結論由已審查紙面證明承擔；三色 β／未用 D、完整原鄰居 degree lists、
全部原坐標的 full-lift 因子及外部 Gallai 刻畫均保留。J2 原 private witness 给
`P_J2={T,D}`，使 q 起始的 T/D 交替不回頭 incidence walk 留在原 S；有限樹矛盾。
不使用 `D∈L(x1)⇒D∈P_J1`、二連通、舊 terminal lemma、R31 minor 或有限 fixtures 外推。

| 項目 | 本次結果 |
| --- | --- |
| BR-SD-1g 完整精確子域 | ACCEPTED scoped exclusion |
| Actual source | NOT TRIGGERED |
| 完整 N45-S-NOU-LS-PAIR 父身份 | OPEN |
| 新增 Lean theorem | 0 |
| 新增完整 OPEN 無條件關閉 | 0 |
| 其他 splits／多旁支／三環形狀、R31、ε≥3、一般 N45／N2／E、K∞=K≤5 | OPEN，不升級 |

## 2. 文件同步與傳播停止

Canonical 保留§1、§2.1–2.10及既採1a／1c／1e合同；只新增1g完整合同、§2結果列、
§3 scoped residual 對帳。Degree-5 guide、interfaces、Kempe guide 及 STATUS
同步該精確結果。HANDOFF 已有 degree-5／Kempe thin routing，依批准提案核對後
保持 bytes；STATUS_HISTORY 是歷史快照，保持 bytes，STATUS 直接索引本新紀錄。
直接 consumers 的 reviewed-unchanged 理由及傳播停止見
[mapping review](../../audits/2026-10-11-br-sd-1g-adoption-publication/mapping/REVIEW.md)。
沒有研究線增減或父身份 closure；不展開全域重寫。

## 3. 驗證與發布證據

命令、環境、stdout／stderr、exit code 與原始收據統一保存在
[正式採納 audit](../../audits/2026-10-11-br-sd-1g-adoption-publication/REPORT.md)。
歷史 publication verifier 的正常及 `PYTHONHASHSEED=17` 重播仍為 **exit 1**：
固定白名單只涵蓋原研究／publication 目錄，不能接受新獨立 review 或正式採納文件。
此結果原樣保留，沒有改寫 verifier 或誤記 PASS。
採納前的原 immutable adapter 正常及 seed17 均 **exit 0**；後續文件／descendant HEAD
相容性由新獨立 adapter 驗證，保護完整歷史 bytes 並固定本次已審查的 live 文件差異。

```sh
python3 -B audits/2026-10-11-br-sd-1g-adoption-publication/verify.py --check --require-tracked
PYTHONHASHSEED=17 python3 -B audits/2026-10-11-br-sd-1g-adoption-publication/verify.py --check --require-tracked
python3 -B scripts/check_docs.py
python3 -B tools/docgraph --include 'docs/**/*.md' check
git diff --check
```

正負 controls 只校準具名 synthetic 測例、完整 lifts 與 custody 拒絕機制。
新 verifier 的相容性成功不證 actual source，不承擔任意大小紙面量詞，也不新增 Lean。
最終發布須通過獨立 bytes 審查、封存讀回及零非預期漂移檢查；即時發布 SHA 以 Git
的 HEAD／origin/main／遠端 main 三者讀回為準，封存紀錄不為填 commit SHA 而改寫。
