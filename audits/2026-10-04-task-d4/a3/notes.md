# A₃ 獨立稽核：固定 01／01 原來源

輸入只讀 `../snapshot/`，未 import production enumerator／join／validator，未改 production、shared docs、其他 audits 或 artifacts。`independent_core.py` 是 D₂ audit 的標準庫 MRV literal-color solver／rotation／schedule／witness 工具原樣副本；`independent_a2.py` 只把其 audit-local import 改為本地名稱。A／A₂ 的完整具名 identity、support screens、rotation 與 minor certificates 亦重新核對，沒有把先前 audit 的 PASS 當作此次驗收。

`attempt-1/` 與 `attempt-2-seed17/` 都實際成功完成；`attempt_comparison.json` 確認全部數學結果、input hashes、獨立完整 relations bytes 相同。兩份 log 與輸出分別保存，沒有失敗 attempt，也沒有覆蓋既有歷史失敗紀錄。`results.json`／`counterexamples.json` 是 attempt-1 的位元相同別名，原 attempt 仍完整保留。

## 覆蓋與精確帳目

| 固定來源 ledger，含 root 交換 | 933 | 941 |
| --- | ---: | ---: |
| A₂ 繼承具名框架 | 20 | 24 |
| A₃ 新排 01／01 框架 | 2 | 2 |
| 逐項保留其餘具名框架 | 18 | 22 |
| 逐項保留 actual U face／support records | 44 | 70 |
| 逐項保留完整 singleton schedules | 56 | 102 |
| Selected 原 support records | 8 | 16 |
| Selected 原 singleton schedules | 12 | 22 |
| 完整來源幾何相容 supports | 4 | 8 |
| 完整來源幾何相容 schedules | 6 | 10 |

四份 selected 原框架各獨立遍歷 144 rotation assignments，共 576 份；各有四份 disk rotations，共 16 份，所有 vertex rings、faces、U placements 及同 rotation 的 C faces 皆核對。Root 交換的原 index 映射逐項重建為 `[1,0,3,2]`，沒有重新正規化顏色或把 component 邊際資料拼合。

八份 literal hub instances、160 份合法三-hub root pairs 及 1,280 份逐點 exact-list external-neighbor subsets 全部重建。來源支持式 (4) 的奇偶性排除空 C support；保留空支援前置 case，並核對 C actual support 只能是該原 face 的框點 h。由完整來源碰齊 B，U actual support 必含 234，因此僅能在同 embedding 的 a 長 face。未選定框架連完整 relations／schedules 與原 A₂ payload 做字面相等比對。

36 張 fixed full-degree graph controls，三種 x／y 身份各 12 張，18 份完整 root 交換。獨立全圖 MRV 回溯重建每個完整 relation，再用另一 incidence join 精確核對；`attempt-*/rebuilt_complete_relations.json` 保存全部 C ternary、U unary、六／五角色 joint tuples 及全部 16 字面 root-pair fibres，包含空 fibres。Full witnesses 逐份在固定 snapshot 留存，並由此次獨立 validator 驗證。

- 2,880 次完整 joins、46,080 份 fibres，其中 38,112 空 fibres。
- 51,248 份六角色 tuple witnesses、2,400 份五角色 tuple witnesses。
- 所有 91,639 個 A₃ serialized coloring fields（包含重複證据與負控制）逐份驗證，沒有漏算替換前後完整 coloring。
- 360 份 `π_(a,b,u) J_G = π_(a,b,u) J_(G−ax)`，5,712 次只替換整份 C 且 C 外所有原頂點逐點保持的 coloring witnesses。
- 720 份合法 root-pair 的完整 C extension fibres；1,440 份原 spoke 接回；360 份原 ax 接回；360 份完整 G−au 乘積／au 接回身份。
- 36 份指定 01202 列的完整 singleton2／固定外部 `(a,b,u)=(3,2,2)` 延拓。
- 26,824 份 graph root-swap 的完整 witness 搬運核對。
- 全部 36 張控制圖的獨立原完整 Σ 恰為 1023。

## 紙面依賴與限制

在明定的有限簡單 induced-C₅ disk、完整 Σ=933／941、非框邊 Σ-critical、ε=2、相鄰完整 degree-5 roots、mixed C incidence (1,2)、另一原 a-unary U、雙側原 spokes 均為 01 的前提下，紙面推理成立。C 外部逐點 coloring 給字面互異色 triangle hubs a,b,h；即使 x=y₀／y₁，原 incidences 與 exact lists 仍保持。

Expanded K₄ 論證使用拒絕 degree assignment 下刪原 bridge 後兩個連通側的 slack，從四個 clique 點得到互不相交外路徑，接入原連通 triangle X，構成原 K₅ minor。K₄-free Gallai 的不限大小三-hub 論證分 leaf odd cycle／leaf bridge：前者選兩個相鄰 private 點並保留 connected remainder；後者用刪 leaf 後的 singleton root domain 與缺 hub 色交換，取得五份互斥連通 bags。Singleton C 因僅有三個外 hub 而不能完整 degree 四。此流程不需要把 G−ax 視為 minimal q-core，也不需要把原 C 收縮成固定 skeleton。

外部定理直接核對作者原始 [List coloring and Gallai trees](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)：Lemma 7（PDF 第 5 頁）與 Theorem 10（第 6 頁）適用於 connected degree assignments；來源全文 PDF 與 hash 存為 `gallai-primary-source.pdf`／`gallai-primary-source.json`。此處確認的是 exact C lists 的 slack／Gallai 刻畫，沒有宣稱完整 G 為 minimal q-core。

原 ax 非 critical 的結論保留的是整份 C 外 witness，因而推出接受列相同；六角色 tuples 可以改變。負控制逐份保存在 `counterexamples.json`：control 6、row 01012，原 joint 有 16 tuples，G−ax 有 24 tuples；omission-only `(2,3,2,2,0,1)` 滿足 X=A，原 ax 不合法，且保存同一 C 外 coloring 的原 G 替換 witness。另一負控制有八個假的 marginal-product tuples，但完整 guarded ternary fibre 為空。

所選繼承 schedules 的指定列紙面 instances 含 singleton2 24 份、singleton3 10 份，皆逐項核對 `(5−d,d,d)` 與 full ternary guards；只有前述 36 張 finite controls 實算 singleton2。**Singleton3 的覆蓋是原 schedules 與三-hub 紙面实例，沒有另一張 finite singleton3 graph realization。**

有限 solver 不證無界拓撲／Gallai 引理；控制圖 Σ1023，不是 disk／critical／933／941 來源實現。任意大小 01／01 原來源排除仍屬外部 list theorem＋紙面 topology／minor 論證；未新增 Lean theorem。停止於 selected 01／01 與整對 root 交換原來源全排，保留其他 18／22 框架、44／70 supports、56／102 schedules。Mixed12 整型、其他 pair、ε≥3、來源實現、一般出口及 K∞=K≤5 均未證。

## 保存與重播

固定 A₃ artifact SHA256：`a3f2ea31aea8cd2b9c008595f85430f0260612b431a8d1b3c03192d9171d70e2`。四份輸入 artifacts 在本 audit 前後 bytes 相同，12 個 A₃ 綁定 input hashes 全通過。獨立重建 complete relations SHA256：`a826cb0f3b439001d870e45cea95aefadee0aaf6c906e5427b8f7e858f3ebacf`。

以下用新的 attempt 目录，避免覆蓋先前结果。每次 replay 若失敗，log／空 attempt 目录也留下；修正後使用另一 fresh attempt。

```bash
python3 audits/2026-10-04-task-d4/a3/audit_a3.py --output audits/2026-10-04-task-d4/a3/attempt-3-replay
PYTHONHASHSEED=17 python3 audits/2026-10-04-task-d4/a3/audit_a3.py --output audits/2026-10-04-task-d4/a3/attempt-4-replay-seed17
```

Production A₃／helper 重播與整輪文件、DocGraph、artifact、diff checks 由 D₄ 整合方記錄；本文件不把未由本子 audit 執行的 checks 冒稱為已執行。未 commit／push。
