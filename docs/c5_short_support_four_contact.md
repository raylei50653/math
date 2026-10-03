# 四原接點的短支援：未見二色 pair 亦不可能

2026-10-03。本頁保留四接點二禁色型的獨立證明；
[通用短支援引理](c5_short_support_singleton.md)另以三-hub 論證涵蓋它。**原 C 有四個不同 root contacts、所有 C 內點
完整 degree 四，actual boundary support 恰為一條 C₅ 框邊的兩端時，
若 C 外有原 r–B 路徑通往第三個框點，則 C 不能禁止該框邊未使用的
兩色。** 紙面證明不限 C 大小；Python 為有限 palettes／原邊 minor
控制，未新增 Lean theorem。

## 1. 同一來源與兩份 palettes

B 為指定有序 C₅ disk 外框，C 是 H−r 的原連通分量，四個不同原
接點 P 保持具名順序。每個 C 頂點在來源中的完整 degree 為四。
S_C={b_a,b_b} 是**全部實際支援**，且 b_ab_b 是原框邊。另有原路徑
L 從 r 到 b_h，h∉{a,b}，其內部避開 B、C。所有附件、旁支及原邊保持。

固定 proper boundary coloring q，令 q(b_a)=a、q(b_b)=b，未見兩色
為 c、d；此處 a、b、c、d 是色名，框點仍寫 b_a、b_b。反設原完整
四接點 relation R_C(q) 的禁色 F_C(q) 包含 {c,d}。

固定 r=c、r=d 各得不可著色 degree lists。沿用連通 slack 引理與
[degree-list 刻畫](c5_degree5_interfaces.md#2-gallai-結構tight-lists-與-block-palettes)，
兩者皆處處 tight，C 為 Gallai tree，並有 block palettes S_K^c、S_K^d。
B∪{r}∪L 是 C 外連通 hub，[既有 K₄ 排除](c5_degree5_tree_components.md#1-連通外框排除-degree-4-分量的-k4)
遂使 C 為 K₄-free。以下只剩 bridges 及 odd cycles，不假設全圖 minimal q。

比較兩份 palettes，沿用 [原 incidence 欄獨立性](c5_single_spoke_four.md#2-三組差異共用一個係數向量)
得唯一係數 τ_K∈{−1,0,1}，滿足

\[
I\tau=\mathbf1_P,\qquad
\mathbf1_{S_K^c}-\mathbf1_{S_K^d}=\tau_K(\mathbf e_d-\mathbf e_c).
\tag{1}
\]

τ≠0 的原 blocks 稱 active。其 incidence forest 的 vertex 葉點恰為
四個 P，非接點 active vertex 恰接一正一負 block。這些只比較同一
原 C、同一 q 的兩個 root 色，未逐分量重選色框。

## 2. 任何原 leaf bridge 都給 K₅

若 v 是 leaf bridge 的私有點，deg_C(v)=1。完整 degree 四及最多
三個外鄰 {r,b_a,b_b} 迫 v 同時鄰接這三點，故 v∈P。
固定 r=c 後 v 只能用 d。O=C−v 連通；刪原 leaf bridge 後其另一端
有 degree slack，所以 O 在原 lists 下可著色。若原鄰點可取非 d 色，
即可補回 v=d；原 C 拒絕，因此 O 的該鄰點在所有完整染色中皆為 d。

O 必實際碰 b_a、b_b：若不碰其中一點，交換那個未見的已用色與 d，
保持 root=c 及 O 的全部實際附件色，便破壞 d 的 singleton 強迫。
O 另含其餘三個原 contacts，故也接 r。

令 X={b_a}、Y={b_b}、Z={r}∪V(L)∪(B∖{b_a,b_b})。三者非空、
不交、連通且兩兩相鄰：補弧由相鄰框點的三點補集構成，L 把 r 接回。
五組 {v}、O、X、Y、Z 有十對鄰接。v–O 是原 leaf bridge，v 及 O
均接 X、Y、Z，故是來源 K₅ minor，矛盾。此步不假設另一 leaf block
也是 bridge；O 的兩點支援來自實際 singleton 強迫。

## 3. Inactive 原 leaf cycle 亦給 K₅

設一個原 leaf odd cycle 的 τ=0。其 private vertices 在式 (1) 中
只碰該 block，故都不是 contacts。每個 private vertex 內度二、完整
degree 四，便同時鄰接 b_a、b_b。取 cycle 上兩個相鄰的 private
vertices u,v；去掉它們後 O_C=C−{u,v} 仍連通，並含全部四個 contacts。

取 {u}、{v}、X={b_a}、Y={b_b}，以及
Z=O_C∪{r}∪V(L)∪(B∖{b_a,b_b})。Z 連通且與前四組不交。u,v
均接 X、Y，彼此有原 cycle 邊，並各經 cycle 的另一側接 Z；X–Y
是原框邊，X–Z、Y–Z 由補弧給出。因此再次得到 K₅。

## 4. 剩餘只可能兩個正 leaf triangles 與原 bridge 鏈

§2–3 後，每個原 leaf block 都是 active odd cycle。若 C 只有一個
block，式 (1) 迫該 cycle 全部頂點都是 contacts；四接點與 odd cycle
矛盾。若至少兩個 blocks，block-cut tree 至少有兩個 leaf blocks。

active 原 leaf cycle 的每個 private vertex 都是 contact，且 τ=+1。
每個 odd cycle 至少有兩個 private vertices；四個 contacts 迫使
**恰兩個原 leaf triangles，各有兩個 private contacts，全部 P 已用盡。**
active forest 不可能把兩個 triangles 分到不同分量：每個含 triangle
的 active tree 至少三葉，總共只有四葉。故它是一棵含兩個 triangles
的樹；葉數式

\[
4=2+\sum_{\text{active odd cycles }K}(|V(K)|-2)
\]

排除其他 active cycles。兩個正 triangles 不能直接共用 cut vertex，
否則該點同時有兩份正 palettes，式 (1) 亦給非法係數和二。
它們之間因此是原 active bridge 鏈，兩端的 bridge 皆為負。

原 block-cut tree 恰有兩葉，故是這條鏈；沒有未記錄的 inactive
旁支，否則會產生額外原 leaf block。也沒有中間 inactive odd cycle，
因它會隔斷已知連通的 active tree。這個論證明確避開「任一 active
leaf triangle 的 cut 點必接 bridge」的錯誤捷徑；未先排 leaf bridges
時，正 triangle 確實可能直接共 cut 接負 triangle 及其接點臂。

選一端 triangle {u,v,x}，u,v 為其原 contacts，x 是接向原 bridge
鏈的 cut vertex。正 triangle palettes 有
S_T^c={d,e}、S_T^d={c,e}，其中 e 是 a、b 的其中一色。兩個 private
點的第四條邊必直達另一色 f 的唯一框點；x 的負 bridge palettes
為 {c}、{d}，所以 x 的第四條邊亦直達同一 f 框點。因而 triangle
加 b_f 是原 K₄。

令 Z 包含 r、剩餘原 bridge 鏈及另一 triangle、L，以及 B∖{b_f}。
Z 連通且避開選定 triangle 及 b_f：其餘兩 contacts 把原 C 餘部接 r，
L 的落點不在 {b_a,b_b}，把 r 接到連通的四點框路徑。{u}、{v}、
{x}、{b_f}、Z 遂是 K₅：u、v 接 r，x 接原 bridge，b_f 接原框餘部。
所有情形皆矛盾，完成四原接點短支援的 unseen-pair 排除。

## 5. 有限控制與適用界線

[Checker](../scripts/c5_short_support_four_contact.py) 及
[artifact](../artifacts/c5_short_support_four_contact/observations.json) 核對
96 份 leaf-bridge 色穩定子、9 份雙 leaf-cycle 接點預算、240 份原邊
minor 控制。三種原圖構造保留四個具名 contacts、原相鄰框點、外部
路徑及全部 branch sets；兩-active-triangle 控制另核對每個 C 內點
完整 degree 四。12 份抽象兩-triangle 控制保留完整有序四接點 relation
及各 tuple 的完整染色 witness。三個負控制拒絕缺 bridge、缺實際附件
及重疊 branch sets。

```bash
python3 scripts/c5_short_support_four_contact.py --check
PYTHONHASHSEED=17 python3 scripts/c5_short_support_four_contact.py --check
python3 scripts/check_docs.py
git diff --check
```

任意大小的 Gallai、active incidence forest 及來源 minors 由紙面推導
承擔；有限 skeletons 不宣稱是完整 disk／list 來源。本頁只排除原
四接點在一條框邊支援的 unseen pair，不把四接點一般 pair 當作 binary，
也不單獨宣稱 (4,1) 整型來源已排除。
