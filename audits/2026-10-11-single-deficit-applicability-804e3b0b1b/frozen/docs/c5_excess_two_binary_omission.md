# ε=2：t=3、(2,1) 的原 binary 省略分支排除

**後續（2026-10-02）**：[t=2、(2,2) 原 binary 省略分支](c5_excess_two_two_binary.md)
亦已排除；兩份 binary 省略均全收。下文保留本輪 t=3 的證據與範圍。

**後續（2026-10-03）**：[t=3 全分拆排除](c5_excess_two_three_spoke_complete.md)
復用原短支援、三 spoke 扇區及同源 S₄ profiles，完成整份 (2,1)
來源排除，不需要本頁省略限制；原省略證書及其範圍保持。

2026-10-02，基準 `bbd900a`，接續工作樹的
[三原 unary 排除](c5_excess_two_three_unary.md)。現況及後續入口見
[Kempe 導覽](c5_kempe_guide.md)，本輪重播見
[研究紀錄](history/2026-10-02-excess-two-binary-omission.md)。

**結論：933／941 的固定完整 Σ、edge-minimal C₅ disk 來源，若 ε=2、
唯一 degree-6 root r、t=3，且 H−r 的原接點分拆為 (2,1)，則刪除
整份原 binary C₂ 後必接受全部十列。**

任意大小原分量及全部附件保持；不縮路徑、不生成來源圖。證據是
紙面必要化約加固定集合證書，未新增 Lean theorem。這只排除指定
省略分支，沒有排除整份 (2,1)、其他 ε=2 或一般候選；共同下界仍為 ε≥2。

## 1. 前提與完整四接點接合

G 有限簡單，指定有序 induced-C₅ 外框 B=(b₀,…,b₄) 是 disk 邊界，
完整 Σ 為 933、941 或整圖 D₅ 像；每條非框邊 e 均有 Σ(G−e)⊋Σ(G)。
有效內部 H 連通，r 的完整 degree 為六，其餘內點完整 degree 為四。
r 的三條原 spokes 端點組成 S；H−r 恰有原 binary C₂ 及原 unary V，
原 root 邊為 rx、ry、rv，其中 x、y 是 C₂ 中兩個不同原接點。

固定 proper boundary coloring b，記原完整 relations 為 R_C(b;x,y)
及 S_V(b;v)。[Slack 引理](c5_excess_two_spoke_unary.md#2-原-v-的-relation-非空不需分類其大小或支援)
同樣適用 C₂：刪 root 後任一接點有至少一單位 slack，以該點為根
逆序貪婪染色。因此兩份 relations 在全部十列都非空，且

\[
\mathcal R_G(b;r,x,y,v)=\{(a,c,d,h):(c,d)\in R_C(b),\ h\in S_V(b),
\ a\notin b(S)\cup\{c,d,h\}\}. \tag{1}
\]

每個 tuple 由同一 b、同一原 C₂ 及 V 的完整染色拼接。定義

\[
F_C(b)=\bigcap_{(c,d)\in R_C(b)}\{c,d\},\quad |F_C|\le2;
\qquad F_V(b)=\begin{cases}S_V(b)&|S_V(b)|=1,\\\varnothing&|S_V(b)|>1.\end{cases}
\]

式 (1) 在 root 上的精確投影是 U∖(b(S)∪F_C∪F_V)。以下只用這個
固定接線的 root 查詢；F_C 不是完整二接點 state，不能拿兩個 marginals
代替 R_C。所有 singleton 列共用 D=3，整圖只共同搬運色框及 D₅ 座標。

## 2. 同一省略圖的單缺失與 V 的 D 身份

反設 L=G−C₂ 拒絕一列 q₀。L 保留全部原 V、rv 及三條原 spokes，
有效內部連通且每個內點完整 degree 四。任取 minimal q₀-core，
degree-4 飽和沿內部傳播迫核心等於整張 L；L 繼承 disk 及 T4。
由[全 degree-4 合成](c5_k4_blocks.md#4-合成全-degree-4-的單缺失結論)，

\[
\Sigma(L)=\Omega\setminus\{q_0\}. \tag{2}
\]

所以 q₀ 是原候選拒絕的 singleton 列，三條原 spokes 在 q₀ 下見到
全部三色，且 F_V(q₀)={D}。由同一 V 的
[單接點 D 守恆](c5_excess_one_subcovers.md#4-單接點分量的跨列-d-身份不能互換)，
五個 singleton 列都有 F_V∈{∅,{D}}。若某列 F_V={D}，V 的實際
boundary 支援必見到三個 boundary 色，否則交換兩個未見色破壞 singleton。
特別地，固定原 V 的共同支援 lift 長度至少二。

本輪不分類 L 中 r 的 path 長度或 V 的 blocks；(2)、原 relation 非空
及 D 守恆已提供所需限制。

## 3. 同一嵌入的兩份支援弧與穩定子

三條原 spokes 把 disk 分成三個扇區，其閉框弧 J₀、J₁、J₂ 的長度
為正整數，總和五。C₂、V 各連通且不能跨過 spokes，所以各自全部
實際 boundary 支援位於一個扇區。

只為拓撲論證，保留 C₂ 的一條原 root 邊而刪另一條，再分別收縮
C₂、V；得到共同 root 的兩葉 fan。這個操作不計算或替換 R_C。
[相容 lifts 引理](c5_independent_support_capacity.md#42-同一-root-的相容-lifts)
在固定 spoke 切口下，給兩份支援的包含弧 I_V、I_C：

- 每份弧在其原閉扇區內，端點是原框頂點。
- 若兩份弧同區，開框邊段互斥，可共享端點；原 root 邊次序的兩種可能均保留。
- |I_V|≥2。**對 I_C 不加正跨度假設**，允許長度零。

若 C₂ 無框附件，可用任一可用扇區端點作長度零的空支援包絡；這只放寬
必要條件。若有附件，取共同 lift 的首末實際附件。每個原來源因此被
下節某份具名配置涵蓋，無需假設 C₂ 有兩點支援或為 Gallai tree。

記 q(I) 為包絡弧上所見色集合。這是可見色的上界，不是把整條弧新增為
實際附件。若 F_V={D}，必有 |q(I_V)|=3。對 C₂，逐色固定 q(I_C) 的
每個置換也固定其實際支援色，故保持完整 R_C 及 F_C。令 A=U∖q(I_C)，則

\[
F_C\cap A=\varnothing\quad\text{或}\quad A\subseteq F_C. \tag{3}
\]

因為置換群在未見色 A 上傳遞。這只用 |F_C|≤2，容許空、單色及二色，
沒有假定二禁色飽和或把含 D 一律視為單色 carrier。

## 4. 已知具名省略限制

由[雙 spoke 排除](c5_excess_two_double_spoke.md)及
[t=3 spoke＋unary 排除](c5_excess_two_three_unary.md)，同一候選來源有

\[
\Sigma(G-\{rb_s,rb_t\})=\Omega,\qquad
\Sigma(G-V-rb_s)=\Omega. \tag{4}
\]

因此每列、每條保留 spoke s 及每對保留 spokes s,t 都必滿足

\[
\{b_s\}\cup F_V\cup F_C\ne U,
\qquad \{b_s,b_t\}\cup F_C\ne U. \tag{5}
\]

第一式保留 V 及 C₂，第二式只省略原 V；都是把式 (1) 用於同一原圖的
指定刪邊，未取兩份獨立正規化的來源。省略 C₂ 則用同一式 (2)。

## 5. 固定必要域與逐項證書

[Checker](../scripts/c5_excess_two_binary_omission.py)及
[artifact](../artifacts/c5_excess_two_binary_omission/observations.json)列出
三條 spokes 的十種位置、全部 250 份具名共同包絡配置、兩候選各五個
D₅ 像及可能的 q₀。q₀ 須在目標中拒絕，spokes 及 I_V 均見到三色。

每個 singleton 列獨立放寬選 F_V∈{∅,{D}}、|F_C|≤2，依序檢查
式 (2)、(3)、目標的接受／拒絕及式 (5)。允許跨列任意選集合是必要域
放寬，並不聲稱那些 relations 有同圖實現。真實來源必在其中；某列
無任何選項即可排除該配置。

| 固定必要域 | 933 五像 | 941 五像 |
| --- | ---: | ---: |
| 同一包絡／q₀／目標比較 | 1,160 | 870 |
| 未套式 (5) 前的存活比較 | 280 | 210 |
| 套式 (5) 後存活 | 0 | 0 |
| 只用整個扇區見色的放寬對照，已套式 (5) | 10 | 20 |

最後一列不與包絡配置計數直接相減：它按 (spokes, V 扇區, C₂ 扇區,
q₀, target) 去重。其 30 份全部逐列選項保留，顯示必須使用共同支援
弧的不重疊；僅有扇區標籤不足。2,030 筆包絡比較各存幾何索引、q₀、
第一個無選項的列及前後五列選項數；checker 重新計算，不讀排除 flags。

局部代數控制遍歷全部 65,535 份非空有序二接點 relations，與十五份
非空 unary relations 的 983,025 次完整四接點接合，驗證 root 投影；
另有 960 次直接 tuples／spoke 過濾及 176 次穩定子控制。保留同 marginals
但禁色不同的反例：R₁={(0,1),(1,0)} 的 F={0,1}，
R₂={(0,0),(1,1)} 的 F=∅。控制輸入是抽象局部 relations，不是來源圖。

固定必要域為空，反設不成立，故本輪完整前提下

\[
\boxed{\Sigma(G-C_2)=\Omega.}
\]

## 6. 重播與停止點

```bash
python3 scripts/c5_excess_two_binary_omission.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_binary_omission.py --check
python3 scripts/c5_excess_two_three_unary.py --check
python3 scripts/c5_excess_two_double_spoke.py --check
python3 scripts/c5_single_spoke_root_conservation.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

已完成 t=3、(2,1) 的 binary 省略分支。連同前序結果，這個分拆的所有
容量二省略（雙 spoke、spoke＋V、整份 C₂）均必全收；若仍有候選來源，
它沒有全 degree-4 的 minimal rejected-row core。這沒有排除含 degree-5
或 degree-6 root 的核心，也不證 (2,1) 來源存在。

其餘 t、t=3 的單三接點分量、兩個 degree-5 roots（含 mixed）及一般
出口均保留；未提高 ε≥2，未證 K∞=K≤5。下一窄入口由導覽維護。
全 degree-4 分類及外部 degree-list／拓撲依賴沿用原報告；新 Python
只證固定必要域，`lake build` 不表示新紙面拓撲已 Lean 化。
