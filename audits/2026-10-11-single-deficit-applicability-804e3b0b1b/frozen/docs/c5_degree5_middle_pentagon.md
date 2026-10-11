# C3–C5–C3：中間環兩個不同接點的實際接線與拓撲

文件整理（2026-09-23），R29：正常形拓撲覆蓋完成；[R30](c5_degree5_middle_cycle_minors.md) 已補中間不同二接點的任意長來源 minors。
系列定位見 [degree-5／R 系列導讀](c5_degree5_guide.md)，研究優先序見
[HANDOFF](HANDOFF.md)。下文「下一步／未解／未提交」保留當輪語境；
歷次驗證與發布見 [研究歷史](STATUS_HISTORY.md)，不代表本次重新驗證。

2026-09-18，R29。沿 [R28](c5_degree5_three_cycle_positions.md) 的四標記
list 目標，完成中間 C5 含兩個不同私有接點、兩末端為 C3、兩外臂
色序列為簡單序列的正常形。本輪為**紙面構造＋Python 有限證書**；
未新增 Lean theorem，未 commit／push。任意長來源 minor 後續由 [R30](c5_degree5_middle_cycle_minors.md) 補完。

## 1. 循環位置與實際圖

固定 q=(A,B,A,B,C)、D=3、z=5，z 接 b0,b1,b4。中間 C5 的
slots 為 0,1,2,3,4，實際頂點為 6,…,10。旋轉使第一共用點在
slot 0；第二共用點在 j∈{1,2,3,4}。從其他三個 slots 選兩個接點，
依 slot 大小命名 p1,p2，剩下一點為 palette 錨點。全部位置如下：

| 第二共用點 j | 接點對 |
| --- | --- |
| 1 | (2,3)、(2,4)、(3,4) |
| 2 | (1,3)、(1,4)、(3,4) |
| 3 | (1,2)、(1,4)、(2,4) |
| 4 | (1,2)、(1,3)、(2,3) |

共 12 個具名位置配置；不除去反射或交換末端環的重複。兩臂 profiles
有序，所以接點排序沒有漏掉臂分派。末端 triangles 為 (6,11,12)
及 (6+j,13,14)。兩共用點只接四條環邊。

取任意二色 S 作中間有效 palette，T=U\S 作末端 palette。
四個末端私有點 lists 都為 T；中間唯一未標記私有點 list 為 S。
兩臂的被迫色序列 w_i=(D,…,c_i)，c_i∈T；接點原 list 為 S∪{c_i}。
相鄰色 a,b 之間放一個 list={a,b} 的臂內點；(D) 表示直接邊 z–p_i。
每條序列四色不重複。c_i=D 時只有 (D)，其餘各有五條簡單序列。
每個位置共有 3×6²+3×10²=408 個 palette／有序臂模板，共 4,896 個。

每個缺色 c≠D 以同色 boundary spoke 實現：A 接 b2、C 接 b4，
B 獨立選 b1 或 b3。缺 D 則新增私有葉，接該頂點及 b2、b4、
b1 或 b3，故 q 下葉色被迫為 D。所有選擇都在區域 arc
(b1,b2,b3,b4)，含每個 D 葉自己的獨立 B 選擇。另一鏡像區域由
既有 R11 定位處理；不宣稱全部 T4 rows 接受。

## 2. Degrees、四列與刪邊著色

共用點各 degree=4；接點有兩條環邊、一條臂邊及一個禁色 attachment；
其餘私有環點及臂內點各有兩條骨架邊及兩個禁色 attachments。
D 葉 degree=4，z degree=5。H−z 的內點圖連通，cycle blocks
長度為 3,5,3，兩個共用點互異。

移除 z 的三條 boundary spokes，分別固定 z 為四種色，以圖回溯求解：
完整 F={D}。R28 的 T–S–T 判準亦解釋此結果：D 列各接點扣掉
c_i 後恢復 S；其他列不可能再同時產生原指定 singleton。
保留 z spokes 的原圖 q 不可延拓。每個模板代表為全部非 boundary
邊保存一份刪邊後完整 q-coloring，並直接核對每個 pin、頂點及邊。

同模板所有接線只改變一條 spoke 的 B 端點 b1↔b3，頂點標號、
內部邊及各內點的 boundary 色多重集固定。程式逐一檢查每個獨立
變數確實只替換該邊，且變數邊互異。因此任意變數組合仍保持 degrees，
並可按原標號搬運四列著色和刪邊著色；若刪的是移動的 spoke，
對應同內點、同 q 色的代表 spoke。這只搬運 fixed-q 著色，不能用來
搬運其他 boundary rows 或拓撲。

## 3. Boolean cube 拓撲覆蓋

[checker](../scripts/c5_degree5_middle_pentagon.py)、
[certificate](../artifacts/c5_degree5_middle_pentagon/observations.json)。
每個 B 端點選擇是一個 Boolean 變數。固定模板的全部實際接線
恰為完整 Boolean cube；不同具名模板可能同構，不把接線數稱作
非同構圖數。

在圖上加一個接全部五個 boundary 點的 apex。如果原圖有 C5 外邊界
的 disk embedding，此 augmentation 必 planar。生成器對尚未覆蓋的
接線找 K5 或 K3,3 subdivision，再讀取路徑所用的變數邊，得到該
subdivision 有效的整個子 cube。逐次扣除子 cube，直到餘集為空。

`--check` 禁用 NetworkX planarity APIs，直接核對保存路徑的邊、
branch 模型及內部互斥；逐筆重建子 cube 並檢查剩餘集合為空。
Boolean cube 差集另用四變數全部 6,561 組 cube 對與真值表獨立核對。
重播重新驗證代表的全部著色、來源及載入的本地依賴 hashes、覆蓋
fingerprint，最後逐 byte 比對緊湊 JSON，且不寫檔。

具體統計與本輪驗證見 [STATUS 歷史 §33](STATUS_HISTORY.md#33-r29-c3c5c3-中間二接點正常形)。

```bash
uv run --with networkx==3.5 python scripts/c5_degree5_middle_pentagon.py --check
uv run python scripts/c5_degree5_three_cycle_positions.py --check
lake build
git diff --check
```

## 4. 精確停止點

後續 [R30](c5_degree5_middle_cycle_minors.md) 已完成任意長來源的 boundary
固定 minors 與拓撲合成，排除兩個不同中間接點的共用點三環鏈。
以下保留 R29 當輪停止點；一般三環仍未排除。

本輪完成 C3–C5–C3、兩個不同中間接點、簡單色序列外臂的正常形
實際接線與非 disk 證書。下一步將任意長奇環／重複色外臂來源縮到
本報告正常形：保留中間兩共用點、兩接點、至少一個 palette 錨點，
建立互斥、連通且 boundary 固定的 branch sets，核對 degrees、四列、
逐邊刪除著色，再把本輪 subdivision 合成回來源。縮臂時不能先假設
z 必須是 singleton branch set；沿用 R27 的來源處理方式另作核對。

R28 的 list 布林等價尚不代替上述來源 minor。因此未宣布任意長的
「兩個不同中間接點」型已排除。其他接點型、環間 bridge 三環型、
一般三環及 degree-5 排除仍開放；不宣稱完整 Q、Σ 保持或 `K∞=K≤5`。
R26／R15／R17／R19 的既有大覆蓋本輪未重跑，亦未當成本輪拓撲證據。
