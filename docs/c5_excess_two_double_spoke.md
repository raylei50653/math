# ε=2：唯一 degree-6 root 的雙 spoke 省略核心排除

**後續（2026-10-02）**：[t=2 的 spoke＋原 unary 省略分支](c5_excess_two_spoke_unary.md)
已由同源五接點接合及兩 root 色存活排除；共同下界仍為 ε≥2，
其餘 ε=2 來源保留。下文維持雙 spoke 分支的當輪結論與驗證。

2026-10-02，基準 `b97b107`，接續工作樹內的
[941 ε≥2](c5_941_three_spoke.md)及[原四接點關係保持](c5_941_two_spoke.md)。
目前停止點由 [Kempe 導覽](c5_kempe_guide.md)維護；實際重播範圍見
[本輪紀錄](history/2026-10-02-excess-two-double-spoke.md)。

**結論：933／941 的 ε=2、唯一 degree-6 root 來源，不可能藉刪除該
root 的兩條不同原 spokes，得到仍拒絕任何 singleton 列的核心。**
這是條件式來源排除；沒有證所有 ε=2 來源都含這種省略核心，兩候選的
下界仍為 ε≥2。兩個 degree-5 roots、其他省略因子及一般來源尚未涵蓋。

證據為任意大小紙面化約及 Python 固定必要域證書；沿用全 degree-4
分類、外部 degree-list 定理及既有有限拓撲證據。沒有新 Lean theorem。

## 1. 完整前提與省略核心

G 是有限簡單圖，B=(b₀,…,b₄) 是指定有序 induced-C₅ disk 外框，
接受全部 T4，完整 Σ 為 933 或 941（或其整圖 D₅ 像）。每條非框邊 e
滿足 Σ(G−e)⊋Σ(G)。忽略孤立內點後，令 H=G−B，
ε=Σ內點(deg_G−4)=2，且恰有一個高 degree 點 r：deg_G(r)=6，
其餘有效內點 degree=4。沿用[來源結構](c5_independent_support_capacity.md#1-兩種-minimality-與來源的基本結構)，H 連通。

另明設兩條不同原 spokes e₁=rb_a、e₂=rb_b，使

\[
K=G-\{e_1,e_2\}\quad\text{仍拒絕某個 singleton 列 }q.
\tag{1}
\]

K 繼承 disk、T4、同一連通 H，且每個內點完整 degree 恰為四。
任取 K 的 minimal q-core；它的有效內點 degree 至少四，因而須保留
該點在 K 中的全部 incident 邊。沿 H 傳播，得到整張 K；故 K 自己
就是全 degree-4 minimal q-obstruction。

對整張圖共同作一次 D₅ 重標及 S4 換色，把 q 對齊 q₄=01012。
其後所有原接點、附件、分量及省略身份共用同一色框。兩個目標的像為

\[
\begin{aligned}
933&:\{933,934,940,948,996\},\\
941&:\{941,949,950,998,1004\}.
\end{aligned}
\]

## 2. 為何恰落在原 148 個標記核心

令 t 是 r 在 G 中的 spoke 數。T4 全收迫 t≤3：若有四個框鄰點，
可令它們使用四個不同顏色，再把剩餘框點設成某個非鄰點的顏色，得到
無法給 r 著色的 proper T4 列。

由[全 degree-4 分類](c5_k4_blocks.md#4-合成全-degree-4-的單缺失結論)，
K 的內部只能是路徑、單 triangle 加不分叉 path tails，或直接 bridge
相連的兩個互斥 triangles。內部 degree 至多三；spoke 刪除不改內部邊，故

\[
3\le 6-t=\deg_H(r)\le3.
\]

因此 t=3，deg_H(r)=3，K 中 r 恰有一條保留 spoke rb_s。樹核心是
路徑，不能提供此位置；tail 的中間點亦只有內部 degree 二。所以 r
必為原 triangle rxy 上接出 bridge ru 的點，xy 是原邊。H−r 恰有
同一 binary 原分量 C₂（原接點 x,y）及 unary 原分量 U（原接點 u）。

這正是 [two-spoke 報告 §2–3](c5_941_two_spoke.md#2-保留-r-的原核心分類)
已涵蓋的標記位置；本輪不額外假設 C₂ 是一條邊、U 是一個點，亦不
刪去它們的附枝或實際支援。單 triangle 的任意長 tails 用該報告的
原首點 transfer 縮減；雙 triangle 本身已有限。

| 全 degree-4 必要核心 | bases | 原 degree-3 root 位置 | 雙 spoke 接回 |
| --- | ---: | ---: | ---: |
| 單 triangle 加一／兩條 tails | 18 | 20 | 120 |
| 直接 bridge 雙 triangle | 64 | 128 | 768 |
| 合計 | 82 | 148 | 888 |

每個 r 已有一條 spoke，其餘四個框點中選兩個，共六種具名接回。
計數包含具名重複，不是新 class 數。

## 3. 雙接回保持同一完整有序關係

固定任一 proper boundary coloring c。前輪原首點化約保留

\[
\mathcal R_K(c;r,x,y,u)=\mathcal R_{K^*}(c;r,x,y,u),
\tag{2}
\]

以及 C₂ 的完整有序 (x,y) relation、U 的原 u relation。全部原 spokes、
xy、三條 root–contact 邊及原端點的實際 boundary 附件保留；縮尾只
在同一原分量內存在量化其他點。不能分別正規化 C₂、U，或以兩個
endpoint marginals 替代 C₂ 的關係。

兩條 spokes 接回只加兩個不等式：

\[
\mathcal R_G(c;r,x,y,u)
=\{z\in\mathcal R_K(c):z_r\ne c_a,\ z_r\ne c_b\}
=\mathcal R_{K^*+e_1+e_2}(c;r,x,y,u).
\tag{3}
\]

式 (2) 對全部 proper c 成立，故式 (3) 保持全部十列及完整 Σ；兩個
接回次序都在同一份原 tuple 上取交集。任意大小涵蓋由這個紙面論證
及既有分類負責，沒有把固定內點數的搜尋外推成一般結論。

## 4. 必要域的結果及較強的有限觀察

接回後不另篩 disk，直接檢查全部 888 張完整圖。456 張不接受全部
T4；剩下 432 張的完整 Σ 恰為：

| Σ | 拒絕 singleton 位置 | 模型數 |
| ---: | --- | ---: |
| 958 | {0,4} | 76 |
| 1020 | {3,4} | 76 |
| 1022 | {4} | 280 |

因此必要放寬域中沒有 933 或 941 的任何 D₅ 像，甚至 T4 全收時
只會有一個拒絕，或兩個相鄰 singleton 拒絕。由 §1–3，排除 (1)
指定的任意大小來源。沒有把這 432 個放寬模型宣稱為 disk 實現。

對候選來源，可將結果寫成必要條件：對 r 的任意兩條不同原 spokes，

\[
\boxed{\Sigma(G-\{e_1,e_2\})=\Omega.}
\tag{4}
\]

因為刪邊後仍接受 T4，若沒有接受全部 Ω，就會提供 (1) 的 singleton
拒絕核心，矛盾。式 (4) 是帶唯一 degree-6／ε=2 等全部前提的結論，
不適用於兩個 degree-5 roots，亦不表示省略其他容量二因子都接受 Ω。

## 5. 證書、重播與信任界線

[Checker](../scripts/c5_excess_two_double_spoke.py) 與
[artifact](../artifacts/c5_excess_two_double_spoke/observations.json)保存原 bases、
原圖邊、apex rotations、逐非框邊 q₄-critical witnesses、分量 ownership、
實際 boundary 附件、原四接點 tuples 及逐 tuple 的完整染色見證。
接回 relation 以原 tuple 索引保存；省略別的 spoke pair 時，relation
可能超出原 K 的 tuples，因此另存完整 tuples 與 witnesses。

新 checker 重新核對 82 個 bases 的 degree／rotation／criticality，
由原邊重建恰好 148 個標記位置，並用分量的完整染色與獨立全圖回溯
核對原關係及接回。每一接回圖的十列皆保存兩個中間次序、五個具名
因子的省略身份及三種原 spoke pair 的省略關係。查詢數為：

- 8,880 次雙接回完整列查詢；17,760 次單接回中間列查詢。
- 44,400 次原因子省略查詢；26,640 次原 spoke pair 省略查詢。

```bash
python3 scripts/c5_excess_two_double_spoke.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_double_spoke.py --check
python3 scripts/c5_941_two_spoke.py --check
python3 scripts/c5_941_three_spoke.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
uv run --with-requirements requirements.txt python tools/artifacts.py status
git diff --check
```

大證書依 `artifacts/MANIFEST.json` 登錄，由 [artifact 工具](../tools/artifacts.py)
按 producer 依賴重建；新 producer 明列前輪 four-port artifact 為輸入，
並核對它的全部 source hashes。本輪沒有新 planarity oracle；任意大小
的分類、外部 degree-list 定理及 tail transfer 沿用原證據。
`lake build` 不會把這些紙面與 Python 結論提升為 Lean theorem。

本輪停止於雙 spoke 省略條件分支；一般 933／941 來源、ε=2 實現、
共同出口及 `K∞=K≤5` 均未證。目前下一個窄問題見 [Kempe 導覽](c5_kempe_guide.md)。
