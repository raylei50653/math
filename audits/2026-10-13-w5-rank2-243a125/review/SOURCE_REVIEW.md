# 圈秩二來源信任鏈與獨立結構審閱

BASE `243a125a80e4d8de40957f59d8da0bdbc974cf69`。本檔是獨立紙面審閱，
不修改上游證據、正式 docs 或其他工作目錄。核讀使用者指定九個入口，並回到
`audits/2026-10-12-c5-deep-five-wheel-01a12ffa/REPORT.md` §§1–4 核對短環結論。
本檔先記來源與獨立推導；本輪最終採納範圍另見 `FINAL_REVIEW.md`。

## 1. 可以使用的前提及不能移植的前提

來源在**全部**目錄外 disk-C5 圖中先最小化內點，再最大化邊數。沿用共面正規形、
十二內點界及完整度數定理，可用：簡單、二連通、原 B chordless、原內面三角形、
原內點完整 degree 至少五、原邊界點 degree 至少四、沒有 occupied triangle、
每個 C4 的有界內部無頂點，以及 proper C5 的有界內部為空或恰一個 W5 中心。
令指定合法全內部 W5 的中心為 v、rim 為 U，則 B/U 十 pins 不交，U 內恰為 v
及五個三角面，`r=k−6≥7`。任取符合這個槽位的 W5 均適用，不能只對重新選輪成立。

完整全域最小性允許和任意合法、同原 B、保完整 Σ 的較小 disk 圖比較。代表不用
繼承三角化、最大邊數、degree≥5 或私人圈秩。反過來，較弱前提的實際圖也不能
冒充真正最小 933／941 來源。

本輪不加入 edge-critical、N2、ε=2、Gallai、私人圖連通或私人 degree≥5。
上游 4CT、普遍 screen、132 目錄、外部計數定理及 K≤12 的信任邊界仍保留。
沒有重播外部計算證書，沒有新增 Lean 定理。

## 2. B/U 附件界是分開證明的

對私人點 x，若接不相鄰 B 點 a,c，短 B 弧 a-b-c 與 x 形成 C4。
其內部清空、B 無 chord 及三角化迫對角線 bx；b 只餘 a,c,x 三鄰點，
違反原邊界 degree≥4。因此 x 在 B 上至多兩鄰点，兩者必相鄰。

若 x 接不相鄰 U 點 ui,uj，原 C4 `ui-v-uj-x-ui` 的兩側分别有 U 的非空開弧。
其有界側因此有頂點，違反 occupied-C4 排除。故 x 在 U 上亦至多兩個相鄰鄰點。
此處使用原中心、原 spokes 與原 rotation；不是把內圈 U 當外框而套 B 論證。

所以 `d_T(x)≤4`、`d_G(x)=d_F(x)+d_T(x)`。孤立私人點不可能；私人 leaf
恰有兩個 B 與兩個 U 鄰點，完整 degree 恰五。其原 link 中移去唯一私人鄰點
後，是含 B/U 的一條 terminal 路徑，必有異環相鄰 pair，因而給一個 BUP 面。

若 x 是原私人三角面的頂點且 `d_F(x)=2`，所有 terminal 附件同在另一側
link 路徑。完整 degree≥5 迫至少三個 terminal，兩環都出現，故也給 BUP 面。
若在這種三角根附私人樹，則以其非根 leaf 收費；不同根的樹互不相交。
這是計帳引理，沒有宣稱可刪枝或支援不變。

## 3. 對 rho=2 的獨立原面計數

令 c 包含所有私人分量與孤立點（孤立點已另排除），h 為 PPP 原三角面數，
a 為只有 B/U 的原三角面數，M 為 BUP 面數，p 為 B-U 邊數。
從 annulus Euler、全部原邊與全部原面重算：

```
e(A)=3r+20,   t(A)=2r+10,   e(F)=r−c+2;
M=2(c−2+h),   p=a+c−2+h;
e(P,B∪U)=2r+8+c−p;
Σ[x∈P] d_G(x)=4r+12−c−p;
r≤12−c−p=14−2c−a−h.
```

因此已有任意大小的普遍有限上界 `r≤11`；這一步不用預猜私人核心大小。
h 不得默認為零，也不能由圈秩一式只改一個常數而省略重算。

## 4. Essential 分支的獨立排除路線

若 F 含分隔 B/U 的 simple cycle，則 p=0，故 `a=M=0`、`c+h=2`。
每個私人 leaf 都給 M，故全部私人圖已等於其 2-core，沒有樹分量或附枝。

若 `c=1,h=1`，連通 rank-two 2-core 的分支點至多兩個：
`Σ(d_F−2)=2`，故僅一個四度分支點或兩個三度分支點。唯一 PPP 三角面的
三點至少一點 private degree 二，§2 迫 M>0，矛盾。

若 `c=2,h=0`，两個分量各是純單環。Contractible 私人環內不能藏另一
無 terminal 的完整 degree≥5 分量；若內部沒有分量，三角化迫原 PPP 面。
因此 h=0 迫兩環均 essential。它們在 annulus 中嵌套，中間區域無 B/U，
不能在不加兩分量之間私人邊的情況下三角化；矛盾。

這條路線對 essential cycle 與 contractible cycle 混合、各種相對嵌入位置
也有量詞覆蓋；不先假設所有私人環都 essential。

## 5. All-contractible 分支及 diamond 的剩餘幾何

所有私人 cycles contractible 時，F 的有界面沒有 terminal。
若其他私人分量浮在其中，其每點全部鄰點均私人，完整 degree≥5 不可能與總
圈秩二共存；否則原面三角化迫每個有界面是 PPP 原三角面。因此 `h=2`、`M=2c`。

依有限簡單圖 2-core 分類：兩個單環分量必為兩個三角環；figure-eight 的兩葉
必為三角環；barbell 的兩端也必為三角環。依序有六、四、四個互異非分支三角根。
各根以自己或附樹 leaf 收費，其他樹分量各給至少兩份 M，皆超過 M=2c。
Theta 的兩個 bounded faces 皆為三角形，三條 branch-to-branch paths 的長度
只能為 1,2,2；其原 2-core 是 diamond K4−e。

Diamond 兩 tips 已恰用兩份 M 收費，其他樹分量恰各兩份。因而 branchpoints
不可另接私人樹，tip 上只能接一条無分枝路徑，其他分量只能是路徑；否則出現
額外 leaves 超出 M。兩 branchpoints 各有 `d_F=3`，其外側 terminal link
不能跨 B/U（否則再給 M），故恰接某一環的兩相鄰 pins，完整 degree 恰五。

**兩 branchpoints 必接不同 terminal 環。** 設 p,q 是共享原邊、x,y 是 tips。
若 p,q 同接 X∈{B,U}，先不能共用 terminal t：pq 兩側原面第三點是 x,y，
所以其他 triangle pqt 的有界內部必含 x 或 y，違反 occupied triangle。
取不同 t∈N_X(p), s∈N_X(q)，原弧 `t-p-q-s` 是 annulus 內從 X 回到 X 的
proper crosscut。它把 annulus 切成一個 disk 與一個 annulus；另一邊界 Y
只在 annulus 側。x,y 位於 pq 的兩側，因此某 tip 及其全部附樹落在無 Y 的
disk 側。無附樹時該 tip 的 d_F=2 迫接 Y；有附樹時其 leaf 迫接 B/U，仍須 Y。
兩者均不能不穿原 crosscut 而實現。這個 argument 對 X=B/U 對稱，沒有更換
原外框或丟棄原中心。

Diamond 域另有 `r≤12−2c−a`，故 `r≥7` 迫 `c≤2`。
這些條件能作有限必要模板的起點；本檔本身不宣稱已交付其完整模板或染色結果。
不能因 branchpoints 不同環，就略過全部 terminal-only faces、B-U 邊、兩 tips
附路或另一私人路徑分量。完整模板須由原 rotation 恢復全部原邊。

## 6. 短環與保存強度防錯

C4 結論是「有界內部無頂點」，允許對角線。Diamond 外 C4 內只有共享對角邊，
正好符合該結論，不能只憑出現 C4 就排除 diamond。Proper C5 cap 定理也允許
一個五度中心；diamond branchpoints 的 link 可恰為這種 W5，不能把它誤判成
occupied-C5 禁止。若要以短環再排除，必交付實際 cycle、原 rotation 及嚴格內點。

保完整外框 Σ 只需 `pr_B R_A³=pr_B R_A′³`；保 R³ 才須保每個 B/U pin
及中心色的雙向 total full-lift 搬運。既有 prism 是前者，已有實際同 Σ 異 R³
控制。引用它必先證新必要域完整 Σ=1023，不能以圈秩一結果推測圈秩二相同。

真正最小 933／941 來源仍標 **not triggered**。紙面完備化約、有限必要模板、
較弱前提真圖控制及真正來源觸發分開記錄；零触發不構成來源排除證據。

## 7. 一個完備而有限的局部 no-go

Diamond 的兩個五度 branchpoints p,q 的 closed stars 聯集，有實際 C6 介面
`D=(x,b0,b1,y,u1,u0)`。原內部恰為 p,q；p 接 D 的 0,1,2,3，q 接 0,3,4,5，
另有原邊 pq。這個 cap 的全部 732 個 proper literal D assignments 中接受
300，拒絕 432，完整 lifts 共 312 份。全部 fibres 與反例保存在
`local_patch.json`，`python3 -B review/local_patch.py` 從頭重算（從 audit 根執行）。

**此 cap 沒有保完整 D 關係、至多一內點的普通簡單 disk 代表。**
九條可能的 boundary chords，每條都有一個原接受 assignment 把其端點染同色。
所以任何同關係代表都不能加入 chord。至多一內點的剩餘可能只有：保原 C6，
一個私人點接任意 D 子集；共 64 個 subsets，包括空鄰集（也涵蓋零內點關係）。
逐份都有完整 D assignment 證其接受關係不同。這個分類甚至沒有用平面性來
縮小 64 個候選，故足以完備排除合法子類。

此有限 no-go 的範圍只到**固定完整 C6 介面的二內點到一內點縮減**。
它完全不排除改动 annulus 其他部分、容許 U 色支援改變、僅保 B 投影 Σ 的
严格縮減。本輪應優先追求使用者允許的較弱目標，不把這個局部 no-go 提升為
一般代表障礙。它是 `triggered and holds` 的局部控制，仍未觸發最小來源。
