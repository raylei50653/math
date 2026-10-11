# 三環共用點鏈：同末端兩個不同接點的正常形拓撲

文件整理（2026-09-23），R31：408 模板／327,968 接線的正常形非 disk 覆蓋完成；任意長來源 minors 仍是保留缺口，不能宣稱此型已任意長排除。
系列定位見 [degree-5／R 系列導讀](c5_degree5_guide.md)，研究優先序見
[HANDOFF](HANDOFF.md)。下文「下一步／未解／未提交」保留當輪語境；
歷次驗證與發布見 [研究歷史](STATUS_HISTORY.md)，不代表本次重新驗證。

2026-09-18，R31。承接 [R28](c5_degree5_three_cycle_positions.md) 的
list 介面，完成 C3–C3–C3、兩個不同私有接點同在一個末端環、
兩臂為簡單色序列的正常形實際接線與非 disk 覆蓋。
本輪為**紙面構造＋Python 有限證書**；未新增 Lean theorem。
任意長來源 minor 尚待建立，一般三環仍未排除。

## 1. 正常形與完整接線域

沿用三-spoke、唯一 degree-5 點 z、其餘有效內點 degree-4、fixed-q
minimal obstruction 的設定，以及既有區域定位與 forcing-list 正規化。
固定 q=(A,B,A,B,C)、D=3、z=5，z 接 b0,b1,b4。
三環為 (6,8,9)、(6,7,10)、(7,11,12)，共用點 r12=6、r23=7。
兩臂分別接 p1=8、p2=9；另一末端的 11、12 都保留。
交換鏈的兩端只是重新命名內點；有序臂對涵蓋接點交換，不交換 boundary。

令中間 palette 為任意二色 S，末端 palette 為 T=U\S。
兩共用點 lists 為 U；10 為 S；11、12 為 T。
兩臂色序列 w_i=(D,…,c_i)，c_i∈S，接點原 list 為 T∪{c_i}。
相鄰色 a,b 之間放一個 list={a,b} 的臂內點；(D) 表示直接邊 z–p_i。
各序列不重複四色；終色 D 只有一條序列，其他終色各五條。
故六個 S 的有序臂對共有 3×6²+3×10²=408 個模板。

每個缺色 A 接 b2，缺色 C 接 b4，缺色 B 獨立選 b1 或 b3。
每個缺色 D 新增私有葉，接該點、b2、b4，以及獨立選擇的 b1 或 b3；
q 下葉色被迫為 D。接線域完整包含區域 arc (b1,b2,b3,b4) 的所有選擇。
另一鏡像區域沿用 R11 定位；本輪不宣稱接受全部 T4。

無接點末端不是 singleton 旁支：其向 r23 交回 S 的二色限制。
本構造保存兩個私有點及全部 attachments，沒有用直接刪環取代它。
這與 R26 的末端各一臂是不同接線域，需獨立拓撲證書。

## 2. Degrees、四列與 minimality

共用點各有四條環邊；接點各有兩環邊、一臂邊及一禁色 attachment；
其餘私有環點及臂內點各有兩骨架邊、兩禁色 attachments。
D 葉 degree=4，z degree=5，H−z 連通且三個 cycle blocks 都是 triangles。

移除 z 的三條 spokes，逐一固定 z 的四色，以圖回溯核對完整 F={D}。
R28 的判準亦給出原因：D 列兩接點恢復 T，形成 T–S–T 拒絕；
未標記末端的 11、12 固定 T。其他列若拒絕，兩臂必再輸出原 c_i，
而指定 singleton 輸出的反向唯一性要求輸入為 D。

每個模板代表另核對保留 z spokes 的 q 拒絕，為每條非 boundary 邊
保存刪邊後完整 q-coloring，逐頂點、pin 及邊驗證。
所有 B 選擇只替換同內點的一條 b1／b3 spoke。程式逐變數核對邊差集，
並核對變數邊彼此互異且不在固定邊中。因此任意組合保持 degrees、
內部圖和各內點的 boundary 色多重集；四列及刪邊著色可按原標號搬運。
若刪除移動的 spoke，對應代表中同內點、同 q 色的 spoke。
此搬運只適用 fixed-q，不宣稱保持其他 boundary rows 或完整 Σ。

## 3. 拓撲證書及重播

[checker](../scripts/c5_degree5_same_terminal_triangles.py)、
[certificate](../artifacts/c5_degree5_same_terminal_triangles/observations.json)。
每模板的獨立 B 選擇構成完整 Boolean cube，總計 327,968 種具名接線，
不是非同構圖數。圖上加入接全部五個 boundary 點的 apex；若原圖為
C5 外邊界 disk，augmentation 必 planar。

生成器從未覆蓋接線找 subdivision，依其使用的變數邊求出有效子 cube，
逐次扣除直到餘集為空。保存 68 份非平面 subdivisions、435 次子 cube
引用。`--check` 停用 NetworkX planarity APIs，直接驗證保存路徑的實際
邊、branch 模型與內部互斥，再重建全部 cube 覆蓋。
四變數全部 6,561 組 cube 對另以獨立真值表核對差集與互斥性。

本輪共驗 1,632 次 z 色查詢、19,020 份刪邊著色。來源與載入的本地
程式依賴 hashes、覆蓋 fingerprint 均保存；重播唯讀逐 byte 比對
1,592,286-byte JSON。生成及重播通過，`lake build` 通過（8,822 jobs，
僅既有 lint），未新增 Lean theorem。詳見 [STATUS 歷史 §35](STATUS_HISTORY.md#35-r31-同末端不同二接點正常形)。

```bash
uv run --with networkx==3.5 python scripts/c5_degree5_same_terminal_triangles.py --check
lake build
git diff --check
```

沿用 R13 attachment／simple-walk helpers、既有圖著色與 subdivision
validator、R17 cube 差集；新正常形骨架與接線覆蓋獨立建立，未讀舊
observations.json。R28 判準引用紙面結果，未重跑其 standalone checker；
R30／R29／R27／R26 及 R15／R17／R19 的既有大覆蓋本輪均未重跑。
既有 scripts／artifacts 未修改。

## 4. 精確停止點

同末端不同二接點的 C3–C3–C3 簡單臂正常形已全部非 disk。
下一步為任意長環及重複色外臂建立 boundary 固定來源 minors：
接點末端保留共用點與兩接點；中間保留兩共用點與一個 S 錨點；
無接點末端保留共用點與兩個 T 錨點。再縮臂並合成本輪拓撲證書回來源，
逐步驗 degrees、完整四列及刪邊著色；縮臂允許 z 吸收臂點。

R28 list 等價尚不取代此圖層工作，故不宣布任意長同末端型已排除。
末端與中間、同點會合、環間 bridge、其他分拆 (2) 及一般三環仍開放。
完整 Q／Σ 不宣稱保持，`K∞=K≤5` 未證；未 commit／push。
