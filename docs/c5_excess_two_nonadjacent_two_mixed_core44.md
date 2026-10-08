# ε=2 非相鄰兩 mixed：U4 的兩-root44身份排除

2026-10-08。接續 [C44″ 的 U4](../artifacts/c5_excess_two_c44pp/REPORT.md#5-最小未覆蓋子分支清單)
及 [E4 的 N2](../artifacts/c5_excess_two_e4/REPORT.md#4-n2局部-diagonal-接回與共同盾弧預算)，
基準 `main @ 2971d46d715d213f25f534958bdab499d2573b69`。
目前研究線與停止點見 [Kempe 導覽](c5_kempe_guide.md#3-停止點與保留缺口)。

**結論：完整 Σ=933／941 或其整圖 D₅ 像、Σ-critical、ε=2 的 induced-C₅ disk
來源，若兩個 degree-5 roots 非相鄰且恰有兩份 mixed，則不存在兩-root
degree-(4,4) minimal rejected-row core。U4 的全部省略身份排除。**

結合 U1／U2／U3 與前序唯一 mixed 排除，完成上述固定完整 Σ 前提下的
兩-root44身份。這不排除沒有44 core的 ε=2 來源；單-root刪除例外、45／54／55
cores、E5新證明要求、ε≥3、一般出口及 `K∞=K≤5` 仍保留。
證據為任意大小紙面化約、既有全四分類及新 Python 固定必要域／獨立重播，未新增 Lean theorem。

## 1. 同一原圖與原 mixed11 省略

G 有限簡單，B=(b₀,…,b₄) 是指定有序 induced C₅ disk 外框。
完整 Σ(G) 是933／941或整圖 D₅ 像，每條非框邊 Σ-critical。
有效內部 H 連通且碰齊五框點，恰兩個完整 degree-5 roots z,w，原 zw 不存在；
其他有效內點完整 degree 四。H−{z,w} 恰有兩份原 mixed，其餘分量為 unary。
原頂點、內邊、ordered contacts、shared contacts、ownership、實際附件／支援、
嵌入環序及原 bridges 始終屬於同一 G。只共同搬運整圖的 D₅／S₄ 色框。

取 G 拒絕的 q 及兩-root44 minimal q-core M。
[E4 原省略身份](../artifacts/c5_excess_two_e4/REPORT.md#6-完整原-relation-的參數化交付與-core-身份)
給 M 恰整份省略一個原 mixed11 O；保留另一 mixed P、全部原 unary 及全部原 spokes。
因此 M=G−V(O)，沒有額外省略。原 degree-4 飽和保留各 piece 的全部內邊與附件。
M 自己的 q-minimality與G的 Σ-criticality分開使用。

M 的內部連通、所有有效內點完整 degree 四；繼承 disk 及 T4。
[全四分類](c5_k4_blocks.md#4-合成全-degree-4-的單缺失結論)
給 Σ(M)=Ω∖{q}，內部為路徑、單 triangle 加不分叉 tails，或兩個互斥 triangles
由直接原 bridge 相連、恰六內點且無 tails。
兩-root44的 retained P 各側 incidence d_z,d_w∈{1,2}；兩側2形成互斥 root triangles。

## 2. 原支援下界、盾弧與新的三-spoke收窄

兩原 mixed 及所有 unary 都 one-sided：刪去任一 mixed，另一份仍連回 z,w。
故 [原盾弧引理](c5_unary_shield_budget.md)適用於原 G，而非只向 M 收費。

**O 的實際支援至少二點。** 假設 |N_B(O)|≤1。刪一條原 root–O 邊的
Σ-critical witness，固定同一原 G−O 的完整染色；原 O 無法接回。
每點的 degree lists 至少內 degree，拒絕迫 tightness及 Gallai tree。
K₄ block 由 [連通外部 hub 的原 K₅ minor](c5_degree5_tree_components.md#1-連通外框排除-degree-4-分量的-k4)
排除：G−O連通，每個K₄點只有一個外接方向；四條互斥tethers都須抵達該外部，
否則未碰外部的連通著色支枝可交換整份顏色，不能提供唯一bridge強迫色。
外部與tethers尾部是一個hub，四個K₄點為另外四bags。較大clique也違反平面性。
餘下 Gallai blocks 為 bridges／odd cycles。每個O點至多一條框附件；
末端bridge的private leaf至少消耗兩條root incidence，末端odd cycle至少兩個
private degree-two點，各消耗一條。多block至少兩個末端，需求≥4；
單bridge需求4、單odd cycle需求≥3，均超過O的兩條原root邊。
Singleton O最多兩個root鄰点與一個框鄰点，degree≤3，亦矛盾。

**P 的實際支援也至少二點。** 全四core至多兩個內degree三點，沒有內degree四點。
若P最多碰一框點，每個P點的內degree至少三，故 |P|≤2。
Singleton不可能有degree四；兩點則必互相相鄰且均同接z,w，得到diamond
K₄−zw，其block不是clique／odd cycle，違反Gallai分類。

Short mixed的支援恰一條框邊的兩端，原盾弧長一；long mixed與unary各至少二。
令ℓ為原long mixed數、u為原unary數，原盾弧互斥給

\[
5\ge\lambda_O+\lambda_P+\sum_U\lambda_U\ge2+\ell+2u.
\]

所以 ℓ+2u≤3，整個u=2身份排除。u=0且兩 mixed 都short沿用
[N-diagonal](../artifacts/c5_excess_two_e4/REPORT.md#4-n2局部-diagonal-接回與共同盾弧預算)：
兩roots都取同一未用色D，接回各份完整piece，原G接受全部三色列，矛盾。

**新的star收窄涵蓋兩short加unary。** 無own unary且d_r=1的root有三條原spokes。
原H−r經O、P及另一root連通，所以全部其餘pieces位在三-spoke star同一面。
原全B-touch迫三spokes連續；该面框弧長三，所有原pieces的完整盾弧亦在其中。
有一份unary時，即使兩mixed都short，也須至少1+1+2=4條框邊，超過三。
故u=1時無unary側必d=2。

Unary側若也d=2，capacity≥2會使root內degree≥4；capacity1則給該root
的P-triangle加原U接枝。單triangle中的另一root是非割degree-two點，兩roots
在同triangle必相鄰；雙triangle不能再有額外tail。兩者均矛盾。
因此u=1必為d(unary側,另一側)=12，k_U∈{1,2}。
k_U=1對應單triangle加tail；k_U=2對應六點雙triangle。

u=0的d11也不保留：若有long，兩root各三spokes的可接觸框弧交集
不含三個連續框點；若兩short，已由N-diagonal排除。
具體令z-spokes為012，另一root的連續三spokes只能234或340；兩長面交集
分別為{0,2,4}或{0,2,3}，都容不下long mixed的連續三點支援。

## 3. 保留原root的任意長度必要域

剩餘M只有以下兩種實際標記形狀：

- 單triangle：w是非接枝triangle點，z在某條不分叉tail；無unary時z為leaf，
  unary容量一時z是非葉點。另一條tail若造成第二份unary，已由§2排除。
- 雙triangle：恰六原內點、直接原bridge。保留全部非相鄰root位置。

Tree/path不可能有無own-unary的d2 root：P的兩contacts與root形成cycle。
u=0的d11已排；u=1已迫d12。沒有用原H有環偷推H_M有環。

單triangle沿用 [18單run／8雙run的原附件分類](c5_triangle_path_reduction.md)。
為保存z，**保持triangle與z為singleton，分別縮z前後的未標記正區段**。
同附件run的可用色集至少二；固定兩端色時，二色靠交替、至少三色可直接选色，
每個正run的完整端點relation只依奇偶。零區段仍為零；正奇縮一、正偶縮二。
各縮減亦是原路徑內的boundary-fixed minor，不碰整份原O。
因此任意字面β下，保存triangle＋z的完整joint，進而保存K_M(β)的兩root投影。
沒有聲稱縮圖與原長圖的全部contact tuples逐座標相同；兩張實際圖各自的
完整contact joint、附件與全圖witnesses分別保存。

Uniform非葉marker的前／後區段為
(p,s)=(0,0),(0,2),(2,0),(2,2),(1,1)；另列leaf。
雙run為X,Y^(正偶數),leaf：marker在X、leaf或Y；Y前後只需
(0,1),(1,0),(1,2),(2,1)。其他tail按原正常形保留。

| 固定必要上界域 | 標記數 |
| --- | ---: |
| 單triangle uniform | 220 |
| 單triangle two-run | 96 |
| 六點雙triangle：retained22、無unary | 256 |
| 六點雙triangle：retained12／21、unary容量二 | 256 |
| 合計 | 828 |

316單triangle域含4份已被star排除的「唯一unary在d2側」marker，保留作安全放寬；
精確必要子域是312。有限排除對放寬域仍零殘留，沒有將這4份當作來源。
雙triangle由128份saved lifts逐列重算後取64份q-core，各列全部8個非相鄰markers。
Root交換只共同轉置全部資料；不獨立正規化pieces。

## 4. 完整同框接回與每行／每列一格容量

固定同一β。T_O(β)先從整份原O的全部染色取得其有序contacts tuple，
shared contact只占一個原頂點，再寫成重複角色。
\(\mathcal T_M(β;P_M)\)是包含原z,w及全部保留piece contacts的完整joint，
每個tuple有M的全圖witness。精確接回為

\[
\{(v,t):v\in\mathcal T_M(β;P_M),\ t\in T_O(β),\
 v_z\ne t_z,\ v_w\ne t_w\}.
\]

先取得M的完整joint，再定義core投影
\(K_M(β)=\pi_{z,w}(\mathcal T_M(β;P_M))\)，並置

\[
F_O(β)=\{(a,b):\nexists(c,d)\in T_O(β),\ a\ne c,\ b\ne d\}.
\]

上述原G整tuple接回非空 iff K_M(β)∖F_O(β)非空。
原zw不存在，允許同色pins。

原O每點完整degree四。刪兩條root incidence後，lists至少內degree加上
該點的原port數。固定w=b至多刪一色，z-contact仍有strict slack；
shared contact時原slack二，扣一色仍有slack。連通生成樹貪婪法給整份原O染色。
因此固定b時，F_O每欄至多一格：若兩個不同a都被禁，該非空完整lift的
z-contact須同時等於兩個不同色。交換roots給每行也至多一格。
這個容量結論來自整份lift，沒有相乘contact marginals，也不要求O是singleton。

新有限域的每份M在q之外的四個三色列，都有兩個完整root pins共用一側座標。
兩對均附同一圖的完整port tuples及全圖witnesses。F_O不能同時覆蓋兩對，
因此O不能新增任何三色拒絕列；G與M接受相同的五個三色列。
M只拒q，故G也只能拒一個三色列，而完整933／941分別拒四／三個三色列，矛盾。

828份核心×4三色列=3,312份容量碰撞全部成立。
另核對828×10目標D₅ masks=8,280次比較：2,484份目標接受空q、
5,796份由同座標容量排除，零殘留。固定S₄支援篩、新收縮星及新的topology
subdivision階段均未觸發；原O的支援與完整relation不曾被替換成自由逐列schedule。

## 5. 證書、實際控制與信任界線

[Primary](../scripts/c5_excess_two_nonadjacent_two_mixed_core44.py)不import歷史producer，
由三份小archive重建必要域；[證書](../artifacts/c5_excess_two_nonadjacent_two_mixed_core44/observations.json)
保存原邊、完整degrees、contacts／ownership／附件／支援、原bridge、全部字面
port tuples、132,480份root fibres（含空者）、全圖witnesses及15,460份q刪邊lifts。
316張標記長圖保存原root singleton branch sets，核對3,160次root pairs與
3,160次triangle＋z完整joint；這些是公式控制，無界證明由§3承擔。

[獨立auditor](../scripts/c5_excess_two_nonadjacent_two_mixed_core44_audit.py)另重建marked
domain、十列、D₅及固定順序全圖回溯，沒有import primary。
[獨立證書](../artifacts/c5_excess_two_nonadjacent_two_mixed_core44/independent_audit.json)
核對完整joints、空fibres、刪邊witnesses、容量碰撞及長圖化約。
其65,536份二元relation代數補驗得到65,431份row／column容量相容relation及89份F像，
但來源排除只使用已證的每行／每列至多一格，不依賴該有限計數。

[具名原圖控制輸入](../artifacts/c5_excess_two_nonadjacent_two_mixed_core44/control_input.json)
保留舊U4 `U4-SHORT-NEAR-1018` 的literal邊、原apex rotation與舊bytes hash，
本輪重新算完整relations、degree、disk rotation及19份原Σ-critical刪邊witnesses。
其Σ(M)=1022、Σ(G)=1018；單列44／完整接回為「觸發且成立」，
完整目標Σ前提為「未觸發」。01023是新增拒絕的第四色列，所以
**整十列Σ(G)=Σ(M)不成立**；本頁只使用三色列的相等。
長圖的全部contact座標等價也不成立；獨立audit保存具名非等價控制，
不影響共同triangle＋z joint及兩root接回。

```sh
python3 scripts/c5_excess_two_nonadjacent_two_mixed_core44.py
python3 scripts/c5_excess_two_nonadjacent_two_mixed_core44_audit.py
python3 scripts/c5_excess_two_nonadjacent_two_mixed_core44.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_nonadjacent_two_mixed_core44.py --check
python3 scripts/c5_excess_two_nonadjacent_two_mixed_core44_audit.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_nonadjacent_two_mixed_core44_audit.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph --include 'docs/**/*.md' check
git diff --check
```

生成與重播只需標準函式庫。大JSON依MANIFEST指定路徑重建；舊U4證书及其
hash漂移未覆寫。任意大小覆蓋沿用degree-list／Gallai、全四分類、triangle接枝／
分叉及run分類的紙面與有限拓撲信任。本輪未重稽核全部上游枚舉、ES／ER、
LC額外targets／axioms。lake build只驗既有Lean專案，未形式化新紙面證明。
實際驗證與檔案hash見 [研究紀錄](history/2026-10-08-u4-two-mixed-core44.md)。

**精確停止點：U4完成，固定完整Σ下的兩-root44身份全部排除。**
剩餘是完全無44 core的來源、單-root例外及45／54／55 cores；E5的新證明要求與
三列的一般推廣另保留。未證ε≥3、猜想E任意大小、一般出口或K∞=K≤5。
