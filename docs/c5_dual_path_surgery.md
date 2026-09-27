---
docgraph:
  id: c5.dual-path-surgery
  family:
    - c5
  requires:
    - c5.single-spoke-two-two
---
# 同一完整染色的三組雙色路徑：有序切口重接與 record 110

2026-09-27。接續 [邊位置對座標 §5](c5_edge_pair_coordinates.md#5-計數層與下一個真正的橋接)
提出的共同路徑問題；研究優先序見 [HANDOFF](HANDOFF.md)。

**本輪結果：** 證明任意大小三價 dual 上的一步精確重接公式，並給出同一張
induced-C5 disk 圖上的反例：兩份完整染色有相同邊界色列、相同三份邊界配對，
交換同色對、同端點的實際路徑後，卻得到不同配對。因此三份邊界配對**不是**
可決定後繼的 state。反例的初始配對恰滿足 record 110 的全部 α 配對限制；
其中一份交換後違反新共同限制，另一份通過。

record 110 仍未排除。本輪得到的是必要的有序接合等式，沒有證明它與兩份
原 bridge 路徑／旁支接線矛盾。證據為紙面證明＋固定既有圖的 Python 重播；
未新增 Lean theorem，也沒有重新枚舉來源圖。

## 1. 同圖、同染色與共同切口

設 T 是有限連通 plane near-triangulation，外框是有序 C5；容許平行邊。
固定**一份完整** proper 四色染色 f，色值取 F₂²。每條 primal 邊 uv 的
dual 色為 f(u) xor f(v)∈{1,2,3}。刪去 dual 的外面頂點，將五個 boundary
half-edges 的端點記為 e0,…,e4。每個內部 dual 頂點各接一條 1、2、3 邊。
這裡的 e_i 是 **primal 邊位置**，不是原 boundary 頂點 b_i。

任取不同色 a,b,c，令 S 是 {a,b} 子圖的一個**完整**路徑分量，端點在
boundary。沿實際方向記內部頂點為 v0,…,v_(m−1)，並保留每条路徑邊的
名字及 a/b 交替次序。每個 v_i 的第三條邊色為 c，將此位置記為 port t_i。

刪除 S 的全部邊，但保留各 v_i 的 c 邊。在剩餘的 {a,c} 子圖中，度數一
的點恰為全部 t_i 與不在 S 上的 {a,c} boundary ends。將每條完整路徑壓成
一個配對，得到 E_ac；另外記錄未碰 ports 的閉圈。以**同一份剩餘圖**
對 {b,c} 做同樣處理，得到 E_bc。即使一條 c 邊直接連兩個 S 頂點，仍是
一份有具名兩端的外部片段，不可丟掉。

令 L_a、L_b 分別是 S 上原 a 邊、原 b 邊所形成的局部連結：內邊連接
相鄰 t_i，兩端的 half-edge 連接 e_s 或 e_t。它們是共同有序路徑上的
兩份交替 partial matchings，不是可以另外挑選的配對。

若 S 是閉圈，採循環次序及相同定義，沒有 e_s、e_t。無內部頂點的退化
strand 則直接保留其兩端連結；以下公式也成立。

## 2. 精確交換公式與共同必要限制

記 Tr 為沿度數至多二的**多重圖**追蹤完整 strands，輸出其 boundary
配對與閉圈；平行連結不可合成一條邊。令 M_xy 為原 boundary matching。
在 S 上交換 a、b 後，有

\[
\begin{aligned}
M_{ab}'&=M_{ab},\\
M_{ac}'&=\operatorname{Tr}(E_{ac}\cup L_b)|_{\partial},\\
M_{bc}'&=\operatorname{Tr}(E_{bc}\cup L_a)|_{\partial}.
\end{aligned}
\]

交換前的兩列則為 Tr(E_ac∪L_a)、Tr(E_bc∪L_b)。在兩個混合色對中，
原來不碰 ports 的閉圈照常保留；重接也可能新生或消除閉圈。

**證明。** S 每個內點原有一條 a 邊、一條 b 邊，兩者都在 S；唯一的 c 邊
不改色。S 外所有邊也不改色。因此新的 {a,c} 子圖恰由舊的外部 {a,c}
片段，加上 S 內原 b 邊組成。將外部度二路徑逐條壓縮不改變端點連通性，
也不會把不同片段的端點混同，故得到第二式；第三式相同。{a,b} 子圖的
邊集合完全不變，給第一式。論證不限制路徑長度，也不依賴平面性。□

同一 disk 染色還必須同時滿足以下限制。

1. **同一順序與側別。** S 是 boundary-to-boundary crosscut 時，兩份 E
   使用同一個 t0,…,t_(m−1) 次序，且每個 t_i 的 c 邊在 S 的同一側。
   切開 S 得兩個 disks；每份外部片段只能連同側 ends，並且在該側的
   真實 boundary order 中非交錯。閉圈切口仍有共同側別，但不能把外側
   annulus 擅自視為 disk。
2. **同一批 c 邊。** E_ac、E_bc 的路徑可能共用 c 邊；這些邊有相同的
   實際兩端與 rotation。分別找到兩個合法配對，不能保證它們有同圖實現。
   證書的每個外部片段保留原 edge ids，不把共用邊當作兩份獨立資源。
3. **共同後繼。** 兩個混合色對都必須使用上式的同一 L_a、L_b 重接。
   交換後再逐對任選 noncrossing matching，不是合法的更新。
4. **內部閉圈。** 不碰外框的交換也可能改變另兩色對的邊界配對；不能因為
   當步的 boundary word 不變，就把它當作無作用。下一節及證書保留閉圈。

因此「有序 ports＋兩份實際 cut matchings＋L_a、L_b」足以決定**指定這
一步的 boundary 後繼**。它尚未被證明能重建下一條交換路徑所需的新 cut
matchings。若保留完整共同外部圖、edge identities 及 rotation，當然可以
在新染色重新切開；本輪沒有把這份任意大小資料壓成有限、可迭代的充分 state。

這與既有 [primal connectivity surgery](c5_kempe_connectivity.md) 的精神
一致，但本節處理 dual **邊色路徑**交換；不將它等同於一次 primal 頂點
Kempe swap，也不把既有 Lean theorem 冒稱為本節的新形式化證明。

## 3. 同一張圖、相同三配對、不同後繼

取既有 catalogue 的 mask 701，boundary 為 0,…,4，內點 5,…,8。除 C5
外，邊為

```
05 08 16 17 18 27 35 37 45 56 57 58 67 68.
```

其定向內面依序為

```
F0=018  F1=054  F2=085  F3=127  F4=168  F5=176
F6=237  F7=345  F8=357  F9=567  F10=586.
```

加上外面 43210，各 directed edge 恰出現一次，每個頂點的 rotation 是
單一 cycle，Euler characteristic 為 2；這給出具體 disk embedding。
boundary 沒有 chords。兩份完整染色為

\[
f_A=(0,1,0,2,3,1,0,3,2),\qquad
f_B=(0,1,0,2,3,1,2,3,3).
\]

兩者 boundary 都是 α=01023，edge word 都是 11213，三份配對均為

| 色對 | 共同的交換前配對 |
| --- | --- |
| 12 | 03、12 |
| 13 | 04、13 |
| 23 | 24 |

此表及以下的 ij 指 e_i↔e_j。在兩份染色中都交換唯一的 23 boundary
path，端點是 e2、e4；但**實際路徑**依次為

```
A: e2–F6–F3–F5–F9–F8–F7–F1–e4
B: e2–F6–F3–F5–F4–F0–F2–F10–F9–F8–F7–F1–e4.
```

| 色對 | A 交換後 | B 交換後 |
| --- | --- | --- |
| 12 | 04、13 | 04、13 |
| 13 | **01、23** | **03、12** |
| 23 | 24 | 24 |

两者新 boundary word 同為 11312。可見同一張圖、同一邊界色框、同一對
色名與交換端點，再加全部三份 boundary matchings，仍不足以決定下一份
matchings。本例不主張連各色對的內部閉圈數也相同。

差異可以直接在 ports 上讀出。以各自路徑的內點依序命名 t0,t1,…，
新 13 路徑由 E_13 與舊色 2 的 L_2 交替接合：

| 染色 | 兩條新 13 路徑的 port 次序 |
| --- | --- |
| A | e0–t2–t1–e1；e2–t0–t4–t3–t6–t5–e3 |
| B | e0–t4–t3–t6–t5–t10–t9–e3；e1–t1–t2–t7–t8–t0–e2 |

完整 E、L、原 edge ids、共同兩側次序與重接所得閉圈都在證書中。這是
真實接合順序造成的差異，不是任選一份抽象非交錯配對。

## 4. 接回 record 110：必要的共同重接等式

沿用 [(2,2) 報告](c5_single_spoke_two_two.md) 的全部來源前提。假設 record
110 有來源 G，則 s=0、actual supports 為 (34,12)，且兩份具名有序關係為

\[
R_0(q)=\{(1,2),(2,1)\},\qquad R_1(q)=\{(2,3),(3,2)\}.
\]

G 接受 T4，拒絕 q=01012、p₁=01021、p₂=01212；邊位置對依次為
{3,4}、{2,3}、{0,4}。C0、C1 各有原奇數 bridge 路徑，C0 的 b3、b4
接線全在旁支；這些原圖資訊繼續保留，不以雙色配對代替兩份完整 R。

### 4.1 保留完整來源與一份染色的 auxiliary triangulation

由 T4 可取 G 的一份完整 α=01023 染色 f。先注意 G 必為 2-connected。
確實，令 B 是含 C5 的 maximal 2-connected block；其他枝塊可用既有 f
限制所得的染色，沿 articulation 逐一作全域色置換後接回，所以任意
B 的染色都延伸到 G。若有 B 外的邊 e，minimal q 保證 G−e 可延伸 q，
其 B 限制再接回所有原枝塊，就會染出 G 的 q，矛盾。G 連通且沒有孤點，
故沒有這些枝塊，G=B。

於是每個內面邊界是 simple cycle。沿用 [逐面補完引理](c5_count_cone_bridge.md#32-保留-c-的逐面補完)：
若某面有一點的兩鄰點異色，加入連接這兩鄰點的面內 diagonal，切下一個
proper triangle；否則顏色以週期二交替，放一個未用色 hub。反覆處理
得到保留 f 的 near-triangulation T_f，必要時容許平行邊。

此處**整份原 G 都作為具名子圖保留**，包括 z、兩分量、全部原 bridges
和實際 tethers。新增邊／點另作標記。Σ(T_f)⊆Σ(G)，故三個拒絕仍成立。
不假設補完保留全部 T4、degree 限制、minimality 或原分量關係；原 bridge
也不必仍是增廣圖的 bridge。不同初始 f 可以使用不同補完。以下所有交換
則在同一份已選定的 T_f 內進行，且其 coloring 限制回去一定仍是 G 的染色。

### 4.2 α 的三份配對全部固定

α 的 edge word 是 11213。四個 12 ends 是 0,1,2,3，只有兩種非交錯配對。
若配成 01、23，交換 23 那條路徑會把少數色位置對變成 {3,4}，得到 q；
故只能配成 03、12。同理，13 ends 的另一種配對 01、34，交換 34 路徑
會給 {2,3}=p₁；故只能配成 04、13。23 配對只有 24 一種。

因此每份 α 完整染色的共同狀態都必是

\[
\boxed{M_{12}=\{03,12\},\quad M_{13}=\{04,13\},\quad M_{23}=\{24\}.}
\]

本段用 q、p₁ 已可固定三份配對；checker 另外核對包含 p₂ 在內的全部
獨立 path-switch 結果。它不宣称三份配對本身有足夠排除力。

### 4.3 交換前後必须相容的兩個等式

在 α 染色中取唯一的 23 boundary path S（端點 24），交換後的 boundary
word 是 11312。再全域交換 dual 色 2、3，便對齊回 11213；這是 F₂² 的
可逆線性換色，對 primal 可取固定 0、1、交換 2、3。對齊後又是一份 α
染色，因此 §4.2 的三配對必全部恢復。換回交換後、尚未對齊的色框，得到

\[
\boxed{
\operatorname{Tr}(E_{12}\cup L_3)|_{\partial}=\{04,13\},\qquad
\operatorname{Tr}(E_{13}\cup L_2)|_{\partial}=\{03,12\}.
}
\]

這兩式必須與交換前的 Tr(E_12∪L_2)={03,12}、
Tr(E_13∪L_3)={04,13} **在同一組有序 ports、同一剩餘圖上同時成立**。
同樣地，任一不碰外框的雙色閉圈交換保持 α，因此交換後也必維持全部
三配對；上式就是可套到實際路徑的共同必要限制。

§3 的 A、B 都滿足初始框中三配對，A 違反第二個重接等式，B 通過兩式。
在 A 的第一次交換後，再交換實際 13 路徑 01，積分回 primal 得到

```
(0,3,0,3,2,1,0,2,2),
```

其 boundary 與 q 全域換色等價。證書保存這兩步的原邊及完整染色。
因此 A 的接合形式不可能出現在 record 110 的 α 補完中；B 僅通過這次
檢查，沒有被認證為可反覆存活。

**重要界線：** mask 701 接受 q，並不是 record 110 的來源。兩份控制
所證的是同初始配對仍有不同後繼，以及新共同限制可以讀取實際接合而
區分它們；它們不給 record 110 的實現或排除。

## 5. 證書、驗證與下一個窄問題

- [checker](../scripts/c5_dual_path_surgery.py)
- [完整 JSON 證書](../artifacts/c5_cells/dual_path_surgery.json)
- [本輪紀錄](history/2026-09-27-dual-path-surgery.md)

只從既有 132 個 witnesses 選取原本已為 induced-C5 triangulation 的 56
個圖；重建並驗證其定向面、單一頂點 rotation、connectedness 及 Euler
characteristic。這是既有圖的 embedding 核對，沒有生成新的圖 catalogue。
710 份完整染色（模全域 S4）共重播 3,550 次 boundary path 交換及 660 次
閉圈交換；8,420 個混合色對更新全部符合公式，4,210 次皆重新積分並核對
primal properness。全部 3,550 個 boundary cut 同時檢查兩份外部配對的
共同側別、實際切口環序與非交錯性。任意大小的充分一步更新由 §2 證明，
有限重播只是控制。

```bash
python3 scripts/c5_dual_path_surgery.py --check
python3 scripts/c5_edge_pair_coordinates.py --check
python3 scripts/c5_single_spoke_two_two.py --check
python3 scripts/check_docs.py
python3 tools/docgraph check
lake build
git diff --check
```

以上重播全部通過；`lake build` 完成 8,826 jobs，只有既有 linter warnings。
文件檢查為 181 頁／2,217 本地連結，DocGraph 為 0 errors／notes。build
不形式化本頁新證明；詳細執行範圍見本輪紀錄。研究輪結束時未 commit／push；發布狀態以 Git 為準。

下一個窄問題已縮成：利用 record 110 的**兩份原奇數 bridge 路徑與旁支
實際 tethers**，限制任一 α 補完所能產生的共同 E_12、E_13 及 L_2、L_3；
證明至少一份必違反 §4.3，或得到保留完整來源接線的新必要正常形。
不能改成獨立枚舉 cut matchings 後宣稱 disk 可實現；也不能假設一般
α coloring 的接合等於 §3 的任一控制。
record 110、一般 (2,2) 分離、有限可迭代 state 與 K∞=K≤5 仍未證。
