# 任意小 cap 的完備測試入口與四度點完整計數分解

2026-10-13。只屬父隔離 audit；不修改舊來源或證書。
本文採用父包 frozen 的 [精確 cap 預算](../frozen/audits/2026-10-13-no4ct-generalization-6943561/cap/PROOF.md)
及 [原 induced C8／來源契約](../frozen/audits/2026-10-13-c5-no4ct-c8-6cafdfb/geometry/PROOF.md)。
兩個下述組合引理皆為直接紙面證明，不以四色定理、plantri 完備性或有限控制代替證明。

## 1. 同點集三角化足以測試任意 cap

令 F 為有限簡單平面圖，含固定有序 simple cycle C_b，所有其他點和邊都畫在
C_b 的閉 disk 內。允許 F 在內部有 disconnected components、isolated vertices、
bridges 或 cutvertices。令 h 為 C_b 外的私人頂點數。

**增廣引理。** 存在同一具名頂點集上的 F⁺，只在 C_b 的內側增加邊，保留
全部 F 邊與原 C_b rotation，使其外面恰為 C_b，且每個內面皆是三角形。
F⁺ 是 simple、2-connected，所有點度數至少二，私人點度數至少三。

**證明。** 在指定 disk 中取對加邊極大的 simple plane supergraph M；頂點集
固定且有限，所以這樣的 M 存在。若 M 不連通，某個面同時接觸兩個 components，
可在該面內加一條連接兩者的邊；孤點也是一個 component。因 C_b 已在同一
component，連線可選在 C_b 內。這違反極大性，故 M 連通。

若 v 是 cutvertex，在 v 的循環 rotation 中選相鄰兩條原邊 vu、vw，讓 u、w
落在 M−v 的不同 components。可在這兩邊之間的面角、沿 v 附近加入 uw。
u、w 不可能已有邊，否則屬於同一 component。若 v 在 C_b 上，C_b−v 全在
同一 component；其他 components 只在 C_b 內側，因此可選上述面角位於內側。
若 v 為私人點，所有面角都在 disk 內。故 M 沒有 cutvertex。因 b≥3，M
為 2-connected，每個面的 boundary walk 因而是 simple cycle。

若某內面 Q 長度至少四，在其環序選四點 u0,u1,u2,u3。兩條交錯對角線
u0u2、u1u3 不可能都已畫在 Q 面以外：Q 的另一側在球面上是 disk，連接
交錯端點的兩條互不相交弧違反 Jordan 分離。因此至少一條尚不存在，可畫入
Q 面內，仍違反極大性。所以全部內面是三角形。取 F⁺=M。私人點若只有
兩個鄰點，兩側三角面將重用同一三角形，迫整圖只有三點或其中一側不是
三角內面；而 C_b 已在私人點之外，兩種情況皆不成立。因此私人度至少三。
證畢。

**二點 cut 的位置。** 任意這樣的 simple 內面三角化 disk，其二點 cut
都恰為某條 boundary chord 的兩端；這不是額外排除的一類 disks。
設 `{u,v}` 是二點 cut。M−{u,v} 的每個 component 都接觸 u 的鄰點：
否則該 component 只可能經 v 接回其餘圖，使 v 已是一點 cut，矛盾。
若 u 為私人點，u 的鄰點按 rotation 形成一個由原三角面邊連成的 cycle；
刪去 v 至多刪此 cycle 一點，餘鄰點仍連通，故 M−{u,v} 只有一個
component，矛盾。因此 u 是 boundary 點；對 v 對稱應用同理，v 亦在
boundary。boundary 點 u 的鄰點在內側 rotation 形成一條原邊 path，
兩端為 u 的兩個 C_b 鄰點。若 v 不是此 path 的內部點，刪去 v 後 path
仍連通，又是矛盾。故 uv 是原邊、兩端在 C_b、且不是 C_b 邊，即 boundary
chord。反之，一條 boundary chord 的兩端刪除後，Jordan 分離使兩條
非空 boundary 開弧分開，確為二點 cut。

因此若生成器對 polygon triangulations 另要求「唯一的二點 cuts 是
boundary chords 的兩端」，此要求已由上述圖類本身推出，不會漏掉 cap。

在同一 literal 色框上，每一個 F⁺ full lift 也是 F 的 full lift，所以

\[
\Sigma_C(F^+)\subseteq\Sigma_C(F),\qquad
|V(F^+)|=b+h. \tag{1}
\]

於是對任意必要上界 U，若 F 拒絕 U，F⁺ 也拒絕 U：

\[
U\cap\Sigma_C(F)=\varnothing
\Longrightarrow U\cap\Sigma_C(F^+)=\varnothing. \tag{2}
\]

**完備測試推論。** 若已完整生成並檢查 b+h 點、外面長 b、simple、2-connected、
內面全三角的所有 *embedded* disks，且每份都與 U 相交，則所有 h 私人點的
simple disk caps 都與 U 相交。必須保留 distinguished outer face 並檢查原
C_b 所有具名環序對應；抽象 graph isomorphism 或只取一個未指派的外面
不能替代此要求。不同 h 要逐一覆蓋，除非另證 padding 包含關係。

本引理提供有限生成器需要覆蓋的精確類別。生成器的完備性、實際參數、
輸出數量及每份原列檢查，仍由父包的生成／驗證證據負責。

## 2. 可免費刪掉的私人低度點

若 F 有私人點 v，d_F(v)≤3，每份 F−v 完整四色染色都可接回 v。因此在固定
C、同一色框中

\[
\Sigma_C(F-v)=\Sigma_C(F). \tag{3}
\]

對每份固定的 F−v lift ψ，其可接回的**實際不同**顏色數恰為
`4−|ψ(N(v))|≥1`。故 (3) 只稱完整關係相等，不稱 fibres 數相等。
由此，私人頂點數最少的拒絕 cap 若存在，其每個私人點度至少四。
此判斷不要求 F 三角化，也沒有動任何具名 boundary pin。

## 3. 四度點給精確同列計數，而非獨立邊緣條件

令 F 為 §1 的三角化 disk，v 是私人四度點，按原 rotation 記鄰點為
u0,u1,u2,u3。四點互異，四條 ui u(i+1) 都是原邊。它們可能另有對角線。
固定一份 F−v 的**完整** literal 染色 ψ，記

\[
e_{02}(\psi)=[\psi(u0)=\psi(u2)],\qquad
e_{13}(\psi)=[\psi(u1)=\psi(u3)].
\]

由四條原 C4 邊 proper，ψ 在這四點使用二、三或四色，分別對應兩個、
一個或零個 opposite equality。故有逐份 lift 的精確恆等式

\[
\boxed{4-|\psi(\{u0,u1,u2,u3\})|
       =e_{02}(\psi)+e_{13}(\psi).} \tag{4}
\]

刪去 v 後，u0,u2 及 u1,u3 分別共面。對每個沒有原邊的 opposite pair，
在 v 原 face 中加入該 pair 的弧並收縮，定義 quotient Q02 或 Q13；平行
邊簡化。若該 pair 已有原邊，等色不可能，將該分支記為零，**不**把 loop
圖當成合法 cap。每一非零分支皆平面，且總頂點數恰比 F 少二。

quotient 的 boundary 可不再是 simple cycle：兩個原 C pins 可能成同一點。
必須保存原 C 到 quotient 的命名映射；只有在被合併原 pins 上同色的原 row
才可有 lift。若一個 boundary pin 與私人點合併，該 pin 的原色仍固定。
不能把這些 quotient 當作新的無標記 C_b 重新正規化。

令 x_F(p) 為固定原 literal row p 的私人全點延伸數。以 quotient pullback
定義 x_Q(p)，即計算同一 F−v 在指定 equality 下的完整延伸數，而合併的
私人色只算一次。將 (4) 對**同一 row p 下的全部 ψ** 求和可得

\[
\boxed{x_F(p)=x_{Q02}(p)+x_{Q13}(p)} \tag{5}
\]

對所有原 rows 都成立，包含零 fibres。兩個 equality 同時成立的 ψ 在右邊
貢獻二，恰等於接回 v 的兩種顏色；不得把重疊只算一次。特別地

\[
\Sigma_C(F)=\Sigma_C(Q02)\cup\Sigma_C(Q13). \tag{6}
\]

若 U 拒絕 F，便同時拒絕每一合法 quotient 分支。這給**同列**完整計數
分解，不把兩個分支的 lifts 拼成一份，也不宣稱 quotient 保留 simple C_b。
固定 cap 的 full lifts 可以用 (5) 作獨立交叉核對。

## 4. 對原最小來源的精確預算

採用 frozen 全域 C5 最小目錄外來源，原 H 有 k 個總頂點、induced 具名
C8 外面，且 `k≥19`。frozen 相對引理給每份至多 k+5 點的 loopless planar
圖可四色。

普通 h≤5 cap F 與 H 黏合恰有 k+h 點。在 §3 的一個非零分支中，原 H
也須隨具名 C pins 的 quotient 共同識別，原邊完整保留。因 C induced，
兩個非相鄰 C pins 沒有原 H 邊，故這種分支不額外造成 H loop；私人 cap
點也沒有 H 中的額外附件。quotient 在 cap 的外側 disk 操作，故整圖平面。
分支圖總頂點恰為

\[
\boxed{k+h-2\le k+3.} \tag{7}
\]

相對引理因此保證每個合法分支都有**一份共同完整**四色染色，拉回後同時
滿足該分支的全部 equality 與附件。這是一次實際 quotient，不是逐一共面
條件自動可同時實現。若兩個 opposite pairs 都有原邊，v 及其四鄰形成 K5，
與 F 平面性矛盾，因此至少有一個合法分支。

更一般地，若任一必要上界 U 含某份實際具名 planar disk W 的**整個**完整
關係，W 有 w 私人點，則任何 h 點 cap F 若滿足

\[
b+w+h\le k+5
\]

都不能拒絕 U：W∪_C F 的相對可染性給 `Σ(W)∩Σ(F)≠∅`，再用 `Σ(W)⊆U`。
此為一個可用的 cap 無效充分條件；本文並未為八份 U 建立這種 witness。

## 5. 同一 exterior 的 independent 識別最多省幾點

令 π 是原 C_b 上的一份 independent noncrossing partition，有 q 個 blocks。
這裡 independent 指任何 block 不含兩個原相鄰 C_b 點；noncrossing 指全部
blocks 可在同一 exterior disk 中以互不相交的 connected scaffolds 實現。
不同 blocks 若各自共面但不能共同畫入，不屬此引理。

每個 block 可選由其原 boundary vertices 組成的 noncrossing chord tree；
例如在 block 的 convex polygon 中取 fan。整份 π 的非交叉性保證不同
trees 也不相交。所有 trees 的聯集是一份 chord forest，其邊數為

\[
d=\sum_{B\in\pi}(|B|-1)=b-q.
\]

加上原 C_b 後，這 d 條 chords 將 disk 分成 d+1 個面。每個面至少含兩條
原 C_b 邊：零條會使其全部面邊構成 forest 內的 cycle；恰一條 uv 則其餘
forest 面邊给一條 u 到 v 的路，迫原相鄰點 u、v 屬同一 block。兩種情況
皆不可能。每條原 C_b 邊恰接觸一個 disk 內面，故

\[
\boxed{b\ge2(d+1),\qquad d\le\lfloor b/2\rfloor-1.} \tag{8}
\]

這個界可達到：取隔一點選出的 `⌊b/2⌋` 個 boundary 點作一個 block，
其餘單點 blocks。該 block independent，並可用其 polygon 內的樹連起。

對原 C8 得 `d≤3`。在 equality scaffolds 已全數收縮後，若共同 gadget
還有 a 個不在原 boundary images 中的新點，最終 H quotient 恰有
`k−d+a` 點。相對大小預算為 `a≤5+d`，從而

\[
\boxed{a\le8\quad(C8\text{，只識別原 boundary pins 的共同 exterior gadget}).}
\tag{9}
\]

此界給剩餘搜尋的明確大小：普通 cap 的五私人點完備測試沒有包含先省
一至三個原點、再用六至八個新點的共同 gadgets；即使 a≤5，也仍須處理
原 boundary map 的非單射性。本引理沒有把 quotient 重新當成 simple C8，
也沒有證明某個 signed dissection grammar 已生成全部 a≤8 gadgets。
若還操作原 H 的其他內點或另有已證合法的縮減，應重新計算，不能套此
只識別原 C8 pins 的 d≤3 界。

## 6. 有限控制與界線

[degree4_check.py](degree4_check.py) 直接枚舉四鄰 literal 指派、兩種可能
對角線條件及 v 的所有顏色，核對 (4)、空 fibres 及兩分支的重數。這是
局部恆等式的控制；任意 cap 增廣、平面 quotient 與相對來源引理的適用
仍由上述紙面證明承擔，沒有以有限結果形式化 topology。

普通 caps 的完備測試不覆蓋所有共同識別 gadgets。若先識別 original pins
淨省 d 點，再加 a 點，正確預算是 `a−d≤5`；這個族可有 a>5，而且邊界
可能重複，不能偷放進 §1 的 simple C8 disk 生成。以同一 U 得到的 cap
無排除也不給 U 本身可實現，不給實際 H 的完整關係或共同 count vector。

以上不改一般 `K∞=K≤5`、無界三支及八項真正來源實現的 OPEN 狀態；
沒有新增 Lean theorem、commit 或 push。
