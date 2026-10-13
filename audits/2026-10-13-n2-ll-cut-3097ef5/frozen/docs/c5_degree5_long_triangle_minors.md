# 一長奇環加 triangle：保留接點的來源 minor 與排除

文件整理（2026-09-23），R21：互斥混合雙環排除完成；[R22](c5_degree5_two_long_cycles.md) 補雙長環，[R24](c5_degree5_shared_cycle_minors.md) 補共用點型。
系列定位見 [degree-5／R 系列導讀](c5_degree5_guide.md)，研究優先序見
[HANDOFF](HANDOFF.md)。下文「下一步／未解／未提交」保留當輪語境；
歷次驗證與發布見 [研究歷史](STATUS_HISTORY.md)，不代表本次重新驗證。

發布註記：本報告與 R21–R23、Lean 接合基礎一併發布，核對見 [STATUS 歷史 §27](STATUS_HISTORY.md#27-r21r23-與-lean-接合基礎發布核對)。
以下保留研究輪當時的提交狀態與驗證範圍。

2026-09-18，R21。從乾淨 HEAD `3d6a647` 接手，完成 R20 指定的圖層缺口。
**唯一 degree-5 點 z 有三條 boundary spokes，連通二接點分量 C=H−z
恰含兩個互斥 odd-cycle blocks，其中一個長奇環、一個 triangle，其餘
為 bridges 時，不存在接受全部 T4 的 C5 disk minimal q-obstruction。**
臂長、長奇環長度及無接點外枝不設上限。

這是紙面化約＋Python 有限來源證書，沒有新增 Lean theorem。
[R20 root 介面](c5_degree5_long_triangle_roots.md)、R17／R19 的接線覆蓋
及所有既有 scripts／artifacts 保留不變；本輪未 commit／push。

後續（R22）：[互斥雙長環](c5_degree5_two_long_cycles.md) 已補完兩步縮減、
兩種順序及真正雙長環來源，任意長度互斥雙 odd-cycle 已排除。
以下保留 R21 當時的停止點。

## 1. 前提與位置分拆

沿用 [三-spoke 區域化約](c5_degree5_sectors.md)：固定
q=(A,B,A,B,C)、D=3、N_B(z)={b0,b1,b4}，C 的 attachments 位於
arc (b1,b2,b3,b4)，F_C(q)={D}；另一區域由鏡像處理。
C 的每個有效內點完整 degree=4，z 的 degree=5。T4 僅用於原圖區域定位。

如果兩環間有 bridge 不分隔兩個 z 接點，消去無接點側後只剩至多一個
odd-cycle，交回既有樹／單環排除。否則每個接點各經外臂到一個環，
兩環間有 bridge 路徑。不含接點的旁枝用單 bridge 消去引理處理，保留
來源中的實際同色 B-spoke；D 禁色以三種 q 色 spokes 的 D 葉點實現。
這一步及其 minimality 前提沿用 [單環 §1](c5_degree5_odd_cycle_components.md)。

每側外臂與中間 bridge 可在同一環點或不同環點接入，合計四型。
不把同色 boundary 點識別，也不把同分量兩個接點當獨立 marginals。

## 2. 從完整 root 到 boundary 固定 minor

長環 bridge root 記 r、外臂接入點記 p。R20 §1–3 已證：拒絕 D 迫使
私有環點的 lists 全是同一二色 S（S 可以含 D），且對固定 z=a：

- p≠r：M_r(D) 為 singleton，其餘三列均為 r 原三色 list。
- p=r：M_r(a)=(U\S)\δ(P(a))，δ 只保留外臂訊息的 singleton。

這些完整四列與保留接點的 triangle 相同。一般三色 root 及任意二元
pinning 的反向控制仍保留在 R20；此處只用 obstruction 必要性之後的公式。

p≠r 時保留 r,p 及任意一個私有點；p=r 時保留 r 及任意兩個私有點。
按長環次序記這三點為 x0,x1,x2。每段 xi 到 x(i+1) 的 arc：

1. 刪除所有不保留環點的 attachments，包括其 D 葉點。
2. 把 arc 內部點全部收進 xi 的 branch set，保留最後一條通往 x(i+1) 的邊。
3. 其他點保持 singleton branch sets；尤其五個 boundary 點和 z 不動。

三個環 branch sets 互斥且連通，目標恰為 triangle。兩個接點不合併；
所有保留點的外臂、中間 bridge、spokes 與 D 葉點均保持原接線。
不要求各 arc 的長度為奇數：只使用 source 與 target 都是奇環。

所得圖是來源的真正 boundary 固定 minor。z 仍 degree=5；各保留環點的
兩條環邊及外向 degree 不變，其他有效內點仍 degree=4。
C 仍連通，兩個 triangles 互斥，其餘 blocks 為 bridges。

## 3. 四種 z 色、minimality 與拓撲接合

長環四列 root 不變，另一 triangle、外臂及中間 bridge 全部原樣保留，
故 R20 §4 的精確串接公式給出完整 F_C(q) 不變，仍為 {D}。
這一步不縮臂，也不以「仍拒絕 D」替代其餘三列。

依 [完整接點介面 §4](c5_degree5_interfaces.md) 的連通 degree-4 分量解除
引理，刪任一碰到 C 的非 boundary 邊均解除其限制；實際 attachments
的 q 色互異及完整 degrees 均保持。刪除三條 z-spokes 分別釋放 A、B、C，
由 F={D} 可延拓。因此目標重新滿足 minimal q-obstruction。
這是從介面與度數重建 criticality，並非任意 minor 都保留 minimality。

假想來源是 C5 disk，則此 boundary 固定 minor 仍是 C5 disk，且所有
attachments 仍位於指定 arc。兩側不同點直接交給
[R17](c5_degree5_bridge_arms.md)；至少一側同點交給
[R19](c5_degree5_bridge_mark_minors.md)。它們的後續縮臂及全部接線
非 disk 覆蓋只需指定 arc、degrees 與 F={D}，不要求目標仍接受全部 T4。
既有正常形 apex 圖含 K5／K3,3 minor，與 disk 性矛盾。

因此四種串接型全部排除，加上 §1 的旁支型，完成所述混合互斥雙環排除。
無界性來自三段 arc 的一般 branch-set 構造、R20 的任意環長公式及既有
任意路徑長度化約；以下有限來源不代替這些紙面論證。

## 4. 有限來源與直接驗證

[程式](../scripts/c5_degree5_long_triangle_minors.py)、
[證書](../artifacts/c5_degree5_long_triangle_minors/observations.json)。
按「長環接點型、另一 triangle 接點型、長環 palette」的 24 組，從既有
R17／R19 模板各選路徑最短／最長代表，共 48 個目標。每個 triangle
分別展開成 arc 長度 (1,2,2)、(2,1,4)、(3,4,2) 的來源，含偶數 arc。
新插入點的 B-spokes 在 b1／b3 間變換；D 葉點亦保留具體接線。

| 核對 | 結果 |
| --- | --- |
| 四種有序接點型 | 不同／不同、不同／同、同／不同、同／同，各 36 張，共 144 張來源 |
| 環與 palettes | C5／C7／C9，各型包含全部六個 S，含 S 含 D 的情況 |
| 圖與著色 | 來源和目標的 degrees、互斥雙環、全部四種 z 色逐圖重算；來源保存 8,946 份非 boundary 刪邊 q-coloring |
| 真正 minor | 保存來源／目標邊、每個 branch set、每條目標邊的來源邊；boundary 與 z 保持 singleton |
| 非 disk 證書 | 直接驗證既有目標 subdivision，再合成到每張來源 apex 圖，直接核對 K5／K3,3 minor |
| 檔案來源 | 保存本輪／既有依賴及三份輸入證書 SHA256，先核對既有來源和輸入指紋 |

checker 不呼叫 planarity oracle，不重跑 R17 的 246,645,568 接線或 R19
的 571,400 接線覆蓋。僅重播本輪具名來源及所用既有 subdivisions。
48 個目標的選擇是機制控制域，不是任意來源或所有接線的枚舉。

```bash
uv run python scripts/c5_degree5_long_triangle_roots.py --check
uv run --with networkx==3.5 python scripts/c5_degree5_long_triangle_minors.py --check
lake build
git diff --check
```

`--check` 唯讀重算、逐 byte 比對。沒有新增 Lean theorem，不宣稱保持
完整 boundary Σ、任意二元 pinning 或所有 T4。

## 5. 精確停止點

已完成一長環＋triangle 的互斥雙環排除。下一個窄問題是**兩個互斥長
odd-cycle blocks，其餘 bridges**：R20 的每側公式已有候選構件，下一步
要明確核對第一側縮環後，第二側的必要性、四列介面及 attachments
仍符合前提，再保存兩步及合成來源 minor／逐邊刪除著色。
不要僅把本輪單側資料複製兩份就宣稱雙側來源證書完成。

共用點長環、更多環、其他 degree-5 接點分拆、一般單側／共同出口、
候選 A 及 `K∞=K≤5` 仍開放。
