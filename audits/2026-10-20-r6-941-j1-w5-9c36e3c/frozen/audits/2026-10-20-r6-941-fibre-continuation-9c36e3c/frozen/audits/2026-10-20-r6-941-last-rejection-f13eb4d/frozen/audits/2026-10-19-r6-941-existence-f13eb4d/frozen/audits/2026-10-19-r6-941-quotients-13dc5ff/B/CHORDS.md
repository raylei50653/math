# 同一 C10 的原度數與短圈 pocket 限制

固定 BASE `13dc5ff163045c85b5c82dde438eb5f275dab999`，完整來源契約是
[前輪契約](../../2026-10-19-r6-941-leakage-b89c591/B/SOURCE_CONTRACT.md)。
本頁只處理原 `(p,h)=(p,ell)`，同一實際
`D10=G-{b,p,h,x,y,r}`，字面圈是 `(a,n,R,L,q,c,s,v,w,t)`。
原圖任意大；沒有把控制向量當成實圖。

## 1. 補回完整來源的 q 度數

既有 [雙低 p,q 定理 §5](../../2026-10-14-c4-return-branches-a11d4bb/pq/PROOF.md)
對同一原 pq 邊及其另一面點 ell 證明
`d_G(p)=d_G(q)=5 => d_G(ell)>=6`。
[後續 low-p §5](../../2026-10-14-lowpq-source-676b102/pq/PROOF.md)保留這一結論。
本輪 `p=h=ell=5`，原內點度數至少五，故 **`d_G(q)>=6`**。
這不要求 active-f matching，也沒有推論原 c>=5。

完整刪除損失是下表；其餘原鄰點與邊全部保留。

| core 框點 | 刪去的原鄰點 | 原來源下界 | core 下界 |
| --- | --- | ---: | ---: |
| a | b,p,y | 6 | 3 |
| n | p,h | 5 | 3 |
| R | h | 5 | 4 |
| L | h | 5 | 4 |
| q | b,p,h | 6 | 3 |
| c | b,x | 4 | 2 |
| s | x,r | 6 | 4 |
| v | r | 5 | 4 |
| w | r | 5 | 4 |
| t | y,r | 6 | 4 |

原完整 stars、原 apex 接觸、h 對 x,y,r 的非邊以及前輪十點相異性，
逐項保證表中沒有其他刪邊。core 私有內點的度數仍為原度數、至少五。

## 2. 任意大小的短弧 pocket 論證

假設 C10 存在 chord uv。取其一條長度 2、3 或 4 的框弧 P。
P 加 uv 是同一原 G 的簡單 C3、C4 或 C5；其 core 側閉 pocket
位於實際 D10 內，沒有被刪除的六點。P 的嚴格中間框點的**全部 core
鄰點**都困在此 pocket，否則某條原邊跨過 uv 或 C10 外框。
這裡不對 chord 的兩個端點施加 pocket 度數上界。

原 C3 必為面、原 C4 有界側空；所以前兩種 pocket 恰是無內點的三角化。
原 C5 定理給兩種完整可能：無內點三角化，或恰一個原五度點且接五框點
的 W5。這保留了原 C5 的完整例外，沒有把所有 C5 都當空圈。

對長度 2、3、4 的弧，分別只有 1、2、5 個無內點三角化及一個 C5 輪。
每個中間點在這些完整填片的度數，必至少是 §1 的 core 下界。
逐一列出的全部 pocket 見 [certificate.json](certificate.json) 的
`geometry.pockets`；checker 直接重建全部填片及度數，包含零可能者。
這個有限列表是任意大小圖論證的局部窮盡，不是有界來源枚舉。

35 個潛在 chords 中，27 個被這條度數／短圈規則排除。
剩下的 `ac,ns` 又分別被原三角面及已證原非邊排除：
若 ac 存在，原 triangle abc 的原外弧 ab、bc 內側至少含互異 p,q，
不可能是面；ns 則是原 low-p 已證非邊。
因此 **D10 的全部可能 chords 僅為**

```
Rv, Ls, Lv, Lw, qs, qt。
```

這是必要 envelope，不宣稱每個子集都有來源實現。

## 3. 剩餘短 chord 的精確原度數代價

* `qs` 的三角 pocket q-c-s 迫 core c 度二，故原 c 度四；反向由原 c
  四度 star 也有 qs。這承接原 apex 定理 `qs iff c=4`。
* 若 `Ls` 存在，原四圈 L-q-c-s 的兩個 triangulations 中，Lc 分支
  使中間 q 的 core 度二，違反 §1；故唯一填片是加 qs。其完整 pocket
  使 q 的 core 度三、c 的 core 度二，故 **原 q=6,c=4**。
* 若 `Lv` 存在，原五圈 L-q-c-s-v 的唯一可用填片是以 s 為扇心，
  加 `Ls,qs`。W5 被中間 s 的 core 下界四排除。完整 pocket 使
  **原 q=6,c=4,s=6**。

以上是必要的單向推論，沒有把不同圖或不同著色的條件拼接。
因此在額外原子分支 `c>=5`，三條 `Ls,Lv,qs` 全不存在；僅可能
`Rv,Lw,qt`。這三個 chord 的端點在 C10 交錯，平面性使其至多一條。
本頁不假設 c>=5；`c=4` 必須保留。

## 4. 完整 fibres 上的作用與兩份控制

令同一 D10 的固定字面完整延拓數是 Z(u)。若其中一條可能 chord ij
實際存在，則每份有 `u_i=u_j` 的完整 fibre 必空：`Z(u)=0`。
這是同一張圖每個完整著色的不等邊約束，保留全部私有點及空 fibres。

checker 用前輪兩份精確控制，對每條上述六個 chord 各求
`sum_{canonical u:u_i=u_j} Z(u)`，不把它當成整個色軌道總數。
兩份控制的每個和都正，因此若任何一份有真來源實現，其 D10 必是
**induced C10**。各和及全部 2,461 格同源讀取記於 certificate。
這是對假想實現的必要條件，不排除這兩份向量，也沒有為它們找到實現。

舊 C10 模型只記錄框邊 properness、平面 span 與分量交換等式；沒有
承諾上述原度數或 chord envelope。原低度定理 q>=6、精確 core 度數
與 pocket 限制是新增顯式真來源結構資訊；沒有證明這些結構條件單獨
足以推出 Q1/Q2 四列合同。allK_source_positive 仍是必要模型的存活控制。

## 5. 量化停止點

本頁新增 `q>=6`、core 邊界度數下界及六 chord envelope，對所有完整
具名來源成立。沒有證明 a1=0、a2=0 或雙正的任何完整拒絕保持分支。
仍須證

`forall G in C941, exists i in {1,2}: ai>0 and ell_i=0`。

這裡四個查詢必在同一 Q_i；本頁沒有用本地 pocket 或控制測試取代它。

本輪後續 [A 的 c=4 排除](../A/PROOF.md)使用同一 core 的完整分量交換，
由原 qs 邊迫原 alpha fibre 空，故對本輪真來源得到 c>=5。結合 §3，
**本輪來源的實際 chord envelope 進一步只剩 Rv,Lw,qt，至多一條**。
B 證書仍保存較弱六 chord envelope 及 c=4 可能填片，未重寫其封存 bytes；
c=4 的來源排除由 A 的獨立證明承擔。

A 又對 Rv、Lw、qt 各自的原邊假設完成同一種完整分量交換排除。
結合本頁 envelope，最後得到本輪每個真來源的 **D10 是 induced C10**。
任意大小的交換橋接、三個額外零 fibre 集與獨立重播都以 A 的證據為準；
B 的有限 pocket 證書不承擔這三條著色排除，也未因後續定理改寫。
