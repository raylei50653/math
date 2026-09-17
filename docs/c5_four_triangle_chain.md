# 四個 triangle blocks 的共用點鏈

後續狀態（2026-09-17 文件整理）：[四環分叉](c5_four_triangle_star.md) 與
[bridge 混合型](c5_shared_pair_bridge.md) 已完成；本文成果已納入 `fb6216e`，
下文未提交字樣是當時紀錄。現況見 [交接](HANDOFF.md)。

2026-09-17。接手 HEAD `f147591`、工作樹乾淨；接續
[三環共用點報告](c5_shared_triangle_blocks.md) §5 的指定窄問題。

**全 degree-4、內部為四個 triangles 依序共用不同 cut vertices，並允許任意
外掛樹的 disk minimal q-obstruction 不存在。** 不需 T4。
這是紙面 list/minor 化約加有限 Python 證書，未新增 Lean theorem。

## 1. 設定與外掛樹

固定 boundary C5、q=01012、未用色 D=3。內部圖 H 連通；四個非 bridge
blocks 依序為

```
(v,a,b), (v,w,x), (w,z,y), (z,c,d).
```

v、w、z 兩兩不同，其他核心點均不同；其餘 blocks 是 bridges，形成接在
此九點核心的外掛樹。每個有效內點在完整圖的 degree=4，刪任一非 boundary
邊後 q 可延拓。共享點各有四個核心鄰居，沒有 spoke 或外枝，list 為四色 U。

其餘六點扣除外掛 bridge 分量的強迫色後，各有二色 residual list。
理由沿用三環報告 §2：刪 bridge 後兩側 root 強迫同一色；各外枝強迫色在
母點 list 中且互異，否則刪該 bridge 仍不能釋放母點色，違反 minimality。
原 |L(u)|=deg_H(u)，扣完外枝後剩下核心 degree 2。這適用任意大小、深度與
分叉的外掛樹，並未枚舉這些樹。

## 2. 禁集 transfer

考慮 triangle (v,w,x)。已處理的左側在 v 禁止 F，故 v 可取 U\F；
x 有二色 list R，w 尚未受右侧約束。輸出禁集為

```
T(F,R) = R   若 F 是二色且 R=U\F；
T(F,R) = ∅   否則，這裡 F∈{∅}∪所有二色集合。
```

證明：F=∅ 時，給定任何 w 色，先替 x 選不同色，再替 v 選避開兩色的
第三色即可。F 為二色時，v、x 各有二色 list；既有 apex 引理說，兩 lists
相同時恰禁止共同的兩色，不同時不禁任何色。因此輸出非空恰在 R=U\F。
空禁集此後永遠保持空。這是集合介面，沒有把它當 bridge singleton 色。

左端 a、b 的 lists 必相同為 P，否則左端不禁 v 任何色，整條鏈必可延拓。
經第一個中間環後，只有 x 的 list=Pᶜ 才保留禁集 Pᶜ；經第二個後，只有
list(y)=P 才保留禁集 P。右端 c、d 必同為 Pᶜ，才與左側禁集共同覆蓋 U。
所以整條鏈不可著色恰在

```
list(a)=list(b)=list(y)=P,
list(x)=list(c)=list(d)=Pᶜ。
```

恰六種配置。checker 對全部 6^6=46,656 種 residual-list 配置，比較
九點實圖的獨立回溯、逐環 transfer 及上述判準；另重算 7×6=42 個 transfer
輸入。不依賴平面性。這裡推導出 transfer，並未假設四環可直接縮成三環。

## 3. 必要 minors 的完整覆蓋

P 與 Pᶜ 各出現三次，所以恰三個非共用點的 residual list 不含 D。
每個此類點必有唯一 D-forcing 外枝；保留該枝並壓成單點 D-forcer。
D-forcer 必碰到全部三個 q 色，否則可交換 D 與未碰到的色。
其他非 D 強迫枝各吸收到母點，保留一條相應色 spoke；這種分量必碰到該色
boundary，亦由色交換得出。不同外枝互不相交，可同時操作。

所得 minor 有九個核心點、三個 D 葉點，共十二內點。共享點 list=U；
其他核心點 list=residual∪{D}；葉點 list={D}。每個缺失 q 色保留恰一條
spoke，枚舉該色全部 boundary 頂點選擇。原有同色重複 spokes 已由
逐邊 minimality 排除。所有操作保留 boundary 頂點互異，不宣稱完整 Σ
或任意 rooted interface 保持。

| 左端 P | lifts | disk |
| --- | ---: | ---: |
| 含 D | 12,288 | 0 |
| 不含 D | 12,288 | 0 |
| 合計 | **24,576** | **0** |

對每個 lift 加一個鄰接全部 boundary 的 apex，保存的 **16 個 K3,3
subdivisions** 覆蓋所有 apex 圖。disk 圖加外側 apex 必平面，而 minor
保持平面性，故排除原 disk obstruction。六個 palette controls 各取一份
實圖，獨立檢查完整 degree=4、q 不可延拓及逐非 boundary 邊刪除可延拓；
其他同色 boundary 接線有相同 lists，因此也具有相同 q-criticality。

## 4. 證書、驗證與停止點

[script](../scripts/c5_four_triangle_chain.py)、
[certificate](../artifacts/c5_four_triangle_chain/observations.json) 保存逐 lift
witness index、subdivisions、枚舉 digest、六份 criticality controls、完整
transfer 表、11 個來源 hashes 與三環證書 hash。`--check` 重建全部 lifts，
檢查 subdivision 路徑／分支／內點互斥與逐例包含性，並要求 JSON 逐 byte
一致；重播不呼叫 planarity search。無界外掛樹的覆蓋由 §1、§3 承擔。

```bash
uv run --with networkx==3.5 python scripts/c5_four_triangle_chain.py --check
uv run --with networkx==3.5 python scripts/c5_shared_triangle_blocks.py --check
lake build
git diff --check
```

上述兩個 checkers 與 `lake build`（8,821 jobs，僅既有 lint）通過；文件連結與
whitespace 亦通過。本輪未提交或推送，沒有背景研究程序。

**下一個窄問題：四環全以共用點相接時的分叉型。** 一個中央 triangle 的
三個不同頂點各接一個末端 triangle；各末端提供二色禁集，中央三點因此各
剩二色 list。先推導它們同色 palette 的必要條件，再建立必要 minor；
不要把本輪鏈的排除當成所有四環連接型態已完成。

本輪不涵蓋四環間含 bridge 的混合連接型、任意長共用點鏈、任意 shared-cut
block tree、較長 odd cycles、K4 blocks 或 degree≥5，亦非 K∞=K≤5 的證明。
