# N45-S-HIGH1：完整契約內的任意大小排除候選

2026-10-10。BASE／執行 HEAD 均為
`dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`。
任務入口為[凍結發布文本](frozen/current/docs/history/2026-10-10-n45-low2-adoption.md)；
九個 current-work pins 全部吻合，與十六份 BASE blobs 分層，見[inputs](inputs.json)。

**交付候選：完整 HIGH1 契約內的來源 G 不存在，待獨立採納。**
先完成 X 自己的 degree／minimality、實際雙分量、完整接合與 BASE (2,1) 映射。
最後排除在原 G 上成立：兩 mixed 的支援邊若相交，直接抽出原 K₃,₃；
若不相交，原 U 的盾弧恰長二，單接點色對稱與完整 diagonal lifts 迫
Q(G) 包含於三個連續框點。933 的四拒絕位置與 941 的非連續三拒絕位置皆矛盾。
不將 X 的新接受列直接當作 G 的接受列；§7 直接構造遵守恢復邊的 G full lift。

沒有具名有限 HIGH1 source、source trigger 數或新 Lean。
Python 只核固定 metadata／色算術／relation 校準；任意大小來源論證是 paper。
本輪不自行採納，也不關 HIGH2/3、long、其他 cores、原55或一般 N2／E。

## 1. 全部來源前提與證據層

以下每項候選均量化任意大小有限 G，而非有限圖目錄。共同契約：

| 前提 | 原來源身份 |
| --- | --- |
| H1 | 有限簡單 disk G，有序 induced C5 B=(b0,…,b4) 圍外面 |
| H2 | 完整有序 Σ(G)=933／941 或一次共同整圖 D5 像；每條非框邊 Σ-critical；ε(G)=2 |
| H3 | 有效 H 連通、full B-touch；忽略的原孤立內點 I 在所有 full lifts 中仍為自由因子 |
| H4 | 非相鄰原 roots r,s 完整 degree5，其他有效原內點完整 degree4 |
| H5 | H−{r,s} 原分量恰 U,P,Q，三者 connected、one-sided、actual support 非空 |
| H6 | P/Q 各支援恰一條真原框邊的兩端，各接兩 roots；ownership／附件全留 |
| H7 | 原 U 只接 s，恰唯一原 contact sx，無 U–r 邊；U 整份保留 |
| H8 | mixed incidence=(3,2)：s 對 P/Q 各一，r 分配1與2，具名身份全留 |
| H9 | 原 r 兩 spokes，僅省略 e=rb_i，X 保另一條 rb_j；原 s 兩 spokes全部保留 |
| H10 | 固定原拒絕 literal β，X=G−e=M 自己是 β inclusion-minimal45／54 core；不從 G criticality 遺傳 |
| H11 | U/P/Q 全部原頂點、內邊、rootcontacts、框附件及其他 spokes 保留；无新增／替換／部分 piece 刪除 |
| H12 | 原 ordered contacts、單一 shared 頂點變量、actual supports／ownership、bridges／rotation、共同 literal 四色框、十列完整 relations、ambient 空／非空 fibres、全部 pins 與 full lifts 保留 |
| H13 | D5、S4、root swap 僅共同搬整圖及全部資料；933 q2 保留；不假定 β 是 U 盾中點列，G／X／刪 contact 圖各有自身邊與 lifts |

候選量詞、前提與依賴逐項另列於[claims](claims.json)。H1–H13 是交付 scope；
某子引理只需較少前提時，仍不在本輪擴大採納範圍。

| 依賴 | 用途／trust |
| --- | --- |
| [BASE R10](frozen/base/docs/c5_degree5_interfaces.md) §§1–4 | 完整 relation、degree-list slack、分量刪邊解除及不可刪減覆蓋，paper |
| [BASE weak lists](frozen/base/docs/c5_weak_list_cores.md) §1 | X 自己 minimality 迫同點的 β-spokes 異色，paper |
| [BASE sectors](frozen/base/docs/c5_degree5_two_spoke_sectors.md) §§1–3 | (2,1) 的區域／spoke 必要表，paper＋既有有限位置算術 |
| [BASE adjacent](frozen/base/docs/c5_two_spoke_adjacent_21.md)、[middle](frozen/base/docs/c5_two_spoke_middle_21.md) | 指定兩相鄰位置的原 K5 排除，含外部 Gallai／connected-exterior K4 trust |
| [BASE reflection](frozen/base/docs/c5_two_spoke_reflection.md) | 整圖／原 rotation／ordered tuples 共同搬運；不交換 C/U 身份 |
| [BASE split-support](frozen/base/docs/c5_two_spoke_split_support.md)、[nonadjacent](frozen/base/docs/c5_two_spoke_nonadjacent.md) | 分別為全列公式及指定 pA/pB 延拓；其任意大小結構與 finite-reduction trust 沿原文，不等於來源排除 |
| [BASE E4](frozen/base/artifacts/c5_excess_two_e4/REPORT.md) §4.1 | 原 one-sided short mixed 的每列全部同色 pins 有完整 lift（局部 N-diagonal）；不是只對已有外部 coloring 的敘述 |
| [BASE shield](frozen/base/docs/c5_unary_shield_budget.md) §2、§3 | 原 one-sided 盾弧連續、邊互斥、full B-touch 下實際支援=盾弧全部頂點；原 critical sx 迫 U 盾長≥2 |
| [BASE short support](frozen/base/docs/c5_short_support_singleton.md)、[K4](frozen/base/docs/c5_degree5_tree_components.md) | 上述 N-diagonal／unary shield 的 hub/Gallai 依賴 |
| [官方 Gallai 講義](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，[凍結 PDF](frozen/gallai.pdf) | 外部 Lemma7：connected degree-list 拒絕迫 tight；Theorem10：Gallai blocks 的不交 palettes 刻畫。此為外部信任，非本輪 Python／Lean 定理 |

九份 current pins 僅證交付身份。LOW1/LOW2 與獨立裁決只作參照；
沒有以 LOW 的 sole C 三接點排除替代 HIGH1 的雙分量論證。
正式推導採 BASE E4／shield 原文，與工作樹的後續註記分層。

## 2. HIGH1-CORE／COMP：X 自己與完整原雙分量

刪唯一 e 只令 r 的完整 degree 由 3 mixed+2 spokes=5 變為4；
s 的 2 mixed+1 U+2 spokes=5 不變，其他有效內點仍完整 degree4。
H_X=H_G，X 仍為 induced-C5 disk，繼承全部 T4。
H10 給 X 每條非框邊自己的 β-critical witness，因此也給自身 Σ-critical；
此處没有從原 G 的 criticality 遺傳。

H_X−s 的原頂點分割恰為 C={r}∪P∪Q 及完整 U。
C 內邊恰 E(P)∪E(Q)∪E(r,P)∪E(r,Q)，含全部三條原 r-mixed contacts；
其全部框附件恰 E(P,B)∪E(Q,B)∪{rb_j}。
U 內邊／框附件仍恰 E(U)／E(U,B)。兩分量之間無邊。
P/Q connected 且各接 r，故 C connected；U 原 connected。

令 s–P、s–Q 的原 contact 頂點為 y_P,y_Q，它們位於不同原 pieces，故互異；
s–U 頂點為 x。保 s 原三 contacts 的總 rotation，C 的 ordered sublist 是
該 rotation 中的 (y_P,y_Q) 次序，U 的 sublist 為 (x)。
r-contact 若同時是 s-contact，仍為同一原頂點、單一色變量；没有複製 port。
r 在 C 的內部 degree3、框 degree1，但完整 degree_X4，符合 R10 逐點前提。

## 3. HIGH1-JOIN／RESTORE：所有 literal γ、空 fibres 與恢復原邊

令 Col={0,1,2,3}。對任意 proper literal γ 定義 S_C(γ) 為原 C 全部
proper assignments，包含全部 C–B 約束，尤其 f_C(r)≠γ(b_j)。
S_U(γ) 同理，沒有 s pin。定義全部 ambient fibres，不先限非空支援：

```text
Fib_C(γ,t,c)={f_C∈S_C(γ): f_C(y_P,y_Q)=t, f_C(r)=c},
  t∈Col², c∈Col；支援外仍保留空 fibre。
Fib_U(γ,d)={f_U∈S_U(γ): f_U(x)=d}, d∈Col。
R_C(γ)={t: ∃c, Fib_C(γ,t,c)≠∅}，R_U(γ) 類同。
```

在同一 s 色 a 接合，X 的全部 full lifts 與下列資料 restriction／union 雙射：

```text
a∉γ(N_B(s)), t∈Col², c,d∈Col,
f_C∈Fib_C(γ,t,c), t 每座標≠a,
f_U∈Fib_U(γ,d), d≠a,
任意 I→Col 的自由原孤立點 assignments。
```

restriction 明確取同一份 full coloring 的 C/U/roots/I；union 使用不相交分量，
只在同一 s 色加三條 contact 不等式，故反向得到全部 X 原邊的合法 coloring。
在 C 內再把 P/Q 與同一 r=c 接合也有同樣雙射，兩條 r–P contacts
同時約束同一份 f_P；shared contact 再加 s 不等式於同一原色坐標。
不独立 normalize、不乘 endpoint marginals、不遺漏空 fibres。

G 的全部 lifts 恰為以上 X 資料再加 **c≠γ(b_i)** 的子集。
因此要證 γ∈Σ(G)，須有某 s query 的非空 C/U full fibre 且 r 投影含
γ(b_i) 以外的色；僅有 s 可用色不足。整個公式含全部十列、所有 r/s pins，
並在一次共同 S4／D5／root swap 下搬運 assignments、attachments、rotation 和空 fibres。

## 4. HIGH1-F：X 的精確不可刪減覆蓋與 HIGH1 的唯一次序

X minimality 迫兩 s-spokes 的 β 色互異，記 u,v，A_s=Col−{u,v}。
否则刪去其中同色 spoke 完全不變 constraints，與自身 β-critical 矛盾。
對 C/U 不 pin s，各 contact 有至少一色 strict slack：完整 degree_X4，
刪 s 少一 incident edge，但沒有扣 s 色。connected slack greedy 給 R_C、R_U 非空。

F_C(γ) 定義為「沒有完整 C tuple 能同時避色 a」的 a 集，F_U 同理。
完整接合給 A_s⊆F_C(β)∪F_U(β)。刪每條 s-spoke 的 full witness 強迫
剛釋出的 u 或 v 不被兩分量禁止，故聯集也包含於 A_s。
任刪某分量的 incident edge，R10 逐原邊的 slack 論證解除其全部禁色：
外邊在 endpoint 新增色、非bridge內邊給 connected slack、bridge 兩側各得 slack。
X 該邊的完整 β witness 遂給該分量的 private color。
兩分量各有 private color且聯集恰二元素 A_s，故 **F_C/F_U 是互異 singleton**。
沒有單憑 (2,1) 接點數猜 singleton。

另用原 G 的局部 N-diagonal。對任意 a≠β(b_j)，置 r=s=a，
P/Q 各有完整原 lift，rb_j 也合法，故 C 可避 s 色 a。
所以 F_C(β)⊆{β(b_j)}，非空迫 F_C={β(b_j)}。
β 是三色列，其未用色 D 不在任何原 spoke；因此
**F_C={c0}, F_U={D}，c0=β(b_j) 是 s-spokes 未用的那個 β 已見色**。
此處没有把 r 色投影丟掉：上述 C lift 特別保 r=a。

## 5. HIGH1-MAP：完整 BASE (2,1) 對應及限制

每個原拒絕 β=q_k 以一次共同 rotation 將 singleton 搬到位置4，
再以一次共同 S4 搬成 q=01012；原 e／rb_j、原 U/P/Q、ordered contacts、
ownership、rotation、全部 assignments/fibres 同時搬運。X 的 hub z=s、C₂=C、C₁=U。
R10、minimal q、T4、逐點完整 degree4/5、恰兩 connected 分量及 distinct contacts
已由§2–4逐項成立。β-normalization 不表示原 G 也成 canonical 933／941；
其完整拒絕位置同時搬運，不丟原 q2。

| normalized s-spokes | BASE 映射與所需充分前提 | HIGH1 處理 |
| --- | --- | --- |
| 02、13 | β 重色，与 X minimality 矛盾 | 排除 |
| 03 | sectors 的 (2,1) 必要位置表不容許；保全部 arcs／實際 attachments | 排除；不套 sole C |
| 01 | adjacent_21：兩不同 connected 分量、兩／一 contacts、同圖兩 crosscuts、degree-lists、Gallai／K4與原 K5 bags；不需第二拒絕列 | 直接適用，兩 singleton 次序原定理皆覆蓋 |
| 12 | middle_21：上述身份＋對應長 region、同圖三 exterior hubs，palette {3} bridge／leaf-cycle 原 K5 bags；不需第二拒絕列 | 直接適用 |
| 23 | reflection 的 ρ(i)=3−i、π=(0 1) 共同搬回01；包括 e、r pin、全部 rotation／tuples | 直接適用；不是獨立換 piece 的色名 |
| 34、40 | split_support：兩實際分量、指定全 support、degree-four結構／原 theorem 的 finite cover與全列 F/Z；40 只共同 reflection | 只證 X 單缺 β；不能改稱 G 不存在。§6–7另作原 G 排除 |
| 14、24 | nonadjacent：C/U 分居長／短 arc、兩 contact 次序；指定 pA=01021、pB=01212，原 completion、parent-pin transfer；24只共同 reflection且兩 query orbit交換 | 只給 X 指定 p 延拓。兩 C-region 身份皆保留，§6–7另排原 G |

HIGH1 的 F_C/F_U 次序由§4固定為已見色／D；既有 BASE 定理是否涵蓋兩次序
仍在表內明列，没有拿接點數替代定理前提。split 的 support 定理與 all-row 公式
不恢復 r 的 lost-spoke constraint；nonadjacent 的 parent-pin transfer 保的是
其定理指定 hub，不能擅自轉稱已保 HIGH1 的原 r projection。

[certificate](certificate.json) 的 theorem_mapping 保留941三 β及933四 β，
各十個 whole D5 actions，共70份 labelled metadata，逐份列全部十個 s-spoke pairs、
共同 β-normalization、原 r retained-spoke 候選與上述路由；重複 orientation 不去重。
這是前提映射算術，不是70份具名來源。無 r-fibre gap 被這張表自行關閉。

## 6. HIGH1-K33／ARC：兩原 mixed 支援迫 U 的原三點支援

P/Q 各有真框邊支援，原 one-sided 盾弧恰為該邊；原盾弧邊互斥，
故兩支援邊不同。若它們共用原框點 b_v，取六個 branch sets：

```text
左側：P、Q、O=B−{b_v}；右側：{r}、{s}、{b_v}。
```

六 sets 兩兩互斥且 connected：P/Q 原 connected，O 是原 C5 刪一點的框路徑。
九對原鄰接逐項如下：P–r、P–s、Q–r、Q–s 是各自原 contacts；
P–b_v、Q–b_v 是各自 actual attachment；O–b_v 有原框邊；
原 r/s 各有兩條不同 spokes，所以各至少一條 endpoint≠b_v，給 O–r、O–s。
這些是原 G 的 K₃,₃ bags 及九條原邊，矛盾 disk 平面性。
其中 O–r 可以恰用省略 e；此處在原 G 證非平面性，沒有在 X 虛構此邊。
P 的兩個原 r-contacts依然保留，未將 contracted bag 用作 coloring replacement。

因此 P/Q 支援邊頂點也互斥。C5 兩條頂點互斥邊的剩餘三條邊，
恰分成長二及長一的兩段。原 U 的唯一 sx 是 Σ-critical，取 G−sx 的新增列
完整 witness：限制到 G−U，s=x 色相同，U 否則可重染避 s 色接回 G，
故该列的完整 U forbidden query 非空。H−U={r,s}∪P∪Q connected；
G full B-touch 及原外路滿足 BASE shield §3 的全部前提，故 |σ_U|≥2。

σ_U 連續，與 P/Q 原盾邊互斥。因此只能恰取剩餘長二段，沒有長三支。
full B-touch 的原支援引理給 **N_B(U)=V(σ_U)，恰三個連續原框點**。
此推導不是把 β 當作盾中點列；先由原 topology／critical witness 決定 support，
再對全部拒絕列查色。

## 7. HIGH1-REJECT／EXCLUSION：恢復 e 的 full lift 與全部來源 orbit

對任意 proper γ，拿掉唯一 s contact 後 U 的 contact x 有 strict slack，
所以原 U 的完整 contact palette 非空。單接點 forbidden 集 F_U(γ) 至多一色：
若 palette 是 singleton {d} 則 F_U={d}，否则 F_U=∅。
這是全部原 U assignments 的存在性投影，不把原 fibres 更換成 singleton star。

令 γ 為任一三色列，未用色為 D。若 U actual support 沒見齊 γ 的三色，
另有 γ 已見色 h 沒在 U support 出現。整份 U 的全部 boundary constraints
在一次 transposition (D h) 下不變，所以它在全部原 assignments 上給雙射，
包括完整 contact palette／空 fibres。因此 F_U 同時包含 D,h 或同時不包含；
容量≤1 迫 **D∉F_U**。取一份完整 f_U 且 f_U(x)≠D。

同一 γ／同一 D 下置原 r=s=D。兩 roots 的全部原 spokes，包括恢復的
**e=rb_i**，皆合法，因為 γ 沒有使用 D。
原 N-diagonal 分別供應 P/Q 的完整 assignments，使各自所有原 r/s contacts
同時避 D。這三份 f_U/f_P/f_Q 和同一兩 root pins、任意 I 自由因子 union，
得到 **原 G 的全部原邊都合法的 full lift**。shared contact 永遠是一個值。
所以這不是先證 X 接受再猜可恢復；r 的具體投影 D≠γ(b_i) 已給出。

由§6，U support 為連續三點 T。三色 C5 的 canonical q_k 在 T 見齊三色
當且僅當其 singleton 位置 k∈T（十列／全部240 literal列的固定算術另核）。
因此所有原 G 的拒絕位置滿足 **Q(G)⊆T**，其中 T 是三個連續原框點。

933 的 Q={0,1,2,3} 有四點，不能包含於 T；941 的 Q={0,1,3} 是非連續三點，
也不等於任何連續三點。每個 whole D5 image 都保此性質；共同 S4 不改 singleton位置。
933 的新增 q2 明列在四點中，沒有以單一 q 正規形漏列。
所以完整 HIGH1 契約內原 G 不能存在。**此為任意大小 paper 候選，未自行採納。**

## 8. 工具控制、原失敗與驗證範圍

[checker](checker.py) 只用標準庫，不 import 上游決策；[certificate](certificate.json)
exclusive-create，`--check` 正常／seed17只讀重算並逐 byte 比對。
`checks-final.json` 保每個實跑的命令、cwd、environment、stdout／stderr檔案 hash與 exit；
原 `checks.json` 與最初 local check 也保留。
[封存工具](seal.py)、`manifest.json`、`delivery.json`、`receipt.json`
另核 payload 與 metadata 精確綁定；只有三個 top-level 當前 metadata 被排除，nested同名 receipt 是 payload。

| 控制 | 範圍／判定 |
| --- | --- |
| 同源 relation toy | 一份固定抽象圖，r 三 mixed contacts／一 retained spoke、s 的兩／一 contacts；P/Q 各有 shared contact 單坐標，U 一 contact，另原孤立點自由因子。十 canonical 列全64 C tuple/r fibres、4 U fibres、16 root pins與全部 full assignments；240 literal列 restriction/union 對直接 whole-graph colorings，**triggered and holds**，僅校準 |
| marginal 過強版本 | toy 在 γ=01023，C tuples={(0,0),(0,1),(2,0),(3,0)}，s-query0 沒有真完整 tuple避0，但兩 marginal 可各避0；**counterexample**，不是來源反例 |
| X延拓即G延拓的過強版本 | 同 toy 在 γ=01012，X 的兩份 lifts 皆 r=1，而 lost-spoke色也是1，G 無 lift；**counterexample**，toy不滿 X β-minimal、未提供 disk，不是 HIGH1 source |
| K₃,₃ schema | 5共端點、P/Q次序、兩 roots 各全部10個二spoke位置組合，共1000具名 adjacency schemas；九對鄰接／O框路徑核回，**triggered and holds**，不是1000 source graphs |
| 互斥支援與 U shield | 10 ordered頂點互斥真框邊 metadata，逐項只有唯一長二剩餘段，**triggered and holds**；連續盾弧／任意大小支援定理仍由 paper 承擔 |
| capacity-one 色對稱 | 5個連續三點 support×240 literal列×全部24 S4，核所有 invariant空／singleton F；100個933／941 whole-D5／support包含反證，**triggered and holds**，不窮盡原 U 圖 |
| β／spoke映射 | 70 labelled whole-source metadata、各10個 spoke pairs；933 q2照留，**triggered and holds**，只核定理路由所用位置算術 |
| finite HIGH1 source | **not triggered**：未建立／未執行來源 controls，沒有 trigger數；toy不是具名合法來源 |

toy 的 X/G full lifts 在240列各為2160／1560份，另自由因子乘4。
它保原 edge/attachment identity，rotation未提供，不聲稱 source realizability。
本輪沒有做新 graph/k 搜尋，沒有重開已採 U/LP/SS/LOW，也不使用 PC LP schema。

| 實跑 | 結果／真正範圍或拒絕階段 |
| --- | --- |
| normal／seed17 `--check` | 各 exit0；stdout／stderr逐 byte相同；certificate 1,960,670bytes，SHA256 `0aa93b73a4a46b204004752d8c32fce899f689d875d4e3368c4808b1e8e0f1bf` |
| bad certificate | exit2，**certificate byte comparison** 拒絕；不是來源前提拒絕 |
| bad input index | exit2，**input validation** 的 frozen-index binding 拒絕，尚未進 certificate比較 |
| 重複 generation | exit2，**exclusive certificate create**／FileExistsError；原 certificate bytes不改 |
| nested receipt omission | exit2，**payload inventory** 明列唯一 missing=`negative/nested/receipt.json`、extra=[]；實際 stdin metadata probe，沒有 synthetic inventory override |
| current `check_docs.py` | exit0，593 Markdown／7161 local links；此工具不掃 audits，另核本 report 20本地連結 |
| 正式 docs DocGraph | exit0，62 documents／213 relations／0errors |
| whole-worktree DocGraph | **exit1，62 duplicate-ID errors**；完整 stdout／stderr保存，原 scratch與本輪 frozen copies皆保留 |
| `git diff --check`／本 report links與新文本 whitespace | 各 exit0；Report補入實跑結果後另做 final local核對，原第一次 log保留 |
| input／tracked custody | 34 frozen inputs、9pins與5899 tracked files bytes不變；Git status 在專屬 audit 外零漂移。舊untracked樹僅對本輪實讀inputs核hash，不冒充全樹custody |

實跑及封存結果詳見 checks-final／receipt。新 report local links／whitespace與 inputs drift另核。
既存 BASE check_docs 的兩個歷史缺檔、全工作樹 DocGraph duplicate-ID 與歷史 E4 provenance FAIL
依原交付保留，沒有修共享文件、刪 scratch 或改旧 audit；本輪不將其統稱 PASS。
全工作樹 DocGraph 本次仍實跑並保存 FAIL，新增 frozen docs 的 duplicate IDs 也照實保留。
未重跑上游 finite結構／分類 checkers、歷史 E4 provenance、lake build／Lean axiom audit；
沒有新 Lean theorem，既有 Lean／有限 checks 不被升級為本候選的形式證明。

重播（canonical root）：

```bash
python3 -B audits/2026-10-10-n45-s-high1/checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-10-n45-s-high1/checker.py --check
python3 -B audits/2026-10-10-n45-s-high1/seal.py --check-delivery
PYTHONHASHSEED=17 python3 -B audits/2026-10-10-n45-s-high1/seal.py --check-delivery
```

## 9. 精確停點與獨立採納入口

十項 paper claims 及 scope 已交；完整 HIGH1 契約內未留下未滿的 r-projection 或 orbit gap。
這一句以§6的原 K₃,₃、§7的恢復 e full lift 與 Q(G) 反證為據，不能由工具 PASS 得出。
待獨立 reviewer 逐項核 CORE／COMP／JOIN／RESTORE／F／MAP／K33／ARC／REJECT／EXCLUSION 的
量詞、全部 H1–H13、BASE shield／N-diagonal／Gallai trust及原 G 九條 minor adjacency。

不自行發布／採納到共享 authority；HIGH2/3、long、其他 S 身份、原55、一般 N2/E、
ε≥3、source realizability 與 Lean 仍 OPEN。只新增本專屬 audit，無 commit／push／PR、
再委派或外部訊息；舊交付與 shared documents 保持原 bytes。
