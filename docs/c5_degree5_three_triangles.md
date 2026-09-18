# 三環共用點鏈：三個 triangle 正常形的實際接線與拓撲

2026-09-18，R26。接手 HEAD `e14874d` 與未提交 R24–R25，沿
[R25](c5_degree5_three_cycle_roots.md) 指定的下一題推進。本輪未 commit／push。
本報告完成 **兩臂各在末端私有點、臂色序列為簡單序列的三個 triangle
鏈正常形**。全部必要接線均有可重播非平面證書；任意長來源的 boundary
固定 minors 尚待接上。成果為紙面構造＋Python 證書，未新增 Lean theorem。

## 1. 精確正常形

固定 q=(A,B,A,B,C)、D=3、z=5，z 的 spokes 接 b0,b1,b4。
三個 triangles 為 (r12,p1,u1)、(r12,r23,w)、(r23,p3,u3)，
r12≠r23；兩臂由 z 分別到 p1、p3。依 R25，拒絕 D 時末端有效
palette 為 T，中間為 S=U\T。共同點的原 list 為 U；u1、u3
的 list 為 T，w 的 list 為 S。

每條臂用被迫色序列 (D,...,c) 表示，c∈S；接點原 list 為 T∪{c}。
序列相鄰兩色 a,b 之間設一個 list={a,b} 的臂內點。序列 (D)
表示 z 直接接末端點，沒有臂內點。若 c≠D，取所有不重複四色的
簡單序列，恰有五種；若 c=D，只取 (D)。

因此 D∈S 時每側有 1+5=6 種，D∉S 時每側有 5+5=10 種；
全部六個 S 共 `3×6²+3×10²=408` 個有序模板。這是固定正常形域的
完整覆蓋，不是任意長臂或任意三環位置的原圖枚舉。

每個缺少的非 D list 色用實際同色 boundary spoke 實現；缺少 D
則接一個具有 A、B、C 三條 spokes 的私有葉點。限定在區域 arc
(b1,b2,b3,b4)，A 接 b2、C 接 b4、B 獨立選 b1 或 b3。
所有 choices 的 Cartesian product 包含每個 D 葉的獨立 B 選擇。
鏡像區域沿用既有區域定位，沒有宣稱這些圖的全部 T4 rows 均接受。

## 2. 四列、degrees 與 minimality

共同點各有四條環邊；末端接點兩條環邊、一條臂邊及一個禁色；
其他私有環點和臂內點各有兩條骨架邊及兩個禁色。D 葉亦 degree=4；
z 恰有三條 boundary 邊和兩條臂邊，degree=5。

固定 z=a 後，R25 的完整接合判準使 D 列拒絕；a≠D 不會再輸出
原指定 singleton，故另外三列接受，完整 F={D}。實作另用 graph
coloring solver 核對每個模板代表的四列及原圖 q 不可著色，並為
每條非 boundary 邊保存刪除後 q-coloring，直接驗證 pins 及全部邊。

同模板的實際接線保留內部頂點標號、全部內部邊，以及每點的 boundary
色多重集；checker 逐接線驗證此事。故固定 q 著色可以按原標號搬運。
對刪除 boundary spoke，對應同內點、同 q 色的 spoke；D 葉的角色
與標號也固定。因此代表的全部刪邊著色涵蓋其餘同模板接線。
這個搬運只用於 fixed-q coloring，不用來搬運其他 boundary rows 或拓撲。

## 3. 拓撲證書及重播

[程式](../scripts/c5_degree5_three_triangles.py)、
[證書](../artifacts/c5_degree5_three_triangles/observations.json)。
每個實際接線加一個連到五個 boundary 點的 apex；若原圖可嵌入 C5
外邊界 disk，則此 augmentation 必 planar。每張 augmentation 都由
已保存的 K5 或 K3,3 subdivision 覆蓋，故所有正常形皆非 disk。

| 核對域 | 數量 |
| --- | ---: |
| 有序 palette／簡單臂模板 | 408 |
| 實際接線，全部非 disk | 327,968 |
| 模板代表的 z 色查詢 | 1,632 |
| 模板代表的逐邊刪除著色 | 19,020 |
| 共用 K3,3 subdivisions | 72 |

生成時使用 NetworkX 找 subdivision；`--check` 主動禁用 planarity
APIs，只驗證保存的 branch 點、各路徑邊、內部互斥以及 subdivision
模型。重播依同一順序重建全部接線與證書索引，核對覆蓋 digest、
程式及載入的本地依賴 hashes，最後逐 byte 比對 artifact；不寫檔。

```bash
uv run --with networkx==3.5 python scripts/c5_degree5_three_triangles.py --check
uv run python scripts/c5_degree5_three_cycle_roots.py --check
lake build
git diff --check
```

新 checker 已在停用 planarity APIs 後唯讀逐 byte 重播通過；
`lake build` 通過（8,822 jobs，僅既有 lint）。本輪統計與驗證結果見 [STATUS §30](STATUS.md#30-r26-三個-triangle-鏈正常形拓撲)。
R15／R17／R19 大覆蓋未重跑，未使用其雙環覆蓋代替本輪三環覆蓋。
R24、R20／R23 standalone checker 亦未重跑；R25 已直接重播。

## 4. 精確停止點

下一步以本報告的已存正常形為目標，建立 **任意長環與重複色外臂的
boundary 固定來源 minors**：保留 r12、r23、末端接點及 palette
錨點，核對每一步的 degrees、四列、逐邊刪除著色，並把本輪 subdivision
合成回來源。尤其 r12、r23 分別可吸收兩個相鄰環的 arc，branch sets
仍須互斥，不能把 R25 的布林縮環直接叫作 graph minor。

目前結論只覆蓋上述 408 個正常形及其全部實際接線；尚未宣布任意
三環鏈的 disk 排除。其他三環接點型、更多環、一般 degree-5／degree≥5、
單側／共同出口及 `K∞=K≤5` 仍開放。完整有序 root 關係與 Σ 不保持。

後續 R27 已補完上述末端二臂鏈型任意長環／重複色臂的來源 minors、
逐步四列與刪邊著色，以及本報告拓撲證書回接；見
[R27](c5_degree5_three_cycle_minors.md)。一般三環排除仍未完成。
