# 三-spoke 的共用點雙 triangle 二接點分量

發布整理（2026-09-18）：本報告隨 R11–R15 五輪成果一併提交。下文的
「未提交／HEAD／下一題」保留各輪當時狀態；最新停止點見
[HANDOFF](HANDOFF.md)，發布前核對見 [STATUS §16](STATUS.md)。

2026-09-18。從 HEAD `be97121` 及前四輪未提交成果接手。
本輪選交接的「恰兩個 triangle blocks」，完成其中的**共用 cut vertex** 分支：

**唯一 degree-5 點 z 有三條 boundary spokes，H−z 是連通二接點分量，
其 blocks 恰含兩個共用 cut vertex 的 triangles、其餘為 bridges 時，
不存在接受全部 T4 的 C5 disk minimal q-obstruction。**

允許任意接點位置、bridge 長度與外枝分叉。成果為紙面化約及 Python
有限證書；沒有新增 Lean theorem，尚未處理兩個互斥 triangles 的連接路徑。
不將全 degree-4 整圖的舊共用點排除直接套到有 z 的二接點分量。

## 1. 接手與位置覆蓋

前輪 [單長奇環](c5_degree5_odd_cycle_components.md) 的 checker 重播通過。
沿用 [區域定位](c5_degree5_sectors.md) 與 [完整介面](c5_degree5_interfaces.md)：

```
q=(A,B,A,B,C), U={0,1,2,3}, D=3,
N_B(z)={b0,b1,b4}, F_C(q)={D}.
```

分量 C 僅接 arc (b1,b2,b3,b4)，鏡像由區域報告處理。
令兩環為 J₁=(r,u,v)、J₂=(r,x,y)，共同點 r 已有四條環邊，因此沒有
外枝、boundary spoke 或 z 邊。z 的兩接點 s,t 不可能是 r。

刪去六條環邊，其餘為樹，各樹至多碰 cluster 的一點。考察 s,t 到 cluster
的兩條路徑：

- 若它們在 cluster 外先相遇，兩環都在 s–t 路徑的一條不含接點的 bridge
  旁支中。按 [單 triangle §2](c5_degree5_triangle_components.md#2-不含保留接點的單-bridge-外枝可消去)
  消去整個旁支，得到已排除的樹分量。
- 若到達不同 cluster 點，兩條臂只共用 z。端點都為私有點，依 cluster
  對稱，只需端點在同一 triangle 或分處兩個 triangles。
- 若兩臂首次在 cluster 的同一私有點 p 會合，保留該點及完整兩環，得到
  帶標記路徑型。兩臂不能同時零長，因 s≠t。

其餘不含接點的 bridge 外枝按同一引理消去。非 D 禁色改成來源的實際
同色 spoke；D 禁色保留成帶三種 q 色 spokes 的 D 葉點。
每點禁色互異，否則違反 minimality。這些 boundary 固定 minors 保留
degrees、全部四個 z 色的查詢與 F_C(q)={D}，不需外枝本身是樹。

## 2. 必須先在同一 root 色下接合

一個 triangle 的 root 為 r，另兩點 lists A、B 都至少二色，則

```
E(A,B) = U\S，若 A=B=S 且 |S|=2；
E(A,B) = U，其他情形。
```

固定 r=c 後，另兩點不能選不同色，恰在 A\{c}、B\{c} 都是同一
singleton。這等價於 A=B={c,d}，故得到上述公式；三色／四色 lists 也涵蓋。

兩環共同點 r 沒有其他限制，故延拓的 r 色集是
`E(L(u),L(v)) ∩ E(L(x),L(y))`。交集為空 iff 兩側私有點的 lists
各為相同二色 palette S₁、S₂，而且 **S₂=U\S₁**。
這是共同色框下的精確接合，不是把各環的可著色布林值獨立相乘。

每條臂的非 cluster 點有二色 residual lists。固定 z=a 後，臂末端
訊息 M 非空；singleton {c} 禁止 cluster 端點用 c，非 singleton 則
不施加限制。兩臂共同固定 a 後才可分別求值。對不同端點，每點原為
三色 list，最多扣一色；對共同端點，原為四色，最多扣兩色。因此所有
私有點的有效 lists 始終至少二色，可對四種 a 使用上述公式。

## 3. 不同 cluster 端點：兩條臂各縮成簡單色序列

在 a=D 下，由 §2 存在互補的 S₁、S₂。未標記私有點的 lists 為其
所屬環的 Sᵢ；有一條臂的端點 p 則原有 `L(p)=Sᵢ∪{c_p}`，其中
c_p∉Sᵢ，且該臂在 D 下恰輸出 singleton {c_p}。

對任意 a，整個 cluster 拒絕 iff 兩條臂再次輸出原來的指定 singletons：

- 分處兩環時，每環還有一個未標記私有點，固定了該環必須使用的 Sᵢ。
- 同環不同點時，另一整環未標記，先固定其 palette，再由互補條件
  固定帶兩個接點的環 palette；不能任意改成另一個共同 pair。

指定臂末端 singleton 的輸入色至多一個，見
[單 triangle §3](c5_degree5_triangle_components.md#3-路徑訊息及指定-singleton-的唯一反向輸入)。
所以這裡完整 F 自動為 {D}。每臂用被迫色序列 D,…,c_p 表示，反覆
刪去重複色之間的閉段後，得到簡單序列。c_p=D 可縮成零長；否則最多
三個內點，每個固定非 D 終色有五條簡單序列。

刪除被移除點的 attachments，再將該路段收縮進前一保留點；前綴收進 z。
兩個 cluster 端點及兩環五點均不識別。保留點 attachments 不變，完整
degree 恢復 4／5，新序列仍輸出同一指定 singleton，因此四種 z 查詢、
F={D} 及 minimality 均保持。沒有宣稱臂的全部 root 訊息表逐項相同。

同環不同點有 408 個 palette 模板。分處兩環時，互補 palettes 恰有一個
含 D；兩端簡單序列選擇分別為 10 與 6，六種 S₁ 共 **360 個模板**。

## 4. 同一私有點會合：保留完整閉色序列

令會合點 p 在 J₁，另一私有點為 v。拒絕 D 迫使 v 的 list 為 S，J₂
兩私有點 lists 同為 T=U\S。J₂ 對共享點 r 的完整可取色集為 S。
因 r,v 相鄰且同在二色 S，它們必用 S 的不同色。因此，整個兩環 gadget
對 p 的完整 root 可取色集恰為 **T**，與 z 色無關。

所以 z 的兩臂連同標記點 p 是一條二色 list 路徑，p 的 list 是 T；其
兩個外接禁色由整個兩環 gadget 實現。既有樹報告的代數給出：F={D}
iff 被迫色序列從 D 回到 D，且使用至少三色。

依 [樹報告 §5](c5_degree5_tree_components.md#5-任意色序列縮到五型)，只刪除
刪後仍至少三色的閉段：

- p 保留時，同時保留兩環另四點與 attachments。
- p 被刪時，刪掉兩環另四點及其 attachments，p 隨主路徑收縮。結果
  是普通樹正常形，接既有樹排除。

每次是真正 minor，且重新由至少三色判準得到全部 F={D}，故不漏掉
刪 z-spoke 的條件。若標記始終保留，五個不可再刪的 motif 每一步都可
標記，得到 `6×(3+4+4+4+5)=120` 個模板。

不能各自將兩臂任意縮短：只用 D、A 的閉序列拒絕 {D,A}，即使 D
仍被拒絕，也已不滿足 minimality。checker 保存此具體負控制。

## 5. 實際接線與有限拓撲證書

在指定 arc，A 的 spoke 只能接 b2，B 可以接 b1 或 b3，C 只能接 b4。
每個同色接點獨立選擇；每個 D 葉點也獨立選三種 q 色的實際 spokes。

| 類型 | Palette 模板 | 全部實際接線 | Disk |
| --- | ---: | ---: | ---: |
| 同一 triangle 的不同私有點 | 408 | 158,496 | 0 |
| 分處兩個 triangles | 360 | 126,096 | 0 |
| 同一私有點會合，五型帶標記 | 120 | 11,328 | 0 |
| 合計 | 888 | 295,920 | 0 |

這是紙面化約後的必要模板，沒有提高 k 或重跑 graph catalog。
每個模板代表直接核對四個 z 色與每條非 boundary 邊刪除後的完整
q-coloring；其餘接線逐張核對 degrees、內部邊及各內點的 boundary 色
多重集。fixed-q 染色及逐邊刪除問題依 attachment role 對應搬運。
其他 boundary rows 的關係不因此相同，拓撲仍逐張核對。

每張來源的 boundary-apex augmentation 都有保存的 K5／K3,3 subdivision，
共用 199 份證書。
`--check` 重建來源邊，檢查 branch 點、路徑及內部互斥，不呼叫 planarity。
有序接線／證書編號 SHA256 與程式、依賴、輸入證書 hashes 一併保存。

無界覆蓋由 §1–4 的位置分類、訊息判準與 minor 構造承擔；假想 disk
來源必有本節某張非 disk 正常形或舊樹正常形為 boundary 固定 minor，矛盾。
T4 僅用於原圖的區域定位，中間 minors 不需保持完整 Σ 或 T4。

## 6. 重播及精確停止點

[checker](../scripts/c5_degree5_shared_triangles.py)、
[certificate](../artifacts/c5_degree5_shared_triangles/observations.json)。
另保存長臂、保留／刪除標記及整個 cluster 位於旁支的具名來源，逐步
核對 degrees、全部 F、criticality、boundary 固定 branch sets，並將最終
非平面證書合成回原始來源。實際數字及執行結果見 [STATUS §15](STATUS.md#15-三-spoke-共用點雙-triangle-排除)。

```bash
uv run --with networkx==3.5 python scripts/c5_degree5_shared_triangles.py --check
uv run --with networkx==3.5 python scripts/c5_degree5_triangle_components.py --check
uv run --with networkx==3.5 python scripts/c5_degree5_tree_components.py --check
lake build
git diff --check
```

**下一個窄問題：C 的兩個 triangles 頂點互斥，由任意 bridge 路徑連接。**
先依兩個 z 接點在連接路徑／兩環／旁支的實際位置分型，再判定哪些
bridge 真正分隔出不含接點的 forcing 分量。兩個接點分落 bridge 兩側時，
切開 C 後兩側仍透過同一 z 關聯，不能把 singleton forcing 當成與 z 色
無關，也不能直接搬用全 degree-4 整圖的「連接路徑必為一條邊」。

本輪只完成兩環共用點分支。互斥雙 triangle、含長環的雙環、更多環、
其他接點分拆、一般 degree-5／degree≥5、單側／共同出口、候選 A 及
`K∞=K≤5` 均仍有缺口。沒有新增 Lean theorem；本輪與前四輪未 commit／push。
