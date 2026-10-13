# 相鄰雙缺失：repair sets、dual flows 與非同面控制

2026-09-16。接續 [minimal obstruction 化約](c5_weak_critical_cores.md)。
**候選 A 仍未完全證明。** 本輪把三出口改寫成最小刪邊 repair sets 的精確充要條件，
再把 disk 圖中的 repair sets 等價寫成平面 dual 上固定 boundary demand 的最小零邊集。
另給出一張 relation 完全相同的平面圖，證明只要 C5 不能作同一個 disk face，
共同出口就真的會失敗；因此剩餘缺口已定位為 dual 5-pole 的拓撲／flow 交集命題。

未新增 Lean theorem，未跑 k=4 disk search，也未重播全量 deletion audit。

## 1. 最小 repair sets

固定有序 C5 圖 G，E 是可刪除的非外圈邊。對缺失 boundary pattern r 定義

\[
\mathcal R_r=\{D\subseteq E:r\in\Sigma(G-D),\quad
  \forall D'\subsetneq D,\ r\notin\Sigma(G-D')\}.
\]

有限性與刪邊單調性立即給出

\[
r\in\Sigma(G-D)\iff \exists R\in\mathcal R_r:\ R\subseteq D. \tag{1}
\]

以下假設 Σ(G)=Ω\{p,q}。其他八個 patterns 在所有刪邊後代仍可延拓，
所以 silent 恰表示尚未包含 𝓡_p 或 𝓡_q 的任何成員。

### 1.1 單側出口

\[
\Omega\setminus\{q\}\in W(G)
\iff
\exists P\in\mathcal R_p\ \forall Q\in\mathcal R_q:\ Q\nsubseteq P. \tag{2}
\]

右推左：按任意順序刪 P；P 的每個真子集不釋放 p，而 q 在 P 已未釋放，
故所有前綴 silent，最後一步只釋放 p。左推右：從出口使用的全部刪邊 D 中
選一個 minimal p-repair P⊆D；q 在 D 仍缺失，故沒有 q-repair 包含於 P。
交換 p,q 得另一個單側出口。

### 1.2 共同出口

\[
\Omega\in W(G)
\iff
\begin{aligned}
\exists P\in\mathcal R_p, Q\in\mathcal R_q, e\in P\cap Q:\quad
&\text{不存在 }R\in\mathcal R_p\cup\mathcal R_q\text{ 使}\
&R\subseteq(P\cup Q)\setminus\{e\}.
\end{aligned}\tag{3}
\]

右推左：先刪 `(P∪Q)\{e}`，由條件全程 silent，再刪 e，P、Q 同時完成。
左推右：令 S→S∪{e} 是共同釋放的最後一步；在 S∪{e} 中各取一個 minimal
repair P、Q。若 e 不在其中之一，該 repair 已包含於 silent 狀態 S，矛盾；
而 S 本身不能包含任何 repair。把 S 縮到 `(P∪Q)\{e}` 即得右式。

這是 [上一報告](c5_weak_critical_cores.md) retained-obstruction 條件的 deletion-side 對偶，
但更直接顯示所需的三種機制：p 專屬 repair、q 專屬 repair、以及共享最後 pivotal edge。
共同出口不要求 P=Q；例如 P={a,e}、Q={b,e} 也可以，只要 {a,b} 仍 silent。

## 2. disk dual 上的零邊集

先 silent 刪去不影響 boundary relation 的枝塊，保留含 C5 的 2-connected block。
T4 全收也排除 boundary chords。令 G* 是固定 disk drawing 的 plane dual，z 是外面頂點；
五條 C5 邊在 dual 中成為 z 的五條依 cyclic order 排列的 incident edges。

把四色識別為 `F₂²`。對任意頂點賦色 c，定義 dual edge value

\[
\phi_c(e^*)=c(u)+c(v),\qquad e=uv.
\]

每個 facial walk 上的和 telescopes 為零，所以 φ_c 是 `F₂²`-flow；反過來，
plane dual flow 可沿 primal paths 積分成頂點賦色，固定一個根點顏色後唯一。
對 boundary word b，其五條外圈 dual edges 的 demand 是

\[
d_i=b_i+b_{i+1}\ne0,qquad \sum_i d_i=0. \tag{4}
\]

而 φ_c(e*)=0 恰等價於 primal edge e 的兩端同色。因此：

> **dual-flow 等價（紙面定理）**：𝓡_r 恰是所有滿足 boundary demand d(r)
> 的 dual flows 之零邊集裡，inclusion-minimal 的那些集合；只計非外圈 edges。

證明不把 flow 當 proper：零邊正是要刪掉才容許的 monochromatic primal edges。
若一個 flow 的零邊集 Z 包含於 D，它積分出的 coloring 在 G−D 上 proper；
反向由 G−D 的 coloring 取得 Z⊆D。取 inclusion-minimal Z 即與 (1) 相同。

相鄰 singleton patterns 可在同一色名下寫成只改一個 boundary vertex x 的顏色；
所以 d(p)、d(q) 只在 x 兩側的兩條**相鄰** outer-dual edges 不同，且兩座標加上
同一個非零元素。這把候選 A 精確改寫為下列 flow 命題：

> **待證 flow-repair intersection lemma**：對 plane dual 5-pole，若十個 C5 demands
> 中恰有上述相鄰的 p,q 沒有 nowhere-zero flow，則其 minimal zero-set families
> 滿足 (2) 的兩個方向與 (3)。

這個 lemma 會直接證候選 A，不需假定 p、q fibers 共用 coloring。
目前尚未證；線性 flow 空間本身也不能省略 plane dual 5-pole 的 cyclic embedding 條件。

## 3. 五個 disk representatives 的 repair 結構

新 checker 從既有 5×1,024 張完整 relation tables 反向抽取 𝓡_p、𝓡_q。
五個 representatives 全部有同一形式：

- 每側有 9 個 minimal repairs，而且全是單邊集合。
- 兩族共有 8 個單邊 repairs。
- 每族另有 1 個專屬單邊 repair。
- 因此 (2) 兩側由兩條私有邊給出，(3) 由任一共同邊給出。

這與上一報告「兩個唯一 retained obstructions，各 9 邊、共享 8 邊」完全對偶，
但 checker 是從全部 subset relation table 重新計算 repairs，沒有把 obstruction 結論硬編碼。
五位置仍只是同一 D5 orbit 的封存代表，不提升成一般 flow lemma。

## 4. 平面但非 disk-cofacial 的精確反例

以下控制保留 boundary C5=(0,1,2,3,4)。取兩組互不相交的內點與非外圈邊

\[
\begin{aligned}
A_0={}&\{05,06,15,25,36,46,56\},\\
A_1={}&\{07,17,18,28,38,47,78\}.
\end{aligned}
\]

對 singleton-0 pattern `(0,1,2,1,2)`，把三個同色類
`{0},{1,3},{2,4}` 各縮成一點後，C5∪A₀ 變成 K5；因此它只拒絕 singleton-0，
且刪 A₀ 任一邊便修復。對 singleton-1 pattern `(0,1,2,0,2)`，
C5∪A₁ 同理，縮約類為 `{0,3},{1},{2,4}`，只拒絕 singleton-1。

這裡「只拒絕」另可直接核對，不靠 K5 推論：在 A₀ 中，內點 5、6 的可用色 lists
分別是四色集扣掉 boundary triples `{b₀,b₁,b₂}`、`{b₀,b₃,b₄}`，且 5、6 必須異色。
兩 lists 無法選異色 iff 都是同一 singleton；C5 properness 迫使此時
`b₃=b₁,b₄=b₂`，恰是 singleton-0 orbit。A₁ 對 triples
`{b₀,b₁,b₄}`、`{b₁,b₂,b₃}` 同理。K5−e 可四色且 boundary triangle 用三個異色，
故任一非外圈邊確為對應 pattern 的單邊 repair。

兩個 gadget 只共用 boundary，故聯集 G 的 relation 是兩 relation 的交集：

\[
\Sigma(G)=\Omega\setminus\{p_0,p_1\}.
\]

兩 gadget 的 disk face lists（省略共同 outer C5）可取
`064,056,015,125,2365,346` 與 `074,017,128,187,238,3478`；
因此把它們分置 C5 兩側便得到 G 的 sphere drawing。可是 A₀、A₁ 的 repairs 完全不交，
所以 G 沒有共同出口：

\[
W(G)=\{\Omega\setminus\{p_0\},\Omega\setminus\{p_1\}\}.
\]

它不能把同一 C5 畫成 disk boundary。加新頂點 9 並連到 0,…,4 後，圖中有明確
K₃,₃ subdivision，兩側 branch sets 為 `{2,3,4}` 與 `{6,8,9}`，九條 paths 為

```
2-5-6, 2-8,   2-9,
3-6,   3-8,   3-9,
4-6,   4-7-8, 4-9.
```

內部 vertices 5、7 各只出現一次。若 C5 能作同一 face，把 apex 放進該 face
並連五條 spoke 應仍平面，與此 K₃,₃ subdivision 矛盾。

checker 對控制的 16,384 個非外圈邊子集，以 compatible-assignment intersection
及獨立完整內點賦色加 subset OR 交叉核對；root 與 14 個單刪圖另以全部 240 個
boundary rows 回溯重驗。結果是 root 唯一 silent 狀態、兩族各 7 個互斥單邊 repairs，
與上述紙面構造一致。

這排除任何只用 relation、單調性、一般平面性或抽象線性空間的證明；
正確論證必須使用「五條 boundary dual edges 同繞 z 排列」的 disk 5-pole 結構。

## 5. 產物、驗證與下一步

- [repair checker](../scripts/c5_weak_flow_repairs.py)
- [逐項證書](../artifacts/c5_weak_flow_repairs/observations.json)

```bash
uv run --with networkx==3.5 python scripts/c5_weak_flow_repairs.py --check
uv run --with networkx==3.5 python scripts/c5_weak_critical_cores.py --check
python scripts/c5_weak_candidates.py --check
python scripts/c5_weak_quotient.py --check
lake build
git diff --check
```

驗證通過：兩個新 checker 與 candidate／quotient checker 逐 byte 重播、
`lake build`（8,820 jobs，僅既有 lint）、142 個本地文件連結與 whitespace 檢查。

下一個窄問題不再是任意 minimal obstructions 的圖形猜測，而是 §2 的 plane-dual lemma。
先證 (2) 的一側即可：若每個 minimal p-zero-set 都包含某個 q-zero-set，利用兩個 demands
只差 z 上相鄰兩條 edges，能否以 flow symmetric difference 造出第三個缺失 demand，
與其已知 nowhere-zero flow 矛盾。若這一步失敗，應保存最小 5-pole abstract flow control，
並檢查它是否違反 cyclic planarity；不擴大一般圖枚舉。
