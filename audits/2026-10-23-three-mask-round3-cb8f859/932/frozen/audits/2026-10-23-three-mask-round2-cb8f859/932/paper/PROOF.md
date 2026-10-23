# 原 C9 三接點的完整 cell 計數與來源排除

2026-10-23。BASE `cb8f8593e273a7426ecadd59797a6e643cc4768e`。
本證明只在 [SOURCE_CONTRACT](../SOURCE_CONTRACT.md) 的原完整、全域最小
no4ct `Σ=932,h=4` 二十種原 collar 來源成立。不使用四色定理、較大來源
圖枚舉、計數 LP、任意 C6 內點數上界或 Lean。

新結論：**每個原嚴格內點最多接兩個原 C9 點；九個原邊面第三點 t_i 的
C9 contacts 均恰為自己原邊的兩端。** 這排除前輪唯一三接點分支，不排除
沒有三接點的原 h=4 來源。

## 1. 繼承的原圖與必須保留的資料

固定同一原 H、原有向 induced `C=(c0,...,c8)`，`I=V(H)\C`。原 c 的 A/Y
名字、原 B attachments、annulus edges/faces/rotation、完整 820 列、每列
十個 annulus fibres（包括空集）及所有 literal full lifts 均採凍結資料。
內部 C3 cap 空、C4 cap 空、C5 cap 空或 W5，以及原 C 點 H-degree≥4、
原 I 點 degree≥5，都是繼承前提。

前輪任意大小紙證已給：若原 x∈I 有三個 C contacts，必為某個原
`t=t_i`，contacts 恰為 `{c_i,c_(i+1),c_(i+5)}`，且它的三條原 spoke
把 C 內側分為空原三角面與兩個 induced C6 cell。前輪還證全 H 至多一個
這樣的點；本輪不把這些幾何結果重算為新發現。

以下先令 i=0；對其他 i 只沿原有向 C 作索引平移，保存原 c 真名，從不
交換兩個 bounded sides，也不把不同原 collar 的內側資料混在一起。

## 2. 完整 fibres 的精確接合

兩個實際原 cell 為

```
D+ = (t,c1,c2,c3,c4,c5),
D− = (t,c5,c6,c7,c8,c0).
```

其閉 disk 交集正是原邊 `tc5`；嚴格內點集合 I+、I− 互斥。原 H 恰由
這兩份 cell 與原空三角面 `(c0,c1,t)` 組成。平面嵌入保證沒有一條原邊
連接兩側的嚴格內點：這種邊必穿過原 separator。所有貼在各 cell 邊界的
原邊均仍屬該原 cell；沒有丟掉 attachment，也沒有合併任何原頂點。

固定同一 literal proper C9 assignment σ。對每個
`κ∈{0,1,2,3}\{σ(c0),σ(c1),σ(c5)}`，令

- `F+_κ(σ)` 為原 D+ 中、原 t 色為 κ、其餘五個邊界點依 σ 的全部嚴格
  內點 full lifts；
- `F−_κ(σ)` 對原 D− 同樣定義。

定義包括所有空 fibres。限制映射及反向聯集給真正的集合雙射

\[
 F_H(\sigma)\cong
 \bigsqcup_{\kappa\notin\{\sigma(c_0),\sigma(c_1),\sigma(c_5)\}}
 F^+_\kappa(\sigma)\times F^-_\kappa(\sigma). \tag{1}
\]

反向接合時，共同原 t、c5 的 literal colors 完全相同，兩側使用同一原 H
的固定 cell，並且原三角面也 proper。因此聯集是原完整 H 的一次 full
lift；沒有補入新點、新邊或另一個見證圖。不同 κ 的聯集互斥。

令 `x_σ=|F_H(σ)|`。式 (1) 的整數版本保留 full lift multiplicities：

\[
 x_\sigma=\sum_\kappa |F^+_\kappa(\sigma)|\,|F^-_\kappa(\sigma)|. \tag{2}
\]

## 3. 三種 anchor 顏色迫出一個具體的 rank-one 限制

固定三個相異的 literal colors
`σ(c0)=a, σ(c1)=b, σ(c5)=c`，第四色為 d。這時 κ=d 唯一。
令 u=(σ(c2),σ(c3),σ(c4))，v=(σ(c6),σ(c7),σ(c8))。
從 b 到 c 的四邊 proper path 恰有 20 個 u；從 c 到 a 同樣有 20 個 v。

同一原 D+ 的 extension count 只依 u，記為 A_u；同一原 D− 的 count
只依 v，記為 B_v。式 (2) 因而給原 H 的完整 20×20 count matrix

\[
 \boxed{X_{u,v}=A_uB_v.} \tag{3}
\]

這不是單獨可行的 marginal counts。A、B 都來自這一個固定原 H 的完整
cell fibres；每次交叉接合都有 (1) 的原圖 full lift。所有 2×2 minors
因此為零，且正支持必為一個 Cartesian rectangle：

\[
 x_{u,v}>0,\ x_{u',v'}>0
 \Longrightarrow x_{u,v'}>0,\ x_{u',v}>0. \tag{4}
\]

這個對同一來源的整數計數／正支持限制是本輪的新輸入。

原 certificate 的 C9 row 以一次整體 S4 正規化保存。對每個三色 anchor
row，先用**唯一的一個整體 S4 permutation** 將 a,b,c,d 同時映到 0,1,2,3，
再取兩條弧。接合兩條弧時兩側已在同一 literal frame；最後才將混合後的
整條 C9 word 作一次既有 row 正規化。沒有對兩條弧或兩個 cell 分別正規化。
每個 i 的 400 個 grid entries 與 anchor 三色的原 row orbits 一一對應。

若三個 anchors 只有兩色，κ 有兩個，式 (2) 是兩個非負 outer products
之和，rank≤2；**不能使用 (3)–(4)**。checker 對這些 rows 不作 rectangle
補閉；把 anchor 三色改成兩色是明確拒絕的負控制。

## 4. 與同一原 H 的 whole Kempe orbit 共同推進

令 S 是目前仍可能包含原 H 正支持的必要 C9 row set。初值恰為繼承的
二十份 annulus／whole-Kempe fixed point，非另選來源或另解 count cone。

對某個正 row p 和任一 complementary color split，取它的一份實際 full
H coloring。該 split 的兩類實際二色分量在 C 上誘導一份 noncrossing
partition；原邊上的同類相鄰 contacts 必在同一分量。任意子集分量的交換
全是同一 H 的合法 full coloring。因此它們的**整個** boundary orbit O
均在原 H 正支持中。這個實際 partition 必出現在固定 C9 checker 完整
重建的 options 中；沒有要求任意形式 partition 都能由原 H 實現。

對 O 中 anchor 三色 rows 先作 §3 的共同 literal restoration，收集其
u、v 投影，加入全部混合 u×v rows；其餘 O rows 保留。記此集合為 cl_i(O)。
由 (4)，若 O 全正，則 cl_i(O) 全正。補閉只需一次：新混合 entries 不會
增加任何 u 或 v projection。

所以若 p 的某個 split 的**每個**可能 whole orbit 都有

\[
 \operatorname{cl}_i(O)\not\subseteq S, \tag{5}
\]

則 p 不可能正，可刪除。式 (5) 檢驗的是每個 orbit 的完整必要補閉，沒有
逐個交換選擇不同的來源見證。每個批次只使用該批次入場 S；同步刪除後
再開始下一批。歸納可知每步 S 仍包含原 H 的全部正支持。

## 5. 精確有限排除範圍

`certificate.json.gz` 保存全部 `20×9=180` 個原 collar／原 t_i 假設、
各自入場支持、每批當時支持、所有刪除 row 及失敗 splits，以及最終空集。
獨立 checker 不 import producer，從頭重建：

1. 完整 820 個 proper C9 row orbits 及十個 C5 rows；
2. 全部 4862 份九圈 noncrossing component partitions；
3. 每 row、每個 split 的 whole options，共 49356 個 orbit entries；
4. 二十份原 annulus 的完整 `820×10` fibres（含空）及全部 full lifts；
5. 九份各 20×20 的 literal-anchor mixed-row grids；
6. 每個 (5) 的當時前提及完整刪除範圍。

180 個最終支持皆空。原完整 Σ932 非空，故原 H 至少一列正；正支持不能
被上述必要刪除刪空。因此這 180 個原 triple-contact 假設逐一排除。
繼承的三接點分類覆蓋所有可能原三接點，遂得

\[
 \boxed{\forall x\in I:\ |N_H(x)\cap C|\le2.} \tag{6}
\]

每個原 t_i 已接自己的原邊兩端，故其 C contacts 現在精確為這兩點。
這是原來源中某一具名幾何分支的排除，並非有限控制圖的來源實現，也不是
全體 h=4 來源排除。

## 6. full-lift 控制、完成成本與停止點

checker 另取前輪一張具名 `one_triple_m11` 有向 disk 控制，按其真正原邊
分出兩個 C6 cells 與共同原 edge。固定三色 anchors 及第四色 t 後，完整
枚舉兩份 cell lifts，逐份 Cartesian 接合；其 full vertex-color tuples
集合與直接 whole graph 枚舉完全相等，全部 400 fibres 包括空集都比較。
控制沒有原 B、完整 Σ932 或全域最小性，所以完整來源狀態是 `not triggered`。
它只校準本輪 (1)、(3) 的集合／計數介面。

本輪使用的重接是原 colouring 的零頂點、零新邊接合，不是候選 smaller
patch。沒有提出需要隱藏 completion vertices 的縮小圖，沒有把任意 C6
換成 bounded hub，也沒有以 rank-one 必要矩陣冒充原來源實現。

現行共同 k≥23 及其外部 C4 census 信任仍只是繼承 authority；本輪不重播
外部計算、不提高 k 下界。不帶 triple 假設時，仍保存全部 820 row order、
完整 annulus relations 及 lifts；沒有宣稱任何無條件 row deletion。
一般 h=4 無三接點分支、h≥5、一般 932、smaller bad、K∞ 及新 Lean 均 OPEN。
下一窄義務是無三接點來源中，原距四 double contacts 的共同嵌入或具名
cell 的可回填化約；本輪在已封存的三接點排除處停止。
