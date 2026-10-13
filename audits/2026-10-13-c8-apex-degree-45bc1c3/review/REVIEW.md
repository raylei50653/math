# C8 apex degree-three：獨立審查

BASE：`45bc1c3dc9dacaee1b10df9d64f1c6a27bb0e954`。
**結論：PASS。** 八個剩餘 C8 查詢的全部五個 apex 都不可能在同一原 H
中 degree 三，因此其 H-degree 至少四、原 G-degree 至少六。
這排除四十份「具名 apex degree 三」子域，不是排除八個完整來源。

## 1. 三項不等式來自同一原 H 的完整染色

沿用已證 induced-C8 與原 disk 三角化。若具名 apex a 在 H 的 degree
為三，其鄰點恰為兩個 boundary 鄰點 u,v 和一個嚴格內點 t；原內側面
必是 `(u,a,t)`、`(a,v,t)`。所以 t 也接 u,v。

固定同一 C8 去掉 a 的完整 literal 染色 s，且 `s(u)=s(v)=c`。
取其餘三色 i,j,k。對同一 H−a，令 z_i,z_j,z_k 分別是符合 s 且 t
取該色的全部延伸數。t 接 u/v，故不能取 c。刪掉或補回同一 a 給出
逐份染色的等式

\[
x_i=z_j+z_k,\quad x_j=z_i+z_k,\quad x_k=z_i+z_j,
\qquad z_i,z_j,z_k\ge0.
\]

因此 `x_i≤x_j+x_k`，另兩式循環成立。這些 x 是固定一份 literal
boundary coloring 的 H 延伸數，不是 boundary-orbit 的總染色數。
對全部原圖施同一 S4 顏色置換給完整染色雙射，所以 canonical row
坐標可直接代入，**沒有 orbit-size 因子**。
三種 a 顏色可能 canonicalize 到重複 row；不等式必保留這個 multiplicity。
證書及兩份獨立程式均保留長三的 tuple，沒有先把它改成 set。

## 2. 對全部來源計數的條件排除

被使用的 U 是上游已證的原來源 support upper，並非某份可行候選向量的
support。故真實 H 的完整共同計數向量 x 在 U 以外恰為零。
沿用上游已證的 `x=E c` signed-span 條件，以及同一 H 的固定色分拆
非負 orbit expansion `x_lifted=V lambda, lambda≥0`。
此處 c 不限制符號，lambda 必非負。

若某 orbit column 含一個已知為零的坐標，該 column 的非負 coefficient
必為零。若某 normalizer row 不被任何仍可用的 column 支撐，對應 x
坐標也必為零。三項不等式中若只剩一個非零可能項且其出現 multiplicity
為一，該項同樣必為零。兩條規則都只推出同一原圖的必要零值。
在集合不再變化前反覆套用，38/40 份假設使至少一個原目標要求存在的
外框 row 無法取得延伸，因而排除。這不要求枚舉或實現任意 H。

剩下 c04-941/a1 和 c07-941/a4 各有 184 個 support 坐標。
各自的 exact dual 在本身的原具名 query 上獨立驗證，不以口頭的反射
對称替代原列搬運。

## 3. 兩份 dual 的符號與適用範圍

寫每個 degree-three inequality 為 `g_l x≥0`；例如
`g_l x=x_i+x_j+x_k−2x_i`，保留重複索引。
兩份證書各給 normalizer 坐標 z、只支撐在 U 外的 a，以及 `b_l≥0`，使

\[
\sum_r z_r E_{p(r),j}+\sum_{i\notin U}a_i E_{i,j}
 +\sum_l b_l\sum_i g_{l,i}E_{i,j}
 =-\sum_i T_{9,i}E_{i,j}
\]

對全部 91 欄 j 精確成立。另外，對每個全部 support 位於 U 的
triangulated orbit column v，`z·v≥0`。因此對任一實際 H，

\[
0\le z\cdot x_{\rm lifted}+\sum_l b_l(g_lx)=-T_9x.
\]

但原目標 941 要求外框第 9 列 `01232` 延伸存在，即 `T_9x>0`，矛盾。
此論證同時量化全部 x、全部 signed span coefficients 和全部非負 orbit
weights；它不是只否定上游某個選定數值向量。
`z·v≥0` 僅需、也只聲稱對 U-supported columns 成立；不把條件 dual
誤稱為所有未受 support 限制 columns 上的普遍不等式。

## 4. 本 reviewer 的獨立重播

[`check_support.py`](check_support.py) 不匯入 producer 或 package checker。
它直接枚舉每個位置的全部七頂點 literal contexts，取得每位置 31 個
三項 tuple，再從 frozen cone columns 重做精確零值傳播，核對 package
certificate 的全部 final supports。結果恰 38 個 support 排除和兩個
上述 residuals。fixed point 條件比較整輪開始／結束的 S，不僅看最後
一条 pruning rule 是否刪點。

[`check_dual.py`](check_dual.py) 以 Python `Fraction` 逐一核對兩份 certificate。
每份重新枚舉 732 個合法 literal contexts，核對全部使用的 degree-three
tuple，全部 91 個 span coordinates，以及全部 418 個 U-supported orbit
columns 的精確非負性。兩份皆 PASS，最小 column dot product 均為零。
沒有匯入 SciPy、數值 solver 或 discovery script，也沒有以浮點容差判定。
兩份 reviewer 程序另以 [`transfer.py`](transfer.py) 直接遍歷 `4^8` literal
指派，保留全部 6,564 個 proper C8 words，按同一具名原 collar 邊與十個
固定 outer words 重算 T。此法獨立於主程序的 S4 orbit lifting，也不讀取
未封存的舊 interface 檔。

```bash
python3 audits/2026-10-13-c8-apex-degree-45bc1c3/review/check_support.py
python3 audits/2026-10-13-c8-apex-degree-45bc1c3/review/check_dual.py dual-c04-a1.json
python3 audits/2026-10-13-c8-apex-degree-45bc1c3/review/check_dual.py dual-c07-a4.json
```

本審查沿用 frozen 上游的 E-span、triangulated cone 完備性、literal transfer
與 source upper 證明；沒有重證那些上游大型證書，也沒有 claim graph realization。

## 5. 度數與大小的精確新界線

五個 apex 在 H 都 degree 至少四；三個 y 原已在 H degree 至少四。
因此整個 C8 boundary 的 H-degree 皆至少四。令 I 是其嚴格內側點，
上游曲率等式给

\[
n_5(I)=6+\sum_{v\in C8}(d_H(v)-4)
            +\sum_{v\in I,\ d_H(v)\ge7}(d_H(v)-6)\ge6.
\]

所以 `|I|≥6`，原 h=3 来源的內點數 `k=8+|I|≥14`。
每個 apex 恰有兩個原 B 附件，所以原 degree 至少六。
按原面第三點 t_i 的既有等價式，現在八個位置都滿足 `t_(i−1)≠t_i`。

不能由此提高一般 `n5(G)≥9`：三個 y 的 degree excess 加上 y 自身仍為
degree-five 的數目只保證至少三，與上述六相加仍是九。
也不能把 h=3 的 `k≥14` 冒稱全部 h≥3 来源的同一新下界；h≥4 路線另有
義務。h≥3、n5(G)≥9、八個完整 C8 必要條件 residuals 及主命題 OPEN
的界線均保留。
真正最小目錄外來源沒有提供實例，實例控制仍是 `not triggered`。
本 conditional exclusion 來自逐圖成立的計數等式與已證必要域的精確反證，
不以零觸發樣本推論來源不存在。
