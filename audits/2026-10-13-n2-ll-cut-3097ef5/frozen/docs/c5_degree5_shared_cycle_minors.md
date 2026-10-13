# 共用點雙奇環：來源 minor 與任意環長排除

文件整理（2026-09-23），R24：結合 R22 完成恰兩個 odd-cycle blocks；指定三環鏈由 [R25–R27](c5_degree5_three_cycle_minors.md) 接續，一般三環仍開放。
系列定位見 [degree-5／R 系列導讀](c5_degree5_guide.md)，研究優先序見
[HANDOFF](HANDOFF.md)。下文「下一步／未解／未提交」保留當輪語境；
歷次驗證與發布見 [研究歷史](STATUS_HISTORY.md)，不代表本次重新驗證。

2026-09-18，R24。接手 HEAD `e14874d`，工作樹乾淨；沿 R23 停止點補完
真正來源 minor、degrees、逐邊刪除著色及 R15 非平面證書合成。
本輪未 commit／push。

**唯一 degree-5 點 z 有三條 boundary spokes，C=H−z 是連通二接點分量，
blocks 恰含兩個共用 cut vertex 的 odd cycles、其餘為 bridges 時，
不存在接受全部 T4 的 C5 disk minimal q-obstruction。**
兩環長度、外臂及無接點外枝大小不限。結合 R22 的互斥情形，這補完
三-spoke／連通二接點分量恰含兩個 odd-cycle blocks 的全部位置。

這是紙面化約＋Python 有限來源證書，未新增 Lean theorem；不保持完整
root 關係、任意 pinning 或完整 Σ，不代表一般 degree-5 排除。

## 1. 來源正規化及保留點

沿用 [R15 §1](c5_degree5_shared_triangles.md) 的位置分類與旁支消去、
[R23 §1–2](c5_degree5_shared_cycle_roots.md) 的共同 root 剛性。
q=(A,B,A,B,C)，D=3，z 的 boundary 鄰點為 b0,b1,b4。
兩個 z 接點通往 cluster 的臂，若先在 cluster 外會合，整個雙環
是無接點旁支，交回既有消去及樹排除。其餘情形只有同環不同私有點、
分處兩環、同一私有點會合；共同點 r 已有四條環邊，不能另接臂。
無接點外枝正規化為實際同色 boundary spoke 或 D 葉點，沿用既有
boundary 固定來源 minor；保留 actual boundary 接線。

固定 z=D，拒絕迫使兩環私有有效 lists 分別為互補二色 S、T。
每環保留 r 及兩個私有點：同環兩接點均保留；只有一接點則另保留
一個未標記點；無接點時任選兩個私有點。同點會合保留會合點與一個
palette 錨點。被移除私有點全無臂，其原 list 就是該環的 palette。

## 2. 三段 arc 的真正 minor，包含偶數 arc

按環順序把保留點記為 v0,v1,v2。對從 vi 到 v(i+1) 的有向 arc，
把所有內點放入 vi 的 branch set，終點不放入；刪除這些內點的
attachments（包括其私有 D 葉點），保留三個端點的全部 attachments。
每段至少一條邊，branch sets 非空、連通、互斥，末條 arc 邊實現
目標 triangle 的對應邊。不要求各 arc 為奇數；總環長為奇數即可。

對兩環同時做此構造，共同 root 的 branch set 是兩側 root branch
sets 的聯集，交集恰為 r，所以仍連通；其餘 branch sets 互斥。
所有 boundary 點與 z 都是 singleton；每個目標點的 branch set
恰含自身這一個被保留的來源點。兩環及兩臂不互相識別。
也可分兩步、任一順序收縮，固定每環順序後，合成 branch sets 相同。

保留點原有環邊各被一條 triangle 邊取代；r 仍四條環邊。其他
attachments／臂不變，故 z degree=5，其他有效內點 degree=4。
剩餘 D 葉點仍 degree=4；不產生 boundary 識別或額外邊。

## 3. 四列與 minimality 的重建

[R23 §3](c5_degree5_shared_cycle_roots.md) 對任意 z=a 證明：共同 root
交集為空 iff 兩側有效私有 lists 是互補共同 pairs。上述保留點選擇
使來源、任一中間圖及雙 triangle 目標的判準一致，故完整 F 保持。
這裡只比較交集是否為空；R23 已保存交集本身改變的反向控制。
第一側縮減後第二側的原圖、lists、臂不變，另一側仍滿足相同判準，
因此第二步合法，不需假設完整 root 色集相同。

來源 minimality 給 F={D}。不同端點型亦可用指定 singleton 的唯一
反向輸入推得；同點型必須保留原 F，不能只測 D 被拒絕。
對縮減後的圖，q 下 z 三條 spokes 恰排除 A,B,C，分量恰排除 D，
故整圖不可著色。刪除碰到 C 的任一邊，由
[degree-4 分量解除引理](c5_degree5_interfaces.md)
使 z=D 可延拓；刪除 z 的任一 spoke，則釋放其 q 色 a∈{A,B,C}，
a∉F，亦可延拓。這覆蓋每條非 boundary 邊，重新證明 minimality，
沒有使用「minor 自動保持 minimality」的假設。

雙 triangle 目標現在滿足 R15 任意臂長化約的全部條件。同點型後續
若刪除標記，整個 cluster 被刪而交回樹正常形；若保留標記則接 R15
帶標記覆蓋。因此假想 disk 來源必有非 disk 的 boundary 固定 minor，
矛盾。T4 僅在來源區域定位使用，中間圖不必保留完整 T4 或 Σ。

## 4. 有限來源控制與重播

[checker](../scripts/c5_degree5_shared_cycle_minors.py)、
[certificate](../artifacts/c5_degree5_shared_cycle_minors/observations.json)。
從 R15 888 個模板選每種接點型、每個有序第一環 palette 的最短／最長
骨架各一張，共 36 張目標；採其已存代表接線及 subdivision。
這是機制控制域，不是全部來源或接線枚舉。

| 核對域 | 結果 |
| --- | ---: |
| 來源圖 | 180 張；同環不同點、分處兩環、同點各 60 |
| 有序環長 | (5,3)、(3,7)、(5,7)、(7,9)、(9,5) |
| 兩種縮減順序 | 360 條、720 個逐步 minors；混合型含 identity 步 |
| 四階段固定 z 著色查詢 | 2,880 次，皆恰拒絕 D |
| 來源逐邊刪除著色 | 11,520 份 |
| 四階段逐邊刪除著色 | 36,360 份（含重複的目標／identity 階段） |
| 來源拓撲 | 每張由 R15 subdivision 合成 K5／K3,3 minor |

arc 長度為 (1,2,2)、(2,1,4)、(3,4,2)，包含偶數段、同環三個
保留點及共享 root 吸收兩環內點。所有著色 witness 直接核對 boundary
pins 與每條邊。所有 branch sets 檢查連通、互斥及目標邊的來源。
來源、依賴及輸入證書 hashes 保存於 artifact；重播不寫既有資料。

另保存實際同點圖：閉色序列 (D,0,D)、環長 (5,7) 及雙 triangle
目標皆 F={0,D}，刪 z–b0 仍不可著色，所以均非 minimal。
其 boundary 固定 minor 也直接核對。沒有將該控制送入排除用的 minimal
來源域，也未要求 R23 不成立的完整 root 保持。

```bash
uv run python scripts/c5_degree5_shared_cycle_roots.py --check
uv run --with networkx==3.5 python scripts/c5_degree5_shared_cycle_minors.py --check
lake build
git diff --check
```

本輪重播 R23、新 checker（另停用 NetworkX planarity APIs 重播）、
`lake build`（8,822 jobs，只有既有 lint）。R15／R17／R19 大型拓撲
覆蓋未重跑；沿用其既有覆蓋，核對指紋並直接重驗本輪所用 subdivisions。
既有 scripts／artifacts 未修改。`lake build` 不表示本輪圖層論證已 Lean 化。

## 5. 新停止點

三-spoke／連通二接點分量恰兩個 odd-cycle blocks 的任意長度與位置
已由 R15–R24 合成排除。下一窄題選 **三環共用點鏈**：
J1 與 J2 共用 r12，J2 與 J3 共用 r23≠r12，兩個外臂分別落在末端環。
先求中間環的完整有序 (r12,r23) 關係，再接兩個末端 root 訊息；
不能把中間環替成兩個獨立 root 色集。先做固定-q 介面，不預先宣稱
縮環或 topology 排除。一般更多環、其他 degree-5 接點分拆、單側出口、
共同出口及 `K∞=K≤5` 仍開放。
