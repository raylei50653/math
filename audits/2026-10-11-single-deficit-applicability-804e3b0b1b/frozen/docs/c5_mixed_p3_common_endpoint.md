# 唯一 mixed 共鄰 P₃：雙扇區局部化、部分來源排除與具名殘留

**獨立驗收（2026-10-04，D₅）**：[最終成果固定快照與稽核](../audits/2026-10-04-task-d5/REPORT.md)
只新增關閉(CPP-134-1,34,60)、side IDs=(27,1)；九份自身支援配置、
27份完整relation組合、contacts次序／原bridges及逐份2↔3 lift雙射均核對。
未知w完整relation保持符號纖維；不以整側禁色聯集代替逐分量檢查。
連同C₂／C₃合用恰三keys，3500key ledger及原36／140／900表不刪，
其餘3497keys未關閉。以下各輪正文／artifacts保持，現行入口由weak-deletion導覽維護。

**獨立驗收（2026-10-04，D₄）**：[正式返回工作區稽核](../audits/2026-10-04-task-d4/REPORT.md)
接續D₃，完整3500key ledger只登記C₂ (CPP-134-1,30,20)
與C₃ (CPP-134-1,34,20)已關閉；原36／140／900表與unknown fibres
保持，未完成整份case。下一具名入口geometry34／join60。

後續（2026-10-04，C₂）：[一色支援三接點 unary](c5_mixed_p3_one_color_ternary_unary.md)
已關閉本文指定的 CPP-134-1／geometry 30／side_join_id 20：原 degree／
單一自身支援迫原 triangle，保留 z–x₂–b₄ 外路得到 K₅ subdivision。
本文 36／140／900 必要表及 rotation 證書維持原輪資料，未刪 profile；
只排除這份原身份，未完成整個 case／geometry 的所有側接合。
後續（2026-10-04，C₃）：[雙框點三接點 unary](c5_mixed_p3_two_frame_ternary_unary.md)
亦已排除同一 case 的 geometry 34／side_join_id 20，原非接點雙框點葉
以外路 K₅ 排除後，重證葉數限制。原表不刪；目前窄入口見導覽。

2026-10-04，Git 基準 `0e38127`。接續
[weak-deletion §3](c5_weak_deletion_guide.md#3-精確停止點與下一個窄問題)、
[mixed 容量](c5_mixed_capacity_contacts.md)與
[middle-endpoint 報告](c5_mixed_p3_middle_endpoint.md)。
**原共鄰 P₃ 的全部 root 側支援可局部化到長度至多三的原框子弧；
x₁ 被迫取唯一框色 2 的兩種色角色全部來源排除。共鄰線尚未全部完成。**

引理容許任意大小 unary、原 bridges 與旁支。原 x₂–x₁–x₀ 鏈、
各點 (3,2,1) 條實際 boundary 附件及同一共鄰點完整保留。
固定控制保留 36 個具名 local／residual 案例、140 份必要側支援幾何；
它們均有幾何 rotation 正控制，未證 source degree／逐邊 minimality 實現。
零 target 查詢；不需 T4／Gallai，未新增 Lean theorem。

[Checker](../scripts/c5_mixed_p3_common_endpoint.py)、
[觀察證書](../artifacts/c5_mixed_p3_common_endpoint/observations.json)與
[rotation 控制](../artifacts/c5_mixed_p3_common_endpoint/rotation_controls.json)
保存完整 triples、具名附件、兩側角色及同一框弧。
實際驗證見[本輪紀錄](history/2026-10-04-mixed-p3-common-endpoint.md)。

## 1. 原 source 前提與完整三點關係

M 有限簡單，B=(b₀,…,b₄) 是 induced C5 disk 外框；H=M−B 非空連通。
q=01012、U={0,1,2,3}；M 拒絕 q，刪任一非框邊後接受 q。
相鄰 roots z,w 完整 degree=5，其餘內點完整 degree=4。
H−{z,w} 的唯一 mixed 原分量恰為 C*=x₀x₁x₂，
P*ᶻ=P*ʷ={x₂}，即 masks=(0,0,3)；其餘原分量都是 unary。
路徑反向型 (3,0,0) 由整份座標反轉涵蓋。

記 Sᵢ=N_B(xᵢ)、Lᵢ=U∖q(Sᵢ)。完整 degree 給

\[
(|S_0|,|S_1|,|S_2|)=(3,2,1),\qquad
\mathcal T=\{t\in L_0\times L_1\times L_2:t_0\ne t_1,\ t_1\ne t_2\}.
\tag{1}
\]

共鄰點只有一個變數：

\[
F^*=\{(u,v):\nexists t\in\mathcal T, t_2\ne u, t_2\ne v\}.
\tag{2}
\]

各原 unary D 的完整禁色仍為 f_D(q)。沿用本線原 source 定義

\[
E_r=U\setminus\left(q(N_B(r))\cup\bigcup_{D\sim r}f_D(q)\right),\qquad
Z_M(q)=(E_z\times E_w)\setminus(\Delta\cup F^*).
\tag{3}
\]

容量、逐邊 minimality 給 1≤|E_r|≤2；刪 zw 釋放可用對角，
刪 mixed 邊釋放非對角。因此 F* 非空。
此處沒有加入 target 拒絕、933／941、完整 Σ 或其他研究線的前提。

固定 (u,v)∈F*，剩餘 lists 為 L₀、L₁、L₂∖{u,v}，大小至少 1、2、1。
三點路徑拒絕恰需兩端強制不同色，中點 list 等於這兩色。
第一端含未用色 3，故必為 {3}；中點必為 {d,3}，d≠3。
令 c 為 S₂ 的 q 色，則 c≠d，另令 a 為第三個已用色。得到六份精確色角色

\[
\boxed{\{a,c,d\}=\{0,1,2\},\quad
q(S_0)=\{a,c,d\},\ q(S_1)=\{a,c\},\ q(S_2)=\{c\},}
\tag{4}
\]
\[
L_0=\{3\},\ L_1=\{d,3\},\ L_2=U\setminus\{c\},\qquad
\mathcal T=\{(3,d,a),(3,d,3)\},\quad F^*=\{(a,3),(3,a)\}.
\tag{5}
\]

這是原 P₃ 的完整三座標等式。後續支援聯集僅用於幾何，未重新定義
任何 list，亦未把原 P₃ 換成 shared singleton。

設 T={a,3}。由 (3)、可用對角與非空非對角，residual 恰有五型：

| branch | E_z | E_w |
| ---: | --- | --- |
| 0 | T | T |
| 1 | {a} | T |
| 2 | {3} | T |
| 3 | T | {a} |
| 4 | T | {3} |

每份色角色有 125 組完整必要側角色接合，各型 25 組。
這些仍帶逐份 unary 接點數／禁色、spoke 色及 root 身份。

## 2. 完整 root 側支援與原 triangle 空內側

定義原整側實際支援

\[
A_r=N_B(r)\cup\bigcup_{D\sim r}\{b_i:N(b_i)\cap D\ne\varnothing\}.
\tag{6}
\]

每份原 unary 有 0<|f_D(q)|≤k_D≤3。非空由逐邊 minimality，
上界由原 root 的 zw 與 mixed incidence 已佔兩條 degree。
若 D 沒有 boundary 附件，其禁色對 S₄ 全不變，只能是 ∅ 或 U，矛盾。
故每份 unary 都碰 B，保留從各原接點經同一原 D 到其實際附件的路徑。

原 simple triangle K=z–x₂–w–z 無 chord。x₀、x₁ 相連且各有直達 B
的原邊，所以都在 K 外側；各 unary 同理。所有直達 B 的邊亦在外側。
其餘內點全屬上述分量，因此 K 的開內側空，K 是原嵌入的一個面。

E_r 是「r 加全部原 unary 及 spokes」的精確 root 可取色集。
任何逐色固定 q(A_r) 的置換，同時作用於所有原染色，必保持 E_r。
交換未見色與 3 給

\[
E_r=T\Rightarrow\{c,d\}\subseteq q(A_r),\quad
E_r=\{a\}\Rightarrow a\in q(A_r),\quad
E_r=\{3\}\Rightarrow q(A_r)=\{a,c,d\}.
\tag{7}
\]

不變性使用同一原側圖的完整染色，不限制 unary 大小。
也不表示只用 (7) 就能實現其所有逐份禁色。

## 3. 任意 unary 大小的雙扇區與 tether 引理

**雙扇區引理。** 存在 S₀ 兩個 cyclic consecutive 點間的原閉框弧
I=[p,q]，長度至多三，使 S₁、S₂、A_z、A_w 全在 I。
設 x₁ 的兩個附件在 I 線序中為 u<v；則 S₂、A_z、A_w 更全在

\[
J\in\{[p,u],[u,v],[v,q]\},\qquad |J|\le3.
\tag{8}
\]

**證明。** x₀ 的三條原 spokes 是 embedded 三-star，將 disk 切成
三個區，其 boundary 部分恰為 S₀ consecutive 點間的三段框弧。
H−x₀ 連通：原 x₁x₂、root triangle 與全部 unary 都仍連在一起。
它不碰 x₀ 或該三-star 的邊內部，故全落在一區；各實際附件的框端
只能落在該區的閉弧 I。S₀ 有三個不同框點，所以 |I|≤5−2=3。

在此區中保留原 x₀x₁ 及 x₁ 的兩條 spokes，得到一個 rooted Y。
它把該區再切成三區，原 B 交集依序為 [p,u]、[u,v]、[v,q]。
H−{x₀,x₁} 仍連通，含 x₂、z,w 及全部 unary，所以同落在一個 Y 區；
全部 S₂、A_z、A_w 位於同一 J。整個論證只用原連通性與 Jordan 分離。
框端點重合時在小鄰域分開入射 darts，仍保留同一具名 bᵢ。
零長 J 合法，不把共享端點收費成兩條框邊。

**Triangle tether 次序引理。** 記 s 為 S₂ 的唯一原框點。
原路徑 x₁–x₂–s 是選中 Y 區內的 crosscut。原 zw 邊避開此路徑，
故 z,w 在同一側；各完整 root 側圖連通且避開這條路徑的內點，
所以 A_z、A_w 全在 J 中 s 的同一側。
空內側 triangle 的 root collars 給同序不交錯的兩側支援。因此
沿 J 的線序只能是

\[
(S_2,A_z,A_w),\ (S_2,A_w,A_z),\
(A_z,A_w,S_2),\ (A_w,A_z,S_2).
\tag{9}
\]

精確而言，各份支援在同一線性 lift 上滿足前塊 max≤後塊 min。
可以共享框端點，但不能重用開框邊。不能強迫 A_z,S₂,A_w 次序：
原 x₁x₂ tether 在 x₂ 外側 collar 上佔有自己的位置。
以上切割始終保留原 x₂–x₁–x₀ 鏈及全部附件。

## 4. 唯一框色的位置給紙面來源排除

q 中色 2 只在 b₄ 出現。依六色角色中 2 的位置分三支；證明均容許
任意 unary 大小，不查有限支援表。

### 4.1 d=2：兩份色角色全部來源排除

至少一側 E=T，依 (7) 其支援須見 c,d，故 b₄∈J。
d=2 又屬 S₀，必是 I 的端點，因此也是 J 的外端。
J 是靠該端點的 outer Y 區；另一個 S₁ 附件仍位於 I 中但不在 J
的開弧內，故 |J|≤2。

從 d 端讀 J，它須見 c。proper q 與 d 唯一，只留下
d–c、d–c–a、d–a–c，含反向；d–c–d 不可能。

- d–c：沒有 a 或三色支援；兩側都 pair 又需兩份正跨度，超過一邊。
- d–c–a：s 是中點 c，(9) 迫兩 sides 同在 s 的一側。pair 必在 d–c
  側，另一側的 singleton a／3 不可能；兩 pair 又超過該側一邊。
- d–a–c：pair 支援含 J 兩端、佔滿兩邊。另一 pair 或 singleton 3
  必重用開框邊；singleton a 的原框點則落在 pair 的開支援弧內，
  違反 (9)。

所以 (a,c,d)=(0,1,2)、(1,0,2) 的全部五型 residual 都無 disk 來源。
這是來源排除，沒有 target 接受。

### 4.2 c=2：只保留 used-singleton／pair

b₄ 同時屬 S₀、S₁、S₂。含 s 的非零 J 只能是 S₁ 兩附件間的 middle
Y 區，兩端色為 a,c；|J|≤3。pair 側須見 d，proper 字串因此只可能

\[
a-d-c\quad\text{或}\quad a-d-a-c
\tag{10}
\]

及反向。兩字串中 d、c 各僅一個原位置；每份 pair 支援均含它們，
故兩 pair 必重用開框邊。singleton 3 也須含 d,c，同樣矛盾。
只剩 branch 1／3，即 {a}/T 或 T/{a}。

另一側的 singleton a 支援不能落在 pair 的開弧內，故必含 (10)
的首端 a，且全部位於首端 a 到 d 的第一條原框邊：可以只取 a，
也可以取 a,d，跨度可為零或一；共享 d 框端點合法。
這個限制尚未證逐份 unary 可實現，也尚未排除該兩型。

### 4.3 a=2：具名保留

共鄰點的已用可取色為 2 時，固定控制仍保留全部五種 residual 中的
部分實際附件。雙扇區與 (9) 成立，但尚未導出完整來源排除或指定出口。

## 5. 固定控制、完整殘留清單與重播

Checker 只用標準函式庫，重用前層的完整介面與 pinned 回溯。
直接讀取 capacity 證書中的六份色配置，重新推導 (4)–(5)；
不用舊接受／排除 flags 判定新結論。

- 全部 10×10×5=500 份實際 (S₀,S₁,S₂)，112 份 F* 非空。
  三點完整 triples、lists 與具名框點分別保存。
- 六色角色；560 local／residual 案例、14,000 必要側角色接合。
  加上 336 份 root／path 變換，共 13,376 次獨立 pinned queries。
  路徑反向型 (3,0,0)、整份 root 交換及框反射連同共同色置換均核對。
- 114,048 份完整側支援／residual 候選經 (7)–(9) 後，524 個案例
  無必要幾何；36 案例／18 份 local 附件留下 140 份側支援。
  每份 retained case 的 25 組側角色仍全部保留，共 900 組。
  未用整側支援代替每份 unary 的自身支援或接受它的可實現性。
- 六色角色的 local／retained-case／retained-geometry 數依序為
  (0,1,2):32/0/0，(0,2,1):8/6/24，(1,0,2):32/0/0，
  (1,2,0):8/6/24，(2,0,1):16/12/46，(2,1,0):16/12/46。
- 140 份必要 skeleton 各有一份獨立 rotation 正控制。原 B、P₃、
  所有 Sᵢ 與 root triangle 邊保留；只在幾何層將各 root 加其全部
  unary 收縮為 root，保留 A_r 的每個具名框端。
  Checker 重算每個 dart／face，檢查 rotation 單圈、連通、Euler=2、
  C5 外面與原 triangle 面；不需執行 NetworkX。
  Rotation 資料由 NetworkX 3.5 探索生成，作為保存的正控制輸入，
  未作負判定 oracle。全部控制覆蓋恰為自行推導的 140 份 retained 幾何。

以下 `014/14/1` 表示 S₀={b₀,b₁,b₄}、S₁={b₁,b₄}、S₂={b₁}。
branch 由 §1 表定義；括號是該具名案例的必要側支援數。
觀察證書逐份保存 Az、Aw、I、J、共同 lifts 及精確側角色 IDs。

| local ID | S₀/S₁/S₂ | a,c,d | 全部 retained case 名稱（幾何數） |
| ---: | --- | --- | --- |
| 131 | 014/14/1 | 2,1,0 | CPP-131-0 (4), CPP-131-1 (11), CPP-131-2 (1), CPP-131-3 (11), CPP-131-4 (1) |
| 133 | 014/14/3 | 2,1,0 | CPP-133-0 (2) |
| 134 | 014/14/4 | 1,2,0 | CPP-134-1 (6), CPP-134-3 (6) |
| 142 | 014/24/2 | 2,0,1 | CPP-142-1 (3), CPP-142-3 (3) |
| 144 | 014/24/4 | 0,2,1 | CPP-144-1 (3), CPP-144-3 (3) |
| 146 | 014/34/1 | 2,1,0 | CPP-146-0 (2) |
| 148 | 014/34/3 | 2,1,0 | CPP-148-0 (2) |
| 381 | 124/14/1 | 2,1,0 | CPP-381-1 (3), CPP-381-3 (3) |
| 384 | 124/14/4 | 1,2,0 | CPP-384-1 (3), CPP-384-3 (3) |
| 392 | 124/24/2 | 2,0,1 | CPP-392-1 (3), CPP-392-3 (3) |
| 394 | 124/24/4 | 0,2,1 | CPP-394-1 (3), CPP-394-3 (3) |
| 465 | 234/04/0 | 2,0,1 | CPP-465-0 (2) |
| 467 | 234/04/2 | 2,0,1 | CPP-467-0 (2) |
| 481 | 234/14/1 | 2,1,0 | CPP-481-1 (3), CPP-481-3 (3) |
| 484 | 234/14/4 | 1,2,0 | CPP-484-1 (3), CPP-484-3 (3) |
| 490 | 234/24/0 | 2,0,1 | CPP-490-0 (2) |
| 492 | 234/24/2 | 2,0,1 | CPP-492-0 (4), CPP-492-1 (11), CPP-492-2 (1), CPP-492-3 (11), CPP-492-4 (1) |
| 494 | 234/24/4 | 0,2,1 | CPP-494-1 (6), CPP-494-3 (6) |

兩個最小幾何正控制都取 local 131，完整 triples={(3,0,2),(3,0,3)}：

| case | Az | Aw | E_z/E_w | V/E/F |
| --- | --- | --- | --- | --- |
| CPP-131-1 | {b₄} | {b₁,b₂} | {2}/{2,3} | 10/19/11 |
| CPP-131-0 | {b₁,b₂} | {b₂,b₃} | {2,3}/{2,3} | 10/20/12 |

兩控制保留原 P₃ 的全部六條 boundary 附件及原 triangle，但 root
degree 未達原 source 的 (5,5)，亦無原 unary 實現／逐邊刪除見證。
其 residual 是待實現的原側角色，並非收縮後 skeleton 的染色介面。
它們只證明「必要幾何已無餘量可直接全排除」不能由前層資料推出。

```bash
python3 scripts/c5_mixed_p3_common_endpoint.py --check
PYTHONHASHSEED=17 python3 scripts/c5_mixed_p3_common_endpoint.py --check
python3 scripts/c5_mixed_capacity_contacts.py --check
python3 scripts/c5_mixed_p3_middle_endpoint.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

無 `--check` 生成 observations；rotation_controls 是獨立保存的正控制輸入，
不會被覆寫。`--check` 重算後逐 byte 比較 observations，內含 checker、
capacity、base SHA 及 rotation 輸入 SHA。兩個 JSON 各小於 1 MB。
Jordan／任意 unary 大小仍屬紙面證明，`lake build` 不形式化本頁結論。

## 6. 停止點與下一個具名入口

最小交付已完成：雙扇區／tether 幾何引理、d=2 的來源排除、c=2 的
residual 限制，配完整三點／實際附件／rotation 固定控制。
**整個共鄰端點 P₃ 仍保留 36 個具名必要案例，尚無指定 target 出口。**
本輪 524 個幾何失敗案例不算 524 個來源圖，140 個幾何也不算 140 個
實現來源；更不能把 retained 的 900 組角色當作存在證書。

下一窄入口取 **CPP-134-1／geometry 30／side_join_id 20**：
S₀=014、S₁=14、S₂=4，(a,c,d)=(1,2,0)，E_z={1}、E_w={1,3}；
完整 triples={(3,0,1),(3,0,3)}。
Az={b₁}、Aw={b₂,b₄}，J=b₁b₂b₃b₄，字串為 1–0–1–2。
側角色 IDs 為 (8,1)：z 側無 spoke、原 unary 接點數 (3)，禁色
f_z={0,2,3}（mask 13）；w 側無 spoke、原 unary 接點數 (3)，禁色
f_w={0,2}（mask 5）。前者飽和，後者缺額一；都保存原三接點身份。

應在這個同一原圖／同一色框上加入**各原 unary 的自身支援、具名
接點與原 tight block／bridge**，先研究 z 側這份飽和三接點 unary：
其自身支援只能見 b₁ 的色 1，原外路 z–x₂–b₄ 與原 B 同時保留。
判定它是否能滿足 source degree／minimality，或從該外路導出矛盾。
若此窄支關閉，再處理 singleton 側可用首條框邊兩端的其餘具名型。
保留 w 側、原 P₃ 與全部附件；未假設 saturated unary 一定是某個固定小圖。

目前入口以[weak-deletion §3](c5_weak_deletion_guide.md#3-精確停止點與下一個窄問題)
為準。其他 P₃ 接線、triangle、更大／多 mixed、跨列 repair、完整 Σ、
一般／共同出口及 `K∞=K≤5` 仍保留；未重啟 no-mixed 十五類枚舉。
