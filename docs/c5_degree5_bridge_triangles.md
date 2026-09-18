# 互斥雙 triangles：bridge 切口與直接私有接點

發布整理（2026-09-18）：本報告隨 R16–R20 一併提交。下文的「未提交／HEAD／
下一題」保留各輪當時狀態；最新停止點見 [HANDOFF](HANDOFF.md)，
本次提交核對見 [STATUS §22](STATUS.md#22-r16r20-提交整理與核對)。


後續 R17：[不同環點接入的任意外臂](c5_degree5_bridge_arms.md) 已完成任意臂長
排除；只剩至少一側在該環 bridge 端點接入的位置分支。下文保留 R16 原停止點。

2026-09-18。從乾淨 HEAD `b55abf4` 接手 R15，開始 R16。
本輪完成兩項推進，**尚未排除所有互斥雙 triangle 二接點分量**：

1. 若某條兩環間的 bridge 將兩個 z 接點留在同側，另一側可消去，
   化回既有單 triangle／樹正常形，故不可能是目標 disk obstruction。
2. 若兩個 z 接點分別直接位於兩個 triangles，且各自不同於該環的
   bridge 路徑端點，則任意長連接路徑及不含接點外枝皆可排除。
   必要正常形有 132 型、43,696 個實際接線，全部非 disk。

成果為紙面化約與 Python 證書；沒有新增 Lean theorem。一般帶臂及環上
共同接點位置仍未完成，不宣稱完整 Σ 或一般 degree-5 單缺失結論。

## 1. 前提與 bridge 切口

沿用 [區域](c5_degree5_sectors.md) 及 [完整介面](c5_degree5_interfaces.md)：
q=(A,B,A,B,C)、D=3、U={0,1,2,3}，z 的 boundary 鄰居是 b0,b1,b4。
C=H−z 連通，只有兩個互斥 triangle blocks，其餘為 bridges；兩個不同
z 接點為 s,t。其他內點完整 degree=4，C 全部位於 arc b1,b2,b3,b4 側。
目標要求 F_C(q)={D}，包括三個刪 z-spoke 的測試。

對 bridge xy，刪除後 C 分成 X,Y。固定**同一** z=a，令 M_X(a)、M_Y(a)
為各自端點 x,y 的完整可取色集，保留各側的 z 接點限制。精確式是

```
a 可延拓 iff 存在 c∈M_X(a), d∈M_Y(a), c≠d。
```

若兩集合非空，拒絕 iff 它們是同一 singleton。一般式仍須保留空集合
情形；目標 degree 前提下，刪 bridge 的 slack 引理保證兩側都非空。
不能先對 a 取聯集再接合，亦不能把 D 下的 singleton 當成常數訊息。

若兩個接點都在 X，Y 不碰 z，M_Y 與 a 無關。minimality 在 D 下給出
M_X(D)=M_Y={c}。因此 Y 對 X 的限制恰是禁 c，可用
[單 triangle §2](c5_degree5_triangle_components.md#2-不含保留接點的單-bridge-外枝可消去)
的 boundary 固定 minor 消去：c≠D 留來源實際同色 spoke；c=D 留三色
spokes 的 D 葉點。此引理不要求 Y 是樹。

若 xy 在兩環連接路徑上，Y 含至少一個 triangle，替換後至多剩一個。
degrees、所有 z 色及 F={D} 保持，可接舊單 triangle／樹的 arc 正常形
排除。中間 minor 不必接受全部 T4；使用的是舊報告在該 arc、F={D}
下的非 disk 正常形證書，T4 只用於最初區域定位。
故尚可能的來源必使**每條兩環間 bridge 都分隔 s,t**。

## 2. 本輪完成的直接私有接點子型

令兩環為 (r,s,u)、(v,t,w)，連接路徑從 r 到 v；s,t 直接鄰接 z，
s≠r、t≠v。所有不含接點外枝先用上節引理消去。允許路徑任意長，
外枝任意分叉；消去後的非 D 禁色仍保留實際同色 boundary 接點，
D 禁色仍由 D 葉點實現。

固定 z=D。u,w 的 lists 各有二色，s,t 移除 D 後亦有二色，r,v 原有
三色 list，路徑內點為二色 list。triangle 的兩個私有點若不是同一
二色 palette，便對 root 無限制，root 保留三色；若同為 S，就禁止
root 使用 S。這是 [共用點雙環 §2](c5_degree5_shared_triangles.md#2-必須先在同一-root-色下接合)
的局部公式。

將兩個 triangle 私有點消去後得到路徑，各端可取色集至少一色。若任一
端有至少兩色，路徑有 slack，從另一端向該端貪婪著色即可。因此拒絕 D
迫使兩端都是 singletons。存在二色 S,T⊆{A,B,C} 及 bridge 色序列
c₀,…,cₘ₋₁，使

```
L(s)=S∪{D}, L(u)=S, L(r)=S∪{c₀}, c₀∉S；
L(t)=T∪{D}, L(w)=T, L(v)=T∪{cₘ₋₁}, cₘ₋₁∉T。
```

其中 m 是 bridge 邊數，m≥1。每個路徑內點 vᵢ 的 list 必為
{cᵢ₋₁,cᵢ}，相鄰色不同。理由是從左 singleton 向右傳遞：任何一步若
變成兩色，後續每個二色 list 都完整可取，最後不會拒絕右 singleton。
所以每步必被迫，最終色與右端 singleton 相同。這也直接涵蓋 m=1。

## 3. 四色語意與任意長 bridge 縮減

單側 triangle 對 root 的完整訊息是

```
M(a)={c}       若 a=D；
M(a)=S∪{c}    若 a≠D。
```

可直接按 root 色驗證：a=D 時兩私有點只能用 S 的兩色；a≠D 時，
給其中的 z 接點使用 D 或 S 中另一色，即可讓 root 使用三色 list 的
任一色。此式的前提包含 D∉S、c∉S，c 可以等於 D。

因此 D 沿 bridge 色序列被拒絕；其他 a 的端點均有三色，路徑 slack
保證可延拓。**所有合法序列的完整 F 都是 {D}**，不僅拒絕 D。

若 cᵢ=cⱼ，i<j，刪掉序列位置 i,…,j−1，保留 cⱼ 作新的第 i 色。
圖上刪掉路徑點 vᵢ₊₁,…,vⱼ 的 attachments，將這些點收縮進 vᵢ。
兩個 triangles 全部保留，最右端 vₘ 不會被收縮掉；若 i=0，收進 r。
保留點的 lists／attachments 不變，新出口色等於舊出口色，各完整 degree
恢復 4，z 仍為 5。boundary 點各自保持 singleton branch set。

每步都是真正 minor；由前述訊息式重新得到四種 z 色的延拓性及 F={D}，
再用既有分量解除引理得到 minimality。沒有聲稱全部二元 root relation
或任意 boundary row 都保持。反覆縮減得到互異色序列，故 **m≤4**。
這裡不能直接斷言 m=1；兩端必須保留的 bridge 色可能不同。

## 4. 有限證書及反向控制

枚舉 S,T⊆{A,B,C} 的二色 pairs，以及長度 1 至 4 的互異色序列，
要求首色不在 S、末色不在 T。共 **132 個必要模板**。
在指定 arc，A spoke 只能接 b2、B 可接 b1 或 b3、C 只能接 b4；
每個同色接點及 D 葉點的三色 spokes 都獨立選取。

- **43,696 個實際接線全部非 disk**：保存 29 個 K5／K3,3 subdivisions，
  對 boundary-apex augmentation 逐張驗證；重播不呼叫 planarity。
- 每個模板代表保存四個 z 色查詢及全部非 boundary 刪邊 coloring；
  其他接線逐張核對 degrees、內部邊與 boundary 鄰居色多重集，
  fixed-q 及刪邊問題依 attachment role 搬運。
- **18 張長來源**：九組有序 palettes 各插入端點／內部閉段，核對
  來源及目標 criticality、boundary 固定 minor，以及合成回來源的非平面 minor。
- 局部代數：全部 **256 組**端點色集接合（含空集合），及 **24 個**
  triangle root 查詢。使用完整 color tuples 交叉核對公式。
- 反向控制 S=T={A,B}、直接 bridge 色 C：每側訊息在 z=A,B,C 時
  為 {A,B,C}，在 z=D 時為 {C}。正確 F={D}；若先對 z 色取聯集，
  就會漏掉 D。這是本子型的條件訊息控制，沒有宣稱是 disk 反例。

無界覆蓋由 §1–3 的紙面論證承擔；有限控制不窮盡任意接點位置。
新證書保存程式與依賴 hashes、有序接線指紋及 networkx 版本。

## 5. 重播與精確停止點

[checker](../scripts/c5_degree5_bridge_triangles.py)、
[certificate](../artifacts/c5_degree5_bridge_triangles/observations.json)。

```bash
uv run --with networkx==3.5 python scripts/c5_degree5_bridge_triangles.py --check
uv run --with networkx==3.5 python scripts/c5_degree5_odd_cycle_components.py --check
lake build
git diff --check
```

**下一步：每條連接 bridge 都分隔 s,t，但接點經外臂到環，或與該環的
bridge 端點相同。** 先處理兩側均在不同環點接入的外臂，推導同一 z=a
下的 triangle root 訊息；再判定臂的簡單色序列縮短是否保持全部 F={D}。
同一環點接入時，該點的 degree 預算與上節三色 root 不同，不能套用本輪公式。

本輪未完成所有互斥雙 triangle 分量；兩環含長環、更多環、其他接點分拆、
一般 degree≥5、單側／共同出口與 `K∞=K≤5` 仍開放。未 commit／push。
