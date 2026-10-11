# BR-SD-1g finite controls

BASE `dbdc4c35f785519c8e3cb0260807f0d2feb82469`。本控制包只校準六份固定小圖及具名錯誤推論；
**actual target source count = 0，完整原來源驗證 = `not triggered`**。
任意大小的 block-incidence-tree 證明量詞由主 PROOF 與獨立 paper review 承擔。
沒有把 degree／palette 合法推成 disk、Σ、criticality、原 ownership 或 M minimality。

## 完整小圖與三層輸出

每份 fixture 的 J1/J2/J3 都是 triangle，原 J1 唯一 witness x1 接 W1 triangle；
x1 的 d_C=4、k=0、t=0，成為 J1/W1 割點，J1 原 witness preservation 為 `counterexample`。
J2 的 w2 未改動，只屬 J2、d_C=2、原兩附件 B0/B1，list 恰 {T,D}；此檢查為 `triggered and holds`。
W1 屬 L，W2 屬 S；所有原附件均在**一次建立含完整兩旁支的 C 後**指定，
沒有把旁支加在已 full-degree4 的舊來源，也沒有删原附件。
每個原 C 點保完整 adjacency、逐點 degree／attachment／s-contact／ownership 表，
同一 M/G 全邊、r 原唯一省略 spoke、s 的三 spokes、literal β、full LD lists。

| 固定配置 | p/q 原臂長 | W2 接點／接入邊數 m | 完整 C/M β lifts | 完整 Gallai palettes |
| --- | --- | --- | ---: | ---: |
| 最小三 triangle | 0/0 | J3 唯一普通 witness w3，m=2 | 64 | 0 |
| v 接點 | 1/0 | v，m=1，stem 加 triangle | 224 | 0 |
| a3 接點 | 0/1 | a3，m=1，stem 加 triangle | 32 | 0 |
| 正長臂內點 | 1/2 | t1，m=2 | 144 | 0 |
| q 接點直接 cycle | 0/1 | q，m=2 | 32 | 0 |
| q 接點 stem | 1/2 | q，m=1，stem 加 triangle | 96 | 0 |

完整 C tuples 與同一 β、s=D 的完整 M tuples 精確雙向相等，並另外計算 G 的全部同 β lifts。
16 個 ordered (p,q) fibres 每個都保存 C/M/G 的全部 tuples，包括空 fibre；不是只保 marginal。
六圖自身都**接受 β**，故 M 拒絕／inclusion-minimal 原來源前提不成立；
這與新排除路線相容，不能把這些 synthetic 圖宣稱是 actual target source。
source-like graph 的原 retained-edge source witnesses 為 `not triggered`；未假造證書。
`finite_palette_search` 保存每個原 block 的全部允許 palette candidates，窮舉互斥與逐點完整 union，
六圖完整 palette assignments 都為空。此項 finite search 為 `triggered and holds`。

`exclusive_T_D_route_premises` 單獨保存同一 T/D：S\{q} 每個 list 皆含兩色、q 含 T 不含 D、
J2 唯一 private witness 的 list={T,D}、J2 連到唯一出口 r、q 各 incident block palette candidates。
這是有限前提校準；其任意大小 alternating-incidence-tree theorem 明確為 `not triggered by finite controls`。

## 保留負控制

`negative_controls` 中所有 synthetic/abstract source status 都是 `not triggered`。

- W1 接入 J1 triangle 唯一 witness：合法 abstract palettes J1={A,B}、J2=W1={T,D}。
  x1 完整 list 含 D，但 D 只在 W1 palette，J1 不含 D；對錯誤 cutpoint 推論為 `counterexample`。
- 「旁支第一 block 一定含 D」也有 `counterexample`：first bridge={A}，旁支 leaf cycle={T,D}。
  W 原點 y 有 d_C=3、B1 附件一份，z/w 有 d_C=2、B0/B1 附件；逐點度4。
  根 x 的 displayed list 僅記 branch-side palettes，未聲稱它是完整 skeleton source list。
- 原 witness 已有兩原 B 附件使完整 degree4，再新增任何旁支邊會至少 degree5；`triggered and holds`。
- 先删原 B1 附件再加旁支雖可偽造總度4，第一個失敗是原 attachment identity 丟失；`triggered and holds`。
- 以同數量附件 B0/B4 取代 B0/B1，degree 數不變，但原 S actual support 變三端；`triggered and holds`。
- a3=v、q 臂0或正長兩種 saturation：非空 W2 的最低完整 degree≥5；`triggered and holds`。
- 独立 degree4 synthetic graph（K5 與另一拒絕 β 的 a–b 分量）自身拒絕 β，
  删具名 K0K1 邊仍無任何完整 β lift；對「拒絕加局部度數即給 minimality」為 `counterexample`。
  此圖不屬本題骨架，也不作本題 actual-source 反例。
- edge a–b 的完整 lifts 只有 (A,B)/(B,A)，兩 marginal 都是 {A,B}；(A,A) 被 marginal 允許卻違反原邊。
  對「marginals 等於完整 lifts」為 `counterexample`。

## 重播、獨立枚舉與失敗保存

從 repo 根執行：

```sh
python3 audits/2026-10-11-br-sd-1g-dbdc4c35/agents/controls/checker.py --check --certificate audits/2026-10-11-br-sd-1g-dbdc4c35/agents/controls/certificate.normal.json
python3 audits/2026-10-11-br-sd-1g-dbdc4c35/agents/controls/checker.py --check --seed 17 --certificate audits/2026-10-11-br-sd-1g-dbdc4c35/agents/controls/certificate.seed17.json
python3 audits/2026-10-11-br-sd-1g-dbdc4c35/agents/controls/independent.py --certificate audits/2026-10-11-br-sd-1g-dbdc4c35/agents/controls/certificate.normal.json
python3 audits/2026-10-11-br-sd-1g-dbdc4c35/agents/controls/independent.py --certificate audits/2026-10-11-br-sd-1g-dbdc4c35/agents/controls/certificate.seed17.json
```

以上四項 exit=0。primary 用完整 backtracking；獨立入口用另一份 lexicographic domain-propagation 枚舉，
重新計算所有完整 C/M/G lifts、all-pin fibres、degree、actual synthetic supports 與具名旁支接入。
`verification-replay.json` 保存 argv、預期／實際 exit、stdout/stderr。
完整 M tuple 損壞、JSON malformed、只删 fibre 中一個 full lift 三種負輸入保存在專屬 certificate 檔；
primary／independent 各自全部 exit=1，已保留 stdout/stderr，不把 rejection 當成功 source 證據。

`--seed 17` 改變 search traversal，排序後全部 graph、lists、lifts、fibres 與正常證書語義完全一致；
兩證書只有 `traversal_seed` metadata 不同。
另外實際 `PYTHONHASHSEED=17` generation 的證書與 normal **byte-for-byte 相同**；
argv、環境、兩 SHA256 與 byte equality 見 `generation.hashseed17.command.json`。

第一次 generation 有可避免的 mistaken assertion：把 fixture 預期寫成「應拒絕 β」，
但新排除機制其實應迫其接受。該 generation exit=1，完整錯誤 log 與 traceback 保留；
後續改成六圖皆接受 β（64/224/32/144/32/96 full lifts）後重跑 exit=0。
最早成功的 pre-route 證書保留為 deterministic gzip archive，`archive.pre-route.v1.json` 保存原／壓縮 hashes。
這份 archive 含當時額外的 synthetic retained-edge deletion tables；最終 controls 不需要它們作來源聲稱。

本包不給 unbounded 證明、來源可實現性、canonical 採納、Lean 或父身份 closure。
**完整父身份仍 OPEN，新增無條件關閉數=0。**
