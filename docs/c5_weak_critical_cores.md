# 相鄰雙缺失：最小阻礙與三種 critical-edge 出口

2026-09-16。接續 [候選 A](c5_weak_candidates.md#1-首選候選相鄰雙-singleton-完全釋放)。
**本輪得到一般的紙面充要條件，以及五個既有代表的共同兩阻礙機制；
尚未由 disk 平面性證出候選 A。** 未新增 Lean theorem，未擴到 k=4，未重跑全量 audit。

後續進度：[repair sets、dual flows 與非同面控制](c5_weak_flow_repairs.md)
給出 deletion-side 精確對偶、plane-dual 零邊集表述，並證明若 C5 不要求同面，
relation 相同而共同出口可失敗；一般 disk flow-repair intersection lemma 仍未證。

## 1. 固定圖上的最小阻礙

固定 G 的全部頂點與有序外圈 C5，令 E 為可刪除的非外圈邊。
對 S⊆E，G[S] 保留外圈與 S，包含刪邊後的孤立頂點。
對合法 boundary pattern p，定義

\[
\mathcal C_p=\{A\subseteq E:p\notin\Sigma(G[A]),\quad
  \forall e\in A,\ p\in\Sigma(G[A\setminus\{e\}])\}.
\]

它是 inclusion-minimal 的 p 不可延拓邊集族，不把外圈邊算入可刪集合。
單邊 minimality 等價於所有真子集都可延拓，因為刪邊只放寬 relation。
有限性給出一般公式

\[
p\notin\Sigma(G[S])\iff \exists A\in\mathcal C_p,\ A\subseteq S. \tag{1}
\]

證明：右推左由加邊單調性；左推右在 S 的不可延拓子集中選 inclusion-minimal 者。
空集可延拓所有合法 C5 patterns，所以每個阻礙都非空。
這是固定 G 的完整阻礙族，不是由 relation 本身決定的資料。

以下假設 Σ(G)=Ω\{p,q}，設族 A=𝒞_p、B=𝒞_q。
其餘 patterns 在所有 G[S] 仍可延拓。因此

\[
\Sigma(G[S])=\Sigma(G)\iff
(\exists A\in\mathcal C_p:A\subseteq S)\land
(\exists B\in\mathcal C_q:B\subseteq S). \tag{2}
\]

而任何與 G 同 relation 的 G[S] 都可 silent-reachable：任意順序刪除 E\S，
中間 relation 夾在兩個相等端點之間。

## 2. 三種出口的精確充要條件（紙面證明）

本節不需要平面性、p/q 相鄰或只有三色；只用固定有限圖、刪邊及兩個缺失 patterns。

### 只釋放 p

\[
\Omega\setminus\{q\}\in W(G)
\iff \exists B\in\mathcal C_q:\ p\in\Sigma(G[B])
\iff \exists B\in\mathcal C_q\ \forall A\in\mathcal C_p:\ A\nsubseteq B. \tag{3}
\]

必要性：取該出口圖 S；它保留某個最小 q 阻礙 B⊆S。p 在 S 可延拓，故在 B
亦可延拓。充分性：沿 G 刪到 G[B]；q 全程缺失，其餘原先接受的 patterns
全程接受，而終點接受 p。因此第一次 strict step 恰只釋放 p。
只釋放 q 的條件由交換 p,q 得到。

### 同時釋放 p,q

\[
\Omega\in W(G)\iff
\exists A\in\mathcal C_p,\ B\in\mathcal C_q,\ e\in A\cap B:\quad
p,q\in\Sigma(G[(A\cup B)\setminus\{e\}]). \tag{4}
\]

必要性：令 H→H−e 是同時釋放的 strict step。在 H 中各選最小阻礙 A、B；
若 e 不在其中某個阻礙，H−e 仍拒絕對應 pattern，矛盾。
刪到 (A∪B)−e 仍接受 p,q。充分性：G[A∪B] 仍拒絕兩者，故由 (2)
可 silent 到達；刪 e 便得到 Ω。

等價地，(4) 要求 (A∪B)−e 不包含族 𝒞_p 或 𝒞_q 的**任何**成員。
僅指出所選 A、B 都被 e 擊中不夠：可能有另一個阻礙存活。
兩個可延拓性各自有自己的完整 coloring，整個論證未要求共用 coloring。

這把候選 A 的一般缺口分成三項：兩個族各有一個不包含對方任何阻礙的成員，
以及一對阻礙有滿足 (4) 的共同邊。相鄰 singleton 與 disk 條件應用於證這三項，
不是用來省略它們。

## 3. 唯一阻礙時的完整答案

若 𝒞_p={A}、𝒞_q={B}，則 (1) 在每個子圖上給出兩個精確因子：
拒絕 p iff A⊆S，拒絕 q iff B⊆S。
由 (3)–(4) 立刻得到

| 首次釋放 | 存在的充要條件 | 在 H=G[A∪B] 可刪的邊 |
| --- | --- | --- |
| 只釋放 p | A\B 非空 | 任意 e∈A\B |
| 只釋放 q | B\A 非空 | 任意 e∈B\A |
| 同時釋放 | A∩B 非空 | 任意 e∈A∩B |

因此**唯一阻礙、互不包含、且相交**足以證三出口。這是有明確額外假設的
一般紙面定理，不是所有候選 A 的 disk graphs 已滿足這些假設。

三個抽象控制展示缺少條件的後果：A={x}, B={y} 無共同釋放；
A=B={x} 只有共同釋放；A={x}, B={x,y} 無只釋放 p。
checker 重播這些 monotone support systems；它們未聲稱有 disk graph realization。

## 4. 既有代表的實際結構

只取封存 audit 對五個相鄰缺失位置各保存的一個 representative。
每個代表有 8 個頂點、10 條非外圈邊；對各自全部 1,024 個子集，
以 compatible-coloring intersection 及獨立完整內點賦色加 subset OR 交叉核對 relation。
五個代表全部具有：

- 每個缺失 pattern 恰有一個最小阻礙，各含 9 條非外圈邊。
- 兩阻礙交集有 8 條邊，各有 1 條私有邊，聯集就是代表的全部非外圈邊。
- 唯一 silent 子圖是代表自己；三種出口在代表上直接刪邊即可得到。
- 全 5,120 個子集符合 §3 的兩因子公式；15 個具體出口另以全部 240 個
  有標號 boundary colorings 的回溯檢查核對。

例如缺 p₀,p₁ 的代表（證書 `k3-t382` 的 submask `2045`，Σ 索引 `943`），
令

\[
J=\{25,27,36,37,46,56,57,67\},
\qquad A_0=J\cup\{15\},\quad A_1=J\cup\{05\}.
\]

這裡 uv 表示無向邊 {u,v}；0,…,4 是 boundary，5,6,7 是內點，C5 邊另保留。
A₀ 唯一阻擋 p₀，A₁ 唯一阻擋 p₁。
刪 15 只釋放 p₀，刪 05 只釋放 p₁，刪任一 J 中的邊同時釋放兩者。
**不是由根圖 edge sensitivity 猜公式：全部子集都已核對，排除了替代最小阻礙。**

disk 合法性沿用已保存 plantri rotation，重新驗 SHA 並核對固定 boundary
重標後的 parent；代表及子圖皆為刪邊後代。這不是新的 topology 形式化。
五位置仍屬同一 D5 orbit，未構成域外驗證；本輪也未分析封存域的每個同 Σ 具體圖。

## 5. 驗證與下一個問題

[checker](../scripts/c5_weak_critical_cores.py)；
[逐項證書](../artifacts/c5_weak_critical_cores/observations.json)。
證書保存父圖定位、邊集、完整子集 relation table、最小阻礙、三種刪邊證據與 abstract controls。

```bash
uv run --with networkx==3.5 python scripts/c5_weak_critical_cores.py --check
python scripts/c5_weak_candidates.py --check
python scripts/c5_weak_quotient.py --check
lake build
git diff --check
```

驗證通過：新 checker 逐 byte 重播、candidate／quotient `--check`、
`lake build`（8,820 jobs，僅既有 lint）、135 個本地文件連結及 whitespace 檢查。

下一個窄問題：對候選 A 的任意 disk G，先證或反駁 (3) 的雙向分離：
**是否每側都有一個 minimal obstruction 接受另一個缺失 singleton？**
若不能證，精確障礙就是某一整族的每個阻礙都包含對方阻礙。
若兩側成立，再處理 (4) 的共同 pivotal edge，特別注意替代阻礙。
不必先猜所有高 k 圖都有唯一阻礙；§2 已提供允許多阻礙的精確目標。
本輪停止於此結構化約與代表機制，候選 A 仍未證。
