---
docgraph:
  id: c5.adjacent-degree5-mixed-edge-shared-t2
  family:
    - c5
    - c5.degree5
  derives_from:
    - c5.adjacent-degree5-mixed-edge-shared
  requires:
    - c5.adjacent-degree5-mixed-edge-order
    - c5.adjacent-degree5-singleton-long-arc
  related:
    - c5.single-sided-exit
---
# 共鄰端點 mixed K2：w 側兩條 spoke 的實際支援與雙列分離

2026-09-28。接續 [完整關係與逐邊 minimality](c5_adjacent_degree5_mixed_edge_shared.md)，
完成其中 **t_w=2、(1) 的 18 筆原必要資料**。在 induced-C5 disk 的同一
minimal q-core 前提下，這個接線型必接受 p₁=01021、p₂=01212，**不需 T4**，
不限制兩份 unary 原分量的大小、block 數或 bridge 長度。

原四環加 chord 的任意大小化約給 280 份幾何支援；接合原 18 筆關係
及 28 組局部 K2 支援後有 38 筆必要資料、30 份不同支援配置。
全部 76 個指定查詢接受、0 個未決；原 18 筆中 10 筆的支援集合為空。
沒有證明其餘資料可 disk 實現，也沒有改寫原 306／288 筆關係證書。

證據為紙面支援／annulus 證明、沿用外部 degree-list 定理，以及 Python
完整禁色集合上界的有限接合。未新增 Lean theorem。一般單側／共同出口
與 K∞=K≤5 仍未證；研究優先序只見 [HANDOFF](HANDOFF.md)。

## 1. 同一來源與原接線

G 有限簡單，B=(b0,…,b4) 是 induced disk 外框；有效內部 H 非空連通。
q=01012、U={0,1,2,3}。G 拒絕 q，刪任一非框邊後接受 q。
相鄰 z、w 完整 degree=5，其餘內點完整 degree=4。
H−{z,w} 的唯一 mixed 原分量為 uv，原 root incidences 恰為 zu、zv、wu。
本輪另取 w 恰有兩條 boundary spokes。

由前報告，z 沒有 spoke，恰接一個二接點 unary 原分量 C_z；w 恰接
一個單接點 unary 原分量 C_w。固定其具名接點 (x₀,x₁)、y，完整 tuples
仍屬同一 C_z、C_w，全部原附件及旁支不變。記 actual supports 為
S_z、S_w；u 的單點支援為 {i}，v 的兩點支援為 {j,k}。

存在互異的 h,e,d∈{0,1,2}，使

\[
q_i=h,\quad\{q_j,q_k\}=\{h,e\},\qquad
F_z(q)\in\{\{h\},\{h,d\},\{h,3\}\},\quad F_w(q)=\{3\}.
\tag{1}
\]

以 s_h、s_d 命名原 w-spoke 的落點，q(s_h)=h、q(s_d)=d；兩點不同，
不是新添的接線。q 下 F_z={h} 的 95 個完整 schemas，以及雙禁色時
兩個相反次序的完整關係都由前報告保留；下文使用從完整關係精確定義
的 F，沒有把 x₀、x₁ 的 marginals 相乘。

## 2. 支援下界與原四環加 chord 的外側

**S_z 至少見兩個 q 色，S_w 必見全部三個 q 色。** 兩份非空 F 的容量
分別不超過二、一。支援為空時，全色對稱與此容量矛盾。若 S_z 只見
一色 a，固定 a 的其餘三色置換迫使 F_z={a}。固定 z=a 後，C_z 的
外鄰只用 a；不可著色 degree lists 的緊性使每點 deg_C≥3。

原 z–u–b_i 路徑避開 C_z，將 B 與 z 接成外部連通 hub，所以
[連通外框 K4 引理](c5_degree5_tree_components.md#1-連通外框排除-degree-4-分量的-k4)
排除 C_z 的 K4 block。不可著色 degree lists 給 Gallai tree，但 K4-free
Gallai tree 的葉塊非 cut 點有內度≤2，矛盾；singleton 亦不例外。
此處沿用 [Dvořák Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
的緊性及 Gallai 結構，本輪核對原文，並非 Python／Lean 內部定理。
若 S_w 缺少 q 色 a，交換 a 與 3 固定其所有原 boundary 色卻移動
F_w={3}，矛盾。故兩個支援跨度下界為一、二。

考慮原 diamond D，其邊為 zw、wu、uv、vz、zu。u、v 各有原 boundary
spoke，w 亦有兩條；z 經 C_z 的一條原路徑到 B，其內部避開 D。
所以 D 的四點都可從 D 外到達 B，必全在 D 的外面上。D 二連通，
外面邊界是 simple cycle；唯一含四點的 cycle 是

\[
Q_D=z-w-u-v-z.
\]

若外面是三角形，就會把 w 或 v 留在有界面內，與其原 boundary 邊
矛盾。因此 **zu 是 Q_D 內側的原 chord**。每份 unary 都碰 B，不能
留在 D 的有界面；有界面也不能容納它的部分頂點，因原分量只能經
自己的 root 穿出，而分量本身連通。因此 Q_D 內除 chord 外無有效接線。
這一步是本接線型自己的證明，沒有把 u 誤當有兩條 boundary spokes。

## 3. 六個原單位的同序支援

取 Q_D 閉內部的小正則鄰域，外側為 annulus。六個單位依序為

\[
C_z,\quad \operatorname{perm}(C_w,s_h,s_d),\quad u,\quad v,
\tag{2}
\]

或整體反向。C_z 的兩個具名 contact 仍保留兩種內部方向。
w 的三個單位可有全部六種次序；chord 在內側，不插入外側單位。

將同一 b_i 的原入射端在小鄰域內分開，仍記作同一 b_i、同一顏色。
各 unary 加截短 root 邊是兩兩不交的連通集合，u、v 的原 spokes
則按其外側小星狀鄰域連起；每個單位都碰 annulus 的兩條邊界。
在一個單位中連接兩個外端的 crosscut，其不含內圓周一側不能有另一
單位的外端，否則後者無法連回內圓周。因此外端也成同序區塊。
這是 [原四環次序引理](c5_adjacent_degree5_mixed_edge_order.md#2-原四環外側的同序區塊與周長界)
的同一 Jordan 論證，此處明確容許 u 與兩條 root-spokes 為零跨度。

從 C_z 第一個外端起讀，各 actual support 可提升為整數集 T_A，使

\[
\min T_{C_z}=a,\quad \max T_{O_r}\le\min T_{O_{r+1}},\quad
\max T_{O_5}\le a+5,\qquad T_A\bmod5=S_A. \tag{3}
\]

各支援點只提升一次：一份支援若首尾重複同一 b_i 就佔滿整圈，與
其餘正跨度單位矛盾。不同單位的端點可以重合，支援內可以有間隙。
這不是將 actual support 擴成整條框弧，也沒有假設 boundary 接線唯一。

令 ℓ_A=max T_A−min T_A，則

\[
\ell_z\ge1,\quad\ell_w\ge2,\quad\ell_v\ge1,\qquad
\ell_z+\ell_w+\ell_v\le5. \tag{4}
\]

所以本型尚有一條框邊的餘量，不能套用前輪總跨度至少六的矛盾。
原兩條 w-spokes 必各落在 (2) 的 w 區塊，且落在不同框點；u 的
落點仍在 w 與 v 的原相鄰位置。這些零跨度限制也納入 (3)。

## 4. 完整的有限必要域與同圖跨列上界

checker 先按 (2)–(3) 遞增生成所有六單位支援，得 **280 份**；尚未套用
q 色，但已要求兩條 w-spokes 的框點不同。另一算法獨立枚舉 Cz、Cw、v
的全部 proper cyclic hull，用框邊 mask 互斥及 w 區塊的整體區間條件
重算相同集合。兩算法均容許共享端點、支援間隙及非最短 cyclic hull。

再套 (1)、q(S_z) 至少兩色、F_z 的支援穩定子與 q(S_w)={0,1,2}，
並引用前報告 28 組具名 K2 支援 ID，得到 **38 筆必要資料**，使用其中
12 組局部 K2 支援、30 份不同六支援配置。原 18 筆關係全部保留索引：
10 筆無相容支援，其餘八筆如下，不能將 18×28 稱為來源數。

| 原 ID | h/e/d | F_z(q) | 相容支援數 | p₁／p₂ |
| ---: | --- | --- | ---: | --- |
| 67 | 0/1/2 | {0} | 7 | 全 A/A |
| 84 | 0/1/2 | {0,2} | 3 | 全 A/A |
| 101 | 0/1/2 | {0,3} | 5 | 全 A/A |
| 169 | 1/0/2 | {1} | 7 | 全 A/A |
| 186 | 1/0/2 | {1,2} | 3 | 全 A/A |
| 203 | 1/0/2 | {1,3} | 5 | 全 A/A |
| 254 | 2/1/0 | {2,3} | 4 | 全 A/A |
| 305 | 2/0/1 | {2,3} | 4 | 全 A/A |

對同一分量的 actual support S 及任意列 β，若 σ 將 q|S 搬到 β|S，
則整份 ordered relation 由同一 σ 搬運，故 F(β)=σF(q)。沒有此置換
時，只使用上界：F(β) 容量不超過原接點數，且受逐色固定 β(S) 的
全部色置換保持。此上界保留整份 F 的所有候選，不宣稱每個候選可實現，
不將 q 的 singleton 容量擅自搬成 target 的 singleton 容量。

對每份候選 F_z′、F_w′，在同一 β、同一色框計算

\[
E_z=U\setminus F_z',\quad
E_w=U\setminus\{\beta(s_h),\beta(s_d)\}\setminus F_w',\quad
X=U\setminus\{\beta_i\},\quad Y=U\setminus\{\beta_j,\beta_k\}.
\]

mixed 關係沿用前報告的精確式，F_* 為空或 Y×{e′}，其中
{e′}=X∖Y、|Y|=2、Y⊂X。逐份核對

\[
(E_z\times E_w)\setminus(\Delta\cup F_*)\ne\varnothing. \tag{5}
\]

每個接受見證另外保存原 (z,w,u,v) 的同一個著色 tuple，直接檢查
zw、wu、uv、vz、**zu** 及全部 root／mixed boundary 邊。所選 root 色
不在完整 F 中，依 F 的精確定義，各原 unary 就存在一份同時避開該色
的完整 tuple 及 coloring；不同分量只在固定這個共同 root pair 後接合。
這些局部 tuples 不冒充整張任意大小來源的顯式 coloring。

**38 筆全部接受兩列，76 個查詢沒有未決項。** 每份資料兩種 C_z 接點
方向均保留；證明不依賴選擇其一。沒有使用 T4 acceptance 或另作 K5
排除；不把必要支援表的非空當成可實現性。

例如原 ID 67 的支援
(S_z,S_w,s_h,s_d,i,{j,k})=(01,234,0,4,2,12)：p₁ 下整分量換色給
F_z={0}、F_w={3}，可取 (z,w,u,v)=(1,2,3,2)。p₂ 下 S_w 只見 1、2，
容量一與交換 0、3 迫使 F_w⊆{1,2}，故 w=3 永遠可用；F_z={0}，
可取 (1,3,0,3)。後一列用的是完整集合上界，沒有獨立任選原分量的 target 關係。

## 5. 反射、出口接合與停止點

ρ(i)=3−i mod5、π=(0 1)，對全部原附件、禁色及同一 boundary row 同時
搬運，Tβ=π∘β∘ρ，則 Tq=q。38 筆支援在此反射下封閉；原 z,w,u,v
身份保持，接點次序整體反向。checker 再核對 76 個反射 target 查詢，
以及每份局部見證的全部 24 個共同色框搬運。沒有只正規化 target。

若此 G 是雙缺失來源 Σ(G₀)=Ω∖{p,q} 的 minimal q-core M，則刪邊繼承
給 Σ(M)⊇Ω∖{p,q}。共同對齊 q 後，p 為 p₁ 或 p₂，因此本輪強迫 M
接受 p、仍拒絕 q，即 Σ(M)=Ω∖{q}。這新增
[條件式出口](c5_single_sided_exit.md#1-定義與定理) 的第八類核心；完整 Σ
使用了來源雙缺失與繼承，不由一般來源的兩列接受單獨推出。

本輪完成 t_w=2、(1) 的支援／環序與雙列分離，沒有完成整個共鄰端點型。
**下一窄入口是 t_w=1、(2) 的 36 筆**：同一原 diamond 外側含 C_z、
C_w、w-spoke、u、v；先保留兩份二接點完整關係與同圖支援，再用飽和
雙禁色的原 bridge／逐塊支援，處理必要的來源排除或指定分離。
t_w=1、(1,1)，t_w=0 兩型、其他 mixed、非相鄰 roots、degree≥6 與
一般出口仍保留；不重開唯一 degree-5 枚舉。

## 6. 證書與重播

[checker](../scripts/c5_adjacent_degree5_mixed_edge_shared_t2.py)、
[JSON](../artifacts/c5_adjacent_degree5_mixed_edge_shared_t2/observations.json) 與
[38 筆表](../artifacts/c5_adjacent_degree5_mixed_edge_shared_t2/support_table.md)
保存 source／直接輸入 SHA256、全部 280 份幾何、18 筆原 ID 的支援集合、
38 筆有序接點與原落點、完整禁色集合上界、root／mixed witnesses 及反射 ID。
checker 另核對允許共享端點的正控制、w-spoke 落進 C_z 開弧的負控制，
以及真的有間隙的支援；不以最短弧或整段填滿取代 actual supports。

```bash
python3 scripts/c5_adjacent_degree5_mixed_edge_shared_t2.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared.py --check
python3 scripts/c5_adjacent_degree5_singleton_long_arc.py --check
python3 scripts/c5_adjacent_degree5_shared_singleton.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際驗證與未重跑範圍見 [本輪紀錄](history/2026-09-28-adjacent-mixed-edge-shared-t2.md)。
`lake build` 不表示上述 annulus、外部 Gallai 定理或跨列接合已 Lean 化。
