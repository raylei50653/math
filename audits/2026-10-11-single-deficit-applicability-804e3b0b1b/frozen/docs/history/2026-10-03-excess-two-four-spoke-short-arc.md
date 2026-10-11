# 2026-10-03：ε=2 四-spoke 共用短框弧的原拒絕列延拓

使用者在「繼續推進 ε ≥ 3」工作中再要求「繼續」。HEAD=`0e38127`，
cwd=`/home/ray/developer/ai/math`，沿用同輪已完成的
[原 crosscut](../c5_excess_two_mixed_core_four_spoke_crosscut.md)及既有
短／長face成果，處理941原02／03 indices155／175，不重開來源catalogue。
沒有commit／push，前序artifacts未覆寫。

## 原身份、完成範圍與證據

[報告](../c5_excess_two_mixed_core_four_spoke_short_arc.md)、
[checker](../../scripts/c5_excess_two_mixed_core_four_spoke_short_arc.py)、
[joint helper](../../scripts/c5_excess_two_four_spoke_short_arc_joint_controls.py)、
[artifact](../../artifacts/c5_excess_two_mixed_core_four_spoke_short_arc/observations.json)
保存固定Σ941／整圖D₅像、Σ edge-minimal induced-C₅ disk、ε=2，
相鄰雙完整degree-5 roots與其餘有效內點完整degree四。
原mixed incidence11、可共鄰的ordered(x,y)、各側一原unary與兩spokes，
全部actual attachments／supports、bridges、旁支、ownership、環序及同一色框保持。

Critical U／V迫它們位於兩個原外faces012／034；C位於原0ab三角或
短框弧23。不同C contacts時只為局部避色收縮ab，保留C degree四
及boundary-only R_C；共鄰時用共同禁色的list slack，兩者都給F_C=∅。
原q=01021：R_C對1↔3不變，F_C=∅迫A=2,D=1／3的完整C fibres非空；
R_U對2↔3不變可避A=2，固定任一原V witness色W後選D∈{1,3}∖{W}。
同一原joint給候選拒絕列的完整coloring，矛盾。

六份原941框架155,175,179,239,243,263全排。實際checker選擇
239的整圖move=[3,2,1,0,4]、不交換roles、Σ→949、原row6；
179 move=[2,3,4,0,1]、Σ→949、row4。其餘身份的Σ→941、row1。
完整原rows、frame、color permutations與root-role搬運均保存，
沒有假設所有D₅搬運都保持941或指定q拒絕。

Unequal從14／24到14／18，共用一框點從0／6到0／0，剩餘全不相交pairs。
此時整個mixed11+兩unary子型仍未完成；後續由
[不相交pairs報告](../c5_excess_two_mixed_core_four_spoke_disjoint_pairs.md)處理。
不宣稱C延拓全部不同rootpairs：sharedsingleton四外色及triangle
swappedseenpair拒絕控制保留；ab收縮不保持完整來源Σ。

固定relation域有1,023非空stable C relations，963份Fempty（含5份
sharedcontact對角型），1,926 guarded fibres；7份U palettes與15份V
palettes，共101,115字面六角色tuple witnesses。這些抽象relations
不提供原圖實現。12張完整degree圖、11variants共1,320獨立整圖
joins／21,120 pinned fibres含空集、1,080原邊接回、660root swaps，
12份q完整witness逐邊核對；沒有disk／candidate／critical圖實現宣稱。

## 實際重播與產物

生成及預設／seed17兩次逐byte重播通過；直接前序crosscut及短支援
已在同一續研turn重播通過。無新Lean檔，既有lake build通過8,831jobs；
全bundle最終文件、DocGraph、artifact與diff檢查見
[後續完成紀錄](2026-10-03-excess-two-four-spoke-disjoint-pairs.md)。

```bash
python3 scripts/c5_excess_two_mixed_core_four_spoke_short_arc.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_short_arc.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_crosscut.py --check
```

新artifact=18,675,547bytes，SHA256
`36ea360ac09ccc978d7168a65ccfb3a13229138ece2436b9f8aa2430d42c6df0`。
MANIFEST／.gitignore登錄producer、依賴與fingerprints，本地原bytes保持。
本輪未重跑degree-6、R系列、全倉來源catalogue或Lean axiom audit。
獨立紙面及checker審閱核對搬運、同框tuple與degree／slack邊界。

## 當輪貼用摘要

```text
HEAD=0e38127；cwd=/home/ray/developer/ai/math；沿用同輪原crosscut與短／長face成果。
固定Σ941、edge-minimal induced-C5 disk、ε=2；四spoke22 mixed11+各側unary。
941共用框點六份155,175,179,239,243,263全排，含原02/03及root交換。
C短支援共同避色Fempty；q01021用原R_C的1↔3及U的2↔3，構造A2,D1/3同框joint。
不同contacts只為局部避色收縮ab；sharedcontact直接slack，沒有Σ保持宣稱。
Unequal14/24→14/18，剩全不相交pairs；C所有異色rootpair延拓未證。
963完整C schemas、101115六角色tuple witnesses、1320整圖joins/21120fibres。
checker：python3 scripts/c5_excess_two_mixed_core_four_spoke_short_arc.py --check。
本輪未commit/push；紙面+固定Python，ε≥3及一般出口仍未證。
下一及目前完成範圍見disjoint-pairs報告和Kempe導覽。
```
