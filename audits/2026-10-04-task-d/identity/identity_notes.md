# 任務 D：47／75 identity ledger、root swap 與 D₅ 的獨立核對

本項只讀稽核以 `/tmp/math-task-d-audit-_l2g06k7/snapshot` 為固定基線。
未修改共用文件、研究 checker 或歷史 artifacts。獨立程式只使用標準函式庫，
不 import 六輪研究 checker，輸出 `identity_results.json`。

重播方式：

```bash
python3 audit_identity.py --repo /path/to/repository-or-snapshot --output /tmp/task-d-identity
```

## 結論與原必要域

從原 `c5_excess_two_mixed_core_single_spoke/observations.json` 自行重新篩選
`status == necessary_skeleton_only` 且原 spoke sizes 為 `(2,2)`，恰有 47／75
個具名 index；與 equal-pair 原域完全一致。每階段 exclusion list、remaining
list 均無重複 index；六階段互斥、並集等於原必要域、最後 residual 為空。
每階段分析判定的 indices 也與其宣告排除 list 一致。

| 排除階段 | 933 排除 | 933 殘留 | 941 排除 | 941 殘留 |
| --- | ---: | ---: | ---: | ---: |
| equal pair | 7 | 40 | 9 | 66 |
| short face | 8 | 32 | 16 | 50 |
| long face | 10 | 22 | 10 | 40 |
| crosscut | 8 | 14 | 16 | 24 |
| short arc | 0 | 14 | 6 | 18 |
| disjoint pairs | 14 | 0 | 18 | 0 |

對六輪 target payload 裡每份帶有原 index 的 frame（552 份 record occurrence：
933 有 203，941 有 349），逐一核對原 root order、spoke supports、named edges、
完整 apex rotation 四欄與相同 source 的原 record 完全相同。這些 occurrence
可在分析清單、排除清單、殘留清單重現同一身份；這是正常 artifact 複本，
並不是 exclusion list 重複計數。

## Root swap：原身份成立，canonical rotation 不必相等

122 份必要 skeleton 的原 edges 均可自行重建為原 FRAME、ab、兩側實際 spokes。
每份 root swap 都有唯一同源 partner，且 involution 成立，六階段的排除集合
及各階段殘留集合皆封閉於該交換。933 有 7 個 self-identities、20 個不同
partner pairs；941 有 9 個 self-identities、33 個不同 partner pairs。

**較強的「stored canonical apex rotation 與 root swap 交換」不成立。**
原 source 用 `nx.check_planarity` 任選一份 canonical embedding witness；
對以下 16 份 equal-pair self-identities，交換 root labels 後的完整 face sets
不等於該同一 record 的既存 canonical face sets：

- 933：96、112、128、144、160、176、192。
- 941：132、154、176、198、220、242、264、286、308。

例如 933 index 96 的 spokes 都是 `01`；原 augmented rotation 含 face
`[0,1,6]`，root swap 後是 `[0,1,5]`，而既存同一 canonical rotation
沒有相同三角 face。兩份 rotation 都是有效 spherical embeddings。

這項觀察**不是來源排除失敗**。獨立程式對全部 122 份都直接搬運整份
rotation，逐頂點核對完整鄰居環、所有 dart 及 Euler 等式；apex 留為原
vertex 7，鄰居恰是原五個 B vertices。刪除 apex 後，原 rotation 及
root-swapped rotation 均恰有一個 C₅ boundary face。equal-pair 的實際
sealing faces `{a,b,h}`、`{a,b,k}` 在原、搬運後及 canonical partner
三份 rotation 都相同。其餘 106 份 unequal frames 的完整 canonical
partner face sets 確實等於搬運後的 face sets。

因此可以宣稱 named source／edges／spokes／roles 的身份保持，以及 transported
embedding 保持有效；不要把此事加強成「每份既存 canonical rotation 原封不動」
或「root swap 必等於重新跑 NetworkX 所挑出的 rotation」。目前文件沒有
明文宣稱這個較強等式，但 equal-pair 的數字描述值得補一句範圍說明。

## D₅、來源 masks、色框與完整 witnesses

對全部 122 份原 necessary frames 各用十個 D₅ moves，自行搬運原 edges、
actual spokes、apex rotation；共 1,220 份。逐份檢查所有十列的同一全域
色置換以及完整 source mask 的十列 bijection：12,200 row/color checks、
1,220 complete mask checks、195,200 literal root-pair guard checks 全通過。
沒有將 933／941 的 moved masks 當成相同原 source mask。

long-face 及 disjoint-pairs 的全部 actual support pair domains 各自等於
相同原 face 的完整 power-set product，沒有遺漏、重複或只留 span。
共 6,400 actual pairs，64,000 D₅ pair transports，35,200 搬運後的
short-support 外路徑 checks 通過。crosscut 的 U／C 支援也各覆蓋完整
8-subset domain；artifact 分析及排除清單各存一份同樣 payload，因此
本程式的 U／C 各 384 次是 stored occurrences，對應各 192 份不同
frame/support records。

short-arc 所有 963 份 C schemas 的 stable orbit masks 是自行窮盡全部
1,023 nonempty masks 後的恰好全部 F-empty schemas；7 份 U stable palettes
和 15 份 V nonempty palettes 也獨立檢查完整且無重複。
六份原 941 frames 的所有 60 row/color transports 與原 source mask 搬運
完全相符；indices 179、239 搬至 949，其餘 155、175、243、263 搬至 941。

對六份 frame 的每一份 schema／palette join witness，使用該原 rejected row
的一個全域 color permutation 的反置換，並依 root role swap 使用
`(b,a,y,x,v,u)` 或 `(a,b,x,y,u,v)` 還原。
**606,690 份六角色 witness pullbacks 全部滿足原 spoke、ab、ax、by、au、bv
guards**；其中 3,150 份 shared-contact witnesses 維持 x=y。
這證明現存 fixed-domain witness tables 的同源與色框一致，不宣稱
abstract schema 已實現成 arbitrary-size source graph。

crosscut 的具名 geometry comparison 933 index 100 → 941 index 134，
其全圖 D₅ 真正搬運的 source mask 為 **940**，不是 941；checker 已明確記錄
`compared_source_masks_equal=False`。這是幾何對照，不可借此合併原來源 relation。

## 現有 checker 覆蓋與具體修訂建議

1. `scripts/c5_excess_two_mixed_core_four_spoke_disjoint_pairs.py:228-265` 的
   completion ledger 是 bookkeeping，docstring 已明言不重證 old proofs。
   它在 249-250、253、256 把 lists 轉為 sets，因此不能單獨檢出後續 list
   的重複 indices；而 240-245 只將第一階段的原 domain 四欄綁回 source。
   本次獨立 audit 補足這兩項，確認現存資料沒有重複或 identity drift。
   可新增獨立 audit entrypoint，或於下一版 checker 加入 list cardinality
   及每階段 identity checks；不要為加強檢查重寫歷史 observations。
2. `docs/c5_excess_two_mixed_core_four_spoke_disjoint_pairs.md:128` 的
   「確認無重複／遺漏」現已獲本次獨立 evidence 支持；若只引用當前
   completion_ledger，應明列它檢查的是 sets 的互斥覆蓋，並連到新的
   list uniqueness／all-stage identity 稽核。
3. `docs/c5_excess_two_mixed_core_four_spoke_equal_pair.md:179-180` 及
   `docs/history/2026-10-03-excess-two-four-spoke-equal-pair.md:26-28` 的
   16 次 root 交換，是 named edge skeleton 和 sealing triangle scope；
   原 checker `equal_pair.py:129-132` 只檢查 swapped edges 等於原 edges。
   建議補句：「root swap 搬運整份 embedding；不要求其等於來源 checker
   任選的 canonical apex rotation。兩個 sealing triangle 身份保持。」
   此為精確化 coverage，並非修補已發現的數學排除錯誤。
4. `single_spoke.py:148-153` 已說 chosen rotation 不提供 full source
   disk realizability，可引用此既有邊界以避免把 chosen witness 讀成
   source 唯一嵌入。
5. `disjoint_pairs.py:179-224` 的 D₅ checks 有 original support/path/row
   covariance，但不重新計算 source masks；本次獨立 mask audit 已補上。
   `short_arc.py:132-145,202-207` 則本來就保存 source mask 的真實整圖搬運。
   報告及摘要須保留 941 → 949 的兩個 original identities，與 crosscut
   933 → 940 的幾何對照。

所有結果仍限於既有固定必要域、固定 schemas／witness tables 及身份核對。
本項未重證任意大小紙面拓撲、一般來源實現、ε≥3、Lean theorem 或一般出口。
