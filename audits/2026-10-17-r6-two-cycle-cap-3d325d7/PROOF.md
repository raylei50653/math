# 主動 f 七-cap：hub 接觸排除、全參考阻斷與 z-圈判準

2026-10-17；exclusive audit BASE `3d325d7197aa05815c71bedc52c1b253d736c7bb`。
本證明整合三份獨立紙證：[A 的來源幾何](A/PROOF.md)、
[B 的全參考與兩圈結構](B/PROOF.md)、[C 的實際共同色圈](C/PROOF.md)。
凍結身份見 [INPUTS.json](INPUTS.json)；舊 77 份研究封存保持原始 bytes。

## 1. 同一來源與量詞

保留原全域最少 completed-source 內點、次級最多邊的 no4ct C5 來源 G，
原有序外框 `(x,y,a,b,c)`、原 x,y,b 四度、r 六度、原支持
`S∈{932,933,941}`、全部原 rotation、私人頂點與接線。保留完整 U319
關係及空 fibres、全部 `(v,r,x,y,b)` 接回和原 r lifts，保持同一色框。
字面 `J=U/(s=t)`、`m=[s=t]`、`D=J*` 與
`e=(vw)*, f=(pq)*, g=(mz)*` 不變。不增加原 v 五度前提。

固定任意實際普通匹配 `M∈P101`，即 `e,g∈M, f∉M`。令 `F=D−M`，
假設其完整補圈之一 C 是含 f 的非面七圈，`X=V(C)`。
沿用前輪已證的實際兩星 disk K：兩中心 u,h，`u∈{p,q}` 在 J 四度，
h 是原/J 五度普通點，邊界是 induced Q5；五條 spokes 全在 M，唯一
內部 matching chord 為 `(uh)*`。這不要求 M 的奇圈數最小或 M 有偶補。

## 2. 任意大小的 cap–m 接觸排除

對上述任意 M、任意圖大小，

\[
N_J(m)\cap V(K)=\{z\},\qquad
\operatorname{dist}_D(X,V(\partial F_m))\ge2.
\]

此處 `∂F_m` 是 primal m 對應的整個 dual 面邊界。證明不需選 R，亦不需
限定補圈數。Q5 上緊鄰 z 的兩個點若接 m，實際三角面同時碰到 g 與一條
matching spoke，立即矛盾。其餘私人接觸按 p 的兩種中心位置，提升回原 G
成 induced C4 或 proper C5；前者違反空 cap 定理，後者迫 alpha/beta 的
完整 W5，再閉合原頂點 link 得內點度四，或 `q=5,c=5`，皆矛盾。
q 側在同一來源逐項反射，使用已成立的兩側圖非邊與 low-q/p 度數定理。
完整原圈、diagonal、面及 reflected 表見 [A](A/PROOF.md)。

任一 m-面 dual 頂點已在 X 外；若和 X 相鄰，對應外側三角面必為 `muv`，
其中 uv 是 Q5 rim 邊，要求 m 在 Q5 上有兩個不同鄰點，違反接觸排除。
這是完整 m-面的距離界，仍不推出交換區域分離。

## 3. 對全部偶補參考成立的阻斷

任取實際完美匹配 R，僅要求 `D−R` 的全部完整圈為偶圈；不限制 R 的標記型。
令 `L_R=D−(M∩R)=F∪(D−R)`。任一完整 L_R 分量 W 同時是若干完整
F 圈、若干完整 `D−R` 圈的聯集。因此

\[
|W|\equiv0\pmod2,\qquad \operatorname{odd}(F[W])\equiv0\pmod2.
\]

若 F 恰有兩個奇圈 C,C′，則對所有這樣的 R，它們都在同一區域；可另有偶圈。
若 g 至少一端在 C′ 且 `g∉R`，則整條 g 留在 L_R，故 `W_C(R)=W_g(R)`。
這包含每個實際 R100，不能以選另一份全異染色解除這項固定 M 阻斷。

若 F **總共恰有兩個完整圈**，即 `F=C7⊔O`，D 的階數為偶數迫 O 也奇。
前述同區結論涵蓋全部頂點，遂對每個偶補 R 都有 L_R 連通。特別地，

\[
\forall\chi\text{（實際完整全異染色）},\quad
W_C(R_{100}(\chi))=W_g(R_{100}(\chi))=V(D).
\]

所以固定這個 M 的最小化目標 `|W_g|=|V(D)|` 是常數。這不證明真正最小
來源存在這類 M，也不否定既有 SEP 條件下降定理；它阻止將 SEP 存在性
用作尚未排除的兩圈子類的通用後續義務。[B](B/PROOF.md) 保留全部量詞。

在這個兩完整圈子類，primal spanning 子圖 `P=(V(J),M*)` 有
`n` 點、`n−2` 邊、兩面。Euler 給 `κ(P)=3, β1(P)=1`。
五條實際 spokes 已給 `Q5⊆P`，故 Q5 是唯一簡單圈。
每個三角面恰有一條 P 邊，可將 P 邊標 0、其餘邊標 1，在球面積分得
`uv∈P iff σ(u)=σ(v)`。取 Q5 值 0；g 與實際面 mvw 迫
`σ(m)=σ(z)=0, σ(p)=σ(h)=σ(v)=σ(w)=1`。三個分量遂精確為：

| 分量 | 必含結構 | 完整結構 |
| --- | --- | --- |
| 中心 | p,h,ph | 完整 K2 |
| 外側 | v,w,vw | 樹；vw 是橋 |
| rim | Q5,m,z,mz | 單圈分量，唯一圈 Q5；mz 是從 z 接出的樹枝上的橋 |

q 中心時以 q 代 p。對每個偶補 R，其某份 Tait 染色將 R 作一個色類，
`S_R=(V(J),(M∩R)*)` 的圈均為偶圈。但 P 唯一圈 Q5 奇，故 S_R 為森林，
從 primal 再得 L_R 連通。這裡的 σ 與四色差值是不同賦值，不作混同。

## 4. 仍可能分離的分支：同一染色的指定 z-圈

固定一份實際完整全異染色，標準化 `e=α,f=β,g=γ`，取其實際 R100 色類 R。
對 p 中心，

\[
W_C(R)\ne W_g(R)
\quad\Longleftrightarrow\quad
S_R\text{ 有實際簡單圈經 z，將 rays }zm,zp\text{ 分在兩側。}
\]

q 中心改為 zm,zq。L_R 分量對應 embedded S_R 的面；f,g 中點分別落在
C 區域與 g 區域。路徑 `mid(mz)−z−p−mid(pq)` 沒有 S_R 邊，而
`deg_S(p)≤1`，所以分隔圈只能在 z 穿越該路徑。反之指定局部兩側條件
使路徑恰穿圈一次，即分隔兩中點。所有圈邊在**同一份**完整染色中皆為
α 差值，故此圈偶長；任意 M* 偶圈不保證有這種同時實現。

若 p 中心，這種分隔四圈不能用 zq：其餘 z 鄰點 A 在原 a 扇區，原
proper 五圈 `(a,A,B,q,b)` 的有界 cap 因 rotation 含 p，再由實際 ph 含 h，
違反 proper C5 至多一個內點。當 `c0=5`，c 扇區候選 zβ0 又因實際面
`mzβ0` 與 g∈M 被排，故任何分隔圈長至少六；q 中心、`a0=5` 有反射結論。
一般兩扇區四圈提升為原 C6，目前不排除。完整拓撲與短圈證明見 [C](C/PROOF.md)。

## 5. 優先修復義務與停止點

優先固定 `M∈P101, D−M=C7⊔O_odd` 及上述三分量結構，尋找一批實際、
彼此頂點不交的 M-交替圈 A，使

\[
e\notin E(\mathcal A),\qquad
f\in E(\mathcal A)\Longleftrightarrow g\in E(\mathcal A),\qquad
D-(M\triangle E(\mathcal A))\text{ 的全部完整圈皆偶。}
\]

前兩條恰在這種圈批次的範圍內保證 `N=M△E(A)∈P101∪P110`：e 保留，
f,g 或皆不翻或同翻。起始恰兩個奇圈，任何嚴格完整奇圈下降直接到零。
本輪沒有構造這批圈，亦沒有排除此子類的來源實現。

未落在上述全參考阻斷中的 M，再研究同一完整全異染色的 z-圈存在性。
若有額外偶圈也仍須檢查兩奇圈／g 同區條件，不能一律回到 SEP。
剩餘 active-f 七圈、其他奇補圈、H 相連修復、`W110+W101>0`、
`omega_e=0`、完整319、一般 T/T0 及主命題均 **OPEN**。
一般 K≤22、固定 r6 的 k≥25 與 completed-source 接回成本 k+5 不變。
無新 Lean theorem；有限控制及 custody 不代替以上任意大小紙證。
