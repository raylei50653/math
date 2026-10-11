# 單缺額定理契約與 N45 同源適用性：獨立唯讀核對

本件只寫本輪專屬 `theorem_contract/`；BASE 為
`4dd11f422c6fa49265a412085116b088786d0344`。下列 `docs/...:line`
皆指本輪 `frozen/docs/`，不指可能變動的共享文件。文獻與非 docs
輸入另列於 `inputs.json`，交由主 audit 凍結。本件未執行來源搜尋、
literal controls、舊 checker、Lean，未修改權威或舊證書。

## 1. 準確結論與 A gate

正式來源為 Daniel W. Cranston 與 Landon Rabern,
*Beyond Degree Choosability*, EJC 24(3) (2017), #P3.29。
[正式 journal PDF](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v24i3p29/pdf/)
已於本輪開啟核對；本地凍結候選 PDF 的 SHA256 是
`8b6b26981671cb839f96667653913e63b690d917a891483d32a44e1d1adc2271`。
本地 `cranston-rabern-2017-final.txt` 是逐行定位的文字提取。

令 `h_s(s)=1`、其餘為 0。單缺額的 list size 是
`f(v)=d_H(v)-h_s(v)`。文獻 Main Lemma（PDF p.3；txt:124–128）
及 Theorem 4.1（PDF p.12；txt:560–562）合起來表示：

- 若 H 二連通、當前大小為 f 的 lists 不可染，則
  `d_H(s)=2` 且 `H-s` 是 Gallai tree，或者
  `d_H(s)>=3` 且 H 是 complete／`(H,h_s)` 屬文獻三族例外 D。
- 這是對當前不可染 lists 的**必要結構析取**。例外存在某份不可染
  lists，不表示來源 β 的 lists 一定等於文獻的那份 lists。
- 文獻 Theorem 3.6（txt:498–511）另有非二連通分類，包括
  s 為割點的 lobe 分支及 s 不為割點、其所在 block 屬 D 的分支。
  不得把連通 H 套入二連通 Main Lemma。

凍結 docs 沒有 `LIT-SD-A` 或單缺額推論的陳述；同時進行的
`audits/2026-10-11-c5-single-deficit-biconnected-5e7a5ffd/` 於本次核對
只有 receipt／文獻及 worker 圖片，沒有 REPORT 或 A 裁決。
因此此处只能使用**候選契約**：

> 若 A 能證明本 C5 disk、degree 4/5、接受 T4、同 β minimal
> 契約排除文獻 complete／D 例外，則二連通 H_M 只能有
> `d_H(s)=2`、`H_M-s` Gallai。

N45 的 r、s 全留且原不相鄰，已單獨排除 H_M complete；D 的來源排除
仍須 A 證明並驗收。所有透過這個候選推論擴張至**全部二連通**
身份的結論一律 `conditional on A`。直接假设 `d_H(s)=2` 的下述
局部論證不依賴 A。

## 2. G、X、M 與完整 profile

權威共同契約見 `docs/c5_excess_two_nonadjacent_unit_core45.md:69–90`。
G 是 ordered induced-C5 disk，完整 Σ=933／941 或整圖共同 D5 像，
每條原非框邊 Σ-critical，ε=2，原 r/s 完整 degree5、不相鄰；
其他有效原內點完整 degree4。H_G 連通；刪 r/s 後實際兩 mixed P,Q
完整保留，餘為 unary，沿用原 one-sided、full B-touch、support 非空。

| 符號／性質 | 精確意義與可用性 |
| --- | --- |
| G 的 Σ-critical | 每條原非框邊刪除會釋放至少一原拒列；釋放列可隨邊不同。不是固定 β 的逐邊 minimality。 |
| derivative X | S 是 `G-e`、e=原 rb_i；U 是 `G-V(U)`、整份原 U 全刪。一般 derivative 僅有 Σ(G)⊆Σ(X)，不遺傳 β-minimality。 |
| actual M | 保原 B 的 inclusion-minimal β-obstruction；非框邊逐刪皆接受同一 β。實際 vertices/edges 必須列明。 |
| β-minimal ⇒ 自身 Σ-critical | 每 retained 非框邊的同 β witness 同時見證 Σ 變大；見 N45:83–84、99。 |
| X=M | N45 選定 S／U 身份的額外等式（N45:77–85）；須有同 β witnesses，不能當 minimization 自動結果。 |
| 一般 M⊊X | 需重新核 M 自己 retained adjacency、完整 degrees、有效 H、所有被刪 contact 及完整 lifts；原 45/54 標記不能代替這一步。 |

從 M 自己計算 `t_M(v)=|N_M(v)∩B|`、`d_H(v)=|N_M(v)\B|`。
β-minimal 的一般紙面限制為 H_M 連通、同一內點的 β-spokes 異色、
每有效內點在 M 完整 degree>=4；見 `docs/c5_weak_list_cores.md:18–35`。
故

`|L_β(v)|=4-t_M(v)`，
`d_H(v)-|L_β(v)|=deg_M(v)-4`。

只有在 M 的**完整** profile 已證為 `s:5`、其餘有效點 `4`
（含 r:4）時，才可代入單缺額 `f=d_H-1_s`。同源 subgraph 的原
degree 上界加 β-minimal 下界可提供 profile 的紙面推導，但此推導
仍是以 M adjacency 已確定為前提的 conditional profile，不是实际
degree 計算或 source realization。

exact S 的原唯一 spoke e 全外框邊省略保 `H_M=H_G`；r 恰失一邊
降到4，s仍5，其他有效點4。exact U 恰省略 unique 原 rx：r降4，
s及所有剩餘 piece 點不失邊，完整 profile 同樣為4/5。
兩種推導各要求整 pieces 及所有其他原 contacts 全留。

原 55 自身 core 有兩個缺額 `d_H-1_r-1_s`；文獻單缺額不可套用。
文獻 txt:98–103、585–589 明述兩缺額的 choosability／AT 分類已不一致；
此處只記適用障礙，不擴張分析。

## 3. 連通、二連通與具名割點

β-minimal 只直接給 H_M **連通**（Weak-list:26–31）。N45 精確共同
契約也只寫 H_G 連通（N45:74），沒有二連通前提。

| 身份 | H_M 連通論據 | 二連通／割點壓力 |
| --- | --- | --- |
| no U、exact S，P/Q全留 | H_G=H_M；兩 P/Q 都接 r/s | r/s 自身不割 H：刪一 root 後 P/Q 仍各接另一 root。P 或 Q 的内部 off-route branch、bridge、割點仍可能割 H；無 actual source 時是 unknown。 |
| U incidence1在r且U全留的S | H_G=H_M | 刪 r 分離 U 與其餘 P/Q/s，所以具名 r 是 H 割點；這是契約內條件拓撲，不是聲稱存在被排來源。 |
| U incidence1在s且U全留的S | H_G=H_M | 刪 s 分離 U 與 C={r}∪P∪Q，所以具名 s 是 H 割點（例如已採 HIGH1；N45:57–58、122）。 |
| U多contact完整保留 | 同原H連通 | 不論原U的contact數，只接同一owner；刪owner必分離完整U與另一root／其餘mixed，所以具名owner是H割點。U內部是否另有branch割點仍unknown。 |
| 整U省略 exact U | 實際 C／P/Q保留及X自己的minimality | 唯一原U消失不自動排 P/Q私有 branch割點；既有排除已採，不重開。 |
| 一般45/54 actual M | M自己的 β-minimality | β-minimal、唯一degree5、root名稱均不推出二連通；逐 M block-cut/rotation資料缺失時 unknown。 |

完整 profile 又令 `d_H(s)=5-t_s>=2`，因三色 β 的異色 spokes 至多3。
在 source 已證 `d_H(s)=2` 時 `t_s=3`；在只給 A 候選時，這個
結論还需 H_M 二連通與 A 排除 D 的證據。

## 4. no-U、d_H(s)=2 的實際 two-terminal core

只取 exact S：原 unary=0，實際 `H_G-{r,s}=P⊔Q`，原 pieces 全留。
令唯一 s-P contact 為 x_P，唯一 s-Q contact 為 x_Q，按原 rotation
保存其有序角色。它們屬不同實際分量，故 `x_P!=x_Q`。

`C=H_M-s={r}∪P∪Q` 連通；`C-r=P⊔Q`，所以 r 是 **C 的具名割點**。
這個 C 割點不等於 H_M 的割點：s 會接回 P/Q 兩側。

C 是 Gallai tree：它是全部 M degree4 點誘導的唯一連通分量，
`docs/c5_weak_list_cores.md:101–107` 已給 Gallai forest；連通升為tree。
所以這份 Gallai 性並非單缺額工具的新增涵蓋。

同 β minimality、三條 β異色 s-spokes給 `A_s(β)={D}`，逐刪 s-spoke
的完整 witnesses 保另外三色可接回，故 **`F_C(β)={D}`**。
完整 fixed-frame 接合及不可刪減覆蓋見
`docs/c5_degree5_interfaces.md:77–106,167–185`、
`docs/c5_degree5_sectors.md:31–45`。兩contacts 的完整共同 R_C 和
fibres／full lifts 不可由這個四值 F_C 反求。

R12 的充分前提亦逐項成立：s有3條B-spokes，C各点完整 degree4，
C 拒絕可用 s 色 D，刪其 incident edge 可接回。所以 C 不含 K4 block；
見 `docs/c5_degree5_tree_components.md:20–24,32–53`。
K5或更大block由度數排：K5各點内部degree4全滿，不能再接s／其他block，
與C有兩實際s contacts矛盾；更大block超完整degree4。
因此 blocks 只有 K2 bridges 與 odd cycles（K3算oddcycle）。

### 二連通的精確 chain 條件

對兩contacts x_P,x_Q，`H=C+s x_P+s x_Q` 二連通 iff：

1. x_P、x_Q 不是 C 割點；
2. C 每個割點 v 都讓 C-v 恰分成兩側，一側含 x_P、另一側含 x_Q。

必要性：沒有contact的 C-v 分量，加入s後仍無路通其餘H-v；若 v
本身是contact，另一側無contact亦造成割點。充分性：刪s留下連通C；
刪任意其他v時 C-v 不分裂或兩側經s接回。這逐頂點證二連通。
等價地，C 的 block-cut tree 是兩contact所在terminal blocks之間的
**一條鏈**，沒有 offpath blocks；單block情形另包含於條件。
no-U中r確為割點，所以鏈至少兩blocks。

r恰鄰兩blocks；一側block於r贡献1(K2)，或2(oddcycle)。三個unordered
profiles `(1,1),(1,2),(2,2)` 給 `d_C(r)=2,3,4`；
M的r-spokes是 `2,1,0`，原G的r-spokes是 **`3,2,1`**。
原contact partition、r的實際附件與 e 的spoke位置不可交換。

由這個 chain 條件：R30中間環兩contact、R31同末端兩contact，均有
無contact的另一端支，所以不是此 H_M 二連通形狀。這不補完一般R31。
恰三個互相共用點的 oddcycle鏈、兩terminal各一contact/arm，正好映射
已採 R27；源契約見 `docs/c5_degree5_three_cycle_minors.md:11–17`。
R27只保 fixed-β 全四s色測試與 F={D}；其來源 minors 明說不保完整Σ、
R_C、任意pins（同檔:65–84）。可用它證本實際來源非disk，不可拿正常形
coloring 替換實際來源或聲稱保留r-fibres。

## 5. 兩個確實較窄的局部來源障礙

### 5.1 no-U TWOLONG：三spoke star 上原盾弧只能收3邊

最弱此处已知充分前提：原G disk／full B-touch；非相鄰 r/s、無U，
實際兩mixed P/Q接兩roots；原one-sided；原long定義為 actual support
不包含於任何框邊，所以原盾費各>=2；原盾弧面定義与互斥引理。
另假设 exact S 保全部内边／pieces且 `d_H(s)=2`。
無需 A、Σ的指定mask或跨列換色來做以下幾何推理。

1. `t_s=3`，且 `H_G-s={r}∪P∪Q` 連通。原 s-star 將 disk 分三面，
   這整塊在同一開面，其所有B附件只能終於該面的閉包框弧 A。
2. 原G full B-touch迫兩個非s-spoke框點都被這整塊碰到，因此都在A。
   三spoke的三gap總長5；有兩非spoke點的gap必長3，另兩gap各1。
   所以A恰為長3框弧；原恢復e也在原嵌入同面，沒有借X fullB-touch。
3. P、Q one-sided：刪P後仍有原 r-Q-s路；刪Q對稱。
   對任一 T∈{P,Q}，K_T的非B部分全在A。其他兩小star面不含T，
   在 K_T 的補面中可經原s及spokes連到H_G-T；所以其他兩條框邊
   在定義F_T的邊界。因此 **`σ_G(T)⊆E(A)`**。
   結論是「包含於長3弧」，不是「包含長3弧」。
4. 原盾弧σ_G(P)、σ_G(Q)互斥，各至少2邊，卻同落3邊A：`2+2>3`矛盾。

盾弧準確定義／互斥見 `docs/c5_unary_shield_budget.md:39–41,54–70`。
原long定義與N2殘留見 `artifacts/c5_excess_two_e4/REPORT.md:274–286`。
既有SL-STAR的面論證见 `audits/2026-10-10-n45-s-long-contract/REPORT.md:94–103`；
本段已重新用P/Q給兩費，未搬用不存在U的盾弧。

故 no-U TWOLONG exact S **必 `t_s<=2`、`d_H(s)>=3`**。
在 A 通過後，二連通單缺額推論迫 `d_H(s)=2`，遂可
**conditional排整個二連通TWOLONG exact-S子型**。
非二連通TWOLONG仍OPEN；本件没有actual 933/941 source，沒有finite trigger。

### 5.2 no-U LONG＋singleton-short：二連通chain的incidence上界

直接假设 no-U、exact S、H_M二連通、`d_H(s)=2`。chain与K4-free
使每件原P/Q的r incidence<=2、s incidence=1，總<=3。
權威原one-sided mixed支援下界（N45:107；所列完整degree4、fullB-touch、
原critical-contact witnesses、兩側positive incidence俱全）迫 actualsupport
至少2点，與 singleton-short矛盾。亦可用N45 S04＋同β CAP的完整
compatibility列證，不能用端點marginals。

故 singleton-short 的 ds2-bic exact-S子型無來源；
A通過後可conditional排該整個二連通子型。剩下可能的二連通no-U
LS short必為真框邊pair，r-side incidence只剩1或2。

## 6. 建議的一個最小後續橋接

選定 no-U LONG＋真框邊pair SHORT、exact S、H_M二連通、`d_H(s)=2`，
原 `t_r=1`、P/Q r-split=(2,2)，原 r-spoke e唯一，C恰三oddcycles，
其中 `J1∩J2={r}`、`J3`與它們不相交，唯一 inter-cycle bridge 是原邊
`uv`，`u∈J2`、`v∈J3` 都是相應環私有點。兩原s contacts 經terminal
arms接J1/J3私有點，沒有offpath blocks；保原有序contact、actual attachments、
support、ownership、rotation、e位置及字面β。

**候選義務：** 為該唯一inter-cycle bridge建立 boundary固定、
來源branch sets互斥連通的 minor，接到R27三共用點鏈；逐步核完整
degree4/5、fixed-β全部四色s probes（恰F_C={D}）及逐邊β witnesses，
並保兩terminal contact角色與R27 palette錨點不被錯誤識別。

最弱此处已知充分前提是：原M以T4完成R11區域定位；boundary固定的
actual minor仍在同一指定框弧；目標逐項進入R25/R26 forcing-list normalized
domain（三shared oddcycle鏈、末端私有contacts／arms、T–S–T palettes及
實際palette錨點），並核fixedβ全部四色s probes、完整degree4/5及β witnesses，
再引用R27**區域定位後**的來源minor合成。R27:65–84明列T4只用於原先
定位，後續minor不需保所有T4，故此路不宣稱target T4；若改以R27首頁
任意大小定理作黑盒套目標，則須另證target接受T4。僅有同個Gallai
block數、region、F_C(D)=false或四查詢仍不可省略normalized-domain／
palette錨點和actual branch-set映射。反例壓力是 bare uv收縮把兩degree4
端點合成完整degree6：四條cycle邊及兩條原B附件。刪附件使degree回4
還不能保拒絕。固定β、s=D的原Gallai tight certificate中，bridge palette
是 `{c}`，J2/J3的兩個二色palettes都避c，故必相交；不能直接沿用成
R27合併點的互斥palettes。若保原palette錨點，merged list是Col但兩
cycle palettes聯集至多3色，會出現slack。因此須另證合法attachment／
palette錨點處理及四s probes保持；且四布林值相同不保
完整relations、空fibres、rootpins。不得把目標lift當原G lift。

成功停止點：合成R27非disk minor回同一原G/M，僅排此具名子型；
無需宣稱完整Σ或r-fibres在minor下保持。失敗停止點：保留首個違反
degree、F四色、contact/palette錨點或branch-set互斥的具名來源控制與
完整原染色witness，回報這個bridge候選不能接R27。沒有actual source
或literal control時保持unknown，不以零觸發報來源排除。

相較之下，跨列r-fibre escape需實際證明某
`γ∈Q(G)\Q(X)` 有完整X lift且 `φ(r)!=γ(b_i)`；那雖直接恢復e，
但要求跨列非空與原完整preimage，較此一bridge非planarity義務大。

## 7. 覆蓋與證據停止點

- 原U省略、兩short S、完整U／long／short的限定契約仍採既有排除，
  不重開；权威范围 N45:49–67、410–422。
- 單缺額工具未给actual source realization；本件新增的是具名前提內
  的幾何／incidence推理，以及A未通過前的conditional二連通覆蓋。
- 既有R12／R14／R22／R24及R27只在逐項完成來源映射時供排除；
  同末端R31／一般更多環和 inter-cycle bridges 不因Gallai字樣全排。
- 本件沒有 literal controls；finite statuses不憑空填 triggered。
  來源前提與實際二連通記為unknown，A-based擴張記為conditional。
- 55只記兩缺額障礙，不擴一般B–E、ε>=3或主命題證明。
