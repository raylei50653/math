# 同一具名原來源的 C10 核心與全部獨立 cap lifts

這是任意大小原來源的幾何引理。所有原前提及逐份 BASE SHA 見
[來源契約](SOURCE_CONTRACT.md)及 [additional-inputs.json](additional-inputs.json)。
它把先前 C8 必要控制尚未使用的完整 r、x、y stars 轉成共同 C10 介面；
引理本身不宣稱任何抽象 C10 關係可由原來源實現。

## 1. 十個接口點確實互異

使用同一原圖，令

```
D10=G-{b,p,h,x,y,r},
C10=(a,n,R,L,q,c,s,v,w,t).
```

原 E 的前六點 `(a,n,R,L,q,c)` 已互異且 n,R,L,q 全是原內點。
原 r link `(x,y,t,w,v,s)` 是簡單 link，所以 s,v,w,t 互異並全是原內點。
只需排除兩組原內點的重疊。

1. q 不等於 s,t，因為五 apex 互異；q 不等於 v,w，因為原 rq 非邊，
   而 rv,rw 是原邊。
2. n 不等於 s，因為 pn 是原邊而 ps 是原非邊。n 不等於 t，因為
   low-p 原 fan 中 `n=t iff d_G(a)=4`，但來源已證 a>=6。n 不等於 v,w，
   因為 pn 是原邊而 pv,pw 是原非邊。
3. h 不等於 r,s,t，因為原度數 h=5、r=6、s,t>=6；h 不等於 v,w，
   因為 ph 是原邊而 pv,pw 是原非邊。已有圖非邊 hs,ht,hv,hw；完整
   r star 又給 hr 為非邊：h 已排除其全部六個鄰點身份。
4. L,R 是 h 的原鄰點，故不能等於 r,s,t,v,w，否則會給前一步已排除
   的原邊。L,R 與 q,n 相異則是原簡單 h link 及六圈的身份條件。

因此 C10 的十點互異，不需額外有限來源或無重疊假設。
第 2 項的 n=t 判準見
[cofacial low-p:41–47](../../2026-10-14-cofacial-fibres-676b102/pq/PROOF.md)；
其餘原圖事實及來源逐項見 [契約 §2–3](SOURCE_CONTRACT.md#2-原附件完整-stars原旋轉)。
這份證明不把兩份舊存在著色當成同一份著色；只共同使用它們已證的圖非邊。

## 2. D10 是實際三角化 disk，並非抽象十接點

同一 E 的實際外框為 `(a,n,R,L,q,c,x,y)`。原完整 r、x、y stars 給出
沿 E 外弧 a-y-x-c 的一塊 disk，其其餘邊界恰為原簡單路

```
a-t-w-v-s-c.
```

具體地，這塊 disk 的八個三角面為

```
ayt, ytr, yrx, xrs, xsc, rtw, rwv, rvs.
```

其中外框為 `(a,y,x,c,s,v,w,t)`，內點恰為 r；x,y 是該塊外框上刪去的
兩點。這八個原面由完整 stars 指定，沒有其他原面或私有點夾在其中。
第 1 節的相異點證明保證這塊 disk 的內側路除 a,c 外，不接觸 E 的另一
條外弧 a-n-R-L-q-c。沿外弧 a-y-x-c 刪下此塊，餘下閉片就是實際 D10，
其外框依序為 `(a,n,R,L,q,c,s,v,w,t)`。其他原邊、內面、全部私有點均保留。
故 D10 是簡單三角化 C10 disk；不需要 C10 induced，可能的原 chord 仍保留。

點數核算：G 有 k+5 點，刪六點後 D10 有 k−1 點，框長十，故 D10 有
k−11 個內點。這不是完成 C5 候選的成本；若以 D10 製造任何新 C5，仍須
逐項計回其接回及換框成本。原三候選完成數保持 k−4,k−4,k−2。

## 3. 全部 cap 邊及同一完整著色的 Cartesian lifts

G 從 D10 接回的兩個點集是 `{b,p,h}` 與 `{x,y,r}`。每條失去的原邊
恰在以下兩份清單中出現一次：

```
left:  ba,bc,bq,bp,pa,pq,ph,pn,hq,hL,hR,hn;   (12 edges)
right: xy,xc,xr,xs,ya,yr,yt,rt,rw,rv,rs.      (11 edges)
```

沒有左右 cap 間的原邊。b 的完整 star、p 的完整 star 直接排除所有此類
邊，h 對 x,y,r 的非邊已在第 1 節及 E 幾何中證明。
加邊數 23 亦與兩張三角化 disk 的 Euler 公式相符：
`(3(k+5)-8)-(3(k-1)-13)=23`。

固定**一份** D10 的完整著色 f，字面接口色寫作
`(A,N,U,V,Q,C,S,I,J,T)=(a,n,R,L,q,c,s,v,w,t)`。
這裡 U,V 只是 R,L 的顏色，避免原點 R 與原中心 r 的顏色混淆。
令顏色全集為 K={0,1,2,3}。兩 cap 的全部合法 assignments 為

```
Left(f) = {(B,P,H) in K^3:
 B not in {A,C,Q,P},
 P not in {A,Q,N,H},
 H not in {Q,U,V,N}};

Right(f) = {(X,Y,Z) in K^3:
 Z not in {S,I,J,T,X,Y},
 X not in {C,S,Y},
 Y not in {A,T}}.
```

每份集合包括全部 assignments，尤其保留空集合。右集合中 Z 是原 r 的
色值；X,Y 是原 x,y 的色值。左右各條清單不等式恰覆蓋其所有 incident
原邊，且沒有一條左右交叉邊。因此完整原 G 的接回 fibre **等於**

```
Left(f) × Right(f).
```

這是逐份完整 f 的等號；沒有任意選擇 cap 顏色，也沒有把兩份 f 的邊界
投影相乘。原十列計數是在全部 f 上，按 `(X,Y,A,B,C)` 的字面列把這個
Cartesian product 的全部成員分組求和。

同樣，完整 E 由 Right(f) 的全部 assignments 接回；b,p,h 仍刪除。
因此三個候選共用**同一份** f 與同一個 Right(f)，左側改成

```
Q1(f) = {B in K: B=N, U=Q, B not in {A,C,Q}},
Q2(f) = {B in K: B=N=V, B not in {A,C,Q}},
GB(f) = {B in K: B not in {A,C,Q,N,U,V}}.
```

Q1,Q2 是沿實際商映射拉回；GB 是實際 fan 三條新邊的不等約束。
每個候選的完整著色恰對應其上述左集合與 Right(f) 的乘積，再遍歷同一
D10 的全部完整 f。商圖頂點可能合併接口點，但同色 pullback 保留 f 的
全部私有顏色，故這是雙射而非只有支援包含。

## 4. 對前輪控制及新方法的限制

前輪 C8 計數、Kempe 交換必要錐及 91 維平面 span，沒有記錄同一 E 必須
有這一塊包含 r、x、y 的**固定實際 cap**。每份原來源 E 的完整 C8 計數
必須由某一張共同 D10 的完整計數，透過第 3 節全部 Right lifts 取得。
共同 D10 本身亦有平面邊界分量的必要線性與 Kempe 條件。

所以新增這個介面時，必須把先前 941 控制向量逐份拿來檢查；舊 C8 控制
若不能通過共同 C10 cap 方程，僅排除該控制，不能直接排除原來源。
反之，即使新必要系統可行，仍未獲得實際 D10、同一原來源、或保壞構造。
這個幾何引理只提供可合法加入的來源前提及其全部 lifts。

## 5. 獨立有限介面核對

[check_core.py](check_core.py) 不匯入 A、C 或前輪程式，逐一重建所有 2,461
個 proper C10 色軌道。對每列，直接以 23 條原 cap 邊枚舉全部 `(b,p,h)`
及 `(x,y,r)`，與第 3 節完整集合逐份相等，並對每個 Cartesian 乘積成員
再核對全部 cap 邊。其 [core-certificate.json](core-certificate.json) 保存
所有列的全部左右 lifts 及三候選 b lifts，空者以空列表保留。
它們是原 cap 介面的完整代數，不是 2,461 份來源著色或來源實現。

正常與 seed17 的唯讀重播皆 PASS：1,216 列的 Left 空，820 列的 Right 空，
全部列合計 1,728 個因子乘積成員。證書 SHA256 為
`15954b972d430691dcb9ae8914276f551642ad49ee9438442536dfebb6fa99b6`。

四個具體負控制保留：漏掉原 rw 邊會引入假 right lifts；漏掉原 pn 邊會
引入假 left lifts；Q2 的 a=q=R 存在合法原 lift；一列只有 Left 非空、
另一列只有 Right 非空，跨列相乘會憑空產生不存在的同列原著色。
這些控制各自針對原附件、完整回填分支及同一份完整來源的實際論證風險。

```
python3 -B audits/2026-10-19-r6-941-leakage-b89c591/B/check_core.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-19-r6-941-leakage-b89c591/B/check_core.py
```

預設只讀；`--build` 只允許 exclusive-create，不覆寫已存證據。
`--certificate PATH` 可供父層以損壞副本核對拒絕，不改寫本證書。
