# 三-spoke 的單 triangle 二接點分量排除

發布整理（2026-09-18）：本報告隨 R11–R15 五輪成果一併提交。下文的
「未提交／HEAD／下一題」保留各輪當時狀態；最新停止點見
[HANDOFF](HANDOFF.md)，發布前核對見 [STATUS §16](STATUS.md)。

後續（2026-09-18）：[單長奇環報告](c5_degree5_odd_cycle_components.md) 已完成
保留接點的 cycle-to-triangle minor，排除任意單 odd-cycle 加 bridges。
下一題為恰兩個 triangle blocks；以下保留本輪原始成果與停止點。

2026-09-18。從 HEAD `be97121` 及前兩輪未提交成果接手。
接續 [任意樹分量排除](c5_degree5_tree_components.md)，完成交接指定的窄問題：

**唯一 degree-5 點 z 有三條 boundary spokes，H−z 是恰含一個 triangle
block、其餘為 bridges 的連通二接點分量時，不存在接受全部 T4 的 C5 disk
minimal q-obstruction。** 不限制兩接點位置、bridge 長度或外掛樹分叉。

這是紙面化約及 Python 有限拓撲證書，未新增 Lean theorem。
本輪沒有證一般含 cycle 的分拆 (2)、其他 degree-5 分拆或 `K∞=K≤5`。
來源圖可任意大；89,224 個接線是化約後的必要模板，並非擴大內點 catalog。

## 1. 接手狀態與三種連接位置

前輪 checker 已重播，HEAD 仍為 `be97121`，區域／樹成果原封保留。
沿用 [區域報告](c5_degree5_sectors.md) 固定

```
q=(A,B,A,B,C), D=3, N_B(z)={b0,b1,b4}, F_C(q)={D}.
```

C 全部位於 arc (b1,b2,b3,b4) 一側；鏡像由前報告處理。
本報告 C 表示分量，色集一律用 U={0,1,2,3} 及 palette 符號。
令 J 為唯一 triangle，s,t 為 z 的兩個不同接點。
刪掉 J 的三條邊後，每個剩餘樹分量恰包含 J 的一個頂點。

- s,t 位於不同樹分量：保留它們到 J 的兩條互斥路徑，得到**不同 triangle
  接點**，記為 u,v；第三個 triangle 點記為 w。
- s,t 位於同一樹分量，且唯一 s–t 路徑經過該 triangle 頂點 r：保留兩條
  到 r 的路徑，得到**共同 triangle 接點**。
- s,t 位於同一樹分量，但 s–t 路徑不碰 J：含 J 的整個旁支只經一條 bridge
  接到該路徑，為**旁支 triangle**。

路徑可以零長，即 s 或 t 本身就是 triangle 頂點。這三型覆蓋全部位置，
不能只研究兩個 z 接點直接落在不同 triangle 點的情形。

## 2. 不含保留接點的單 bridge 外枝可消去

保留 §1 的路徑及所需 triangle；每個其餘分枝只經一條 bridge 與保留部分
相接，而且不含 z 接點。固定 q、z=D，刪該 bridge 後兩側可著色；原圖
不可著色，故 bridge 兩端的可取色集必為同一 singleton {c}。
外枝不碰 z，因此對全部四種 z 色，其限制都恰為「保留端點不能取 c」。

此論證只用連通性及單 bridge 接合，**不要求外枝是樹**。若 c≠D，外枝
必碰某個 c 色 boundary 頂點，否則交換 c、D 會破壞 singleton 強迫。
將外枝併入保留端點，只留一條實際 c 色 spoke。若 c=D，外枝必碰全部
三個 q 色；將外枝收縮成一個 D 葉點，保留每種 q 色各一條實際 spoke。
所有 boundary 頂點都是 singleton branch sets。

同一保留點的外接禁色必互異；若重複，刪一條相應 bridge／spoke 後原限制
仍存在，與 minimality 矛盾。因而替換保持完整 degree=4、固定 q 的全部
四個 z 色查詢及 F_C(q)={D}。由完整介面的充要條件，仍為 minimal q。
只要求 fixed-q 語意，不聲稱完整 Σ、T4 或其他 rows 保持。

旁支 triangle 可整個作上述外枝處理，所得 C 為樹，再接既有任意樹排除。
checker 保存五個原始含 triangle 的旁支控制，核對完整 root singleton、
真正的 boundary 固定 minor，並將舊模板的非平面 minor 合成回各來源。

## 3. 路徑訊息及指定 singleton 的唯一反向輸入

正常形中，一條 z 到 triangle 的路徑，除 triangle 端點外依序有 k 個
內點，每點 residual list 是二色 pair R_i；k 可以為零。
固定 z=a，令 M_0={a}，傳遞

```
M_i={c∈R_i : 存在 d∈M_(i−1), c≠d}.
```

若某一步有兩色，此後每步都等於該點完整的二色 list。故末端 singleton
恰在每步都被迫時出現，可以記成色序列

```
a=c_0,c_1,…,c_k,   R_i={c_(i−1),c_i}, c_(i−1)≠c_i.
```

**指定末端 singleton {c_k} 時，輸入 a 至多一個。** 從末端向後，每一步
都只能取 R_i 中另一色，唯一決定前一色；k=0 時也是 a=c_k。
若末端 M 有至少兩色，triangle 端點可避開任意指定色，不受該路徑限制。

checker 對 k=0,…,4 的全部 1,555 組 pairs，以完整 color tuples 與集合傳遞
交叉核對，另檢查 singleton 反向唯一性。任意長度由上述歸納承擔。
這是在同一 q／a 下的精確分離；triangle 的三點仍共同接合。

## 4. 不同 triangle 接點：兩條簡單色序列

消去外枝後，u,v 各有三色 list，w 有二色 list S。u、v 各只有一個外接
禁色，w 有兩個；D 禁色用 §2 的 D 葉點實現。
固定 z=D 後，triangle 不可著色。三個 lists 都至少二色；triangle 的
不可著色情形恰是三個 lists 都為同一二色 S。因此兩條路徑必各送出
singleton c_u、c_v，且

```
c_u,c_v∈U\S,
L(u)=S∪{c_u}, L(v)=S∪{c_v}, L(w)=S.
```

這也可直接證明：若其中有三色 list，可先為另兩點選不同色，再為此點
選第三色；三個二色 lists 不全相同時亦可選出三個不同色。

要在其他 z=a 下仍拒絕，路徑必再送出相同的 c_u、c_v。§3 的反向唯一性
表明 a 必為 D。因此正常形的完整禁色集自動為 {D}，不會漏掉 z=A、B、C
的刪-spoke 條件。

兩條色序列都從 D 出發。若 c_i=c_j，刪去 i 至 j 的閉子序列，保留起點
D 及終點 c_u／c_v。重複此操作至各序列無重複色；若終點就是 D，可以
縮成零內點路徑。其餘每條最多三個內點。

刪掉被移除點的外接部分，再將連續路段併入其前一保留點；若是前綴則
併入 z。Triangle 三點保持分離，兩條路徑只共享 z，每次都是真正 minor。
保留點的 attachments 不變，degree 恢復為指定的 4／5。新序列仍從 D
送出同一 singleton，故上述論證重新給 F={D} 及 minimality。

S 有六種。若 D∈S，兩個末端各有兩種選擇，每個終點有五條簡單序列，
得到 3×10²=300 型。若 D∉S，末端為 D 時一種空序列、為另一色時五種，
得到 3×6²=108 型。合計 **408 個 palette 模板**。

## 5. 共同 triangle 接點：帶標記的閉色序列

共同接點 r 在保留骨架已滿 degree=4：兩條 triangle 邊及兩個朝 z 的方向。
其餘 triangle 兩點的 lists 在拒絕 D 時必為同一二色 S。整個 triangle
對 r 的精確限制是 **r∈T=U\S**：r∈S 時兩鄰點都只剩同一色，r∉S 時
可給兩鄰點 S 的兩個不同色。此限制與 z 色無關。

因此 z–s…r…t–z 的全部路徑內點都是二色 lists，r 的 list 為 T；完整
F_C(q) 等於這個二色路徑對兩端共同 z 色的禁集。既有樹報告的代數直接
給出：F={D} iff 對應色序列從 D 回到 D，且至少使用三色。r 是其中一個
**被標記的步驟**，它的外接限制由 triangle 共同實現。

沿用前報告刪閉子序列的規則：每次保留至少三色。

- 若標記 r 保留，其 triangle 兩點及 attachments 亦保留，得到較短共同接點型。
- 若 r 被刪除，同時刪掉 triangle 另外兩點及其外接部分；r 隨路徑收縮
  進 branch set。所得圖是普通樹正常形，直接接既有樹排除。

不能各自任意消去兩臂的全部重複色：那可能把 F={D} 變成雙禁色。
這裡使用完整閉序列的「仍至少三色」判準，避免該退化。

若 triangle 始終保留，最終必是前報告五種不可再刪的閉色序列，並標記
其中一個步驟：6×(3+4+4+4+5)=**120 個模板**。每步 minor 的 branch sets
與前報告相同，另保留或刪去 triangle 的兩個私有點；不新增邊或識別 boundary。

十個長控制逐步核對：四個最終保留 triangle，六個轉入樹模板，並各將
最後非平面 minor 合成回來源。無界覆蓋來自既有五型分類及上述標記處理。

## 6. 全部實際 boundary 接線排除

固定 arc 上，A 只能接 b2，B 可以接 b1 或 b3，C 只能接 b4。
每個非 D 外接禁色都獨立選其實際 boundary 頂點；D 葉點各選 A、B、C
spokes。不存在「同色／同 palette 必共用同一 boundary 頂點」的假設。

| 類別 | Palette 模板 | 全部接線 | Disk |
| --- | ---: | ---: | ---: |
| 不同 triangle 接點 | 408 | 81,992 | 0 |
| 共同 triangle 接點、五型帶標記 | 120 | 7,232 | 0 |
| 合計 | 528 | 89,224 | 0 |

每張圖的 boundary-apex augmentation 均含已保存的 K5 或 K3,3 subdivision，
共用 **143 份證書**。`--check` 逐張重建來源邊，檢查路徑、內部互斥及 branch
接線，不呼叫 planarity。全部接線／證書編號的有序 SHA256 一併核對。

每個 palette 模板取一個代表，直接核對四個 z 色及每條非 boundary 邊刪除
後的完整 q-coloring。其餘接線逐張核對 degree、內部邊及各內點的 boundary
鄰居色多重集；它們只在同 q 色的 b1／b3 之間改換實際接點，所以固定 q
的染色問題與逐邊刪除問題按 attachment role 一一對應。沒有聲稱完整 Σ
也相同；拓撲仍對所有實際接線分別驗證。

假想來源 disk 經 §2–5 的 boundary 固定 minors，必落入既有樹排除或本節
非 disk 模板，矛盾。T4 只用於最初的區域定位，中間 minors 不需保持 T4。

## 7. 重播與證據邊界

[checker](../scripts/c5_degree5_triangle_components.py)、
[certificate](../artifacts/c5_degree5_triangle_components/observations.json)。

另保存 24 個不同接點的長來源，48 次單臂縮減（包括縮成零長）、10 個共同
接點長來源及 20 次縮減、5 個旁支 triangle 原始控制。每步檢查 boundary
固定 branch sets、degree、完整 F 及 criticality，並保存來源圖上的非平面 minor。
程式、直接 import 及前輪樹證書皆保存 SHA256；重播結果逐 byte 比對。

```bash
uv run --with networkx==3.5 python scripts/c5_degree5_triangle_components.py --check
uv run --with networkx==3.5 python scripts/c5_degree5_tree_components.py --check
uv run --with networkx==3.5 python scripts/c5_degree5_sectors.py --check
lake build
git diff --check
```

實際驗證見 [STATUS §13](STATUS.md#13-三-spoke-單-triangle-二接點排除)。
無界位置／分枝／長度的覆蓋是紙面證明，有限 topology 證書仍包含 Python
checker 及 apex-disk 紙面等價的信任；沒有新增 Lean theorem，沒有重播舊
全量 catalogue／deletion audit，也沒有改動前兩輪 scripts／artifacts。

## 8. 新停止點

三-spoke 分拆 (2) 的 C 已不能是樹或「一個 triangle 加任意 bridges」。
連通外框仍排除 K4。剩餘為：**恰一個長 odd-cycle**，或至少兩個 odd-cycle blocks。

下一個窄問題選恰一個長 odd-cycle：先保留兩接點到 cycle 的路徑及實際
spokes，研究能否將 cycle 縮成 triangle，並分別核對共同／不同接點的全部
固定-q z 色。此時 cycle 的介面及 minor 必須重新驗證，不能直接套用全
degree-4 整圖的長環排除。尚未啟動多環或提高 k 的 catalog。

一般 degree-5 單缺失、一般 degree≥5、單側／共同出口、候選 A 與
`K∞=K≤5` 仍未證。本輪及前兩輪研究成果未 commit／push。
