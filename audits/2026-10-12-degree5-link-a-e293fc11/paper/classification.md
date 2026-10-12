# 任務 A：degree-5 link 的位置與完整具名替換

本稿只依 `INPUTS.json` 凍結的 BASE 前提。它是條件來源的紙面定理；
沒有聲稱 933／941 的實際來源已存在。幾何控制與紙面定理分開。

## 1. 來源、link 與三角形

固定原具名外框 `B=(a,b,c,d,e)`，原內點 `v` degree 五，原循環鄰點 `L`。
來源是在所有目錄外 disk 圖中先最小化內點數，再最大化邊數者。
沿用 BASE：簡單、二連通、B induced、所有內面三角形，`k(G)≥13`，
外點度數至少四、內點至少五，C4 完整關係有至多三內點代表，
以及 `K≤12=K` 和每個 K 關係至多五內點的 C5 disk witness。
screen／4CT／外部 Dvořák–Lidický 計算定理仍是上游依賴，沒有重證。

先重證本輪使用的三角形排除。任意原簡單三角形 T 的有界內部不能包含頂點。
若包含，它們皆不是原 B 點：B 點沿外側接到無窮遠，不可能嚴格落在一個
位於原 disk 內的 Jordan 曲線裡。刪去 T 內部頂點及邊得到較小 disk 圖。
原來源至少有一份四色著色（上游必要 screen 已給接受列）；固定其 T 內部著色。
任意刪除後的著色在 T 上有三個不同顏色，用一個全域色置換對齊此固定內側著色，
便可接回。限制與接回證明完整 Σ 相同，違反全域內點最小性。
這也適用於碰到 B 的三角形，不需要 edge-critical、deficiency 或 Gallai 前提。

簡單圖使五個鄰點互異；內點 v 周圍每個面都是三角形，故原 rotation 中的
連續鄰點有原邊，形成簡單 Jordan C5 `L=(ℓ0,…,ℓ4)`。
五個面 `(v,ℓi,ℓi+1)` 填滿 L 所圍的 star disk D_L，其內只有 v。
若 L 有非連續點間 chord `ℓiℓj`，它不能穿過已填滿的 star 面；
三角形 `vℓiℓj` 的兩個 v 扇區各有另一鄰點，故其有界側至少有一個頂點。
有界側的該點不能是外框點，與前段矛盾。因此 **L induced**。
此論證不曾把 L 當成完全內部五環；L 可以與 B 共點、共邊。

## 2. 接觸分類的完整規則

令 `S=V(B)∩V(L)`、`m=|S|`。為敘述幾何，先沿各自有界 disk 同一方向遍歷
B 和 L；若原具名 L 清單採反方向，保存方向符號，所有公式仍用原點名。
這是記錄 traversal 的選擇，不是把不同圖、不同色框或附件另行正規化。

接觸點沿兩圈有相同循環次序。可在每個接點周圍取小 disk，將 L 稍向自身
內側推開，並用不交叉的短弧連回接點；disk 中不交叉接觸弧不能交換端點順序。
同理，兩個接點之間的兩條圈弧只能圍住它們之間的外側區域，不能跨過另一接點。
兩圈共邊時，兩個有界 disk 位於邊的同側，所以兩種同向 traversal 沿共邊同向。
這也排除了 m=2 時把一條實際共邊誤配給另一條長弧的退化畫法。

對 m≥2，按此共同順序寫接點 `s0,…,s(m−1)`，令相鄰接點間的 B 弧長為 pi，
對應 L 弧長為 qi。則

```
sum pi = sum qi = 5;   pi,qi≥1;
pi=1  ⇔  qi=1;
otherwise pi,qi≥2.
```

理由：相鄰 B 點間的原邊若不在 L 上便是 induced L 的 chord；
相鄰 L 點若不是 B 的相鄰點便是 B 的 chord。共邊方向再決定是哪個 gap。
對每個 `(pi,qi)≠(1,1)`，取原 B 弧接 L 弧的反向路徑，得到簡單
`C_(pi+qi)` cap 邊界；兩路徑內部不交且沒有其他接點，Jordan 分離給真正 disk。
不同 gap 的開 cap 互不相交。`(1,1)` 是同一條邊，沒有二邊形 cap。
這些規則的正整數分拆正好給下面九型，沒有其他排列。

表中原 B 一律 `(a,b,c,d,e)`，兩圈同向；cap 邊界按實際區域列出。
`x,y,z,w,t` 都是不同原內點。控制的 tuple 及面 rotation 可直接對照此表。

| ID | m | 原 L 代表 | 區域／邊界 | 在條件來源中的結論 |
| --- | ---: | --- | --- | --- |
| M0 | 0 | `(x,y,z,w,t)` | annulus，雙邊界 B、L | 保留 |
| M1 | 1 | `(a,x,y,z,w)` | pinched annulus，邊界 walk `(a,b,c,d,e,a,w,z,y,x,a)` | 保留 |
| M2E | 2 | `(a,b,x,y,z)` | 共邊 ab；C8 cap `(b,c,d,e,a,z,y,x)` | 保留 |
| M2-46 | 2 | `(a,x,c,y,z)` | C4 `(a,b,c,x)`；C6 `(c,d,e,a,z,y)` | §5.1 原 cap 最小性與度數排除 |
| M2-55 | 2 | `(a,x,y,c,z)` | C5 `(a,b,c,y,x)`；C5 `(c,d,e,a,z)` | §5.1 原 cap 最小性与度數排除；不採用任務 C |
| M3P | 3 | `(a,b,c,x,y)` | 共邊 ab、bc；C6 `(c,d,e,a,y,x)` | b degree 三，不可能 |
| M3S | 3 | `(a,b,x,d,y)` | 共邊 ab；C4 `(b,c,d,x)`；C4 `(d,e,a,y)` | 替換後至多九內點，不可能 |
| M4 | 4 | `(a,b,c,d,x)` | 共邊 ab、bc、cd；C4 `(d,e,a,x)` | b、c degree 三，不可能 |
| M5 | 5 | B | 五條共邊，star 填滿原 disk，沒有外 cap | 外點 degree 三，且 k=1，不可能 |

m=3 的 gap 只能是 `(1,1,3)` 對 `(1,1,3)` 或 `(1,2,2)` 對 `(1,2,2)`；
m=4 只能 `(1,1,1,2)`；m=5 只能全一。三個連續共點的中央外點，
其 B 兩邊之間的內側 rotation 已由兩個含 v 的面填滿，故只有兩個 B 鄰點與 v，
degree 恰三。這給 M3P、M4、M5 的排除，不能僅從抽象共點數宣稱不可能。

對 m=2 的非相鄰接點，外框短／長弧是 2／3 邊，link 也是 2／3 邊：
短配短給 4+6；短配長給 5+5。**原 tuple 而沒有 rotation／側配對不足以區分兩型。**
例如任務 C 的原 `L=(a,x,c,y,z)` 使用另一個相對方向，明示 caps 為
`(a,b,c,y,z)` 與 `(a,x,c,d,e)`，因此屬 M2-55；不是本表同向清單的 M2-46。
可用全圖具名搬運對上代表，但必須同時搬運 B、L、rotation、所有附件及色指派。
完整有標號分類是以上 gap 規則；D5 代表只方便閱讀，不丟棄原 `bi,ℓj` 身份。

## 3. 區域、原邊與 ownership

固定 skeleton `S0=B∪L∪{vℓi:0≤i<5}`。每個原非 skeleton 頂點落在
`D_B\D_L` 的唯一開區域；刪除 skeleton 後的每個連通分量以及其 incident 邊
也落在同一區域。記錄它實際連到哪些具名邊界點，包含重複接點的所在扇區。
若一個 component 或 bridge 接到兩個不同開 cap 的私有部分，其原連通路徑
必穿過 B、L 或已填滿的 star 面，違反原平面嵌入。跨 cap 私有點間沒有原邊。
接到共用 pin 的不同扇區可以屬不同 caps；不能把 pin 的鄰邊任意交換 ownership。

每個 cap 是「指定原區域中的子圖」，不是對邊界頂點取 induced subgraph。
例如 M2E 的共邊 ab 留在固定 skeleton，雖然 a、b 都在 C8 的邊界，
ab 的實際嵌入不在這個 cap 內，不能複製成 cap chord。
邊界 B、L 邊由 skeleton 保留一份，patch 關係可以重複檢查這些 properness 條件。

在各簡單 cap 中，B–B 與 L–L 的非圈邊已由 inducedness 禁止；接觸點同屬兩圈，
因此它也不能額外形成 cap 邊界 chord。唯一尚可能的邊界 chord 是
`B\L` 到 `L\B` 的跨弧邊，必須實際嵌在該 cap，並與其他 chords 不交叉。
內部頂點／分量可按原 rotation 附著於多個邊界 pins；一律保存實際 supports。
C4 cap 的唯一此類 diagonal 若存在，兩個三角形都因 §1 而空；
該 cap 的 L 私有點便只鄰接兩個 contact、B 私有點及 v，總 degree 四。
所以在目前條件來源中，C4 cap 的這條 diagonal 也不可能存在。
替換後的小代表不必繼續满足來源的度數或 inducedness 正規形。

M0 是真正 annulus，兩個邊界各有五個不同 pins。其 B–L 邊、跨環 bridges
與分量仍按原 rotation 留在 annulus；不能把內邊界「填掉」。沿一條實際
B 到 L 的路徑切開會產生含該路徑正反兩份的邊界 walk，路徑所有頂點都是
新增介面，兩份 copy 的顏色必須相同；它不會變成只有五個 pins 的普通 C5。

M1 的開外側區域是一個 disk，但閉包在 a 有兩個外側扇區。其邊界 walk 中
a 出現兩次（末尾閉合出現不另計），不能稱為簡單 C10 或 C5 邊界。
切開此 pin 得簡單十邊形的 normalization；黏回時兩個 a 必須是同一原點、
同一顏色，且 incident 邊維持各自扇區。M0、M1 可用一般具名替換引理，
不能直接用普通 C5 小代表替換這份帶孔／重複 pin 的介面。

## 4. 完整介面替換及十列 full lifts

令一般 patch P 與同一外部圖 E 的全部共用頂點為具名集合 I。
任何由 E 接入 P 的端點都必須在 I；patch private vertices 無外接邊。
I 包括所保留的 B 點、全部實際 attachment pins、切割路徑頂點與共享中心
（若中心放在外部）；重複 boundary occurrences 仍指同一頂點。
固定四色集 C，定義

```
F_P(α) = {f:V(P)→C : f proper, f|I=α},   R_P={α∈C^I:F_P(α)≠∅}.
```

空 fibres 也保留。若 P′ 與 P 有相同的 I、相同完整 R，且 P′ 能放入原
幾何 slot 並維持 pin 次序、重複點識別、incident sectors、原 B 的五個 labels，
則 `Σ(E∪P)=Σ(E∪P′)`。

證明逐份全圖著色進行。從 `f∈Col(E∪P)` 取 `α=f|I`。
完整 R 相等給某份 `g∈F_P′(α)`；`f|E` 和 g 在所有 I 一致，
所以沿同一具名點黏合就是新圖的完整 proper coloring，原 B 值逐點不變。
反向從新圖著色用 `F_P(α)` 選一份舊 lift，作相同構造。
可用固定點序／色序選 lexicographically first lift 使兩個構造成為明確函數；
不主張它們互逆，也不主張 fibre 基數相同。

替換可能帶入與外部同端點的邊：先依原 slot 形成平面 multigraph，再只去掉
同端點平行副本，保留原 B 邊與具名 skeleton 邊；proper-coloring 條件完全相同。
禁止識別不同 B labels、產生 loop、或用圖論平面性取代指定 rotation 可嵌性。

以下公式同時適用表中全部九型。令 `T=L\B`，p 遍歷原 B 的十個 proper
色軌道代表，`α:T→C`，s 為 v 的顏色；共同指派 `h=p∪α∪{v↦s}`。
對各實際外側 patch Pj，用其完整介面 Ij（必要時包括額外 pins），定義

```
J_G(p) = {(α,s,(fj)j):
          h proper on B∪L, s∉h(L),
          fj∈F_Pj(h|Ij) for every j }.
```

有額外 pins 時，把它們的共同指派一起納入 α；原重合身份只取一個值。
所有原全圖著色與此 join 的逐點限制／黏合對應，十列每一列（包括空列）都有
`p∈Σ(G) ⇔ J_G(p)≠∅`。各 patch 替換時在**同一個** `(p,α,s)` 上選 lifts，
給完整十列的雙向構造，不可從不同原圖或不同列拿成功 mask 相乘。
普通 C4／C5 boundary relation 使用全部 boundary pins，色軌道的每個代表
必先展開到共同四色框，故可用於上述 α；不得在 join 中分別置換色名。

只保存外圈十 bit，等同先 existentially 忘掉額外 I pins，會在
「`α∈R_P` 推得 `F_P′(α)≠∅`」這一步失效。
具體平面反控制見 `../review/projection/certificate.json`：
P0 為 B 加 z-a，P1 為 B 加 z-e，二者外圈關係都是 1023；
同一 E 加 z-b、z-c、z-d，完成圖分別是 255 與 987。
在 p=`01231`，前者 z 看見四色而拒絕，後者有全圖 lift `012310`。
兩種新邊都能畫在同一 E 面 `(z,d,e,a,b)`，因此這不是不合法嵌入造成的差異。
此例只是具名 pin 遺失的反控制，不是目錄外來源。

## 5. 每型內點數、已排除部分及殘餘

完整替換外側區域時，保留原 `v` 及 `L\B`，恰有
`t=1+(5−m)=6−m` 個原內點。各新 patch 的 k 只計其介面以外的私有頂點，
不同 patch 私有頂點互不相交。因此

```
k(H) = (6−m) + Σj k(Pj′).
```

若另切路徑、保留額外原介面 J，必改成 `t=|(L\B)∪{v}∪(J\B)|`，
不能把額外 pins 當 patch 私有點後又遺漏；共享點按 union 只計一次。

每個原簡單 C5 cap 的私有內點數不超過 `k(G)−(6−m)<k(G)`。
它本身是合法具名 C5 disk（允許 chords），故**全域**最小性給其關係在 K，
可換至多五內點代表。C4 用 BASE 的三內點界。各代表外圈全部 pins 皆固定，
可在原 cap disk 沿相同 boundary order 嵌入，再以 §4 共同色框接回。

| 型 | 精確 t 的原點 | 計數式／已有上界 | ≤12 所需的尚未取得界 |
| --- | --- | --- | --- |
| M0 | `v,x,y,z,w,t` | `6+r_ann` | 同一十 pin annulus relation 有 `r_ann≤6` 代表 |
| M1 | `v,x,y,z,w` | `5+r_pinched` | 同一九 pin／雙 a occurrence relation 有 `r_pinched≤7` 代表 |
| M2E | `v,x,y,z` | `4+r8` | 完整八 pin disk relation 有 `r8≤8` 代表 |
| M2-46 | `v,x,y,z` | 單靠大小界為 `4+r4+r6≤7+r6` | 不需新 C6 界，§5.1 從原 C4 cap 度數排除 |
| M2-55 | `v,x,y,z` | 單靠大小界為 `4+r5+r5′≤14` | §5.1 對原 cap 再用最小性／度數，排除此來源型 |
| M3P | `v,x,y` | `3+r6` | 已由 degree 三排除，不宣稱 C6 小代表 |
| M3S | `v,x,y` | `3+r4+r4′≤9` | 已足夠排除此型 |
| M4 | `v,x` | `2+r4≤5` | 已由 degree 三排除；此計數亦有條件成立 |
| M5 | `v` | `1` | 已由 degree 三及 k≥13 排除 |

M3S 的 H 是至多九內點合法 disk 圖且 Σ(H)=Σ(G)，由 `K≤12=K` 矛盾。
因此先有**條件最小來源的每個 degree-5 內點至多碰兩個原外框點**。
只使用上述大小界時會留下 M0、M1、M2E、M2-46、M2-55；
下一段利用來源本身的度數與同一全域最小性，再排最後兩型。

### 5.1 原 cap 的局部最小性與小外框度數引理

完整具名替換另有一項直接後果：若一個原 cap 的完整 boundary relation
已有 q 私有內點代表，則該**原 cap 本身**的私有內點數 r 必有 `r≤q`。
否則在同一原圖用此代表換掉 cap，§4 保持完整 Σ，卻減少全圖內點，
直接違反全域內點最小性。這不需要替換後仍滿足最大邊數或原度數下界。
因此原 C4 cap 已有 `r≤3`，原 C5 cap 已有 `r≤5`。

以下只對**原 cap**使用原度數。設 cap 為簡單 p 邊界 disk，`p∈{4,5}`，
有 r 個私有內點。所有私有內點的原 incident 邊都留在此 cap，故其 cap degree
等於 full-G degree，至少五。設 H 是這些 r 點的 induced graph，
其邊數為 e；cap 邊界 chords 數為 d。原 cap 的內面三角化，故 Euler 給

```
|E(cap)| = 3r+2p−3,
Σ_private deg_G = |E(cap)|−p−d+e = 3r+p−3−d+e.
```

當 `2≤r≤5`，每個私有點至多有 `r−1≤4` 個私有鄰點，
所以至少有一條原邊連到 cap 邊界。這條邊的內部不交 H；其邊界端點
可以沿 cap 外側連到無窮遠，因此該原邊位於 H 的無界面。
每個 H 頂點都 incident 到這個無界面，即 H 是 outerplane graph。
即使 H 不連通，也可在無界面連接其分量而保所有點在外側；
對所得連通簡單 outerplane graph 用 Euler 與面長計數，得到 `e≤2r−3`。
具體地，外面 boundary walk 長至少 r，內面長至少三，
`2e≥3(f−1)+r` 與 `r−e+f=2` 合併給此界。
因此

```
5r ≤ Σ_private deg_G ≤ 3r+p−3+(2r−3) = 5r+p−6 < 5r,
```

矛盾。`r=1,p=4` 時唯一私有點最多四個鄰點，也不可能；
`r=1,p=5` 只能是它鄰接全部五個邊界點的 wheel。

結合局部最小性，**原 C4 cap 只能 r=0；原 C5 cap 只能 r=0 或 1**。
這是對原最小來源 cap 的引理，不是對任意 C4/C5 小代表施加原度數。

在 M2-46，r=0 的 C4 必有一條 diagonal；連兩個 contact 的 diagonal
違反 induced B／L，所以只剩 B 私有點 b 與 L 私有點 x 間的 bx。
此時 b 在原圖只鄰接 a、c、x，degree 三（x 也只有 a、c、b、v，degree 四），
矛盾。因此 M2-46 排除，完全不需要 C6 小代表界。

在 M2-55，兩個原 C5 cap 各有至多一個私有內點，
所以原來源自身 `k(G)=4+rP+rQ≤6`，與 `k(G)≥13` 矛盾。
此排除沒有證明「任意 132² 有序 cap pairs 的聯集閉合」；
那是任務 C 的另一個有限命題，本輪未計算也不依賴它。

最終條件性結論是：

> 每個 degree-5 內點的原 B 接點，恰屬空集、單點或一條 B 邊的兩端點之一。
> 兩接點若出現，該原邊同時是 L 的一條原邊。

**僅 M0、M1、M2E 尚未排除**；不聲稱三型已有實際目錄外來源。

還須區分：`G−v` 作為普通外 C5 圖，其內點較少，的確已有 Σ 在 K 的五內點
unmarked 代表；這對所有 m 都成立。但是它會忘掉 L 的原五個 pins、內側空位
及各 pin 的 incident sectors，不能按原 star 接回 v。M0/M1 的 open obligation
正是這個 **marked** relation／rotation 的小代表界，不是否認普通 C5 定理。

## 6. 停止點與證據分層

紙面完成：九型的完整位置表、原區域與 ownership 分解、具名替換及 full lifts、
各型計數；排除 m≥3 及兩個非相鄰接點型。有限 skeleton 控制只核對分類的幾何骨架與完整色關係，
不是所有條件來源的枚舉。沒有依賴任務 B 或 C 的新結果。

真正 933／941（含整圖 D5 像）最小來源：`not triggered`。
普通十 bit 投影足夠保具名替換：`counterexample`。
有限控制與重播狀態見 REPORT／VERIFICATION；未新增或執行 Lean 證明。
未證保留三型中必有可縮減 degree-5 點，也未證一般壓縮或 `K∞=K≤5`。
