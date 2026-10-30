# 計數錐與跨 split 手術提案的獨立驗證

2026-10-29。核對「四個突破點」中的第 4 項。基準為 `4476049`；本頁是提案驗證，
不改 [LOCK-NO-GAIN](../counting/ck_d_lock_comparison.md) 的原裁決。適用資料、同源與完整接口前提
仍以原報告為準。

結論：計數與手術確實是可用工具，但提案中的單純非負邊際式沒有超過 D；補成標準
block-count 錐後，C5 的 932 仍有明確整數可行證書。手術可精確更新已指定原圖上的
合法交換，卻尚未提供由 Ck 邊界分割決定後繼的有限狀態定理。

**同日續進：** [共同切口與完整分量反例](four_color_counts_surgery_continuation.md)
以共同側別／側內 noncrossing 排除一個通過 B5 及全部交換的具名 932 非 disk 模型；
另在真 disk 證三份全部具名頂點分割仍不能迭代，純 boundary 規則四步可區分。
尚未排除一般平面 932，不改本頁停止裁決。

## 1. 只有非負邊際，沒有新增限制

固定非空 D 一致集合 B。對每個 c∈B、split θ，令
`P_B(c,θ)={π : O(c,θ,π)⊆B}`，並給任意正數 n(c)。若所加限制只有

\[
n(c)=\sum_{\pi\in P_B(c,\theta)}w(c,\theta,\pi),\qquad w\ge0,
\]

則選一份 `π*(c,θ)∈P_B(c,θ)`，把該座標設為 n(c)，其餘設 0，即滿足全部限制。
反之，n(c)>0 與此式迫使 `P_B(c,θ)` 非空。因此它在支援層恰好等價於 D，
而且不限制 B 內任意正的計數比例。若連 `orbit⊆B` 都未要求，限制更弱。

這是一般有限域的紙面推導。新 [checker](../../../../scripts/four_color_counts_cone_verification.py)
另對 C5 的全部 153 份非空 D 一致集合，用故意不均勻的 `n(c)=index(c)+1`
產出權重，逐一核對 3,090 條邊際等式。

非平凡計數錐還需要交換雙射帶來的**不同 boundary 列之間的權重等式**。
[Dvořák–Lidický §1.2–2](https://arxiv.org/pdf/1907.04066v2#page=4)
以 noncrossing signed matching S 記錄 dual 雙色路徑。對相容的 precolorings，
固定 S 的延伸數由交換雙射相等，故用同一個 y(S) 滿足所有
`x(ψ)=Σ_{S compatible with (ψ,i,j)} y(S)`，而非每個 `(ψ,i,j)` 任選權重。
這是既有 block-count 層，不能把任意邊際重新命名成這個錐。

文獻敘述也須收窄：[Steinberger 導言第 4 頁](https://arxiv.org/pdf/0905.0043#page=4)
區分原 RSST 的 633 構形集與另提的 591 替代集；前者未用 block-count，後者才包含
這類構形。因此不能把原集內一般 C-可約但非布林 D 的構形都說成被 block-count 排除。

## 2. 標準 B5 也容許 932：明確可行證書

以 `ψ∈{1,2,3}^5` 為三種非零字母各出現奇數次的 60 個 parity words。
從基準色 0 逐步 XOR 積分成 primal boundary b，定義

\[
x(\psi)=\begin{cases}1&b\text{ 恰用四色},\\0&b\text{ 恰用三色}.\end{cases}
\]

其 primal 色型支援就是 932 的五個 T4 型。對 signature 的每個 pair `(a,b,s)`，
相容條件為：pair 全部覆蓋 ψ 的所選兩色位置，且 `ψ(a)=ψ(b) ⇔ s=−1`。
以下十份 signatures 設共同權重 y=1，其餘 51 份全部設 0；位置編號 0–4：

```text
{(0,2,+)}        {(0,3,+)}        {(1,3,+)}
{(1,4,+)}        {(2,4,+)}
{(0,3,−),(1,2,+)}  {(0,1,+),(2,4,−)}
{(0,4,+),(1,3,−)}  {(0,2,−),(3,4,+)}
{(1,4,−),(2,3,+)}
```

checker 獨立列舉全部 61 份 partial noncrossing signed matchings，對 60 words × 3
雙色對的 **180 條標準錐等式**逐條核對成立。每條正值等式恰有一份上述 signature；
每條零值等式皆無。逐一刪掉十個正權重的負控制均破壞等式。
這裡的 x 是抽象計數向量，沒有聲稱存在以它為延伸計數的平面 disk。

因此，即使把第 1 節修正為標準 block-count 錐，也不能靠這層排除 932。
[原文 Theorem 5、Lemma 6–7](https://arxiv.org/pdf/1907.04066v2#page=5)
說明 B5 的例外 ray 與此來源缺口；本次只讀並核對所引段落，不聲稱重播該文完整計算，
也不把其導言採用的 4CT 當成本 checker 前提。

## 3. 唯一 pairing 與 XOR 的前提

對已指定的 plane near-cubic 圖，除了特殊邊界頂點外皆三度；一份實際 proper
Tait 三邊染色在每個內點各用三色。刪特殊頂點、保留帶標號半邊後，每個雙色 system
的內點度數 2、有效 boundary terminal 度數 1，因此分量是路徑或閉圈；路徑唯一配對
其兩個 terminals。平面嵌入再保證 noncrossing。任意頂點四色圖的 primal 雙色分量
則可能分叉，不能不經近三角化／dual 轉換就當成 matching。

三個完整原邊集合確有 `F23 △ F13=F12`，但這是逐條原邊的色型恆等式。
投影成三個 boundary pairings 後，原邊身份與內部切開方式已丟失；此恆等式
不能直接用來推導三份抽象 boundary 分割同源可實現。

## 4. 已證的手術，需要哪些輸入

[KempeSurgery.lean](../../../../Math/KempeSurgery.lean) 不是 C5 專用：頂點型別任意，
不需平面性。`pairGraph_swap_mixed`（297 行）在下列前提證精確等式：

- 同一原圖 G 與一份 proper 染色 c；
- 指定 S 是 `{a,b}` 的 Kempe set（包含於該兩色頂點，且對該兩色鄰接封閉）；
- a、b、d 互異。

目標 `{a,d}` 圖恰為 `retained G c a d S ⊔ stars G c b d S`。
`mixed_reachable_iff_quotient`（331 行）再用 retained **切開後**的完整分量與新增星邊，
精確計算目標連通性。29–94 行的 quotient 引理本身只證兩張指定圖聯集的連通性。
它沒有從舊 boundary pairing 自動生成 retained 分量、合法 S 或 stars。

[既有 cut-interface 報告](../../../reference/c5/c5_cut_interfaces.md) 已有直接負控制：同一 Errera disk、
同一字面 boundary、同一三組 boundary pairing、同一 cycle counts 的四份染色，
對同一 `Comp_BC(0)` 選取規則，目標 mixed pairing 與相容性不同。完整切開接口可
正確預測，粗摘要無法決定。這次實際重播全部 196 transitions × 3 systems = 588 次，
且四份來源／十條歷史與三個過時 component 拒絕控制皆通過。

所以「同一完整染色與合法 action 決定後繼」成立；「三份 Ck 分割決定後繼」仍未證，
且上述粗版本已被反例否定。把此工具接到消元仍須定義能從當前 state 生成下一步
切開接口的資料，證明同源閉合，再給 D／block-count 留下而新條件排空的具名見證。

## 5. Lean 範圍與本次重播

`C5ParityWord.lean` 的 `fiber_card`、`extensionCount_of_edgeWord` 證四對一與延伸數
的色名對稱；`IsParityWord` 明確是 `Fin 5`。一般 Ck 要把奇偶條件改成三種字母的次數
皆與 k 同奇偶。此檔未形式化 dual graph 或一般 Ck 計數錐。
`C5Counts.lean` 第 8–13 行明說只做十個數的整數代數；
`ofCoefficients_chordTotalConst` 以給定係數形狀為前提，
`all_chords_positive` 另要求 chord-total identity、`y≥0`、support 位於一條 chord
與指定 `x_e>0`。沒有一般平面來源的非負計數錐 membership 定理。

本次執行成功：

```bash
python3 scripts/four_color_counts_cone_verification.py --out audits/2026-10-29-four-fronts-verification-4476049/counts-cone.json
.venv/bin/python scripts/c5_cut_interfaces.py --check
lake env lean Math/C5CountsAudit.lean
lake env lean Math/KempeSurgeryAudit.lean
```

兩份 Lean audit 全部只列 `propext / Classical.choice / Quot.sound`（或無公理），
沒有 `sorryAx`。這驗證既有定理，不代表新增 Ck 橋接形式化。
新固定域證據見 [counts-cone.json](../../../../audits/2026-10-29-four-fronts-verification-4476049/counts-cone.json)。
原單 split LOCK-NO-GAIN 與一般 932／4CT 的 OPEN 邊界保持不變。
