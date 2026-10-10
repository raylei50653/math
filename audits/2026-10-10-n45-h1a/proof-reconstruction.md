# HIGH1 十項 claims 的獨立重推

量化任意有限大小原來源 G；每項結論都保留 worker REPORT 的全部 H1–H13。
以下只是本輪獨立紙面裁決，不能由 Python 或 metadata PASS 替代。
原 worker 的完整 [REPORT](../2026-10-10-n45-s-high1/REPORT.md) 與
[claims](../2026-10-10-n45-s-high1/claims.json) 均為只讀輸入。

## 1. CORE 與 COMP

原 degree r=3 mixed+2 spokes=5、s=2 mixed+1 unary+2 spokes=5。
唯一刪 e=rb_i 使 r 完整 degree4，s 仍5；所有其餘有效點完整4。
X β-minimal 是 H10 的獨立前提。它給每條非框邊刪去後的 β full witness，
而 β 本身拒絕，遂使 X 自身 Σ-critical；沒有將 G 的 criticality 遺傳給 X。
邊刪除保留 disk、induced B，且 G 的任一 T4 full lift 仍是 X 的 lift。

H 未改，H_X−s 精確是 C={r}∪P∪Q 及 U。P/Q 各原 connected 且各接 r，
所以 C connected；U 原 connected。C 保三條 r–mixed 原 edges、一條 rb_j、
全部 P/Q 內邊及框附件；U 保全部原內邊／框附件。兩分量無邊。
s 的 contacts y_P,y_Q,x 互異，(y_P,y_Q) 是原 s rotation 的有序子列。
原 shared rootcontact 若位於同一 piece 頂點，始終同一變量；不複製 port。
r 在 C 內 degree3、boundary degree1，完整 X degree4 正好滿 R10。

## 2. JOIN 與 RESTORE

對任意 proper literal γ，先保存 C 的全部原 assignments（含 r≠γ(b_j)）
及 U 的全部原 assignments，再為每個 ambient t∈Col²,c,d∈Col 保存
Fib_C(γ,t,c)、Fib_U(γ,d)，支援外是空集合。
同一 s=a 避其兩原 spokes，三個 contacts 同時避 a，原孤立點 I 自由取色。
restriction 取得這些資料；union 沿不相交原頂點集加回同一 s 及三原邊，
兩方向互逆。C 內的 P/Q 也只能用同一 r=c 接合。

G 比 X 恰多原 edge rb_i，故其 full lifts 精確是上述 full assignments
滿 c≠γ(b_i) 的子集合。這對全部 literal rows、全部 pins、空 fibres、
所有 I 自由因子成立。γ∈Σ(X) 不足以推出 γ∈Σ(G)。共同 D5/S4/root swap
是整圖、全部 edges/contacts/rotation/pins/assignments 的一個雙射，
不能對 C、U 另作 normalization。

## 3. F 的 private-cover 與未用色身份

β 下 s 的两原 spokes 異色 u,v，否則刪一條重色 spoke constraints 不變，
違反 X 自身 β-minimality。A_s=Col\{u,v} 有二色。
忽略 s pin 時各 C/U contact 至少一色 slack；其餘點是 degree-lists，
兩 connected 分量皆有 full assignment，因此 R_C、R_U 非空。

完整接合與拒絕給 A_s⊆F_C∪F_U。刪兩 s-spokes 各有 β full witness，
新可用色分別為 u、v；原拒絕迫 witness 使用該新色，故 u,v 都不在任一 F。
所以聯集恰 A_s。刪每分量的一條原 contact edge，僅該分量約束改變；
X 的 β witness 給此分量的 private forbidden color。R10 全 degree4
刪邊解除引理（boundary/contact 新色、非bridge degree slack、bridge兩側slack）
逐點可用於 C，包括 r。兩分量各有私色而聯集只有二元素，故各是不同 singleton。

BASE E4 §4.1 是局部 N-diagonal：對原 one-sided degree4 mixed、真框邊
support、任意 proper γ、任意色 a，同色 r=s=a 有完整原 piece assignment。
它明文毋須已有 G−piece 的合法 exterior coloring。
對 β，a≠β(b_j) 時把兩原 pieces 各 full assignment 接在 r=a 上，得 C
全部 contacts 同避 a，且 retained spoke 合法。因此 F_C⊆{β(b_j)}。
非空迫 F_C={c0=β(b_j)}；β 三色的未用 D 不在 s-spokes，
故 A_s={c0,D}、F_U={D}。此步保 r=a 的完整投影，並無 marginal 替代。

## 4. MAP 的八個 BASE routes

用一次整圖 D5 把 β singleton 搬到4，再一次共同 S4 把 β 搬成 q=01012。
原完整拒絕位置集合、被刪 edge、retained spoke、兩原分量、所有 fibres
同時搬；不將原來源 Σ 當作仍在同一固定 933/941 標號。
X 的實際 hub 是 s，唯一完整 degree5，H−s 分量正是二／一接點 C/U。
它是 connected q-minimal disk、所有其餘有效點完整4、接受全部 T4，
接點互異，R10 所需 private singleton 身份已成立。

| s-spokes | 所核原定理與必要／充分前提 | 結果界線 |
| --- | --- | --- |
| 02、13 | q 重色；weak lists／自身 minimality | 不可能 |
| 03 | sectors §§1–3：上述完整 X 前提、兩 actual regions、共同色置換 | (2,1) necessary table 不容許；不使用 sole-C theorem |
| 01 | adjacent_21 §§1–5：兩不同 connected 分量、兩／一 contacts、長 region、both private-color orders、actual crosscuts、Gallai/K4與原 K5 | 排除 X 此位置；不需第二拒絕列 |
| 12 | middle_21 §§1–4：同 X identity、長 region、both orders；三 actual exterior hubs、bridge/leaf-cycle palettes與原 K5 | 排除 X 此位置；不需第二拒絕列 |
| 23 | reflection §1–2，ρ(i)=3−i、π=(0 1)，q保留且整圖/rotation/tuple搬到01 | 排除此整圖像，不交換兩／一接點身份 |
| 34、40 | reflection support theorem＋split_support §§1–6；完整 X source hypotheses、實際 support、全 degree4 arbitrary-size reduction與既有 finite cover | 只得 X 全列 single-missing，仍須原 r 恢復條件；40僅整圖reflection |
| 14、24 | nonadjacent §§1–7：完整 q-minimal/T4 X、兩 opposite regions、兩contact counts及各F次序、原 degree4 structural reductions、全部 parent-pin transfer | 指定 pA/pB 延拓只屬 X；24整圖reflection與相應 query搬運 |

Gallai、connected-exterior K4、原 degree4 structural reductions及既有有限必要
模板 cover 都是明列繼承 trust。本輪讀原 paper 前提／結論，未重跑所有上游
finite checkers 或新形式化。X 的 pA/pB witness 可能 r=γ(b_i)，因此此段
ancillary 不承擔 HIGH1 的最終原 G 排除；下述 K33/ARC/REJECT 独立補足。

## 5. K33：原 G 的六 bags、九鄰接

P/Q actual supports 都是一條真框邊的兩端。BASE shield §2、引理2 與 full B-touch
使盾弧就是各一條原框邊；互斥使兩邊不同。若共端點 b_v，取左右 bags
(P,Q,O=B−{b_v})／({r},{s},{b_v})。
六 bags 互斥、非空、connected；O 是 C5 刪一點的四點原框路徑。
九原鄰接為 P-r、P-s、P-b_v、Q-r、Q-s、Q-b_v、O-r、O-s、O-b_v。
前四 rootcontacts 與兩 attachments 是 H5/H6/H8 的原邊。
原 r/s 各有兩個不同 boundary 鄰點，所以至少一條 spoke 不終於 b_v，
給 O-r、O-s；O-b_v 有原框 edge。O-r 可使用 e：此 minor 位於原 G。
不將原 G 邊在 X 中虛構，也不將 bags 當作可任意重染的 coloring replacement。
這是 K₃,₃ minor，與 disk 平面性矛盾，故 P/Q 支援邊頂點互斥。

## 6. ARC：critical sx 與原 U support

H−U={r,s}∪P∪Q connected，U 原 connected，且 x-s 唯一原 contact。
Σ-critical sx 有 γ∉Σ(G)、γ∈Σ(G−sx) 的完整原刪邊 witness f。
必有 f(s)=f(x)，否則 f 已是 G full lift。若 U 可另完整重染令 x避 f(s)，
保同 γ 及 G−U 的整份 assignment 即拼成 G full lift，矛盾。
所以該列 U 的 full forbidden query 非空；不是宣稱所有 β 下都如此。
BASE shield §3 的外路由 H−U connected 加 full B-touch 得到：若 U support
在任一框邊內，外部有抵達別框點的同源路，短支援 hub 引理令 F_U 全空，
矛盾。故原 |σ_U|≥2。

U 盾弧連續，且與 P/Q 各一條原盾邊互斥。C5 兩條頂點互斥邊的補集
是唯一長二段與另一長一段；唯一能容連續長≥2的 U 盾弧就是長二段全部。
BASE shield 引理2（full B-touch）把 σ_U 的每個端點及內點都還原為實際
attachment support，所以 N_B(U)=V(σ_U)=T，恰三連續原框點。
沒有 β 中點、spoke 正規化或 reduced-graph shield 費用假設。

## 7. REJECT：任意三色 row 的原 G full lift

對任意 proper γ，忽略 s contact 後，U 的 x 有 strict slack，其餘點有
degree-lists，故完整 U assignments 非空。唯一 contact 的完整 palette A_x
非空；F_U(γ) 若非空則 A_x 是 singleton，因此 |F_U|≤1。
這是一個完整 palette 投影，完整 fibres 仍是原 U 的全部 assignments。

取任意三色 γ、未用 D。若 U actual support T 沒見齊三色，取已見而不在
T 出現的 h。整份 U boundary constraints 在 (D h) 下不變，故此單一
整 piece 色置換是 full assignments／ambient fibres 的雙射，F_U invariant。
若 D∈F_U 則 h∈F_U，違反容量≤1；所以 D∉F_U，有完整 f_U 令 x≠D。

同 γ 下選原 r=s=D。兩 roots 的全部原 spokes 均合法，包括 rb_i=e，
因 γ 所有 boundary 顏色都不是 D。BASE local N-diagonal 在同一 γ/D 下
各給 P/Q 完整原 assignments，所有 rootcontacts 均避 D。
三 pieces、兩同色但非相鄰 roots、B、I 的 assignments 沿原圖 union，
每條原內邊、框附件、rootcontact、spoke 都合法，shared contact 不複製。
因此 γ∈Σ(G)。此見證在 G 而非僅 X，且 r projection D≠γ(b_i) 明確成立。

## 8. EXCLUSION：全部 source orbit 與 933 q2

canonical 三色 q_k 在三連續框點 T 見齊三色恰當 singleton k∈T。
理由：三色 C5 是 A B A B C 的 whole D5/S4 像；連續三點含singleton時
兩側鄰色為另兩色，未含singleton時只見重複A/B。
§7 因此迫原所有拒絕位置 Q(G)⊆T。
933 的四點 {0,1,2,3} 不可能包含於三點 T；941 的 {0,1,3} 是非連續三點，
不等於任何連續 T。whole D5 保基數與連續性，共同 S4 保 singleton位置。
933 q2 明確包含；無單一 q-normal form 遺漏另一拒絕列。

故十項 claims 均在完整 H1–H13 下成立，沒有新增來源前提。
任意大小排除由上述 paper ＋ BASE／外部 trust 承擔；無 finite source／Lean。
