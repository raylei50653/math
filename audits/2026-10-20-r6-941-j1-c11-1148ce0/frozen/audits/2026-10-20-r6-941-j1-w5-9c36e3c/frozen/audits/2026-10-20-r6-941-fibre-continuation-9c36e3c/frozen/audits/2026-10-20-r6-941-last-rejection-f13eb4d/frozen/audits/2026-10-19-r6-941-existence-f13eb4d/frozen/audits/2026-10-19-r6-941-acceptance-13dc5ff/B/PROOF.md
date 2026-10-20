# B：原 n 五度迫 a 至少七度，且 t、R 距離至少三

固定 BASE `13dc5ff163045c85b5c82dde438eb5f275dab999`；本輪承接未提交
但已逐份凍結的 406 份輸入，不以 HEAD 代替其 bytes。完整原來源、旋轉、
全部附件、私有點、原 C3/C4/C5 定理、原全域最小性及支持恰為 941，逐項
承接[完整來源契約](../../2026-10-19-r6-941-quotients-13dc5ff/SOURCE_CONTRACT.md)。
特別保留原 `d_G(p)=d_G(h)=5`、`h=ell`、原 `n` 是 p link 中的點而非任何商點，以及
同一原框 `(x,y,a,b,c)`。本頁不使用 active-f matching。證書 scope 欄的 `p=h=5` 只縮寫這兩個原度數等式，不識別原相異點 p,h。

本頁在這個任意大小真來源域新增兩個原圖結論：

```
d_G(n)=5  ==>  d_G(a)>=7,
dist_G(t,R)>=3.
```

這不排除 n 五度本身；同一接受候選三拒絕、較小 bad 及一般來源仍 OPEN。

## 1. n 五度的實際十圈介面

舊完整 stars 給原面 `apn,pnh,hnR`。若原 n 五度，其原簡單 link 因而是
`(a,p,h,R,u)`，或全體同時反向。只有一個中間點 u；完整原鄰點恰為
`{a,p,h,R,u}`，原面 `anu,nRu` 也隨之確定。這不假設其他點沒有附件。

舊實際核心 `D10=G-{b,p,h,x,y,r}` 已證有 induced rim
`(a,n,R,L,q,c,s,v,w,t)`。u 不是 a 或 R，且不能是其餘任何 rim 點：
否則原邊 nu 是這個 induced C10 的 chord。u 也不是已刪 cap 點：原簡單 n link 排除 p,h；原 nb 非邊排除 b；完整 x,y,r stars 均不含 n，故排除 x,y,r。因此 u 是 D10 的私有內點。
刪 n 正好剝下兩個原面 `anu,nRu`，以原簡單路 a-u-R 取代 a-n-R，得到
實際三角化 disk

```
F=G-{b,p,h,n,x,y,r}, outer(F)=(a,u,R,L,q,c,s,v,w,t).
```

十點互異，其他原邊和每個其他私有點均保留。這不是任意十點的抽象關係。
G 有 k+5 點，F 有 k−2 點，故 F 的內點數為 k−12。這只是共同核心的
大小；本頁沒有把它當成完成 C5 候選，也沒有聲稱製造較小 bad。

若另有原 a=6，則 a 在舊 D10 的度數正好為三：其刪失鄰點恰為 b,p,y。
已知三個 core 鄰點 t,n,u 互異，故原框點 a 的完整有序 link 路徑為
`(y,t,u,n,p,b)`。原面 atu 因而給出**實際原邊 ut**。F 的 rim 不必
induced；這裡恰需要保留 ut 這一條 chord。

## 2. 全部完整 F fibres 的七點接回

固定同一份完整 F 著色 f，包括它的全部私有點。f 的十個接口色依序是
`(a,u,R,L,q,c,s,v,w,t)`。兩側 cap 的完整原邊分別為

```
left: ba,bc,bq,bp,pa,pq,ph,pn,hq,hL,hR,hn,na,nR,nu;
right: xy,xc,xr,xs,ya,yr,yt,rt,rw,rv,rs.
```

左側全部接回是 `(b,p,h,n)` 滿足

```
b outside {a,c,q,p}, p outside {a,q,n,h},
h outside {q,R,L,n}, n outside {a,R,u};
```

右側全部接回是 `(x,y,r)` 滿足

```
r outside {s,v,w,t,x,y}, x outside {c,s,y}, y outside {a,t}.
```

原完整 stars 及原非邊保證沒有左右 cap 交叉邊。每份原完整 G 著色因此
與固定同一份 f 上這兩個**全部**集合的 Cartesian product 逐份雙射。
空集合保存為空，不能將兩份不同 f 的非空側相乘。假設 a=6 時 ut 是
F 保留的原邊，故所有 f(u)=f(t) 的完整 F fibres 必空。

[cap-lifts.json](cap-lifts.json) 保存全部 2,461 個 proper C10 字面色軌道
的兩側完整 assignments，包括空者。checker 逐一以 26 條原 cap 邊直接
核對上面兩組公式，並對每個 product 成員重新檢查全部原 cap 邊。

將每個接回成員按同一框 `(x,y,a,b,c)` 的十列字面順序分組，就得到
[certificate.json](certificate.json) 的完整原計數矩陣 M。全圖色置換
作用於每份完整著色；若 core 只用 d 個顏色，固定 canonical core 的
cap assignments 有 `(4-d)!` 個未用顏色置換重數。原 C5 字面列均用至少
三色，stabilizer 為一，故各格除以這個 core 重數，得到固定字面 fibre
計數。checker 精確檢查每格整除，不把軌道總數當成單一字面計數。

## 3. 任意大小的分量交換排除

對這個實際 F 使用[前輪三角化完整分量分割定理](../../2026-10-19-r6-941-quotients-13dc5ff/A/PROOF.md#3-三角化給出的完整分量邊界分割)：
在一份完整著色及固定互補色對分拆中，實際邊界分量分割必 noncrossing、
同側相鄰點同塊，且塊數等於 side 轉換次數的一半加一。每組邊界分量
的全部交換仍是同一 F 的完整著色；不拼接其他色對的獨立路徑。

checker 從凍結程式重建全部 59,052 個 proper 字面列、7,382 個 H 軌道
及 10,798 個容許交換 columns。所有實際分割都包含其中；未實現分割
只使這個必要 family 更寬。原三拒絕 `01021,01202,01212` 的 cap 矩陣
非負，所以某格能接回任何拒絕列時，該完整 F fibre 必空。a=6 分支另
將 u=t 的格置零，除此之外沒有任意刪除可能正格。

若某個 live 格的一個 H 軌道，沒有任何交換 column 完全留在當前 live
集合中，則任何假想完整著色的實際分割會產生一份已證空 fibre，矛盾。
每輪只用前一輪的空格，同時刪除該輪各格；每格均保存 H-row witness。
checker 另逐份驗證 witness 的**每一個**相關 column 都被前一輪空格
阻斷，沒有循環引用。

| 原假設 | 初始 live | 各輪刪除數 | 最後 live | 原 G 投影上界 | alpha 正格 |
| --- | ---: | --- | ---: | ---: | ---: |
| n=5 | 2183 | 128,42,8 | 2005 | 941 | 36 |
| n=5,a=6，保留實際 ut | 1452 | 322,178,81,49,40,26 | 756 | 429 | 0 |

第二列的每個最後 live 格對原固定 `01232` 的完整 cap 係數皆為零，
所以 `N01232(G)=0`，違反原完整支持恰為 941。因此排除原 n=5,a=6。
原已知 a>=6 便給 **原 n=5=>a>=7**。

第一列是範圍控制：此必要零閉包仍留原 alpha 36 格，不能宣稱 n=5
本身已排除；這 36 格也不是一張真來源或一份完整正計數控制的實現。

## 4. 同一原圖 t、R 的距離

舊 induced C10 先給 tR 非邊。若 D10 存在共同鄰點 z，z 不能是 rim
點，否則 t-z 或 R-z 是原 C10 chord；所以 z 是私有內點。原簡單 C5

```
(t,a,n,R,z)
```

的 bounded pocket 在 D10 內，沒有任何已刪 cap 點。a,n 的全部 D10
鄰點都困於此 pocket。原短圈定理給空三角化或單個 W5 兩種完整情形。

空五邊形的五種三角化中，任何 t-n、t-R 或 a-R 對角線都是舊 C10
chord，故唯一可用填片是以 z 為扇心加 z-a、z-n。這使 a,n 的 core
度數均為三。W5 例外也使這兩個 pocket 框點度數均為三；不能把 W5
省掉，但它給同一必要度數結論。因此兩種情況都迫原 a=6,n=5，已被
§3 排除。故 D10 中 t,R 沒有共同鄰點。

原 G 另外六點 `{b,p,h,x,y,r}` 也沒有任何共同鄰點：b,p,x,y 的完整
stars 各排除同時接 t,R；h-t 是原非邊；r-R 由完整 r star 排除。
因此原 G 中 t,R 既無邊也無共同鄰點，得到 **dist_G(t,R)>=3**。

[certificate.json](certificate.json) 完整保存五種空填片及 W5 度數，
程式重播這個局部窮盡；共同鄰點在何側、全部 core 鄰點被 pocket
困住及原 degree 損失由上述實際嵌入論證承擔。

## 5. 重播與停止點

```bash
python3 -B audits/2026-10-19-r6-941-acceptance-13dc5ff/B/check.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-19-r6-941-acceptance-13dc5ff/B/check.py
```

預設唯讀，標準庫，不連網；`--build` 只 exclusive-create。八個負控制
涵蓋原 nu 邊、完整 cap lift、a=6 的實際 ut、交換輪 witness、W5 例外、
n=5 未排除邊界、core 刪除成本及誤升級主目標，均須拒絕。

舊 `allK_source_positive` 是舊 C10 的計數控制；它沒有宣稱一個原 n=5
位置、其新增私有 u 或此處新 core 的完整 fibres，故本頁 n=5 分支對它
標為 **not triggered**。不能從這個條件性排除宣稱一般 allK 控制失效。
本頁沒有建立任一新較小 C5 的完整支援證書，沒有來源實現、Lean 定理、
一般來源覆蓋或新的 k 下界。同一張接受候選的三拒絕仍 OPEN。
