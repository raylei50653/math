# ε=2：t=2 原四接點整型復用共同 active forest 排除

2026-10-03。**933／941 固定完整 Σ、edge-minimal induced-C₅ disk
來源，在 ε=2、唯一 degree-6 root、t=2 下，不可能有原接點分拆 `(4)`。**
這是整型來源排除，沒有用「無全 degree-4 真子核心」代替反證。
本線入口見 [Kempe 導覽](c5_kempe_guide.md)。

本頁復用 [t=1 四接點＋unary 報告](c5_excess_two_four_one.md) 的同一
原 incidence matrix、共同 D 係數、兩份固定原末端袋及完整 rooted
relation。新的兩條原 spokes 將支援限定在同一實際 sector；全部
200 份具名必要查詢，100 份由三禁色 K₅ 排除，其餘 100 份的非空
末端袋支援族都不能同時並排。Python 另核對 526,336 次完整五接點
接合及 5,120 份保留兩原 spokes 的 K₅ 控制。任意大小、tethers 及
平面次序仍由紙面證明承擔；沒有新 Lean theorem。

## 1. 原四接點的精確完整接合

G 有限簡單，B=(b₀,…,b₄) 是指定有序 induced-C₅ disk 外框。
有效內部 H 連通，r 完整 degree 六，其他內點完整 degree 四。
r 的兩條不同原 spokes 是 rb_s、rb_t，s<t；H−r=C 連通，
P=(x₀,x₁,x₂,x₃) 是四個不同、有序的原接點。保留同一原 C、全部
實際 boundary 附件、ownership、環序、嵌入及字面四色框 U={0,1,2,3}。

固定 proper boundary row q，令

\[
R_C(q)=\{(f(x_0),f(x_1),f(x_2),f(x_3)):
 f\text{ 是原 C 的完整 boundary-list coloring}\},\qquad
F_C(q)=\bigcap_{p\in R_C(q)}\operatorname{set}(p).
\]

刪去 r 後，每個接點都有 degree-list slack；C 連通，生成樹逆序
貪婪保證 R_C(q) 非空。全部五接點關係與 root 投影恰為

\[
\begin{aligned}
\mathcal R_G(q)
 &=\{(a,p_0,p_1,p_2,p_3):p\in R_C(q),\\
 &\hspace{35mm}a\notin\{q_s,q_t,p_0,p_1,p_2,p_3\}\},\\
\operatorname{pr}_r\mathcal R_G(q)
 &=U\setminus\bigl(\{q_s,q_t\}\cup F_C(q)\bigr). \tag{1}
\end{aligned}
\]

式 (1) 對同一原完整 relation 存在量化；不是四個 endpoint marginals
的乘積。F_C 只在這個共同 root 色接合中作精確投影，不能反向重建 R_C。

## 2. 三禁色上界與每份拒絕列的共同 D

原 spoke 已使 B∪{r} 連通，所以
[外部連通 K₄ 引理](c5_degree5_tree_components.md) 對 C 適用，
不要求 root degree 五。原 C 的拒絕 degree lists 因而給 K₄-free
Gallai tree；blocks 只有 bridges 與 odd cycles，完整 palette 介面見
[degree-list 報告](c5_degree5_interfaces.md)。

若 |F_C(q)|≥3，取其中三色。沿用
[四接點三禁色證明](c5_no_spoke_exterior.md) §5 及
[原三份 palettes](c5_single_spoke_four.md) §2–5：共同 active tree
恰為兩個正 triangles、單負 bridge、零 contact arms。三條實際
boundary tethers 與 r 的任一原 spoke 給 K₅。此局部證明只需同一
C、三份拒絕 lists、原內點 degree 四及外部連通 hub；不需要 q 下的
整圖 minimality。因此任意 proper q 都有

\[
|F_C(q)|\le2. \tag{2}
\]

若 G 拒絕 singleton 列 q，式 (1) 與 (2) 迫 q_s≠q_t；否则三個
root 色皆須屬 F_C，已矛盾。兩個不同 spoke 色時則精確有

\[
\boxed{F_C(q)=U\setminus\{q_s,q_t\}=\{D,a_q\}},\qquad D=3. \tag{3}
\]

所有三色 canonical rows 都在同一字面框中不用 D。Checker 保存
完整十列 target mask，並只以其拒絕列施加式 (3)；未對其餘列新增
來源假設。省去 acceptance 限制只是放寬必要域，沒有改寫完整 Σ。

## 3. 全部拒絕列共用同一原 active forest

固定 q，對原 C 的 root=D、root=a_q 取两份拒絕 lists 及 Gallai
palettes。tightness 使每個原接點的 boundary 色避開 D、a_q，故

\[
\mathbf1_{M_D(v)}-\mathbf1_{M_{a_q}(v)}
 =\mathbf1_{v\in P}(\mathbf e_{a_q}-\mathbf e_D).
\]

令 I 是原 C 的 vertex–block incidence matrix。I 的欄線性獨立，
所以 palette 差異只有唯一係數向量 τ，滿足

\[
I\tau=\mathbf1_P,\qquad
\mathbf1_{S_K^D}-\mathbf1_{S_K^{a_q}}
 =\tau_K(\mathbf e_{a_q}-\mathbf e_D),\qquad \tau_K\in\{-1,0,1\}. \tag{4}
\]

只看 D membership，I 與右側均不隨 q 改變，因此全部拒絕列用
**同一 τ、同一原 active blocks 及同一原 bridge paths**。不能在
不同列各選同構但不同的原樹；此點直接復用
[t=1 報告](c5_excess_two_four_one.md) §3。

同頂點的正、負 active palettes 各至多一份；active incidence
forest 的葉點恰為原 P。若有 h 個非空分量，葉數公式給

\[
4=2h+\sum_{\text{active odd cycles }K}(|V(K)|-2). \tag{5}
\]

因此只有一棵含兩個 triangles 的連通樹，或兩條互不交的原 bridge
paths。所有 inactive 旁支及任意長度均保留。連通型包含兩 triangles
共一 cut vertex 的零長 connector，不能省去。

## 4. 連通型復用原圖 K₅

連通型的四條原 contact arms、兩 triangles、原 bridge connector
及實際 boundary tethers，正是 [t=1 報告](c5_excess_two_four_one.md)
§4 的兩種構造。每個非 shared-cut triangle 頂點已使用三條原邊，
剩餘原邊直達 B，或進入沒有其他 contact 的 inactive 支路。若支路
不碰 B，slack-list coloring 及整體色置換可拼回被拒絕 lists，故其
實際 tether 必存在。不同選定頂點的 tether 內部互不交。

兩 triangles 不交時，取第一個 triangle 的兩條 contact arms 為
A、A′，其第三點 x 為 X；Z 含 r、connector 除 x 外的部分、第二
triangle 及另兩條 arms；O 含 B 及第一個 triangle 的三條 tethers
除起點外的部分。五組的十對鄰接由原 triangle、原 contacts、原
connector、三條 tethers 及任一 rb_s／rb_t 給出。

共 cut x 時寫 triangles 為 {a,b,x}、{c,d,x}。取 a、b 完整 arms
為 A、A′，X={x,c}，Z={r}∪d 的完整 arm，O 含 B 及 a、b、c 的
三條實際 tethers。X–Z 用原 cd，其餘鄰接同前，亦得 K₅。
這些角色名稱不重排原 R_C 的有序四接點。

兩條原 spokes 都留在 G；構造只需其中一條提供 Z–O。合併 B
只用來反證 planarity，不宣稱這個 minor 操作保留 Σ。

## 5. 兩原 paths 給兩份固定末端袋

餘下兩條 active paths 均只含原 bridges。C 內的唯一 connector
在每條 path 上各只碰一個頂點。各選遠離 connector 的一個原
contact x，切掉其第一條 active bridge，取含 x 的原連通分量 V_x。
兩份 V₀、V₁ 因而固定、互不交，且各恰含一個原 contact。全部
inactive 旁支及實際 boundary 附件仍在袋中；不用包含另一條
active path 的中央袋。

令 E_x(q) 是 V_x 中、尚未扣 root 色及被切 bridge 鄰色前，x 的
完整可延拓色集。只有 x 接 r，所以 root=D／a_q 時 x 的色集恰為
E_x∖{D}／E_x∖{a_q}。x 是 active leaf，第一條 bridge 的兩份
palettes 分別為 {a_q}／{D}；切 bridge 的兩側均有 slack 可染，
原 C 的拒絕迫兩端各強迫同一 bridge 色。因此

\[
E_x(q)\setminus\{D\}=\{a_q\},\qquad
E_x(q)\setminus\{a_q\}=\{D\},\qquad
\boxed{E_x(q)=F_C(q)=\{D,a_q\}.} \tag{6}
\]

這直接復用 [t=1 末端袋證明](c5_excess_two_four_one.md) §5。
式 (6) 是每份固定原袋的完整 rooted relation，沒有把整個四接點
C 當成 binary，也沒有忘記中央袋的其餘 contacts。

## 6. 同一兩-spoke sector 的固定支援族不能並排

兩條原 spokes 把 disk 分成兩個 closed sectors；框弧包含兩端
b_s、b_t，長度之和五。C 連通且不能穿过 spokes，所以全部
實際支援在同一 sector。按原框方向固定其線性次序為
s,…,t 或 t,…,s；弧長一至四，不重複任何框點。

兩份原袋各經自己的原 contact 邊接 r，內部互不交。在這個固定
sector 內，它們的實際支援 T₀、T₁ 必有不交開內部的 hulls：

\[
\max I(T_0)\le\min I(T_1)
\quad\text{或}\quad
\max I(T_1)\le\min I(T_0). \tag{7}
\]

這是同一原嵌入的 crosscut 次序，沿用
[同 root 相容 lifts](c5_independent_support_capacity.md) §4.2；
共享框端點允許。不能把一份袋改用跨越另一個原 spoke sector 的
補弧來縮短 hull，也沒有將 sector 中間的位置新增為實際附件。

若 π 固定 q(T_x)，原 V_x 的完整 coloring 置換迫 πE_x(q)=E_x(q)；
若 p|T_x=πq|T_x，則 E_x(p)=πE_x(q)。因此兩份袋的固定實際
支援都必屬於同一族：逐拒絕列通過穩定子，逐列對通過全部 S₄
alignments，全部列用同一 T_x。Checker 復用 t=1 的支援族函數，
另用全部 24 置換的獨立定義重算；此處 sector 序列皆無重複框點。

| 具名必要查詢 | 數目 | 排除原因 |
| --- | ---: | --- |
| 非相鄰 spoke pair × 兩 sectors × 十個 target 像 | 100 | 至少一份拒絕列有相同 spoke 色，違反三禁色 K₅ |
| 相鄰 spoke pair × 兩 sectors × 十個 target 像 | 100 | 固定末端袋支援族非空，但無兩份滿足式 (7) |
| 全部存活 | 0 | 整型 `(4)` 排除 |

每份最後支援族都包含整個所選 sector，故不是由空 relation 排除。
來源矛盾是同一原 C 中的兩份固定袋須同時存在，卻不能在同一
原 sector 放入其兩份實際支援。這裡不需要另用來源碰齊全部 B
來迫兩原 spokes 相鄰；所有二十份 spoke／sector 選擇均已核對。

## 7. 證書、重播與停止點

[Checker](../scripts/c5_excess_two_two_spoke_four.py) 與
[artifact](../artifacts/c5_excess_two_two_spoke_four/observations.json) 保存
200 份完整 target／原 spoke／原 sector 記錄、三禁色見證或逐步
固定支援族、100 份非空最終族及原線性 hulls。明留 non-D-pair
guard；正控制在 q=01012、包絡 0123、E={2,3} 時容許 01、23 兩份
並排支援，避免將任何兩份袋都誤判為不可放入。

5,120 份原圖 minor 控制涵蓋十種兩原 spokes、任選其中一條作
hub、shared cut 及 connector 長度 1／2／3、四臂各長度 0／1、
直接／細分 tethers 及共同／不同框末端。80 份代表保存全部原邊及
五組十鄰接，其餘以具名參數域及 digest 綁定。全部 root 完整 degree
六；省去未用旁支的 skeleton 不宣稱是完整 degree-list 来源。
正控制分別刪任一 spoke 仍保留指定 minor；負控制拒絕兩 spokes
都缺失、必要 shared-case 鄰接缺失與 branch sets 重疊。

全部 256 份 singleton 四接點 relations、32,640 份二 tuple
relations 及十六種字面 spoke 色對，逐完整 tuple 核對式 (1)，共
526,336 次五接點接合。另有完整 relation 被 endpoint marginals
錯誤放行的負控制。一般非空 R_C 的公式由式 (1) 證明承擔，這些
抽象 relations 不宣稱有 disk 實現。

```bash
python3 scripts/c5_excess_two_two_spoke_four.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_two_spoke_four.py --check
python3 scripts/c5_excess_two_four_one.py --check
python3 scripts/c5_single_spoke_four.py --check
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

任意大小共同 forest、tether 抽取及 sector 的平面次序屬紙面論證，
外部 degree-list 定理沿用指定依賴，Python 不形式化拓撲。本頁未
提高共同 ε≥2，下述其餘來源未由這一分支涵蓋：其他 t、兩個
degree-5 roots（含 mixed）、一般候選排除與 `K∞=K≤5`。t=2 的
其他原分拆依 [Kempe 導覽](c5_kempe_guide.md) 的當前證書及停止點。
