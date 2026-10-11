# ε=2 相鄰兩份 mixed：U2 的兩-root (4,4) 身份排除

**後續（2026-10-08，U4完成）。** [非相鄰兩mixed的U4](c5_excess_two_nonadjacent_two_mixed_core44.md)
現亦全排，固定完整Σ933／941下兩-root44身份全部完成。
下文保留本頁當輪停止點及後續紀錄；單-root例外、45／54／55與ε≥3仍保留。

**後續（2026-10-08，U3完成）。** [U3 mixed12／21](c5_excess_two_nonadjacent_mixed12_core44.md)
連同mixed11／22關閉U3兩-root44身份；目前完整Σ下的44殘留只剩U4。
下文保留U2當輪範圍與驗證。

**後續（2026-10-08）。** [U3 sole mixed11](c5_excess_two_nonadjacent_one_mixed_core44.md)
已排兩-root44身份；完整Σ下44殘留為U3 mixed12／21及U4。本頁保留U2當輪結論與驗證。

2026-10-08。接續 [C44″ 的 U2](../artifacts/c5_excess_two_c44pp/REPORT.md#5-最小未覆蓋子分支清單)，
基準 `main @ 2971d46d715d213f25f534958bdab499d2573b69`。
目前研究線與停止點見 [Kempe 導覽](c5_kempe_guide.md#3-停止點與保留缺口)。

**結論：完整 Σ=933／941 或其整圖 D₅ 像、Σ-critical、ε=2 的 disk 來源，
若兩個 degree-5 roots 相鄰且恰有兩份 mixed，則不存在兩-root (4,4)
minimal rejected-row core。更精確地，任一原 incidence-(1,1) mixed D 都滿足
Σ(G−D)=Ω。**

這關閉 U2 的44省略身份；不排除整個相鄰 m=2 來源。
(4,5)/(5,4)、原 (5,5) core、非相鄰 U3／U4 及 ε≥3 仍保留。
證據為任意大小紙面化約、既有外部／有限分類及新 Python 固定必要域；未新增 Lean theorem。

## 1. 同一原來源與省略身份

G 有限簡單，B=(b₀,…,b₄) 是指定有序 induced C₅，為 disk 外框。
完整 Σ(G) 是933／941或其整圖 D₅ 像，每條非框邊 Σ-critical。
有效內部 H 連通，恰有兩個相鄰完整 degree-5 roots z,w，其他有效內點
完整 degree 四。H−{z,w} 恰有兩份原 mixed，其他原分量為 unary。
所有原內邊、ordered contacts、實際附件、ownership、支援、cyclic order
及共同色框始終屬於同一 G。

[Root／zw 全收](c5_excess_two_root_deletions.md#4-相鄰-mixed刪原-root-邊的全-degree-4-化約)
給 Σ(G−zw)=Ω，兩個刪 root 圖也都全收。因此拒絕列的 minimal core
保留 z,w,zw。原 degree-four 飽和使每份原 piece 全取或全不取。
[共同省略身份](../artifacts/c5_excess_two_e6/REPORT.md#3-e6-bcj6-的共同-core欄位與框邊預算)
給44核心只能整份省略一個 mixed11 D，不能再省略 spoke 或 unary；另一份
mixed C 也為11，其 contacts 共用原 x，形成原 triangle zwx。記 M=G−D。

M 的有效內部連通，所有有效內點完整 degree 四。若 M 拒絕 q，任一 minimal
q-core 的飽和沿內部連通性傳播至整張 M，所以 M 自己是 minimal q-obstruction。
它繼承 disk、T4；[全 degree-4 分類](c5_k4_blocks.md#4-合成全-degree-4-的單缺失結論)
給 Σ(M)=Ω∖{q}。

反過來，即使只先選任一原 mixed11 D，而不先假設44核心，M 也全 degree 四且
內部連通。若拒絕 q，以上飽和與分類會迫保留的另一份 mixed 恰為共鄰 C11，
故仍落在本報告的必要域。這說明 Σ(G−D)=Ω 的較強措辭。

在 M 自己套 [保留 mixed 的原形限制](c5_excess_two_mixed_core_spokes.md#3-44-且保留-mixed原形比-contact-數更受限)：

- 單 triangle：C 是從 x 起的原不分叉路徑，允許 C={x}；原 unary
  每側至多一份、capacity 一。C 非 singleton 時，兩 roots 合計至多一份 unary。
- 雙 triangle：兩個互斥 triangles 直接橋接，恰六內點、無外掛樹。
  C 是 singleton x，或 x 直接橋接第二個 triangle 的四點原分量。
- 每側 t_r+u_r=2，u_r∈{0,1}，所以 t_r∈{1,2}；雙 triangle 的 roots
  若保留 unary，該 unary 本身可以含另一個 triangle，不把它當普通路徑枝。

這裡沒有提前把 C 或 D 改成 singleton。E6-A 的兩 mixed 外界路限制仍適用：
含 B 的 theta 面由兩份 mixed 路圍成，zw 在有界側。本輪排除域放寬而未額外
篩這個條件，也未按原盾弧預算刪支援，故不依賴此幾何條件提升覆蓋。

## 2. 完整同框接回與原 D 的89份禁對

固定同一 proper boundary coloring β。令 P 依序包含原 z,w 及 M 的所有
原分量 contacts，共鄰 x 只佔一個頂點座標；\(\mathcal T_M(β;P)\) 是完整
P-tuple relation，每個 tuple 有 M 的全圖染色 witness。原 D 的 ordered
contacts 為 (s,t)，容許 s=t；\(T_D(β;s,t)\) 先由原 D 的完整染色取得，
共鄰時只記一個原頂點，再寫成重複角色 (c,c)。

精確接回是

\[
\{(v,u):v\in\mathcal T_M(β;P),\ u\in T_D(β;s,t),
       \ v_z\ne u_s,\ v_w\ne u_t\}. \tag{1}
\]

兩份完整原 witness 只共用固定 B，檢查兩條原 root–D 邊後即可拼接。
原 zw 已在 M，不能另把 z,w 的 marginals 相乘。取得完整式 (1) 後才投影
\(K_M(β)=\{(v_z,v_w):v\in\mathcal T_M(β;P)\}\)，並定義

\[
F_D(β)=\{(a,b):\nexists(c,d)\in T_D(β;s,t),\ a\ne c,\ b\ne d\},
\qquad β\in\Sigma(G)\iff K_M(β)\setminus F_D(β)\ne\varnothing. \tag{2}
\]

原 D 每點的 degree 恰四。去掉兩條 root incidence 後，其 lists 滿足
\(|L_D(v)|\ge\deg_D(v)+[v=s]+[v=t]\)；s=t 時兩個 slack 都計入。
固定 w=b 最多在 t 去掉一色，s 仍有 slack，連通生成樹貪婪法給一份完整
D 染色。因此 F_D 每欄至多一格；交換 roots 給每列至多一格。
兩份不同禁對 (a,b)、(c,d) 若同時存在，完整 T_D 必落在
\(\{(a,d),(c,b)\}\)，容量使兩個 tuples 都存在，遂不可能有第三禁對。
沿用 [各一 incidence 的證明](c5_mixed_capacity_contacts.md#5-各一-incidence至多兩個禁對與新的對稱-residual)，
不要求 D 為唯一 mixed。

所以 F_D 只有空、單格、兩格且 rows／columns 均不同，共89份必要選項。
[獨立 auditor](../scripts/c5_excess_two_adjacent_two_mixed_core44_audit.py)
由全部65,536份完整二元 relations 重建 F；65,431份滿足 row／column 容量，
其像恰為89份。這是有限代數控制，不是來源圖枚舉。

唯一原實際支援 S=N_B(D) 在所有列固定。若 p|S=π(β|S)，置換整份原 D
染色給 \(T_D(p)=πT_D(β)\)、\(F_D(p)=πF_D(β)\)。每個 equality shape
只能共用一份選擇，且必被代表支援色的 stabilizer 固定。本輪保存全部32份
具名 S、81個 shapes、逐列 S₄ transport；包含空支援只是必要域的放寬。
相同 shape 的十列要求取交，不能逐列自由挑選禁對或原支援。

## 3. 原 triangle markers 的任意大小必要域

整張來源只作一次 D₅／S₄ 搬運，使 q=01012；roots、pieces、附件、
全部十列及完整 Σ 同步搬運。任意大小 M 的原 branches 使用
[單 triangle run 化約](c5_triangle_path_reduction.md)及
[第一分叉排除](c5_triangle_forks.md)。三個原 triangle 頂點都保持 singleton；
正奇長度 uniform run 縮成一點，雙 run 的 X 首點保持、正偶長度 Y 縮成兩點，
原 leaf 保持。對任意 β，同附件 run 的可用色集至少兩色，兩端 relation
由交替染色／至少三色的直接選色，只依正長度奇偶。

固定完整 triangle tuple 後，每份原 branch 可各自選完整 witness，因此縮減
保存三點聯合 relation，投影後保存 K_M。縮減也是 boundary 固定 minor，
各 branch sets 在原路徑內連通、互斥，且與整份原 D 互斥。
雙 triangle 已恰六點，不作長枝替換。

| 核心家族 | 正常形 | triangle 邊 root 標記 |
| --- | ---: | ---: |
| 單 triangle、單 run | 18 | 54 |
| 單 triangle、雙 run | 8 | 24 |
| 無枝 triangle、T4 全收必要支援 | 36 | 108 |
| 雙 triangle、直接 bridge | 64 | 384 |
| 合計 | 126 | 570 |

此域沿用 [既有126域](c5_excess_two_mixed_core_spokes.md#4-雙-spoke-省略的任意大小覆蓋)，
不是344份 bridge-marker 域：U2 的 z,w 在原 triangle 上。
無枝域先列出80份 q-critical 支援，按實際 T4 保留36份，不先篩 disk。
雙 triangle 128份 saved lifts 的十列重算後取64份 q-core；所有正常形均核對
完整 degree 四及逐邊 q-critical witnesses。
每條 triangle 邊用遞增標號作 ordered roots；任意原 root 命名可同步交換，
K 與 F 同時 transpose，式 (2) 不變，89域亦對 transpose 封閉。

## 4. 全部排除與同源收縮星

126核心／570標記對兩候選各五個 D₅ mask，共5,700份完整比較：

| 排除階段 | 查詢數 |
| --- | ---: |
| 目標接受列在 M 已空 | 1,710 |
| 目標拒絕列的完整 K 不可能由89域禁對覆蓋 | 3,927 |
| 進入固定原支援階段 | 63 |

63×32=2,016份支援查詢中，1,917份同 shape 跨列交集為空；剩餘99份
保存完整 shape assignment 與 literal 禁對 schedule。後者全部屬無枝 triangle，
其 S 有四或五點；這是計算結果，不是預先假設 retained C 是 singleton。

對相容的同一 S，僅為拓撲反證，把整份連通原 D 收縮成 d，保留 zd、wd
及全部實際 S 的附件。与§3的 M* branch sets 可同時在同一原 G 操作，得到

\[
J=M^*+zd+wd+\{db:b\in S\}. \tag{3}
\]

disk 來源在外框外側加 apex α 連全 B，迫 J+α 平面。去重後27份 J+α
全部有明示 subdivision：24份 K₃,₃、3份 K₅，共246條原邊路徑；覆蓋全部99份
查詢。新 checker 驗每條路徑、端點、內點互斥及全部模型鄰接。
這個星點不保持 D 的染色、degree 或 Σ，沒有用作式 (1) 的染色替換。
任意大小來源必給一份已排除的同源 minor，矛盾，故 Σ(G−D)=Ω。
結合§1省略身份，U2 的44 core 全排。

## 5. 證書、重播與信任界線

[Primary checker](../scripts/c5_excess_two_adjacent_two_mixed_core44.py)直接讀三份較小
既有 artifacts，不 import 歷史 producer；自行重建126域、MRV全圖回溯與完整
root/contact tuples，5,700份逐列 joint／直接 root-pair 比較一致。
[Primary artifact](../artifacts/c5_excess_two_adjacent_two_mixed_core44/observations.json)
保存完整邊集、原保留 pieces／ownership／contacts／附件／支援、空 fibres、
全圖 witnesses、逐列限制、相容 schedules 與27份 subdivision。

另保存20張實際接上 shared-singleton／shared-edge／distinct-edge／path／triangle D
的原圖；200份完整接回與獨立全圖回溯一致，976份整個 D 的 S₄ transport成立。
這些控制有真實 degree、原內邊、contacts 及 witnesses，不宣稱 disk 或 Σ-critical。
26張實際長 core 的260份**原 triangle 邊保留時**完整三點 joints 與短圖相等；
不把縮圖染色冒充原長圖染色。原 G 拓撲 witnesses 與這些染色控制分開保存。

[獨立支援 artifact](../artifacts/c5_excess_two_adjacent_two_mixed_core44/independent_support_audit.json)
由另一實作重建列、89域、32支援域及S₄交集，核對全部5,700判定與2,016支援查詢，
沒有 import primary 或舊 producer。其範圍限有限支援計算；primary 重播核對圖染色及路徑。

```sh
python3 scripts/c5_excess_two_adjacent_two_mixed_core44.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_adjacent_two_mixed_core44.py --check
python3 scripts/c5_excess_two_adjacent_two_mixed_core44_audit.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_adjacent_two_mixed_core44_audit.py --check
```

兩個 replay 皆只用標準函式庫；primary 生成新 subdivision 才用 NetworkX 3.5。
任意大小覆蓋仍依賴既有 Gallai／degree-list、全四分類、triangle接枝／分叉與
run化約，以及其有限拓撲證書／部分 NetworkX 排除信任。本輪未重稽核全部上游枚舉。
未構造完整Σ933／941來源，未擴大k搜尋，未新增Lean theorem；lake build
通過只驗既有形式化專案。本輪實際驗證見[研究紀錄](history/2026-10-08-u2-two-mixed-core44.md)。

**精確停止點：U2 的44身份完成；完整Σ下44殘留只剩非相鄰U3／U4。**
相鄰m=2其他core型、N1單-root刪除例外、E5新證明要求、三列推廣、ε≥3、
猜想E任意大小、一般出口與K∞=K≤5均未由本輪完成。
