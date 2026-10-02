# 941 excess-one：原 triangle 接點的 t=3 排除與 ε≥2

**後續（2026-10-02）**：[ε=2 雙 spoke 省略核心分支](c5_excess_two_double_spoke.md)
已以原四接點關係及 888 次接回排除兩候選；
[t=3 spoke＋unary 的原 triangle 位置](c5_excess_two_three_spoke_unary.md)
再沿用本輪 398 個位置，以完整接合及共享省略限制排除。
其餘 ε=2 來源保留，共同下界維持 ε≥2。下文保留本輪結果及驗證。

2026-10-02，基準 `b97b107`，接續工作樹內的
[two-spoke 來源排除](c5_941_two_spoke.md)。目前停止點見
[Kempe 導覽](c5_kempe_guide.md)，實際驗證見
[本輪紀錄](history/2026-10-02-941-three-spoke.md)。

**結論：完整 Σ=941 的 edge-minimal C₅ disk source 不可能有
ε=1、t=3、原分量接點分拆 (2)。** 連同既有 t=1、t=2 排除，得到

\[
\boxed{\Sigma(G)=941\quad\Longrightarrow\quad\varepsilon(G)\ge2.}
\]

適用前提與 [933 下界](c5_excess_one_subcovers.md#61-933ε≥2) 相同：G 為有限
簡單圖，B 是指定有序 induced-C₅ disk 外框，接受全部 T4；每條非框邊
e 都滿足 Σ(G−e)⊋Σ(G)。ε=Σ有效內點(deg_G−4)，孤立內點忽略。
此下界也隨整圖 D₅ 重標搬運；沒有證 ε=2 可實現或排除一般 941 來源。

任意大小涵蓋沿用全 degree-4 分類及尾枝化約。新增證據是紙面接合與
Python 固定域的完整有序關係；沒有新 Lean theorem 或大圖枚舉。

## 1. 省略一條具名 spoke 得到全 degree-4 核心

由[四容量子覆蓋](c5_excess_one_subcovers.md#62-941恰一份共同二接點原分量)，
ε=1 的唯一高 degree 點 r 有 degree=5，其餘有效內點 degree=4。
t=3 時，H−r 恰為同一原分量 C₂，原有序接點為 (x,y)；其餘三份因子
是連向三個不同框點的原 spokes。q₀、q₁ 都有真子核心，且其省略身份
不共用；這些身份只能是 spokes。

選其中一列 q_j 及其省略 spoke e。K=G−e 仍拒絕 q_j、接受 T4，
有效內部仍是同一個連通 H，每個內點的完整 degree 都為四。
任取 minimal q_j-core，其內點的 degree 至少四，故必保留 K 中全部
incident 邊；沿 H 傳播得到整張 K。因此 K 自己就是全 degree-4
minimal q_j-obstruction，原 r 有兩個內部鄰點及兩條保留 spokes。

對**整張圖**共同作 D₅ 框點搬運及 S4 換色，使 q_j 成為 q₄=01012。
完整來源 941 的可能像為 {941,949,950,998,1004}。所有列、附件及接點
使用同一色框，之後不獨立正規化 C₂ 或任何尾枝。

## 2. 原 degree-2 root 的完整位置分類

C₂ 連通，rx、C₂ 內的 x–y 路徑與 yr 給出經 r 的 cycle。
[全 degree-4 合成](c5_k4_blocks.md#4-合成全-degree-4-的單缺失結論)
迫該 cycle 位於原 triangle rxy；xy 是原邊。r 的內部 degree 恰為二，
所以不能是任何 bridge 的端點。只剩：

1. **無枝 triangle。** H 恰為 rxy；每點各有兩個實際 boundary 鄰點。
2. **單 triangle 加一／兩條 path tails。** 接枝位置只可在 x、y，
   全部尾枝仍屬原 C₂；r 不是 tail-root，也沒有獨立 unary 分量。
3. **兩個 triangle 由直接 bridge 相連。** r 是其中一個 triangle
   的非 bridge 端點；原 C₂ 包括 xy、bridge 及另一個完整 triangle。

第二類的無界長度由[路徑枝化約](c5_triangle_path_reduction.md)及
[分叉排除](c5_triangle_forks.md)涵蓋；第三類由
[雙 triangle 分類](c5_two_triangle_blocks.md#1-範圍與結果)排除中間路徑與外掛樹。
這些結構依賴包含外部 degree-list 定理、紙面及既有有限拓撲證據，
本輪沒有重證其大模板全集。

## 3. 保持同一 C₂ 的有序 relation 後接回

固定任一 proper boundary coloring b。第二類的每條尾枝只透過一條
bridge 接到 x 或 y。前輪 [原首點保持](c5_941_two_spoke.md#3-從-bridge-保持提升到原接點保持)
證明，任意長的單 run X^(2m+1),L 或兩-run X,Y^(2m),L，
可以改成原 endpoint 短枝 X,L，保持原首點的全部可取色。
其中 X、Y、L 始終是原實際框鄰點；兩-run 使用封存的八個 contexts。
Endpoint 短枝同時是保留框點的原圖 minor；所得 K* 仍為 disk、全 degree-4，
並由 q₄ 拒絕及飽和傳播保持 criticality，故落在既有 18 份帶枝 bases 中。

固定原 x、y 的色，可分別選尾枝首點異於其 parent 的完整延拓；
各尾枝內點互斥、只共用 B，所以可同時拼接。依次縮尾得到 C₂*，並有

\[
R_{C_2}(b;x,y)=R_{C_2^*}(b;x,y). \tag{1}
\]

原 x、y、xy 及其原 spokes 均未變，沒有以兩個 endpoint marginals
取代 (1)。無枝與雙 triangle 兩類本身有限，不需改寫。

令保留 spokes 的框端點為 s,t，被省略 e 的框端點為 u。
同圖三接點聯合關係為

\[
\mathcal R_K(b;r,x,y)=
\{(a,c,d):(c,d)\in R_{C_2}(b;x,y),\quad
 a\notin\{b_s,b_t,c,d\}\}. \tag{2}
\]

接回原 e 只是加上 a≠b_u，所以 (1)–(2) 同時保持 K 與 G=K+e
的完整三接點 relation、全部十列及完整 Σ。刪除任一具名 spoke，
亦只是省略 (2) 對應的同一不等式；省略身份沒有因縮尾而改名。
原分量 C₂ 的擁有者、邊及全支援都存入證書。

## 4. 無枝 triangle 的必要域與全部接回結果

無枝時，q₄ 下三個 triangle lists 各有至少二色；拒絕迫三者恰為
同一個二色集合 P，且 D=3∈P。因此每點的兩條實際 spokes 必各見到
{0,1,2}∖P 中的一色。三種 P 的支持數為 4³+2³+2³=80。

Checker 直接列出全部 80 份具名接線，完整染色核對十列及每條非框邊的
q₄-critical 見證。其中 44 份不接受 T4，剩 36 份全為 Σ=1022。
**這 36 份沒有再作 disk 篩選**，只是涵蓋全部真實無枝來源的必要放寬域。
不把它們稱作 36 個 disk bases。

帶枝與雙 triangle 採前輪封存 bases，重新核對原邊、degree、完整 Σ、
apex rotation 和逐邊 critical 見證，再改標本輪所需的 degree-2 位置：

| 必要核心族 | bases | 可標記原 r 的位置 | 接回第三條 spoke |
| --- | ---: | ---: | ---: |
| 無枝 triangle，T4 全收必要支援 | 36 | 108 | 324 |
| 一／兩條 tails 的單 triangle | 18 | 34 | 102 |
| 直接 bridge 的雙 triangle | 64 | 256 | 768 |
| 合計 | 118 | 398 | 1,194 |

每個 r 已有兩條具名 spokes，新端點有三種。所有接回圖亦不另篩 disk，
而是直接計算完整 relation。結果：

| 完整 Σ | 接回模型數 | 接受全部 T4 |
| ---: | ---: | --- |
| 774 | 3 | 否 |
| 830 | 33 | 否 |
| 894 | 4 | 否 |
| 942 | 3 | 是 |
| 956 | 3 | 是 |
| 958 | 12 | 是 |
| 960 | 3 | 否 |
| 1012 | 3 | 是 |
| 1016 | 33 | 否 |
| 1018 | 4 | 否 |
| 1020 | 12 | 是 |
| 1022 | 1,081 | 是 |

**沒有任何模型屬於 941 的五個 D₅ 像。** 由 §1–3 的任意大小涵蓋，
排除 t=3、(2)。與 [t=1](c5_941_single_spoke.md)、[t=2](c5_941_two_spoke.md)
及四容量子覆蓋排除的其他 ε=1 型合成，941 的 ε≥2 成立。

放寬域中的 942、956、1012 各拒絕三個連續 singleton 位置；它們來自
無枝必要模型，不是 disk 實現聲明。因此本輪不能沿用前輪
「T4 全收接回圖至多拒絕兩列」的較強觀察。計數含具名重複，不是 class 數。

## 5. 證書、重播與剩餘邊界

[Checker](../scripts/c5_941_three_spoke.py) 與
[artifact](../artifacts/c5_941_three_spoke/observations.json) 保存全部具名 bases、
原附件、C₂ 有序 tuples、(r,x,y) 聯合 tuples 及逐 tuple 完整染色見證。
接回列索引同一 base 的原 tuples；另以完整圖回溯核對 11,940 次十列
查詢及 47,760 次具名因子刪除查詢。分量完整枚舉與全圖回溯獨立接合。
20 份單 run／八份兩-run 的原首點控制亦重播；無界部分仍由紙面 transfer 負責。

```bash
python3 scripts/c5_941_three_spoke.py --check
PYTHONHASHSEED=17 python3 scripts/c5_941_three_spoke.py --check
python3 scripts/c5_941_two_spoke.py --check
python3 scripts/c5_941_single_spoke.py --check
python3 scripts/c5_excess_one_subcovers.py --check
python3 scripts/c5_independent_support_capacity.py --check
uv run --with networkx==3.5 python scripts/c5_triangle_path_reduction.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

大證書由 `artifacts/MANIFEST.json` 的 producer／依賴順序重建；政策及
命令見 [artifact 工具](../tools/artifacts.py)。新增 checker 不用 planarity
oracle，只驗既存帶枝／雙 triangle 的 rotation。
`lake build` 不把紙面分類或 Python 排除提升為 Lean theorem。

933 與 941 現均有 ε≥2；一般來源排除、共同出口及 `K∞=K≤5` 仍未證。
ε=2 要分唯一 degree-6 root 與兩個 degree-5 roots，不能直接延用
ε=1 的省略一因子分類。下一個窄入口見 [Kempe 導覽](c5_kempe_guide.md)。
