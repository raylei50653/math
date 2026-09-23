# 互斥雙 triangles：標記路徑 minor 與同點接入排除

文件整理（2026-09-23），R19：結合 R15–R17 完成恰兩個 triangles；含長環的雙環由 [R20–R24](c5_degree5_shared_cycle_minors.md) 補完。
系列定位見 [degree-5／R 系列導讀](c5_degree5_guide.md)，研究優先序見
[HANDOFF](HANDOFF.md)。下文「下一步／未解／未提交」保留當輪語境；
歷次驗證與發布見 [研究歷史](STATUS_HISTORY.md)，不代表本次重新驗證。

發布整理（2026-09-18）：本報告隨 R16–R20 一併提交。下文的「未提交／HEAD／
下一題」保留各輪當時狀態；最新停止點見 [HANDOFF](HANDOFF.md)，
本次提交核對見 [STATUS 歷史 §22](STATUS_HISTORY.md#22-r16r20-提交整理與核對)。


後續（R20）：[長奇環加 triangle 的完整條件 root](c5_degree5_long_triangle_roots.md)
已完成同點／不同點四列介面及縮環的 list 等價；下一步為混合來源的真正
boundary 固定 minor 與刪邊著色。以下保留 R19 成果及當時停止點。

2026-09-18，R19。從 HEAD `b55abf4` 及未提交 R16–R18 接手，補完
[R18](c5_degree5_bridge_marks.md) 指定的兩個缺口：真正來源 minors 與
全部接線的拓撲覆蓋。R16–R18 scripts／artifacts 原封保留，未 commit／push。

**三-spoke、唯一 degree-5 的 C5 disk minimal q-obstruction，若接受全部
T4，且連通二接點分量 C=H−z 恰含兩個互斥 triangle blocks、其餘為 bridges，
便不存在。** 本輪處理至少一側外臂與中間 bridge 在同一環點接入；
兩側不同環點由 R17 處理，同側旁支由 R16 處理。不限制路徑長度及外枝分叉。
結合 R15，恰兩個 triangle blocks 的共用點／互斥兩種情形皆已排除。

這是紙面化約＋Python 有限證書，沒有新增 Lean theorem。兩環含長
odd-cycle、更多環、其他 degree-5 分拆及 `K∞=K≤5` 仍開放。

## 1. 延用介面與完整位置分拆

固定 q=(A,B,A,B,C)、D=3、N_B(z)={b0,b1,b4}，C 位於 arc
(b1,b2,b3,b4) 一側，F_C(q)={D}；鏡像由區域化約涵蓋。
每個非 z 有效內點完整 degree=4。T4 只用於來源的區域定位。

若兩環間某條 bridge 不分隔兩個 z 接點，R16 已把不含接點側消成
單 triangle／樹。否則每個 z 接點各經一條外臂抵達一個環，與中間
bridge 路徑形成串接；不含接點的外枝按單 bridge 引理消去。
每側只有「外臂與 bridge 在不同環點」或「同一環點」兩種。
兩側不同點是 R17；剩下一側同點、兩側同點，正是 R18 的兩組正常形。

同點 root r 的兩個私有 triangle 點若有相同二色 list S，則完整
root 介面為 U\S；若 lists 不同則為 U。後者提供 slack，不能出現在
拒絕 D 的串接中。因此同點 root 是路徑上的**標記二色 list 步驟**，
其二色限制由一個真正 triangle 實現，對四種 z 色皆相同。

- 一側同點：另一 triangle 保留不同接點，其一條外臂含一個標記。
  兩臂各從 D 輸出指定 singleton，刪閉段後成簡單色序列。保留標記
  的終端共 858 型；若標記消失，進入既有單 triangle 正常形。
- 兩側同點：兩個標記位於兩端接 z 的同一條二色路徑。
  F={D} 等價於強迫色序列從 D 回到 D 且至少使用三色。
  只刪仍保留至少三色的閉段；兩標記都保留的終端共 186 型。
  剩一個／零個標記時，進入既有共同接點單 triangle／樹正常形。

序列的無界終止與五型分類沿用 R12–R13；標記始終按步驟位置追蹤，
相同色不表示相同頂點。R18 的 D,A,D,B,D → D,B,D 反向控制仍適用：
任意刪閉段會把 F={D} 變成 F={B,D}，故不能只保持拒絕 D。

## 2. 每一步的 boundary 固定 minor

設路徑內點為 v₀,…,vₙ₋₁，vᵢ 的 list 是 {cᵢ,cᵢ₊₁}。
刪去 cᵢ=cⱼ 之間的閉段後，保留的步驟索引為

```
0,…,i−1, j,…,n−1。
```

新步驟的二色 list 與對應舊步驟完全相同。以下構造不新增邊：

1. 每個保留路徑點的 branch set 包含該點及其後、下一保留點之前的
   被移除路徑點；最後保留點亦吸收被移除後綴。
2. 被移除前綴收進 z 的 branch set。開路徑若全部消失，整條臂收進 z，
   保留末端 triangle 點，從原最後一條臂邊得到 z 與該點的直接邊。
   閉路徑至少三色，故至少三個步驟保留，兩個 z 接點不會合併。
3. 標記步驟保留時，該 triangle 的兩個私有點各為 singleton branch
   set，並保留其實際 attachments。標記移除時，刪掉其兩私有點及
   全部 attachments；標記 root 本身依第 1／2 項收縮。
4. 只保留未移除路徑點／私有點的 attachments。其 D 葉點各保持
   singleton，已移除點的 D 葉點直接刪除。收縮可能帶來的多餘邊刪掉。
   五個 boundary 點始終各自 singleton，不識別同色 boundary 點。

各 branch set 連通且互斥，目標每條邊均有具名來源邊；原 boundary
cycle 保持。保留的色對、私有 triangle 及 attachments 與目標 schema
一致，所以 z 的 degree 恢復 5，其餘有效內點恢復 4。

開序列保持從 D 到原指定 singleton 的強迫傳遞，反向唯一性排除其他
z 色產生同一拒絕；閉序列保留至少三色及 D 首尾，故完整 F 仍為 {D}。
連通 degree-4 分量解除引理給出每條分量邊的刪除著色；三條 z-spokes
各釋放 A、B、C，亦因 F={D} 而可延拓。因此目標仍為 minimal q-obstruction。
這不是聲稱任意 minor 自動保持 minimality、完整 Σ 或 T4。

每次至少刪兩個路徑步驟，故任意有限來源會終止。若標記消失，後續
縮減仍可繼續至既有較少環的正常形；若全部標記保留，終端落在 R18
的 1,044 型中。這是任意長度的紙面覆蓋，以下具名來源只是構造控制。

## 3. 全部接線的非 disk 證書

沿用 R17 的 Boolean cube 方法。A spoke 只能接 b2、C spoke 只能接 b4，
每條 B spoke 可獨立接 b1 或 b3；D 葉點的 B spoke 也有獨立選項。
這列出指定 arc 的全部實際接線，不把同色 boundary 點合併。

對每個模板加上鄰接全部五個 boundary 點的 apex。一份 K5／K3,3
subdivision 所使用的 B 邊，只固定部分二元選項；故整個對應子 cube
皆非平面。逐份精確扣去覆蓋，直到剩餘 cube 集為空。覆蓋之外的
選項不會改動證書使用的邊，沒有抽樣或估算。

| 型別 | 必要模板 | 全部實際接線 |
| --- | ---: | ---: |
| 一側同點、單標記外臂 | 858 | 533,728 |
| 兩側同點、雙標記閉序列 | 186 | 37,672 |
| 合計 | 1,044 | 571,400 |

合計 **130 份 subdivisions、1,069 次子 cube 引用**，全部餘集為空。
checker 重算每型代表的四種 z 色及全部非 boundary 刪邊 coloring，
與 R18 原證書逐項一致；其他接線保持 attachment 色及 degree，固定-q
染色問題相同。每個 subdivision 的所有路徑及來源邊皆直接驗證。

來源若為 C5 disk，boundary 固定 minor 仍為 C5 disk，其 apex 圖應
平面，與上述證書矛盾。較少環終端使用 R12／R13 的既有非 disk 證書。
apex-disk 等價與無界來源化約仍在紙面層，未由 Python 或 Lean 取代。

## 4. 長來源控制與驗證邊界

保存 **198 張長來源、432 次縮減**，每個來源及每步目標直接核對
degrees、全部四個 z 色及每條非 boundary 邊的刪除 coloring。
保存來源／目標圖、實際接線、逐步及合成 branch sets，並把最後
K5／K3,3 minor 合成回來源的 apex 圖；不是僅核對色序列語意。

| 來源類別 | 最後剩餘標記數 | 來源數 |
| --- | ---: | ---: |
| 單標記外臂 | 0／1 | 30／18 |
| 雙標記閉序列 | 0／1／2 | 60／30／60 |

單標記控制涵蓋六個 palettes、長左右臂、全部選定長左臂步驟，以及
六張整條標記臂收進 z 的零長目標。雙標記控制涵蓋五種 motifs 的全部
三十個色實例；含相鄰標記、同一步刪兩標記、分步刪標記及兩標記保留。
縮減步中，312 次前綴收進 z、120 次內部／後綴；30 步同時刪兩標記。
這些來源不宣稱窮盡任意長度；一般性來自 §1–2。

## 5. 重播與下一個窄問題

[程式](../scripts/c5_degree5_bridge_mark_minors.py)、
[證書](../artifacts/c5_degree5_bridge_mark_minors/observations.json)。

```bash
uv run --with networkx==3.5 python scripts/c5_degree5_bridge_mark_minors.py --check
uv run --with networkx==3.5 python scripts/c5_degree5_bridge_marks.py --check
lake build
git diff --check
```

新 `--check` 唯讀、逐 byte 比對；重算完整 cube 覆蓋與全部具名來源，
不呼叫 planarity。保存程式／依賴及 R18／單 triangle／樹輸入證書的
SHA256。既有 R17 的 36,672 型大覆蓋不需重跑。本輪結果見 STATUS §20。

**下一題：C 恰有兩個互斥 odd-cycle blocks，一個為長奇環，另一為
triangle，其餘 bridges。** 先區分長環的外臂與 bridge 同點／不同點，
求四種 z 色的完整條件 root 介面，再決定能否保留接點縮為 triangle。
R14 的單環縮減及全 degree-4 的長環結論不能直接套用到此耦合介面；
一般 root 可能有三色訊息，須先檢查而不能只追蹤 D 下的 singleton。

兩長環、共用點長環、多環一般分拆 (2)、其他 degree-5 接點分拆、
一般 degree≥5、單側／共同出口與主命題仍各自保留缺口。
