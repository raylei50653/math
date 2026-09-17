# Bridge forcer 替換與四環混合連接型

後續狀態（2026-09-17）：[任意 triangle tree](c5_triangle_tree_palettes.md)
已完成本文的 cluster 停止點；一般 triangles／bridges 類別中，triangles
必頂點互斥且至多二。本文四環證書與 singleton 替換仍作依賴保留。

2026-09-17。接續 [四環分叉型](c5_four_triangle_star.md)。
本輪先完成兩對共用點 triangles 的 bridge-path 問題，再用同一替換引理
補齊四環所有混合連接型。**全 degree-4、內部連通、恰四個 triangle blocks
且其餘 blocks 都是 bridges 的 disk minimal q-obstruction 不存在。**
不需 T4，允許任意外掛樹、bridge 路徑與連接樹。

這是紙面化約加既有 topology 證書及新的 Python 介面核對；未新增 Lean
theorem，也未宣稱任意 triangle 數至多二。

## 1. 一般 bridge pruning 引理

固定 boundary C5、q=01012、D=3。所有有效內點完整 degree=4，原圖不能
延拓 q，但刪任一非 boundary 邊都可。設內部 bridge uv 切開後保留 u 側 K，
移除 v 側 F；兩側均指內部連通分量，boundary 固定且共用。

G−uv 的 q-extension 說明兩側均可著色；原圖不可著色說明兩 root 的
可取色集合都是同一 singleton {c}。F 可以含任意 cycles，不要求是樹。

### c≠D：吸收為一條 spoke

F 必碰到 c 色 boundary，否則交換 F 內 c、D 會破壞唯一強迫性。
把 F 連同 uv 收縮到 u，只保留一條 c 色 spoke ub，其餘新增 spokes 刪去。
u 原本沒有 c 色 spoke，因 G−uv 可讓 u 取 c，故 ub 是新邊。

新圖仍不可著色：K 強迫 u=c，但 ub 禁 c。u 用一條 spoke 取代 bridge，
所有保留內點 degree 不變。對任一保留的舊非 boundary 邊 e，限制 G−e
的延拓；F 及 uv 未動，所以 u≠c，這是新圖刪 e 的延拓。對新 spoke ub，
取 K 的 u=c 染色即可。因此逐邊 minimality 保留。

### c=D：收縮為一個 D 葉點

F 必碰到 q 的全部三種色，否則交換 D 與缺失色會破壞唯一強迫性。
把 F 的內點收縮成新點 t，保留 ut；每個 q 色各留一條 spoke tb_s，
其餘 F 邊與 spokes 刪去。新點 t 的 list={D}、degree=4。
u 仍保有一條 bridge，所有舊內點 degree 不變。這是 boundary 固定的 minor。

新圖不可著色，因 K 強迫 u=D，而 t 也只能取 D。逐邊 minimality 分三類：

1. 保留的舊非 boundary 邊 e：限制 G−e 的染色到 K。F 未動仍強迫 v=D，
   所以 u≠D；令 t=D 即可延拓新圖刪 e。
2. 新 bridge ut：K 可取 u=D，另令 t=D；刪 bridge 後可拼接。
3. 新 spoke tb_s：K 取 u=D，令 t=s；刪該 spoke 後 t 可取 s，且 s≠D。

因此兩種替換都保留 disk 性、全 degree-4、固定 q 不可延拓及逐邊 minimality。
只保持這些性質，沒有聲稱完整 boundary relation 或任意 rooted 介面等價。
D 情形補足既有非 D 吸收引理；關鍵是檢查新葉點三條 spokes 的刪邊延拓，
不能僅由「是 minor」推出 minimality。

## 2. 兩對共用點 triangles 的連接端

任取緊鄰其中一對、朝另一對的 bridge，保留第一對的一側。其餘路徑、
第二對與路徑外掛樹全屬被替換側 F，套 §1 後只剩兩個共用點 triangles
及外掛樹。由 [兩環分類](c5_two_triangle_blocks.md) 的共用點排除，矛盾。
所以任意 bridge path 長度都排除，完全不必增加路徑長度作枚舉。

為獨立核對 root 介面，五點核心記為 (v,r,x)、(v,a,b)，r 是朝 bridge
的 root。扣除其他外枝強迫色、但尚未扣除朝外 bridge 色時：

```
L(v)=U，|L(r)|=3，|L(x)|=|L(a)|=|L(b)|=2。
```

若 a、b 不同 list，v 可取 U，故 r 可取全部 L(r)。若同為 P，v 可取 Pᶜ；
僅在 L(x)=Pᶜ 時，這個 triangle 對 r 禁止 Pᶜ。因此 r 唯一強迫 c 恰在

```
L(a)=L(b)=P，L(x)=Pᶜ，L(r)=Pᶜ∪{c}，c∈P。
```

864 個 list 配置由完整五點 coloring 枚舉及介面公式交叉核對，恰 12 個
singleton 配置，每個色各三個。**D 不能在純 list 層排除**；需要 §1 的
D-forcer 替換加既有 disk 障礙。c=D 時，正規化 root 外側 D-forcer 及 x
的 D 外枝後，三種 palette 恰逐項吻合既有兩環 `shared` 模板，無新拓撲搜尋。

## 3. 四環全部連接型態

把所有互相經共享 cut vertex 連接的 triangles 歸為一個 cluster；只含一環
也算 cluster。不同 clusters 之間透過 bridge 連接樹相連。
對選定 cluster，每條離開它的 bridge 都可用 §1 去除外側分量。
外側可以含其他 triangles、Steiner 點或任意樹；每次替換保持全部假設，
最後只留下該 cluster 及外掛樹／新 D 葉點。

恰四環時，依 cluster 大小：

- 有大小 2：隔離後與兩環共用點排除矛盾。
- 有大小 3：隔離後與既有恰三環排除矛盾。
- 有大小 4：全部四環經共用點相連，已由鏈型與分叉型排除。
- 全部大小 1：四環頂點互斥，既有互斥 triangle blocks 至多二的結果排除。

涵蓋所有 partition，不需要逐一搜尋混合 bridge 接線。結合既有三環結論，
目前可排除恰三／四環；一般更多環仍可能有大小至少 5 的共用點 cluster。

## 4. 核對、信任邊界與下一步

[script](../scripts/c5_shared_pair_bridge.py)、
[certificate](../artifacts/c5_shared_pair_bridge/observations.json) 保存全部 864
root 介面、12 個 singleton 配置、64 個 bridge 固定 q 可著色性控制、三個
D-spoke 刪除控制、三個舊模板對應、十三個來源 hashes 與五份依賴證書 hashes。
`--check` 全部重算並要求 JSON 逐 byte 一致。64 個控制遍歷任意 root 可取色
子集與四種外側強迫色，僅核對可著色性；**§1 的一般 minor、degree 與
逐邊 minimality 證明仍由紙面論證承擔**。沒有新 planarity search 或 Lean theorem。

```bash
uv run --with networkx==3.5 python scripts/c5_shared_pair_bridge.py --check
uv run --with networkx==3.5 python scripts/c5_two_triangle_blocks.py --check
uv run --with networkx==3.5 python scripts/c5_shared_triangle_blocks.py --check
uv run --with networkx==3.5 python scripts/c5_three_triangle_blocks.py --check
uv run --with networkx==3.5 python scripts/c5_four_triangle_chain.py --check
uv run --with networkx==3.5 python scripts/c5_four_triangle_star.py --check
lake build
git diff --check
```

下一方向：**任意純共用點 triangle tree 的 palette 相容性與局部 minor**。
§1 已把 bridge 混合問題化到共用點 clusters；先判斷是否能從較大 cluster
抽出已排除的必要 minor，且正確保留共享點的二色禁集。不要僅增加五環
catalog，也不要把剪 bridge 的 singleton 替換套到 cut vertex 的二色介面。

本次發布包含本輪與前兩輪的 scripts、證書、報告及 README／HANDOFF。
上述六個 checkers、`lake build`（8,821 jobs，僅既有 lint）、文件連結與
whitespace 檢查通過。研究停止在上述共用點 triangle tree 問題，無背景研究程序。
