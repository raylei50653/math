# C8 apex 度數三的排除證明

狀態：**proved，沿用 frozen C8-STRUCT 來源、共同 equality 計數空間及三角化 Kempe 軌道定理。**

## 1. 同一來源及全稱量詞

G 是所有完整 C5 關係不在 K132 中的來源，先最小化原內點數，再最大化邊數。
原外框 B、五個具名 apex、三個具名私人點及其實際附件、rotation，全部沿用
[frozen source contract](frozen/audits/2026-10-13-c8-struct-243a125/SOURCE_CONTRACT.md)。
假設 h=3。上游已排除 70 項中的 62 項，所以只需研究餘下八項。
其內側 H 是**同一張**具有 induced C8 外框的三角化 disk；每個 apex 有兩個
原 B 附件，故 deg_G(a)=deg_H(a)+2。三個 y 的 H 度數至少四，H 嚴格內點
度數至少五。全域最小性、小 cap 及無內弦結論均為已證前提。

對每份固定 literal 四色 C8 指派 p，x_p 是 H 延伸 p 的全部完整染色數。
全圖一次 S4 改色給雙射，所以以 274 個 canonical words 儲存 x，不改變
固定 literal 指派的延伸數，也不乘除 boundary 軌道大小。

上游 RESULTS 的支援 U 是**每一個實際來源關係的必要上界**，不是假設已存
正向量等於實際來源。171 列上界含上游已普遍迫零的兩列刪除；其餘為
134／175／193 列上界。以下論證只使用 x 在 U 外為零，以及原完整 Σ
每個接受列的計數為正；不要求 U 中每列為正。

## 2. 新局部計數引理

假設某具名 apex a 的 H 度數為三。記其 C8 鄰點 u、v。無內弦使它恰有
一個嚴格內側鄰點 t；原三角面為 (u,a,t)、(a,v,t)，故 tu、tv 都是原邊。

固定 C8 去掉 a 後的一份 literal 指派 s，且 s(u)=s(v)=c。在**同一 H-a**
上，令 z_d 計數所有延伸 s 且 t 色為 d 的完整染色。因 tu、tv 為原邊，
z_c=0。設其他三個色為 i、j、k。逐份保持全部 H-a 染色不動，只補回 a：

\[
x_{s,i}=z_j+z_k,\qquad x_{s,j}=z_i+z_k,\qquad x_{s,k}=z_i+z_j.
\]

因此三項均滿足

\[
2x_{s,i}\le x_{s,i}+x_{s,j}+x_{s,k}. \tag{D3}
\]

這是所有完整延伸的計數雙射；a 之外的每個點及原圖都固定。若 canonical
化後兩項索引相同，必保留其**重數**。特別地，在某三項中若僅一項可非零，
且該項只出現一次，則它亦被迫為零。不能把含重複索引的三項先改成集合。

## 3. 38 份支援排除

對每份查詢與每個具名 apex 的 deg_H(a)=3 假設，從上游 U 開始反覆施行：

1. 用 (D3) 刪除三項中唯一仍允許且只出現一次的座標。
2. 用上游 821 個固定 split literal representatives 及 981 個三角化完整軌道
   向量：若軌道含已為零的座標，非負軌道權重必為零；如果某 canonical p
   的任一 literal representative 已無可用軌道，則 x_p=0。

每次刪除保留全部實際來源的支援。算法至同一支援不再改變才停止。
[certificate.json](certificate.json) 保存每步具名刪除；check.py 獨立重算。
四十項中的三十八項在此已失去至少一個原接受列，全部失去 `01232`。
其中可能整個支援清空，但論證只需一個必要接受列消失。

## 4. 其餘兩份的精確共同計數排除

剩下 c04-941/a1 與 c07-941/a4。分別保存獨立的 rational 證書，沒有只靠
反射猜測係數。設 E 是上游 274×91 完整 equality 計數矩陣；每個來源 x=Ec，
c 可有任意符號。Lx 是 821 列共同色框拉回；由上游可逆 Kempe 定理
Lx=Vλ，λ≥0。原 U 外的座標 x_Z=0。

每個證書給 z、α、β，滿足在全部 91 個 c 座標上的**精確**恆等式

\[
z^T L E+\alpha^T E_Z+\sum_t\beta_t D_t E=-T_9E, \tag{F}
\]

其中 D_t x 是 (D3) 右側減左側，β_t≥0；對支援包含於 U 的全部軌道 j，
z^T V_j≥0。T_9 對應原外框完整接受列 `01232`。
將同一來源 x=Ec 代入 (F)，得到

\[
0\le\sum_j\lambda_j(z^TV_j)+\sum_t\beta_tD_tx=-T_9x.
\]

但原 Σ=941 要求 T_9x>0，矛盾。所有等式、非負性與 literal transfer
由 Python 標準庫 Fraction 檢查；SciPy 僅用於發現候選。

T 不從邊際關係或獨立改色取得。check.py 對每個原外列 r、每個內列 p，枚舉
p 的全部**不同** literal S4 lifts，沿同一份 `collar_edges` 的所有具名原邊
逐一檢查，重建 T[r,p]。二色列重複的色名置換只算一次。

## 5. 新結論及精確邊界

四十項條件假設均矛盾，故八份剩餘 C8 契約的每個 apex 都滿足

\[
\deg_H(a_i)\ge4,\qquad\deg_G(a_i)\ge6.
\]

沿用同一 H 的 Euler 曲率式，寫 I=V(H)\C8、A 為五個 apex、Y 為三個私人點：

\[
n_5(I)=1+\sum_{a\in A}(\deg_Ha-3)
+\sum_{y\in Y}(\deg_Hy-4)
+\sum_{v\in I,\deg_Hv\ge7}(\deg_Hv-6)\ge6.
\]

所以 |I|≥6，而 G 在 B 內有八個 C8 點，得到**h=3 ⇒ 原內點數≥14**。
這也排除 h=3 且某個 apex 原完整度數為五的所有任意大小來源子域。

沒有排除八份查詢的全部來源；h 仍≥3、全域 n5 仍≥9。
此條件結論不能排除 h≥4 的十三內點來源，所以不宣稱 K≤13=K≤5 或
K∞=K≤5。尚缺同一 H 在更高 apex 度數下的完整關係實現或不可能性。
