# 四個 triangle blocks 的共用點分叉型

後續狀態（2026-09-17 文件整理）：[bridge pruning](c5_shared_pair_bridge.md)
已補齊本文未涵蓋的四環混合型；本文成果已納入 `fb6216e`，
下文未提交字樣是當時紀錄。現況見 [交接](HANDOFF.md)。

2026-09-17。接續 [四環共用點鏈](c5_four_triangle_chain.md) 的停止點。
保留前輪尚未提交的鏈型產物。

**全 degree-4、中央 triangle 的三個不同頂點各共用一個末端 triangle，
並允許任意外掛樹的 disk minimal q-obstruction 不存在。** 不需 T4。
本結論是紙面 list/minor 化約加 Python 有限證書，未新增 Lean theorem。

## 1. 九點核心及 residual lists

固定 boundary C5、q=01012、未用色 D=3、四色集合 U。內部圖 H 連通，
四個非 bridge blocks 為

```
(u,v,w), (u,a,b), (v,c,d), (w,e,f).
```

九個核心頂點互異，其餘 blocks 都是 bridges，形成任意外掛樹。
每個有效內點的完整 degree=4；原圖不延拓 q，但刪任一非 boundary 邊可延拓。
u、v、w 都有四個核心鄰居，故無 spokes 或外枝，原始 list=U。

沿用 [三環共用點報告](c5_shared_triangle_blocks.md) §2：每個外掛 bridge
分量唯一強迫一個色；同一母點的外枝強迫色在原始 list 中且互異，否則刪
相應 bridge 不能釋放母點色，違反 minimality。由 |L(t)|=deg_H(t)，扣除
所有外枝強迫色後，a 至 f 各有恰二色 residual list。此步涵蓋任意大小、
分叉及深度的外掛樹。

## 2. 三個禁集共同阻擋的充要條件

末端 (u,a,b) 對 u 的禁集，當 list(a)=list(b)=P 時為 P，否則為空；
其他兩端同理。這是既有 apex 二色 list 引理。

若任一末端禁集為空，中央對應點可用四色，另兩點至少各有兩色。
先替後兩點選不同色，再替四色點選第三色，即可延拓中央及三個末端。
因此不可著色要求三對末端 lists 各相等，分別記為 P、Q、R。
中央 triangle 的可用 lists 於是為 U\P、U\Q、U\R，均有兩色。
三個二色 lists 的 triangle 不可著色恰在三 lists 相等，因此

```
q 不可延拓 ⇔ list(a)=list(b)=list(c)=list(d)=list(e)=list(f)=P。
```

恰六種 palette 配置。中央有效 list 為 Pᶜ，而非原始 list U。
checker 遍歷 6^6=46,656 個配置，比較九點實圖的獨立回溯、三個末端介面
拼接及上述判準；恰六個拒絕配置。此論證不需平面性，也不把禁集當成
bridge 的單色強迫。

## 3. 必要 minors

若 D∈P，六個末端非共用點的所有外枝強迫色都非 D，吸收成母點的相應色
spokes 後，得到九內點核心。若 D∉P，六點各有一個 D-forcing 外枝；各
保留成單點 D-forcer，其餘非 D 分量吸收成 spokes，得到十五內點。

D-forcer 必碰到全部三個 q 色，非 D 的 s-forcer 必碰到 s 色 boundary；
否則以 D 與缺失色對換可破壞唯一強迫性。故可收縮並各保留一條所需色的
spoke。不同外掛分量互不相交，操作可同時進行且不識別 boundary 頂點。
這只建立 boundary 固定的必要 minor，不宣稱完整 relation 保持。

模板中中央三點 list=U；六個末端點 list=P∪{D}；新增葉點 list={D}。
每個缺失 q 色恰一條 spoke，枚舉該色全部 boundary 鄰居選擇，無同構去重。

| 末端 palette P | 內點數 | lifts | disk |
| --- | ---: | ---: | ---: |
| 含 D | 9 | 4,224 | 0 |
| 不含 D | 15 | 528,384 | 0 |
| 合計 | | **532,608** | **0** |

全部由 **111 份 K3,3 subdivisions** 覆蓋：每個 lift 在外側新增鄰接全部
boundary 的 apex，保存的 subdivision 必包含於該 apex 圖。若原圖為 disk，
此 apex 圖及其 minors 應平面，矛盾。六個 palette controls 各選一個接線
代表，独立核對所有內點 degree=4、q 不可延拓與逐非 boundary 邊 criticality；
其他同色 boundary 鄰居選擇給相同 lists，因此也有相同 q-criticality。

## 4. 四環純共用點連接的範圍

若四個 triangles 全經共用 cut vertices 連成一塊、沒有環間 bridge，
每個共用點至多屬於兩環，因三環共用一點會使該點 degree≥6。
把每個 triangle 看成節點、共享點看成邊，block-cut tree 性質給出四節點樹。
四節點樹只有 path 與三叉 star：path 是前輪的鏈型，star 是本輪。
因此**四環純共用點連接、任意外掛樹的情形已全部排除**。

這未涵蓋四環由 bridge 與共用點混合連接，也不能直接推出任意環數至多二。
沒有證明任意長鏈可縮成三／四環，更沒有把本輪升格為一般 shared-cut
block tree、較長 odd cycles、K4 blocks、degree≥5 或 K∞=K≤5 的定理。

## 5. 證書與下一步

[script](../scripts/c5_four_triangle_star.py)、
[certificate](../artifacts/c5_four_triangle_star/observations.json) 保存逐 lift 的
witness index、共用 subdivisions、枚舉 digest、六份 criticality controls、
46,656 個配置的重算結果、12 個來源 hashes 與兩個依賴證書 hashes。
`--check` 重建全部 lifts、驗證每個模型的真實路徑／分支／內點互斥及逐例
包含性，並要求 JSON 逐 byte 一致；不呼叫 planarity search。
無界外掛樹覆蓋由 §1、§3 的紙面化約承擔。

```bash
uv run --with networkx==3.5 python scripts/c5_four_triangle_star.py --check
uv run --with networkx==3.5 python scripts/c5_four_triangle_chain.py --check
lake build
git diff --check
```

下一個窄問題：**兩對共用點 triangles，以 bridge path 相連**。
先求每一對在連接端 root 的可取色介面，判斷 bridge 強迫色能否為 D，
再決定可用的吸收或必要 minor。不要將二色禁集直接當作 bridge 強迫色，
也不要只增加連接路徑長度做枚舉。

本輪及鏈型 checkers、`lake build`（8,821 jobs，僅既有 lint）、文件連結與
whitespace 檢查通過。保留前輪產物；兩輪尚未提交或推送，無背景研究程序。
