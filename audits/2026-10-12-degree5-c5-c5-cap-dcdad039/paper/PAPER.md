# Task C：具名 C5＋C5 cap 分支的紙面來源契約

日期：2026-10-12。凍結 BASE：`bc7c0820e6b5e585869b8a59e04f52da0dad2d33`。
本文件只處理任務 C 的指定朝向；全部引用以本包 `frozen/` 中的副本為準。
有限核對的實際執行結果由本包 `REPORT.md` 與 checker 證書負責；下文的有限
閉合前提不因寫下而視為已驗證。

## 1. 前提與來源身份

沿用凍結的 `docs/c5_saturation_degree_bound.md` 及
`docs/c5_cofacial_normal_form.md` 的已採納前提：

* 圖類為有限簡單 plane disk 圖，外邊界是具名、有序的簡單 C5，允許 disk
  內的邊界 chords。完整關係只商掉全體色名置換，不商掉邊界位置。
* 目錄 \(K\) 恰有 132 個具名關係，每個有至多五內點的實際 disk 代表。
  目錄與 literal witnesses 是凍結輸入，並非本文件重新證明的枚舉完備性。
* 假設存在目錄外來源，在**所有**目錄外來源中全域最小化內點數，再於此
  內點數最大化邊數，選得 \(G\)。它簡單、二連通、外 C5 無 chord、內面皆
  三角形，且不存在內部含頂點的分離三角形。
* 上游必要 screen 的普遍性、其中的四色定理依賴，以及
  \(K_{\le12}=K\) 所用的外部 Dvořák–Lidický 定理，仍按上游文件分列。
  本文件不重播外部定理、不引入 edge-critical／edge-minimal 身份。

固定原圖上的同一組名稱

\[
B=(a,b,c,d,e),\qquad L=(a,x,c,y,z),\qquad
N_G(v)=\{a,x,c,y,z\}.
\]

其中 \(x,y,z,v\) 是互異的原內點；\(a,c\) 是僅有的 link 外框點。
\(L\) 按 \(v\) 的原 rotation 讀取。任務 C 的朝向條件是：在原嵌入中，
短外弧 \(a-b-c\) 與 link 長弧 \(a-z-y-c\) 相鄰，長外弧
\(c-d-e-a\) 與 link 短弧 \(a-x-c\) 相鄰。這是須由來源 rotation
確認的前提，不能只由 \(|L\cap B|=2\) 推出；另一朝向的 C4＋C6 不在此域。

## 2. 從原 rotation 得到兩個 disk

### 2.1 Link 與星形 disk

\(G\) 簡單且 \(\deg(v)=5\)，所以 rotation 中的五個鄰點互異。
\(v\) 是內點，每兩條相鄰 spokes 之間的面皆為三角面，因此原圖中實際存在

\[
ax,xc,cy,yz,za;
\qquad va,vx,vc,vy,vz.
\]

這五個三角面 \(vax,vxc,vcy,vyz,vza\) 的閉包按原 rotation 黏合。
每條 spoke 有且僅有這兩個相鄰面；每條 link 邊位於此聯集的邊界。
因此其聯集 \(S\) 是以簡單 Jordan C5 \(L\) 為邊界的閉 disk，
內部只有 \(v\)，沒有其他原頂點或邊。此敘述保持原面與 rotation，
沒有把五鄰點換成另一份抽象 C5。

實際上 \(L\) induced：若兩個非連續 link 頂點 \(u,w\) 有 chord，
該 chord 不能穿過已被五個面填滿的 \(S\) 內部。它與 \(vu,vw\) 組成
Jordan 三角形。在 \(v\) 的兩個扇區各至少有一個其他 link 鄰點，
所以三角形的有界內側包含原頂點，違反分離三角形排除。
有界內側不可能嚴格包含原外框點，故被刪除的頂點確為原內點；上游的
分離三角形排除適用。這裡只用全域最小來源的已採納性質。

### 2.2 Crosscut 證明與指定朝向

令 \(D\) 是原外 C5 所圍的閉 disk，令

\[
\alpha=a-x-c,\qquad \beta=a-z-y-c.
\]

兩條路徑都是 \(D\) 中的簡單 crosscut：端點為 \(a,c\)，其餘點
及邊的內部位於 \(\mathring D\)，且兩者內部不交。Jordan 分離先沿
\(\alpha\) 將 \(D\) 分成兩個閉 disk，邊界分別為
\(a-b-c-x-a\) 及 \(a-x-c-d-e-a\)。由本任務的原 rotation
朝向條件，\(\beta\) 的內部位於前一個 disk 的內部。

再以 \(\beta\) 切開前一個 disk，得到邊界為
\(a-b-c-y-z-a\) 的 disk 及邊界为 \(L\) 的 disk。後者就是
\(S\)：它的內側已完全由五個 incident triangular faces 填滿。
於是

\[
D=D_P\cup S\cup D_Q,
\quad \partial D_P=(a,b,c,y,z),
\quad \partial D_Q=(a,x,c,d,e).
\]

三者的開內部兩兩不交，交界精確為

\[
D_P\cap S=c-y-z-a,\quad
D_Q\cap S=a-x-c,\quad
D_P\cap D_Q=\{a,c\}.
\]

這證明兩 cap 是具簡單邊界的 disk，而不是 annulus 或帶重複 pins 的
boundary walk。也證明原圖的每個非星形支援都有確定的所在側。

### 2.3 原頂點、原邊、附件與 bridge 的 ownership

令 \(P,Q\) 分別為原圖限制於閉區域 \(D_P,D_Q\) 的子圖，保留原嵌入、
所有邊界邊與所有落在相應閉 disk 的原邊。令

\[
I_P=V(P)\setminus\{a,b,c,y,z\},\quad
I_Q=V(Q)\setminus\{a,x,c,d,e\},\quad
p=|I_P|,\ q=|I_Q|.
\]

完整頂點分割為

\[
V(G)=V(B)\;\dot\cup\;\{x,y,z,v\}
\;\dot\cup\;I_P\;\dot\cup\;I_Q,
\qquad k(G)=p+q+4.
\]

每條不在骨架 \(B\cup L\cup\{v\ell:\ell\in L\}\) 的原邊，其開邊
不能穿越該骨架，故唯一位於 \(\mathring D_P\) 或
\(\mathring D_Q\)。同理，刪骨架後每個連通分量及其全部 attachments
均歸同一 cap；只有 attachment 點可以位於該 cap 邊界。
對骨架的單邊 bridge 也以其實際開邊所在區域歸屬。這保留整個 bridge，
不依其 attachment 集的抽象形狀重新分配。

特別地，沒有 \(I_P\) 至 \(I_Q\)、\(I_P\) 至 \(x,v,d,e\)，或
\(I_Q\) 至 \(y,z,v,b\) 的邊，也沒有跨兩區域私有邊界點的邊。
cap 的內部構造可包含任意分量與割點；全圖替換的唯一介面就是該 cap
具名的五個邊界 pins。

原 \(P\) 的非邊界邊界 chord 只可能是 \(by,bz\)：\(ac\) 被外框
無 chord 排除，\(ay,cz\) 被 induced link 排除。
原 \(Q\) 的邊界 chord 只可能是 \(xd,xe\)：\(ac,ad,ce\) 被外框
無 chord 排除。以上沒有排除 cap 中連到私有內點的其他合法邊。

## 3. 全域最小性給出兩個目錄關係

\(P\) 是外框固定為 \((a,b,c,y,z)\) 的簡單 disk，內點數恰為 \(p\)；
\(Q\) 是外框固定為 \((a,x,c,d,e)\) 的簡單 disk，內點數恰為 \(q\)。
從 \(k(G)=p+q+4\) 得 \(p,q<k(G)\)。
若其中任一具名關係不在 \(K\)，該 cap 本身就是更少內點的目錄外來源，
違反在**所有**目錄外來源中的最小性。因此

\[
R_P=\Sigma(P)\in K,\qquad R_Q=\Sigma(Q)\in K.
\]

此步不要求 cap 繼承 \(G\) 的外點度數界、內點度數界、無 chord 或
edge-critical 身份。cap label 到位置的字典固定為
\((a,b,c,y,z)\mapsto(0,1,2,3,4)\) 及
\((a,x,c,d,e)\mapsto(0,1,2,3,4)\)，並非各自做 D5 正規化。

## 4. 全部十列、共同色框與 full lifts

色集合固定為 \(\mathcal C=\{0,1,2,3\}\)。凍結十列按位元 0 至 9 為：

| 位元 | 原外圈 \((A,B,C,D,E)\) |
| --- | --- |
| 0 | `01012` |
| 1 | `01021` |
| 2 | `01023` |
| 3 | `01201` |
| 4 | `01202` |
| 5 | `01203` |
| 6 | `01212` |
| 7 | `01213` |
| 8 | `01231` |
| 9 | `01232` |

對任意五元色指派 \(t\)，以 \(F_P(t)\) 表示 \(P\) 在該具名邊界
指派下的**全部** proper coloring，包含其所有私有內點；若不 proper 或
不可延伸則 \(F_P(t)=\varnothing\)。\(F_Q(t)\) 同定義。
以 \(\widehat R\) 表示關係 \(R\) 展開成共同色集合上的 proper
具名指派集合。於是 \(t\in\widehat R_P\) 等價於
\(F_P(t)\ne\varnothing\)，\(Q\) 同理。

對表中**每一列** \(\rho=(A,B,C,D,E)\)，定義完整 joint

\[
\begin{split}
\mathcal J_G(\rho)=\{&(X,Y,Z,V,f_P,f_Q):
X,Y,Z,V\in\mathcal C,\\
&f_P\in F_P(A,B,C,Y,Z),\quad
f_Q\in F_Q(A,X,C,D,E),\\
&V\notin\{A,X,C,Y,Z\}\}.
\end{split}
\tag{1}
\]

此式保留所有介面共同指派、所有 cap full lifts 與全部空 fibres。
它不只記錄單點／成對 marginals，也不把不同 \((X,Y,Z,V)\) 的成功
片段拼在一起。對每個共同指派，若任一 cap fibre 為空，該完整 fibre
便為空；中心沒有可用色時亦為空。

restriction 將每份原圖著色送到式 (1) 的唯一元素。反向則合併
\(f_P,f_Q\)，並給原 \(x,y,z,v\) 顏色 \(X,Y,Z,V\)。兩 cap 只在
\(a,c\) 相交且已用同一 \(A,C\)；與星形共享的五条 link 邊由 cap
properness 檢查；五條原 spokes 由最後一行檢查；§2.3 排除了未列出的
跨區域邊。因此反向恰為原全圖 proper coloring。這對十列逐列建立
原 full lifts 與 \(\mathcal J_G(\rho)\) 的雙向構造，實際上是雙射。

投影為介面 assignment 時，令

\[
J_{R_P,R_Q}(\rho)=\{(X,Y,Z,V):
(A,B,C,Y,Z)\in\widehat R_P,
(A,X,C,D,E)\in\widehat R_Q,
V\notin\{A,X,C,Y,Z\}\}.
\tag{2}
\]

則

\[
\rho\in\Sigma(G)
\iff\mathcal J_G(\rho)\ne\varnothing
\iff J_{R_P,R_Q}(\rho)\ne\varnothing.
\tag{3}
\]

沒有為未知的條件來源捏造數值 fibres；式 (1) 是任意大小來源的完整
symbolic fibre 公式。有限部分須將凍結 literal caps 的 fibres 實際保存
或以可無損展開的完整分塊編碼保存，不能僅保存式 (3) 的十 bit 投影。

## 5. 實際 disk 代表替換及兩向提升

任取凍結目錄中 \(R_P,R_Q\) 的實際代表 \(P',Q'\)，以既定位置字典
將其邊界命名為 \((a,b,c,y,z)\) 與 \((a,x,c,d,e)\)，並把兩組私有
內點重新命名為互異的 \(I'_P,I'_Q\)，且與九個骨架點不相混。
每個代表的 boundary-cycle embedding 可由 disk 的同胚嵌入對應的
\(D_P,D_Q\)；若必須反射，連同整份 cap 嵌入反射，邊界 labels
不交換。外框順序與原骨架 rotation 因此保留。

先沿 link seam **識別同一條幾何邊**，再接上同一個原具名星形：

\[
ax,xc,cy,yz,za,va,vx,vc,vy,vz.
\]

這一步的 link 邊是 cap 邊界與 star 的共同邊，並非另放一份平行邊。
兩 cap 的其他邊若有相同兩端點，因它們的共同頂點只有 \(a,c\)，
唯一可能的非 seam 重邊是兩份 \(ac\) chord。它們先按各 cap 原嵌入
放在互不相交的 cap 內部，形成平面 multigraph；若兩份都存在，約定
保留 \(P'\) 側的 \(ac\)，刪除 \(Q'\) 側那份。刪边仍保留原外框
\(B\) 的 outer face；proper coloring 只要求同一條 \(A\ne C\)，
所以刪除重複約束不改完整著色集合。

除 seam 的既定識別及此一可選 \(ac\) 簡化外，不識別不同骨架 labels，
不增加任何跨 cap 邊。新圖 \(H\) 因而是具指定簡單外 C5 \(B\) 的
實際簡單 plane disk 圖。它無須保留來源 \(G\) 的度數、三角化、
induced link 或無外框 chord 性質；這些不是 disk 目錄圖類的要求。

因代表完整關係相等，任一 \(t\in\widehat R_P\) 在 \(P\) 與
\(P'\) 都有 lift，\(Q\) 同理。對原 \(G\) 的一份全圖著色：

1. 保存其同一 \((A,B,C,D,E,X,Y,Z,V)\)；
2. 分別選取 \(P',Q'\) 在這些**相同具名邊界顏色**下的完整 lift；
3. 合併並保留 \(v\) 的顏色 \(V\)，得到 \(H\) 的全圖著色。

反向對 \(H\) 著色做同樣限制，再選取 \(P,Q\) 的 lifts，便得到
原 \(G\) 著色。若 \(Q'\) 的 \(ac\) 已被刪除，\(H\) 中保留的
\(P'\) 邊仍迫 \(A\ne C\)，故 restriction 仍是原未簡化 \(Q'\)
的 proper coloring，反向步驟不失效。

此構造逐列保留存在性，故

\[
\Sigma(H)=\Sigma(G)=
\{\rho:J_{R_P,R_Q}(\rho)\ne\varnothing\}.
\tag{4}
\]

只需任選相同邊界顏色的 lift，無需也不主張新舊 private fibres 有相同
大小或存在雙射。商掉色名時可把**整份** cap 著色用同一個 \(S_4\)
置換搬到既定指派；不能先各自更名再直接把不相同的 \(a,c\) 黏合。

內點數的完整帳目是

\[
k(H)=|I'_P|+|I'_Q|+4\le5+5+4=14.
\tag{5}
\]

四個額外內點恰是原 \(x,y,z,v\)；\(a,b,c,d,e\) 留在原外框。
因此不能只援引 \(K_{\le12}=K\) 判斷 \(\Sigma(H)\in K\)。
下一節的 132² 有限閉合核對是此分支的額外內容。

## 6. 有限閉合命題與原圖子域排除

**有限前提 FC。** 對全部 \((R_P,R_Q)\in K\times K\) 的
\(132^2=17,424\) 個**有序** pair，在全部十列上依式 (2) 的同一色框
共同枚舉，所得

\[
T(R_P,R_Q)=\{\rho:J_{R_P,R_Q}(\rho)\ne\varnothing\}
\]

全部屬於凍結目錄 \(K\)。每個 pair 也按 §5 由 literal witnesses
構成實際 disk 圖，且獨立 literal 全圖著色核對與 joint 相等；完整
fibres、空列及 cap／全圖 lifts 均可重播。

**條件排除定理。** 若凍結的上游前提與 FC 均成立，則全域最小目錄外
來源 \(G\) 不可能含有任務 C 指定的具名 C5＋C5 cap 位置。

**證明。** §2 在同一原圖上給出兩個具名 cap。§3 由全域最小性得到
\(R_P,R_Q\in K\)。§4–5 的十列完整關係與兩向 full lifts 給
\(\Sigma(G)=T(R_P,R_Q)\)。FC 使其屬於 \(K\)，與來源身份矛盾。□

此推論處理任意大小的原 \(G\)，但只處理已指定的 rotation 子域。
它不是由測試了 17,424 個小圖便自動推廣；推廣步驟正是 §2–5 的來源
分解、全域最小性與完整關係替換。

若 FC 失敗，需先以 §5 的實際嵌入和獨立 literal 著色確認該 pair。
合法且關係確在 \(K\) 外的結果是有限閉合命題的可實現反例，仍需依
任務逐項核對 screen。錯 label、錯朝向、未展開的色名、遺漏 spoke、
不合法嵌入或重邊處理錯誤則是 checker finding，不是數學反例。

## 7. 證據層與精確停止點

| 項目 | 本文件的狀態／界線 |
| --- | --- |
| 指定原 rotation 下的 C5＋C5 disk 分解、ownership、完整 fibres 公式 | 紙面條件證明已給；實際最小目錄外來源仍 `not triggered` |
| 由全域最小性推出兩 cap 關係在 K | 紙面條件證明已給；未使用 edge-critical 身份 |
| 任意目錄 cap pair 的合法 disk 黏合與兩向 lift | 紙面一般構造已給；數值核對見本包有限證書 |
| 全部 17,424 有序 pairs 閉合 | 本文件僅陳述 FC；是否 `triggered and holds` 或 `counterexample` 以有限 checker 實際結果為準 |
| 933／941 的實際全域最小目錄外來源 | `not triggered`；未實現、未從零觸發排除 |
| 新 Lean theorem | 未提供，亦未以現有 build 代替本證明 |

以下仍 **OPEN**：一般十三內點以上的目錄外來源、至少六個 degree-5
內點能否迫使任一個出現本位置、另一 C4＋C6 朝向、只碰一個外框點、
全內部 link、其他接觸分類、一般 pinned relation 壓縮及
\(K_\infty=K_{\le5}\)。本文件不依任務 A、B 的新結果，也不把有限
閉合核對提升為上述一般問題的解答。
