# 唯一 mixed P₃：中點／端點接線的原末端附件與六跨度排除

後續（2026-10-04）：[共鄰端點的雙扇區引理](c5_mixed_p3_common_endpoint.md)
已保留原鏈及 (3,2,1) 附件，給任意 unary 大小的短子弧與部分來源排除。
共鄰端點仍留 36 具名必要 residual；本頁不同接點接線的完成結論不變。

2026-09-30，Git 基準 `d72b6cb`，接續工作樹中既有的
[兩端接線完成](c5_mixed_p3_asymmetric.md)及
[mixed 容量](c5_mixed_capacity_contacts.md)。
**唯一 mixed 原分量為 P₃=x₀x₁x₂，z 只接中點 x₁、w 只接端點 x₂ 時，
全部 source residual 都不存在 induced-C5 disk 來源。**
整份 root 交換、路徑反向及兩者合成都包含在內。

未接 root 的 x₀ 及三條實際 boundary 附件始終保留。它們迫使原四環
外側的一個連通區塊見到三種已用色；完整側支援與原環序再迫至少六條
框邊。兩種 residual 分別用跨度相加及兩段原框弧計費，一色側可零跨度。
不限制 unary 大小、bridges 或旁支，不需 T4、Gallai／degree-list 外部
定理；零 target 查詢，未新增 Lean theorem。

[Checker](../scripts/c5_mixed_p3_middle_endpoint.py)及
[證書](../artifacts/c5_mixed_p3_middle_endpoint/observations.json)保留實際附件、
完整 triples、有序 root 色對與整份側角色。驗證範圍見
[研究紀錄](history/2026-09-30-mixed-p3-middle-endpoint.md)，目前停止點見
[weak-deletion 導覽](c5_weak_deletion_guide.md)。

## 1. 原圖前提與完整 root 介面

M 有限簡單，B=(b0,…,b4) 是 induced C5 disk 外框，H=M−B 非空連通。
q=01012、U={0,1,2,3}；M 拒絕 q，刪任一非框邊後接受 q。
相鄰 roots z,w 完整 degree=5，其餘內點完整 degree=4。
H−{z,w} 的唯一 mixed 原分量恰為 C*=x₀x₁x₂，contacts 恰為
P*ᶻ={x₁}、P*ʷ={x₂}，即 root masks=(0,1,2)。其餘原分量均 unary。

記 S_i=N_B(x_i)，由完整 degree 得

\[
(|S_0|,|S_1|,|S_2|)=(3,1,2),\qquad L_i=U\setminus q(S_i).
\tag{1}
\]

這些是原具名框點的集合，未把同 q 色框點識別。令 \(\mathcal T\)
為三個原點的完整合法 triples，定義

\[
F^*=\{(a,b):\nexists t\in\mathcal T,\ t_1\ne a,\ t_2\ne b\}.
\]

各原 unary D 的禁色仍為 f_D(q)，且

\[
E_r=U\setminus\left(q(N_B(r))\cup\bigcup_{D\sim r}f_D(q)\right),\qquad
Z_M(q)=(E_z\times E_w)\setminus(\Delta\cup F^*).
\tag{2}
\]

同一份完整 tuple 必須同時滿足兩個 root 限制；不改成端點 marginals。
容量與 minimality 沿用[前層 §2–5](c5_mixed_capacity_contacts.md)：
1≤|E_r|≤2，刪 zw 釋放可用對角，刪 mixed 邊釋放非對角。
因此 E_z×E_w 至少有一個非對角，原圖拒絕又迫使 F* 非空。

## 2. 完整 P₃ 關係只禁一對，residual 恰剩兩型

固定任一 (a,b)∈F*。P₃ 的剩餘 lists 為

\[
M_0=L_0,\qquad M_1=L_1\setminus\{a\},\qquad
M_2=L_2\setminus\{b\}.
\]

它們的大小分別至少 1、2、1。若任何一點有 slack，可從另一端貪心
完成；否則拒絕恰須兩端各被迫不同色 s,t，中點 list 恰為 {s,t}。
因 L₀ 含未用色 3，所以 M₀={3}。於是 M₂={d}，d≠3；L₂ 含 3，
故 b=3、L₂={d,3}。S₁ 單點，設其 q 色為 c，則
L₁=U∖{c}={a,d,3}，從而

\[
\boxed{\{a,c,d\}=\{0,1,2\},\quad
L_0=\{3\},\quad L_1=\{a,d,3\},\quad L_2=\{d,3\}.}
\tag{3}
\]

特別是 q(S₀)={a,c,d}、q(S₁)={c}、q(S₂)={a,c}。
直接保留三個座標，得到精確關係

\[
\mathcal T=\{(3,a,d),(3,a,3),(3,d,3)\},\qquad F^*=\{(a,3)\}.
\tag{4}
\]

這是原圖的完整關係等式，不是三個 list 的必要上界。配合 (2)、可用
對角及非空非對角，source residual 只剩

| 型 | E_z | E_w |
| --- | --- | --- |
| I | {a} | {a,3} |
| II | {a,3} | {3} |

兩側都是 pair 會產生至少兩個非對角，F* 的唯一禁對無法覆蓋。
兩側都是 singleton 則不能同時具有可用對角與非對角。
表中兩型在固定 masks=(0,1,2) 下都要處理；不能以交換 residual 而
保留接點不變的方式把它們當成同一型。

## 3. 原四環空內側與保留末端的四個外側區塊

每個原 unary D 都有 0<|f_D(q)|≤k_D≤3。非空由逐邊 minimality 得到，
上界來自原 root 的 zw 與 mixed incidence 已佔兩條 degree。
若 D 無 boundary 附件，f_D 對全 S₄ 不變，只能為 ∅ 或 U，矛盾。
故每份原 unary 都碰 B，並保有從其每個 root contact 經原 D 到 B 的
路徑；路徑內部避開其他原分量。

取原 simple cycle J=z–x₁–x₂–w–z。它沒有 chord。x₀ 與 J 不交，且
有三條直達 B 的原邊，所以 x₀ 在 J 外側；各 unary 同理在外側。
所有直達 B 的邊亦在外側，因此 J 的開內側空，J 是原嵌入的一個面。
另外 z–x₁–B、w–x₂–B 的原外部路徑也保留。

定義完整 root 側支援

\[
A_r=N_B(r)\cup\bigcup_{D\sim r}\{b_i:N(b_i)\cap D\ne\varnothing\}.
\tag{5}
\]

J 外側 annulus 的四個具名連通區塊依序為

\[
\mathcal U_z,\quad (x_1\text{ collar}+x_0\text{ 及全部原附件}),\quad
x_2,\quad\mathcal U_w,
\tag{6}
\]

或整體反向。它們的實際外支援分別為

\[
A_z,\quad S_{01}=S_0\cup S_1,\quad S_2,\quad A_w.
\tag{7}
\]

第二塊包括原 x₀x₁ 邊、x₀ 的三條附件與 x₁ 的一條附件。這個支援
聯集只用來讀取原嵌入次序，不刪 x₀、不收縮為 K2，也不將 (4) 換成
一個用 S₀₁ 重新定義的 list。其內部附件次序可有進一步限制；下文
在較弱的四塊必要條件上已得矛盾，不需假設所有四塊配置可實現。

四塊可取兩兩不交的連通細鄰域，各碰內、外圓周。兩外端的原
crosscut 把不含內圓周的一側切開；另一塊若有外端位於其開支援弧，
就無法接回自己的內端。這給同序、互不交錯的外支援，與
[前層 annulus 證明](c5_mixed_p3_symmetric.md#3-兩份完整側支援與五份同序區塊)
相同。框點處只分開入射端，仍保留同一 b_i。

所以存在沿同一方向的整數 lifts

\[
T_z,T_{01},T_2,T_w,\qquad
\max T_z\le\min T_{01}\le\max T_{01}\le\min T_2
\le\max T_2\le\min T_w\le\max T_w\le\min T_z+5.
\tag{8}
\]

模五正是 (7)，容許共享框端點、零跨度及間隙。q(S₀₁) 已見三色，
q(S₂) 見 a,c，故這兩塊跨度分別至少 2、1。

## 4. 兩型各迫六框邊

E_r 是原整側圖的精確 root 可取色集。任何逐色固定 q(A_r) 的置換，
同時作用於全部原 unary 的完整染色，必保持 E_r。與前層相同，得到

\[
E_r=\{a\}\Longrightarrow a\in q(A_r),\quad
E_r=\{a,3\}\Longrightarrow\{c,d\}\subseteq q(A_r),\quad
E_r=\{3\}\Longrightarrow q(A_r)=\{a,c,d\}.
\tag{9}
\]

證明只需交換一個未見色與 3：若未見色跨過 E_r 與其補集，便違反
不變性。這保留全部原分量、同一 boundary row 及共同色框。

**型 II。** A_z 至少見 c,d，A_w 至少見三色。沿 (8) 的四份跨度依序
至少 1、2、1、2，總和至少六，與外框只有五邊矛盾。

**型 I。** 取 T_z 中 q 色為 a 的 lift h，令 u=min T₂、v=max T₂。
原 S₂ 恰有兩個框點，顏色為 a,c。從 h 到 u 的原框弧完整包含 S₀₁，
故見三色；從 v 到 h+5 的弧完整包含 A_w，故見 c,d，再回到色 a。
依 u 的顏色分兩種：

| q(u) | h→u 的必要長度 | u→h+5 的必要長度 | 總長度 |
| --- | ---: | ---: | ---: |
| a | ≥3：由 a 回 a，途中見 c,d | ≥3：u 的 a、v 的 c、A_w 的 d、最後 a | ≥6 |
| c | ≥2：由 a 到 c，途中見 d | ≥4：u 的 c、v 的 a、A_w 的 c,d、最後 a | ≥6 |

第二列的 c,d 可依任一順序出現，都是 v 之後、h+5 之前的兩個不同
框點。兩段恰分割同一份原框的 h→h+5，不重用開框邊，所以兩列都
與長度五矛盾。A_z 可以只有一點、跨度零；本證明不需把它算成正跨度。

兩型全部作 **disk 來源排除**。交換整份 z/w 側圖會轉置完整 F*；
反向命名原 P₃ 會反轉 triple 座標。因而四個具名 masks
(0,1,2)、(0,2,1)、(2,1,0)、(1,2,0) 全部涵蓋。
結合[兩端接線](c5_mixed_p3_asymmetric.md)，唯一 mixed 原 P₃ 的
**兩個不同接點、各一 root incidence** 已全部排除。

## 5. 固定域證書及重播

Checker 只用標準函式庫，重用既有完整介面與 pinned 回溯；不讀舊
artifact 的接受／排除 flags，不生成新的圖目錄或重跑 no-mixed 枚舉。

- 窮盡 10×5×10=500 組實際 (S₀,S₁,S₂)，保存完整 triple、contact、F*
  masks。112 組有非空禁對，色角色恰為 (a,c,d) 的六種排列。
- 每份有兩型 residual，共 224 案例。型 I／II 每份各有 85／115 組
  完整逐邊 minimality 側角色接合，合計 22,400 組必要接合。
- 全部 500 組及 112×3 份 root／path 變換，共 13,376 次獨立 pinned
  queries；另核對每份變換的完整 triples、禁對與全部側角色交換。
  框反射 ρ=(3,2,1,0,4) 連同共同色置換 π=(0 1) 亦逐份核對。
- 共同 lifts／gaps 與由實際子集生成 cyclic hull 的兩種方法，得到
  相同 570 份四區塊必要幾何。原 x₀／x₁ 附件仍分別保存；幾何層只
  取其聯集，不要求兩份附件在該塊內的精細次序。
- 44 案例／4,400 組側角色無原四環次序支援；另 180 案例／18,000 組
  側角色在 1,032 份相容幾何中均有完整側支援的不變性反證。
  零保留、零 target；這些不是來源圖的數量。
- 288 份支援／residual 不變性檢查，直接核對 (9)。三色字串控制獨立
  得兩弧下界 (3,3) 或 (2,4)。另留長度六、A_z 零跨度的必要支援
  正控制，含原 P₃ 三份附件及完整 triples；不宣稱 degree／minimality 實現。

```bash
python3 scripts/c5_mixed_p3_middle_endpoint.py --check
PYTHONHASHSEED=17 python3 scripts/c5_mixed_p3_middle_endpoint.py --check
python3 scripts/c5_mixed_capacity_contacts.py --check
python3 scripts/c5_mixed_p3_asymmetric.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

無 `--check` 只生成本層證書；`--check` 重算逐 byte 比較。本 checker、
capacity 與 base interface 的 Python SHA 均綁在證書中。有限控制使用
共享的前層函式，獨立性只指明列的 pinned 回溯及第二份 hull 生成器。
Jordan／任意 unary 大小屬紙面證明，未新增外部定理或 Lean theorem；
`lake build` 不形式化本頁結論。

## 6. 停止點與保留缺口

本輪完成中點／端點接線的全部 residual 排除，並接回單側出口的
失敗核心限制。只增加來源限制，沒有新增空的可處理出口類別。
接手方向由[weak-deletion 導覽](c5_weak_deletion_guide.md#3-精確停止點與下一個窄問題)
維護；下一窄題可取兩 roots 同接一個端點的 masks=(0,0,3) 及反向型，
保留原末端鏈和 (3,2,1) 份 boundary 附件，不能直接換成 shared singleton。

共鄰接點型、較多 root incidences、triangle、更大／多 mixed 的幾何及
跨列、逐染色 repair、完整 Σ、一般／共同出口與 `K∞=K≤5` 仍未由本輪證成。
