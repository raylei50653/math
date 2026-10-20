# A 對 B、C 的獨立審查

BASE `b89c5913cea9df2305845be0f65fa6f1c1aaf55f`。本審查不匯入 B 或 C
的程式作為 A 的計算權威；A 自己的完整邊界矩陣與 C 的四圖矩陣相同。

**B：PASS。** CORE 的兩塊 cap 沒有交叉邊，23 條原 incident 邊恰分為
12+11；Right 的 r 條件保留 rv,rw，Left 的 p 條件保留 pn。
FORCED_SECTORS 的兩份 D_old 字面 fibre 先使用各自完整 p 與 xy lifts，
再以原 b 的完整鄰集恢復唯一 b=B。兩個 xy lifts 的正規化像以原 q=0/1
分開，故 A_a>=2d_a、A_b>=2d_b 的單射不會重複計數。A 獨立在 C10
上逐份枚舉完整 p,h,b,x,y,r 邊限制，得到同樣的六格／四格正子 fibres。
沒有把不同 witnesses 的 Kempe 路拼接。

**C：PASS。** 完整 C8 矩陣逐列保留所有 p,h lifts；Q2 的 a=q 分支
在直接邊 predicate 中仍存在。GB941 checker 以 Fraction 重建全部 91
個 planar columns 的秩，及原必要零列限制後的 44 維完整 kernel；
四個精確殘差泛函逐一消去每個基向量。這是任意大小 disk 的線性空間
紙證加完整有理數核對，不是對有限外側樣本的擬合。

由 `A_a=N_tau(GB)+2N_01202(GB)` 和
`N_01212(GB)=N_tau(GB)+N_01202(GB)`，非負性及 B 的 A_a>0
確實迫 G_B 的 01212 完整 fibre 非空；B 的 A_b>0 同時迫 G_B 接受
01232。因此這張固定候選的指定四列合同普遍不可能。此結論沒有推出
G_B 的完整支持都在 K132，亦沒有排除其他支持證書或 Q1／Q2。

A 的 source-positive 控制與這個新定理相容：兩份控制的 G_B 均為
1021 或 1023，兩者皆接受 01212。控制保留兩份來源正子 fibres，
卻沒有來源圖實現；它們不削弱已證的 G_B 定理。

已執行 C/check.py --negative-controls；正常結論及六個負控制均 PASS。
B 的獨立 checker 及其輸入雜湊另外由父層工程檢查核對。
