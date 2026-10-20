# B 對 A 共同 C10 控制的獨立核對

結論：**PASS，權威限於必要模型的精確控制。** 沒有來源實現或較小 bad。
審查 [A/PROOF.md](../A/PROOF.md)、[A/model.py](../A/model.py)、
[A/check.py](../A/check.py) 及兩份完整整數證書。

1. 原介面及 cap 與 B 的獨立原邊重建相同。A 的 E→C10 矩陣固定一份
   E 字面列，枚舉全部 s,v,w,t,r；它保留的八條額外 cap 邊，配上 E
   原 properness 的 cx,xy,ya，恰為 B 的 11 條完整右 cap 邊。
2. B 另從自己的 `core-certificate.json` 的全部 Right lifts 出發，枚舉
   全部 24 個全域色置換，按 core stabilizer 及 E 色軌道大小還原固定字面
   重數。所得 **274×2461 所有格**與 A 的 T 逐格相等。這項核對不沿用
   A 的 cap 枚舉迴圈，特別覆蓋二色 core／E 的不同 stabilizer。
3. A 的兩個 source-positive subset 恰為 B 兩份 D_old 完整 fibres。
   固定 A=0,B=1,C=2,D=3，h=a 一份的 (R,L) 有三支、(v,w) 有兩支，
   h=b 一份的 (R,L) 有兩支、(v,w) 有兩支。6／4 格完整，沒有把一份
   正 fibre 拆開後選錯 h 或 r 的顏色，也沒有混合兩份原 witnesses。
4. C10 的 signed planar coefficients 只作線性重建，無非負假設。
   分量交換保留全部 7382 個字面 H 軌道等式、完整交換結果的重數及
   不接框分量的共同權重。控制的同一 Z 同時供所有原圖及候選查詢；
   各份控制有自己的 Z，沒有跨候選或跨向量拼接拒絕結論。
5. 正常及 seed17 執行 `A/check.py --negative-controls` 均 PASS，六個
   損壞全部被正確拒絕。較強 Q2 控制同一向量得 (Q1,Q2,G_B)=(1021,941,1021)，
   且 d_a=d_b=4；另一份同向量得三個 1023、d_a=10,d_b=16。

精確停止點正確：較強必要模型不能排除 Q2 四列合同，也不能強迫三候選
中至少一張目錄外。這不證任何真正來源存在，不排除未加入模型的真實
來源條件能閉合 Q1／Q2。A 明確把前輪三份缺正原 fibre 的控制降為負控制，
沒有藉其 C10 lift 又宣稱它們滿足完整原來源。

G_B 的新洩漏定理由 C 的另一份普遍計數證書負責；A 的控制不能取代該
定理，亦不能由一份 allK 控制推成「全部真正 G_B 支持皆在 K132」。
