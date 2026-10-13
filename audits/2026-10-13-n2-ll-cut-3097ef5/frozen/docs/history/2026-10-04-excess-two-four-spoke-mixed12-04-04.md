# 2026-10-04：A₄，mixed12 原04／04具名三hub與完整joint來源排除

使用者指定接續 A₃ 01／01 報告與 Kempe 導覽 §3，只處理原共用
spokes=04／04 與 root 交換，重核四份 disk rotations、原 C 共同
faces、U actual supports／singleton schedules、完整 ternary 與六角色
joint；逐項核對互異色、完整 degree-list 與原外部路徑前提。

接手 HEAD=`0e3812712b68f57927df86f30a07bb8074e090f9`，根目錄
`/home/ray/developer/ai/math`。既有 A／B／C 系列、稽核與未提交產物
保持；本輪沒有 commit／push，沒有重開來源圖 catalogue。

## 成果、原前提與證據層

[A₄ 報告](../c5_excess_two_mixed_core_four_spoke_mixed12_04_04.md)只在
A 的固定完整 Σ933／941、Σ edge-minimal induced-C₅ disk、連通有效
H、ε=2、相鄰兩完整 degree-5 roots、其餘有效內點完整 degree 四、
唯一 mixed C incidence=(1,2)、a 側一原 unary U 與原 ab 前提下，
排除 **原 04／04 整份來源，含 root 交換**。

從 A₃ 原 artifact 唯讀取出四份原 named frames，在 generic source
indices 128／198 逐份重新建立；所有原 omission identities、actual
supports、完整 relations 與 rotations 完全相同。每骨架 144 rotation
assignments 恰四份 disk rotations，C 共同 faces 恰為 0ab、4ab。
原 degree 握手式迫 support 恰为 {0}／{4}；完整來源觸碰五框點迫 U
實際含 123。U 長 face 使用 a=5 的 indices 1、2，a=6 的 0、3；
root swap 的 rotation bijection 是 [1,0,3,2]。

每份合法外染色中，a,b,h 是**原連通互異色三角形**。原 C 每點的
exact list 等於 deg_C；x=yⱼ 时仍保留兩個不同 owner incidences。
拒絕則 Gallai degree-list 刻畫給原 Gallai tree；K₄ 每點的一個原
外方向由 bridge slack／singleton domain 迫抵達原三角，四條互斥
paths 給原 K₅。K₄-free 後末端 cycle／bridge 各分支也核對原 K₅
branch sets，故每份合法 C 外 coloring 皆能延拓整份原 C。

只重染 C、固定其他每個原頂點，得到
π_(a,b,u)J_G=π_(a,b,u)J_(G−ax)，使固定原 ax 非 Σ-critical。
完整六角色 joint 不必相等；反例與整份 replacement witness 保存。
共同原拒絕列 01202 的 singleton 是 **1 或 3**，取
(a,b,u)=(4−d,d,d)，即 (3,1,1)／(1,3,3)，再接出完整 ternary
與原 joint，亦違反拒絕。不得抄用 A₃ 的 singleton2／3 色表。

本輪直接讀取 [Dvořák 原講義](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，
核對 Lemma 7／Theorem 10 的 connected degree assignment、tightness
及 blockwise uniform 前提；不要求整份來源或 omission 是 minimal
q-core。不限接點數的 hub／minor 論證是紙面證明，Python 是固定域
資料與 witnesses，未新增 Lean theorem。

原短 U 路徑前提另逐項核對：每個選定 frame 有 19 份 inherited
short-support audits，14 份直接用原 skeleton 邊驗證避開 C／U 的
外路徑，5 份包络 04 的 conditional path 只由完整支援迫 C 接到
04 外；新 C geometry 排除後者的來源前提。沒有把這條 conditional
path 寫成 skeleton edge；整份 C extension 不依賴任何短 U 排除。

## 完整 ledger 與 D₅ 界線

| 同一必要域，含 root 交換 | 933 | 941 |
| --- | ---: | ---: |
| A₃ 原具名 frames | 18 | 22 |
| 本輪選定原 04／04 | 2 | 2 |
| 選定原 U support records | 4 | 12 |
| 選定完整 schedules | 6 | 18 |
| 來源支援相容 records | 4 | 6 |
| 來源支援相容 schedules | 6 | 10 |
| 本入口來源殘留 | 0 | 0 |
| 保存其餘原具名 frames | 16 | 20 |
| 保存其餘 actual U support records | 40 | 58 |
| 保存其餘完整 schedules | 50 | 84 |

933 的完整 schedule 有 (2,2,1,1) 與全 3；941 有 (2,1,1) 與全 3。
同一原 U 的 schedules 逐份保存，不逐列改选或獨立正規化。未選
原 frames 的完整物件與順序，独立核對等於 A₃ ledger 只刪原 04／04
所得的列表；其他 pairs 沒有新增來源排除。

來源證明沒有使用 D₅ 搬運。另保存 01→04 診斷：reflection
(0,4,3,2,1) 將 933／941 送至 948／950；shift (4,0,1,2,3)
送至 934／950。兩份診斷同時搬動完整 Σ、十列 row mapping、
原拒絕列及每列一份共同 color permutation，並明列原 root roles
與 U owner 固定；没有搬運原 source relations 或使用搬運來源結論。
Root 交換則獨立核對實體 5↔6、C owners、U owner、原邊、四 rotations
及 same-rotation 的 C／U 相容性。沒有固定 933／941 mask shortcut。

新 [主 checker](../../scripts/c5_excess_two_mixed_core_four_spoke_mixed12_04_04.py)
保存完整 [artifact](../../artifacts/c5_excess_two_mixed_core_four_spoke_mixed12_04_04/observations.json)：
54,015,850 bytes，SHA-256
`84f4062c0148763d3c1ccb90c8d18defed0e0c99ac633510a72f243099d1cf49`。
大型 payload 留磁碟，由 MANIFEST／產生器重播；A／A₂／A₃ 原
payload 及歷史 input hashes 均不覆寫。

## 完整 joint controls、witnesses 與負控制

[新 helper](../../scripts/c5_excess_two_four_spoke_mixed12_04_04_joint_controls.py)
有 24 張明列完整 degree 圖、12 份 root swaps；C support=0／4，
x 獨立／共享 y₀／共享 y₁ 各八張。保留所有原邊、actual attachments、
原 degree-list、paths、完整 ternary／U relation、六／五角色 tuples、
整份 witnesses 與四份 skeleton rotations，沒有縮成 contact marginals。

- 1,920 independent whole-graph joins；30,720 份 pinned root-pair
  fibres，每 row／variant 保留全部 16 份，包括 25,632 空 fibres。
- 25,568 份六角色、1,600 份五角色 tuple witnesses。
- 240 份 ax exterior 投影等式，2,912 份只替換整份 C 的 witnesses；
  全部 boundary、roots 及 U 每個頂點的原字面 coloring 保持。
- 480 份合法 root-pair 完整 C extensions／互異色核對，2,080 份
  逐點 exact degree-list checks；24 份連通原 exterior／四 rotations。
- 960 份原 spoke 接回、240 份 ax guard 接回、240 份
  G−au=T_N×R_U 完整接合／singleton identity 核對。
- q=01202 的 d=1、3 各 12 張 fixed-exterior 完整原 joint 控制。
  Triangle U support124 給 d=1，但缺來源必要 endpoint3；singleton
  U support123 給 d=3，只符合 support inclusion，不實現原必要
  schedules（support123 在兩 masks 都無 survivor）。
- Ternary marginals 假接合負控制與 root-spoke 資格分開；另保留
  六角色不等 control4、row01012：省略 tuple(1,3,1,1,0,0)，
  只重染 C 恢復原 tuple(1,3,0,0,1,0)，exterior(1,3,0) 不動。

24 張控制圖獨立完整 Σ 均為 1023；不宣稱 disk、Σ-critical、
933／941 來源或 necessary schedules 實現。兩個 singleton 顏色都有
固定 controls，也不能提升為所有繼承 actual supports 的來源控制。
Helper seed0／17 完整 payload byte-identical，SHA-256
`94c14a8c3e194495c986743089e17ba796fa49eb5979e81f15102c3be0548a6a`。

## 實際重播與工作區檢查

已通過的新入口與相關依賴檢查：

```bash
python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed12_04_04.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed12_04_04.py --check
python3 scripts/c5_excess_two_four_spoke_mixed12_04_04_joint_controls.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_four_spoke_mixed12_04_04_joint_controls.py --check
python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed12_01_01.py --check
python3 scripts/c5_short_support_singleton.py --check
lake build
```

Main 兩次重播均唯讀逐 byte 比對；helper seed0／17 也比較完整
payload。`lake build` 成功（8,831 jobs，既有 linter warnings 保持），
不表示新 paper disk／Gallai／minor 論證已 Lean 化。
没有全面重跑 A 必要域、所有歷史 minimality、容量／省略或 R 系列；
沿用前序原 artifact provenance 與紙面前提。

新 artifact 按指定路徑 record，MANIFEST 保存 144 files／139 producers。
README、Kempe 導覽、STATUS 及 A₃ 頁首接上本輪；HANDOFF 仍為同一
研究線的薄索引，線別與 tags 无變化。

`python3 tools/artifacts.py status` 通過：`ok=144`。
`python3 tools/docgraph check` 通過：62 documents、213 relations、
5 families，0 errors／notes；`git diff --check` 通過。
獨立只讀審閱另核對完整 A₄ helper 與 artifact，確認每份未選 frame
等於原 A₃ 同序物件，完整 fibres／witnesses 與 source-support 界線一致。

首次全工作區 `check_docs.py` 有七個 missing-history errors，來自
同期另兩條研究支線尚未完成的 mixed22 shared4 與 P₃ two-frame-two-unary
研究紀錄；沒有修改其內容或製造 placeholder。A₄ 所有新連結與直接
索引已建立；全工作區最終檢查結果在下方另記。

其兩份研究紀錄由原支線完成後，全工作區 `check_docs.py` 通過：
536 份 Markdown、5,565 個本地連結，anchors／直接索引／HANDOFF
合約均合格。新 A₄ scripts／reports 的尾端空白與最後換行另行核對。

## 停止點與貼用摘要

停止於原 04／04 及 root 交換來源排除；其餘 16／20 完整具名 frames
與 40／58 supports、50／84 schedules 保留。後續入口由
[Kempe 導覽 §3](../c5_kempe_guide.md#3-停止點與保留缺口)維護；可再固定
原 12／12 及 root 交換，重新核對原 rotations、actual supports、完整
ternary 與 degree-list 前提，本輪不登記它的來源排除。
Mixed12 整型、來源實現、ε≥3、一般出口與 K∞=K≤5 均未證。

> A₄ 原 mixed12 的共用 spokes04／04，含 root 交換，已在原來源前提下
> 全排。四 rotations 迫 C support={0}／{4}、U 實際含123；原互異色
> 三角与 exact degree-list／連通外部 K₄ 前提核對後，三-hub 引理延拓
> 整份 C，使固定原 ax 非 Σ-critical。01202 的 U singleton1／3 各接
> 完整 ternary／六角色 joint；不使用 A₃ 色表或 D₅ 固定-mask shortcut。
> A₃ 18／22 ledger 降為16／20，其餘完整物件不改；主重播：
> `PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed12_04_04.py --check`。
> 紙面＋固定 Python，未 Lean 化，mixed12 整型與 ε≥3 未證；未 commit／push。
