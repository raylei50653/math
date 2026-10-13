# 圈秩三 essential 分支：獨立紙面審查

BASE：`45bc1c3dc9dacaee1b10df9d64f1c6a27bb0e954`。
本審查直接由凍結的圈秩二 `STRUCTURE.md`／`TOPOLOGY.md` 所列原面、
完整 degree 及 attachment 前提重新推導；沒有把圈秩二結論機械外推。
本檔只處理存在私人 essential cycle 的圈秩三來源，不處理全部
contractible 圈秩三來源，也不宣稱圈秩至少四。

## 1. 計帳及 connectedness

保留全部原私人點的 induced plane 圖 `F=G[P]`，寫 `r=|P|`、`c=c(F)`、
`rho=e(F)-r+c`。由原 annulus 三角化獨立重算：

\[
e(F)=r-c+\rho,\quad
M=2(c-\rho+h),\quad p=a+c-\rho+h,
\]

\[
e(T,P)=2r+10+c-\rho-p,\qquad
\sum_{x\in P}d_G(x)=4r+10-c+\rho-p.
\]

`F` 有恰 `rho` 個 bounded faces。若存在 essential cycle，連通的 `U`
位於其中恰一面；每個其他 bounded face 必是原 PPP 三角面，故
`h=rho-1`。Jordan 分隔給 `p=0`，於是 `0=a+c-1`。
因 `a≥0,c≥1`，恰有 `a=0,c=1,M=0`。
這一步先證連通，未預設連通。

私人 leaf 由完整 `d_G≥5` 與各環最多兩個附件，必同時有兩個 B、兩個 U
附件；原 link 中必產生 BUP 面。因此 `M=0` 排除所有 leaves。
孤立私人點早由 `d_G≤4` 排除，所以每個私人點 `d_F≥2`，並有

\[
\sum_{x\in P}(d_F(x)-2)=2\rho-2.
\]

取 `rho=3` 得 excess 恰四，`h=2`，並由完整 degree 和上游 `r≥7` 得
`7≤r≤12`。這是原來源的普遍大小界；不依賴有限染色成功。

## 2. 兩三角面確實迫 diamond 加一條 tip 路徑

若原 PPP 三角面的頂點 `x` 有 `d_F(x)=2`，兩私人邊的一個 sector 是該
三角面，全部 terminal 鄰點只能在另一個 link 區間。
完整 `d_G(x)≥5` 迫至少三 terminal 鄰点，因此 B/U 都出現；該區間至少
一個相鄰 B/U pair 產生 M 面。這與 `M=0` 矛盾。
故兩 PPP 三角面的每個頂點均有 `d_F≥3`。

excess 四迫它們的頂點聯集至多四點。兩個不同三角面不可能恰有相同
三個頂點：在有限簡單 plane 圖中，同一 C3 兩側同為面會令該連通分量
只有此 C3，與已證 `c=1,rho=3` 衝突。
所以兩面恰共享一條原邊，頂點聯集恰四點；這四點各 `d_F=3`，其餘
私人點各 `d_F=2`。

把共享邊端點寫為 `qB,qU`，另兩 tips 為 `x,y`。兩個共享邊端點的
三條私人邊已由 diamond 用盡，不能再接其他私人邊。`x,y` 在 diamond
中各 degree 二，因此各尚有一條私人邊。其餘私人點全 degree 二；
連通性及此度數序列迫剩餘邊恰是一條 x-y 路徑，不能另有 cycle 分量
或附枝。故完整 F 是 `K4` 中 `xy` 邊的一個 subdivision；沒有刪除原邊。

原兩 PPP 面固定其 embedding。另兩 F 面的邊界各為該 x-y 路徑加上
`x-qB-y` 或 `x-qU-y`，一個含 B，另一個含 U；各 cycle 長 `r-1≥6`。
兩個共享邊端點分別只有 B 或 U 可作 terminal 鄰點，據此才命名
`qB,qU`。它們各 `d_F=3`，所以各恰接對應環上的兩個相鄰 pins，
完整 degree 恰五。

這不是 occupied-C4 矛盾：diamond 外 C4 內只有共享 diagonal，無頂點；
兩個 essential cycles 已至少六長。僅憑本節不能直接排除來源。

## 3. 原附件的完整循環編码

令 x-y 路徑為 `z0=x,...,z_(n-1)=y`，`n=r-2∈{5,...,10}`。
沿路徑的一個共同平面方向，在兩側分別記當前 pins `(b_j,u_k)`。
每個 `z_i` 在 B 側至少有一附件：該側 incident 私人邊的原三角面必有
B 作第三點；U 側同理。每側的全部 terminal 鄰點是連續 fan，而附件
上界限制 fan 恰為一個 pin 或兩個相鄰 pins。

因此唯一需要的局部資料是
`(deltaB_i,deltaU_i)∈{0,1}²`：接當前 pin，若 delta=1 再接下一 pin，
然後更新當前 index。每條私人路徑邊兩側的第三點，是該步更新後的
B pin 和 U pin。tips 的全部四個 letters 都可先保留；其他路徑內點
的完整 degree 是 `4+deltaB+deltaU`，故排除 `(0,0)`。

閉合一側經 `y-qB-x`，另一側經 `y-qU-x`；`qB,qU` 各消耗對應環的
一條原邊，其餘環邊恰由路徑 fan 消耗。因此精確要求

\[
\sum_i\delta B_i=\sum_i\delta U_i=4.
\]

這是總前進量五的一次繞行，不是 index mod 5 後只驗端點相等。
兩個 pins 可以共用而不前進；每條環邊恰用一次。此記錄保留原所有
framework 邊、diamond 邊、路徑邊、terminal 附件和面；沒有剩餘可跨面
添加的原邊。必要域可以保留違反其他尚未檢驗來源條件的模板。

直接枚舉上述 word 域的獨立計數為：

| r | 7 | 8 | 9 | 10 | 11 | 12 | 合計 |
|---|---:|---:|---:|---:|---:|---:|---:|
| words | 22 | 131 | 340 | 440 | 280 | 70 | 1,283 |

計數採 product 四種 letters，刪內部 `00`，保留兩 column sums 都四的
words。這只核對參數域大小，並非 source-realizability 或染色證明。

程式使用等價的循環 backbone 記號 `w0,w1,...,w_(n-1)`，把 `w0-w1`
gap 替成 diamond；故程式允許 `00` 的位置是 `0,1`。
本節的實際路徑次序則為 `w1,w2,...,w_(n-1),w0`，因此恰只有路徑兩端
可以 `00`。兩者以這個明確循環換序和相應原 pin maps 互轉，沒有漏掉
gap 位置，也沒有令另一個內部路徑點錯誤取得 tip 的 degree 豁免。

## 4. pins 的原標號與方向

把起始 pins 寫成 `(b0,u0)` 是編碼的座標選擇；對任一原來源必同時保存
由模板 pins 到原 pins 的明確 bijections `phi_B,phi_U`。
在兩原框採相同 ambient 循環方向的記號下，它們形如

\[
\phi_B(b_i)=b^{\rm src}_{\alpha+\epsilon i},\qquad
\phi_U(u_i)=u^{\rm src}_{\beta+\epsilon i},\qquad \epsilon\in\{1,-1\}.
\]

若來源原有序 U 採相反方向，先把這個既定方向差記入 `phi_U`；不能為
兩側獨立選擇 reflection。`alpha,beta` 可以不同，因它們各由原 x 的
fan 起點决定。這些 maps 重新標記同一張原圖，不是以相對位移替換附件。
先選哪個 tip 作 x 只改變編碼方向，word 域保留全部 words，故不需依賴
同構去重或固定 orientation 恰好涵蓋所有來源的額外假設。

對任一原 B 染色 `gamma`，模板上應檢驗的是
`gamma_template(b_i)=gamma(phi_B(b_i))`；之後才以單一全域 S4 顏色置換
轉成十列的固定 canonical row。若 `row(gamma_template)` 是該列，則
原來源的這一列延伸存在性等於模板的該列延伸存在性。
一般 mask 必按此 row permutation 拉回，不能把兩個已 independently
normalized 的 masks 直接當成原標號同一 relation。

若經完整十列驗證所得 mask 全為 `1023`，此全列集合在任一上述拉回下
仍是 `1023`，所以可以合法還原原 B 的全部十列。
這只處理完整 `Sigma(G)`；不表示保留 annulus 的具名 `(B,U)` cells、
`R³`、原 lifts、lift 數量或同槽位 attachment。U 的重新標記在補回全
spokes 後只作內點重標記，不能據此聲稱一個 annulus marked representative。

## 5. 採納條件與保留範圍

上面紙面化約及 word-domain 完備性通過獨立審查。
由這份化約排除來源所需的有限義務是：逐 word 重建
指定 B 外面及 U 空面、保留原所有邊及 rotation、補回同一中心和五條
spokes，再逐一檢驗完整十列的存在／不存在。若採直接矛盾證法，原來源
只可能是 933/941 的 D5 像，故完整 `Sigma=1023` 已排除目錄外來源，
不另需要 replacement representative。只有若另主張嚴格代表替換時，
才須驗證該代表是實際合法 disk-C5 圖且具有同一完整十列。

後續已閱讀 `structure/PROOF.md`、主程序及獨立程序原碼，並核對
`logs/independent.log` 的全部 1,283 words 完整重播 PASS：13,137,920 cells、
12,714,781 空 cells、730,480 A lifts、352,020 G lifts，所有完整 masks
均為 1023。独立程序從附件區間建原邊、從 rotation 走原面，以固定變量
順序直接列舉 A/G；沒有匯入主程序。`logs/negative.log` 另記錄漏 diamond
原邊、錯 U pin map、反轉 U 面及漏 A lift 各被兩個 validator 拒絕。
**最終審查 PASS：可採納 essential 圈秩三來源排除。** 此 reviewer 沒有
把上述整份可重播程序再重跑一次；已驗的重播記錄由本包獨立程序產生。

此審查不將零觸發控制當作來源排除。真正最小目錄外来源仍無實例，
其實例控制應維持 `not triggered`；條件排除如成立，來自完整來源前提、
本紙面覆蓋及有限必要域的逐列驗證。
全部 contractible 的圈秩三、任意圈秩至少四、一般同槽位 annulus 代表、
Lean 形式化及 `K_infinity=K_<=5` 仍各有獨立義務。
