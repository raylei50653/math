# No-mixed 增長完備性：三個側弧位置與免表共同分離

2026-09-29，Git 基準 `3174f08`，接續工作樹中的
[無增長定理](c5_no_mixed_no_growth.md)與[共同局部規則](c5_no_mixed_local_screen.md)。
**在同一 no-mixed 圖類下，影響 root 可用色的 singleton→pair 增長，必被
守恆原路徑／非守恆原端點規則排除。結合無增長定理，指定 p₁、p₂ 的
共同分離有免查必要支援表的紙面證明。**

關鍵是從共同側跨度導出三個可能位置，再直接指定框弧分割；不用七類
records、target 接受 flags 或全表成功來證明完備性。這仍使用已證的
任意大小 source 結構、原路徑引理及外部 Gallai 定理，未 Lean 化。
它證明延拓存在，沒有給從一份指定 source 染色出發的逐步 repair 演算法。

新 [checker](../scripts/c5_no_mixed_growth_completion.py)／
[證書](../artifacts/c5_no_mixed_growth_completion/observations.json) 在既有
2,240 個增長候選與 11,096 joins 上重播證明的固定配方，作為有限控制。
沒有新增來源排除或 target 接受，也未證 disk 實現、完整 Σ、一般／共同
出口或 `K∞=K≤5`。目前入口見 [weak-deletion 導覽](c5_weak_deletion_guide.md)，
實際驗證見[研究紀錄](history/2026-09-29-no-mixed-growth-completion.md)。

## 1. 完整前提與色框正規化

沿用[跨度報告 §1–2](c5_no_mixed_span_budget.md#1-適用前提與精確語義)：
M 有限簡單，B=(b0,…,b4) 為 induced C5 disk 外框，H=M−B 非空連通；
q=01012 拒絕，刪任一非框邊後接受 q。恰有相鄰 z,w 完整 degree=5，
其餘內點完整 degree=4；H−{z,w} 的每份原分量恰接一個 root。
U={0,1,2,3}，p₁=01021、p₂=01212。不需 T4，不限制分量大小。

保留原 C、具名 contacts、全部 bridges／旁支、actual support S_C、
spokes、zw、共同環序及兩列完整有序接點關係。定義不變：

\[
F_C(\beta)=\bigcap_{\tau\in T_C(\beta)}\operatorname{set}(\tau),\qquad
E_r(\beta)=U\setminus\left(\beta(N_B(r))\cup\bigcup_{C\sim r}F_C(\beta)\right).
\]

T_C(β) 非空；延拓恰當 (E_z×E_w)∖Δ 非空。Source 各側禁色沒有重疊，
t_r+Σ|F_C(q)|=3，E_z(q)=E_w(q) singleton；兩個共同側弧的跨度各至少二、
和至多五。A/B/C/E 側分別有二／一／零／零 spokes，原分量禁色大小為
(1)、(1,1)、(1,2)、(1,1,1)。D 側已由 source 跨度排除。
本輪不把任何 source 等號施加到 target。

以下先證 p=p₂，只在 b2 把色 0 改成 2。p₁ 由明示的整列雙射還原：
框點反射 ρ=(3,2,1,0,4)，source 色置換 σ_q=(1,0,2,3)，target 色置換
σ_p=(1,2,0,3)。逐點有 σ_q(q(ρ(i)))=q(i)、σ_p(p₁(ρ(i)))=p₂(i)。
每列的**所有**原分量完整關係、禁色、root 色一起搬運；不為不同分量
選不同置換。這是對整列重新命名，不把 source 禁色硬傳到 target。
Source／target 的兩個置換與逆像 root pair 均記入證書。固定色條件在
正規化後的共同字面色框重新計算，最後由 σ_p⁻¹ 還原原 p₁。

## 2. 增長只能落在三個側弧位置

**位置引理。** 若 |F_C(p)|>|F_C(q)|，則 C 是二接點、F_C(q)={d}、
F_C(p)=D 為 pair，C 所在側只能是 A 或 B，且共同側弧只能是

\[
I_r=(2,3,4),\qquad(1,2,3,4),\qquad(4,0,1,2).\tag{1}
\]

數字表示具名框點，保留弧方向；例如 4012 的長度是三，不能改選 234。

**證明。** 一接點禁色至多一；source 已為 pair 的二接點分量也不能
增長。有整份支援色置換的 C 精確搬運，故增長 C 必不可搬運。
q 與 p 只在 b2 不同；限制到 S 的色相等關係發生變化，恰當

\[
2\in S,\qquad S\cap\{0,4\}\ne\varnothing.\tag{2}
\]

否則兩列在 S 上有共同色置換。b2 與 b0、b4 均不相鄰，因此 C 的
同序 hull 至少長二。若它在 C 側，另一飽和分量至少長二；若在 E 側，
另外兩原分量各至少長一，皆迫側跨度至少四，與另一側至少二矛盾。
所以只剩 A/B。

[無增長報告 §3–4](c5_no_mixed_no_growth.md#4-三色-c5-的唯一單現點與無增長定理)
對 source 的短側結論不需 target 無增長假設：每個長度二的 source
側弧都以單現點 b4 為端點。因此短側只可能 234 或 401。
若增長側短，(2) 排除 401；若增長側長三，另一側必短且共同框邊
內部不交，故它恰是另一短側的補弧，即 1234 或 4012。證畢。

還需三個不查表的 source 推論。

**(a) 長度二的 source 側實際碰到弧上三點。** 該側為 A/B，各分量
source 禁色皆 singleton。若全部 actual supports 加 spokes 只見兩色，
支援穩定子迫每個 singleton 禁色在這兩色中，不能留下 singleton E。
短弧三點三色，故三點均有實際附件或 spoke。從另一 root 經 zw 可到達
每一點；取路徑首次碰 B 處，取得避開增長 C 的原外部路徑。
所以 1234 情形有外路落 b0，4012 情形有外路落 b3。

**(b) 在短側 234，必 S=234、d∈{1,3}，並有外路落 {b0,b1}。**
跨度至少二的 C 占滿短側，故該側是 A、spokes 在 b2,b4；d 避開
q 色 0,2。singleton 穩定子迫 S 還包含 b3，所以 S=234。
若所有外部附件都只落 b2,b4，另一側若有兩個以上原分量，它們每份
都須見至少兩個 q 色，只能同用補弧 4012，違反同序 hull 邊內部不交。
若另一側是 A，兩 spokes 必在 b2,b4，而唯一 C 的 singleton 禁色只能
是支援所見的 0 或 2，違反 source 無重疊。因此必有外路落 b0 或 b1。
這個外路可經另一原分量，不能將它替換成新 root–B 邊。

**(c) 在長側 4012，必 d∈{1,3}；在 1234，若 1∈S，則是 A、
spokes 在 b1,b4、d∈{0,3}。** 對 4012，若 C hull 長三，只能 A，
spokes 在 b4,b2，直接迫 d∈{1,3}。若 hull 長二，(2) 迫 S⊆012；
source 至少見兩色再迫 S=012。A 的其餘 spokes 只可落 4/0/2；
B 的另一原分量支援為 40，spoke 也只可落 4/0/2。這些禁色皆在
{0,2}，而 d∈{0,1}；source 三個禁色互異迫 d=1。
對 1234，(2) 迫 2,4∈S；再有 1∈S 就占滿三邊，只能 A，spokes
在兩端 1,4，其 q 色 1,2 迫 d∈{0,3}。

這些推論只從共同單位次序、正跨度及 source 容量推出；沒有枚舉支援表。

## 3. 直接指定框弧的共同排除配方

固定增長 C 與原奇數 bridge 路徑 P=x₀…xℓ。刪去 P 邊後的 W_j
保留全部旁支，實際支援 T_j⊆S。沿用[共同局部規則 §3](c5_no_mixed_local_screen.md#3-同一局部規則的兩個分支)：
守恆 d 適用每條奇數 bridge 的同一 source residual {d,β}；非守恆 d
只對兩個**原端點**使用 {d,β₀}、{d,βℓ}，不假設兩 β 相同。
Target 在這些原路徑位置的 rooted residual 為 D；它不是完整 F 的邊際。

由 (2)，兩個移動色 0,2 都不守恆，固定色集恰為 K={1,3}。
任何相容 β 都滿足

\[
\{d,\beta\}\cap K=D\cap K.\tag{3}
\]

對使用色 0,1,2 的一列 s，二元 residual A 被 s(T) 的逐色穩定子保持，
恰當 s(T) 包含 A（3∉A），或包含 U∖A（3∈A）。因未見色可任意置換，
若未見色同時跨 A 及其補集就不保持 A；反之全部未見色落同一側即可。
以下「T 必碰 X、Y」都由這個兩色條件直接推出。

若每個可能 T 都碰同一 X、Y，B=X⊔Y⊔D_B 為三段非空連通框弧，
且已取得落在 D_B 的同一原外路 L，則沿用固定框弧 K5：守恆分支用
相鄰原 W_j、W_{j+1} 與剩餘路徑；非守恆分支用

\[
\bigcup_{j<\ell}W_j,\quad W_\ell,\quad V(L)\cup D_B,\quad X,\quad Y.
\]

原 bridges、兩條 contact 邊、實際附件與框弧切口給十鄰接，branch sets
不交且連通。任意長度及旁支由前層紙面引理承擔，非有限 skeleton 外推。

### 3.1 守恆 d：排至最多一個 β 即足夠

d∈{1,3} 而 d∉D 時，原端點固定色 tightness 已矛盾。下設 d∈D。

**I_r=4012。** 已證 d∈{1,3}，外路可固定落 b3。

| Target D | 相容支援必碰的點／集合 | 固定 X、Y、D_B | 結果 |
| --- | --- | --- | --- |
| {0,1} 或 {2,3} | target 條件迫 0、1 | {0}；{1}；{2,3,4} | 全部 β 排除 |
| {1,3} | (3) 迫 source residual {1,3}；兩列共同迫 0、4 | {0}；{4}；{1,2,3} | 全部 β 排除 |
| {1,2} 或 {0,3} | 取 source residual {1,2} 或 {0,3} 的 β，source 條件迫 1、4 | {0,1}；{4}；{2,3} | 排除這個 β，最多剩一個 |

第二列中，q(T) 須見 0,2，p(T) 也須見 0,2；在 4012 上，q 的 2
只在 b4、p 的 0 只在 b0，所以兩點皆必碰。第三列其餘相容 β 至多
一個，無需把每個 β 全部作幾何排除。空支援族直接排除。

**I_r=234，或 I_r=1234 且 S⊆234。** 外路可落 {b0,b1}；長側時
固定落 b0。Target S 只見 1,2，所以 D 只能是 {1,2} 或 {0,3}。
每個相容 source residual 為下列兩組之一：

| Source residual | 每個 T 必碰 | 固定 X、Y、D_B |
| --- | --- | --- |
| {0,1} 或 {2,3} | b2、b3 | {2}；{3}；{4,0,1} |
| {1,2} 或 {0,3} | b3、b4 | {3}；{4}；{0,1,2} |

因此所有 β 排除。兩個補弧都含 b0,b1，同一原外路足夠。

**I_r=1234 且 1∈S。** 由 §2(c)，守恆分支只可能 d=3；D 必為
{0,3}。相容 β 為 0,2。β=0 時，q residual {0,3} 迫 T 碰 b4 與
{b1,b3}，故固定

\[
X=\{4\},\quad Y=\{1,2,3\},\quad D_B=\{0\}
\]

及落 b0 的原外路，排除 β=0；最多剩 β=2。

**剩唯一 β 的收尾。** 上述配方在每條奇數原 bridge 上使用同一可行
β 集。若全空，原路徑不存在；若只剩 b，全部奇數 bridge 用 {d,b}、
偶數 bridge 用 {d}。沿用[整條路徑 palette 交換](c5_adjacent_degree5_no_mixed_t2_path_palettes.md#3-唯一剩餘-β-迫使第二個-source-禁色)，
保留所有旁支 palettes，交換原 P 邊的 d/b，得到同一原 C 在 root=b
時的完整拒絕證書，推出 b∈F_C(q)，矛盾於 F_C(q)={d}。
這一步使用 Gallai 充分方向；不是從某個端點 residual 猜完整 F。

故**所有守恆 singleton→pair 增長均被共同規則排除**。

### 3.2 非守恆 d：有害 pair 的原端點聯集被同一框弧排除

由 §2，d∉{1,3} 只能在 I_r=1234，d∈{0,2}。支援不含 b0，target
只見 1,2，故 D∈{{1,2},{0,3}}。先取 D={0,3}。

(3) 迫兩個原端點各自的 β 都等於 3；這是由固定色條件推得，沒有
先假設非守恆路徑的內點 palette 交替。

- d=0 時，source residual {0,3} 迫每個可能 T 碰 b4 與 {b1,b3}。
  取 X={4}、Y={1,2,3}、D_B={0}。
- d=2 時，§2(c) 排除 1∈S，故 S⊆234。Source residual {2,3}
  迫 T 碰 b2,b3。取 X={2}、Y={3}、D_B={4,0,1}。

兩者都使用 §2(a) 的落 b0 原外路；固定分割涵蓋**整個原端點支援聯集**。
原端點 K5 排除 D={0,3}，包括 ℓ=1，不依賴整張圖是否拒絕 target。

## 4. 剩下的 pair 必不影響 R，並完成共同分離

只剩 I_r=1234、d∈{0,2}、D={1,2}。另一側是短弧 401，p=q 在
這三點完全相同，所以該側所有完整關係精確不變。

若增長側為 A，當 C 占滿 1234 時，spokes 在 1,4，直接禁 target
色 1,2，source d 只能是 0；若 C hull 為 234，spokes 可落 1/2/4。
由 source 無重疊，d=0 時兩 spokes 禁 1,2；d=2 時兩 spokes 禁 0,1。
改 b2 的 0 為 2 後，兩種情形皆禁 target 1,2。

若增長側為 B，C 必占 234，另一單接點原分量 C′ 支援恰為 12，
spoke 可落 1/2/4。另一側短弧 401 的 source E 只能是 {3} 或 {0}。
本側 C 禁 d∈{0,2}，C′ 的 singleton 只能在 q(12)={0,1} 中，spoke
也不能禁 3，所以共同 source E 必為 {3}。另外兩個禁色恰是
{0,1,2}∖{d}。若 d=0，它們是 1,2；若 d=2，它們是 0,1。
C′ 在支援 12 上精確搬運 0↦2、1↦1，spoke 同樣按 p 取色，故在
target 兩者恰禁 1,2。

在這些 A/B 情形，除 C 外每份原分量都精確搬運；另一側 source E={3}
（A 側亦由三個 source 禁色為 0,1,2 得到），target 仍為 {3}。因此

\[
R_r(p)=\{0,3\},\qquad E_{r'}(p)=\{3\},\qquad
D\cap R_r(p)=\varnothing.\tag{4}
\]

於是 E_r={0,3}，可取 r=0、r′=3。這證明剩下的增長全都無害；
不聲稱這些局部 pair 可實現，也無須再判定它們是否被較強規則排除。

現在對真實 F tuple：若沒有增長，直接用[無增長定理](c5_no_mixed_no_growth.md)
取得異色 root pair；若有增長，§3 排除所有守恆及非守恆的 {0,3}，
剩下者由 (4) 直接延拓，且其餘分量皆已精確搬運。因此

\[
\boxed{(E_z(p_i)\times E_w(p_i))\setminus\Delta\ne\varnothing
\quad(i=1,2).}\tag{5}
\]

(5) 在 §1 任意大小圖類及所沿用的 source／原路徑引理下成立。
**共同局部規則對影響 R 的增長之完備性、及指定雙列分離，均已免查
必要支援表證成。** 這不是「所有 singleton 永不增長」，也沒有把
必要支援存在等同來源圖存在。

## 5. 有限重播與前層數字的關係

Checker 從 root-transport 的原完整 records 重建候選域及每份共同 lift，
驗證三個弧位置、分量跨度、source 禁色限制、指定外路、全部 β 支援族、
固定框弧及無害條件。不呼叫舊 `local_rule` 或 `frame_evidence` 搜尋器，
不讀原接受／排除 flags 作判定；完整 schemas、contacts、placements
沿原 record pointer/hash 保留。

| 控制 | 結果 |
| --- | ---: |
| 兩列 pair 支援穩定子代數 | 384 |
| 重建原查詢／joins | 4,164／11,096 |
| 全部 singleton→pair 候選 | 2,240 |
| 守恆色不在 target pair | 890 |
| 指定框弧排除全部 β | 644 |
| 排至唯一 β 後整條原路徑交換 | 246 |
| 非守恆原端點排除 | 230 |
| 保留的無害增長 pair／joins | 230／230 |
| 被排除 joins | 3,018 |
| 保留且有異色 pair | 8,078＝7,848 無增長＋230 無害增長 |
| 重新取得排除的原失敗 joins | 434 |
| 原 minor skeleton 控制 | 1,524 |

前層較強搜尋排除 2,208 個局部 pair、保留 32；本輪僅需排除 2,010、
保留 230。其中多保留的 198 個全都無害，並非推翻舊排除，也非新接受。
前層原 40 個唯一 β，本輪變為 246，是因本輪在排至至多一個 β 即停止，
不再搜尋額外框弧；這只是證明路徑不同。AA54/p₁/j4 仍用整條路徑
交換，AB22/p₂/j4 仍用非守恆原端點；證書 `controls` 保留兩個錨點。

本 checker 重用前層的共同 lift 解碼、候選搬運與原 minor skeleton
控制函式，不是全部幾何引擎的獨立重寫。端點 skeleton 重算長度 1/3/5，
逐奇數 bridge 控制重算兩相鄰原塊；這些不是 degree-list 來源實現。
任意長度與旁支的證明依 §3 沿用引理，不由 skeleton 長度上界推出。

## 6. 重播與剩餘界線

```bash
python3 scripts/c5_no_mixed_growth_completion.py --check
PYTHONHASHSEED=17 python3 scripts/c5_no_mixed_growth_completion.py --check
python3 scripts/c5_no_mixed_no_growth.py --check
python3 scripts/c5_no_mixed_local_screen.py --check
python3 scripts/c5_no_mixed_root_transport.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

無 `--check` 只生成本層 artifact；前後核對 11 份舊輸入 SHA 不變。
本層另綁定所有載入的研究 Python 模組 SHA。實際通過及未重跑清單
以[當輪歷史](history/2026-09-29-no-mixed-growth-completion.md)為準。

本輪完成的是紙面存在性分離及其有限控制。未新增 Lean theorem 或
`native_decide`；`lake build` 不表示新幾何已形式化。外部 degree-list／
Gallai 及前層 annulus、原路徑引理沿用既有證明，未重讀外部文獻。
未給從指定 source 染色出發且保留指定外部染色的建構式 repair；必要
支援實現性、完整 Σ、較大 mixed 原分量、一般出口及 `K∞=K≤5` 仍開放。
目前下一窄題由研究線導覽維護，不再把本輪已證的增長完備性列為未解。
