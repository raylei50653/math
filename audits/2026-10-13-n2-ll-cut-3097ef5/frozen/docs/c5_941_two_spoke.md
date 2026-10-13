# 941 excess-one：保留原接點的 spoke 接回與 t=2 排除

**後續（2026-10-02）**：[Three-spoke 排除](c5_941_three_spoke.md)已完成
最後的 t=3、(2)，941 下界提高至 ε≥2。下文保留本輪結果及停止點。

2026-10-02，基準 `b97b107`。接續 [single-spoke 排除](c5_941_single_spoke.md)
及[四容量子覆蓋](c5_excess_one_subcovers.md#62-941恰一份共同二接點原分量)。
目前停止點由 [Kempe 導覽](c5_kempe_guide.md)維護。

**結論：固定完整 Σ=941 的 edge-minimal C₅ disk source，不可能有
ε=1、t=2、原分量接點分拆 (2,1)。** 連同前輪 t=1 排除，ε=1 只剩
t=3、(2)。941 的 ε≥2 與一般來源排除仍未證。

任意大小化約沿用全 degree-4 結構與路徑枝分類；新增原 branch-root
關係保持及固定域 Python 接回證書。保留原 root r、binary 接點 (x,y)、
unary 接點 u、具名 boundary 附件及省略身份。沒有新 Lean theorem，
沒有重開大圖枚舉，亦未把有限模型全當成 disk 實現。

## 1. 至少一列必省略原 spoke

沿用前報的全部來源前提：G 是有限簡單 induced-C₅ disk 圖，指定有序
外框 B；完整 Σ=941、接受全部 T4；刪任一非框邊都改變完整 Σ。
有效內部 H 連通，ε=Σ內點(deg−4)=1，唯一 degree-5 root 為 r，其餘
有效內點完整 degree=4。t=2 時因子為兩條不同原 spokes rb_s、rb_t，
同一 binary 原分量 C₂ 及一份 unary 原分量 U，原接點分別為 (x,y)、u。

三個拒絕 singleton 列是 q₀=01212、q₁=01202、q₃=01021；q₂、q₄
及全部 T4 接受。q₀、q₁ 各有全 degree-4 真子核心，省略身份不共用。
可省略身份只有兩條 spokes 與 U。因此不論兩列都省略 spoke，或一列
省略 U，**至少一個 j∈{0,1} 及一條原 spoke e 滿足 K=G−e 拒絕 q_j**。

K 接受 T4，有效內部仍為同一 H；所有內點完整 degree=4。degree-4
飽和沿 H 傳播，故 K 自己就是 minimal q_j-obstruction。此時原 r 有
三個內部鄰居 x,y,u 及一條保留 spoke。

只在此處對**整張圖**共同作 D₅ 框點搬運與 S4 換色，把被省略列 q_j
對齊 q₄=01012。之後所有列、接點及附件共用此一具名色框。
941 的可能像為 `{941,949,950,998,1004}`；不各自正規化分量。

## 2. 保留 r 的原核心分類

C₂ 連通，故 rx、C₂ 內的 x–y 路徑、yr 構成經 r 的 cycle。
[全 degree-4 分類](c5_k4_blocks.md#4-合成全-degree-4-的單缺失結論)
迫它為原 triangle rxy；特別地，xy 是原邊。ru 是 triangle 外的 bridge。

K 只有下列兩類：

1. **一個 triangle 加路徑枝。** r 上必有 U 枝；至多再有一枝，接在
   x 或 y。接枝至多兩處且不同點由 [triangle 接枝](c5_triangle_branches.md)
   保證，枝為路徑由[第一分叉排除](c5_triangle_forks.md)保證。
   若 C₂≠xy，額外枝仍屬原 C₂，不能另算成一份 root 因子。
2. **兩個互斥 triangles 以直接 bridge 相連。**
   [雙 triangle 分類](c5_two_triangle_blocks.md#1-範圍與結果)排除中間路徑
   及外掛樹。r 是 bridge 一端，C₂ 恰為 xy，U 為第二個原 triangle。
   此類本身已是六內點有限形，無需改寫。

所有數量與全域涵蓋性沿用原分類的紙面／外部 degree-list／有限拓撲
證據。下節只在第一類的原 path tails 內作有明確介面的縮減。

## 3. 從 bridge 保持提升到原接點保持

既有[路徑枝化約 §2–5](c5_triangle_path_reduction.md#5-保持-bridge-介面的有限縮減)
把每條任意長枝限制為下列兩種，保留其原首點及原末端 leaf 附件：

- 單 run：`X^(2m+1), L`，m≥0；
- 兩個 runs：`X, Y^(2m), L`，m≥1，只能出現在八個單枝 contexts。

X、Y 是每個非葉點的兩個**實際** boundary 鄰點，L 是末端三個實際
鄰點。端點短枝為 `X,L`；它來自原圖的 endpoint minor，框點未識別。

本題要接回原 spoke，並保留 (r,x,y,u)，故不能只用縮圖的完整 Σ 相等。
以下證明縮減更保持每份尾枝**原首點的全部可取色**，對每個 proper
boundary coloring b 同時成立。

### 3.1 單 run 的原首點色集合

令 S=四色\b(X)、T=四色\b(L)。S 至少二色，T 非空。
若 |S|=2，奇數個 S 點的交替使原首點色與最後一個 S 點色相同，故
原首點可取色恰為 `{a∈S : T−{a}≠∅}`，等於短枝 `X,L`。

若 |S|≥3，X 的兩個框點必同色。封存的 18 個 disk endpoint bases、
20 個具名 tail slots 全滿足

\[
\boxed{X\text{ 的兩點相鄰，或 }X\subseteq L.} \tag{1}
\]

第一種不可能在 proper b 下同色；第二種使 b(L) 至多兩色，故 |T|≥2。
從 leaf 向首點遞迴，每個 S 點的可取色都是整個 S；長枝、短枝的原
首點色集合相同。式 (1) 在 checker 中逐具名原附件重新核對。

### 3.2 兩個 runs 的原首點色集合

固定原 X 首點色及 L 葉點色，Y^(2m) 可縮成 Y,Y：若 Y-list 大小為二，
只依偶數長度；若至少三色，任何兩個外部端點色都可跨越至少兩個
Y 點。這是所有 m≥1 的 transfer 論證。

剩下八個具名 `X,Y,Y,L` contexts。本輪對每個 context 的全部 240 個
字面 proper boundary rows，以 path DP 和獨立完整染色枚舉核對：

\[
\operatorname{Colors}_{\mathrm{first}}(X,Y,Y,L;b)
=\operatorname{Colors}_{\mathrm{first}}(X,L;b). \tag{2}
\]

這加強了前報只使用的 bridge-mask equality。保存十個 canonical rows
的各個 root-color 染色見證；其餘 rows 亦實際重播，沒有只比色集合大小。
有限八項等式與 §3.1 的紙面式，共同支持任意長原首點色保持。

### 3.3 同圖接合與接回原 spoke

每條枝只經原首點／一條 bridge 接到原 triangle，枝之間只共用 B。
固定同一 b 及原首點色，可取各枝的完整延拓。因此依次縮枝保持

\[
\mathcal R_K(b;r,x,y,u)=\mathcal R_{K^*}(b;r,x,y,u), \tag{3}
\]

其中是有序四點**聯合**關係；r,x,y,u 都是原頂點。對 C₂，額外枝若在
x 或 y，原 xy 邊與兩個有序座標始終保留，因而完整 R_C₂(b;x,y) 也保持；
U 的原首點 relation 由 (1)–(2) 保持。其餘原頂點僅在這份已證明的
局部關係內被存在量化；沒有以兩個 endpoint marginals 取代 C₂。

原 e=rb_t 的合法性就是 (3) 的 r 色不等於 b_t。故

\[
\mathcal R_G(b;r,x,y,u)
=\{z\in\mathcal R_K(b):z_r\ne b_t\}
=\mathcal R_{K^*+e}(b;r,x,y,u). \tag{4}
\]

式 (4) 對全部十列及共同 S4 色名成立，所以保存完整 Σ。亦可刪任一
具名單容量因子後再接合，保留各省略身份；不靠單一成功染色推論完整性。
被保留的 endpoint 附件、框環次序和來源 base ID 均存入證書。

## 4. 全部具名接回模型的完整結果

只使用原封存模板，沒有新增圖大小上界搜尋：

| 原全 degree-4 核心 | q₄-critical bases | 可標記為 r 的位置 | 接回一條原 spoke |
| --- | ---: | ---: | ---: |
| 單 triangle／一或兩枝 | 18 | 20 | 80 |
| 直接 bridge 雙 triangle | 64 | 128 | 512 |
| 合計 | 82 | 148 | 592 |

每個 marked r 原本恰一條 spoke，故新 spoke 的框端點有四種可能。
雙 triangle 舊 artifact 共有 128 個 disk templates；只有 64 個拒絕
指定 q₄，另 64 個不是本題核心，沒有混入。每個 base 的原邊、degree、
apex rotation、完整十列及逐非框邊 q₄-critical 見證均重新核對。

對 592 個接回圖全部計算完整十列；暫不額外過濾接回後的 disk 性質，
所以是一個含所有真實來源的放寬域。其 Σ 分布為：

| Σ | 模型數 | 接受全部 T4 |
| ---: | ---: | --- |
| 830 | 72 | 否 |
| 894 | 2 | 否 |
| 958 | 40 | 是 |
| 1016 | 72 | 否 |
| 1018 | 2 | 否 |
| 1020 | 40 | 是 |
| 1022 | 364 | 是 |

T4 全收的 444 個模型只可能拒絕 `{q₄}`、`{q₄,q₀}` 或 `{q₄,q₃}`，
後兩者是相鄰 singleton 位置。**沒有任何模型屬於 941 的五個 D₅ 像，
甚至不必先過濾接回後的 disk 條件。** 由 §1–3 的任意大小涵蓋與完整
關係保持，排除原 t=2 來源。模型數含具名重複，不是新 class 數或實現分類。

## 5. 證書、重播與信任界線

[Checker](../scripts/c5_941_two_spoke.py) 與
[artifact](../artifacts/c5_941_two_spoke/observations.json) 保存：

- 20 份單 run 接線條件、19,200 次完整 rows／奇數長度控制；無界部分由
  §3.1 證明。八個兩-run 原首點等式共 1,920 次獨立染色核對。
- 82 個 base 的全部原邊、rotation、q₄ 刪邊見證及來源索引。
- 148 個 marked cores 的 C₂／U 原分量身份、contacts、實際支援、完整
  ordered relations、(r,x,y,u) 聯合 tuples 及逐 tuple 完整染色見證。
- 592 次接回的 5,920 次十列查詢；每個接回 relation 以原聯合 tuple
  索引完整保存，該 tuple 的原染色見證仍有效，不以 root masks 取代。
- 23,680 次具名四因子刪除查詢，獨立回溯核對各列省略身份；包含先前
  「兩列都省略 spoke／一列省略 unary」兩種必要情形。

```bash
python3 scripts/c5_941_two_spoke.py --check
PYTHONHASHSEED=17 python3 scripts/c5_941_two_spoke.py --check
python3 scripts/c5_excess_one_subcovers.py --check
python3 scripts/c5_941_single_spoke.py --check
uv run --with networkx==3.5 python scripts/c5_triangle_path_reduction.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

若大證書尚未落地，依 `artifacts/MANIFEST.json` 的 producers／依賴順序
重建；大檔政策與命令見 [artifact 工具](../tools/artifacts.py)。
實際驗證與未重驗範圍見[本輪紀錄](history/2026-10-02-941-two-spoke.md)。

原 18／64 bases 的涵蓋性仍依賴既有全 degree-4 分類、Gallai／degree-list
外部定理、原 template topology 及分叉排除；本輪未重跑其大模板全集。
新計算無 planarity oracle；只驗既有 bases 的 rotation。接回圖的 disk
實現與排除性質不互換；必要域整體沒有 941 已足夠。沒有新增 Lean
theorem，`lake build` 不形式化上述原首點 transfer 或任意大小化約。

本輪停止於 **941 ε=1 的 t=2 來源排除**。剩餘 t=3、(2) 有三條原
spokes，唯一 C₂ 的兩接點仍需保留；省略 spoke 後 r 只有兩個內部鄰居，
不在本輪 148 個 degree-three 標記位置內。933 下界維持 ε≥2、941
維持 ε≥1；一般候選來源、共同出口、H1 全部及 K∞=K≤5 仍未證。
