# K4 block 排除與全 degree-4 單缺失結論

後續（2026-09-18）：[degree-5 完整接點介面](c5_degree5_interfaces.md) 已完成
本文 R10 的染色介面與 minimality 條件；共同 disk／T4 排除仍開放。

2026-09-18。從乾淨 HEAD `dad5940` 接續 [多長環報告](c5_multi_odd_cycles.md)
的 R9。**全 degree-4 的 planar minimal q-obstruction 不含內部 K4 block。**
外接 bridge 側可以是任意大小、任意 blocks 的連通圖；不需 T4，甚至此步
只需一般 planarity。結合既有 degree-choosability 與 odd-cycle／tree 報告，
得到：**接受全部 T4 的 C5 disk minimal q-obstruction，若所有有效內點的
完整 degree 都是 4，則 `Σ(G)=Ω\{q}`。**

成果是紙面證明與 Python 有限證書，未新增 Lean theorem。一般單側出口、
共同 pivotal edge、候選 A 與 `K∞=K≤5` 仍未證。

## 1. K4 四個外接方向與 bridge forcing

令 boundary 為 B=C5，固定 q=01012，U={0,1,2,3}，D=3。
G 不能延拓 q，但刪任一非 boundary 邊都可；H 是有效內點誘導圖。
設 K={v₁,v₂,v₃,v₄} 是 H 的 K4 block，每個有效內點完整 degree=4。

K 的每個點已有三個 K 內鄰居，故恰有一個 K 外鄰居。這唯一外接邊若不是
boundary spoke，便是 H 的 bridge：否則它屬另一個非平凡 block，該 block
在此點至少再用兩條邊，使完整 degree≥5；或外部路徑返回另一個 K 點，
使 K 不再是 maximal biconnected block。不同 K 點的 bridge 外側內點分量
因此互斥，且各自只接自己的 K 點。此處沒有假定外側是樹或沒有 K4。

對 bridge vw，刪邊後令 K 側 root 可取色集為 S，外側 F 的 root 可取色集
為 T。minimality 使 S、T 非空；若存在 s∈S、t∈T 且 s≠t，便可拼回原圖
的 q-extension。因此 `S=T={c}`。

外側 F 必接到 boundary：若沒有 boundary 鄰居，其一個 coloring 可以
任意置換四色，root 可取全部 U，與 singleton 矛盾。更精確地，既有
[swap 論證](c5_shared_pair_bridge.md) 給出：c≠D 時 F 必碰 c 色 boundary；
c=D 時 F 必碰全部三種 q 色。只需此最弱的「至少一個接點」便可證 §3。
這一步從刪橋後確實存在的 coloring 出發，沒有使用四色定理。

## 2. Residual lists、root 介面及正常形

若 v 的外接是 spoke，令 c_v 為該 boundary 的 q 色；若是 bridge，令 c_v
為外側的唯一強迫色。消去四個相互獨立的外側後，K 上的 residual lists
恰為 `R(v)=U\{c_v}`，每個大小為三。這是固定 q 的精確消去。

四個三色 lists 可給 K4 著色，當且僅當它們不全相同：Hall 條件中，至多
三個 lists 的 union 至少三色，只有全部四個的 union 可能不足四色；不足
恰在四個 lists 是共同三色集合 P。因此 obstruction 強迫四個 c_v 同為 c。
也就是 K4 palette 為三色 P=U\{c}，四個外接方向同色 c。

保留一個 root 的 list=U，只消去其他三點外枝時，root 介面為

```
其他三個 residual lists 同為 P：A=U\P，是 singleton；
其他三個 residual lists 不全同：A=U。
```

證明：固定 root 色 r 後，其餘 triangle 各有至少二色；若有三色 list，或
三個二色 lists 不全同，便可著色。失敗只在三個 lists 原本同為含 r 的 P。
checker 直接枚舉四點完整色指派：256 個 unrooted 輸入恰四個不可著色；
64 個 rooted 輸入恰四個 singleton、60 個 U。這些是完整局部介面計算。

沿用既有 bridge pruning，可得保持 boundary、degree-4、固定 q 拒絕及
逐邊 minimality 的兩種正常形：

- c≠D：每個 bridge 外側吸收成一條 c 色 spoke，剩 K4 加四條 spokes。
- c=D：每個外側縮成有三條異色 spokes 的 D 葉點，剩 K4 加四個 D 葉點。

以實際 boundary 頂點為接點，前類 c=0、1、2 分別有 16、16、1 個 lifts；
後類有 4⁴=256 個，共 289 個。checker 核對每張完整圖的 degree、q 拒絕、
所有非 boundary 刪邊的具體 coloring，及下節的 minor。
一般 pruning 的新邊 minimality 引用原引理，不從「是 minor」直接推得。

## 3. 不需正常形枚舉的 K5 minor

每個 K 點 v 選一條通到 boundary 的路徑 P_v：spoke 情形取該邊；bridge
情形由 §1 在外側連通分量內走到第一個 boundary 接點。四條路徑除 boundary
端點可能相同外，內點互斥，且各只碰自己的 K 點。

先給出 **boundary 固定的 minor**：對每個 v，把 P_v 除 boundary 端點以外
的全部點併入 v 的 branch set；五個 boundary 點各保留 singleton。保留
K 的六條邊、C5 與四條新 spokes，其餘邊刪除。每個 branch set 連通且互斥。
這一步只用來排除 planarity，不聲稱保持 q 拒絕、minimality 或完整 Σ。

最後將整個 boundary cycle 收縮成一點 h，得到 K4 加一個與四點皆相鄰的 h，
即 K5，與原圖 planar 矛盾。**這最後一步會識別 boundary，只作非平面性
證書，不是 boundary-state 操作。** 同一 minor 可直接在來源圖表示為：

```
h 的 branch set = B ∪ ⋃_v (P_v 去掉 v 與 boundary 端點後的內點)；
其他四個 branch sets = {v₁}, {v₂}, {v₃}, {v₄}。
```

h 的 branch set 由 C5 及四條接上 boundary 的尾路徑組成，連通；五組互斥，
每兩組之間皆有來源邊。故任意外枝的排除由這個紙面構造負責，並非將 289
個正常形外推。無需新增 planarity 搜尋、apex oracle 或 bridge 長度枚舉。

## 4. 合成全 degree-4 的單缺失結論

現在另假設 G 是 C5 **disk**、接受全部 T4、是 minimal q-obstruction，且
每個有效內點完整 degree=4；孤立內點忽略。

1. T4 排除 boundary chords；minimality 排除重複 q 色 spokes，且使 H
   非空連通。每個 list 都含 D，`|L(v)|=deg_H(v)`。
2. 使用既有 [degree-choosability 化約](c5_weak_list_cores.md)：不可 list-color
   的 H 必為 Gallai tree，每個 block 是 clique 或 odd cycle。這一步依賴
   標準外部定理，敘述已核對 [Cranston–Rabern 的摘要](https://arxiv.org/abs/1511.00350)。
   此外部定理不是本輪 Python 或 Lean 證書的一部分。
3. Planarity 排除 K5 及更大 clique；§3 排除 K4 block。餘下只有 odd cycles
   與 bridges，故 [多長環報告](c5_multi_odd_cycles.md) 適用：沒有長環，
   triangles 頂點互斥且至多二。
4. 零 triangle 用 [樹核心定理](c5_tree_cores.md)，一個 triangle 用
   [任意外掛樹定理](c5_triangle_forks.md)，兩個用
   [直接 bridge 六內點分類](c5_two_triangle_blocks.md)。三種情況各得
   `Σ(G)=Ω\{q}`；前兩者在此處使用接受 T4 的前提。

這完成全 degree-4 的 minimal obstruction 分支，沒有內點數限制。
後三步依賴既有紙面化約與有限 topology 證書，不代表新增純 Lean 定理。
§3 不要求 T4，但本節的單缺失結論仍保留 T4／disk 假設。

對候選 A 的直接推論：來源 `Σ(G)=Ω\{p,q}` 若有一個全 degree-4 的 minimal
q-obstruction B，則 B 只拒絕 q，故刪到 B 的 first strict step 只釋放 p。
因此 **只釋放 p 的出口若失敗，每一個 minimal q-obstruction 都必有完整
degree≥5 的內點**；degree 在該 obstruction 自己的圖中計算。
交換 p、q 同理。兩個單側結論不能推出共同出口。

## 5. 證書與重播

[checker](../scripts/c5_k4_blocks.py)、
[certificate](../artifacts/c5_k4_blocks/observations.json)。

- 256 個 unrooted 與 64 個 rooted list 配置，用完整色指派核對公式。
- 289 個正常形 lifts 全部核對 degree、q-criticality、bridge 兩側 singleton。
- 10 個具名分枝控制：四個外側 K4（含 D-forcing 情形）、長度 2／4／6／8
  的四個 path forcers，以及混合 spoke／path／K4。它們是明知非平面的
  obstruction 控制，不是新的 disk witnesses。
- 共 299 張圖各保存全部刪邊 coloring、真實連通路徑、boundary 固定的
  minor branch sets／每條目標邊來源，以及直接回到原圖的 K5 branch sets。
- `--check` 重算所有值並逐 byte 比對；證書包含本程式 SHA256，無新
  planarity oracle 或四色定理。任意外枝及 §4 的合成仍是紙面論證。

```bash
uv run --with networkx==3.5 python scripts/c5_k4_blocks.py --check
uv run --with networkx==3.5 python scripts/c5_multi_odd_cycles.py --check
uv run --with networkx==3.5 python scripts/c5_tree_cores.py --check
uv run --with networkx==3.5 python scripts/c5_triangle_forks.py --check
uv run --with networkx==3.5 python scripts/c5_two_triangle_blocks.py --check
lake build
git diff --check
```

本輪實際驗證結果記於 [STATUS §9](STATUS.md#9-k4-排除與-degree-4-合成基準-dad5940)。

## 6. 下一個窄問題

R9 完成，下一題 R10 選 **恰有一個完整 degree=5 的有效內點 z，其餘皆
degree=4 的 minimal q-obstruction**。先利用 degree-4 誘導分量的 Gallai
結構，保留它們連到 z 的所有端點與共同色框，推導整個分量的可延拓介面。
需同時控制 degree-5 點與多個接點；不能把一個分量的多個端點拆成獨立
bridge singleton，也不能直接套用「所有內點 degree=4」的 disk 排除。

先測這個介面能否支持雙缺失／T4 的必要條件，再決定 minor 或反例方向；
不直接提高 graph catalog 的 k。一般 degree≥5、單側／共同出口、候選 A、
weak-deletion congruence 與 `K∞=K≤5` 仍未證。本輪成果與後續 degree-5 介面一併提交發布。
