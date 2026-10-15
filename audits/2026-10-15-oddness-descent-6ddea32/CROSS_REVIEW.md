# 第二輪只讀交叉審查

2026-10-15。只讀被審兩組交付；本檔與重播 logs 只寫 oddness-descent
獨占目錄。被審檔 SHA256、命令、exit、耗時與前後 drift=0 見
[CROSS_VERIFICATION.json](CROSS_VERIFICATION.json)。

## 1. 720-state Kempe compatibility

已讀對方 [PROOF](../2026-10-15-kempe-compatibility-6ddea32/PROOF.md)、
[REPORT](../2026-10-15-kempe-compatibility-6ddea32/REPORT.md)、完整
[checker](../2026-10-15-kempe-compatibility-6ddea32/check.py)。
正常及 seed17 獨立只讀重播均 exit0、stdout相同。

採納其明列抽象公理界線，未見阻擋問題：

- 每state是固定layer與單份字面七pin列，三個complementary pairings
  的六份terminal partitions確實同時存於該state，沒有逐色對換state。
- 全部component子集的target id存在、同pairing partitions不變；直接
  table replay核每個bitmask及XOR組合，因此包含可逆性、可交換性。
- S4同時作用全state的七個字面顏色，搬運pairing、partition及各單步
  switch；proper C5至少三色確保每canonical row的S4 orbit自由。
- 同一pair的全部blocks之product正是整體該兩色交換。此模型的components
  全可見；文中明列真圖可以有hidden components，沒有把無hidden當來源前提。
- 全4^7賦色的all-r predicate與凍結原實作逐列比較；沒有合法r色時
  for-loop不排該列，故保留原universal空量詞義務。
- support完整等於舊22列固定點，外框mask319；不是只保留一個子集合。
- 七頂點非實現控制成立：容納全部支持列的任意原邊只能落在共同
  inequality骨架，而ABABCBD已proper著色整骨架且不屬支持。此論證
  只排「恰七頂點、無額外內點」的精確關係實現。

採納結論：這份明列交換公理系統不能再刪上述22列。不能採納更強的
「六色對components已由同一原圖實現」；checker未保存共同hidden頂點、
原邊incidences或那些邊在重疊色對交換後的行為。報告已正確保留這個
區別及完整來源not triggered，未把720states作真圖反例。

## 2. COUNT_BRIDGE

已讀 [COUNT_BRIDGE](../2026-10-15-route-round2-6ddea32/COUNT_BRIDGE.md)
及完整 [check_counts.py](../2026-10-15-route-round2-6ddea32/check_counts.py)。
正常及seed17獨立只讀重播均 exit0、stdout相同。

紙面三步均成立：

1. H是保留同a色原邊的spanning子圖，孤立點保留。其邊數n−2；刪掉
   原跨色邊造成的原三角面合併，恰由Q−M的連通分量描述，即H的面數c。
   不連通平面Euler式給n−(n−2)+c=1+κ，所以κ=c+1，無需偶補前提。
2. 同一a的兩個誘導圖皆二分時，每連通分量恰兩份b，固定根b=0後
   恰2^(κ−1)=2^c；否則空。根未固定才是2^(c+1)，文稿區分正確。
3. 全部標籤Tait染色中，e色α、f色β的列整體交換α與β，落到反方向；
   在image以e色再交換即復原。故兩方向Σ2^c相等；沒有要求每份
   匹配對應反方向一份相同環數匹配，也沒有把相等升格成正值。

checker從根固定a與b完整列舉並和獨立原圖四色DFS逐tuple比較；
同時核每份M的2^c及全部邊對的逐Tait列involution。因M對應α=1的
匹配，每份Tait列被計數一次，無額外×2或×3因子。輸入的球面性
由定向面接合、每點link及Euler核對。原空b fibre列保留。

採納一般計數橋及有限完整控制；不採納普通PM正值推出加權偶補正值。
來源ω=0、完整319來源排除、一般主命題仍OPEN。
