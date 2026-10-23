# 原C6／C7的群平均OR接合排除全部距四中心

2026-10-23；BASE `cb8f8593e273a7426ecadd59797a6e643cc4768e`。
固定[SOURCE_CONTRACT](../SOURCE_CONTRACT.md)的同一全域最小no4ct、完整Σ932、
h=4來源；全部二十份原有序C9 collar逐份保留。沒有在932內另取最小圖。

**新定理：原嚴格內點不存在距四C9雙接點。因此原內點若接兩個C9點，
恰為某條原C邊的面第三點。第三輪每collar的19模板只餘零距四pair。**
零pair來源、一般932、h≥5、smaller bad、K∞及Lean仍OPEN，共同k≥23不變。

## 1. 原圖分解及兩個／三個中心色

寫同一原induced C9為`C=(c0,...,c8)`，`I=V(H)\C`。繼承T2的原完整度數
`d_H(C)≥4,d_H(I)≥5`與接點距離只能1或4；第二輪已排三接點；第三輪已證
距四接點只能使用同一pair且至多兩原中心，兩中心必有原邊。
這些原來源前提的exact bytes分別凍結，沒有由控制圖重新證明。

反設有距四pair，旋轉記號令其為`{a,b}={c0,c4}`。第三輪的原分離給同一H
的實際induced C6／C7 cells：短弧用`u=(c1,c2,c3)`，長弧用`v=(c5,c6,c7,c8)`。
單中心x時，兩cell沿原路a-x-b相交。雙中心x、y時，x靠短弧，y靠長弧，
兩cell只交a、b；其間恰為原邊xy及兩個空原三角面axy、bxy。沒有跨cell
未知原邊、隱藏私有點或補完成本；所有其他原頂點都保留在所屬原cell。

固定anchors的literal colors `α,β`，令`K={0,1,2,3}\{α,β}`、`m=|K|`。
若α≠β，m=2；若α=β，m=3。記`F⁺κ(u)`、`F⁻κ(v)`為這兩個固定原cell
的全部full lifts，原中心色為κ。它們包括所有空fibres，並保留完整原頂點
color tuples。令`Aκ(u)=|F⁺κ(u)|`、`Bκ(v)=|F⁻κ(v)|`。

第三輪的集合雙射給原H的完整extension count

`X(u,v)=Σκ∈K Aκ(u) Bκ(v)`                            （單中心），(1)

`X(u,v)=Σκ,λ∈K,κ≠λ Aκ(u) Bλ(v)`                      （雙中心）。(2)

式(2)完整保留原xy邊的proper約束。每份product的共同原頂點都有同一literal
colors；各sector因原中心色不同互斥，其聯集正是同一原H的全full lifts。
原X本身只能得rank≤2或3；本輪不把它當rank one。

## 2. 對整份原cell作群平均，才得到rank one

令G為固定α、β並任意置換K的**整體四色permutation群**，即S_m。
它作用於整份原cell full coloring，並固定原有序anchors。它不移動任何
原點、邊、rotation或附件。對同一原cell的全體colorings有真正full-lift雙射

`Bλ(gv)=B_(g⁻¹λ)(v)`；A也有同樣等變性。                (3)

定義群和（不除群大小）

`Y(u,v)=Σg∈G X(u,g v)`。                               (4)

這是對同一原H中**整條**C9 literal row的counts求和。式(1)–(3)給

`Y(u,v)=(m−1)! · (Σκ Aκ(u)) · (Σλ Bλ(v))`              （單中心），(5)

`Y(u,v)=(m−1)(m−1)! · (Σκ Aκ(u)) · (Σλ Bλ(v))`        （雙中心）。(6)

例如固定κ後，g⁻¹κ遍歷K且每色出現(m−1)!次；雙中心另有m−1個可選λ。
不同anchors的兩係數都是1；相同anchors的係數分別2、4。若v有非平凡
stabilizer，群元素可能給**重複字詞**，仍逐群元素計算，絕不以distinct
字詞集合取代群和；(5)–(6)完整保留這些multiplicities。

由同一H的全域color symmetry，Y在u的G軌道及v的G軌道上各自為常數。
因此它下降到短／長原弧G軌道索引的矩陣`Y_[u],[v]`。式(5)–(6)證這個
**群和後**矩陣是非負outer product，故其正支持必是rectangle。

不同anchors可一次whole-S4搬到(0,1)：短弧有20份literal words、10個G軌道，
長弧有61份words、31個軌道，得10×31 folded grid。相同anchors一次搬到
(0,0)：短弧21份words、4個S3軌道，長弧60份words、10個軌道，得4×10 grid。
每條完整C9 row只在最後作一次whole-S4 row編碼；兩cell從未各自正規化。

## 3. Folded cell是原rows的OR，不是每列都正

固定一份folded cell([u],[v])。先選軌道代表u、v，在共同literal frame形成
全部整條原C9 rows `(α,u,β,g v)`，逐份作一次whole-S4編碼，去除重複**row
indices**後記其集合為`Ω([u],[v])`。這裡去重只用於support OR；(4)的count
群和仍保留全部群元素。

全部Ω在固定anchor模式下互不重疊：不同anchors覆蓋610個原C9 rows，
相同anchors覆蓋210個，合完整820列。由(4)的非負性，

`Y_[u],[v]>0 ⇔ 存在 p∈Ω([u],[v])，x_p>0`。             (7)

其中x_p是同一原H對固定literal代表的完整extension count。故folded正格
只要求**至少一份原row正**，不能把Ω內所有原rows加為正，也不能選一份
獨立來源見證代替原H。原X的非零2×2 minors仍可存在，與(5)–(7)完全相容。

## 4. 只在整個實際whole-Kempe orbit正時使用rectangle

令S為目前仍包含同一原H真實正支持的必要上界。入場S恰為對應原collar
凍結的annulus／whole-Kempe fixed point。原完整Σ932非空，故真正正支持
非空；不是假設S的每列皆正。各query入場大小為352／356／376。

若某原row p真正正，任一互補palette split的實際full H coloring給一份
完整boundary-component partition。它在固定C9的全部noncrossing options
中；任意子集的**完整實際分量**交換都留在同一H，所以其整個boundary orbit
O的每份row都正。對每份O原row，只可作一次whole-H color restoration，
使本pair anchors成(0,1)或(0,0)，其兩個cell仍同框。

對一個固定anchor模式，取O碰到的folded短弧座標集合L及長弧座標集合R。
每個座標都由O中真正正row見證。因此(5)–(7)迫

`∀l∈L ∀r∈R：存在 p∈Ω(l,r)，x_p>0`。                 (8)

若某整格`Ω(l,r)∩S=∅`，(8)與真正支持⊆S矛盾，這個完整orbit O便不可能。
另若O有任何原row不在S，它也不可能。注意：S上界自身不是rectangle，完全
不構成來源排除；只有一份必須全正的實際whole orbit迫(8)，且某**整個OR
cell**在當時S全空，才有矛盾。

因此對p的某個split，若**每個**完整可能orbit O都因上述兩種理由之一
不可能，便可刪p。每批只用入場S，同步刪除後再開始下一批。歸納可知
每步S都包含真實原H正支持。這個論證沒有挑不同的來源圖、逐次交換見證
或獨立的cell colorings來完成(8)。

## 5. 完整有限證書及獨立重播

`certificate.json.gz`保存全部20×9原collar／pair假設。每份共同支持證書
同時適用單／雙中心，合360份具名multiplicity假設。每份trace保留非空入場S、
每批before、全部row removals與當時所有failed splits、after及最終空支持。
checker對每個failed split量化**全部**whole options，逐份使用整個orbit，
不以挑選一個swap、分量邊際或格子平均取代。

獨立checker不import producer，從頭重建：

1. 820個proper C9 rows、十個原C5 rows；
2. 4862份noncrossing component partitions及49356份完整whole-Kempe options；
3. 二十原annulus的164000份fibres（151605空）及13990份full lifts；
4. **literal-first**列舉全部anchored C9 words，再求兩弧群軌道的18份OR maps；
5. 每批入場支持、每個row／split／完整orbit的當時必要失敗。

獨立重播得全部180個pair支持空，共920批、64800次**帶pair假設**的row
刪除。failed splits內有2185560次whole orbit缺row及11100次整格OR空的拒絕。
因真正Σ932非空，其原H支持不能被sound必要刪除刪空。故每個原pair假設
逐一矛盾；第三輪已涵蓋全部距四中心情形，遂得

`∀x∈I：N_H(x)∩C 若有兩點，必是原C相鄰兩點。`          (9)

原C3空cap再辨識這個x正是相應原邊面第三點t_i。無pair時本輪不套(1)–(8)，
沒有刪任何無條件C9 row。第三輪的19份模板保存在原case binding作入場
provenance；本輪排掉其中18份，剩每collar唯一零pair模板，共20份，並未排來源。

## 6. 原圖控制、multiplicity與狀態

凍結第三輪的兩張具名有向disk控制仍各有一／二中心。它們的geometry、
完整links、原面及小cap前提由原控制authority保管；本輪獨立由原邊重算
full lifts，完整比較兩原cell的sector Cartesian union與direct whole tuples。

不同anchors的全部1220份fibres（每圖536空），兩圖各2000 lifts；相同anchors
各1260份fibres，單中心354空／2772 lifts、雙中心90空／5544 lifts。每份
空／非空fibre都比較。群和後的10×31／4×10矩陣逐格滿足(5)–(6)，全部
2×2 minors為零；係數依次為1／2及1／4，包含非自由軌道的重複群像。

不同anchors下原raw count minors仍為`[[4,2],[4,6]]`、`[[4,6],[4,2]]`，
行列式±16；把raw矩陣當rank one的控制狀態為`counterexample`。本輪群和
與完整接合控制為`triggered and holds`。這兩圖沒有原B、完整Σ932、全域
最小性，完整來源狀態一律`not triggered`；它們不提供來源存在或來源排除。

正常／seed17唯讀重播相同；15項語義反控制拒絕漏OR選項、以AND冒充OR、
抹去群multiplicity、改batch前後、漏完整split／原case、抬高來源控制等。
18份immutable authority及六routing entry快照分開保管，live routing drift
獨立報告，不改前三輪或共享文件。一次producer在凍結後因routing欄位名
不合中止，尚未產生certificate；保留失敗receipt與frozen bytes，修正後
逐byte驗證既有freeze，再exclusive-create本certificate，無覆寫舊證書。

## 7. 零pair的原下一層Q與至少一個深點

這一步是(9)後的任意大小原rotation推論，不是另一個有限圖搜尋。令s_i為
**只接原c_i**的I點數。由(9)，c_i的完整H內側link依序為

`t_(i−1), z_(i,1),...,z_(i,s_i), t_i`，

其中z的順序取自同一原rotation。九個t互異；每個z只接自己c_i，故各段
沒有重複z，也不與t alias。原有界面皆三角形，link相鄰點間的原邊全存在。
九段接成簡單原圈

`Q=(t0,z_(1,1),...,t1,z_(2,1),...,t8,z_(0,1),...)`，

長度`|Q|=9+s`，`s=Σs_i`。九個原C邊面與這九個原link扇區構成完整annulus，
外框C、內框Q；所有C鄰點恰在Q。原圖`J=H−C`因此是以Q為外框的原三角
disk。Q可能有弦，本輪**不宣稱Q induced**。所有不接C的原點在Q嚴格內部，
全部原邊、原面、attachment與rotation都留在J或該annulus。

每個t_i恰刪兩個C鄰點，故`d_J(t_i)≥3`；每個z恰刪一個，故`d_J(z)≥4`；
其餘原點degree≥5。若Q內沒有點，J就是沒有內點的多邊形三角剖分，必有
degree2耳點，與全部Q點的完整J-degree≥3矛盾。因此

`Q內至少一個原點完全不接C； m≥10+s，亦即 k≥19+s。`     (10)

這是邊界負擔s的局部條件界；不提高共同k≥23。certificate的`new_k_bound=false`
也只表示沒有新的共同數值下界。原`d_H(c_i)=4+s_i`，下一輪可從這一份原
Q與完整annulus接續，不需再保留19種距四模板。

## 8. 停止點

全部原距四接點已排；仍未排零pair h=4、一般932或h≥5。沒有新較小bad、
K∞、Lean或普遍四色可染性。下一窄義務是同一原Q、九個t_i與全部single
contacts的完整relation／可回填化約；Q長度可變且可能有弦，不能改成固定
小輪、抹掉single contacts或借用不同來源的邊際可行性。
