# 全內部 W5：十 pin 完整纖維與五個合法識別的精確縮減

2026-10-12。BASE：`e299ae987fcc4cdeb55dd41bede0a3a7c9d9db86`。
本輪接續 [全內部五輪入口](../../docs/c5_degree5_link_reductions.md)，
在獨立目錄交付完整關係縮減；凍結輸入及原 SHA256 見 [INPUTS](INPUTS.json)。

**已證的是同一原圖的完整染色消去與五個合法較小圖的帶符號重建。**
五個較小圖各自的外 C5 關係不足以執行重建，必須保存它們拉回同一原圖後的
完整染色及重疊。這尚不是普通 disk 關係的正聯集縮減，亦未證一般五輪可縮減
或 `K∞=K≤5`。原共用文件及歷史證書未改動。

## 1. 精確來源及具名介面

固定有限簡單 plane disk 圖 G，原外框依序為
\(B=(b_0,b_1,b_2,b_3,b_4)\)。取原內點 v，要求

\[
N_G(v)=U=\{u_0,u_1,u_2,u_3,u_4\},\qquad U\cap B=\varnothing.
\]

U 依原旋轉形成 induced C5，五個面 \(vu_iu_{i+1}\) 填滿其有界內側，
其中沒有其他頂點或邊。所有下標模五。刪去 v 得 H；指定 U 內側為空五邊面，
其餘原圖位於 B、U 之間。保留全部原邊、旋轉、附件、分量、bridges 及 ownership。
若 H 不具有這個具名嵌入槽位，下面代數仍可成立，但不能宣稱局部平面識別合法。

上述前提由上游最小目錄外來源的全內部五輪定理條件性供應；本輪代數定理本身
不需要最小性、degree-list、edge-critical 或 N2 身份。沒有提供實際最小目錄外來源。

共用色集 \(C=\{0,1,2,3\}\)。固定外框十列的順序為

```text
01012,01021,01023,01201,01202,01203,01212,01213,01231,01232
```

每列 beta 使用其 literal 色名；全圖只能共同作 S4 搬運。不得另行正規化 U。
令

\[
J_H(\beta,\tau)=\{\eta:V(H)\to C:\eta\text{ proper},\quad
\eta(B)=\beta,\ \eta(U)=\tau\},\quad\tau\in C^5.
\]

J 是十列、每列 1024 個 cells 的**集合值**表；包括全部空格，非空格保存每份
完整 H 著色。其 support \(R_H=\{(\beta,\tau):J_H(\beta,\tau)\ne\varnothing\}\)
與更弱的外框投影 \(\Sigma(H)\) 分開。只有 support 不能還原每份原圖 full lift。

## 2. 中心消去：五個互斥的完整纖維分支

令 \(M(\tau)=C\setminus\{\tau_0,\ldots,\tau_4\}\)。限制到 H 及補回中心給雙射

\[
\mathcal C_G(\beta)\ \longleftrightarrow
\bigsqcup_{\tau\in C^5}J_H(\beta,\tau)\times M(\tau).
\tag{1}
\]

由於 U 是奇五環，proper tau 必用三或四色。三色時唯一的缺色就是 v 的色；
四色時該 H lift 不能延伸。三色的色類大小必為 (2,2,1)。定義

\[
E_i(\tau):\quad
\tau_{i+1}=\tau_{i+3}\quad\land\quad\tau_{i+2}=\tau_{i+4}.
\]

在 proper U 著色上，E_i 的三個色類是
\(\{u_i\},\{u_{i+1},u_{i+3}\},\{u_{i+2},u_{i+4}\}\)；它們因原環邊而互異。
故五個 E_i 互斥，且其聯集恰為可延伸的 tau。因而 (1) 等於這五個分支的
不交聯集，逐份 eta 加入唯一缺色即可，不丟棄任何原 G lift。

\[
\beta\in\Sigma(G)
\iff \exists i,\tau,\eta\in J_H(\beta,\tau):E_i(\tau).
\tag{2}
\]

兩個等式必須由**同一份 eta** 同時滿足，不能把兩個各自非空的邊界投影相交
當作 (2)。五分支是完整具名關係的分解；兩對同色點沿 U 交錯，故不能直接把
每個 E_i 當成在空五邊面內合法完成的兩次同時識別。

## 3. 五個合法較小圖與逐染色重建

對每個 j，令 Q_j 由 H 在空五邊面內識別 \(u_j=u_{j+2}\) 得到。先在該面內
加入一條弧，再沿弧收縮；兩端原本非鄰接，故不產生 loop。只簡化平行邊，
保存各原邊像及 preimages。B 的五個原 labels 不被識別，仍是指定外面。
各個 Q_j 單獨合法；不是同時實施五次操作。

設 \(\pi_j:V(H)\to V(Q_j)\)。Q_j 的完整著色透過 \(\eta=\chi\circ\pi_j\)
拉回 H，與下列集合雙射：

\[
S_j(\beta)=\{\eta\in\mathcal C_H(\beta):
\eta(u_j)=\eta(u_{j+2})\}.
\tag{3}
\]

反向是按 block 常值下降。Q_j 中兩個 U pin 的像重合，但仍保存兩個原 pin 名稱
及 pi_j；不聲稱商圖還有十個不同頂點。所有 fibres 都以原 B、U 的座標拉回比較。

**完整染色重數引理。** 對每份 \(\eta\in\mathcal C_H(\beta)\)，令
\(m(\eta)=\sum_{j=0}^4\mathbf1[\eta\in S_j(\beta)]\)。則

\[
m(\eta)=
\begin{cases}
2,&\eta(U)\text{ 用三色};\\
1,&\eta(U)\text{ 用四色}.
\end{cases}
\tag{4}
\]

證明：C5 的獨立集大小至多二。三色時恰有兩個二點同色類，四色時恰有一個，
所有同色對都是五條非邊 \(u_ju_{j+2}\) 之一。沒有第三個同色對。

因此在以**每份原 H 完整著色**為基底的自由阿貝爾群中有係數逐項等式

\[
\boxed{\quad
[\operatorname{res}_H\mathcal C_G(\beta)]
=\sum_{j=0}^4[S_j(\beta)]-[\mathcal C_H(\beta)].\quad}
\tag{5}
\]

右邊係數恰為 0 或 1。保留係數 1 的 eta，再插入 U 缺少的唯一顏色，
便還原全部 G lifts。也可直接取在五份 pullbacks 中出現兩次的完整 eta；
這是同一色框的重疊偵測，不能用各圖自己的色名或不同 full-lift 編號比較。

更強地，(4) 的重數永不為零，故 \(\bigcup_jS_j(\beta)=\mathcal C_H(\beta)\)。
**只給五份 Q_j 的完整 lifts 及原 label maps，便能先重建全部 H fibres，再重建
全部 G fibres；不必另外枚舉 H。** 具體流程是逐列拉回、以完整 eta 去重並記錄
所屬 j，依原 U tuple 分入 1024 格；重數二者補中心，重數一者保留為不可延伸。
每個 Q_j 內自己的不同 lifts 不會拉回同一 eta，因 pi_j 滿射；所以重數不會
混入同一分支的重複計數。這給出五個內點數 k−2 的合法圖之間可執行的無損縮減。

各固定 \((\beta,\tau)\) 亦有 (5)。若只取總數，可得推論

\[
|\mathcal C_G(\beta)|=
\sum_{j=0}^4|\mathcal C_{Q_j}(\beta)|-|\mathcal C_H(\beta)|.
\tag{6}
\]

式 (6) 是計數推論，完整重建使用 (3)–(5)。各圖的十個非空 bits 不足以算出
右邊的重數；\(\bigcup_j\Sigma(Q_j)=\Sigma(H)\)，一般不是 \(\Sigma(G)\)。
即使 \(\beta\in\Sigma(Q_j)\cap\Sigma(Q_{j+1})\)，兩個 witnesses 仍可能不同。

若 G 有 k 個內點，H 有 k−1 個，Q_j 各有 k−2 個。在上游最小來源前提下，
這些較小圖各自的外框關係都在 K；但 (5) 含減項並依賴完整 lifts，K 的普通
關係聯集封閉不能消去這項依賴。沒有由此宣稱 K 的完整性已證。

## 4. 為何不能用純局部、零新頂點的正聯集取代

以下是針對**所有 annulus contexts 都有效**的局部 gadget 限制，不是對指定 H
或一般五輪縮減的不可能定理。

若局部替換只用原 U 五個頂點及加邊，任一被接受的三色著色均可拆開其中一個
二點色類，產生仍 proper 的四色著色。因此任何含有 wheel 接受列的這類分支
亦接受 wheel 拒絕列，不能作為普遍 sound 的正聯集分支。

容許在空五邊面作非交叉識別也沒有解決此問題：原環邊不容許相鄰點同 block，
三點 block 亦不可能，且所有兩對二點 block 的三色分割都交叉。合法 partition
故只可能留至少四個 blocks。若一個分支已有三色著色，可將某個同色的不同
blocks 拆開，仍得四色著色。於是「加邊＋合法非交叉識別＋零新頂點」的任何
正聯集都不能普遍實現完整 wheel rim 關係。

這個限制保留兩個出口：特定原 annulus H 可能過濾掉局部多出的四色 lifts；
或改動／壓縮 annulus 的其他頂點，構造更大的具名操作。兩者都須回到完整 J。

## 5. annulus 代表的精確剩餘義務

設 A 是 H 的 annulus 圖；若能在同一 B、U 邊界槽位找到 A'，並有

\[
\forall\beta,\tau:\quad
J_A(\beta,\tau)\ne\varnothing
\iff J_{A'}(\beta,\tau)\ne\varnothing,
\tag{7}
\]

則取原 lift 的同一 \((\beta,\tau)\)，選另一邊 fibre 中的 lift，再保留／補回
唯一中心色，即給 G 與 A'+v 的兩向完整延伸構造。代表的私人頂點不同，
所以 (7) 不宣稱原、新 fibres 等基數或雙射；完整原 fibres 仍需另存以作無損追溯。

若 A' 在 B、U 之外至多 r=6 個私人點，補中心後內點數為 \(5+r+1\le12\)，
才可接上游十二內點界。**本輪未構造這份任意來源的 annulus 代表。**
更弱的專用目標可只保持五個 E_i 分支的接受列聯集，但也必須給出合法 disk
圖、兩向 lifts 及同一原圖的共同見證，不能由外圈 bits 假定成立。

## 6. 證據、重播及範圍

紙面推導及獨立審查見 [THEORY](review/THEORY.md) 與
[INDEPENDENT](review/INDEPENDENT.md)。有限資料由
[checker](controls/check_w5.py) 產生並核對；全部資料見
[壓縮完整證書](controls/certificate.json.gz) 與 [摘要及反控制](controls/summary.json)。

固定控制域是 pentagonal prism annulus、其五個四邊面各選一條對角線的全部
32 個 triangulations，及在 prism 一個 annular face 添一個二度點的控制，共 34 圖。
原 B=0..4、U=5..9、v=10；額外點為 11。全部原邊、面 dart、旋轉與具名外面
經一致性／Euler 核對；單對商圖保存原面內弧、識別映射與全部邊 preimages。

| 完整控制項 | 數量 |
| --- | ---: |
| 十列乘全部 U tuples 的 cells | 348,160 |
| 空／非空 cells | 345,580／2,580 |
| 完整 H lifts／補中心後完整 G lifts | 3,250／1,620 |
| 合法單對商圖／完整商圖 lifts | 170／4,870 |
| 直接商圖 DFS 與原 H 拉回核對的列 | 1,700 |

直接全 G DFS 與中心重建逐份相等；直接商圖 DFS 與原 H 同色對篩選逐份相等。
額外點控制同一 \((\beta,\tau)\) 有兩份不同 full lifts，避免只校準單元素 fibres。
獨立 checker 另對全部主證書圖直接枚舉，並以不同的 annular spoke subdivision
控制核對 10,240 格、1,853 份 H lifts、932 份 G lifts 及 2,785 份 quotient lifts。

**只存外圈的具名反例。** 令 H0 的邊為 B 環、U 環及五條 \(b_iu_i\)。
H1 在同一 annulus 加入
\(b_0u_1,b_2u_1,b_3u_2,b_4u_3,b_0u_4\)，即 `triangulated_01`。
兩者都有 \(\Sigma(H0)=\Sigma(H1)=1023\)，補回相同具名五輪中心後，
\(\Sigma(H0+v)=1023\)、\(\Sigma(H1+v)=831\)。H1+v 丟掉 `01212`、`01213`。
固定 beta=`01212`，H0+v 的全圖 lift（頂點 0..10）為
`01212101032`；H1 的全部 H lifts 只有 `0121223031`，其 U 已用四色，不能接中心。
這個控制保留原 U 的命名及合法嵌入位置，沒有借用另一組 pins。

**不同見證不能拼成共同見證。** H1 的 beta=`01012` 下，Q1、Q2 均接受，
拉回 H 的全部 lifts 分別只有 `0101223231` 與 `0101212303`，交集為空。
另保存獨立正規化 U 後違反全部五條 \(b_iu_i\) 的反例，及單對識別仍用四色的反例。
這四項錯誤充分條件均標為 `counterexample`。

**交叉商圖的實際非平面控制。** 在 H0 同時識別
\(a=u_1=u_3\)、\(c=u_2=u_4\) 並刪掉 u0，得到 K3,3 subdivision：兩側是
\(\{c,b_1,b_3\}\)、\(\{a,b_2,b_4\}\)。九條跨邊除 \(b_1b_4\) 外都是原商圖邊，
該條用路徑 \(b_1b_0b_4\)；內點彼此不交。具名路徑由獨立 checker 核對。

只讀重播：

```bash
python3 -B audits/2026-10-12-w5-marked-relation-e299ae98/controls/check_w5.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-12-w5-marked-relation-e299ae98/controls/check_w5.py --check --seed 17
python3 -B audits/2026-10-12-w5-marked-relation-e299ae98/review/independent_check.py --primary audits/2026-10-12-w5-marked-relation-e299ae98/controls/certificate.json.gz
```

[verify.py](verify.py) 將正常／seed17、獨立枚舉、六種破損證書及拒絕覆寫測試的
實际輸出保存到 [verification.json](verification.json) 及其 logs。再次執行時須用
`--output` 指定不存在的驗證檔，不覆寫原驗證；一般只讀重播使用上述三個命令。
本輪正式文件檢查與 docs 範圍 DocGraph 通過；全工作樹 DocGraph 因保留的歷史
副本重複 IDs 失敗，未刪歷史資料。凍結及重播期間 evidence hash 的核對見該驗證檔。

| 層次 | 界線 |
| --- | --- |
| 紙面 | (1)–(7) 與局部零新頂點正聯集限制，均在明列前提下 |
| 有限來源 | 合法全內部五輪的 synthetic annuli；不代替最小目錄外來源 |
| 真正 933／941 最小來源 | not triggered |
| Lean | 未新增 theorem，未執行 lake build |
| 上游外部定理／大型枚舉 | 沿用凍結入口，本輪未重跑 |
| 一般合法正聯集縮減、r≤6 annulus 代表、K∞=K≤5 | OPEN |

L0 為本獨立包；L1 已核對原 [Kempe 導覽](../../docs/c5_kempe_guide.md) 與
[STATUS](../../docs/STATUS.md) 的 annulus OPEN 停止點，仍正確。此包尚未正式採納
至共用文件，故不更改原 routing。L2 父題仍 OPEN；傳播停於此，不改其他研究線。
沒有 commit、push 或對外發布。
