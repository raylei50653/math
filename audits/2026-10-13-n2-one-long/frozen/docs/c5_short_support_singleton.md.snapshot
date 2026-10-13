# 短支援：兩／三個外部 hubs 的 Gallai K₅ 排除

**後續（2026-10-03）**：[t=0 全分拆報告 §2](c5_excess_two_no_spoke_complete.md#2-無-spoke-的真實外部-hub-與共同跨度)
核對無原 spoke 的適用範圍：同一原圖的外部路徑 L 亦恢復 K₄ 排除
所需的連通 hub，因此本頁兩／三 hub 證明不再需要額外直接 spoke。
下文保留原前提與控制；沒有改寫舊證書或宣稱所有無 spoke 圖皆有 L。

2026-10-03，接續 [完整接點介面](c5_degree5_interfaces.md)、
[同 root 支援跨度](c5_independent_support_capacity.md)及
[原路徑 frame-arc K₅](c5_single_spoke_frame_arc.md)。目前停止點及
整批來源分拆的結果見 [Kempe 導覽](c5_kempe_guide.md)。

**結論：原 degree-4 分量 C 的實際支援包含於相鄰兩框點 {a,b}，若
同一原圖另有避開 C 的 r–(B∖{a,b}) 路徑，則 C 的禁色集在每個
proper boundary row 都為空。** 原 root 至少有一條 spoke；接點數
不設上限。已見框色用兩-hub 引理排除，未見色用三-hub 引理排除。
所以任意接點數的短分量都不能成為非空禁色 carrier。

這是任意大小紙面 minor 證明，沿用外部 degree-list／Gallai 刻畫及
既有 K₄-block 排除；Python 核對具名有限 skeletons 的原邊、連通
branch sets 與十條鄰接。沒有圖 catalogue 搜尋、來源實現宣稱或新
Lean theorem。未見二色 pair 的排除有獨立三-hub 紙面證明，沒有把
binary 路徑定理直接套到四接點或更多接點。

## 1. 原圖、完整接點 relation 與外部路徑

G 有限簡單，B=(b₀,…,b₄) 是指定有序 induced-C₅ disk 外框。r 是
原內點且至少有一條原 spoke。C 是 H−r 的一份原連通分量，C 中
每點在完整 G 的 degree 恰四，原有序接點為 P=N(r)∩C，P 非空。
保留 C 的全部原邊、attachments、支援、ownership、環序及同一嵌入。

令相鄰原框點 a,b 滿足 N_B(C)⊆{a,b}。假設存在原簡單路徑

\[
L:r\leadsto h,\qquad h\in B\setminus\{a,b\},\qquad
V(L)\setminus\{r,h\}\subseteq H\setminus(C\cup\{r\}). \tag{1}
\]

L 可為原 spoke；否則其內部在另一份原分量。固定任一 proper boundary
coloring q，記完整有序 relation 及其特殊 root 投影為

\[
R_C(q)=\{(f(p))_{p\in P}:f\text{ 是原 }C\text{ 的完整合法染色}\},
\qquad F_C(q)=\bigcap_{t\in R_C(q)}\operatorname{set}(t). \tag{2}
\]

R_C 非空由接點 slack 的生成樹貪婪法得到。F_C 只描述所有接點必須
共同避開同一 root 色的接合，不代替完整 R_C；未取 marginals 或
逐分量重新命名色框。先證已見色部分

\[
\boxed{F_C(q)\cap\{q(a),q(b)\}=\varnothing.} \tag{3}
\]

第 4 節再排除所有未見色，得到 F_C(q)=∅。不要求 G 在 q 是 minimal，
也不要求 q 拒絕整份 G；結論是每個原分量、每列皆成立的必要條件。

在固定完整 Σ 為 933／941 的 edge-minimal 來源中，
[完整支援引理](c5_independent_support_capacity.md#11-degree-與完整支援)
使 G 碰齊五個框點。若 C 只碰 {a,b}，取任何外面的已碰框點 h：其
內部鄰點是 r，或位於另一原分量，故 (1) 自動存在。這個外路徑是
**同一原來源**的一部分；不能從不同核心或不同列的路徑拼湊。

## 2. Tightness 使同色 hub 合併保留 degree

反設 q(a)∈F_C(q)，固定 r 的色為 q(a)。C 的拒絕 lists 為

\[
M(v)=U_4\setminus\bigl(q(N_B(v))\cup
(\{q(a)\}\text{ if }v\in P\text{ else }\varnothing)\bigr).
\]

各 |M(v)|≥deg_C(v)。連通 degree-list 若有一點 slack，即可按生成樹
逆序貪婪染色，故拒絕使所有 lists tight。每點所有外鄰色因此互異；
特別是 **C 的同一點不能同時鄰接 r 與 a**。由外部 degree-list
刻畫，C 是 Gallai tree；r 的原 spoke 使 B∪{r} 連通，因此
[連通外框 K₄ 引理](c5_degree5_tree_components.md#1-連通外框排除-degree-4-分量的-k4)
排除 K₄ block。這個引理只用 C 的拒絕 lists 與原外部連通 hub，
不要求整份 G 是 minimal q-core。

在原 G 中取兩個互不相交的外部連通 branch sets

\[
X=\{b\},\qquad
Y=(B\setminus\{b\})\cup\{r\}\cup(V(L)\setminus\{h\}). \tag{4}
\]

B∖{b} 是原框路徑，含 a,h；L 使 r 接到它，所以 Y 連通。X、Y
避開整個 C 且互不相交，原邊 ab 給 X–Y 鄰接。刪除其他未用部分，
分別收縮 X、Y。C 的外鄰原本僅可能為 r,a,b；tightness 禁止同點
同接 r,a，故合併後 C 的每個頂點 degree **仍恰四**，沒有被合併
成重邊的兩條 incident 邊。C 的內部圖及其 blocks 完全沒動。

於是得到下一節的兩-hub 圖。此 contraction 只用於非平面性反證；
它會識別 boundary，不是保持完整 Σ 或 source relation 的操作。

## 3. 兩-hub Gallai 引理：五個 branch sets

**純圖引理。** 設 C 為非空連通 K₄-free Gallai tree，圖 J 的其餘
點恰為相鄰 X,Y，且每個 C 點在 J 的 degree 為四。則 J 含 K₅ minor。

因每個 C 點最多有兩個外鄰，min deg_C≥2。K₄-free Gallai blocks
只有 bridges 與 odd cycles；末端 block 不可能是 bridge，否則其
private vertex 內部 degree 為一。因此存在末端 odd cycle Q。
Q 至多一個 cut vertex，故能選兩個相鄰 private vertices u,w。
兩者原 deg_C 都是二，故各與 X,Y 相鄰。

令 O=C∖{u,w}。移去 cycle 上兩個相鄰 private vertices 後，餘下的
cycle 路徑非空且連通，仍含 Q 的 cut vertex（若有），所以 O 非空
連通。此外 O 含另一個**原 deg_C=2** 的頂點 v：

- C 只有一個 block 時，Q 的任何剩餘點即可。
- C 有多個 blocks 時，其 block-cut tree 至少有另一個末端 block；
  它亦是 odd cycle，任取其 private vertex 即可。

因此 O 同時鄰接 X,Y。Q 的另外兩條端邊使 O 分別鄰接 u,w；在
triangle 情形，兩邊可有同一個 O 端點。五個 branch sets 就是

\[
\{X\},\quad\{Y\},\quad\{u\},\quad\{w\},\quad O. \tag{5}
\]

前四組構成 K₄（XY、uw 及四條 hub 邊），O 連通並鄰接四組，故
得到 K₅ minor。這段涵蓋任意多 blocks、任意 odd cycle 長度及任意
bridges，不靠有限 skeleton 的覆蓋外推。

將 (5) 的 X,Y 展開為原圖 (4)，即得五組原 G 的互斥連通 branch
sets；所有十對鄰接都有原邊來源。與 G planar 矛盾，排除 q(a)。
交換具名框點 a,b，同理排除 q(b)，完成式 (3)。

## 4. 三-hub 引理排除未見色，接點數不設上限

假設 c∈F_C(q) 且 c∉{q(a),q(b)}。固定 r=c，仍有 tight 拒絕 lists
及 K₄-free Gallai 結構。這次取三個互不相交的外部 branch sets

\[
X=\{a\},\qquad Y=\{b\},\qquad
Z=(B\setminus\{a,b\})\cup\{r\}\cup V(L). \tag{6}
\]

a,b 相鄰，使 B∖{a,b} 是連通三點路徑；L 保證 Z 連通。原框邊
ab 及補弧兩端的框邊，使 X,Y,Z 兩兩相鄰。C 的三種可能外鄰 a,b,r
分別進入不同 hub，收縮後 C 的 degree 仍四。三個 hub 的指定色
q(a),q(b),c 互異，C 的原 lists 完全保留；其他被合併外點的原顏色
與 C 無接線，因此不影響這個局部 list 判定。這是 minor 反證的
輔助 hub 色，不聲稱保留原外部完整染色。

**三-hub 引理。** 設連通 K₄-free Gallai 圖 C 外有三個兩兩相鄰
的 hubs，C 每點完整 degree 四。固定三個 hub 為不同色；若 C 的
lists 不可著色，則整圖含 K₅ minor。

三個外鄰上限使 min deg_C≥1；singleton C 不可能完整 degree 四。
取一個末端 block，分兩種情形。

**末端 odd cycle。** Degree-list palettes 使其所有 private vertices
有同一二元 list。三 hub 色互異，而 private vertex 內部 degree 二，
所以它們各鄰接同一對 hubs X₁,X₂。取相鄰 private u,w，C′=C∖{u,w}
非空連通。若第三 hub X₃ 碰 C，它不碰 u,w，故 C′∪{X₃} 連通。
令 O=C′∪{X₃}，則 {X₁},{X₂},{u},{w},O 為 K₅ branch sets：O 經
hub triangle 鄰接 X₁,X₂，經 cycle 端邊鄰接 u,w。如果 X₃ 完全
不碰 C，刪它後正好符合第 3 節兩-hub 引理，亦得到 K₅。

**末端 bridge uv，u 是 private vertex。** u 在 C 中 degree 一，
所以它接到全部三 hubs，其 list 恰為唯一未用色 D。刪 uv 後，
C′=C∖{u} 連通且 v 有 list slack，故可著色。若有任何 coloring 令
v≠D，即能接回 u=D，與拒絕矛盾。因此 C′ 的完整 root domain 恰為
{D}。C′ 必碰到三個 hubs：若漏掉某 hub 的色 A，交換整份 C′
coloring 的 D,A 保持所有實際外部附件色，卻使 v=A，矛盾。於是
三個 hub singletons、{u}、C′ 是 K₅ branch sets；C′ 經 uv 鄰接 u，
並經實際附件鄰接全部 hubs。

兩種末端 block 已窮盡 K₄-free Gallai 結構，因此三-hub 引理成立。
展開原圖 (6) 的 hubs，得到原 G 的 K₅ minor，排除 c。結合 (3)，

\[
\boxed{F_C(q)=\varnothing\quad\text{對每個 proper }q.} \tag{7}
\]

證明只需一個被拒絕的 root 色，不要求 pair、固定三接點或四接點。
Binary 原 bridge-path K₅ 可作較窄的獨立既有證據，本定理不依賴
將其提升到任意接點數。

## 5. 固定原來源的跨度推論

完整 Σ edge-minimality 使每個原分量 C 有私有禁色見證：取其一條
原 contact 邊 e，G−e 新接受的列及 root 色 a 使 a∈F_C，而其他
原因子可避開 a。第 1 節已說明 933／941 的固定來源碰齊框點，故
短支援自動有外路徑 L。式 (7) 因而排除所有包含於相鄰兩點的支援。
空支援亦包含於任一框邊，單點支援包含於相鄰框邊，所以一併排除。

因此每份原分量的共同支援弧都滿足 ℓ_C≥2，**不分接點數**。
三份同一原來源的分量便需要至少六段框邊，與共同五段預算矛盾。
不同分量可用不同私有色見證；相加的是各份固定原支援的幾何下界，
不是不同列的負載。此推論還不足以排除只有一、兩份原分量的來源；
整批各分拆的具體結論見導覽及各報告。

## 6. 固定控制、重播與信任界線

[Checker](../scripts/c5_short_support_singleton.py)與
[artifact](../artifacts/c5_short_support_singleton/observations.json)保存：

- 八個原外鄰子集，逐一核對 tightness 恰禁止 r,a 同時出現，並
  保證 hub 合併不丟失 degree。
- 八個兩點支援穩定子不變禁色集；排除兩個已見色後恰剩空集及
  未見二色 pair，第 4 節再以三-hub 引理排除後者。
- 21 個手列 Gallai motifs：長度 3／5／7 的單 cycle、共享 cut
  vertex 的 cycles、不同 bridge 長度、三 cycle chain、三葉分叉。
  逐一驗證指定 blocks 的 incidence graph 是樹，及 min deg_C≥2。
  全部 degree-three 頂點的兩種 hub 接法共 135 份 skeletons，保存
  完整邊、所選 leaf cycle／private pair、O 中的原 degree-two 頂點
  和五份 K₅ branch sets／十條來源邊。
- 2,400 份回到原 C₅ 的 skeletons：十份有向框邊、五個原 spoke
  位置、三個外路徑終點、兩種路徑長度，以及 triangle／pentagon
  的具名原 contact 集。保存 actual support 與其兩點包絡的區別、
  完整原邊、L、r、spoke 及未收縮的 X,Y branch sets。
- 九個手列三-hub Gallai motifs 的 1,201 份完整 degree-four 接線：
  直接計算全部 list colorings，28 份拒絕配置逐一保存 leaf-bridge
  或 leaf-cycle 的 K₅ branch sets。其餘配置接受，沒有將一般三-hub
  圖都當成拒絕圖。Leaf-bridge 保存刪邊後完整染色及 root domain。
- 600 份未見 pair 的原 C₅ skeletons，C 是全接 root 的兩點／四點
  路徑；保存原 r、contacts、frame、spoke、L 及展開的三-hub K₅。

這些 skeletons 刻意呈現必然非平面的原接線；外部路徑內點未補滿
來源 degree，不宣稱是完整 degree-6 來源或 disk witnesses。有限
控制不證無界 Gallai 定理、不使用 planarity oracle；任意大小結論
由 §§1–4 及既有外部定理依賴承擔。未重新重播歷史 Gallai／K₄
分類的全部證書，亦未新增 Lean theorem。

```bash
python3 scripts/c5_short_support_singleton.py --check
PYTHONHASHSEED=17 python3 scripts/c5_short_support_singleton.py --check
```

兩次新 checker 重播已通過。整批 artifact、文件與既有 Lean 專案
驗證由本輪總研究紀錄保存；目前下一步見 [Kempe 導覽](c5_kempe_guide.md)。
