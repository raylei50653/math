# r₂ 的相鄰共同配對與合法封口：獨立紙面核對

2026-10-29。本 note 僅給全來源必要條件，不聲稱射線排除。來源為
`docs/ck_bernhart_retained_intersection.md`、`docs/ck_bernhart_cross_split_audit.md`
及後者保存的第二個 primitive full lift。未使用普通 PM 計數或外部定理。

## 固定資料

r₂ 有 46 個正 signed signatures，各 primitive 權重為 1。逐項檢查可將其唯一分成
23 對 `(S, S ∪ {(2,3,−1)})`，其中 S 不含葉 2、3。這是完整 signature 的配對，
包括空 S，不是 endpoint marginals。其全部 243 個正 literal 八葉 words 中均有
`w₂=w₃`。刪除兩位置後共有 81 個正 literal 六葉 words；每個六葉 word u 的三份
插入字 `u[0:2]+(x,x)+u[2:]`（x=1,2,3）primitive count 相同，定義為 h(u)。
75 個 u 有 h=1、6 個 u 有 h=2，故 Σh=87；全八葉質量為 3·87=261。
這些是固定有限資料，實際來源的量詞另由下述論證承擔。

## 全來源引理 A：同圖三個 fibres 等勢

設同一實際 plane near-cubic disk Q 的全部 (y,n)=λr₂，λ>0（不需先用偶性）。
固定任一完整 Tait 染色 φ。因零字無染色，φ 在 e₂、e₃ 上有共同色 x。
取 y≠x。完整 xy 系統中 e₂、e₃ 所在的路必互相配成 e₂–e₃：其實際
signed signature 為正權重 signature，而上列 23 對已覆蓋全部允許 signature。
因此交換這條**同圖實際完整路**的 x、y，保持其餘六葉，將共同色 x 改為 y。
逆交換是在所得染色的同一條無向原路上，故是雙射。對每個固定六葉 word u，
三個共同色 fibres 各有 λh(u) 份完整染色。此敘述對所有允許來源和所有 λ 成立，
不把不同染色的路徑拼接在一起，也未聲稱三條交換可選成相同原路。

## 全來源引理 B：相鄰二葉的封口與標記邊

先假設 e₂、e₃ 的 leaf edges 分別接不同 cubic vertices p、q。兩內端點必互異：
若相同，proper Tait 在該點不可能給兩條不同 incident 原邊相同色。刪除兩葉及
兩 leaf edges，在原葉間**不含其他葉的相鄰外邊界弧**附近添入 p–q 邊 f，沿原兩
leaf stems 及該弧走線。其餘原邊與 rotation 保留；p、q 的 f dart 佔被刪 stem
的原 rotation 位置。這是同一 disk 中的平面封口；f 可以與舊邊平行，不把它們
當同一原邊。所得 Q̂ 是六葉 near-cubic disk，f 是具名標記邊。

每份 Q 染色將兩相同色 stems 合成同色 f，得一份 Q̂ 染色；反向切開 f 亦唯一。
Q̂ 的任意完整染色切開都給 Q 的完整染色，因 Q 的全部計數假設而落在原支援。
故這是**全部**染色的一一對應，並非只對選定 fibres。對每個六葉 u，
`n_Q̂(u)=Σ_x n_Q(u with x,x)=3λh(u)`。

完整 six-lift 也可精確寫出。將 23 對中的 S 依剩餘葉序 `(0,1,4,5,6,7)` 重標，
得 k 的 23 個正六葉 signatures，權重均 1。固定任一 split ab 及與 S 相容的六葉
word u；以 c 為第三色。f 色為 c 的染色，切開後的八葉 signature 是 S，計數
λk(S)；f 色為 a 或 b 的兩個互斥子族，切開後 signature 都是
`S∪{(2,3,−1)}`，各計數 λk(S)。封口只把這條已迫出的路關成偶閉圈，不改其他
邊界路或其長度奇偶，所以新六葉 signature 仍恰是 S。故
`y_Q̂(S)=λk(S)+2λk(S)=3λk(S)`；原權重為零的 signatures 在封口後也逐項為零。
這裡使用的是「固定 compatible boundary word 下、實際完整 Tait 染色的 signature
計數」等價於 y 的定義，並非把 y 當普通 PM 數。於是全部 `(y,n)_Q̂=3λ(k,h)`。

更強地，對 Q̂ 的任意染色，令 f 的色為 x。對每個 y≠x，f 必在 xy 系統的
**閉圈**上：若它在 boundary-to-boundary 路上，沿 f 切開將把該路分成兩條路，
使原 Q 中 e₂、e₃ 各配到其他葉；這與引理 A 的完整 signature 互配結論矛盾。
原 e₂–e₃ 奇長路在封口時以一條 f 取代兩條 stems，長度減一成偶圈；
反向切開長度加一，與原 signature 的 sign −1 一致。此處閉圈包括平行邊
所成二圈；沒有假設閉圈是面邊界、沒有內部附件，亦沒有收縮它。

### leaf-to-leaf 例外

若 e₂ 的 leaf edge 直接接另一葉 eⱼ，則該原邊是獨立分量，可任意改其色而
保持所有其他原邊。Q 有完整染色且每份均 e₂=e₃，迫 j=3。此時 e₂e₃ 本就是
獨立 free edge。可刪此分量得到真正六葉圖 Q₆；三個共同色 fibres 均直接等於
Q₆ 全部 fibres，因此 `n_Q₆(u)=λh(u)`。若欲統一保留總計數 3λh，則封口對象
必擴充為「Q₆ 加一個無頂點、三色可選的獨立標記圈」，這不是通常有限圖的
near-cubic disk，必須明說，不能默認成普通標記邊。連通且有 cubic interior 的
來源不會有這個 leaf-to-leaf 分支。若 e₂、e₃ 分別是不同 free edges，其顏色可
獨立改變，立即違反全支援相等性，因此不允許。

## 能推出什麼、不能推出什麼

封口把任意候選來源轉為一個完整計數 3λh 的六葉來源，並帶有在所有染色中對
兩個包含其色的系統皆在閉圈上的同一標記邊。這是所有原路長、所有內圈及全部
rotation 的普遍必要條件；沒有固定長度截斷。

尚未證：上述「全染色中在閉圈」性質迫 f 屬於可剝離的二端分量，或准許刪 f／
收縮任一閉圈而保持全部其餘六葉 fibres。圈兩側可能有原附件，不能作無條件
plane vertex 收縮。即使某個所選封口失敗，也未排空全部標記六葉來源；目前
沒有從此引理得到任一 λ 的全面不存在性，更沒有全部正偶 λ 的排除。
也不能由 r₂ 排除（若日後證成）推出原 76 列任一座標必零。
