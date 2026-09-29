---
docgraph:
  id: c5.exchange-geometry-scope
  family:
    - c5
    - c5.degree5
  derives_from:
    - c5.root-degree-excess
    - c5.adjacent-degree5-no-mixed-t2-path-palettes
    - c5.adjacent-degree5-no-mixed-t2-t1-endpoints
    - c5.adjacent-degree5-no-mixed-t2-t0-singles
---
# 「交換或幾何阻斷」假設：適用範圍遍歷

後續（2026-09-29）：[A–C 缺額型](c5_adjacent_degree5_no_mixed_t2_t0_pairs.md)
已完成：364 份支援中 source K5 排除 340，保留 24 份的 48 查詢全證；
最後八項亦只需飽和分量的 target K5。覆蓋擴為四種交換型／744 份原接合，
餘 2,804 份。新 JSON 的 coverage_extension 綁定正反向新增 192 個 IDs；
下文 3 類／552 份矩陣及 checker／artifacts 保留原輪快照，一般 A 仍未證。

2026-09-29，Git 基準 `f29b899`，納入工作區已有的三分量／四分量成果。
本輪回答 [Root 預算 §6](c5_root_degree_excess.md#6-已證機制與三層待證目標)
的 A 層機制完備性假設。**已完成子類支持這個機制；一般完備性仍未證。**
本輪窮盡原 3,548 份必要接合的分拆分類，重算已建支援表的全部候選，
另窮盡明定範圍的 1,920 份抽象路徑 list 控制。
未建立其餘分拆的新 actual-support 覆蓋，未新增來源排除或 target 定理。

任意大小結論沿用原報告的紙面證明與外部 degree-list 定理；本輪新增的是
Python 範圍稽核及有界控制，未新增 Lean theorem。研究優先序見 [HANDOFF](HANDOFF.md)。

## 1. 假設的精確位置

固定同一有限簡單圖 M，B=(b0,…,b4) 為 induced C5 disk 外框，
H=M−B 非空連通。M 為 q=01012 的 edge-minimal obstruction（不刪框邊）。
相鄰 z、w 的完整 degree=5，其餘內點完整 degree=4；
H−{z,w} 無 mixed，每個原分量只接一個 root。
指定 targets 為 p₁=01021、p₂=01212。

每個 F_C(t) 都由原 C 的**完整有序接點關係**取 tuples 色集的交集。
原圖精確接合為

\[
E_r(t)=U\setminus\left(t(N_B(r))\cup\bigcup_{C\sim r}F_C(t)\right),
\qquad Z_M(t)=(E_z(t)\times E_w(t))\setminus\Delta.
\]

target 失敗只有 empty_z、empty_w、same_singleton 三類。A 問的是：
這些失敗所要求的額外禁色，是否總能由同一來源的支援／拓撲矛盾，
或完整 palette 證書重建出的額外 source 禁色來反駁。
這仍是機制層問題；「目前程式沒有規則可用」不是 A 的數學反例。

source 預算 D+O=1 來自 q 的 minimality；不能直接當作 target 預算。
下面三個已完成子類給更強的雙列分離，**不需 T4 或其他來源接受列**。
出口接合仍須另用來源雙缺失及刪邊繼承，不能只憑 p₁、p₂ 接受推出完整 Σ。

## 2. 全部側型與原 3,548 份接合

原平面化約的四種分拆，將 (2,2) 的缺額／重疊分開後有五型：

| 代號 | t、接點分拆 | (D,O) | source F 的大小 |
| --- | --- | --- | --- |
| A | 2、(2) | (1,0) | (1) |
| B | 1、(2,1) | (1,0) | (1,1) |
| C | 0、(2,2) | (1,0) | (1,2) 或 (2,1) |
| D | 0、(2,2) | (0,1) | (2,2)，恰重疊一色 |
| E | 0、(2,1,1) | (1,0) | (1,1,1) |

逐筆保留原 join ID、兩側 ID、共同字面色 c、具名分量次序與預算。
下表數字是**必要正常形接合份數**；✓ 表示該整型已有指定雙列分離。

| z \ w | A | B | C | D | E |
| --- | ---: | ---: | ---: | ---: | ---: |
| A | 88 ✓ | 136 ✓ | 96 | 96 | 96 ✓ |
| B | 136 ✓ | 236 | 180 | 180 | 180 |
| C | 96 | 180 | 144 | 144 | 144 |
| D | 96 | 180 | 144 | 144 | 144 |
| E | 96 ✓ | 180 | 144 | 144 | 144 |

25 格全部分類；交換整張來源的 roots 後是 15 種組合，其中 3 種已完成。
已覆蓋 552 份原有序接合，另 2,996 份所在子類尚無完整支援表。
這不是「15.6% 的來源圖成立」：正常形沒有自然機率權重，且未證可實現性。

三份原有序子表共 320 份正常形，其中 144 份有必要支援、176 份纖維為空；
其非空纖維合計 1,002 份支援。整型結論包含空纖維的來源不可能性，
但本輪未新增刪除，也不把 1,002 份支援當成 1,002 張 disk 圖。

## 3. 全部已建支援表的機制遍歷

每一組完整候選都先以獨立的 16 種字面 root 色對枚舉核對 Z。
失敗候選依序重算固定框弧、首橋、原雙端點、整路徑交換的既有規則。
保存原 record／target／join 索引、完整禁色與 residual、全部支援選言、
每個框弧測試的一份 witness，以及完整重算 evidence 的 hash。
原證書 hash 綁定全部 contacts、schemas、placements、rotations、旁支與原外部路徑。

| 子類 | 必要支援 | 完整候選 joins | target 查詢 | 原失敗候選 |
| --- | ---: | ---: | ---: | ---: |
| A–A | 322 | 2,892 | 644 | 160 |
| A–B | 560 | 3,148 | 1,120 | 146 |
| A–E | 120 | 336 | 240 | 0 |
| 合計 | 1,002 | 6,376 | 2,004 | 306 |

| 最先足夠的層 | 關閉的失敗候選 | 整個 target 在此層完成 |
| --- | ---: | ---: |
| 完整搬運／容量上界，所有候選已有 root 色對 | — | 1,754 |
| 固定框弧／target 支援 | 142 | 86 |
| 同一首橋跨列限制 | 34 | 34 |
| 兩個原接點及全部中間路徑 | 126 | 126 |
| 所有奇數原 bridge 的 palette 交換 | 4 | 4 |
| 合計 | 306 | 2,004 |

所以目前 302 組由支援／幾何及跨列限制反駁，4 組需要整路徑交換。
302 不全是新 K5：其中也包含空支援族與守恆色矛盾。
這是按指定優先序分類；不宣稱規則互斥或交換規則只能處理四筆。
候選數與查詢數不同，禁止把關閉 306 候選稱作新增 306 個延拓。
本輪全為既有結論的重播，新增延拓數為零。

## 4. 各機制的必要條件與不能外推之處

| 機制 | 現有證明需要的資料／條件 | 不能略過的界線 |
| --- | --- | --- |
| 完整色置換搬運 | 同一實際支援上的 q、p 由同一四色置換對齊；搬運原完整 relation | 不可只搬端點 marginals；無對齊置換時只能用已證上界 |
| 固定框弧 K5 | 原二接點分量的 target pair 路徑；同一三框弧；兩塊的每個允許支援都碰兩指定弧；避開該 C 的原 root–B 路徑 | 必須是「存在一固定分割，對全部允許支援有效」；逐支援另選分割不夠 |
| 同一首橋 | source F_C(q)={d}；d 在實際支援上守恆；同一 bridge 兩端的 β | 首橋的 β 未必控制後續奇數 bridge；不適用 singleton target 或單接點分量 |
| 原雙端點 | source singleton、target pair、兩個原接點的 tightness；全 β 聯集及固定框弧 | 不要求 d 守恆；兩端限制不能套給下一個內點，全部中間 bridges 必須保留 |
| 整路徑交換 | source singleton d、target pair 包含 d、d 守恆、奇數長原路徑；排除每一奇數位置的其他 β 後只剩同一 b | 只交換路徑 block palettes、保持旁支；須重建整個 C 的拒絕證書，才能推出 b∈F_C(q) |

兩個具體邊界：

- **非守恆 d 仍可能幾何阻斷。** A–B record 22／p₂ 有 d=2、K={1,3}。
  首橋不適用；原雙端點強迫支援族 {23,234}，原 w–z–b0 路徑給 K5。
  不能把「交換不適用」誤記為整個 A 假設失敗。
- **首橋固定不等於全路徑固定。** 抽象 list 控制 d=3、原邊 palettes
  (2,3,1) 的完整端點 relation 只有禁色 {3}；改為 (2,3,2) 才得到 {2,3}。
  兩者首橋同為 2，因此第二禁色結論實際使用了全路徑條件。

為檢查第二點，另窮盡 d 的四色、長度 1／3／5／7、每個奇數位置獨立
選 U∖{d}、偶數位置為 d，以及 bare／leaf／triangle／nested 四種旁支。
**1,920 份皆以完整有序端點 relation 回溯核對**：192 份奇數 palettes
恒定者恰禁 {d,b}；1,728 份有變動者恰只禁 {d}。
同色框、具名端點與全部旁支保留，沒有做對稱商。
這是明定範圍的抽象 Gallai list 控制，沒有 C5 附件／完整 degree 的來源保證；
它否定「首橋足夠」的局部強化，**不是 A／B／C 的 disk 反例**。

## 5. 尚未覆蓋的適用範圍與下一入口

C、D 含 source 飽和二禁色分量。現有「重建第二禁色」反證明用
F_C(q) 為 singleton；對已有二禁色者，多找到其中一色不產生矛盾。
必須保留完整 relation，重新判定需要第三禁色、丟失原禁色或何種幾何排除。
因此不能只把 A–A／A–B 的 checker 改分拆數就宣稱完成。

B–B、B–E、E–E 雖沒有飽和二禁色，也尚缺各自的 actual-support／rotation
必要覆蓋；每側的預算不能代替兩側共用的環序。
所有未標 ✓ 的格都只列為待研究，沒有把獨立上界接合稱為實現反例。

範圍再往外擴時：

- **degree-5 root 樹：** source 邊標色與 κ=0 已證，target 仍需完整半樹訊息；
  雙 root 的相同 singleton 拒絕式不能代替整樹遞迴。
- **degree≥6／非樹：** source 預算恆等式可用，但缺額可大於一，κ 未必為零；
  本表的側型分類不適用。
- **mixed／非相鄰 roots：** 要保留多 root 有序 relation 或新的骨架接合；
  本表的 unary F 聯集和經 zw 的原外部路徑不自動可用。
- **一般平面、非 disk 外框：** 原 K5 witness 本身仍是非平面證書，
  但此處的環序必要覆蓋依賴指定 C5 是 disk 外框。

依 [HANDOFF](HANDOFF.md)，下一步仍是 A–C：96 份有序資料，首項
retained-join ID=3036、sides=(133,16)，B_z=01、F_z={2}，
w 無 spoke、F=({0},{1,2})、共同 c=3。先建立三原分量、六接點、
兩 spokes、zw 與共同色框的支援／rotation 覆蓋，尤其保存飽和 pair 的完整關係。
A–D 另有 96 份，不能與 A–C 合併為同一缺額問題。

## 6. 證書與重播

[Checker](../scripts/c5_exchange_geometry_scope.py)、
[JSON](../artifacts/c5_exchange_geometry_scope/observations.json) 與
[生成表](../artifacts/c5_exchange_geometry_scope/scope_table.md) 保留所有 25 格 IDs、
首筆具名資料、306 組反證的重算結果、2,004 個查詢分類及 1,920 個路徑控制。
所有原 artifacts 保持；`--check` 重算後逐 byte 比對，無參數只生成本層。

```bash
python3 scripts/c5_exchange_geometry_scope.py --check
python3 scripts/c5_adjacent_degree5_no_mixed.py --check
python3 scripts/c5_root_degree_excess.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_path_palettes.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t1_endpoints.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t0_singles.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際驗證與省略範圍見 [當輪紀錄](history/2026-09-29-exchange-geometry-scope.md)。
`lake build` 只驗既有 Lean 專案，不形式化本輪範圍稽核或原紙面幾何證明。
