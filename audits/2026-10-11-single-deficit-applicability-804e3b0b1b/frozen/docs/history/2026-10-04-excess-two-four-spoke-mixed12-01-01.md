# 2026-10-04：A₃，mixed12 共用01／01四rotations與原ax非critical

使用者指定接續Kempe導覽§3，僅處理原spokes=01／01及root交換，
保持每份四disk rotations、C完整ternary、U actual supports／singleton
relation與完整六角色joint，不直接套mixed11 sealed triangle結論。
接手HEAD=`0e3812712b68f57927df86f30a07bb8074e090f9`，工作根目錄
`/home/ray/developer/ai/math`；既有A、A₂、B、B₂、P₃與稽核等未提交
成果保持，本輪沒有commit／push。

## 成果與證據層

[A₃報告](../c5_excess_two_mixed_core_four_spoke_mixed12_01_01.md)在A的
固定完整Σ933／941、Σ edge-minimal induced-C₅ disk、連通有效H、ε=2、
相鄰兩個完整degree-5 roots、其他有效內點degree四、唯一mixed C
incidence=(1,2)、a側一原單接點unary U與原ab的前提下，排除
**原01／01整份來源，含root交換**。

每份固定七頂點骨架的144份rotation assignments恰有四份disk
rotations。C共同faces一直是0–a–b、1–a–b；U長face為
0–4–3–2–1–a，a=5對應indices0,3，a=6對應1,2。
原C三條contact edges與完整degree的握手式排除empty support，
因此C實際支援正是某個固定{h}，h=0或1；完整來源碰齊五框點迫
同一原U實際碰齊2,3,4。

任一合法C外染色的原a,b,h形成互異色三角。反設C不能延拓，
degree-list tightness迫Gallai；展開K₄的四個原外方向，到連通原
三角的互斥路徑給K₅。K₄-free後用一般三-hub Gallai引理再給K₅，
因此C必有完整原ternary witness，包含x独立或x=y₀／y₁的情形。
只替換整份C、固定其他原頂點，得到
π_(a,b,u)J_G=π_(a,b,u)J_(G−ax)，使**固定原ax非critical**。
這裡沒有宣稱完整六角色joints相等，也沒有借用mixed11省略或
sealed triangle結論。原C大小、blocks、bridges、旁支與actual
attachments不受有限控制圖限制。

指定共同拒絕列01202亦給独立的完整joint矛盾：原R_U={d}，
d=2或3時取(a,b,u)=(5−d,d,d)，上述完整C延拓接出原joint tuple。
保留兩種singleton，不把同一U的schedules逐列自由改選。

本輪即時讀取[Dvořák原講義](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，
核對Lemma 7／Theorem 10的connected degree assignment、tightness、
Gallai tree與blockwise uniform前提。無界K₄／hub論證由紙面承擔；
Python只核對具名有限資料，未新增Lean theorem或形式化上述拓撲。

## Ledger、witnesses與負控制

[A₃ checker](../../scripts/c5_excess_two_mixed_core_four_spoke_mixed12_01_01.py)
唯讀A₂原artifact，逐項重建四份選定具名框架；完整四rotations、
原omission identities、所有實際U支援及完整singleton schedules保留。
Root交換核對原邊、rotations的具名bijection、原faces、同rotation的
C／U相容性、ownership及字面relation，boundary與色框固定。

| 同一必要域，含root交換 | 933 | 941 |
| --- | ---: | ---: |
| A₂原具名殘留 | 20 | 24 |
| A₃選定並排除01／01 | 2 | 2 |
| 選定原U face／support records | 8 | 16 |
| 選定完整singleton schedules | 12 | 22 |
| 完整來源支援限制後的U records | 4 | 8 |
| 完整來源支援限制後的schedules | 6 | 10 |
| 本入口來源殘留 | 0 | 0 |
| 保存其餘完整框架 | 18 | 22 |
| 保存其餘實際U支援 | 44 | 70 |
| 保存其餘完整singleton schedules | 56 | 102 |

941每份原root方向是8份支援、11份schedules；不把它寫成12份。
其餘具名物件全部原樣保存；前序完整witness入口及輸入SHA-256保持。
新[artifact](../../artifacts/c5_excess_two_mixed_core_four_spoke_mixed12_01_01/observations.json)
為80,967,491 bytes，SHA-256：
`a3f2ea31aea8cd2b9c008595f85430f0260612b431a8d1b3c03192d9171d70e2`。
大型payload留磁碟，由MANIFEST／產生器重播；沒有覆寫A／A₂ payload。

[新joint helper](../../scripts/c5_excess_two_four_spoke_mixed12_01_01_joint_controls.py)
有36張手建完整degree圖、18份root swaps；C實際支援0／1，三種
x身份各12張，U三份實際支援023／234／0234。這些控制只核對關係
語義，不代表每個source ledger schedule都有來源實現。

- 2,880次独立全圖joins、46,080份pinned fibres，包括38,112空纖維。
- 51,248份六角色tuple witnesses與2,400份五角色witnesses。
- 360份ax省略前後的(a,b,u)投影等式，5,712份只重染原C的整份
  coloring replacements，逐點保持原U、boundary與roots。
- 720份合法root-pair完整C fibres，36份01202的R_U={2}與
  (a,b,u)=(3,2,2)完整joint延拓。
- 1,440份原spoke接回、360份ax接回、360份G−au=T_N×R_U接回。
- 完整ternary與marginal假接合負控制分開；後者的root-spoke資格
  另列，不當作來源的合法root pair。
- 六角色不相等負控制：record6，01012，ax省略獨有tuple
  (2,3,2,2,0,1)，含整份合法witness；其(a,b,u)投影仍可重染C恢復。

36張控制圖完整Σ均為1023；不宣稱disk、Σ-critical或候選來源實現。
原C empty support無法製成同degree控制，因4|C|−3不是偶數；
沒有用缺少這種控制當作一般證明。

## 實際重播與工作區檢查

下列研究檢查通過，兩份A₃ main重播均唯讀逐byte比對：

```bash
python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed12_01_01.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed12_01_01.py --check
python3 scripts/c5_excess_two_four_spoke_mixed12_01_01_joint_controls.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_four_spoke_mixed12_01_01_joint_controls.py --check
python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed12_01_12.py --check
python3 scripts/c5_short_support_singleton.py --check
lake build
```

`lake build`成功（8,831 jobs，既有linter warnings保持）；不表示新
紙面論證已Lean化。未全面重跑A必要域的完整產生器、舊省略／容量／
T4／R系列或整份歷史checkers；沿用前序紙面與原artifact provenance。

新artifact已按指定路徑record；`python3 tools/artifacts.py status`
首輪回報`ok=142`，最終掃描回報`ok=143`（工作區另有同期產物加入）。
README、Kempe導覽、STATUS及前序報告頁首接上A₃；
HANDOFF仍為同一研究線的薄索引，無需更改線別或tag。
`python3 scripts/check_docs.py`最終通過：529份Markdown、5,477個
本地連結，anchors／直接索引／HANDOFF合約均合格。
`python3 tools/docgraph check`通過：62 documents、213 relations、
5 families，0 errors／notes。`git diff --check`通過，另核對四份新
A₃檔案的尾端空白及最後換行，全部合格。

第一次全工作區文件檢查時，另一條正在寫入的P₃ two-frame報告
尚缺其history，出現四個missing-path errors；該檔案由原工作完成後，
上列全工作區重播通過。本輪沒有代寫或改動那條研究的內容。

## 停止点與貼用摘要

停止於原01／01及root交換來源排除；其他具名入口未登記新排除。
目前窄入口由[Kempe導覽§3](../c5_kempe_guide.md#3-停止點與保留缺口)維護。
Mixed12整型、來源實現、ε≥3、一般出口與K∞=K≤5均未證。

> A₃已完成mixed12共用01／01，含root交換。四rotations中原C只在
> 0ab／1ab，actual support正是0或1；原互異色三hub延拓每份合法
> exterior，完整C重染使固定ax非Σ-critical。01202上U singleton
> 2／3均給完整六角色joint矛盾。四份框架全排，本入口0／0；其餘
> 18／22框架、44／70實際支援、56／102完整schedules原樣保存。
> 36完整degree controls保存360投影等式、5,712份C替換witnesses，
> 不主張六角色joints相等，不套mixed11。重播main --check，未commit／push。
