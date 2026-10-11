# ε=2：t=2 的 spoke＋原 unary 省略核心排除

**後續（2026-10-02）**：[三原 unary 共同扇區排除](c5_excess_two_three_unary.md)
已關閉 t=3 path／tail 分支，連同 triangle 位置完成 t=3 spoke＋unary
省略分支。下文保留當輪證據及停止點。

**後續（2026-10-02）**：[t=3 的原 triangle 位置](c5_excess_two_three_spoke_unary.md)
已由完整四接點接合、同一 binary 省略圖至多拒絕一列及既有雙 spoke
省略結論排除；t=3 的 path／tail 位置仍保留。下文維持當輪 t=2 結論。

2026-10-02，基準 `b97b107`，接續工作樹的
[雙 spoke 省略核心排除](c5_excess_two_double_spoke.md)及
[原四接點保持](c5_941_two_spoke.md)。目前停止點見
[Kempe 導覽](c5_kempe_guide.md)，實際驗證見
[本輪紀錄](history/2026-10-02-excess-two-spoke-unary.md)。

**結論：933／941 的 ε=2、唯一 degree-6 root、t=2 來源，不可能省略
一條原 spoke 及一份原 unary 分量後，仍拒絕任何 singleton 列。**
這完成前輪指定的條件分支；沒有證所有 ε=2 來源都有這種核心。
共同下界仍為 ε≥2，t=3 的同種省略、其他容量二省略及兩個 degree-5
roots 均未涵蓋。

證據是任意大小紙面接合與 Python 固定核心證書。全 degree-4 分類及
原首點 tail transfer 沿用既有紙面、外部 degree-list 及有限拓撲證據；
本輪沒有新增 Lean theorem、unary 圖枚舉或 disk oracle。

## 1. 前提與同一原核心

G 為有限簡單圖，B=(b₀,…,b₄) 是指定有序 induced-C₅ disk 外框；
接受全部 T4，完整 Σ 為 933、941 或其整圖 D₅ 像；每條非框邊 e 都有
Σ(G−e)⊋Σ(G)。忽略孤立內點，H=G−B 連通，ε=Σ內點(deg_G−4)=2，
唯一高 degree 點 r 的完整 degree 為六，其餘內點完整 degree 為四。
本輪另明設：

- r 恰有兩條不同原 spokes rb_s、e=rb_t。
- V 是 H−r 的一份**原**連通分量，恰有一個 r 接點 v；rv 是其唯一 root 邊。
- K 是從 G 省略整份 V、其全部 incident 邊及 e 後的圖，且 K 拒絕某個
  singleton 列 q。V 的所有 boundary 附件都屬原 V，沒有挪給其他分量。

K 繼承 T4 與 disk，剩餘有效內部連通，每個內點完整 degree 恰為四。
任取 minimal q-core，degree-4 飽和沿內部傳播使它等於整張 K。
r 在 K 的內部 degree=3，故全 degree-4 分類迫 r 位於原 triangle rxy，
另有原 bridge ru。K−r 的原內部分量恰為 binary C₂（接點 x,y）及
unary U（接點 u）；原 G−r 的分量便是同一 C₂、U、V。

對整張圖共同作一次 D₅ 與 S4 搬運，使 q=q₄=01012。兩候選的像為

\[
933:\{933,934,940,948,996\},\qquad
941:\{941,949,950,998,1004\}.
\]

K 正好落在 [two-spoke 報告 §2–3](c5_941_two_spoke.md#2-保留-r-的原核心分類)
的任意大小涵蓋：單 triangle 的 18 個 endpoint bases，或直接 bridge
雙 triangle 的 64 個 bases，合計 148 個原 degree-3 root 位置。
原首點化約保持 C₂、U 的完整 relation 及
\(\mathcal R_K(b;r,x,y,u)\)，對每個 proper boundary coloring b 都成立。
它只作用於 K 內的原 tails，**V、v、rv 及 V 的全部實際附件保持原樣**。
各分量共用同一 B、色框及原 ownership。

## 2. 原 V 的 relation 非空，不需分類其大小或支援

固定任一 proper b，令

\[
S_V(b)=\{d:\text{原 V 有延拓 b 的完整染色，且 }v=d\}.
\]

這是原圖的完整一接點 relation，不是任選的禁止色。對 z∈V，刪去
boundary 已用色後的 list L_b(z) 滿足

\[
|L_b(z)|\ge\deg_V(z)\quad(z\ne v),\qquad
|L_b(v)|\ge\deg_V(v)+1.
\tag{1}
\]

因為每點在 G 中完整 degree=4，且唯一額外的 root 邊為 rv。
取 V 的一棵以 v 為根的 spanning tree，按距 v 由遠到近貪婪染色。
每個非根點尚有一個未染的 parent；最後 v 有一單位 slack。因此

\[
\boxed{S_V(b)\ne\varnothing\quad\text{對全部 proper }b.} \tag{2}
\]

式 (1) 使用原逐點附件，容許其 boundary 色重複；不需要 Gallai、
V 的 path／block 正常形，或任何大小上界。接回 rv 後，V 禁止的 root
色恰為 \(\{d\}\)（若 \(S_V(b)=\{d\}\)），否則為空；容量至多一。

## 3. 五接點的精確接合與兩色存活引理

令 \(\mathcal T(b)\) 是接回 e 後的原四接點 relation：

\[
\mathcal T(b)=\{z\in\mathcal R_K(b;r,x,y,u):z_r\ne b_t\}.
\]

原來源完整五接點 relation **恰為**

\[
\mathcal R_G(b;r,x,y,u,v)
=\{(z,d):z\in\mathcal T(b),\ d\in S_V(b),\ z_r\ne d\}. \tag{3}
\]

固定同一 b，右邊每個 tuple 都有 K+e 的完整染色及原 V 的完整染色，
兩者只共用 B，另檢查 rv 即可拼回原 G。反向由限制染色直接成立。
原首點化約保持整份 \(\mathcal T\)，故也保持式 (3)，沒有獨立換色、
抹去 xy，或把 C₂ 的兩個端點 marginals 當成完整二接點 relation。

令 \(A(b)=\{z_r:z\in\mathcal T(b)\}\)。由 (2)–(3)：

\[
\boxed{|A(b)|\ge2\ \Longrightarrow\ G\text{ 接受 }b.} \tag{4}
\]

證明：選原 V 的任一完整染色，記 v 色為 d。A 有至少兩色，故有
一個 a≠d；取 \(z_r=a\) 的**完整四接點 tuple 與染色**，再接上該份
V 染色。這是對每份原 V 的一致證明，不為不同列虛構不同 V。

有限 checker 存的是五接點**接合算子**
\(\mathcal J(b)=\{(z,d):z\in\mathcal T(b),d\in\{0,1,2,3\},z_r\ne d\}\)。
它對最後一欄限制到原 \(S_V(b)\) 才成為式 (3)。原 V 未給定，因此
證書不宣稱已枚舉 V 的完整染色；每個算子 tuple 的核心染色有保存，
V 的染色由 (2) 提供。放寬 d 為自由變數只用於核對算子，沒有把 V
替換成一個 degree-one source vertex，亦不聲稱任選十列 unary relations
有同圖實現。

## 4. 固定核心全表與排除見證

148 個原 marked cores 各有四個可能的另一條 spoke，共 592 次接回；
其中 148 個中間圖已不接受 T4，另 444 個接受 T4。
對每個中間圖及其全部十列，重算完整 \(\mathcal T\)、\(\mathcal J\)，
並核對所有十五份非空 unary relation 的接合。

對每一個候選完整 mask M，只可能有兩種排除理由：

1. M 要接受的某列已被 K+e 拒絕；接上原 V 不能恢復接受。
2. M 要拒絕的某列在 K+e 有至少兩個 root 色；由 (4) 必接受。
   證書對四種可能的 v 色各保存一個五接點 tuple 及核心染色索引。

| 目標 orbit | 比較數 | 已拒絕目標接受列 | 兩 root 色迫目標拒絕列接受 | 剩餘 |
| --- | ---: | ---: | ---: | ---: |
| 933 的五像 | 2,960 | 1,264 | 1,696 | 0 |
| 941 的五像 | 2,960 | 1,788 | 1,172 | 0 |

第二類見證列全部是 singleton 列。兩候選在整個必要域都被排除，
故不需要額外限制原 V 的實際支援或 cyclic placement；真實來源仍須
保有那些資料，但無論其合法值為何都滿足 (2)–(4)。沒有新增六跨度主張。

另令 \(L=T4\cup\{b:|A(b)|\ge2\}\)，\(P=\Sigma(K+e)\)。
任何接受 T4 的真實接回圖都滿足 \(L\subseteq\Sigma(G)\subseteq P\)。
這個必要區間的全表是：

| P | L | 具名模型數 |
| ---: | ---: | ---: |
| 958 | 942 | 4 |
| 958 | 958 | 36 |
| 1020 | 1012 | 4 |
| 1020 | 1020 | 36 |
| 1022 | 942 | 2 |
| 1022 | 958 | 176 |
| 1022 | 1012 | 2 |
| 1022 | 1020 | 176 |
| 1022 | 1022 | 8 |

全部區間的 mask 聯集是 `{942,958,1006,1012,1014,1020,1022}`，
沒有任一目標像。這些是必要放寬值，不是完整 Σ 的實現分類；各列選擇
仍可能不屬於任何同一原 V。放寬值含三拒絕 mask，不能宣稱至多兩拒絕。

由 §1–3 的任意大小涵蓋與全表，原假設矛盾。等價地，在本輪全部
候選／唯一 degree-6／t=2 前提下，對任一原 unary V 和任一原 spoke e，

\[
\boxed{\Sigma\bigl(G-V-e\bigr)=\Omega.} \tag{5}
\]

刪除後若未全收，繼承 T4 使其拒絕列必為 singleton，便回到已排除的
條件分支。式 (5) 不包含 t=3、binary 省略或兩個 degree-5 roots。

## 5. 重播與剩餘邊界

[Checker](../scripts/c5_excess_two_spoke_unary.py) 與
[artifact](../artifacts/c5_excess_two_spoke_unary/observations.json) 保留原 bases、
原邊、boundary 附件、分量 ownership、原 tuples、逐 tuple 完整核心
染色、spoke／V 省略身份、五接點算子及逐候選排除見證。
全部 82 bases 的 degree／rotation／q₄-criticality 與 148 個標記位置
重新核對，不讀舊接受 flags 作判定。

新增計算核對 1,480 次原核心列關係、5,920 次 spoke 接回列關係、
5,920 次五接點算子與獨立完整回溯，以及 88,800 次非空 unary relation
接合。核心 witnesses 是完整染色；算子控制的額外 v 只標記 endpoint
色，不能冒充未給定原 V 的內部染色。

```bash
python3 scripts/c5_excess_two_spoke_unary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_spoke_unary.py --check
python3 scripts/c5_941_two_spoke.py --check
python3 scripts/c5_excess_two_double_spoke.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
uv run --with-requirements requirements.txt python tools/artifacts.py status
git diff --check
```

大證書依 `artifacts/MANIFEST.json` 的 producer 依賴重建；政策見
[artifact 工具](../tools/artifacts.py)。新 producer 明列原 four-port artifact
為輸入並核對它的全部直接 source hashes；任意大小分類與 tail transfer
沿用原證據。既有 `lake build` 不把新紙面／Python 論證形式化。

本輪停止於 t=2 的 spoke＋unary 省略分支；沒有提高 ε≥2 下界，沒有
排除一般來源、證明共同出口或 `K∞=K≤5`。下一個窄入口見
[Kempe 導覽](c5_kempe_guide.md)。
