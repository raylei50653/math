# ε=2 no-mixed：兩-root (4,4) core 的 U1 身份排除

**後續（2026-10-08，U4完成）。** [非相鄰兩mixed的U4](c5_excess_two_nonadjacent_two_mixed_core44.md)
現亦全排，固定完整Σ933／941下兩-root44身份全部完成。
下文保留本頁當輪停止點及後續紀錄；單-root例外、45／54／55與ε≥3仍保留。

**後續（2026-10-08，U3完成）。** [U3 mixed12／21](c5_excess_two_nonadjacent_mixed12_core44.md)
連同mixed11／22關閉U3兩-root44身份；目前完整Σ下的44殘留只剩U4。
下文保留各輪停止點，其他core型不受此更新排除。

**後續（2026-10-08）。** [U2相鄰兩mixed44](c5_excess_two_adjacent_two_mixed_core44.md)
已排除，完整Σ下44殘留現只剩非相鄰U3／U4。本頁保留U1當輪停止點及驗證。

2026-10-07。接續 [C44″ §5](../artifacts/c5_excess_two_c44pp/REPORT.md#5-最小未覆蓋子分支清單)
的 U1；同輪 [唯一 mixed 稽核](../audits/2026-10-07-c44pp-mixed-audit/REPORT.md)
另行交付。研究線與目前停止點見 [Kempe 導覽](c5_kempe_guide.md#3-停止點與保留缺口)。

**結論：完整 Σ=933／941 或其整圖 D₅ 像的 ε=2 相鄰 no-mixed 來源，
不存在保留兩個原 roots、兩者 core degree 都四的 minimal rejected-row core。**
C44″ 的 U1 兩份省略身份全排；U2–U4、單-root 刪除例外、(4,5)/(5,4)
及原 (5,5) core 保留。這不排除整個 no-mixed 來源，不證 ε≥3。

## 1. 前提與原省略身份

G 有限簡單，指定有序 induced C₅ B 是 disk 外框；完整 Σ(G) 是933／941
或其整圖 D₅ 像，每條非框邊 Σ-critical。有效內部 H 連通，完整 degree
恰兩個相鄰 degree-5 roots z,w，其他有效內點完整 degree 四，ε=2。
H−{z,w} 沒有 mixed，保留全部原附件、contacts、ownership及共同色框。

令 q∉Σ(G)，M⊆G 是包含 B、保留原 z,w 的 inclusion-minimal q-core，
且 deg_M(z)=deg_M(w)=4。M 繼承 disk、T4；degree-4 飽和給原 pieces
全取或全不取。原 zw 保留：刪去 zw 後兩側獨立，若仍拒絕 q，某一侧
就已拒絕，可再省掉另一側，違反 M 的 minimality。此處不假設 G−zw 全收。

依 [E6-D](../artifacts/c5_excess_two_e6/REPORT.md#4-e6-dno-mixed-的整側預算與精確殘留)，
恰有一份原 U_z、一份原 U_w，capacity k_r=4−t_r。
[C44″ U1](../artifacts/c5_excess_two_c44pp/REPORT.md#5-最小未覆蓋子分支清單)
將身份限制為：

| 身份 | 原 spokes | 保留於 M 的分量 |
| --- | --- | --- |
| 兩側各省略一條 spoke | (2,2)，或941的(2,3)含交換 | U_z、U_w均保留，capacity分別為4−t_z、4−t_w |
| 一側 spoke、另一側 unit-unary | (2,3)，含交換；三-spoke僅941／013型 | capacity-two U_z；整份U_w省略 |

兩 unit-unary 同省略會要求兩側各三 spokes，已由 E6-D 排除。

**必要限制更正。** C44″原先將双spoke省略縮為(2,2)，但其「結合E6-D的t_r≤2」
不適用941，因為E6-D在941容許t_r=3。三-spoke側若保留unit U再省略spoke，
core內度仍為2，內部最大度≤3不能排它。上表補保留這個身份；§3直接覆蓋
全部bridge-marker核心及雙spoke接回，不依該收窄。這不是聲稱新增身份有來源實例。
下文不再使用013的字面位置，只用原容量與完整relation。

## 2. (2,3)：leaf 強迫未用色與 triangle palette 衝突

交換 roots 可令 z 側省略 spoke、w 側省略整份 unit U_w。
M 中 z 的內部 degree 是3：zw 加 U_z 的兩個不同原 contacts x,y。
w 的內部 degree 是1：只有原 zw，另有三條原 spokes。

U_z 連通，x、y 之間的原路加 z 形成環；
[全 degree-4 分類](c5_k4_blocks.md#4-合成全-degree-4-的單缺失結論)
只容許 triangle，因此 xy 是原邊，zxy 是 triangle。
若 M 有第二個 triangle，[雙 triangle 分類](c5_two_triangle_blocks.md#1-範圍與結果)
迫只有六個 triangle 頂點、直接 bridge、沒有外掛樹，與 w 是 leaf 矛盾。
所以 M 的唯一 cycle 是 zxy，w 是它的單點外掛樹。

在 M 自己的 q-criticality 下，w 的三條 spokes 不可在 q 下重色，否則
刪一條重複禁色 spoke 仍拒絕 q。故它們見齊三個 q 色，w 的可用色只有
未用色 D。切開原 zw 後，w 側的完整 root relation 恰為{D}。
Bridge forcing 迫這份 branch 強迫 D。

[Triangle palette 引理](c5_triangle_branches.md#1-任意大小的單-triangle-核心接枝位置限制)
在任意大小單 triangle disk minimal q-obstruction 證共同剩餘 palette P 含D，
且每條外掛 tree bridge 的強迫色不在 P。因此此 bridge 的強迫色必≠D，矛盾。
這不把 G 視為 q-minimal，也不限制被省略 U_w 的大小或 relation。

## 3. 雙 spoke：全部344份bridge-marker核心的完整接回

此身份沒有省略任何原 piece，G恰是M加回兩條具名spokes。
原zw在M仍是bridge。將整個原來源一次D₅／S₄搬運至q=01012，
所有roots、spokes、附件與完整Σ同步搬動。

[既有344域的化約](c5_excess_two_mixed_omission.md#4-保留相鄰-roots-的任意長度覆蓋)
適用於任何全degree-4、帶原相鄰bridge markers的minimal q-core；
化約本身不要求外面還有一份mixed。本輪[指定稽核](../audits/2026-10-07-c44pp-mixed-audit/REPORT.md#14-省略-mixed11-的完整二維介面與344域)
亦已核對這個前提與標記run覆蓋。
因此任意大小M都有同框正常形M*，保留z,w為singleton且保留zw，
在全部十列保持完整root-pair relation；原兩條spokes的字面過濾也保持。
所以G與M*加同一兩spokes有相同完整Σ，不需聲稱縮減保持其他contact座標。

固定同一β，令K_β是M*的完整有序root-pair relation，精確接回為

\[
K_β(G)=\{(a,d)\in K_β(M^*):a\ne β(b_z),\ d\ne β(b_w)\}.
\]

每個pair仍來自同一份M*全圖染色；只加這兩條具名邊。
全部不存在於M*的spoke位置均展開，不先按原來源的spoke上界、disk或
Σ-criticality篩接回，放寬不漏來源：

| 核心家族 | 核心／bridge markers | 雙spoke接回 |
| --- | ---: | ---: |
| 單triangle、單run | 160 | 1,440 |
| 單triangle、雙run | 64 | 576 |
| 偶數path | 56 | 458 |
| 雙triangle、直接bridge | 64 | 1,024 |
| 合計 | 344 | 3,498 |

全部3,498份接回的完整Σ與兩個目標的D₅軌道無交集，故雙spoke身份全排。
這同時涵蓋941可能的三-spoke側，不將必要身份收窄錯誤當作排除前提。

### 3.1 原(2,2)子型的六點直接化約

兩原 U 都保留，每份各有兩個不同 root contacts。連通性及只容許triangle的分類
在 z 側、w 側各迫一個原 triangle；两份 U 互斥，所以兩 triangles 互斥。
雙 triangle 分類迫 M 恰有六個有效內點、由原 zw 直接 bridge 相連、無其他枝。
因此 U_z、U_w 各恰一條原 edge；M 沒有任意長度殘留。

此時 M 正是雙 triangle分類的64份具名 q-critical disk lifts 之一，完整Σ(M)=1022。
未先按 G 的 disk 或 Σ-criticality 過濾接回；放寬只增加待排除案例。

每個 bridge root 在 M 有一條 spoke，原 G 各加回恰一條不存在於 M 的
spoke，所以每份核心有4×4=16個具名接回。
64×16=1,024個接回完整十列Σ如下：

| Σ(G) | 接回數 |
| --- | ---: |
| 830 | 224 |
| 958 | 96 |
| 1016 | 224 |
| 1020 | 96 |
| 1022 | 384 |

933的D₅軌道是{933,934,940,948,996}，941的是{941,949,950,998,1004}。
上表無交集，故沒有符合原來源完整Σ的接回，(2,2)身份全排。
原字面 q 未正規化前的來源，由同一整圖搬運涵蓋。

## 4. 證書、重播與信任界線

[新 checker](../scripts/c5_excess_two_no_mixed_core44.py) 僅用標準函式庫；
讀 [既有344域](../artifacts/c5_excess_two_mixed_omission/observations.json) 的全部344份核心，
核對原bridge與完整degree；雙triangle另核對六點／兩互斥三環。
自行回溯原完整邊集，重算十列完整root-pair relation，再對每份原接回圖
獨立回溯，34,980次查詢與字面過濾一致。沒有 import 舊 producer 或 planarity oracle。

[新 artifact](../artifacts/c5_excess_two_no_mixed_core44/observations.json) 保存原核心邊、
具名roots／unary頂點、全部root pairs及全圖染色witnesses、兩條接回spokes、
逐列存活pair索引、完整Σ及來源hash；空關係以空索引保存。
Witness indices 指向同一份原 M 的全染色，確實滿足列出的原接回邊。
這是固定必要域證書，沒有聲稱得到完整Σ933／941的來源正控制。

```sh
python3 scripts/c5_excess_two_no_mixed_core44.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_no_mixed_core44.py --check
```

本輪產生新證書並執行上述兩次完整重播；實際文件驗證另見
[本輪紀錄](history/2026-10-07-no-mixed-core44.md)。沒有執行lake build或擴大k搜尋。
任意大小來源到上表的覆蓋由§1–3紙面化約提供，依賴既有 Gallai／degree-list
全四分類、E6-D、triangle palette及雙 triangle分類與它們原有的有限拓撲信任界線。
本輪没有重新稽核它們全部上游枚舉；triangle palette 的部分拒絕模板仍依賴
既有NetworkX planarity replay，不將其混称純紙面或Lean證明。

**精確停止點：U1的兩-root44身份全排。** no-mixed 的其他core型及單-root
省略例外保留；相鄰m=2、非相鄰N1 incidence11／12／21、N2五族仍未覆蓋。
完整Σ前提不能直接換成E3–E6的三列前提，E5要求的新證明亦未完成。
ε≥3、猜想E任意大小、一般出口與K∞=K≤5仍未證。
