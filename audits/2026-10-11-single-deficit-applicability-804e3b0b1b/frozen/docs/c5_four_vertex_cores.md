# 四內點最小阻礙：單缺失分類與無界 odd-path 家族

文件整理（2026-09-23）：四內點分類與無界家族仍保留；[odd-join](c5_odd_join_cores.md) 已處理指定 quotient 家族，不能改猜所有 minimal cores 大小有界。
系列依賴與證據界線見 [全 degree-4／block 導讀](c5_degree4_guide.md)，研究優先序見
[HANDOFF](HANDOFF.md)。下文舊停止點與驗證紀錄保留當輪語境；本次未重跑研究 checker。

2026-09-17。接續 [list-critical core 路線](c5_weak_list_cores.md)。
本輪完整處理恰好四個有效內點的 minimal singleton obstructions；
符合 disk 與全部 T4 條件者，仍全部只拒絕指定 singleton。
另給出具有任意多有效內點的單缺失 minimal obstruction 家族。
前者是紙面必要條件加有限計算，後者是局部替換的紙面歸納；均未進 Lean。
候選 A 的一般單側及共同出口仍未證。

後續：[整個 odd-join 家族的單缺失分離](c5_odd_join_cores.md) 已處理 §5 提出的
任意奇環長度問題；以有限 minor 排除與路徑著色把兩種 lifts 縮回四內點。
一般 minimal quotient 與共同出口仍未處理，以下保留本輪結果。

## 1. 四內點的完整搜尋範圍

固定三色 pattern p，D 為未使用的第四色。沿用上一報告的紙面化約：
沒有 boundary chords；有效內點圖 H 連通；每個內點的 boundary 鄰居在 p 下
顏色互異；總 degree 至少 4。因此 lists 都含 D，且 `1≤|L(v)|≤deg_H(v)`。

四點的 64 個具名內部 edge masks 中，38 個連通。逐一遍歷 24 個內點置換，
得到全部六個形狀：star、P4、paw、C4、diamond、K4。
對每個形狀列出所有包含 D 且大小不超過 interior degree 的 lists，要求：

1. 原圖不可 list-color。
2. 刪任一 internal edge 後可 list-color。
3. 將任一個被禁止的 boundary 色加入任一 list 後可 list-color。

第 3 項正是刪一條 spoke；因 boundary 鄰居的 p 色互異，沒有重複 spoke-color。
這三項等價於此模板的逐非外圈邊 minimality，再由單調性得到 inclusion-minimality。
位元集合計算與獨立完整 assignment 回溯核對所有留下的 abstract lists。
剩下 18 個 list assignments，只有三種形式（A、B、C 是 p 使用的三色）：

| 內部形狀 | lists 的形式 | 總 degree | assignments |
| --- | --- | --- | --- |
| P4，依路徑順序 | `{D}, {D,A}, {D,A}, {D}` | 全 4 | 3 |
| diamond，u/v 為 degree-3 點，x/y 不相鄰 | `L(u)={D}, L(v)={D,A,B}, L(x)={D,A}, L(y)={D,B}` | u 為 6，其他 4 | 12 |
| K4 | 四個 lists 都等於 `{D,A,B}` | 全 4 | 3 |

例如 P4 兩端強迫 D，兩個中點都被迫 A 而相鄰；diamond 則依序迫使
u=D、x=A、y=B，使 v 無色可用。star、paw、C4 沒有符合 minimality 的 lists。
形狀與 lists 的窮盡由 checker 完成，不把上述表格稱為純紙面完整分類。

## 2. 同面與 T4 篩選結果

每一個被禁止的顏色，在實際 C5 上選恰好一個同色頂點作鄰居。
對五個 p 全部展開，有 4,965 個模板；已商內部形狀，但未再商其 automorphisms，
所以以下是模板數，不是不同 boundary-fixed graphs 的個數。

| 形狀 | 全部模板 | boundary-apex planar | 並且接受全部 T4 |
| --- | ---: | ---: | ---: |
| P4 | 1,920 | 40 | 20 |
| diamond | 2,880 | 160 | 80 |
| K4 | 165 | 0 | 0 |
| 合計 | 4,965 | 200 | 100 |

對 200 個 disk templates 逐圖核對完整 240-row relation，並對每條非外圈邊的
刪除再次核對完整 relation 與 p 可延拓性。100 個 disk/T4 templates 全部滿足
`Σ=Ω\{p}`。證書保存六形狀覆蓋、18 組 lists、全部 enumeration digest、
200 個 disk templates 的邊集、完整 relation 及 apex rotation。

K4 的 disk 排除也有短紙面證明：每個內點都有一條 boundary spoke。
加 boundary apex 後，把 apex 與 boundary 收縮成一點，就得到連到內部 K4
所有頂點的第五點，含 K5 minor。因此原圖不可能有 C5 同面 drawing。

**條件式推論。** 合併至多三內點結果，任意大小的候選 A 來源 G，只要存在
至多四有效內點的 minimal q-obstruction，就有只釋放 p 的出口。
故單側出口失敗要求該側每個 minimal obstruction 至少有五個有效內點。
此推論有 Python／NetworkX／apex-disk 紙面等價的外部信任依賴，沒有新增 Lean theorem。

## 3. 兩種 disk 核心其實共享同一個 obstruction

把 boundary 的三個 p 色類分別識別成三個頂點，C5 變成一個 triangle。
對所有 100 個 disk/T4 templates，所得簡單圖都是 `K2 ∨ C5`：
兩個相鄰 universal vertices，外加五環，每個 universal vertex 連到五環全部頂點。
checker 保存兩個 universal vertices 與五環的具體 edges。

這直接解釋不可四色：K2 占兩色，五環只能用剩下兩色，矛盾。
對 P4，兩個 universal vertices 都是 boundary 色類；對 diamond，
一個是 boundary 色類，另一個是 singleton-list 的內點 u。

**識別同色 boundary 點不是 planar minor operation 的聲明。**
原圖是 disk planar，而色類識別後的圖可非平面；不能因此推翻原 drawing。
這裡用的是固定 p 的著色等價，不是平面性的保存。

## 4. 無界的最小單缺失阻礙家族

四內點 P4 模板中有以下具體 disk core，boundary 為 0,…,4，
缺失 pattern 是 singleton-4：`p=(0,1,0,1,2)`。
非外圈 edges 為

```
07, 15, 16, 17, 28, 38, 45, 46, 47, 48, 56, 58, 67.
```

內部路徑是 `7–6–5–8`。邊 56 兩側的 faces 是 156、456；
5、6 都連到 boundary 頂點 1、4，而 p(1)≠p(4)。
以下替換可反覆使用。

### 局部替換引理（紙面）

假設 G 是 minimal p-obstruction，Σ(G)=Ω\{p}。內部邊 uv 兩側 faces
為 auv、buv，其中 a,b 是 p 顏色不同的 boundary 頂點。
刪 uv，加入新內點 s,t、路徑 `u–s–t–v`，並把 s,t 都連到 a,b。

則新圖仍是 disk minimal p-obstruction，relation 不變。

- **Drawing：** 在兩個三角形組成的 quadrilateral 內替換，外部 drawing 不變。
  新中央邊 st 仍有兩側三角形 ast、bst，故可以繼續替換。
- **已有 patterns 仍延拓：** 原 proper coloring 中 u≠v，令 s 用 v 的色、t 用 u
  的色，就能延拓到新圖。
- **p 仍被拒絕：** a,b 的兩個不同顏色，使 u,s,t,v 都只能用另外兩色。
  三條邊的奇路徑迫使 u≠v，若新圖能延拓 p，限制回原圖便矛盾。
- **舊邊 e≠uv 的 minimality：** G−e 有 p coloring，且保留 uv，所以 u≠v。
  s,t 可從 a,b 以外的兩色選相異值，使整條路徑 proper。
  即使 e 是 u 或 v 的 spoke、端點因此使用 a/b 的色，仍可以選擇這兩色的排列；
  兩種排列同時失敗只可能是 u=v 且同屬該兩色，這裡不會發生。
- **新邊的 minimality：** G−uv 的任何 p coloring 必有 u=v=c，否則已延拓 G。
  若刪一條新路徑邊，用剩餘兩色分別著色斷開的路徑即可。
  若刪 s–a，令 s 用 p(a)、t 用剩餘兩色中不同於 c 的色；其他新 spokes 對稱。

所以每條非外圈邊仍 critical。從四內點模板反覆替換，得到每個偶數
`k=4,6,8,…` 的 disk minimal p-obstruction，且永遠只拒絕 singleton-4。
同色 boundary 識別後是 `K2 ∨ C_(k+1)`，同一個 odd-cycle 機制。

checker 核對局部 patch 的全部 256 組端點／hub 色配置，以及 k=6 的完整 relation、
19 個單邊刪除的完整 relation、apex planarity 和可再替換的兩個 faces。
任意 k 的結論依賴上述紙面歸納，不是跑過所有 k。

**含義：** 一般 T4 disk minimal singleton obstruction 沒有固定的有效內點上限。
不能僅靠把小模板上限一直提高來完成一般論證。
這些圖只有一個缺失 pattern，不是候選 A 反例；也沒有否定「候選 A 來源另有小阻礙」
這種更特殊、仍待證的可能性。

## 5. 下一步與信任範圍

比繼續做 k=5 全圖枚舉更值得先問：**對任意 `K2 ∨ C_(2m+1)` 型的
boundary-color quotient，disk drawing 加全部 T4 可延拓，是否迫使對應
minimal obstruction 只缺一個 singleton？** 這會一次涵蓋一個無界家族。
注意本輪只證出一條可延長的子家族；不是所有這類 quotient 的 disk realizations
都已分類，也沒有證明所有 minimal obstructions 都屬於此族。

若此族的分離性成立，再尋找不屬於此族的 minimal core，或研究它們的組合。
一般三出口中，共同 pivotal edge 仍是獨立缺口。

產物：[checker](../scripts/c5_four_vertex_cores.py)、
[證書](../artifacts/c5_four_vertex_cores/observations.json)。

```bash
uv run --with networkx==3.5 python scripts/c5_four_vertex_cores.py --check
uv run --with networkx==3.5 python scripts/c5_weak_list_cores.py --check
lake build
git diff --check
```

本輪未跑 k=4／k=5 全圖枚舉，未重播全量 deletion audit，未新增 Lean theorem。
小核心分類用到紙面 degree/list 化約與 Python 搜尋；disk 合法性用 NetworkX
及已記錄的 apex/disk 等價；無界構造是紙面引理加兩個規模的計算核對。

驗證通過：新 checker 與 list-core checker 逐 byte 重播、`lake build`
（8,820 jobs，僅既有 lint）、四份入口／報告的 142 個本地 file link targets、
`git diff --check`。本輪及上一輪的 scripts、證書、報告與入口文件一併納入發布提交。
