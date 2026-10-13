# C8-TERMINAL-S1：原具名分類、C6 繼承條件與任意大小接合

2026-10-13。只屬本次隔離 audit；原輸入由父目錄 `INPUTS.json` 封存。
下文的 L 是**原来源剩餘 terminal disk**，其嚴格內點數 r 不設上限；
不是六私人點 C6 cap 型錄。沒有使用四色定理或一般 C6 代表定理。

## 1. 原契約及直接依賴

固定全域最小內點、再最大邊數的目錄外原 C5 disk G，原外框 B 的順序、
同一有序 C8、全部原 attachment、rotation 和共同四色集合
`A={0,1,2,3}` 均一次固定。取 h=3、p∈{1,2}、s=1。
八份必要來源是原 `c15/c18-933` 及
`c04/c07/c15/c18/c20/c30-941`；932 的 h=3 已另行排除。

直接消費以下既有紙面結論，均以 frozen bytes 為準：

1. `docs/c5_c8_peeling.md` §1 及
   `audits/2026-10-13-c8-peeling-6cafdfb/structure/PROOF.md` §§1–4：
   C induced、H 內面三角化、d_H(C)≥4、d_H(I)≥5，八個不同原面第三點
   t_i，相鄰雙接唯一性、完整 link walk、正對 pair 唯一、PINCH／BRIDGE
   完備分類以及每個 terminal 皆 occupied。
2. `audits/2026-10-13-c5-no4ct-frontier-6943561/terminals/PROOF.md`
   §§2–4：任何 `s_side=0` 的原 terminal 精確是原 W5；原六點介面的
   4096 literal fibres 和全部 lifts 已存於 `full_lifts.v2.json.gz`。
3. `audits/2026-10-13-c5-no4ct-c8-6cafdfb/geometry/PROOF.md` §§1–5：
   原內部 C3／C4 cap 空、C5 cap 空或 W5；loopless planar
   `N≤k+5` 相對可染性。這些結論的來源最小性契約不可丟棄。

後文每個小環都由原 G 的內點構成。其 cap 嚴格內點數至多 `k−|Q|<k`，
所以 C4／C5 使用的是正確的相對大小結論，沒有把 L 當成較小 C5。

## 2. s=1 的完整原位置分類

下標模 8。以 `0≤i<4` 固定原正對 pair `{c_i,c_(i+4)}`，並以
`ε∈{0,1}` 指定含唯一單接點 w 的半側，令 `a=i+4ε`。
該半側沿原 C 的順序是

`(c_a,c_(a+1),c_(a+2),c_(a+3),c_(a+4))`。

其 endpoint 記 e；另一半側 endpoint 記 f。PINCH 中 `e=f=x` 是同一
原頂點，沒有第二份 x。BRIDGE 中 e、f 是兩個不同原頂點，原邊 ef 存在；
固定半側 ownership 決定哪一個原點是 e，不能逐色列交換。

唯一單接點 w 有唯一原 C 鄰點 `c_(a+j)`，其中 `j∈{0,1,2,3,4}`。
剩餘 disk L 的有序原框 D，是在

`(e,t_a,t_(a+1),t_(a+2),t_(a+3))`

的第 j 個位置插入 w：j=0 在 e、t_a 之間，j=4 在 t_(a+3)、e
之間；j=1,2,3 則在 t_(a+j−1)、t_(a+j) 之間。故 D 為六個互異原點。
這五個位置包括兩個正對端點的單接位置，不可只枚舉半弧的三個內點。

另一側 `s_side=0`，故由既有 T0 恰為原 W5，其 rim 為

`(f,t_(a+4),t_(a+5),t_(a+6),t_(a+7))`，

唯一中心記 z。沒有其餘該側私人點或額外 rim chord。L 本身仍是任意
有限大小的三角化 disk；其嚴格內點數 r≥1，且所有這些點都無 C 接點。

原 C-I 邊精確是八份 `t_ℓ–{c_ℓ,c_(ℓ+1)}`、全部正對 endpoint
到 `{c_i,c_(i+4)}` 的邊，以及唯一 `wc_(a+j)`。沒有未列出的附件。
所有 C-Q collar 面由原 link paths 精確恢復：

* 在 c_a，link 是 `(t_(a−1),f,e,t_a)`，PINCH 合併重複的 f=e；
  j=0 時在 e、t_a 之間插入 w。
* 在 c_(a+4)，link 是 `(t_(a+3),e,f,t_(a+4))`，PINCH 同樣只留
  一個 endpoint；j=4 時在 t_(a+3)、e 之間插入 w。
* 其他 c_ℓ 的 link 是 `(t_(ℓ−1),t_ℓ)`；若 ℓ=a+j 且 1≤j≤3，
  則在兩者之間插入 w。

每條連續 link 邊和 c_ℓ 形成原三角面；另有八個原面
`c_ℓ c_(ℓ+1) t_ℓ`。BRIDGE 的兩個 endpoint link 同時保留原 ef 邊
的兩個面側。這給出原 rotation，不只是抽象鄰接表。

因此分類索引恰為

`8 collars × 4 pairs × 2 types × 2 sides × 5 slots = 640`。

這不是對 r 作搜尋截斷；所有任意大小 s=1 原圖都屬其中一個固定外側
配置。可能多份配置在抽象圖同構，但固定 B/C/attachment 的計算仍逐份
保留，不用不同色列上的獨立同構或旋轉替代。

## 3. L 可繼承和不可直接繼承的條件

所有 L 內面均為原 G 三角面，L 在 D 內側包括所有原點及所有原邊。
L 嚴格內點沒有任何 L 外鄰點。逐類精確度數為：

| 原點 | 原 H 度數 | L 中必有的度數 |
| --- | --- | --- |
| L 側四個 t | `d_L(t)+2` | `d_L(t)≥3` |
| 唯一單接點 w | `d_L(w)+1` | `d_L(w)≥4` |
| PINCH 的 e | `d_L(e)+3+2` | 只先得 disk 邊界下界 `d_L(e)≥2` |
| BRIDGE 的 e | `d_L(e)+1+2` | `d_L(e)≥2` |
| L 嚴格內點 v | `d_L(v)` | `d_L(v)≥5` |

PINCH 的額外 3 是另一個 W5 的兩條 rim 邊及中心邊；BRIDGE 的額外
1 是原橋邊。故不能假設 D 上六點都至少度四，也不能從 H 的全體內度
至少五推論 e 在 L 中至少度三。

固定側四個 t 的 H-degree 恰五，z 的 degree 恰五。BRIDGE 固定端 f
的 H-degree 恰六。原 C 點的 H-degree 為
`4 + p·1_{ℓ∈{i,i+4}} + 1_{ℓ=a+j}`。

L 內部的 C3／C4 cap 皆空，C5 cap 空或 W5；任意原小環即使含有 D
點也仍按同一原嵌入選不含 B 的 cap 側。這個約束比單看 L 的 degree
更強。下一節逐一推導 boundary chord 的可能性，不預先假設無弦。

## 4. 新的 C6 chord 分類：唯一可能是 endpoint 耳加 W5

**引理 S1-CHORD。** 若 L 有 boundary chord，則 L 精確為一個 W5
沿其一條 rim 邊附上一個以 e 為尖端的三角耳。w 必鄰接 e，故 j=0
或 j=4；該 chord 是 e 的兩個 D 鄰點之間的邊。此時 r=1。

證明。六環 chord 的較短 D 弧長是 2 或 3。

若為 3，兩側均為原 C4 cap，依原小 cap 定理皆無嚴格內點；因此 L
無嚴格內點，與 terminal occupied 矛盾。

若為 2，其短側是空原 C3，故短弧中點 u 在 L 的完整 sector 只有
兩條 D 邊，即 `d_L(u)=2`。所有四個 t 及 w 都至少度三，所以 u=e。
chord 的另一側是原 C5 cap，包含 L 的全部嚴格內點，必 occupied，
故精確是 W5。除 chord 兩端以外的 W5 rim 點在 L 中度三；w 至少
度四，因此 w 必是 chord 端點，也就是 e 的一個 D 鄰點。證畢。

這是原圖任意大小子族的完整分類：由小 cap 和度數強制 r=1，而非
只搜尋 r=1。它也顯示不能在入口直接假設 L induced；j=0,4 的 chord
候選須由完整來源條件另行排除。

若 L 無 chord，則 e 至少度三：若 e 在 L 度二，其 incident 內面會迫
e 兩個 D 鄰點之間有 chord。故 induced 子域中全部 D 点至少度三，
w 至少度四。此外 r=1 時三角化迫 L=W6，使 w 只有度三，矛盾。
所以 induced 子域有 r≥2；此處不對 r 設任何上界。

## 5. 新的原 contact 限制與合法識別

以下只論 induced 子域，將 D 從 w 起依原順序寫成
`(d0=w,d1,d2,d3,d4,d5)`，不重新旋轉原外框 C 或 B。

**引理 S1-WCONTACT。** 任一 L 嚴格內點 v，不能同接一條長 2 或長 3
的 D 弧之兩端，而把 w 留在該弧嚴格內部。特別地，其 D 接點集合
不得包含下列任何一對：

`{d5,d1}, {d1,d4}, {d2,d5}`。

證明。長 2 弧和 v 的兩條接邊形成原 C4 cap；該 cap 空且 D induced，
唯一三角化是從 v 向弧中點 w 作 fan。w 的完整 L sector 都在該 cap
中，因此 `d_L(w)=3`，矛盾。長 3 弧則形成原 C5 cap：空側因 D 無弦
只能是 v 對兩個弧內點的 fan；occupied 側恰為 W5。兩種情況都令該
弧內點在 L 度三，包含 w，仍矛盾。證畢。

故嚴格內點若同接一對 D 正對點，該對必包含 w。這不是「下一層至多
兩接點」：目前沒有那個結論；也沒有把 D 的其他度三點誤當成度四。
S1-CHORD 和 S1-WCONTACT 明確消費原 degree、原 cap 側及原 attachment，
是通用 C8 gadget／計數條件未包含的原圖資訊。

原相對大小可染性亦可合法作用於 L。由 §2 的確切點數，

`|V(P)|=23+p, |V(G)|=r+23+p=k+5, |V(L)|=r+6`。

在 D 外側作 noncrossing partition π，若每個 block 都是 L 的獨立集，
收縮各 block 的外側樹會給 loopless planar quotient，點數為 `r+|π|`，
不超過 k+5；故有完整四色染色。拉回給同一原 L 的完整染色，並在各
block 常值。不同 blocks 可以同色；不能擅加它們兩兩異色。

若 L induced，block 只須不含相鄰 D 點。若 L 是 S1-CHORD 型，則還
必避開那條原 chord 的兩端；忽略 chord 會把帶 loop 的商圖錯當合法。
以上只給整個指定 equality 集合中至少一份延伸，沒有指定單獨 literal
row 必延伸。主來源排除採用下一節更強的外側轉移障礙，因此不以這些
正性限制的有限可行性冒充原來源實現。

## 6. 精確原 patch、空 fibres 與 full lifts

對 §2 每一份配置，令 P 包含：原 B–C8 collar；全部原 C-Q collar
邊及面；固定側原 W5；原 D 六環；BRIDGE 時的原 ef 邊。P 不含
L 的未知內部或未知 chord。若 L 有 D chord，它完整保留在 L 中。

有 `V(P)∩V(L)=D`，且 `E(G)=E(P)∪E(L)`。D 的六條邊同時屬兩邊
不妨礙接合；除此以外不存在遺漏的跨界邊。理由是原 terminal 分類
已定位全部 C 接點、全部 Q blocks 及唯一 bridge，L 嚴格內點均無
C 接點，也不接固定另一 terminal。P 的 W5 以既有 literal 原子
kernel 接入，其原六點 J 保留同一具名 C 半弧、endpoint 及原色框。

固定原 B 十列之一 β。對每一 literal `γ∈A^D`，令
`F_P(β,γ)` 為 P 上所有同時限制到 β、γ 的完整染色，令 `F_L(γ)`
為 L 上所有限制到 γ 的完整染色。包括所有 improper γ 及 proper
空 fibres。則有完整染色集合的一一對應

\[
\boxed{\mathcal F_G(\beta)=
\bigsqcup_{\gamma\in A^D}
\mathcal F_P(\beta,\gamma)\Join_D\mathcal F_L(\gamma).}
\tag{S1-JOIN}
\]

證明。限制任意原 G 染色給出同一 γ 及上述兩個完整 lifts；反向上，
兩份 lifts 在同一 D 逐點同色，可作唯一聯集，所有原邊已由 P 或 L
檢查。不同 γ 的聯集不相交。PINCH 的 e 在 P、L、兩個 terminal
中全是同一原點；BRIDGE 的 e、f 是不同原點，ef 的異色條件在 P
內檢查，從未刪去橋邊或把兩個 endpoint 獨立重新著色。證畢。

式 (S1-JOIN) 保留所有空 fibres 及 full lifts，適用任意有限 r。
染色數亦為 `N_G(β)=Σ_γ N_P(β,γ) N_L(γ)`，因私人原点集互斥。
這個數式不能在同一 γ 上獨立正規化 P、L 的色名。

## 7. 足以排除任意 L 的有限外側判準

此節是有限轉移證書採用的普遍引理；具體 640 份輸出及獨立重播由
父報告與 transfer 子包記錄，不能以本節公式本身代替驗證。

令 Ω 是原有序 D 上 proper C6 literal rows 的**共同** S4 軌道集合。
對每一軌道 o，定義十列 mask

\[
T_P(o)=\{b\in\{0,\ldots,9\}:\exists\gamma\in o,
\mathcal F_P(\beta_b,\gamma)\ne\varnothing\}.
\tag{S1-OUT}
\]

這裡 β_b 一直固定；只把同一 L relation 中必同時存在的全部 γ 列
合併為一個 mask。不能只取每個 o 的 canonical γ 對固定 β 計算。
P 的計算須先在同一 literal 色框完整保存每個 `(β_b,γ)` cell。

L 是沒有額外色名限制的原圖，故其全部完整 fibres 在全域 S4 作用下
等變。對任何 o，要麼其每個 literal γ 的 fibre 均空，要麼均非空。
令 `S_L⊆Ω` 是非空軌道集合。由 (S1-JOIN) 立即得到

\[
\boxed{\Sigma(G)=\bigcup_{o\in S_L}T_P(o).}
\tag{S1-UNION}
\]

這是同一原 L 的整份 relation；沒有把不同 L 或不同位置的成功列拼湊。
但若要證不可能，可以把 S_L 放寬成 Ω 的**任意**子集，甚至空集合。
這是一個嚴格放寬：放寬域都不能產生 target，當然排除任何真實 L，
無論 r 大小、L 的 chord、內部結構或 colouring counts 如何。

對指定原 target τ∈{933,941}，定義

\[
\mathrm{Safe}(P,\tau)=\{o:T_P(o)\subseteq\tau\},\qquad
M(P,\tau)=\bigcup_{o\in\mathrm{Safe}(P,\tau)}T_P(o).
\tag{S1-SAFE}
\]

若 Σ(G)=τ，任何真正非空軌道都必在 Safe 中；否則其一個 P 完整 lift
與 L 的同列完整 lift 接合就產生 τ 禁止的原 B 列。故 `τ⊆M(P,τ)`
是來源必要條件。定義又給 `M(P,τ)⊆τ`，所以必要條件就是 `M=τ`。
只要證書對固定 P 給出 `M≠τ`，即排除該配置的**所有任意大小 L**。

這個判準新增的實際原圖資訊是：s=1 強制唯一單接位置及一端完整原
W5，從而固定 P；它使用 P 對全部 D literal rows 的精確可延伸性。
一般 C8 exterior gadget 正性或通用線性計數條件並未固定這一份原
W5、endpoint ownership、bridge 邊、slot 和原 collar 的同列接合。
因此若 640 份皆通過 `M≠τ`，成果不是只重寫 separator 公式。

## 8. 可採納邊界

§§2–6 的分類、度數、chord／contact 限制及 full-lift 接合是任意有限
來源的紙面結論。§7 提供可機器核對的有限外側排除判準；只有採納
父報告所列 640 份完整轉移及重播後，才得本輪來源命題

\[
h=3,\ p>0\Longrightarrow s\ge2.
\]

它與既有 terminal 下界一起只提高這兩個分支為 PINCH `m≥13`、
BRIDGE `m≥14`，即各有 `k≥21`、`k≥22`。一般 h=3 的 `k≥19`
不因此提高；p=0 RING、s≥2 的兩型、h≥4、一般主命題及本輪新論證
Lean 形式化仍未在此完成。沒有自動擴到那些域的枚舉或搜尋。

紙面分類對主程式的獨立結構核對由 `check_structure.py` 保存：從本文件
的附件及 link 公式另建全部 80 份 H 邊集，逐一比較 D 原次序、全部
640 條 C-link paths、C 度數、原三角面方向與保存的 cyclic rotation。
它不搜尋 L，不重算染色，且不寫證據檔；normal 與 seed 17 輸出分別在
`check_structure.log`、`check_structure.seed17.log`，內容相同。錯接端點
slot、刪原 bridge 及反轉 bridge 原面方向三項 in-memory 負控制皆拒絕。

```bash
python3 -B audits/2026-10-13-c8-terminal-s1-d521163/theory/check_structure.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-c8-terminal-s1-d521163/theory/check_structure.py
```
