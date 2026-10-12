# 全內部 degree-five wheel：完整 fibres 與局部識別界線

本檔只處理本輪已推出的窄出口：內點 `v` 的五個鄰点全為原內點，依平面
rotation 記作 `u0,...,u4`，link 為 induced C5。所有十列均保留原外框
`(0,1,2,3,4)` 及同一色框。有限控制見
[`degree5_local.json`](../controls/degree5_local.json)，獨立 product／MRV checker
見 [`degree5_local.py`](../controls/degree5_local.py)。

## 1. 精確恢復條件，以及兩種識別的不同問題

令 `D=G-v`。對每個原外框列 `p`，保留其全部 `D` 完整染色 `F(p)`。
因 link 是奇五環，每份 `f` 在 link 上恰用三色或四色，並有

\[
 p\in\Sigma(G)\iff
 \exists f\in F(p):\lvert f(\{u_0,\dots,u_4\})\rvert=3.
\]

三色情形中心有唯一可用色。令
`E_i(f) := [f(ui)=f(u(i+2))]`，下標均模五。十種 link orbit 的完整核對顯示：

* 三色 link 恰有兩個 `E_i=1`；兩對端點互不相同，且沿 link 交錯。
* 四色 link 恰有一個 `E_i=1`。

因此五個 single quotient `Q_i=D/(ui=u(i+2))` 都是合法的較小 C5 disk
來源，但其完整 fibre 精確等於 `F(p)` 中 `E_i=1` 的部分，其中仍可能有
四色 link。刪中心之後少一內點，再識別少一內點。可確定

\[
 \Sigma(G)\subseteq\bigcup_{i=0}^4\Sigma(Q_i),
\]

卻不能刪掉「link 恰用三色」的恢復條件而宣稱等號。

若同時施行某個三色 link 的兩對等色識別，則著色層面確實保留恰可恢復
中心的 fibres，五個 double quotient 的關係聯集精確等於原 `Sigma(G)`。
但兩組端點交錯，不能在原 vacated disk 中以互不相交的識別路徑完成。
下面更給出五個所得抽象圖全都 nonplanar 的控制。因此它們不自動屬於
允許套用目錄最小性的 disk 來源。

## 2. 同時滿足度數限制的六內點控制

`ICO-ANNULUS-K6` 的外框是 `0,...,4`，內圈是 `5,...,9`，中心是 `10`。
保留兩個五環、五條中心 spokes，並加

```
(i,5+i), ((i+1) mod 5,5+i)       (i=0,...,4).
```

這是 simple chordless-C5 near-triangulation，所有外點 degree 四，六個
內點全 degree 五，中心的 induced 五環完全位於原內部。原關係是 `1023`。
五個合法 single quotients 的完整關係依次為

```
231, 977, 636, 442, 783.
```

每個都嚴格丟失原接受列。五者聯集恰為原關係，故此控制只反駁「任一單個
鄰域識別便保持完整 Sigma」；它沒有反駁聯集縮減對這張圖成立。

另一方面，對五種三色 link 分別施行兩對識別，所得五張八頂點圖均經
NetworkX 檢查為 **nonplanar**，並各保存一份 literal K5 subdivision：十條
branch paths 逐邊核對，且所有路徑內點互斥並避開五個 branch vertices。
完整 quotient fibres 與拉回的同名 `D`
fibres 逐列相等，其關係聯集亦精確為 `1023`。著色條件完全正確仍不足以
使這五張 quotient 成為 disk 來源。

本控制是目錄內來源，並非最小目錄外來源；後者為 **not triggered**。

## 3. 五個 single quotients 的聯集也可能新增列

`WHEEL-QUOTIENT-LEAK-K6` 使用同樣兩個五環和中心 spokes，改用附件

```
05, 08, 09, 15, 25, 26, 36, 46, 47, 48.
```

它仍是六內點 simple chordless-C5 near-triangulation，中心仍 degree 五，
link 仍是全內部 induced C5。但本控制不主張滿足最小來源的度數界。

原完整關係為 `887`；五個合法 single quotients 依次為

```
854, 567, 997, 854, 567.
```

其聯集是 `1015`，新增原拒絕列 `01213`。具體 `Q_2` 識別 `7=9`，
保留原 `p*=01232` 染色

```
(0,1,2,3,2, 3,0,1,3,1, 2)
```

在刪去中心後的下降，但 `Q_2` 同時丟失 `01021,01202` 並新增 `01213`。
新增列的所有拉回 fibres 都在 link 用四色，故無法恢復中心；原 `01213`
fibre 為空。這裡不是只保留一列的 marginal，而是 JSON 保存每個原列的
全部 source、deleted-source、quotient、pulled-back、可恢復與不可恢復 fibres。

本控制同樣在目錄內；933／941 目標來源為 **not triggered**。它反駁一般
single-quotient 聯集公式，沒有排除最小目錄外來源上利用額外結構的更強縮減。

## 4. 最小目錄外来源上的精確反向見證

還可沿用既有 finite subcone 事實：對共同 D5 對齊後的
`R in {933,941}`、`p*=01232`，不存在 `S in K` 滿足 `p* in S subset R`。
參見既有
[`rewire_analysis.md` §3.1](../../2026-10-12-cofacial-uniform-separation-eb6b2303/review/rewire_analysis.md)。

固定最小目錄外 `G` 的任一 `p*` 完整染色。它在本輪 deep wheel 上恰有兩個
等色對 `E_i=1`。對每一對，原染色下降到合法較小 `Q_i`，所以
`p* in Sigma(Q_i) in K`。因此各自存在原拒絕列

\[
 p_i\in\Sigma(Q_i)\setminus R.
\]

把該列完整染色拉回同一 `D`，link 必用四色，否則可恢復中心，與 `p_i`
被原圖拒絕矛盾。因此它的唯一等色對就是所選的 `E_i`。

這給每份原 `p*` 延伸的兩個精確反向見證；不保證兩者是同一原拒絕列，
更不保證它們是同一份完整染色。單輪的必要關係尚未給出縮減。

## 5. 核對與範圍

```
python3 controls/degree5_local.py --check controls/degree5_local.json
```

需環境提供 NetworkX。所有十列包含空 fibres，先以直接笛卡兒積、再以独立
MRV 回溯核對；兩張 source 及十張 single quotients 均核對外側 apex 平面性；
五張 ICO double quotients 均核對非平面性及 literal K5 subdivision。每個 quotient 的完整染色都拉回
原命名頂點並與對應 equality fibres 比較。未聲稱 source 933／941 被觸發、
未證一般縮減、未新增 Lean theorem。

normal、`PYTHONHASHSEED=17` 均通過；故意損壞一份 pulled-back full lift 的
證書被 checker 拒絕。實際測試用 NetworkX 3.6.1，結果及三態標示保存在
[`local_wheel_checks.json`](local_wheel_checks.json)。三個過強的一般縮減主張為
`counterexample`，完整 fibre 與 K5 路徑核對為 `triggered and holds`，完整
outside-K source 為 `not triggered`。
