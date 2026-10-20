# J1 五邊路的精確殘餘與同源計數接口

本輪在 BASE `417732fc5ef0a012829fd6712333b1c906128d3a`，僅寫本目錄。
承接[原來源合同](../frozen/audits/2026-10-20-r6-941-fibre-continuation-9c36e3c/frozen/audits/2026-10-20-r6-941-last-rejection-f13eb4d/SOURCE_CONTRACT.md)、
[同染色三分型](../frozen/audits/2026-10-20-r6-941-fibre-continuation-9c36e3c/geometry/PROOF.md)
及[精確殘餘公式](../frozen/audits/2026-10-20-kempe-residual-iteration-af0df80/theory/REPORT.md)。
完整原圖、原框、原附件、完整 stars、旋轉、私有點、全域最小性及原短圈定理均保留。

結果是可用於這一具名五邊路來源的**一般精確 transport 定理**，以及真 disk 的
可重播負控。它把歷史相容性、候選重數與 cap 相容性加入同源計數的義務。
它沒有排除 J1，也沒有給完整來源或一般小狀態界。

## 1. 固定實際來源與五邊路

令 `F=G−{b,p,h,x,y,r}`，原有序 C10 框
`B=(a,n,R,L,q,c,s,v,w,t)`。對一份已選的殘餘完整染色，固定字面列

```
(a,n,R,L,q,c,s,v,w,t)=(0,1,3,2,3,1,2,e0,e1,2),
(e0,e1)=(0,1) 或 (1,0).
```

選 type III 與一條實際簡單五邊路
`P=n–u4–u3–u2–u1–L`，其色依序為 `1,2,1,2,1,2`。
P 的全部點身份與原附件都固定；**一般情況不先宣告所有 ui 私有，也不宣告
C7 內只有 R**。`u2=t` 或 `u3=z1` 等身份必須由同一來源的實際幾何處理。
嚴格的 only-R 子型由[幾何證明](../geometry/PROOF.md)另證四點私有，才可改用
實際 C13 核心 `F*=G−{b,p,h,R,x,y,r}`；本頁不把該子型當一般五邊路。

以下可在 F 上使用原 B，或在已證合法的 F* 上使用完整 C13 框。
固定其中一張實際圖 H 與一份具名有序觀測框 C，令
`X=Col_4(H)` 為**全部原私有點在內的全部字面 proper 完整染色**。
定義 J(c) 為 C 上字面框色及六色對的實際 maximal component 接框分割。
六項均來自同一 c；不能用六份各自可行的染色代替。

令 A5 為 X 中符合所選初始字面框、type III、具名 P 條件的完整染色集合。
若用 F*，初始條件由原完整見證限制，並以其完整 R lift 核對。
A5 可以再按實際初始 J 分桶；它不是 X 的替代品。

## 2. 帶原始身份的精確 transport

對 `a=(ij,root)`，root 取 C 中具名點，令

```
D_a={c : c(root)∈{i,j}},
T_a(c)=在 c 中交換含 root 的全部實際 ij component，c∈D_a.
```

該交換保留 ij induced graph，所以 `T_a²=id` 在 D_a 上成立。
非法動作在其餘座標無像；不能補成合法 self-loop。令 P_a 為這個**部分置換**
的 0/1 矩陣，D_o 為 `J(c)=o` 的對角遮罩。固定原始來源集合 A⊆A5，
已讀歷史 `o0,a1,o1,…,at,ot`，則

```
r0=1_A D_o0,
rt=r0 P_a1 D_o1 … P_at D_ot.
```

這裡 r_t 是確切當前完整染色集合的 incidence。令 F_t 為合法 action 的合成，
原始候選 A_t 是 A 中通過全部 prefix 合法性與觀測者，則

```
R_t=F_t(A_t),  A_(t+1)⊆A_t,  |R_t|=|A_t|.
```

證明是逐步歸納：每一步只搬運已存末端，再用同一完整觀測篩選；不加入其他
末端，也不丟掉符合 prefix 的末端。每個 T_a 單射，故不同原始完整染色仍有
不同末端。可明存 `E_t(x,y)=[x∈A_t,y=F_t(x)]`，或保存歷史後反序執行對合
以回到原始 x。當前 R_t 一般不嵌套；真正嵌套的是 A_t。

若完成圖 cap 造成同一 core 有多個原始完整 lifts，則原始 ID 應為
`(core colouring,完整 cap assignment)`。投影成 core 權重後，r 可為非負整數，
不再保證 0/1；同一部分置換仍精確搬運該權重。不得先丟 lift ID，再聲稱重建了
同一原始完成圖見證。

## 3. 可以加入哪些精確計數條件

令 `q_h=|A_h|=|R_h|`。對固定 action a，所有合法後繼共同觀測形成互斥分桶：

```
q_(h,a,o)=Σ_y r_h(y)[y∈D_a,J(T_a y)=o],
Σ_o q_(h,a,o)=Σ_y r_h(y)[y∈D_a] ≤ q_h.
```

根在觀測框內時，J 含根色，非空 R_h 的合法性一致。全部整數、全部零桶均保留。
在全 X 的 J-fibres 上還可設完整一步聯合計數
`m_(q,a,o)=#{c:J(c)=q,c∈D_a,J(T_a c)=o}`；對合給
`m_(q,a,o)=m_(o,a,q)`。這是同一圖、同一 action 的兩端雙射。
若先篩為 A5 或某段歷史，反向初始條件亦須搬為 `T_a(A5)` 或完整 survivor mask；
不能仍用原 A5 宣稱同樣的對稱計數。

對任意 phase，若用逐候選完整 component 身份算出端點 P_w，則

```
r_end=r_start D_S P_w,
S={phase起點中通過全部 prefix 合法性與共同觀測者}.
```

即使 w=aa，`P_a D_o P_a` 也可能為非平凡篩選器；不能只因端點 parity 為零
就刪中途觀測。多台觀測必須在同一末端列共同測試。

因此可增加的是：**原始完整染色的共同身份、逐步整數質量守恆、全歷史相容性、
實際分量的單射搬運，以及所用 cap 的完整 lift 相容性**。只給一個按 rim 計數
的 Z 向量，通常不足以計算這些條件；至少要有相容的完整染色／聯合觀測分解。
單步邊際各自可行不保證兩步存在同一原始來源。

若要以某個有限探索排除 A5，仍須證明所有初始完整候選都被探索覆蓋，且所有
可執行觀測分支最終落入已證空集或原來源不可能的 fibre。單條歷史的殘餘為空，
只排除該歷史；不是 A5=∅。質量不增加亦不保證嚴格下降或終止。

## 4. 與全源 Z 及 cap 計數的正確接口

[同源計數](../counting/PROOF.md)的 Z_i 是同一實際 F* 在固定字面 rim 代表上的
**全部**完整染色數。選定五邊路完整見證可推出相應 Z_i>0。
但 `Y_(h,i)=#{c∈R_h:rim(c)=i}` 是另一組有歷史遮罩的量，通常既不保全域色
置換，也不是完整互補色對 component-orbits 的聯集。

故不能把 Y 直接代入全源 `AZ=Bβ`、全源 cap counts、全源正性方程或已用 S4
正規化的 Z。完整 Z 仍可滿足那些方程；歷史 Y 只可經第 2–3 節的精確接口與它
聯繫。完整 orbit 證明若要用於 Y，必須另證 survivor mask 對該 orbit 群不變，
或保留 orbit 被遮罩的每個實際位置與重數；後者不再是未篩選的原 columns。

對完成圖 M，令 `K_M(c,ρ)` 是在 core 完整染色 c 上，按原 stars/識別映射
接回所有刪點、且得到固定字面完成框 ρ 的**完整 assignment 集合**。則

```
C_(M,h)(ρ)=Σ_c r_h(c) |K_M(c,ρ)|.
```

這是「當前 selected core 上的所有完成」的精確計數。它不能自動理解為
原來那些 M 完整染色經 action 搬運後的數量。要作後一解讀，需要明列 lift
bijection U_a，使下面交換圖成立，且保留原始 lift 身份：

```
π U_a = T_a π,      U_a : 完整M合法域 → 完整M合法域,
```

其中 π 是 restriction。完整圖 Kempe swap 可能經 cap 點連接 core 的不同分量；
其 restriction 一般不是 core 上同 root 的 Kempe swap。甚至
`|K_M(T_a c)|≠|K_M(c)|`。若沒有相容 U_a，只能把原 lift 權重當作原始身份的記帳，
或重新計算當前完整 K_M；前者不保證當前仍有合法 M lift，兩者不可混作同一 conserved count。

## 5. 真 disk 重播與負控

[check.py](check.py)只用標準庫，從原邊重枚舉，沒有匯入舊 transition table、
舊完整染色或 cell95 的候選數界。第一片為實際 W7 輪，rim
`(n,h,L,u1,u2,u3,u4)`、中心 R；第二片為凍結八點 disk 的九個三角面，
沿 hL 邊接合。得到 14 點、29 邊、16 三角面及有序十框
`(n,h,d4,d3,d2,L,u1,u2,u3,u4)` 的真 disk。它保留具名五邊路，
但**不是完整 J1 來源**，沒有補造原 C10、原接受／拒絕與全部全域來源條件。

獨立枚舉得到 11088 份完整染色，8064 個完整 J 類；60 個 rooted actions 共
332640 個合法完整染色 action 邊均逐一核對對合。刪 R 後的 48048 份完整 core
與完整 R star lifts，接回集合恰等於直接整圖全部染色。這張 local disk 的完整
R star 含 h，恰為七個輪框鄰點；它與 F13 cap 的六個 rim 鄰點加另枚舉的
h 變數是不同的 restriction 合同。
全部 59052 個 proper 字面外框均保留，其中 53004 個完成 fibre 為空。

證書保留兩份同初始 J、同字面五邊路的完整候選。對 `a=(12,L)`，讀第一個
後繼觀測得到候選數 `2→1`，再做 a 回到原圖染色但仍只留一份；第三次 a
若聲稱另一分支觀測，得到 `2→1→1→0`。只用 aa parity 會補回第二份。
另存以下獨立可重算負控：

- 不搬運就套新觀測：錯得 0，正確為 1。
- 補滿整個新 J-fibre：加入一個反序不來自原集合的假來源。
- 六項觀測各自借 witness：各座標有見證，但整份共同觀測沒有任何完整染色。
- 把非法 action 當 loop：錯收 2，合法成功歷史實為空。
- 漏掉 R–u3 一項原完整 star：加入一份違反實際原邊的假 cap lift。
- 假設 restriction 與 Kempe 交換：完整圖和 core 後繼不同，而且完整 R cap
  重數由 1 變 0；因此不存在所假設的 lift bijection。
- 將 selected fibre 當全源：兩個全域 0↔1 換色的字面框，全源數同為 3；
  selected 數卻為 2、0。全源 S4 正規化及完整 orbit 等式不能直接用於它。

所有數字僅屬這張真 disk。它不提供一般圖的 fibre 上界、一般壓縮、
一般五邊路覆蓋、J1 排除或較小 bad。

## 6. 停止點

一般來源尚需：處理 C7 內多點／可能的原框接觸；對欲使用的 action 證明實際
分量或保留足夠完整描述；建立與全 Z 同時相容的歷史分解；若用完成圖上的
舊見證則補完 cap-compatible lift transport；最後給覆蓋所有候選的正計數矛盾
或完整來源下降。這些不是單靠 `R_next=T_a(R)∩J^-1(o)` 自動成立的結論。

一般精確更新紙證完成；有限控制的 full lifts、所有空 fibres 及負控已核對。
真 J1 來源 `not triggered`，一般來源排除、較小 bad 與新 Lean 仍 OPEN。
重播及證書破壞負控見 [checks.json](checks.json)。
